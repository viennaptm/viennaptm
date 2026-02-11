import os
import unittest
import shutil
from pathlib import Path

from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from viennaptm.gromacs.pdb2gmx import PDB2GMX, PDB2GMXParameters
from viennaptm.utils.paths import attach_root_path


class Test_PDB2GMX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if shutil.which("gmx") is None:
            raise unittest.SkipTest("GROMACS (gmx) not found on PATH")

    def setUp(self):
        self._workdir = Path(attach_root_path(UNITTEST_JUNK_FOLDER)) / "pdb2gmx"
        if os.path.exists(self._workdir):
            shutil.rmtree(self._workdir)
        self._workdir.mkdir(parents=True, exist_ok=True)

        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)

        self._output_gro = self._workdir / "conf.gro"
        self._topology = self._workdir / "topol.top"

        self.params = PDB2GMXParameters(
            input=self._1vii_PDB_path,
            output_gro=self._output_gro,
            topology=self._topology,
            forcefield="gromos54a7",
            water="spc",
            ignore_h=True
        )

    def tearDown(self):
        pass

    def test_pdb2gmx_execution(self):
        cmd = PDB2GMX(
            params=self.params,
            workdir=self._workdir,
            stdin="1\n"
        )

        result = cmd.run()

        self.assertEqual(result.returncode, 0)
        self.assertTrue(self._output_gro.exists())
        self.assertTrue(self._topology.exists())

        self.assertGreater(self._output_gro.stat().st_size, 0)
        self.assertGreater(self._topology.stat().st_size, 0)
