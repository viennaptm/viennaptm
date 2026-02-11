import os
import shutil


def resolve_gmx_binary() -> str:
    """
    Determine the GROMACS executable to invoke.

    The GROMACS binary is resolved using the following precedence:

    1. The ``GMX_BIN`` environment variable, if defined.
    2. The ``gmx`` executable discovered on the system ``PATH``.

    This function does not validate the GROMACS version; it only
    ensures that an executable can be located.

    :return:
        Path to the GROMACS executable or its command name.
    :rtype: str

    :raises RuntimeError:
        If neither the ``GMX_BIN`` environment variable is set nor a
        ``gmx`` executable can be found on the system ``PATH``.
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
