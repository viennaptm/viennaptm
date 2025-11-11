import unittest

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class TestModificationLog(unittest.TestCase):

    def setUp(self):
        self.annotated_structure = AnnotatedStructure("jj")
        self.modification = [60, "A", "V3H", "mod_name"]
        self.columns = ["residue_number", "chain_identifier", "target_abbreviation", "modification_name"]
        self.annotated_structure.add_to_modification_log(*self.modification)


    def test_if_dataframe_CONTAINS_required_columns(self):
        self.assertTrue(set(self.annotated_structure.modification_log.columns.to_list()) == set(self.columns))

    def test_if_dataframe_IS_NOT_empty(self):
        self.assertFalse(self.annotated_structure.modification_log.empty)

    def test_if_dataframe_CONTAINS_added_row(self):
        self.assertTrue(set(self.annotated_structure.modification_log.values[-1].tolist()) == set(self.modification))
