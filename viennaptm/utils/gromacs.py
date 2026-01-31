import os
import shutil


def resolve_gmx_binary() -> str:
    """
    Resolve the GROMACS binary to use.

    Resolution order:
    1. GMX_BIN environment variable
    2. `gmx` on PATH

    Returns
    -------
    str
        Absolute path or executable name for gmx.

    Raises
    ------
    RuntimeError
        If no GROMACS binary can be found.
    """
    gmx = os.environ.get("GMX_BIN")
    if gmx:
        return gmx

    gmx = shutil.which("gmx")
    if gmx:
        return gmx

    raise RuntimeError(
        "GROMACS binary not found. "
        "Set GMX_BIN or ensure `gmx` is within PATH."
    )
