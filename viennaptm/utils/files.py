import os


def file_exists(path, check_content: bool = False) -> bool:
    # check if file exists and has (any) content; it is possible that file was created
    # but could not be written to
    if os.path.isfile(path):
        if check_content and os.path.getsize(path) == 0:
            return False
        return True
    return False


def log_writeout(logger, path):
    if file_exists(path, check_content=True):
        logger.info(f"Data saved to {path}")
    else:
        logger.warning(f"Data could not be saved to {path}.")
