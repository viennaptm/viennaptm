import os


def move_directory_up(path: str, n=1) -> str:
    """
    Move up a given number of directory levels from a path.

    This function resolves the absolute path of the input and then
    iteratively ascends ``n`` directory levels. If the provided path
    points to a file, one additional level is traversed to account for
    the file itself.

    Examples
    --------
    >>> move_directory_up("/a/b/c/file.txt", n=1)
    '/a/b'

    >>> move_directory_up("/a/b/c", n=2)
    '/a'

    :param path:
        File or directory path from which to move upward.
    :type path: str

    :param n:
        Number of directory levels to ascend. If ``path`` refers to a file,
        the effective number of levels ascended is ``n + 1``.
    :type n: int

    :return:
        Absolute path obtained after moving up the specified number of
        directory levels.
    :rtype: str
    """

    # add +1 to take file into account
    if os.path.isfile(path):
        n += 1
    for _ in range(n):
        path = os.path.dirname(os.path.abspath(path))
    return path


def attach_root_path(path: str) -> str:
    """
    Prepend a path relative to the project root directory.

    The project root is determined by ascending two directory levels
    from the location of the current module file (``__file__``).
    The provided path is then joined to this root directory.

    This utility is typically used to construct absolute paths to
    bundled resources such as configuration files, libraries, or
    template data.

    :param path:
        Relative path to append to the project root.
    :type path: str

    :return:
        Absolute path formed by joining the project root directory
        with the given relative path.
    :rtype: str
    """

    abs_path = os.path.abspath(move_directory_up(__file__, n=2))
    return os.path.join(abs_path, path)
