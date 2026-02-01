import os
import unittest
import shutil
from pathlib import Path

from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from viennaptm.gromacs.minimization_pipeline import minimize_and_write_pdb
from viennaptm.gromacs.pdb2gmx import PDB2GMX, PDB2GMXParameters
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
        self._minim_mdp = ViennaPTMFixtures().GROMACS_MINIM_MDP_DEFAULT

    def tearDown(self):
        pass

    def test_minimize_and_write_pdb(self):
        conf_gro = self._workdir / "conf.gro"
        topol = self._workdir / "topol.top"

        PDB2GMX(
            params=PDB2GMXParameters(
                input=self._pdb,
                output_gro=conf_gro,
                topology=topol,
                forcefield="gromos54a7",
                water="spc",
                ignore_h=True
            ),
            workdir=self._workdir,
            stdin="1\n",
        ).run()

        self.assertTrue(conf_gro.exists())
        self.assertTrue(topol.exists())

        minimized_pdb = minimize_and_write_pdb(
            conf_gro=conf_gro,
            topology=topol,
            minim_mdp=self._minim_mdp,
            workdir=self._workdir
        )

        self.assertTrue(minimized_pdb.exists())
        self.assertEqual(minimized_pdb.suffix, ".pdb")
        self.assertGreater(minimized_pdb.stat().st_size, 0)
