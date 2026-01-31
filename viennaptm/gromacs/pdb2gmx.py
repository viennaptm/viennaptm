import logging
from pydantic import Field, field_validator, BaseModel
from typing import List, Optional
from pathlib import Path

from viennaptm.gromacs.gromacs_command import GromacsCommand, MPIConfig

logger = logging.getLogger(__name__)


class PDB2GMXParameters(BaseModel):
    input: Path

    output_gro: Path = Field(Path("conf.gro"))
    topology: Path = Field(Path("topol.top"))
    posre_itp: Optional[Path] = Field(Path("posre.itp"))
    index_file: Optional[Path] = None
    clean_pdb: Optional[Path] = None

    forcefield: Optional[str] = None
    water: Optional[str] = None

    chainsep: Optional[str] = None
    merge: Optional[str] = None

    ignore_h: bool = False
    verbose: bool = False

    @field_validator(
        "input",
        "output_gro",
        "topology",
        "posre_itp",
        "index_file",
        "clean_pdb",
        mode="after",
    )
    @classmethod
    def ensure_paths(cls, v):
        return Path(v) if v is not None else v


class PDB2GMX(GromacsCommand):
    def __init__(
        self,
        params: PDB2GMXParameters,
        mpi: Optional[MPIConfig] = None,
        workdir: Optional[Path] = None,
        stdin: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[dict] = None,
    ):
        self.params = params

        super().__init__(
            mpi=mpi,
            workdir=workdir,
            stdin=stdin,
            timeout=timeout,
            env=env,
        )

    def build_gromacs_cmd(self) -> List[str]:
        p = self.params

        cmd = [
            self.gmx_bin,
            "pdb2gmx",
            "-f", str(p.input),
            "-o", str(p.output_gro),
            "-p", str(p.topology),
        ]

        if p.posre_itp:
            cmd += ["-i", str(p.posre_itp)]
        if p.index_file:
            cmd += ["-n", str(p.index_file)]
        if p.clean_pdb:
            cmd += ["-q", str(p.clean_pdb)]

        if p.forcefield:
            cmd += ["-ff", p.forcefield]
        if p.water:
            cmd += ["-water", p.water]

        if p.chainsep:
            cmd += ["-chainsep", p.chainsep]
        if p.merge:
            cmd += ["-merge", p.merge]

        if p.ignore_h:
            cmd.append("-ignh")
        if p.verbose:
            cmd.append("-v")

        return cmd

    def expected_outputs(self) -> List[Path]:
        outputs = [
            self.params.output_gro,
            self.params.topology,
        ]
        return outputs
