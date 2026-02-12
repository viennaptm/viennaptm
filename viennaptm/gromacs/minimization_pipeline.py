import logging
import shutil
import tempfile
from pathlib import Path
from typing import Union

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.gromacs.editconf import EditConf
from viennaptm.gromacs.grompp import Grompp
from viennaptm.gromacs.mdrun import Mdrun
from viennaptm.gromacs.pdb2gmx import PDB2GMX, PDB2GMXParameters
from viennaptm.gromacs.trjconv import Trjconv
from viennaptm.utils.fixtures import ViennaPTMFixtures

logger = logging.getLogger(__name__)


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


def execute_energy_minimization(structure: AnnotatedStructure, workdir: Union[Path, str] = None, clean_up: bool = True) -> AnnotatedStructure:
    """
    Perform GROMACS-based energy minimization on a structure.

    The structure is written to a temporary or user-provided working
    directory, processed using a standard GROMACS minimization pipeline
    (``pdb2gmx`` followed by energy minimization), and reloaded as a new
    :class:`AnnotatedStructure` instance.

    If no working directory is provided, a temporary directory is created.
    Optionally, the working directory is removed after completion.

    :param structure: The input structure to be energy minimized.
    :type structure: AnnotatedStructure

    :param workdir: Directory in which GROMACS files are created and
                    executed. If ``None``, a temporary directory is used.
    :type workdir: str or pathlib.Path or None

    :param clean_up: Whether to remove the working directory after
                     successful minimization.
    :type clean_up: bool

    :return: The minimized structure reloaded from the resulting PDB file.
    :rtype: AnnotatedStructure

    :raises OSError: If working directory creation or deletion fails.
    :raises RuntimeError: If any GROMACS step in the minimization
                          pipeline fails.
    """

    # prepare temporary folder and input
    if not workdir:
        workdir = Path(tempfile.mkdtemp(suffix=None, prefix="viennaptm_", dir=None))
    else:
        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Executing energy minimization in this directory: {workdir}")
    input_path = workdir / "input.pdb"
    structure.to_pdb(input_path.resolve())

    # prepare GROMACS paths
    conf_gro = workdir / "conf.gro"
    topol = workdir / "topol.top"
    minim_mdp = ViennaPTMFixtures().GROMACS_MINIM_MDP_DEFAULT

    # execute PDB2GMX
    PDB2GMX(
        params=PDB2GMXParameters(
            input=input_path,
            output_gro=conf_gro,
            topology=topol,
            forcefield="gromos54a7",
            water="spc",
            ignore_h=True
        ),
        workdir=workdir,
        stdin="1\n",
    ).run()

    # execute remaining energy minimization pipeline
    minimized_path = minimize_and_write_pdb(
        conf_gro=conf_gro,
        topology=topol,
        minim_mdp=minim_mdp,
        workdir=workdir
    )

    # reload, clean up (if set to True) and return minimized structure
    minimized_structure = AnnotatedStructure.from_pdb(minimized_path)
    if clean_up:
        shutil.rmtree(workdir)
    return minimized_structure
