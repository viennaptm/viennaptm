import os
import tempfile
import shutil
from Bio.PDB import PDBParser, PDBList, PDBIO
from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class IOStructure:
    """Class to handle structure input files."""

    def __init__(self):
        pass

    @staticmethod
    def from_pdb_file(path: str) -> AnnotatedStructure:
        if not isinstance(path, str):
            raise AttributeError("Parameter path required to be a path (as string) to a local PDB file.")

        # load the file and return structure
        parser = PDBParser()
        structure = parser.get_structure(id=os.path.basename(path), file=path)

        # Caution: __init__() of AnnotatedStructure is not executed! Manually add attributes!
        structure.__class__ = AnnotatedStructure
        structure._init_calls()
        return structure

    def from_pdb_db(self, identifier: str) -> AnnotatedStructure:
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
        structure = self.from_pdb_file(path=path)
        shutil.rmtree(os.path.dirname(path))
        return structure

    @staticmethod
    def to_pdb_file(structure: AnnotatedStructure, path: str) -> None:
        io = PDBIO()
        io.set_structure(structure)
        io.save(file=path)
