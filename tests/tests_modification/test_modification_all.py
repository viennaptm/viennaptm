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
        self._reinitialize()

    def _reinitialize(self):
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

# ARG
    def test_ARG_RCI(self):
        self._test_mod(residue_number=55, target_abbreviation="RCI",
                       internal_residue_number=14, atom_name="NH2",
                       coordinates=[-2.718, -4.319, -5.115])

    def test_ARG_RSM(self):
        self._test_mod(residue_number=55, target_abbreviation="RSM",
                       internal_residue_number=14, atom_name="CT2",
                       coordinates=[-4.149, -4.28, -5.039])
        self._reinitialize()
        self._test_mod(residue_number=55, target_abbreviation="RSM",
                       internal_residue_number=14, atom_name="CT1",
                       coordinates=[-2.035, -4.278, -0.431])


    def test_ARG_RMS(self):
        self._test_mod(residue_number=55, target_abbreviation="RMS",
                       internal_residue_number=14, atom_name="CT2",
                       coordinates=[-4.117, -4.258, -5.046])
        self._reinitialize()
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

# ASN
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

# ASP
    def test_ASP_DN3(self):
        self._test_mod(residue_number=44, target_abbreviation="DN3",
                       internal_residue_number=3, atom_name="OD1",
                       coordinates=[-9.683, -5.69, 2.259])
        self._reinitialize()
        self._test_mod(residue_number=44, target_abbreviation="DN3",
                       internal_residue_number=3, atom_name="HG1",
                       coordinates=[-8.914, -9.359, 2.571])

    def test_ASP_D3N(self):
        self._test_mod(residue_number=44, target_abbreviation="D3N",
                       internal_residue_number=3, atom_name="OG1",
                       coordinates=[-9.184, -8.425, 0.085])
        self._reinitialize()
        self._test_mod(residue_number=44, target_abbreviation="D3N",
                       internal_residue_number=3, atom_name="OD1",
                       coordinates=[-9.382, -5.413, 1.509])

    def test_ASP_D3H(self):
        self._test_mod(residue_number=44, target_abbreviation="D3H",
                       internal_residue_number=3, atom_name="HG1",
                       coordinates=[-10.101, -9.034, 0.517])

    def test_ASP_DH3(self):
        self._test_mod(residue_number=44, target_abbreviation="DH3",
                       internal_residue_number=3, atom_name="OG1",
                       coordinates=[-9.624, -8.365, 2.311])

    def test_ASP_DMA(self):
        self._test_mod(residue_number=44, target_abbreviation="DMA",
                       internal_residue_number=3, atom_name="CE",
                       coordinates=[-10.76, -5.601, 1.782])

    def test_ASP_D1P(self):
        self._test_mod(residue_number=44, target_abbreviation="D1P",
                       internal_residue_number=3, atom_name="PE",
                       coordinates=[-11.721, -8.226, -0.21])

    def test_ASP_D2P(self):
        self._test_mod(residue_number=44, target_abbreviation="D2P",
                       internal_residue_number=3, atom_name="OZ2",
                       coordinates=[-13.109, -8.223, 0.148])

# CYS
    def test_CYS_CSE(self):
        self._test_mod(residue_number=75, target_abbreviation="CSE",
                       internal_residue_number=34, atom_name="OD3",
                       coordinates=[10.134, -3.805, 1.341])

    def test_CYS_CAM(self):
        self._test_mod(residue_number=75, target_abbreviation="CAM",
                       internal_residue_number=34, atom_name="NE2",
                       coordinates=[10.95, -6.483, 1.945])

    def test_CYS_CSA(self):
        self._test_mod(residue_number=75, target_abbreviation="CSA",
                       internal_residue_number=34, atom_name="OD2",
                       coordinates=[9.088, -6.275, 1.157])

    def test_CYS_CYH(self):
        self._test_mod(residue_number=75, target_abbreviation="CYH",
                        internal_residue_number=34, atom_name="OD",
                        coordinates=[8.443, -4.204, -0.144])

    def test_CYS_CSN(self):
        self._test_mod(residue_number=75, target_abbreviation="CSN",
                        internal_residue_number=34, atom_name="ND",
                        coordinates=[9.2, -3.178, 0.482])

    def test_CYS_CYM(self):
        self._test_mod(residue_number=75, target_abbreviation="CYM",
                       internal_residue_number=34, atom_name="CD",
                       coordinates=[10.384, -5.059, 2.358])

