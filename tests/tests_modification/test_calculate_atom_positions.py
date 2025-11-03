import unittest
import numpy as np

from Bio.PDB.vectors import Vector

from viennaptm.modification.calculate_atom_positions import AtomPositionCalculator


class Test_AtomPositionCalculator(unittest.TestCase):

    def test_relative_coordinate_system_construction(self):
        # simple loading
        anchor = np.array([1, 0, 2])
        vec_1 = np.array([1, 0, 0])
        vec_2 = np.array([0, 0, 1])
        APCalc = AtomPositionCalculator(anchor_coordinates=anchor, vector_1=vec_1, vector_2=vec_2)
        anchor = APCalc.get_anchor_coordinates()
        axes = APCalc.get_axes()
        self.assertListEqual(list(anchor), list(np.array([1.0, 0.0, 2.0])))
        self.assertListEqual(list(axes[0]), list(np.array([1.0, 0.0, 0.0])))

        # non-orthogonal, non-normalized input vectors
        vec_1 = np.array([121, 98, 111])
        vec_2 = np.array([98, 0, 12])
        APCalc = AtomPositionCalculator(anchor_coordinates=anchor, vector_1=vec_1, vector_2=vec_2)
        axes = [Vector(x) for x in APCalc.get_axes()]
        self.assertListEqual([0.7694293307360616, -0.5004230192716838, -0.3969323705444901], list(axes[1]))
        self.assertListEqual([1.0, 1.0, 1.0], [x.norm() for x in axes])
        angles = [axes[0].angle(axes[1]), axes[0].angle(axes[2]), axes[1].angle(axes[2])]
        self.assertListEqual([round(np.rad2deg(x), ndigits=9) for x in angles], [90.0, 90.0, 90.0])

    def test_project_coordinates(self):
        anchor = np.array([3, 3, 3])
        vec_1 = np.array([1, 0, 0])
        vec_2 = np.array([0, 0, 1])
        APCalc = AtomPositionCalculator(anchor_coordinates=anchor, vector_1=vec_1, vector_2=vec_2)
        p1 = np.array([0, 0, 3])
        p2 = np.array([0, 1.5, 12])
        p3 = np.array([1, 1, 1])
        self.assertListEqual(list(np.array([3.0, 0.0, 3.0])), list(APCalc.project_coordinates(p1)))
        self.assertListEqual(list(np.array([3.0, -9.0, 4.5])), list(APCalc.project_coordinates(p2)))
        self.assertListEqual(list(np.array([4.0, 2.0, 4.0])), list(APCalc.project_coordinates(p3)))
