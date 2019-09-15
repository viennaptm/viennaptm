import os

def move_directory_up(path, n=1):
    """Function, to move up "n" directories for a given "path"."""
    # add +1 to take file into account
    if os.path.isfile(path):
        n += 1
    for _ in range(n):
        path = os.path.dirname(os.path.abspath(path))
    return path
