from pathlib import Path
from viennaptm.gromacs.gromacs_command import GromacsCommand


class EditConf(GromacsCommand):
    def __init__(self, input_gro: Path, output_gro: Path, **kwargs):
        self.input_gro = input_gro
        self.output_gro = output_gro
        super().__init__(**kwargs)

    def build_gromacs_cmd(self):
        return [
            self.gmx_bin, "editconf",
            "-f", str(self.input_gro),
            "-o", str(self.output_gro),
            "-c",
            "-d", "1.0",
            "-bt", "cubic",
        ]

    def expected_outputs(self):
        return [self.output_gro]
