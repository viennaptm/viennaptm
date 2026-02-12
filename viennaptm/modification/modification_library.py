import json
import logging
import os
from pathlib import Path
from typing import List, Tuple, Union, Dict, Optional

from Bio.PDB import PDBParser
from Bio.PDB.Residue import Residue
from pydantic import BaseModel, ConfigDict, Field, model_validator

from viennaptm.utils.error_handling import raise_with_logging_error
from viennaptm.utils.fixtures import ViennaPTMFixtures

logger = logging.getLogger(__name__)
fixtures = ViennaPTMFixtures()


class AddBranch(BaseModel):
    """
    Definition of an application branch for residue transformation.

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
    #       plan is to use another JSON in the "metadata" resource folder for this purpose
    model_config = ConfigDict(extra="forbid")


class ModificationLibraryMetadata(BaseModel):
    """
    Container for library metadata such as the date it was created.
    """
    date: Optional[str] = "undefined"
    custom_library: bool = False


class ModificationLibrary(BaseModel):
    """
    Container and loader for residue modifications and template structures.

    The :class:`ModificationLibrary` loads application definitions from a JSON
    library file and associates them with minimized :class:`Biopython PDB template structure`.
    It provides indexed access to modifications and utilities for loading
    template residues.

    :ivar modifications: List of available residue modifications.
    :vartype modifications: list[Modification]

    :ivar metadata: Metadata of the library.
    :vartype metadata: ModificationLibraryMetadata

    :ivar target_templates: Mapping of residue abbreviations to PDB file paths.
    :vartype target_templates: dict[str, str]
    """

    modifications: List[Modification] = Field(default_factory=list)
    metadata: ModificationLibraryMetadata = Field(default_factory=ModificationLibraryMetadata)
    target_templates: Dict[str, str] = Field(default_factory=dict)
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

        # if not set, assume, that the default (i.e. latest installed) PTM library and the latest PDBs are to be used
        if not library_path or not pdbs_minimized:
            library_path = fixtures.PTMS_LIBRARY_PATH
            pdbs_minimized = fixtures.PTMS_PDBS_DIR_PATH
            logger.info(f"No modifications library or PDB directory specified, loading current default.")
        else:
            self.metadata.custom_library = True
            logger.info(f"Using custom library ({library_path}) and PDB directory ({pdbs_minimized}).")

        # load modification information and paths to pre-minimized PDB files
        self._load_library(library_path)
        self._populate_minimized_PDBs(pdbs_minimized)

        logger.info(f"Modification library version: {self.metadata.date} (custom_library={self.metadata.custom_library})")
        logger.info(f"---> Comprised of {len(self.modifications)} modifications, indexed {len(self.target_templates)} PDB files.")

    def _load_library(self, library_path: Union[str, Path] = None):
        """
        Load a modification library from a JSON file.

        The JSON file must contain the top-level keys ``"metadata"`` and
        ``"modifications"``. Each entry in ``"modifications"`` must use the
        format ``"<original>_<modified>"`` (e.g., ``"SER_pSER"``) to define
        the residue conversion.

        :param library_path: Path to the JSON modification library file.
        :type library_path: str or pathlib.Path or None

        :raises KeyError: If required top-level keys are missing.
        :raises FileNotFoundError: If the specified file does not exist.
        :raises json.JSONDecodeError: If the file is not valid JSON.
        """

        # load application library from JSON (modifications and metadata
        with open(library_path, 'r') as f:
            library = json.load(f)

        # check if required keys are present
        required_keys = ["metadata", "modifications"]
        if [key for key in required_keys if key not in library]:
            raise_with_logging_error(message=f"The following keys need to be present on the top level of a valid modification library: [{', '.join(required_keys)}]",
                                     logger=logger,
                                     exception_type=KeyError)

        # parse metadata
        self.metadata = ModificationLibraryMetadata.model_validate(library["metadata"])

        # parse application file and report on loading
        for key in library["modifications"].keys():
            original, modified = key.split('_')
            self.modifications.append(Modification(residue_original_abbreviation=original,
                                                   residue_modified_abbreviation=modified,
                                                   **library["modifications"][key]))
            logger.debug(f"Modification {original}->{modified} added.")

    def _populate_minimized_PDBs(self, pdbs_minimized: Union[Path, str]):
        """
        Populate the internal template dictionary with minimized PDB files.

        The specified directory is scanned for PDB files (matching
        ``fixtures.PDB_ENDING``). Each valid file is stored in
        ``self.target_templates`` as a mapping from the filename (without
        extension) to its absolute path.

        Example structure::

            {
                "MOD1": "/full/path/MOD1.pdb",
                "MOD2": "/full/path/MOD2.pdb"
            }

        :param pdbs_minimized: Path to a directory containing minimized
                               PDB template files.
        :type pdbs_minimized: str or pathlib.Path

        :raises FileNotFoundError: If the directory does not exist.
        :raises FileNotFoundError: If no valid PDB files are found in the directory.
        """

        # make sure that minimized PDBs are available and store the absolute paths
        # in dictionary of the form: {"MOD1": "/full/path/MOD1.pdb", ...}
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
        self.target_templates = {f[:-4]: os.path.join(pdbs_minimized, f) for f in minimized_pdb_files if
                                 f.endswith(".pdb")}

    def __getitem__(self, index):
        """
        Retrieve an application by index or residue pair.

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
        """
        Replace an application at the specified index.

        :param index: Index of the application to replace.
        :type index: int

        :param value: New application.
        :type value: Modification
        """

        logger.debug(f"Modification {self.modificationsp[index]} has value {value}.")
        self.modifications[index] = value

    def __len__(self):
        """
        Return the number of available modifications.

        :return: Number of modifications.
        :rtype: int
        """

        logger.debug(f"Number of modifications: {len(self.modifications)}")
        return len(self.modifications)

    def __iter__(self):
        """
        Iterate over available modifications.

        :return: Iterator over modifications.
        :rtype: iterator[Modification]
        """

        logger.debug(f"{self.modifications} has been iterated over.")
        return iter(self.modifications)
