from IOclasses.io_modlibrary import IO_ModLibrary
from modification.mod_library import ModLibrary
from modification.modification import Modification
from Bio.PDB.Structure import Structure

class Modifier:
    """Class that actually applies any number of modifications in a modification library to a structure"""

    def __init__(self, structure: Structure, library = None):
        # if no library is specified, load the internal default
        if library is None:
            io_lib = IO_ModLibrary()
            library = io_lib.load_database(path=None)

        self._library = library
        self._structure = structure

    def apply_modification(self, mods):
        pass

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

mods = [{"residue": {"model": None, "chain": None, "number": 1},
         "modification_name": "PHOS",
         "target_abbreviation": None},
        {"residue": {"model": None, "chain": None, "number": 10},
         "modification_name": "PHOS",
         "target_abbreviation": None}]
