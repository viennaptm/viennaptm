import logging
import sys

from pathlib import Path
from typing import Union, Optional, Literal
from pydantic import BaseModel, field_validator
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

# pydantic model
class ModifierParameters(BaseModel):
    input_pdb: Union[Path, str]
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

    # TODO: integrate with actual business logic


def main():
    raw_kwargs = collect_kwargs(sys.argv)
    cfg = ModifierParameters(**raw_kwargs)

    # initialize logging; file logging also prints to console
    # model only allows file or console as values (pydantic)
    if cfg.logger == "file":
        setup_file_logging()
    elif cfg.logger == "console":
        setup_console_logging()

### TODO delete me:
#    print(cfg.output_pdb)
#    logger.info("testmessage")

if __name__ == "__main__":
    main()



