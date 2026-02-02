import sys
import logging
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from datetime import datetime

from viennaptm.dataclasses.parameters.modifier_parameters import ModifierParameters

# --- various logging formats (one for DEBUG, one for INFO)
DEBUG_FORMAT = "%(asctime)s|%(name)s|%(levelname)s: %(message)s"
"""
Logging format used in debug mode.

Includes timestamp, logger name, log level, and message to aid
fine-grained debugging and traceability.
"""

DEBUG_DATEFMT = "%Y-%m-%d|%H:%M"
"""
Date format used in debug logging.

Applied only when debug logging is enabled.
"""

INFO_FORMAT = "%(levelname)s: %(message)s"
"""
Logging format used in non-debug (INFO) mode.

Provides concise log output suitable for CLI usage.
"""

def setup_file_logging(log_file: Path, debug: bool = False) -> None:
    """
    Configure logging to write to both a file and stdout.

    This function initializes the root logger using ``logging.basicConfig``.
    Log messages are written to the specified file and simultaneously
    echoed to the console.

    When debug mode is enabled, the logging level is set to ``DEBUG`` and
    a verbose format including timestamps and logger names is used.

    :param log_file:
        Path to the log file. The file is opened in append mode.
    :type log_file: pathlib.Path

    :param debug:
        If ``True``, enable DEBUG-level logging with verbose formatting.
        Otherwise, INFO-level logging with a concise format is used.
    :type debug: bool
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
    Configure logging to write to stdout only.

    This function initializes the root logger using ``logging.basicConfig``
    with a single console handler.

    When debug mode is enabled, DEBUG-level logging and verbose formatting
    (including timestamps) are activated.

    :param debug:
        If ``True``, enable DEBUG-level logging with verbose formatting.
        Otherwise, INFO-level logging with a concise format is used.
    :type debug: bool
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
    Create or return a dedicated logger for configuration reporting.

    The configuration logger is intended for printing resolved configuration
    values in a clean, human-readable format:

    * Messages are emitted without log level prefixes.
    * Output is always sent to stdout.
    * Optionally, messages are also written to the active log file.

    The logger does not propagate messages to the root logger and is
    initialized only once.

    :param include_file_handler:
        If ``True``, clone the active file handler from the root logger
        and attach it to this logger.
    :type include_file_handler: bool

    :return:
        A configured logger instance for configuration output.
    :rtype: logging.Logger
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
    """
    Retrieve the installed version of a Python package.

    If the package cannot be found in the current environment, the
    string ``"unknown"`` is returned instead of raising an exception.

    :param pkg_name:
        Name of the Python package.
    :type pkg_name: str

    :return:
        Installed package version or ``"unknown"`` if not available.
    :rtype: str
    """

    try:
        return version(pkg_name)
    except PackageNotFoundError:
        return "unknown"


def instantiate_logging_CLI(cfg: ModifierParameters, logger) -> None:
    """
    Initialize logging for command-line execution and emit a log header.

    This function performs the following steps:

    * Configures logging based on the resolved CLI configuration
      (console-only or file + console).
    * Logs the execution start timestamp.
    * Logs the installed Vienna-PTM package version.
    * Logs the fully resolved configuration with a dedicated configuration logger.

    CLI arguments override configuration file values when both are present.

    :param cfg:
        Resolved modifier configuration parameters.
    :type cfg: ModifierParameters

    :param logger:
        Logger used for general execution messages.
    :type logger: logging.Logger
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
