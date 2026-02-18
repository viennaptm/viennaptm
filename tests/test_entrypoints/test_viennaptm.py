import os
import subprocess
import unittest
import shutil
from pathlib import Path

from tests.file_paths import UNITTEST_PATH_1VII_PDB, UNITTEST_JUNK_FOLDER
from tests.helper_functions import get_aa_sequence_from_file
from viennaptm.utils.paths import attach_root_path


class Test_ViennaPTM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._workdir = Path(attach_root_path(UNITTEST_JUNK_FOLDER)) / "entrypoints"

        # remove lingering artefact from previous runs, if present
        if os.path.exists(cls._workdir):
            shutil.rmtree(cls._workdir)
        cls._workdir.mkdir(parents=True, exist_ok=True)

    def setUp(self):
        self._1vii_PDB_path = attach_root_path(UNITTEST_PATH_1VII_PDB)

    def tearDown(self):
        pass

    def test_viennaptm_modification_only_pdb(self):
        # test legacy PDB generation
        output_path = self._workdir / "modification_only.pdb"
        result = subprocess.run(
            [
                "viennaptm",
                "--input", str(self._1vii_PDB_path),
                "--modify", "A:50=V3H",
                "--output", str(output_path)
            ],
            capture_output=True,
            text=True
        )

        # file creation sanity check
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 44000)

        # check successful modification
        aa_seq = get_aa_sequence_from_file(output_path)
        self.assertListEqual(aa_seq['A'], [
                             "MET", "LEU", "SER", "ASP", "GLU", "ASP", "PHE",
                             "LYS", "ALA", "V3H", "PHE", "GLY", "MET", "THR",
                             "ARG", "SER", "ALA", "PHE", "ALA", "ASN", "LEU",
                             "PRO", "LEU", "TRP", "LYS", "GLN", "GLN", "ASN",
                             "LEU", "LYS", "LYS", "GLU", "LYS", "HIS", "CYS",
                             "TYR"])

    def test_viennaptm_modification_only_cif(self):
        # test mmCIF generation
        output_path = self._workdir / "modification_only.cif"
        result = subprocess.run(
            [
                "viennaptm",
                "--input", str(self._1vii_PDB_path),
                "--modify", "A:50=V3H",
                "--output", str(output_path)
            ],
            capture_output=True,
            text=True
        )

        # file creation sanity check
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 40000)

        # check successful modification
        aa_seq = get_aa_sequence_from_file(output_path)
        self.assertListEqual(aa_seq['A'], [
                             "MET", "LEU", "SER", "ASP", "GLU", "ASP", "PHE",
                             "LYS", "ALA", "V3H", "PHE", "GLY", "MET", "THR",
                             "ARG", "SER", "ALA", "PHE", "ALA", "ASN", "LEU",
                             "PRO", "LEU", "TRP", "LYS", "GLN", "GLN", "ASN",
                             "LEU", "LYS", "LYS", "GLU", "LYS", "HIS", "CYS",
                             "TYR"])

    def test_viennaptm_minimization_pdb(self):
        if shutil.which("gmx") is None:
            raise unittest.SkipTest("GROMACS (gmx) not available.")

        # test mmCIF generation
        output_path = self._workdir / "minimization.pdb"
        result = subprocess.run(
            [
                "viennaptm",
                "--input", str(self._1vii_PDB_path),
                # TODO: enable, once force-field parameters are installed
                #"--modify", "A:50=V3H",
                "--gromacs.minimize", "True",
                "--output", str(output_path)
            ],
            capture_output=True,
            text=True
        )

        # file creation sanity check
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 27000)
