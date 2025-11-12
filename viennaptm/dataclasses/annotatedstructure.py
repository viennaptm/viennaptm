import os
import shutil
import tempfile
import pandas as pd

from Bio.PDB import PDBIO, PDBParser, PDBList
from Bio.PDB.Structure import Structure
from viennaptm.modification.modification.modification_report import ModificationReport


class AnnotatedStructure(Structure):
    """The AnnotatedStructure class extends the original structure."""

    def __init__(self, id):
        """Initialize the class."""
        Structure.__init__(self, id)
        self._init_calls()
        ###TODO add "atoms_added", "atoms_deleted" and "atoms_renamed"

    def _init_calls(self):
        self.modification_log = pd.DataFrame(columns=["residue_number", "chain_identifier",
                                                      "target_abbreviation", "modification_name",
                                                      "atoms_added", "atoms_deleted", "atoms_renamed"])

    def add_to_modification_log(self, residue_number: int, chain_identifier: str,
                                target_abbreviation: str, modification_name: str,
                                atoms_added: int, atoms_deleted: int, atoms_renamed: int):
        self.modification_log.loc[len(self.modification_log)] = [residue_number, chain_identifier,
                                                                 target_abbreviation, modification_name,
                                                                 atoms_added, atoms_deleted, atoms_renamed]
        ###TODO set modification input to user input

    def get_log(self) -> pd.DataFrame:
        return self.modification_log

    def print_log(self):
        # settings allow printing of long and wide dataframes
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', 1000)

        # removes index
        blankIndex = [''] * len(self.modification_log)
        self.modification_log.index = blankIndex

        # adds a line for better visibility
        print('\n')
        print(self.modification_log)

    def delete_log_entry(self, residue_number: int, chain_identifier: str,):
        self.modification_log.drop(self.modification_log[(self.modification_log["residue_number"] == residue_number)&
                                                         (self.modification_log["chain_identifier"] == chain_identifier)].index,
                                    inplace=True)

    @classmethod
    def from_pdb_db(cls, identifier: str):
        if not isinstance(identifier, str) or len(identifier) != 4:
            raise AttributeError("Parameter identifier required to be a string of length four.")

        # download the file; store it in a local copy (to provide identical results to "from_pdb_file()"
        downloader = PDBList()
        tmp_folder = tempfile.mkdtemp()
        path = downloader.retrieve_pdb_file(pdb_code=identifier, pdir=tmp_folder, file_format="pdb")

        # check whether file exists (success) or not
        if not os.path.isfile(path):
            raise Exception("Could not retrieve PDB file with identifier specified.")

        # load the file, clean it up and return structure
        annotated_structure = cls.from_pdb(path=path)
        shutil.rmtree(os.path.dirname(path))
        return annotated_structure

    @classmethod
    def from_pdb(cls, path: str):
        if not isinstance(path, str):
            raise AttributeError("Parameter path required to be a path (as string) to a local PDB file.")

        # load the file and return structure
        parser = PDBParser()
        return parser.get_structure(id=os.path.basename(path), file=path)

    def to_pdb(self, path: str) -> None:
        io = PDBIO()
        io.set_structure(self)
        io.save(file=path)