# GLN
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
                       coordinates=[0.965, 6.568, -3.42])

    def test_GLN_GLUH(self):
        self._test_mod(residue_number=66, target_abbreviation="GLUH",
                       internal_residue_number=25, atom_name="OE2",
                       coordinates=[1.045, 5.804, -3.324])

    def test_GLU_ECA(self):
        self._test_mod(residue_number=72, target_abbreviation="ECA",
                       internal_residue_number=31, atom_name="CD1",
                       coordinates=[9.54, 2.715, 6.518])

    def test_GLU_ECN(self):
        self._test_mod(residue_number=72, target_abbreviation="ECN",
                       internal_residue_number=31, atom_name="OE1",
                       coordinates=[10.368, 1.909, 6.701])

    def test_GLU_EME(self):
        self._test_mod(residue_number=72, target_abbreviation="EME",
                       internal_residue_number=31, atom_name="CZ",
                       coordinates=[10.597, 3.714, 8.186])

# HIS
    def test_HIS_H2X(self):
        self._test_mod(residue_number=74, target_abbreviation="H2X",
                       internal_residue_number=33, atom_name="OZ",
                       coordinates=[5.639, 0.626, 2.96])
        self._reinitialize()
        self._test_mod(residue_number=74, target_abbreviation="H2X",
                       internal_residue_number=33, atom_name="HD1",
                       coordinates=[3.973, -0.978, 4.35])

    def test_HIS_H3M(self):
        self._test_mod(residue_number=74, target_abbreviation="H3M",
                       internal_residue_number=33, atom_name="CE3",
                       coordinates=[3.866, -0.877, 4.807])

    def test_HIS_H3C(self):
        self._test_mod(residue_number=74, target_abbreviation="H3C",
                       internal_residue_number=33, atom_name="CE3",
                       coordinates=[3.767, -0.698, 4.771])

    def test_HIS_H1C(self):
        self._test_mod(residue_number=74, target_abbreviation="H1C",
                       internal_residue_number=33, atom_name="CZ",
                       coordinates=[5.7, -0.211, 0.143])
        self._reinitialize()
        self._test_mod(residue_number=74, target_abbreviation="H1C",
                       internal_residue_number=33, atom_name="HD1",
                       coordinates=[4.098, -1.15, 4.359])

    def test_HIS_H1M(self):
        self._test_mod(residue_number=74, target_abbreviation="H1M",
                       internal_residue_number=33, atom_name="CZ",
                       coordinates=[5.688, -0.167, 0.146])

    def test_HIS_H32(self):
        self._test_mod(residue_number=74, target_abbreviation="H32",
                       internal_residue_number=33, atom_name="PE3",
                       coordinates=[4.234, -1.04, 4.827])

    def test_HIS_H31(self):
        self._test_mod(residue_number=74, target_abbreviation="H31",
                       internal_residue_number=33, atom_name="OZ3",
                       coordinates=[2.613, -0.837, 5.349])

    def test_HIS_H12(self):
        self._test_mod(residue_number=74, target_abbreviation="H12",
                       internal_residue_number=33, atom_name="OH3",
                       coordinates=[7.01, 0.016, 0.414])

    def test_HIS_H11(self):
        self._test_mod(residue_number=74, target_abbreviation="H11",
                       internal_residue_number=33, atom_name="OH1",
                       coordinates=[5.293, 1.266, -0.028])

    def test_HIS_ASP(self):
        self._test_mod(residue_number=74, target_abbreviation="ASP",
                       internal_residue_number=33, atom_name="OD2",
                       coordinates=[3.065, -0.782, 2.005])

    def test_HIS_ASPH(self):
        self._test_mod(residue_number=74, target_abbreviation="ASPH",
                       internal_residue_number=33, atom_name="OD1",
                       coordinates=[4.075, -1.336, 3.467])

    def test_HIS_ASN(self):
        self._test_mod(residue_number=74, target_abbreviation="ASN",
                       internal_residue_number=33, atom_name="ND2",
                       coordinates=[3.623, -0.861, 3.33])

