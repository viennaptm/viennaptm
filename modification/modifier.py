from copy import deepcopy

from IOclasses.iomodlibrary import IOModLibrary
from Bio.PDB.Residue import Residue
from Bio.PDB.Structure import Structure
from modification.modification import Modification
from modification.modification_report import ModificationReport

class Modifier:
    """Class that actually applies any number of modifications in a modification library to a structure"""

    def __init__(self, structure: Structure, library=None):
        # if no library is specified, load the internal default
        if library is None:
            io_lib = IOModLibrary()
            library = io_lib.load_database(path=None)

        self._library = library
        self._original_structure = structure
        self._structure = deepcopy(structure)

    def _execute_modification(self, residue: Residue, modification: Modification) -> ModificationReport:
        pass

    def apply_modification(self, chain_identifier: str, residue_number: int,
                           target_abbreviation=None, modification_name=None) -> ModificationReport:

        # get residue from structure
        # note: this assumes that chain IDs are unique over all models
        residue = None
        for cur_residue in self._structure.get_residues():
            # get the full residue identifier, e.g. ("1vii.pdb", 0, 'A', (' ', 41, ' '))
            # this means (target identifier, model number, chain identifier, (hetero- or non-hetero residue, residue
            # number, insertion code))
            full_id = cur_residue.get_full_id()
            if full_id[2] == chain_identifier and full_id[3][1] == residue_number:
                residue = cur_residue
                break
        if residue is None:
            raise Exception("Could not find specified residue in specified chain.")

        # try to get modification from library
        modification = self._library.get_modification(initial_abbreviation=residue.get_resname(),
                                                      target_abbreviation=target_abbreviation,
                                                      modification_name=modification_name)

        # apply the modification
        return self._execute_modification(residue=residue, modification=modification)

    def reset_structure(self):
        self._structure = deepcopy(self._original_structure)

    @property
    def get_library(self):
        return self._library

    @get_library.setter
    def get_library(self, value):
        raise ValueError("Libraries cannot be changed explicitly after initialization.")

    @property
    def get_structure(self):
        return self._structure

    @get_structure.setter
    def get_structure(self, value):
        raise ValueError("Structures cannot be changed explicitly after initialization.")
