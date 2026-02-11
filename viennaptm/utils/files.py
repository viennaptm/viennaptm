import os


def file_exists(path, check_content: bool = False) -> bool:
    """
    Check whether a file exists and is optionally non-empty.

    This function verifies that the given path points to an existing
    regular file. If ``check_content`` is enabled, the file must also
    have a size greater than zero.

    :param path:
        Path to the file to check.
    :type path: str or pathlib.Path
    :param check_content:
        If ``True``, require the file to contain data.
    :type check_content: bool
    :return:
        ``True`` if the file exists (and is non-empty if requested),
        otherwise ``False``.
    :rtype: bool
    """

    # check if file exists and has (any) content; it is possible that file was created
    # but could not be written to
    if os.path.isfile(path):
        if check_content and os.path.getsize(path) == 0:
            return False
        return True
    return False


def log_writeout(logger, path):
    """
    Log the outcome of a file write operation.

    This function checks whether a file exists and contains data, and
    logs an informational message on success or a warning on failure.

    :param logger:
        Logger instance used to emit messages.
    :type logger: logging.Logger
    :param path:
        Path to the file that was written.
    :type path: str or pathlib.Path
    """

    if file_exists(path, check_content=True):
        logger.info(f"Data saved to {path}")
    else:
        logger.warning(f"Data could not be saved to {path}.")
