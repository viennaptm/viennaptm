import logging
import unittest
import os

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.modification.modification.modifier import Modifier
from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from viennaptm.utils.paths import attach_root_path
from pathlib import Path

logger = logging.getLogger(__name__)


class Test_Modification(unittest.TestCase):

    def setUp(self):
        self._struc_io = AnnotatedStructure("dd")
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)
        Path(attach_root_path(UNITTEST_JUNK_FOLDER)).mkdir(parents=True, exist_ok=True)

    def test_apply_modifications(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb(path=self._1vii_PDB_path)

        # initialize modifier with most recent internal modification database
        modifier = Modifier(structure=structure)

        # apply a modification
        report = modifier.apply_modification(chain_identifier='A',
                                             residue_number=50,
                                             target_abbreviation="V3H")

        self.assertListEqual([report.atoms_added, report.atoms_deleted, report.atoms_renamed],
                             [4, 2, 0])
        atoms = list(list(modifier.get_structure().get_residues())[9].get_atoms())
        atom_names = [atom.get_name() for atom in atoms]
        self.assertListEqual(['N', "CA", 'C', 'O', "CB", 'H', "HA", "HB", "HG11",
                              "HG12", "HG13", "HG21", "HG22", "HG23", "OG3", "HG3", "CG1", "CG2"],
                             atom_names)
        self.assertListEqual(list(atoms[15].get_coord()), [0.9564358629429937, -3.0478645520202967, 5.9284670164914965])

        # add another modification
        report = modifier.apply_modification(chain_identifier='A',
                                             residue_number=60,
                                             modification_name="HYDR")
        self.assertListEqual([report.atoms_added, report.atoms_deleted, report.atoms_renamed],
                             [2, 0, 1])
        atoms = list(list(modifier.get_structure().get_residues())[19].get_atoms())
        atom_names = [atom.get_name() for atom in atoms]

        self.assertListEqual(['N', "CA", 'C', 'O', "CB", "OD1", "ND2", 'H', "HA",
                              "HB2", "HB3", "HD21", "HD22", "CG2", "OG1", "HG1"],
                             atom_names)
        self.assertListEqual(list(atoms[14].get_coord()), [-5.165642997088467, 10.039277956283929, -1.0099377162671168])

    def test_to_pdb(self):
        # Creates temporary path
        temp_pdb_path = os.path.join(attach_root_path(UNITTEST_JUNK_FOLDER), "to_pdb_unittest.pdb")

        # Check if file exists, if so, delete it
        if os.path.exists(temp_pdb_path):
            os.remove(temp_pdb_path)

        # Generates a structure of class AnnotatedStructure
        structure = self._struc_io.from_pdb(path=self._1vii_PDB_path)

        # Write structure to temporary path
        structure.to_pdb(path=temp_pdb_path)

        self.assertTrue(os.path.exists(temp_pdb_path))
        self.assertGreater(os.path.getsize(temp_pdb_path), 30000)

