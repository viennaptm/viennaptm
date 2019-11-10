import os
import tempfile
import shutil
from Bio.PDB import PDBParser, PDBList


class IOStructure:
    """Class to handle structure input files."""

    def __init__(self):
        pass

    @staticmethod
    def from_pdb_file(path):
        if not isinstance(path, str):
            raise AttributeError("Parameter path required to be a path (as string) to a local PDB file.")

        # load the file and return structure
        parser = PDBParser()
        return parser.get_structure(id=os.path.basename(path), file=path)

    @staticmethod
    def from_pdb_db(identifier):
        if not isinstance(identifier, str) or len(identifier) != 4:
            raise AttributeError("Parameter identifier required to be a string of length four.")

        # download the file; store it in a local copy (to provide identical results to "from_pdb_file()"
        parser = PDBParser()
        downloader = PDBList()
        tmp_folder = tempfile.mkdtemp()
        path = downloader.retrieve_pdb_file(pdb_code=identifier, pdir=tmp_folder, file_format="pdb")

        # check whether file exists (success) or not
        if not os.path.isfile(path):
            raise Exception("Could not retrieve PDB file with identifier specified.")

        # load the file, clean it up and return structure
        structure = parser.get_structure(id=os.path.basename(path), file=path)
        shutil.rmtree(os.path.dirname(path))
        return structure
