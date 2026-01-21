import json
import logging
import os
from pathlib import Path
from typing import List, Tuple, Union, Dict

from Bio.PDB import PDBParser
from Bio.PDB.Residue import Residue
from pydantic import BaseModel, ConfigDict, Field, model_validator

from viennaptm.utils.error_handling import raise_with_logging_error
from viennaptm.utils.fixtures import ViennaPTMFixtures

logger = logging.getLogger(__name__)


class AddBranch(BaseModel):
    """
    Definition of a application branch for residue transformation.

    An :class:`AddBranch` describes how a specific part (branch) of a residue
    should be modified. It specifies anchor atoms used for geometric alignment,
    optional weights for the alignment, and atoms to be added from a template
    residue.

    Each branch is applied independently, allowing complex modifications to be
    decomposed into multiple localized transformations.

    :ivar anchor_atoms: Atom names defining the alignment reference.
    :vartype anchor_atoms: list[str]

    :ivar weights: Weights applied to anchor atoms during alignment.
                   If empty, all anchor atoms are weighted equally.
    :vartype weights: list[float]

    :ivar add_atoms: Atom names to be added from the template residue.
    :vartype add_atoms: list[str]

    Note:
    If no weights are provided but anchor atoms are defined, equal weights
    are automatically assigned during validation.
    """

    ### TODO create alignment class for anchor and weights
    # atoms that define the overlay, i.e. the orientation
    anchor_atoms: List[str] = Field(default_factory=list)

    # not all atoms are equally important, hence they may contribute
    # do a varying extent (this needs to be optimized manually for
    # new modifications)
    weights: List[float] = Field(default_factory=list)

    # atoms to be added (removal happens via the mapping in atom pairs)
    add_atoms: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_branch(self):
        """
        Validate anchor atom and weight consistency.

        Ensures that the number of weights matches the number of anchor atoms.
        If no weights are provided, equal weights are assigned automatically.

        :raises ValueError:
            If the number of weights does not match the number of anchor atoms.
        """

        # if weights are specified, we need to ensure that we have the
        # right number (one per anchor atom)
        if self.weights:
            if len(self.weights) != len(self.anchor_atoms):
                raise_with_logging_error(f"For a branch, the number of anchor atoms {len(self.anchor_atoms)} does not equal the number of atoms {len(self.weights)}.",
                                         logger,
                                         ValueError)

        # if no weights are specified, we can assume all anchor atoms are equally important
        if len(self.weights) == 0 and len(self.anchor_atoms) > 0:
            self.weights = [1.0 for _ in range(len(self.anchor_atoms))]
            logger.warning(f"No weights provided for {len(self.anchor_atoms)} atoms, assuming they are equally important.")

        return self


class Modification(BaseModel):
    """
    Definition of a residue application.

    A :class:`Modification` specifies how an original residue is transformed
    into a modified residue. It includes atom mappings between the two residue
    states and one or more application branches that describe how atoms are
    added and aligned.

    :ivar residue_original_abbreviation: Abbreviation of the original residue.
    :vartype residue_original_abbreviation: str

    :ivar residue_modified_abbreviation: Abbreviation of the modified residue.
    :vartype residue_modified_abbreviation: str

    :ivar atom_mapping: Mapping between original and modified atom names.
                        Each entry is a tuple ``(original, modified)`` where
                        either element may be ``None`` to indicate deletion
                        or addition.
    :vartype atom_mapping: list[tuple[str | None, str | None]]

    :ivar add_branches: Branches defining how atoms are geometrically added.
    :vartype add_branches: list[AddBranch]

    Note:
        Atom deletions and renaming are handled exclusively via
        ``atom_mapping``; branches only describe atom additions.
    """


    residue_original_abbreviation: str
    residue_modified_abbreviation: str

    # contains a list of the form [('N', 'N'), ...] which maps the original residue's atom names
    # to the modified residue's; if an atom does not exist in one of the end-states, it is set to None
    # for example, atoms that need to be deleted during application, are marked as None
    atom_mapping: List[Tuple[Union[str, None], Union[str, None]]] = Field(default_factory=list)
    logger.debug(f"List of atoms mapped: {atom_mapping}")

    # each AddBranch contains information on how to modify _one_ part (or branch) of the original
    # residue into the target, modified PTM; for most modifications, only one branch is needed, but
    # this setup allows to modify the original residues in different regions without a need to
    # 'truncate' back all the way to last common atom
    add_branches: List[AddBranch] = Field(default_factory=list)
    logger.debug(f"List of added branches: {add_branches}")

    # TODO: add actual modified names for PTMs (should be part of the server files)
    model_config = ConfigDict(extra="forbid")