# LEU
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
                   coordinates=[0.507, -3.75, 3.496])

    def test_LEU_L5H(self):
        self._test_mod(residue_number=42, target_abbreviation="L5H",
                   internal_residue_number=1, atom_name="HE",
                   coordinates=[-1.38, -4.679, 4.07])

    def test_LEU_LNO(self):
        self._test_mod(residue_number=42, target_abbreviation="LNO",
                   internal_residue_number=1, atom_name="CE",
                   coordinates=[0.877, -5.64, 3.916])

# LYS
    def test_LYS_KAL(self):
        self._test_mod(residue_number=73, target_abbreviation="KAL",
                   internal_residue_number=32, atom_name="OZ",
                   coordinates=[3.696, 1.536, 9.663])

    def test_LYS_KAM(self):
        self._test_mod(residue_number=73, target_abbreviation="KAM",
                   internal_residue_number=32, atom_name="OI1",
                   coordinates=[2.98, 2.667, 11.075])

    def test_LYS_KH5(self):
        self._test_mod(residue_number=73, target_abbreviation="KH5",
                   internal_residue_number=32, atom_name="HE1",
                   coordinates=[1.838, -0.99, 9.4])

    def test_LYS_K5H(self):
        self._test_mod(residue_number=73, target_abbreviation="K5H",
                   internal_residue_number=32, atom_name="HE1",
                   coordinates=[2.637, 1.99, 7.525])

    def test_LYS_KHP(self):
        self._test_mod(residue_number=73, target_abbreviation="KHP",
                   internal_residue_number=32, atom_name="OE1",
                   coordinates=[1.891, 1.198, 7.482])

    def test_LYS_KPH(self):
        self._test_mod(residue_number=73, target_abbreviation="KPH",
                   internal_residue_number=32, atom_name="HE1",
                   coordinates=[1.813, -1.731, 8.045])

    def test_LYS_KCA(self):
        self._test_mod(residue_number=73, target_abbreviation="KCA",
                   internal_residue_number=32, atom_name="OI1",
                   coordinates=[1.283, 1.091, 12.207])


    def test_LYS_KCN(self):
        self._test_mod(residue_number=73, target_abbreviation="KCN",
                   internal_residue_number=32, atom_name="HI2",
                   coordinates=[0.99, -0.501, 12.869])

    def test_LYS_KHR(self):
        self._test_mod(residue_number=73, target_abbreviation="KHR",
                   internal_residue_number=32, atom_name="NL",
                   coordinates=[-3.252, 0.309, 11.231])

    def test_LYS_KHS(self):
        self._test_mod(residue_number=73, target_abbreviation="KHS",
                   internal_residue_number=32, atom_name="HL2",
                   coordinates=[-2.826, 0.735, 11.076])

    def test_LYS_KLA(self):
        self._test_mod(residue_number=73, target_abbreviation="KLA",
                   internal_residue_number=32, atom_name="NN",
                   coordinates=[4.265, -4.642, 15.741])

    def test_LYS_KLB(self):
        self._test_mod(residue_number=73, target_abbreviation="KLB",
                   internal_residue_number=32, atom_name="NK1",
                   coordinates=[-1.214, -1.027, 9.903])

    def test_LYS_KAC(self):
        self._test_mod(residue_number=73, target_abbreviation="KAC",
                   internal_residue_number=32, atom_name="CI1",
                   coordinates=[0.804, 0.294, 12.29])

    def test_LYS_K3C(self):
        self._test_mod(residue_number=73, target_abbreviation="K3C",
                   internal_residue_number=32, atom_name="CH2",
                   coordinates=[1.238, -0.426, 10.488])

    def test_LYS_K2M(self):
        self._test_mod(residue_number=73, target_abbreviation="K2M",
                   internal_residue_number=32, atom_name="CH1",
                   coordinates=[2.858, 1.157, 11.571])

    def test_LYS_KMN(self):
        self._test_mod(residue_number=73, target_abbreviation="KMN",
                   internal_residue_number=32, atom_name="CH",
                   coordinates=[1.425, -0.538, 10.648])

    def test_LYS_KMC(self):
        self._test_mod(residue_number=73, target_abbreviation="KMC",
                   internal_residue_number=32, atom_name="CH",
                   coordinates=[1.417, -0.535, 10.643])

    def test_LYS_K2C(self):
        self._test_mod(residue_number=73, target_abbreviation="K2C",
                   internal_residue_number=32, atom_name="CH1",
                   coordinates=[1.461, 1.942, 10.122])

    def test_LYS_K1P(self):
        self._test_mod(residue_number=73, target_abbreviation="K1P",
                   internal_residue_number=32, atom_name="PH",
                   coordinates=[1.903, -0.203, 11.493])

    def test_LYS_LNO(self):
        with self.assertRaises(KeyError) as context:
            # LNO removes atom NZ, no new atoms added
            self._test_mod(residue_number=73, target_abbreviation="LNO",
                           internal_residue_number=32, atom_name="NZ",
                           coordinates=[1.891, 1.198, 7.482])
        self.assertEqual(str(context.exception), "'NZ'")

    def test_LYS_K2P(self):
        self._test_mod(residue_number=73, target_abbreviation="K2P",
                   internal_residue_number=32, atom_name="OI3",
                   coordinates=[3.111, -0.421, 12.295])

