from pathlib import Path

from viennaptm.gromacs.editconf import EditConf
from viennaptm.gromacs.grompp import Grompp
from viennaptm.gromacs.mdrun import Mdrun
from viennaptm.gromacs.trjconv import Trjconv


def minimize_and_write_pdb(
    conf_gro: Path,
    topology: Path,
    minim_mdp: Path,
    workdir: Path,
) -> Path:
    """
    Run an energy minimization workflow and write a minimized PDB file.

    This function performs a minimal GROMACS preprocessing and execution
    pipeline starting from an existing GRO structure. The workflow
    defines a simulation box, preprocesses inputs, runs an energy
    minimization, and converts the minimized structure to PDB format.

    The workflow assumes that topology generation (e.g. via
    ``pdb2gmx``) has already been performed.

    :param conf_gro:
        Input GRO structure file.
    :type conf_gro: pathlib.Path
    :param topology:
        GROMACS topology file.
    :type topology: pathlib.Path
    :param minim_mdp:
        Energy minimization MDP parameter file.
    :type minim_mdp: pathlib.Path
    :param workdir:
        Working directory used for all intermediate and output files.
    :type workdir: pathlib.Path
    :return:
        Path to the minimized PDB file.
    :rtype: pathlib.Path
    """

    boxed = workdir / "boxed.gro"
    tpr = workdir / "em.tpr"
    minimized = workdir / "em.gro"
    minimized_pdb = workdir / "em.pdb"

    EditConf(
        input_gro=conf_gro,
        output_gro=boxed,
        workdir=workdir
    ).run()

    Grompp(
        mdp=minim_mdp,
        structure=boxed,
        topology=topology,
        tpr=tpr,
        workdir=workdir
    ).run()

    Mdrun(
        deffnm="em",
        workdir=workdir
    ).run()

    Trjconv(
        structure=minimized,
        tpr=tpr,
        output_pdb=minimized_pdb,
        workdir=workdir
    ).run()

    return minimized_pdb
