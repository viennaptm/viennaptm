from pathlib import Path
from viennaptm.gromacs.gromacs_command import GromacsCommand


class Mdrun(GromacsCommand):
    def __init__(self, deffnm: str, **kwargs):
        self.deffnm = deffnm
        super().__init__(**kwargs)

    def build_gromacs_cmd(self):
        return [
            self.gmx_bin, "mdrun",
            "-deffnm", self.deffnm,
        ]

    def expected_outputs(self):
        if self.workdir:
            return [self.workdir / f"{self.deffnm}.gro"]
        return [Path(f"{self.deffnm}.gro")]
