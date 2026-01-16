from typing import List
import numpy as np
from Bio.PDB.Residue import Residue


def get_coords_for_atom(residue: Residue, atom_name: str) -> List[float]:
    return np.round(residue[atom_name].get_coord(), 3).tolist()
