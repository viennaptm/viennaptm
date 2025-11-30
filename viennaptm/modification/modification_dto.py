from typing import List, Tuple

from pydantic import BaseModel, ConfigDict, Field


class AddBranch(BaseModel):
    anchor_atoms: List[str]
    add_atoms: List[str]
    weights: List[float] = None
    model_config = ConfigDict(extra="forbid")


class Modification(BaseModel):
    residue_original_abbreviation: str
    residue_modified_abbreviation: str

    # contains a list of the form [('N', 'N'), ...] which maps the original residue's atom names
    # to the modified residue's; if an atom does not exist in one of the end-states, it is set to None
    # for example, atoms that need to be deleted during modification, are marked as None
    atom_pairs: List[Tuple[str, str]] = Field(default_factory=list)

    # each AddBranch contains information on how to modify _one_ part (or branch) of the original
    # residue into the target, modified PTM; for most modifications, only one branch is needed, but
    # this setup allows to modify the original residues in different regions without a need to
    # 'truncate' back all the way to last common atom
    add_branches: List[AddBranch] = Field(default_factory=list)

    # TODO: add actual modified names for PTMs (should be part of the server files)
    model_config = ConfigDict(extra="forbid")

