from pathlib import Path
from viennaptm.gromacs.gromacs_command import GromacsCommand


class Grompp(GromacsCommand):
    def __init__(
        self,
        mdp: Path,
        structure: Path,
        topology: Path,
        tpr: Path,
        **kwargs,
    ):
        self.mdp = mdp
        self.structure = structure
        self.topology = topology
        self.tpr = tpr
        super().__init__(**kwargs)

    def build_gromacs_cmd(self):
        return [
            self.gmx_bin, "grompp",
            "-f", str(self.mdp),
            "-c", str(self.structure),
            "-p", str(self.topology),
            "-o", str(self.tpr),
            "-maxwarn", "50"
        ]

    def expected_outputs(self):
        return [self.tpr]
