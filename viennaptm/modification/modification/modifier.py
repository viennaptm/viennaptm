from typing import List

import numpy as np
import logging
from copy import deepcopy

from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from pydantic import BaseModel

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.modification.calculation.align import compute_alignment_transform, apply_transform
from viennaptm.modification.modification_library import ModificationLibrary, Modification
from viennaptm.utils.error_handling import raise_with_logging_error

logger = logging.getLogger(__name__)


class Modifier(BaseModel):
    """Class that actually applies any number of modifications from a modification library to a structure"""

    def __init__(self, library: ModificationLibrary=None):
        BaseModel.__init__(self)

        # if no library is specified, load the internal default
        if library is None:
            library = ModificationLibrary()

        self._library = library

    def apply_modification(self,
                           structure: AnnotatedStructure,
                           chain_identifier: str,
                           residue_number: int,
                           target_abbreviation: str,
                           inplace: bool = True) -> AnnotatedStructure:
        # if inplace is set to False, make a copy for the manipulation
        if not inplace:
            structure = deepcopy(structure)

        # get residue from structure
        # note: this assumes that chain IDs are unique over all models
        residue = None
        for cur_residue in structure.get_residues():
            # get the full residue identifier, e.g. ("1vii.pdb", 0, 'A', (' ', 41, ' '))
            # this means (target identifier, model number, chain identifier, (hetero- or non-hetero residue, residue
            # number, insertion code))
            full_id = cur_residue.get_full_id()

            if full_id[2] == chain_identifier and full_id[3][1] == residue_number:
                residue = cur_residue
                break

        if residue is None:
            raise_with_logging_error(f"Could not find specified residue in specified chain: {chain_identifier}:{residue_number}.",
                                     logger=logger,
                                     exception_type=ValueError)

        self.remove_hydrogens(residue)

        # fetch the desired modification and load the respective template PDB file
        # note: this assumes, that for all modifications a template PDB exists
        original_residue_abbreviation = residue.get_resname()
        modification = self._library[original_residue_abbreviation, target_abbreviation]
        target_residue = self._library.load_residue_from_pdb(target_abbreviation)

        # apply the modification (changes to the respective residue are saved, since it is mutable) and log it
        self._execute_modification(residue=residue,
                                   modification=modification,
                                   template_residue=target_residue)
        residue.resname = target_residue.get_resname()

        # attach information on applied modification
        structure.add_to_modification_log(residue_number=residue_number,
                                          chain_identifier=chain_identifier,
                                          original_abbreviation=original_residue_abbreviation,
                                          target_abbreviation=target_abbreviation)
        return structure

    @staticmethod
    def _execute_modification(residue: Residue,
                              modification: Modification,
                              template_residue: Residue):
        for branch in modification.add_branches:
            # atoms names may change from the original to the modified residue; therefore, we use
            # the atom mapping to get the anchor lists for both with the right atom
            # identity (irrespective of name); for example, in VAL->V3H the template residue's anchor atoms
            # ['CB', 'CA', 'CG1', 'C', 'N'] map to ['CB', 'CA', 'CG2', 'C', 'N'] in the original residue
            _mapping = {temp: ori for ori, temp in modification.atom_mapping}
            anchor_atoms_in_original_residue = [_mapping[x] for x in branch.anchor_atoms]
            logger.debug(f"Anchor atoms used for {residue.get_resname()}->{template_residue.get_resname()}: {anchor_atoms_in_original_residue} and {branch.anchor_atoms}")

            # extract Atoms for anchor atoms in both original residue and template
            # the following ensures that the order of atoms is identical in both lists
            try:
                original_anchor_atoms = [residue[atom_name] for atom_name in anchor_atoms_in_original_residue]
            except KeyError:
                raise_with_logging_error(f"Key Error of original anchor atoms. Atom names do not match original"
                                         f" residue: {anchor_atoms_in_original_residue}. Check for spelling errors.",
                                         logger=logger,
                                         exception_type=KeyError)

            try:
                template_anchor_atoms = [template_residue[atom_name] for atom_name in branch.anchor_atoms]
            except KeyError:
                raise_with_logging_error(f"Key Error of template anchor atoms. Atom names do not match template"
                                         f" residue: {branch.anchor_atoms}. Check library.",
                                         logger=logger,
                                         exception_type=KeyError)

            # create roto-translational alignment
            M_rotation, v_translation = compute_alignment_transform(coord_reference=Modifier.atoms_to_array(original_anchor_atoms),
                                                                    coord_template=Modifier.atoms_to_array(template_anchor_atoms),
                                                                    weights=np.array(branch.weights))

            # extract the atoms that are to be transferred from the template to the original residue
            add_atoms = [template_residue[atom_name] for atom_name in branch.add_atoms]
            coords = Modifier.atoms_to_array(add_atoms)

            # transform atoms to be added
            coords_aligned = apply_transform(coords=coords,
                                             M_rotation=M_rotation,
                                             v_translation=v_translation)

            # add new atoms
            for atom_idx, atom in enumerate(add_atoms):
                residue.add(Atom(name=atom.get_fullname(),
                                 coord=coords_aligned[atom_idx],
                                 bfactor=0,
                                 occupancy=1.0,
                                 altloc=' ',
                                 fullname=atom.get_fullname().center(4, ' '),
                                 serial_number=None,
                                 element=atom.element))

            # rename atoms based on atom_mapping (remove those that are mapped to "None" in the updated form)
            for ori, tar in modification.atom_mapping:
                # skip atoms that are not present in the original residue (they were added in the previous step)
                if ori is not None:
                    if tar is None:
                        # this indicates, that this particular ori-atom is to be removed
                        if ori in residue:
                            residue.detach_child(ori)
                    else:
                        # this means, an atom is to be renamed
                        if ori != tar:
                            residue[ori].name = tar

    @staticmethod
    def atoms_to_array(atoms: List[Atom]) -> np.ndarray:
        return np.array([atom.get_coord() for atom in atoms])

    @staticmethod
    def remove_hydrogens(residue: Residue):
        # deletes atom if it is a Hydrogen, because otherwise they could be "lingering" if they do not conform
        # to the standard naming scheme; note that Hydrogen deletions are not part of the ModificationLibrary
        to_delete = [atom.name for atom in residue.get_atoms() if atom.name.startswith("H")]
        for atom_name in to_delete:
            residue.detach_child(atom_name)


    def get_library(self):
        return self._library

