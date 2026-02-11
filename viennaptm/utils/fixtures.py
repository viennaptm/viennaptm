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

    PTMS_LIBRARY_PATH: Path = None
    PTMS_PDBS_DIR_PATH: Path = None

    PDB_ENDING: str = ".pdb"

    GROMACS_MINIM_MDP_DEFAULT: Path = None

    @model_validator(mode="after")
    def ptms_fixture_validator(self):
        """
        Resolve and attach default fixture paths.

        This validator populates internal path attributes for the
        modification library, minimized PDB templates, and default
        GROMACS energy minimization parameters.

        :return:
            The validated fixture configuration instance.
        :rtype: ViennaPTMFixtures
        """

        self.PTMS_LIBRARY_PATH = attach_root_path(os.path.join("viennaptm",
                                                               "resources",
                                                               "libraries",
                                                               "library.json"))
        self.PTMS_PDBS_DIR_PATH = attach_root_path(os.path.join("viennaptm",
                                                                "resources",
                                                                "pdbs_minimized"))
        self.GROMACS_MINIM_MDP_DEFAULT = attach_root_path(os.path.join("viennaptm",
                                                                       "resources",
                                                                       "gromacs",
                                                                       "minim.mdp"))
        return self
