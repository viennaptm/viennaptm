import unittest
from io import StringIO
import sys
from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class TestModificationLog(unittest.TestCase):

    def setUp(self):
        self.annotated_structure = AnnotatedStructure("jj")
        self.modification = [60, "A", "V3H", "mod_name"]
        self.columns = ["residue_number", "chain_identifier",
                        "target_abbreviation", "modification_name"]

        # adds modifications, df has now 1 row
        self.annotated_structure.add_to_modification_log(*self.modification)

    def test_if_dataframe_CONTAINS_required_columns(self):
        self.assertTrue(set(self.annotated_structure.modification_log.columns.to_list()) == set(self.columns))

    def test_if_dataframe_IS_NOT_empty(self):
        self.assertFalse(self.annotated_structure.modification_log.empty)

    def test_if_dataframe_CONTAINS_added_row(self):
        self.assertTrue(set(self.annotated_structure.modification_log.values[-1].tolist()) == set(self.modification))

    def test_if_row_is_deleted(self):
        modification2 = [50, "A", "V3H", "mod_name"]
        modification3 = [50, "B", "V3H", "mod_name"]

        # adds more modifications, df has now 3 rows
        self.annotated_structure.add_to_modification_log(*modification2)
        self.annotated_structure.add_to_modification_log(*modification3)
        self.assertTrue(len(self.annotated_structure.get_log()), 3)

        # deletes row with given residue and chain_identifier, df now has 1 row again
        self.annotated_structure.delete_log_entry(60, "A")
        self.assertTrue(len(self.annotated_structure.get_log()), 1)

        # checks whether correct row has been deleted
        deleted_row = self.annotated_structure.modification_log.loc[(self.annotated_structure.modification_log['residue_number'] == 60) &
                                                                    (self.annotated_structure.modification_log['chain_identifier'] == "A")]
        not_deleted_row = self.annotated_structure.modification_log.loc[(self.annotated_structure.modification_log['residue_number'] == 50) &
                                                                    (self.annotated_structure.modification_log['chain_identifier'] == "A")]
        self.assertTrue(deleted_row.empty)
        self.assertFalse(not_deleted_row.empty)

    def test_printing(self):
        # Make StringIO
        temp_out = StringIO()

        # Redirect stdout
        sys.stdout = temp_out

        # Call function
        self.annotated_structure.print_log()

        # Reset redirect
        sys.stdout = sys.__stdout__

        self.assertIn("residue_number", temp_out.getvalue())