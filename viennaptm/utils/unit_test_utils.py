from typing import List
import numpy as np
from Bio.PDB.Residue import Residue


def get_coords_for_atom(residue: Residue, atom_name: str) -> List[float]:
    """
    Retrieve the Cartesian coordinates of a specific atom in a residue.

    The coordinates are extracted from the atom object, rounded to three
    decimal places, and returned as a plain Python list. This representation
    is suitable for serialization, logging, or comparison operations.

    :param residue:
        Residue containing the requested atom.
    :type residue: Bio.PDB.Residue.Residue

    :param atom_name:
        Name of the atom whose coordinates should be retrieved.
    :type atom_name: str

    :returns:
        A list of three floating-point values ``[x, y, z]`` representing
        the atom's Cartesian coordinates, rounded to three decimals.
    :rtype: list[float]

    :raises KeyError:
        If the specified atom name does not exist in the residue.
    """
    return np.round(residue[atom_name].get_coord(), 3).tolist()
