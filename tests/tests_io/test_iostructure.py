import unittest

from IOclasses.iostructures import IOStructure


class Test_IOStructure(unittest.TestCase):

    def setUp(self):
        self._struc_io = IOStructure()

    def test_loading_localPDB(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb_file(path="../tests_data/1vii.pdb")
        self.assertEqual('A', list(structure.get_chains())[0].get_id())
        self.assertEqual(len(structure.get_list()[0].get_list()[0].get_list()), 36)

    def test_loading_PDBdb(self):
        # load PDB structure from database
        struc_io = IOStructure()
        structure = self._struc_io.from_pdb_db(identifier="1vii")
        self.assertEqual('A', list(structure.get_chains())[0].get_id())
        self.assertEqual(len(structure.get_list()[0].get_list()[0].get_list()), 36)

