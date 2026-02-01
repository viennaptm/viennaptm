from pathlib import Path
from typing import Dict, List, Union

from Bio.PDB import PDBParser, MMCIFParser


BACKBONE_ATOMS = {"N", "CA", "C"}


def is_protein_residue(residue) -> bool:
    atom_names = {atom.get_name() for atom in residue.get_atoms()}
    return BACKBONE_ATOMS.issubset(atom_names)


def get_aa_sequence_from_file(
    path: Union[str, Path],
) -> Dict[str, List[str]]:
    """
    Returns a dictionary, the first element is the chain ID and the second element is a list of residue 3-letter codes.
    """

    path = Path(path)

    if path.suffix.lower() == ".pdb":
        parser = PDBParser(QUIET=True)
    elif path.suffix.lower() in {".cif", ".mmcif"}:
        parser = MMCIFParser(QUIET=True)
    else:
        raise ValueError(f"Unsupported structure format: {path.suffix}")

    structure = parser.get_structure(path.stem, str(path))
    model = structure[0]

    sequences: Dict[str, List[str]] = {}

    for chain in model:
        aa_codes: List[str] = []

        for residue in chain:
            if is_protein_residue(residue):
                aa_codes.append(residue.get_resname())

        if aa_codes:
            sequences[chain.id] = aa_codes

    return sequences
