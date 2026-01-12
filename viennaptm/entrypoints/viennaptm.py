import logging
import re
import sys

from pathlib import Path
from typing import Union, Optional, Literal
from pydantic import BaseModel, field_validator

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.modification.application.modifier import Modifier
from viennaptm.utils.entrypoint_helper import collect_kwargs

# logger settings
def setup_file_logging() -> None:
    """
    Configure logging to write both to a file and to the console.

    This function initializes the root logger using :func:`logging.basicConfig`.
    Log messages are written to a file named ``viennaptm.log`` (append mode,
    UTF-8 encoded) and simultaneously streamed to standard output.

    The logging level is set to ``INFO``.

    :return: None
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        handlers=[
            logging.FileHandler("viennaptm.log", mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def setup_console_logging() -> None:
    """
    Configure logging to write only to the console.

    This function initializes the root logger using :func:`logging.basicConfig`
    with output directed exclusively to standard output. The logging level
    is set to ``INFO``.

    :return: None
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger(__name__)


class ModifierParameters(BaseModel):
    """
    Pydantic model defining configuration parameters for a structure modification run.

    This model validates user input for loading a :class:`Biopython PDB structure`, applying
    one or more residue modifications, selecting a logging mode, and
    defining the output file.

    :param input:
        Either a path to a local PDB file or a four-character `PDB database identifier <https://www.rcsb.org/>`_.
    :type input: Union[pathlib.Path, str]

    :param modification:
        One or more modification strings of the form ``"A:50=V3H"``.
        Multiple modifications may be supplied as a list.
    :type modification: Union[list[str], str]

    :param output_pdb:
        Output PDB filename or path. Must end with ``.pdb``.
    :type output_pdb: Optional[Union[pathlib.Path, str]]

    :param logger:
        Logging mode. Either ``"console"`` or ``"file"``.
    :type logger: Literal['console', 'file']
    """

    input: Union[Path, str]
    modification: Union[list[str], str]
    output_pdb: Optional[Union[Path, str]] = "output.pdb"

    logger: Literal['console', 'file'] = 'console'

    @field_validator("output_pdb", mode="after")
    @classmethod
    def validate_output_pdb(cls, out: Union[Path, str]) -> Path:
        """
        Validate the output PDB path.

        Ensures that the output filename ends with the ``.pdb`` suffix and
        converts string paths to :class:`pathlib.Path`.

        :param out: Output path or filename.
        :type out: Union[pathlib.Path, str]

        :raises ValueError:
            If the output file does not end with ``.pdb``.

        :return: Validated output path.
        :rtype: pathlib.Path
        """

        if isinstance(out, str):
            out = Path(out)
        if out.suffix == ".pdb":
            pass
        else:
            raise ValueError("Output must be PDB format (ending must be \".pdb\").")
        return out

    @field_validator("modification", mode="after")
    @classmethod
    def validate_input_modification(cls, input_modification: Union[list[str], str]) -> list[str]:
        """
        Normalize modification input to a list of strings.

        Single modification strings are wrapped into a list to ensure
        consistent downstream handling.

        :param input_modification: Modification or list of modifications.
        :type input_modification: Union[list[str], str]

        :return: List of modification strings.
        :rtype: list[str]
        """

        # lists are mutable, therefore use [] to generate new list in memory
        if isinstance(input_modification, str):
            input_modification = [input_modification]
        return input_modification

    @field_validator("input", mode="after")
    @classmethod
    def validate_file_input(cls, inp: Union[Path, str]):
        """
        Validate the input structure source.

        If the input is a string ending with ``.pdb``, it is interpreted as a
        file path and converted to :class:`pathlib.Path`. Otherwise, the string
        is interpreted as a PDB database identifier and must be exactly four
        characters long.

        :param inp: Input path or PDB identifier.
        :type inp: Union[pathlib.Path, str]

        :raises ValueError:
            If a database identifier is not exactly four characters long.

        :return: Validated input value.
        :rtype: Union[pathlib.Path, str]
        """

        if isinstance(inp, str):
            if inp.lower()[-4:] == ".pdb":
                # If input ends with ".pdb" assume it is a path
                inp = Path(inp)
            else:
                # Assume that string is database identifier
                if len(inp) != 4:
                    raise ValueError(f"Database identifier are exactly 4 characters long. Input {inp} does not conform.")
        return inp


def main():
    """
    Entry point for the :class:`AnnotatedStructure` modification command-line interface.

    This function:
    - Parses command-line arguments
    - Validates parameters using :class:`ModifierParameters`
    - Initializes logging
    - Loads a :class:`Biopython PDB structure` (local file or database)
    - Applies one or more residue modifications
    - Writes the modified :class:`AnnotatedStructure` to a PDB file

    :raises ValueError:
        If modification strings do not conform to the expected format.
    """

    raw_kwargs = collect_kwargs(sys.argv)
    cfg = ModifierParameters(**raw_kwargs)

    # initialize logging; file logging also prints to console
    # model only allows file or console as values (pydantic)
    if cfg.logger == "file":
        setup_file_logging()
    elif cfg.logger == "console":
        setup_console_logging()

    # load internal PDB file
    if isinstance(cfg.input, Path):
        structure = AnnotatedStructure.from_pdb(path=cfg.input)
    else:
        structure = AnnotatedStructure.from_pdb_db(identifier=cfg.input)

    # initialize modifier with most recent internal modification database
    modifier = Modifier()

    modlist = cfg.modification
    for mod_input in modlist:
        modification = (re.split(":|=", mod_input))
        if not len(modification[0]) == 1:
            raise ValueError(f"Modification input needs to be a string of format 'A:50=V3H' "
                             f"with the chain identifier being a string of length 1.")

        # check, whether the second string element (residue number) can be cast to an integer
        _ = int(modification[1])

        if not len(modification[2]) == 3:
            raise ValueError(f"Modification input needs to be a string of format 'A:50=V3H' "
                             f"with the target residue abbreviation being a string of length 3.")

        # apply a modification
        structure = modifier.apply_modification(structure = structure,
                                                chain_identifier=modification[0],
                                                residue_number=int(modification[1]),
                                                target_abbreviation=modification[2])

        logger.debug(f"Modification with parameters: "
                     f"chain identifier {modification[0]}, "
                     f"residue number {modification[1]} and"
                     f"target abbreviation {modification[2]} has been successfully applied.")

    # write modified pdb
    structure.to_pdb(str(cfg.output_pdb))
    logger.debug(f"Wrote structure to temporary PDB file: {cfg.output_pdb}")

if __name__ == "__main__":
    main()
