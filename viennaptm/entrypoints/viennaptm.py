import logging
import re
import sys

from pathlib import Path
from typing import Union, Optional, Literal
from pydantic import BaseModel, field_validator

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.modification.modification.modifier import Modifier
from viennaptm.utils.entrypoint_helper import collect_kwargs

# logger settings
def setup_file_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        handlers=[
            logging.FileHandler("viennaptm.log", mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def setup_console_logging() -> None:
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
        Pydantic model containing parameters for a structure modification task.

        :param input: Path object or string pointing to the input structure.
        :type input: Union[Path, str]

        :param modification: One or more modifications to apply. For example, ``--modification "A:50=V3H" "Y:65=Y1P"``.
        :type modification: Union[list[str], str]

        :param output_pdb: Output PDB filename or Path object. Defaults to ``"output.pdb"``.
        :type output_pdb: Optional[Union[Path, str]]

        :param logger: Logging mode, either ``"console"`` or ``"file"``. Defaults to ``"console"``.
        :type logger: Literal['console', 'file']
        """

    input: Union[Path, str]
    modification: Union[list[str], str]
    output_pdb: Optional[Union[Path, str]] = "output.pdb"

    logger: Literal['console', 'file'] = 'console'

    @field_validator("output_pdb", mode="after")
    @classmethod
    def validate_output_pdb(cls, out: Union[Path, str]) -> Path:
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
        # lists are mutable, therefore use [] to generate new list in memory
        if isinstance(input_modification, str):
            input_modification = [input_modification]
        return input_modification

    @field_validator("input", mode="after")
    @classmethod
    def validate_file_input(cls, inp: Union[Path, str]):
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