# MET
    def test_MET_MES(self):
        self._test_mod(residue_number=53, target_abbreviation="MES",
                   internal_residue_number=12, atom_name="OE3",
                   coordinates=[-9.037, 5.197, 5.917])

    def test_MET_MXS(self):
        self._test_mod(residue_number=53, target_abbreviation="MXS",
                   internal_residue_number=12, atom_name="OE2",
                   coordinates=[-9.249, 5.042, 5.458])

    def test_MET_MSX(self):
        self._test_mod(residue_number=53, target_abbreviation="MSX",
                   internal_residue_number=12, atom_name="OE2",
                   coordinates=[-7.144, 6.019, 4.069])

    def test_MET_LNO(self):
        self._test_mod(residue_number=53, target_abbreviation="LNO",
                   internal_residue_number=12, atom_name="CD",
                   coordinates=[-8.117, 3.973, 6.48])

# PHE
    def test_PHE_F23(self):
        self._test_mod(residue_number=51, target_abbreviation="F23",
                   internal_residue_number=10, atom_name="OZ1",
                   coordinates=[-8.117, 3.973, 6.48])
        self._reinitialize()
        self._test_mod(residue_number=51, target_abbreviation="F23",
                   internal_residue_number=10, atom_name="HE3",
                   coordinates=[-8.117, 3.973, 6.48])

    def test_PHE_F2H(self):
        self._test_mod(residue_number=51, target_abbreviation="F2H",
                   internal_residue_number=10, atom_name="OE3",
                   coordinates=[0.323, 1.755, 4.236])

    def test_PHE_F3H(self):
        self._test_mod(residue_number=51, target_abbreviation="F3H",
                   internal_residue_number=10, atom_name="OZ1",
                   coordinates=[0.323, 1.755, 4.236])

    def test_PHE_TYR(self):
        self._test_mod(residue_number=51, target_abbreviation="TYR",
                   internal_residue_number=10, atom_name="HH",
                   coordinates=[1.865, -2.254, 0.758])

