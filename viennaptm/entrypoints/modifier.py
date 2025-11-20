import logging
import pathlib
import sys
from typing import Union, Optional
from pydantic import BaseModel, FileUrl, FilePath, field_validator

# logger settings
logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")

logger = logging.getLogger(__name__)

# TODO: make unit test
class ModifierParameters(BaseModel):
    input_pdb: Union[FilePath, FileUrl]
    modification: list[str]
    output_pdb: Optional[FilePath] = "output.pdb"

    @field_validator("output_pdb", mode="after")
    def validate_output_pdb(self, out: FilePath) -> FilePath:
        if out.name[:-4] == ".pdb":
            pass
        else:
            raise ValueError("Output must be PDB format (ending must be \".pdb\").")
        return out




def main():
    pass

if __name__ == "__main__":
 #   sys.exit(main(sys.argv))
 # TODO: google to find how to parse CLI arguments in python using a pydantic BaseModel
    pass


#    def main(argv: list[str]) -> int:
#        argc: int = len(argv)  # get length of argv
#        n: int = int(argv[1])
#        print(n + 1)
#        return 0

