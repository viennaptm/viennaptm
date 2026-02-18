import logging
from pydantic import Field, field_validator, BaseModel
from typing import List, Optional
from pathlib import Path

from viennaptm.gromacs.gromacs_command import GromacsCommand, MPIConfig

logger = logging.getLogger(__name__)


class PDB2GMXParameters(BaseModel):
    """
    Parameter model for the GROMACS ``pdb2gmx`` command.

    This model defines all input and output paths as well as optional
    command-line flags controlling force-field selection, water model,
    chain handling, and verbosity.

    All path-like parameters are normalized to :class:`pathlib.Path`
    instances after validation.

    :param input:
        Input PDB structure file.
    :type input: pathlib.Path
    :param output_gro:
        Output GRO structure file.
    :type output_gro: pathlib.Path
    :param topology:
        Output topology file.
    :type topology: pathlib.Path
    :param posre_itp:
        Position restraint include file.
    :type posre_itp: pathlib.Path or None
    :param index_file:
        Optional index file.
    :type index_file: pathlib.Path or None
    :param clean_pdb:
        Optional cleaned PDB output file.
    :type clean_pdb: pathlib.Path or None
    :param forcefield:
        Force-field identifier passed to ``pdb2gmx``.
    :type forcefield: str or None
    :param water:
        Water model identifier.
    :type water: str or None
    :param chainsep:
        Chain separation mode.
    :type chainsep: str or None
    :param merge:
        Chain merge behavior.
    :type merge: str or None
    :param ignore_h:
        Ignore hydrogen atoms present in the input structure.
    :type ignore_h: bool
    :param verbose:
        Enable verbose output.
    :type verbose: bool
    """

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
        mode="after"
    )
    @classmethod
    def ensure_paths(cls, v):
        return Path(v) if v is not None else v


class PDB2GMX(GromacsCommand):
    """
    Wrapper for the GROMACS ``pdb2gmx`` topology generation command.

    This command converts a PDB structure into a GROMACS-compatible
    coordinate file and topology using the provided force-field and
    water model settings.

    Command-line arguments are derived from a
    :class:`PDB2GMXParameters` instance.

    :param params:
        Parameter model defining all ``pdb2gmx`` options.
    :type params: PDB2GMXParameters
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

    def __init__(
        self,
        params: PDB2GMXParameters,
        mpi: Optional[MPIConfig] = None,
        workdir: Optional[Path] = None,
        stdin: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[dict] = None
    ):
        self.params = params

        super().__init__(
            mpi=mpi,
            workdir=workdir,
            stdin=stdin,
            timeout=timeout,
            env=env
        )

    def build_gromacs_cmd(self) -> List[str]:
        """
        Construct the ``gmx pdb2gmx`` command invocation.

        Command-line arguments are conditionally assembled based on
        the values provided in the associated parameter model.

        :return:
            Command-line argument list suitable for execution.
        :rtype: list[str]
        """

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
        """
        Declare the files expected to be generated by this command.

        :return:
            List containing the generated GRO structure file and
            topology file.
        :rtype: list[pathlib.Path]
        """

        outputs = [
            self.params.output_gro,
            self.params.topology
        ]
        return outputs
