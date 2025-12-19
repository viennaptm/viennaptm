import json
import logging
import os
from pathlib import Path
from typing import List, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

from viennaptm.utils.error_handling import raise_with_logging_error
from viennaptm.utils.fixtures import ViennaPTMFixtures


logger = logging.getLogger(__name__)


class AddBranch(BaseModel):
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
    residue_original_abbreviation: str
    residue_modified_abbreviation: str

    # contains a list of the form [('N', 'N'), ...] which maps the original residue's atom names
    # to the modified residue's; if an atom does not exist in one of the end-states, it is set to None
    # for example, atoms that need to be deleted during modification, are marked as None
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
    modifications: List[Modification] = Field(default_factory=list)
    library_version: str = None
    model_config = ConfigDict(extra="forbid")

    def __init__(self, library_path: Union[str, Path] = None, pdbs_minimized: Union[str, Path] = None):
        BaseModel.__init__(self)

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

        # load modification library, make sure that minimized PDBs are available
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

        # parse modification file and report on loading
        for key in library.keys():
            original, modified = key.split('_')
            self.modifications.append(Modification(residue_original_abbreviation=original,
                                                   residue_modified_abbreviation=modified,
                                                   **library[key]))
            logger.debug(f"Modification {original}->{modified} added.")
        logger.info(f"Loaded {len(self.modifications)} modifications and indexed {len(minimized_pdb_files)} PDB files for library {fixtures.LATEST_PTMS_VERSION_DATE}.")

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.modifications[index]
        elif isinstance(index, tuple):
            # assume the first element is the original residue's abbreviation and the
            # second element the modified one's
            original, modified = index
            for mod in self.modifications:
                if mod.residue_original_abbreviation == original and mod.residue_modified_abbreviation == modified:
                    return mod
        raise IndexError(f"Index {index} is out of range.")


    def __setitem__(self, index, value):
        logger.debug(f"Modification {self.modificationsp[index]} has value {value}.")
        self.modifications[index] = value

    def __len__(self):
        logger.debug(f"Number of modifications: {len(self.modifications)}")
        return len(self.modifications)

    def __iter__(self):
        logger.debug(f"{self.modifications} has been iterated over.")
        return iter(self.modifications)
