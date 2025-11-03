import numpy as np
from copy import deepcopy

from viennaptm.IOclasses.iomodlibrary import IOModLibrary
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from Bio.PDB.Structure import Structure
from viennaptm.modification.modification import Modification
from viennaptm.modification.modification_report import ModificationReport
from viennaptm.modification.calculate_atom_positions import AtomPositionCalculator


class Modifier:
    """Class that actually applies any number of modifications in a modification library to a structure"""

    def __init__(self, structure: Structure, library=None):
        # if no library is specified, load the internal default
        if library is None:
            io_lib = IOModLibrary()
            library = io_lib.load_database(path=None)

        self._library = library
        self._original_structure = structure
        self._structure = deepcopy(structure)

    @staticmethod
    def _execute_modification(residue: Residue, modification: Modification) -> ModificationReport:
        report = ModificationReport()

        # change name of target (three-letter abbreviation only!)
        residue.resname = modification.target_abbreviation

        # delete atoms, if specified
        if len(modification.atom_deletions) > 0:
            for deletion in modification.atom_deletions:
                if deletion.name in residue:
                    residue.detach_child(deletion.name)
                    report.atoms_deleted += 1

        # rename atoms, if specified
        # note: do not forget to update the element-type in case this is required
        if len(modification.atom_replacements) > 0:
            for replacement in modification.atom_replacements:
                if replacement.name in residue:
                    # create a new atom to properly update parent dictionary
                    oldAtom = residue[replacement.name]
                    repAtom = Atom(name=replacement.by,
                                   coord=oldAtom.coord,
                                   bfactor=oldAtom.bfactor,
                                   occupancy=oldAtom.occupancy,
                                   altloc=oldAtom.altloc,
                                   fullname=replacement.by.center(4, ' '),
                                   serial_number=oldAtom.serial_number,
                                   element=oldAtom.element if replacement.new_eletype is None else replacement.new_eletype)
                    residue.detach_child(replacement.name)
                    residue.add(repAtom)
                    report.atoms_renamed += 1

        # if specified, start by obtain an internal, relative coordinate system
        if len(modification.atom_additions) > 0:
            AtomPosCalc = AtomPositionCalculator(anchor_coordinates=residue[modification.anchor].coord,
                                                 vector_1=residue[modification.axis1.p2].coord -
                                                          residue[modification.axis1.p1].coord,
                                                 vector_2=residue[modification.axis2.p2].coord -
                                                          residue[modification.axis2.p1].coord)
            for addition in modification.atom_additions:
                if addition.name not in residue:
                    residue.add(Atom(name=addition.name,
                                     coord=AtomPosCalc.project_coordinates(coordinates=np.array([addition.xcoorr,
                                                                                                 addition.ycoorr,
                                                                                                 addition.zcoorr])),
                                     bfactor=0,
                                     occupancy=1.0,
                                     altloc=' ',
                                     fullname=addition.name.center(4, ' '),
                                     serial_number=None,
                                     element=addition.eletype))
                    report.atoms_added += 1

        return report

    def apply_modification(self, chain_identifier: str, residue_number: int,
                           target_abbreviation=None, modification_name=None) -> ModificationReport:

        # get residue from structure
        # note: this assumes that chain IDs are unique over all models
        residue = None
        for cur_residue in self._structure.get_residues():
            # get the full residue identifier, e.g. ("1vii.pdb", 0, 'A', (' ', 41, ' '))
            # this means (target identifier, model number, chain identifier, (hetero- or non-hetero residue, residue
            # number, insertion code))
            full_id = cur_residue.get_full_id()
            if full_id[2] == chain_identifier and full_id[3][1] == residue_number:
                residue = cur_residue
                break
        if residue is None:
            raise Exception("Could not find specified residue in specified chain.")

        # try to get modification from library
        modification = self._library.get_modification(initial_abbreviation=residue.get_resname(),
                                                      target_abbreviation=target_abbreviation,
                                                      modification_name=modification_name)

        # apply the modification
        return self._execute_modification(residue=residue, modification=modification)

    def reset_structure(self):
        self._structure = deepcopy(self._original_structure)

    def get_library(self):
        return self._library

    def get_structure(self):
        return self._structure
