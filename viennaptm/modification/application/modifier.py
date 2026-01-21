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
    """
    Applies residue-level chemical modifications to a biomolecular structure.

    The :class:`Modifier` class acts as a high-level interface between a
    :class:`ModificationLibrary` and an annotated structure. It locates a
    specific residue within a structure, removes hydrogen atoms, applies the
    requested modification using a template residue, and records the
    modification in the structure's modification log.

    :param library:
        Library containing residue modification definitions and template
        residues. If ``None``, an internal default
        :class:`~ModificationLibrary` is loaded.
    :type library: ModificationLibrary, optional
    """

    def __init__(self, library: ModificationLibrary=None):
        """
        Initialize a :class:`Modifier` instance.

        :param library:
            Library providing available residue modifications. If not provided,
            a default internal library is instantiated.
        :type library: ModificationLibrary, optional
        """

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
        """
        Apply a residue modification to a structure.

        This method locates a residue by chain identifier and residue number,
        removes all hydrogen atoms, applies a modification defined in the
        modification library, and optionally returns a modified copy of the
        structure.

        :param structure:
            The structure to be modified.
        :type structure: AnnotatedStructure

        :param chain_identifier:
            Chain identifier of the target residue (commonly a single uppercase
            letter).
        :type chain_identifier: str

        :param residue_number:
            Position of the residue in the polypeptide chain, starting at \(1\)
            from the N-terminus.
        :type residue_number: int

        :param target_abbreviation:
            Three-letter abbreviation of the target (modified) residue.
        :type target_abbreviation: str

        :param inplace:
            If ``True``, the structure is modified in place.
            If ``False``, a deep copy of the structure is created and modified.
        :type inplace: bool

        :returns:
            The modified structure. This is either the original structure
            (if ``inplace=True``) or a modified copy.
        :rtype: AnnotatedStructure

        :raises ValueError:
            If the specified residue cannot be found in the given chain.
        :raises KeyError:
            If atom names required for the modification do not match those
            in the structure or the template residue.

        . note::
            This method assumes that:

            * Chain identifiers are unique across all models.
            * A template PDB exists for every supported modification.
            * The structure supports modification logging via
              ``add_to_modification_log``.
        """

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

        # fetch the desired application and load the respective template PDB file
        # note: this assumes, that for all modifications a template PDB exists
        original_residue_abbreviation = residue.get_resname()
        modification = self._library[original_residue_abbreviation, target_abbreviation]
        target_residue = self._library.load_residue_from_pdb(target_abbreviation)

        # apply the application (changes to the respective residue are saved, since it is mutable) and log it
        self._execute_modification(residue=residue,
                                   modification=modification,
                                   template_residue=target_residue)
        residue.resname = target_residue.get_resname()

        # attach information on applied application
        structure.add_to_modification_log(residue_number=residue_number,
                                          chain_identifier=chain_identifier,
                                          original_abbreviation=original_residue_abbreviation,
                                          target_abbreviation=target_abbreviation)
        return structure

    @staticmethod
    def _rename_atom(residue: Residue, old_name: str, new_name: str):
        atom = residue[old_name]

        # Remove atom from residue internal list of atoms
        residue.detach_child(old_name)

        # Update atom properties
        atom.name = new_name
        atom.fullname = f"{new_name:>4}"
        atom.id = new_name

        # Reinsert atom with new name
        residue.add(atom)

    @staticmethod
    def _execute_modification(residue: Residue,
                              modification: Modification,
                              template_residue: Residue):
        """
        Execute a residue modification in place.

        This method performs the low-level operations required to apply a
        modification, including atom alignment, rigid-body transformation,
        and atom addition, removal, or renaming.

        :param residue:
            The original residue to be modified.
        :type residue: Residue

        :param modification:
            Modification definition describing atom mappings, anchor atoms,
            and added branches.
        :type modification: Modification

        :param template_residue:
            Template residue containing the target atom geometry.
        :type template_residue: Residue

        :raises KeyError:
            If required anchor atoms are missing in either the original or
            template residue.
        """

        # since branches may rename atoms, multi-branch application could run into issues if the later branches
        # attempt to rename again; therefore, only execute renaming for the first one
        branch_first = True
        for branch in modification.add_branches:
            # atoms names may change from the original to the modified residue; therefore, we use
            # the atom mapping to get the anchor lists for both with the right atom
            # identity (irrespective of name); for example, in VAL<>V3H the template residue's anchor atoms
            # ['CB', 'CA', 'CG1', 'C', 'N'] map to ['CB', 'CA', 'CG2', 'C', 'N'] in the original residue
            _mapping = {temp: ori for ori, temp in modification.atom_mapping}
            anchor_atoms_in_original_residue = [_mapping[x] for x in branch.anchor_atoms]
            logger.debug(f"Anchor atoms used for {residue.get_resname()}->{template_residue.get_resname()}: {anchor_atoms_in_original_residue} and {branch.anchor_atoms}")

            # extract Atoms for anchor atoms in both original residue and template
            # the following ensures that the order of atoms is identical in both lists
            try:
                original_anchor_atoms = [residue[atom_name] for atom_name in anchor_atoms_in_original_residue]
            except KeyError as e:
                raise_with_logging_error(f"Key Error of original anchor atoms. Atom names do not match original"
                                         f" residue: {anchor_atoms_in_original_residue}. Check for spelling errors.",
                                         logger=logger,
                                         exception_type=KeyError,
                                         exp=e)

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

            # rename and delete atoms based on atom_mapping (remove those that are mapped to "None" in the updated form)
            if branch_first:
                for ori, tar in modification.atom_mapping:
                    if ori == tar:
                        continue

                    # skip atoms that are not present in the original residue (they were added in the previous step)
                    if ori is not None:
                        if tar is None:
                            # this indicates, that this particular ori-atom is to be removed
                            if ori in residue:
                                residue.detach_child(ori)
                        else:
                            # this means, an atom is to be renamed
                            if ori != tar:
                                Modifier._rename_atom(residue, ori, tar)

            # add new atoms
            for atom_idx, atom in enumerate(add_atoms):
                residue.add(Atom(name=atom.get_name(),
                                 coord=coords_aligned[atom_idx],
                                 bfactor=0,
                                 occupancy=1.0,
                                 altloc=' ',
                                 fullname= f"{atom.get_fullname():>4}",
                                 serial_number=None,
                                 element=atom.element))
            branch_first = False

    @staticmethod
    def atoms_to_array(atoms: List[Atom]) -> np.ndarray:
        """
        Convert a list of atoms to a NumPy coordinate array.

        :param atoms:
            Atoms whose coordinates should be extracted.
        :type atoms: list[Atom]

        :returns:
            Array of shape ``(n_atoms, 3)`` containing atomic coordinates.
        :rtype: numpy.ndarray
        """

        return np.array([atom.get_coord() for atom in atoms])

    @staticmethod
    def remove_hydrogens(residue: Residue):
        """
        Remove all hydrogen atoms from a residue.

        Hydrogen atoms are identified by atom names starting with ``"H"``.
        This step avoids inconsistencies in atom naming schemes during
        modification.

        :param residue:
            Residue from which hydrogen atoms will be removed.
        :type residue: Residue
        """

        # deletes atom if it is a Hydrogen, because otherwise they could be "lingering" if they do not conform
        # to the standard naming scheme; note that Hydrogen deletions are not part of the ModificationLibrary
        to_delete = [atom.name for atom in residue.get_atoms() if atom.name.startswith("H")]
        for atom_name in to_delete:
            residue.detach_child(atom_name)


    def get_library(self):
        """
        Return the associated modification library.

        :returns:
            The library used by this :class:`Modifier` instance.
        :rtype: ModificationLibrary
        """

        return self._library