class ModificationLibrary(BaseModel):
    """
    Container and loader for residue modifications and template structures.

    The :class:`ModificationLibrary` loads application definitions from a JSON
    library file and associates them with minimized :class:`Biopython PDB template structure`.
    It provides indexed access to modifications and utilities for loading
    template residues.

    :ivar modifications: List of available residue modifications.
    :vartype modifications: list[Modification]

    :ivar target_templates: Mapping of residue abbreviations to PDB file paths.
    :vartype target_templates: dict[str, str]

    :ivar library_version: Version identifier of the loaded library.
    :vartype library_version: str or None
    """

    modifications: List[Modification] = Field(default_factory=list)
    target_templates: Dict[str, str] = Field(default_factory=dict)
    library_version: str = None
    model_config = ConfigDict(extra="forbid")

    def __init__(self, library_path: Union[str, Path] = None, pdbs_minimized: Union[str, Path] = None):
        BaseModel.__init__(self)
        """
        Load a :class:`ModificationLibrary` and associated template PDB files.

        If no paths are provided, the latest installed default application
        library and minimized PDB directory are loaded automatically.

        :param library_path: Path to the JSON application library file.
        :type library_path: str or pathlib.Path or None
        
        :param pdbs_minimized: Directory containing minimized PDB templates.
        :type pdbs_minimized: str or pathlib.Path or None

        :raises FileNotFoundError:
            If the PDB directory does not exist or contains no PDB files.
        :raises ValueError:
            If library parsing fails or required templates are missing.
        """

        fixtures = ViennaPTMFixtures()

        # if not set, assume, that the default (i.e. latest installed) PTM library and the latest PDBs are to be used
        if not library_path or not pdbs_minimized:
            self.library_version = fixtures.LATEST_PTMS_VERSION_DATE
            library_path = fixtures.LATEST_PTMS_LIBRARY_PATH
            pdbs_minimized = fixtures.LATEST_PTMS_PDBS_DIR_PATH
            logger.info(f"No modifications library or PDB directory specified, loading current default: {fixtures.LATEST_PTMS_VERSION_DATE}")
        else:
            self.library_version = "custom"
            logger.info(f"Using custom library ({library_path}) and PDB directory ({pdbs_minimized}).")

        # load application library, make sure that minimized PDBs are available and store the absolute paths
        # in dictionary of the form: {"MOD1": "/full/path/MOD1.pdb", ...}
        with open(library_path, 'r') as f:
            library = json.load(f)
        if not os.path.isdir(pdbs_minimized):
            raise_with_logging_error(f"The specified PDB directory does not exist: {pdbs_minimized}",
                                     logger,
                                     FileNotFoundError)
        minimized_pdb_files = os.listdir(pdbs_minimized)
        minimized_pdb_files = {x for x in minimized_pdb_files if x.lower().endswith(fixtures.PDB_ENDING)}
        if len(minimized_pdb_files) == 0:
            raise_with_logging_error(f"The specified PDB directory does not contain any PDB files: {pdbs_minimized}",
                                     logger,
                                     FileNotFoundError)
        self.target_templates = {f[:-4]: os.path.join(pdbs_minimized, f) for f in minimized_pdb_files if f.endswith(".pdb")}

        # parse application file and report on loading
        for key in library.keys():
            original, modified = key.split('_')
            self.modifications.append(Modification(residue_original_abbreviation=original,
                                                   residue_modified_abbreviation=modified,
                                                   **library[key]))
            logger.debug(f"Modification {original}->{modified} added.")
        logger.info(f"Loaded {len(self.modifications)} modifications and indexed {len(minimized_pdb_files)} PDB files for library {fixtures.LATEST_PTMS_VERSION_DATE}.")

    def __getitem__(self, index):
        """
        Retrieve a application by index or residue pair.

        :param index: Either an integer index or a tuple
                        ``(original_abbreviation, modified_abbreviation)``.
        :type index: int or tuple[str, str]

        :return: Matching application.
        :rtype: Modification

        :raises IndexError: If no matching application is found.
        """

        if isinstance(index, int):
            return self.modifications[index]
        elif isinstance(index, tuple):
            # assume the first element is the original residue's abbreviation and the
            # second element the modified one's
            original, modified = index
            for mod in self.modifications:
                if mod.residue_original_abbreviation == original and mod.residue_modified_abbreviation == modified:
                    return mod
        raise IndexError(f"Modification {index} not found in library.")

    def load_residue_from_pdb(self, target_abbreviation: str) -> Residue:
        """
        Load a template residue from a minimized PDB file.

        The PDB file must contain exactly one residue whose name matches
        the requested target abbreviation.

        :param target_abbreviation: Residue abbreviation to load.
        :type target_abbreviation: str

        :return: Template residue.
        :rtype: Residue

        :raises ValueError:
            If the PDB file does not contain exactly one matching residue.
        """

        target_template_path = self.target_templates[target_abbreviation]

        parser = PDBParser()
        structure = parser.get_structure(id=target_abbreviation, file=target_template_path)

        # this assumes, that the template PDB files contain exactly one residue
        residue = next(structure.get_residues())
        if residue.resname not in target_abbreviation:
            raise_with_logging_error(f"File {target_template_path} needs to contain exactly one residue entry for {target_abbreviation} with the residue name being part of the target name, abort.",
                                     logger, ValueError)
        return residue

    def __setitem__(self, index, value):
        logger.debug(f"Modification {self.modificationsp[index]} has value {value}.")
        """
        Replace a application at the specified index.

        :param index: Index of the application to replace.
        :type index: int

        :param value: New application.
        :type value: Modification
        """

        self.modifications[index] = value

    def __len__(self):
        logger.debug(f"Number of modifications: {len(self.modifications)}")
        """
        Return the number of available modifications.

        :return: Number of modifications.
        :rtype: int
        """

        return len(self.modifications)

    def __iter__(self):
        logger.debug(f"{self.modifications} has been iterated over.")
        """
        Iterate over available modifications.

        :return: Iterator over modifications.
        :rtype: iterator[Modification]
        """

        return iter(self.modifications)
