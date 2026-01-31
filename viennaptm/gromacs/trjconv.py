from pathlib import Path
from viennaptm.gromacs.gromacs_command import GromacsCommand


class Trjconv(GromacsCommand):
    def __init__(
        self,
        structure: Path,
        tpr: Path,
        output_pdb: Path,
        **kwargs,
    ):
        self.structure = structure
        self.tpr = tpr
        self.output_pdb = output_pdb
        super().__init__(stdin="0\n", **kwargs)

    def build_gromacs_cmd(self):
        return [
            self.gmx_bin, "trjconv",
            "-s", str(self.tpr),
            "-f", str(self.structure),
            "-o", str(self.output_pdb),
        ]

    def expected_outputs(self):
        return [self.output_pdb]
