from pathlib import Path
from viennaptm.gromacs.gromacs_command import GromacsCommand


class Mdrun(GromacsCommand):
    """
    Wrapper for the GROMACS ``mdrun`` execution command.

    This class runs a molecular dynamics simulation using a prepared
    run input file (``.tpr``) identified by a default filename prefix.
    All standard GROMACS output files are generated using this prefix.

    :param deffnm:
        Default filename prefix for input and output files.
    :type deffnm: str
    :param kwargs:
        Additional keyword arguments forwarded to
        :class:`GromacsCommand`.
    :type kwargs: dict
    """

    def __init__(self, deffnm: str, **kwargs):
        self.deffnm = deffnm
        super().__init__(**kwargs)

    def build_gromacs_cmd(self):
        """
        Construct the ``gmx mdrun`` command invocation.

        The command uses the default filename prefix to locate the
        input ``.tpr`` file and generate all simulation output files.

        :return:
            Command-line argument list suitable for execution.
        :rtype: list[str]
        """

        return [
            self.gmx_bin, "mdrun",
            "-deffnm", self.deffnm
        ]

    def expected_outputs(self):
        """
        Declare the primary output files expected from the simulation.

        The output structure file (``.gro``) is resolved relative to
        the working directory if one is configured.

        :return:
            List containing the generated output structure file path.
        :rtype: list[pathlib.Path]
        """

        if self.workdir:
            return [self.workdir / f"{self.deffnm}.gro"]
        return [Path(f"{self.deffnm}.gro")]
