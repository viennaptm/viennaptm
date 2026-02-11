import logging

from pydantic import BaseModel, Field
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from pathlib import Path

from viennaptm.utils.gromacs import resolve_gmx_binary

logger = logging.getLogger(__name__)


class MPIConfig(BaseModel):
    """
    Configuration model for MPI execution settings.

    This model controls whether a GROMACS command is executed via MPI
    and defines the launcher command and number of processes to use.

    :param enabled:
        Whether MPI execution is enabled.
    :type enabled: bool
    :param np:
        Number of MPI processes to launch.
    :type np: int
    :param launcher:
        MPI launcher executable (e.g. ``mpirun`` or ``mpiexec``).
    :type launcher: str
    """

    enabled: bool = False
    np: int = Field(1, ge=1)
    launcher: str = "mpirun"


class GromacsCommand(ABC):
    """
    Abstract base class for all GROMACS command wrappers.

    This class provides common functionality for constructing,
    executing, and validating GROMACS command-line invocations,
    including optional MPI execution, environment handling, and
    post-run output validation.

    Subclasses must implement :meth:`build_gromacs_cmd` and
    :meth:`expected_outputs`.
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
        """
        Initialize a GROMACS command wrapper.

        :param gmx_bin:
            Path to the GROMACS executable. If ``None``, the binary
            is resolved automatically.
        :type gmx_bin: str or None
        :param mpi:
            MPI execution configuration.
        :type mpi: MPIConfig or None
        :param workdir:
            Working directory in which the command is executed.
        :type workdir: pathlib.Path or None
        :param stdin:
            Optional standard input passed to the command.
        :type stdin: str or None
        :param timeout:
            Maximum execution time in seconds.
        :type timeout: int or None
        :param env:
            Environment variables to use for command execution.
        :type env: dict[str, str] or None
        """

        self.gmx_bin = gmx_bin or resolve_gmx_binary()
        self.mpi = mpi or MPIConfig()
        self.workdir = workdir
        self.stdin = stdin
        self.timeout = timeout
        self.env = env

    def mpi_prefix(self) -> List[str]:
        """
        Construct the MPI command prefix.

        If MPI execution is disabled, an empty list is returned.
        Otherwise, the launcher and process count are included.

        :return:
            MPI command prefix suitable for prepending to the
            GROMACS command.
        :rtype: list[str]
        """

        if not self.mpi.enabled:
            return []
        return [self.mpi.launcher, "-np", str(self.mpi.np)]

    @abstractmethod
    def build_gromacs_cmd(self) -> List[str]:
        """
        Build the GROMACS command invocation.

        This method must be implemented by subclasses and should
        return the command arguments excluding any MPI prefix.

        :return:
            Command-line argument list for the GROMACS command.
        :rtype: list[str]
        """

        pass

    def build_command(self) -> List[str]:
        """
        Build the full command invocation.

        This includes the optional MPI prefix followed by the
        GROMACS command constructed by the subclass.

        :return:
            Complete command-line argument list.
        :rtype: list[str]
        """

        return self.mpi_prefix() + self.build_gromacs_cmd()

    def run(self) -> subprocess.CompletedProcess:
        """
        Execute the GROMACS command.

        The command is executed synchronously. Standard output and
        error streams are captured and inspected for fatal errors.

        :raises RuntimeError:
            If execution times out or a fatal GROMACS error is detected.
        :raises FileNotFoundError:
            If expected output files are missing after execution.
        :return:
            Completed subprocess result.
        :rtype: subprocess.CompletedProcess
        """

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
        """
        Inspect command output for fatal GROMACS errors.

        Both stdout and stderr are scanned for known fatal error
        markers. If detected, a readable error snippet is extracted
        and raised as an exception.

        :param result:
            Completed subprocess result to inspect.
        :type result: subprocess.CompletedProcess
        :raises RuntimeError:
            If a fatal GROMACS error marker is found.
        """

        fatal_markers = (
            "Fatal error",
            "Segmentation fault",
            "MPI_ABORT"
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
        """
        Declare output files expected from this command.

        Subclasses must return a list of paths that should exist
        after successful execution.

        :return:
            List of expected output file paths.
        :rtype: list[pathlib.Path]
        """

        pass

    def post_run_checks(self) -> None:
        """
        Verify that expected output files were created.

        :raises FileNotFoundError:
            If any expected output file is missing.
        """

        for path in self.expected_outputs():
            if not path.exists():
                raise FileNotFoundError(
                    f"Expected output missing: {path}"
                )
