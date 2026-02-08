import os
import unittest
import shutil
from pathlib import Path

from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.gromacs.minimization_pipeline import execute_energy_minimization
from viennaptm.utils.fixtures import ViennaPTMFixtures
from viennaptm.utils.paths import attach_root_path


class Test_MinimizeAndWritePDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if shutil.which("gmx") is None:
            raise unittest.SkipTest("GROMACS (gmx) not available.")

        cls.gmx_bin = shutil.which("gmx")

        # remove lingering artefact from previous runs, if present
        cls._workdir = Path(os.path.join(attach_root_path(UNITTEST_JUNK_FOLDER))) / "minimization_pipeline"
        if os.path.exists(cls._workdir):
            shutil.rmtree(cls._workdir)
        cls._workdir.mkdir(parents=True, exist_ok=True)

    def setUp(self):
        self._pdb = attach_root_path(UNITTEST_PATH_1VII_PDB)
        self._structure = AnnotatedStructure.from_pdb(self._pdb)
        self._minim_mdp = ViennaPTMFixtures().GROMACS_MINIM_MDP_DEFAULT

    def tearDown(self):
        pass

    def test_CLI_minimize_pdb(self):
        minimized_structure = execute_energy_minimization(self._structure,
                                                          workdir=self._workdir,
                                                          clean_up=False)

        residues = [residue for residue in minimized_structure.get_residues()]
        self.assertEqual(len(residues), 36)

        atoms = [atom for atom in minimized_structure.get_atoms()]
        self.assertEqual(len(atoms), 398)

        atoms_original = [atom for atom in self._structure.get_atoms()]
        self.assertListEqual([-0.15, -8.75, -7.26], [round(x, 2) for x in atoms_original[6].coord])
        self.assertListEqual([25.19, 18.06, 18.3], [round(x, 2) for x in atoms[6].coord])
