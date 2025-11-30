import os
from pathlib import Path

from pydantic import BaseModel, model_validator

from viennaptm.utils.paths import attach_root_path


class ViennaPTMFixtures(BaseModel):
    LATEST_PTMS_VERSION_DATE: str = "2025-11-30"
    LATEST_PTMS_LIBRARY_PATH: Path = None
    LATEST_PTMS_PDBS_DIR_PATH: Path = None

    PDB_ENDING: str = ".pdb"

    @model_validator(mode="after")
    def ptms_fixture_validator(self):
        self.LATEST_PTMS_LIBRARY_PATH = attach_root_path(os.path.join("viennaptm",
                                                                      "resources",
                                                                      "libraries",
                                                                      self.LATEST_PTMS_VERSION_DATE,
                                                                      "library.json"))
        self.LATEST_PTMS_PDBS_DIR_PATH = attach_root_path(os.path.join("viennaptm",
                                                                       "resources",
                                                                       "pdbs_minimized",
                                                                       self.LATEST_PTMS_VERSION_DATE))
        return self
