import unittest
from viennaptm.modification.modification_library import ModificationLibrary, Modification


class Test_Resources(unittest.TestCase):

    def test_library_loading(self):
        # load standard, internal database
        modifications = ModificationLibrary()

        # test instance of class Modification
        self.assertTrue(isinstance(modifications[0], Modification))
        self.assertTrue(isinstance(modifications["ARG", "RMN"], Modification))

        # test not a ptm
        with self.assertRaises(IndexError):
            _ = modifications["ARG", "RMB"]

        # test number of modifications
        with self.assertRaises(IndexError):
            _ = modifications[1250]

        # test right number of atom pairs and added branches
        self.assertEqual(len(modifications[99].add_branches), 1)
        self.assertEqual(len(modifications[99].atom_mapping), 11)

        self.assertEqual(len(modifications["VAL", "V3H"].add_branches), 1)
        self.assertEqual(len(modifications["VAL", "V3H"].atom_mapping), 11)