# PRO
    def test_PRO_PGA(self):
        # bug, Atom names do not match template residue.
        self._test_mod(residue_number=62, target_abbreviation="PGA",
                   internal_residue_number=21, atom_name="CD",
                   coordinates=[1.865, -2.254, 0.758])
        self._reinitialize()
        self._test_mod(residue_number=51, target_abbreviation="PGA",
                       internal_residue_number=10, atom_name="CA",
                       coordinates=[-8.117, 3.973, 6.48])

    def test_PRO_PHH(self):
        # bug, Atom names do not match template residue.
        self._test_mod(residue_number=62, target_abbreviation="PHH",
                   internal_residue_number=21, atom_name="OD1",
                   coordinates=[1.865, -2.254, 0.758])
        self._reinitialize()
        self._test_mod(residue_number=51, target_abbreviation="PHH",
                       internal_residue_number=10, atom_name="HG1",
                       coordinates=[-8.117, 3.973, 6.48])

    def test_PRO_HY2(self):
        self._test_mod(residue_number=62, target_abbreviation="HY2",
                   internal_residue_number=21, atom_name="OD1",
                   coordinates=[2.511, 13.724, 1.828])

    def test_PRO_PH3(self):
        self._test_mod(residue_number=62, target_abbreviation="PH3",
                   internal_residue_number=21, atom_name="OG1",
                   coordinates=[4.585, 11.614, 0.6])

    def test_PRO_P3H(self):
        self._test_mod(residue_number=62, target_abbreviation="P3H",
                   internal_residue_number=21, atom_name="HG1",
                   coordinates=[3.764, 14.262, -0.758])

    def test_PRO_HYP(self):
        self._test_mod(residue_number=62, target_abbreviation="HYP",
                   internal_residue_number=21, atom_name="OD1",
                   coordinates=[3.438, 12.432, 2.444])

    def test_PRO_P5H(self):
        self._test_mod(residue_number=62, target_abbreviation="P5H",
                   internal_residue_number=21, atom_name="OE",
                   coordinates=[1.308, 10.622, 2.235])

    def test_PRO_PH5(self):
        self._test_mod(residue_number=62, target_abbreviation="PH5",
                   internal_residue_number=21, atom_name="HE",
                   coordinates=[0.083, 12.473, 2.266])

    def test_PRO_GSA(self):
        # bug, Atom names do not match template residue.
        self._test_mod(residue_number=62, target_abbreviation="GSA",
                   internal_residue_number=21, atom_name="CB",
                   coordinates=[0.083, 12.473, 2.266])
        self._reinitialize()
        self._test_mod(residue_number=51, target_abbreviation="GSA",
                       internal_residue_number=10, atom_name="H",
                       coordinates=[-8.117, 3.973, 6.48])

# SER
    def test_SER_SOG(self):
        self._test_mod(residue_number=43, target_abbreviation="SOG",
                   internal_residue_number=2, atom_name="C2",
                   coordinates=[-1.679, -12.589, 0.318])

    def test_SER_S1P(self):
        self._test_mod(residue_number=43, target_abbreviation="S1P",
                   internal_residue_number=2, atom_name="OE3",
                   coordinates=[-5.472, -11.411, 2.811])

    def test_SER_SDH(self):
        # bug, Atom names do not match template residue.
        self._test_mod(residue_number=43, target_abbreviation="SDH",
                   internal_residue_number=2, atom_name="CB",
                   coordinates=[-5.472, -11.411, 2.811])

    def test_SER_S2P(self):
        self._test_mod(residue_number=43, target_abbreviation="S2P",
                   internal_residue_number=2, atom_name="PD",
                   coordinates=[-4.126, -11.983, 2.331])

# THR
    def test_THR_TOX(self):
        self._test_mod(residue_number=54, target_abbreviation="TOX",
                   internal_residue_number=13, atom_name="OG1",
                   coordinates=[-8.895, 0.822, 1.119])

    def test_THR_TOG(self):
        self._test_mod(residue_number=54, target_abbreviation="TOG",
                   internal_residue_number=13, atom_name="C7",
                   coordinates=[-7.322, 0.336, 4.806])

    def test_THR_T1P(self):
        self._test_mod(residue_number=54, target_abbreviation="T1P",
                   internal_residue_number=13, atom_name="HE3",
                   coordinates=[-9.531, -0.437, 4.101])

    def test_THR_TDH(self):
        # bug, Atom names do not match template residue.
        self._test_mod(residue_number=54, target_abbreviation="TDH",
                   internal_residue_number=13, atom_name="CB",
                   coordinates=[-9.531, -0.437, 4.101])

    def test_THR_T2P(self):
        self._test_mod(residue_number=54, target_abbreviation="T2P",
                   internal_residue_number=13, atom_name="PD",
                   coordinates=[-9.386, 1.072, 2.818])

