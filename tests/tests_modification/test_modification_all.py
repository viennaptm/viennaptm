import logging
import unittest
from copy import deepcopy
from typing import List

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from tests.file_paths import UNITTEST_PATH_1VII_PDB
from viennaptm.modification.application.modifier import Modifier
from viennaptm.utils.paths import attach_root_path

from viennaptm.utils.unit_test_utils import get_coords_for_atom

logger = logging.getLogger(__name__)


class Test_Modification_All(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _struc_io = AnnotatedStructure("dd")
        cls._structure_ori = _struc_io.from_pdb(path=attach_root_path(UNITTEST_PATH_1VII_PDB))

    def setUp(self):
        self._structure = deepcopy(self._structure_ori)
        self._modifier = Modifier()

    def _test_mod(self,
                  residue_number: int,
                  target_abbreviation: str,
                  internal_residue_number: int,
                  atom_name: str,
                  coordinates: List[float]):
        modified_structure = self._modifier.apply_modification(structure=self._structure,
                                                               chain_identifier='A',
                                                               residue_number=residue_number,
                                                               target_abbreviation=target_abbreviation)
        modified_residue = list(modified_structure.get_residues())[internal_residue_number]
        self.assertEquals(modified_residue.get_resname(), target_abbreviation)
        self.assertListEqual(get_coords_for_atom(modified_residue, atom_name),
                             coordinates)

    def test_ARG_GSA(self):
        self._test_mod(residue_number=55, target_abbreviation="GSA",
                       internal_residue_number=14, atom_name="OE",
                       coordinates=[-1.729, -3.245, -3.182])
