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

        if len(modified_residue.get_resname()) == len(target_abbreviation):
            self.assertEqual(modified_residue.get_resname(), target_abbreviation)
        else:
            self.assertTrue(modified_residue.get_resname() in target_abbreviation)
        self.assertListEqual(get_coords_for_atom(modified_residue, atom_name),
                             coordinates)


    def test_ARG_RCI(self):
        self._test_mod(residue_number=55, target_abbreviation="RCI",
                       internal_residue_number=14, atom_name="NH2",
                       coordinates=[-2.718, -4.319, -5.115])

    def test_ARG_RSM(self):
        self._test_mod(residue_number=55, target_abbreviation="RSM",
                       internal_residue_number=14, atom_name="CT2",
                       coordinates=[-4.149, -4.28, -5.039])

    def test_ARG_RMS(self):
        self._test_mod(residue_number=55, target_abbreviation="RMS",
                       internal_residue_number=14, atom_name="CT1",
                       coordinates=[-2.074, -4.193, -0.409])

    def test_ARG_RAM(self):
        self._test_mod(residue_number=55, target_abbreviation="RAM",
                       internal_residue_number=14, atom_name="CT2",
                       coordinates=[-4.172, -4.007, -4.958])

    def test_ARG_RMA(self):
        self._test_mod(residue_number=55, target_abbreviation="RMA",
                       internal_residue_number=14, atom_name="CT1",
                       coordinates=[-4.761, -5.743, -3.237])

    def test_ARG_RMN(self):
        self._test_mod(residue_number=55, target_abbreviation="RMN",
                       internal_residue_number=14, atom_name="CT",
                       coordinates=[-2.037, -4.267, -0.438])

    def test_ARG_RMC(self):
        self._test_mod(residue_number=55, target_abbreviation="RMC",
                       internal_residue_number=14, atom_name="CT",
                       coordinates=[-4.89, -5.633, -3.292])

    def test_ARG_R0P(self):
        self._test_mod(residue_number=55, target_abbreviation="R0P",
                       internal_residue_number=14, atom_name="OI2",
                       coordinates=[-5.62, -5.949, -4.591])

    def test_ARG_GSA(self):
        self._test_mod(residue_number=55, target_abbreviation="GSA",
                       internal_residue_number=14, atom_name="OE",
                       coordinates=[-1.729, -3.245, -3.182])

    def test_ARG_R1P(self):
        self._test_mod(residue_number=55, target_abbreviation="R1P",
                       internal_residue_number=14, atom_name="PT",
                       coordinates=[-4.667, -5.831, -3.394])

    def test_ASN_N3H(self):
        self._test_mod(residue_number=68, target_abbreviation="N3H",
                       internal_residue_number=27, atom_name="HG1",
                       coordinates=[6.459, 5.563, 5.28])

    def test_ASN_NH3(self):
        self._test_mod(residue_number=68, target_abbreviation="NH3",
                       internal_residue_number=27, atom_name="OG1",
                       coordinates=[6.868, 6.784, 2.852])

    def test_ASN_NNG(self):
        self._test_mod(residue_number=68, target_abbreviation="NNG",
                       internal_residue_number=27, atom_name="O3",
                       coordinates=[13.899, 10.241, 3.971])

    def test_ASN_NME(self):
        self._test_mod(residue_number=68, target_abbreviation="NME",
                       internal_residue_number=27, atom_name="CE",
                       coordinates=[10.423, 8.957, 3.919])

    def test_ASN_ASP(self):
        self._test_mod(residue_number=68, target_abbreviation="ASP",
                       internal_residue_number=27, atom_name="OD2",
                       coordinates=[9.186, 7.968, 4.45])

    def test_ASN_ASPH(self):
        self._test_mod(residue_number=68, target_abbreviation="ASPH",
                       internal_residue_number=27, atom_name="OD1",
                       coordinates=[10.043, 6.322, 4.595])

    def test_ASP_DN3(self):
        #bug
        self._test_mod(residue_number=44, target_abbreviation="DN3",
                       internal_residue_number=4, atom_name="OD1",
                       coordinates=[9.186, 7.968, 4.45])

    def test_ASP_D3N(self):
        #bug
        self._test_mod(residue_number=46, target_abbreviation="D3N",
                       internal_residue_number=5, atom_name="OG1",
                       coordinates=[9.186, 7.968, 4.45])

    def test_GLN_Q4H(self):
        self._test_mod(residue_number=66, target_abbreviation="Q4H",
                   internal_residue_number=25, atom_name="OD1",
                   coordinates=[3.631, 7.759, -1.905])

    def test_GLN_QH4(self):
        self._test_mod(residue_number=66, target_abbreviation="QH4",
                       internal_residue_number=25, atom_name="OD1",
                       coordinates=[1.95, 7.084, -0.782])

    def test_GLN_QME(self):
        self._test_mod(residue_number=66, target_abbreviation="QME",
                       internal_residue_number=25, atom_name="CZ",
                       coordinates=[3.504, 4.211, -3.522])

    def test_GLN_GLU(self):
        self._test_mod(residue_number=66, target_abbreviation="GLU",
                       internal_residue_number=25, atom_name="OE2",
                       coordinates=[9.186, 7.968, 4.45])

    def test_GLN_GLUH(self):
        #bug
        self._test_mod(residue_number=66, target_abbreviation="GLUH",
                       internal_residue_number=25, atom_name="OE2",
                       coordinates=[0.965, 6.568, -3.42])

    def test_GLU_ECA(self):
        self._test_mod(residue_number=72, target_abbreviation="ECA",
                       internal_residue_number=31, atom_name="CD1",
                       coordinates=[9.54, 2.715, 6.518])

    def test_GLU_ECN(self):
        self._test_mod(residue_number=72, target_abbreviation="ECN",
                       internal_residue_number=31, atom_name="OE1",
                       coordinates=[10.368, 1.909, 6.701])

    def test_GLU_EME(self):
        #bug
        self._test_mod(residue_number=72, target_abbreviation="EME",
                       internal_residue_number=31, atom_name="CZ",
                       coordinates=[9.186, 7.968, 4.45])





    def test_LEU_L3H(self):
        self._test_mod(residue_number=42, target_abbreviation="L3H",
                   internal_residue_number=1, atom_name="OG1",
                   coordinates=[-0.334, -5.515, -0.267])

    def test_LEU_LH3(self):
        self._test_mod(residue_number=42, target_abbreviation="LH3",
                   internal_residue_number=1, atom_name="OG1",
                   coordinates=[-2.085, -5.619, 0.599])

    def test_LEU_L4H(self):
        self._test_mod(residue_number=42, target_abbreviation="L4H",
                   internal_residue_number=1, atom_name="OD3",
                   coordinates=[1.156, -7.167, 1.328])

    def test_LEU_LH5(self):
        self._test_mod(residue_number=42, target_abbreviation="LH5",
                   internal_residue_number=1, atom_name="HE",
                   coordinates=[1.156, -7.167, 1.328])

