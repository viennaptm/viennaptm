import unittest

from modification.modifier import Modifier
from tests.file_paths import UNITTEST_PATH_1VII_PDB
from utils.paths import attach_root_path
from IOclasses.iostructures import IOStructure


class Test_Modification(unittest.TestCase):

    def setUp(self):
        self._struc_io = IOStructure()
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)

    def test_apply_modifications(self):
        # load internal PDB file
        structure = self._struc_io.from_pdb_file(path=self._1vii_PDB_path)

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
