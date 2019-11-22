import unittest

from Bio.PDB.vectors import Vector
from modification.calculate_atom_positions import AtomPositionCalculator


class Test_AtomPositionCalculator(unittest.TestCase):

    def test_atom_position_calculations(self):
        anchor = Vector(*(3, 3, 3))
        vec_1 = Vector(*(1, 0, 0))
        vec_2 = Vector(*(1, 0, 0))
