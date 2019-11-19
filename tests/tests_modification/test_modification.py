import unittest

from modification.modifier import Modifier
from tests.file_paths import UNITTEST_PATH_1VII_PDB
from utils.paths import attach_root_path
from IOclasses.iostructures import IOStructure


class Test_Modification(unittest.TestCase):

    def setUp(self):
        self._struc_io = IOStructure()
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)

    def test_apply_modifications(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb_file(path=self._1vii_PDB_path)

        # initialize modifier with most recent internal modification database
        modifier = Modifier(structure=structure)

        # apply a modification
        modifier.apply_modification(chain_identifier='A',
                                    residue_number=50,
                                    target_abbreviation="V3H")
