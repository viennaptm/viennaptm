import logging

from pydantic import BaseModel, Field
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from pathlib import Path

from viennaptm.utils.gromacs import resolve_gmx_binary

logger = logging.getLogger(__name__)


class MPIConfig(BaseModel):
    enabled: bool = False
    np: int = Field(1, ge=1)
    launcher: str = "mpirun"


class GromacsCommand(ABC):
    """
    Base class for all GROMACS commands.
    """

    def __init__(
        self,
        gmx_bin: Optional[str] = None,
        mpi: Optional[MPIConfig] = None,
        workdir: Optional[Path] = None,
        stdin: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[Dict[str, str]] = None
    ):
        self.gmx_bin = gmx_bin or resolve_gmx_binary()
        self.mpi = mpi or MPIConfig()
        self.workdir = workdir
        self.stdin = stdin
        self.timeout = timeout
        self.env = env

    def mpi_prefix(self) -> List[str]:
        if not self.mpi.enabled:
            return []
        return [self.mpi.launcher, "-np", str(self.mpi.np)]

    @abstractmethod
    def build_gromacs_cmd(self) -> List[str]:
        pass

    def build_command(self) -> List[str]:
        return self.mpi_prefix() + self.build_gromacs_cmd()

    def run(self) -> subprocess.CompletedProcess:
        cmd = self.build_command()
        logger.info("Executing: %s", " ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                cwd=self.workdir,
                input=self.stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout,
                env=self.env
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("GROMACS command timed out")

        logger.info(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)

        self.inspect_result(result)
        self.post_run_checks()

        return result

    def inspect_result(self, result: subprocess.CompletedProcess) -> None:
        fatal_markers = (
            "Fatal error",
            "Segmentation fault",
            "MPI_ABORT",
        )

        combined = "\n".join(
            s for s in (result.stderr, result.stdout) if s
        )

        for marker in fatal_markers:
            if marker in combined:
                # extract a readable error snippet
                lines = combined.splitlines()
                start = next((i for i, line in enumerate(lines) if marker in line), 0)
                snippet = "\n".join(lines[start:start + 20])

                raise RuntimeError(
                    "GROMACS fatal error detected:\n"
                    + snippet
                )

    @abstractmethod
    def expected_outputs(self) -> List[Path]:
        pass

    def post_run_checks(self) -> None:
        for path in self.expected_outputs():
            if not path.exists():
                raise FileNotFoundError(
                    f"Expected output missing: {path}"
                )