# TRP
    def test_TRP_W2H(self):
        self._test_mod(residue_number=64, target_abbreviation="W2H",
                   internal_residue_number=23, atom_name="HE4",
                   coordinates=[7.19, 13.445, -2.433])

    def test_TRP_W4H(self):
        self._test_mod(residue_number=64, target_abbreviation="W4H",
                   internal_residue_number=23, atom_name="OZ4",
                   coordinates=[7.785, 10.508, 2.945])

    def test_TRP_W5H(self):
        self._test_mod(residue_number=64, target_abbreviation="W5H",
                   internal_residue_number=23, atom_name="HH3",
                   coordinates=[6.607, 10.324, 4.865])

    def test_TRP_W6H(self):
        self._test_mod(residue_number=64, target_abbreviation="W6H",
                   internal_residue_number=23, atom_name="OI",
                   coordinates=[4.414, 13.346, 4.682])

    def test_TRP_W7H(self):
        self._test_mod(residue_number=64, target_abbreviation="W7H",
                   internal_residue_number=23, atom_name="OH2",
                   coordinates=[4.413, 14.733, 2.237])

    def test_TRP_WNI(self):
        self._test_mod(residue_number=64, target_abbreviation="WNI",
                   internal_residue_number=23, atom_name="NT",
                   coordinates=[4.327, 13.268, 4.654])

    def test_TRP_WBR(self):
        self._test_mod(residue_number=64, target_abbreviation="WBR",
                   internal_residue_number=23, atom_name="BRT",
                   coordinates=[4.085, 13.498, 5.132])

    def test_TRP_WKF(self):
        self._test_mod(residue_number=64, target_abbreviation="WKF",
                   internal_residue_number=23, atom_name="NZ1",
                   coordinates=[8.295, 12.519, -2.68])

    def test_TRP_WKH(self):
        self._test_mod(residue_number=64, target_abbreviation="WKH",
                   internal_residue_number=23, atom_name="CZ3",
                   coordinates=[5.373, 14.715, -0.985])

    def test_TRP_WKY(self):
        self._test_mod(residue_number=64, target_abbreviation="WKY",
                   internal_residue_number=23, atom_name="HZ11",
                   coordinates=[8.289, 11.141, -2.502])

# TYR
    def test_TYR_YSU(self):
        self._test_mod(residue_number=76, target_abbreviation="YSU",
                       internal_residue_number=35, atom_name="OI2",
                       coordinates=[7.366, -13.306, 9.324])

    def test_TYR_HTY(self):
        self._test_mod(residue_number=76, target_abbreviation="HTY",
                       internal_residue_number=35, atom_name="OZ1",
                       coordinates=[8.701, -13.086, 5.837])

    def test_TYR_YNB(self):
        self._test_mod(residue_number=76, target_abbreviation="YNB",
                       internal_residue_number=35, atom_name="OH2",
                       coordinates=[8.289, 11.141, -2.502])

    def test_TYR_YNN(self):
        self._test_mod(residue_number=76, target_abbreviation="YNN",
                       internal_residue_number=35, atom_name="NZ1",
                       coordinates=[8.289, 11.141, -2.502])

    def test_TYR_YNI(self):
        self._test_mod(residue_number=76, target_abbreviation="YNI",
                       internal_residue_number=35, atom_name="OH1",
                       coordinates=[9.058, -12.71, 4.317])

    def test_TYR_Y1P(self):
        self._test_mod(residue_number=76, target_abbreviation="Y1P",
                       internal_residue_number=35, atom_name="PT",
                       coordinates=[7.114, -15.471, 6.361])

    def test_TYR_YCH(self):
        self._test_mod(residue_number=76, target_abbreviation="YCH",
                       internal_residue_number=35, atom_name="CLZ1",
                       coordinates=[8.976, -13.349, 5.729])

    def test_TYR_Y2P(self):
        self._test_mod(residue_number=76, target_abbreviation="Y2P",
                       internal_residue_number=35, atom_name="OI1",
                       coordinates=[8.443, -15.321, 5.957])

# VAL
    def test_VAL_V3H(self):
        self._test_mod(residue_number=50, target_abbreviation="V3H",
                       internal_residue_number=9, atom_name="HG3",
                       coordinates=[1.029, -3.052, 5.974])
