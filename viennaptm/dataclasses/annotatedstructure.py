import os
import shutil
import tempfile

from Bio.PDB import PDBIO, PDBParser, PDBList
from Bio.PDB.Structure import Structure
from viennaptm.modification.modification.modification_report import ModificationReport


class AnnotatedStructure(Structure):
    """The AnnotatedStructure class extends the original structure."""
    ##TODO modification_history
    ##TODO more to come


    def __init__(self, id):
        """Initialize the class."""
        Structure.__init__(self, id)

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

    def generate_report(self):   ###TODO?
        report = ModificationReport()
        return report.__add__(self)