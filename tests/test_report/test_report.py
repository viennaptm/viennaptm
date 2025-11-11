import unittest
import pandas as pd

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.modification.modification.modifier import Modifier
from tests.file_paths import UNITTEST_PATH_1VII_PDB
from viennaptm.utils.paths import attach_root_path
from viennaptm.io.structures import IOStructure

class TestReport(unittest.TestCase):

    def setUp(self):
        self.annotated_structure = AnnotatedStructure("jj")
        self.modification = [50, "A", "V3H", "mod_name"]
        self.columns = ["residue_number", "chain_identifier", "target_abbreviation", "modification_name"]
        self.annotated_structure.add_to_modification_log(50, "A", "V3H", "mod_name")

 #   def test_if_dataframe_CONTAINS_required_columns(self):
 #       self.assertTrue(set(self.annotated_structure.modification_log.columns.to_list()) == set(self.columns))

#    def test_if_dataframe_IS_NOT_empty(self):
#        self.assertFalse(self.annotated_structure.modification_log.empty)

#    def test_if_dataframe_CONTAINS_added_row(self):
 #       self.assertTrue(set(self.annotated_structure.modification_log.values[-1].tolist()) == set(self.modification))
