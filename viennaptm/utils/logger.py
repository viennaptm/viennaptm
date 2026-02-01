import sys
import logging
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from datetime import datetime

from viennaptm.dataclasses.parameters.modifier_parameters import ModifierParameters

# --- various logging formats (one for DEBUG, one for INFO)
DEBUG_FORMAT = "%(asctime)s|%(name)s|%(levelname)s: %(message)s"
DEBUG_DATEFMT = "%Y-%m-%d|%H:%M"
INFO_FORMAT = "%(levelname)s: %(message)s"


def setup_file_logging(log_file: Path, debug: bool = False) -> None:
    """
    Configure logging to write to a file and the console.

    Debug mode enables verbose formatting and DEBUG level.
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format=DEBUG_FORMAT if debug else INFO_FORMAT,
        datefmt=DEBUG_DATEFMT if debug else None,
        handlers=[
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def setup_console_logging(debug: bool = False) -> None:
    """
    Configure console logging.

    Debug mode enables verbose formatting and DEBUG level.
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format=DEBUG_FORMAT if debug else INFO_FORMAT,
        datefmt=DEBUG_DATEFMT if debug else None,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_config_logger(include_file_handler: bool = False) -> logging.Logger:
    """
    Logger for recording the resolved configuration.

    - Always logs to stdout with no prefix.
    - Optionally also logs to the active file handler.
    """
    logger = logging.getLogger("modifier.config")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Plain stdout handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stream_handler)

    if include_file_handler:
        root = logging.getLogger()

        for handler in root.handlers:
            if isinstance(handler, logging.FileHandler):
                # Clone file handler safely
                file_handler = logging.FileHandler(
                    handler.baseFilename,
                    mode="a",
                    encoding=getattr(handler, "encoding", None),
                    delay=True,
                )
                file_handler.setFormatter(logging.Formatter("%(message)s"))
                logger.addHandler(file_handler)
                break

    return logger


def get_package_version(pkg_name: str) -> str:
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        return "unknown"


def instantiate_logging_CLI(cfg: ModifierParameters, logger) -> None:
    """
    Initialize logging and log header.

      - Configures logging (console or file and console).
      - Logs the package version.
      - Logs the resolved configuration.
    """

    # initialize logging
    if cfg.is_console_logging():
        setup_console_logging(debug=cfg.debug)
    else:
        setup_file_logging(cfg.log_file_path(), debug=cfg.debug)

    # log (localized) execution start
    logger.info("Starting execution: %s",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # log header region with package version number installed
    pkg_version = get_package_version("viennaptm")
    logging.getLogger().info("Vienna-PTM version installed: %s", pkg_version)

    # log resolved configuration: --config (if used) is the base, CLI arguments override selectively
    config_logger = get_config_logger(include_file_handler=not cfg.is_console_logging())
    config_logger.info("Resolved configuration:\n%s", cfg.dump_resolved_config())
