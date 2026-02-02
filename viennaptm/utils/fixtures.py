import os
from pathlib import Path

from pydantic import BaseModel, model_validator

from viennaptm.utils.paths import attach_root_path


class ViennaPTMFixtures(BaseModel):
    """
    Container for file-system fixtures used by Vienna-PTM.

    This model centralizes paths to bundled resources such as the
    modification library, template PDB files, and default GROMACS
    parameter files. Paths are resolved relative to the project root
    during validation.

    The currently supported PTM library version is selected via a
    fixed version date.
    """

    # TODO: replace by actually looking for the latest one instead of hard-coding it
    LATEST_PTMS_VERSION_DATE: str = "2025-12-18"
    LATEST_PTMS_LIBRARY_PATH: Path = None
    LATEST_PTMS_PDBS_DIR_PATH: Path = None

    PDB_ENDING: str = ".pdb"

    GROMACS_MINIM_MDP_DEFAULT: Path = None

    @model_validator(mode="after")
    def ptms_fixture_validator(self):
        """
        Resolve and attach default fixture paths.

        This validator populates internal path attributes for the
        modification library, minimized PDB templates, and default
        GROMACS energy minimization parameters based on the configured
        PTM version date.

        :return:
            The validated fixture configuration instance.
        :rtype: ViennaPTMFixtures
        """

        self.LATEST_PTMS_LIBRARY_PATH = attach_root_path(os.path.join("viennaptm",
                                                                      "resources",
                                                                      "libraries",
                                                                      self.LATEST_PTMS_VERSION_DATE,
                                                                      "library.json"))
        self.LATEST_PTMS_PDBS_DIR_PATH = attach_root_path(os.path.join("viennaptm",
                                                                       "resources",
                                                                       "pdbs_minimized",
                                                                       self.LATEST_PTMS_VERSION_DATE))
        self.GROMACS_MINIM_MDP_DEFAULT = attach_root_path(os.path.join("viennaptm",
                                                                       "resources",
                                                                       "gromacs",
                                                                       "minim.mdp"))
        return self
