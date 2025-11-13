import unittest

from tests.file_paths import UNITTEST_PATH_1VII_PDB
from viennaptm.utils.paths import attach_root_path
from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class Test_IOStructure(unittest.TestCase):

    def setUp(self):
        self._struc_io = AnnotatedStructure("dd")
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)

    def test_loading_localPDB(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb(path=self._1vii_PDB_path)
        self.assertTrue(isinstance(structure, AnnotatedStructure))
        self.assertEqual('A', list(structure.get_chains())[0].get_id())
        self.assertEqual(len(structure.get_list()[0].get_list()[0].get_list()), 36)

    def test_loading_PDBdb(self):
        # load PDB structure from database
        structure = self._struc_io.from_pdb_db(identifier="1vii")
        self.assertTrue(isinstance(structure, AnnotatedStructure))
        self.assertEqual('A', list(structure.get_chains())[0].get_id())
        self.assertEqual(len(structure.get_list()[0].get_list()[0].get_list()), 36)
