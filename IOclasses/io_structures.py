import os
import shutil
from Bio.PDB import PDBParser, PDBList

class IO_structure:
    """Class to handle structure input files"""
    def __init__(self, inp):
        if not isinstance(inp, str):
            raise AttributeError("Currently, only PDB URLs and file paths are supported.")

        # load the file
        parser = PDBParser()
        if os.path.isfile(inp):
            _structure = parser.get_structure(id=os.path.basename(inp), file=inp)
        else:
            downloader = PDBList()
            path = downloader.retrieve_pdb_file(pdb_code=inp)
            _structure = parser.get_structure(id=os.path.basename(path), file=path)
            shutil.rmtree(os.path.dirname(path))

        self._structure = _structure

    def get_structure(self):
        return self._structure
