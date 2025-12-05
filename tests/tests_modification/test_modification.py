import logging
import unittest
import os

from Bio.PDB.Residue import Residue
from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from viennaptm.modification.modification.modifier import Modifier
from viennaptm.utils.paths import attach_root_path
from pathlib import Path

logger = logging.getLogger(__name__)


class Test_Modification(unittest.TestCase):

    def setUp(self):
        self._struc_io = AnnotatedStructure("dd")
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)
        Path(attach_root_path(UNITTEST_JUNK_FOLDER)).mkdir(parents=True, exist_ok=True)

    def test_apply_modifications(self):
        output_pdb_path = os.path.join(UNITTEST_JUNK_FOLDER, "apply_modifications.pdb")
        if os.path.exists(output_pdb_path):
            os.remove(output_pdb_path)

        # load internal PDB file
        structure = self._struc_io.from_pdb(path=self._1vii_PDB_path)

        # use API pattern to apply two modification
        modifier = Modifier()
        structure = modifier.apply_modification(structure=structure,
                                                chain_identifier='A',
                                                residue_number=50,
                                                target_abbreviation="V3H")
        structure = modifier.apply_modification(structure=structure,
                                                chain_identifier='A',
                                                residue_number=55,
                                                target_abbreviation="GSA")

        # check write-out
        structure.to_pdb(output_pdb_path)
        self.assertTrue(os.path.exists(output_pdb_path))
        self.assertEqual(os.path.getsize(output_pdb_path), 46649)

        ###TODO check on structure object


    def test_deletion_hydrogen_atoms(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb(path=self._1vii_PDB_path)

        residue = list(structure.get_residues())[12]
        atoms_before = [atom.name for atom in residue.get_atoms()]
        Modifier.remove_hydrogens(residue)
        atoms_after = [atom.name for atom in residue.get_atoms()]

        self.assertNotEqual(len(atoms_before), len(atoms_after))
        self.assertFalse(atoms_after == atoms_before)

        self.assertListEqual(['N', 'CA', 'C', 'O', 'CB', 'CG', 'SD', 'CE', 'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3',
                                  'HE1', 'HE2', 'HE3'], atoms_before)
        self.assertListEqual(['N', 'CA', 'C', 'O', 'CB', 'CG', 'SD', 'CE'], atoms_after)