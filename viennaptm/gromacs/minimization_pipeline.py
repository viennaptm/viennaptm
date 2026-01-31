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
    Run an energy minimization starting from a processed GRO file
    and write out a minimized PDB. Does not include pdb2gmx.

    Parameters
    ----------
    conf_gro : Path
        Input structure (from pdb2gmx)
    topology : Path
        GROMACS topology file
    minim_mdp : Path
        Energy minimization MDP file
    workdir : Path
        Working directory

    Returns
    -------
    Path
        Path to the minimized PDB file
    """
    boxed = workdir / "boxed.gro"
    tpr = workdir / "em.tpr"
    minimized = workdir / "em.gro"
    minimized_pdb = workdir / "em.pdb"

    # ---- define box ----
    EditConf(
        input_gro=conf_gro,
        output_gro=boxed,
        workdir=workdir,
    ).run()

    Grompp(
        mdp=minim_mdp,
        structure=boxed,
        topology=topology,
        tpr=tpr,
        workdir=workdir,
    ).run()

    Mdrun(
        deffnm="em",
        workdir=workdir,
    ).run()

    Trjconv(
        structure=minimized,
        tpr=tpr,
        output_pdb=minimized_pdb,
        workdir=workdir,
    ).run()

    return minimized_pdb
