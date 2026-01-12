import os
import unittest
from viennaptm.modification.modification_library import ModificationLibrary, Modification


class Test_Resources(unittest.TestCase):

    def test_library_instructions_loading(self):
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
        self.assertEqual(len(modifications[99].atom_mapping), 14)

        self.assertEqual(len(modifications["VAL", "V3H"].add_branches), 1)
        self.assertEqual(len(modifications["VAL", "V3H"].atom_mapping), 11)

    def test_library_template_loading(self):
        # load standard, internal database
        modifications = ModificationLibrary()

        # check, that "target_templates" is a dictionary of the form: {"MOD1": "/full/path/MOD1.pkl", ...}
        templates = modifications.target_templates
        self.assertTrue(isinstance(templates, dict))
        self.assertTrue("T1P" in templates["T1P"])
        self.assertTrue(not "T2P" in templates["T1P"])

        # check, that PDB template file paths are correct
        self.assertEqual(os.path.getsize(templates["T1P"]), 1414)
        self.assertEqual(os.path.getsize(templates["T2P"]), 1335)