"""              
    def test_ASP_DH3(self):
        self._test_mod(residue_number=44/46, target_abbreviation="DH3",
                   internal_residue_number=4/6, atom_name="OG1",
                   coordinates=[9.186, 7.968, 4.45])
                     
    def test_ASP_DMA(self):
        self._test_mod(residue_number=44/46, target_abbreviation="DMA",
                   internal_residue_number=4/6, atom_name="CE",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_ASP_D1P(self):
        self._test_mod(residue_number=44/46, target_abbreviation="D1P",
                   internal_residue_number=4/6, atom_name="PE",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_ASP_D2P(self):
        self._test_mod(residue_number=44/46, target_abbreviation="D2P",
                   internal_residue_number=4/6, atom_name="OZ2",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CSE(self):
        self._test_mod(residue_number=, target_abbreviation="CSE",
                   internal_residue_number=, atom_name="OD3",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CAM(self):
        self._test_mod(residue_number=, target_abbreviation="CAM",
                   internal_residue_number=, atom_name="NE2",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CSA(self):
        self._test_mod(residue_number=, target_abbreviation="CSA",
                   internal_residue_number=, atom_name="OD2",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CYH(self):
        self._test_mod(residue_number=, target_abbreviation="CYH",
                   internal_residue_number=, atom_name="OD",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CYH(self):
        self._test_mod(residue_number=, target_abbreviation="CYH",
                   internal_residue_number=, atom_name="OD",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CSN(self):
        self._test_mod(residue_number=, target_abbreviation="CYS_CSN",
                   internal_residue_number=, atom_name="ND",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_CYS_CYM(self):
        self._test_mod(residue_number=, target_abbreviation="CYM",
                   internal_residue_number=, atom_name="CD",
                   coordinates=[9.186, 7.968, 4.45])          
              
    def test_HIS_H2X(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H2X",
                   internal_residue_number=26/27, atom_name="OZ",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_HIS_H2X(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H2X",
                   internal_residue_number=26/27, atom_name="HD1",
                   coordinates=[9.186, 7.968, 4.45])
    
    def test_HIS_H3M(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H3M",
                   internal_residue_number=26/27, atom_name="CE3",
                   coordinates=[9.186, 7.968, 4.45])
                   
    def test_HIS_H3C(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H3C",
                   internal_residue_number=26/27, atom_name="CE3",
                   coordinates=[9.186, 7.968, 4.45])   
    
    def test_HIS_H1C(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H1C",
                   internal_residue_number=26/27, atom_name="CZ",
                   coordinates=[9.186, 7.968, 4.45])   
    
    def test_HIS_H1C(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H1C",
                   internal_residue_number=26/27, atom_name="HD1",
                   coordinates=[9.186, 7.968, 4.45])
    
    def test_HIS_H1M(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H1M",
                   internal_residue_number=26/27, atom_name="CZ",
                   coordinates=[9.186, 7.968, 4.45])       
    
    def test_HIS_H32(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H32",
                   internal_residue_number=26/27, atom_name="PE3",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_H31(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H31",
                   internal_residue_number=26/27, atom_name="OZ3",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_H12(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H12",
                   internal_residue_number=26/27, atom_name="OH3",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_H11(self):
        self._test_mod(residue_number=66/67, target_abbreviation="H11",
                   internal_residue_number=26/27, atom_name="OH1",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_ASP(self):
        self._test_mod(residue_number=66/67, target_abbreviation="ASP",
                   internal_residue_number=26/27, atom_name="OD2",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_ASPH(self):
        self._test_mod(residue_number=66/67, target_abbreviation="ASPH",
                   internal_residue_number=26/27, atom_name="OD1",
                   coordinates=[9.186, 7.968, 4.45]) 
                   
    def test_HIS_ASN(self):
        self._test_mod(residue_number=66/67, target_abbreviation="ASN",
                   internal_residue_number=26/27, atom_name="ND2",
                   coordinates=[9.186, 7.968, 4.45]) 
                   

"""
