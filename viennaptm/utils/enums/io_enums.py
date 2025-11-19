import logging

from viennaptm.utils.error_handling import raise_with_logging_error, raise_with_logging_warning

logger = logging.getLogger(__name__)

class IOModificationEnum:
    """Class to store all modification library strings."""

    # library file attributes
    # ---------
    INTERNAL_LIBRARY_PATH = "resources/libraries"
    INTERNAL_LIBRARY_SUFFIX = "_library.xml"

    # library XML format
    # ---------
    LIBRARY = "library"
    LIBRARY_LAST_UPDATE = "last_update"
    LIBRARY_VERSION = "version"

    RESIDUE = "residue"
    RESIDUE_ABBREVIATION = "abbreviation"
    RESIDUE_NAME = "name"
    MODIFICATION = "modification"
    MODIFICATION_NAME = "name"
    TARGET_ABBREVIATION = "target_abbreviation"
    TARGET_NAME = "target_name"

    ANCHOR = "anchor"
    AXES = "axes"
    AXIS = "axis"
    AXIS_NUMBER = "number"
    AXIS_POINT1 = "p1"
    AXIS_POINT2 = "p2"

    ADDITIONS = "additions"
    ADD = "add"
    ADD_ATOM_NAME = "name"
    ADD_ATOM_ELETYPE = "eletype"
    ADD_ATOM_XCOORR = "xcoorr"
    ADD_ATOM_YCOORR = "ycoorr"
    ADD_ATOM_ZCOORR = "zcoorr"
    ADD_ATOM_TEMPFACTOR = "tempfactor"

    DELETIONS = "deletions"
    DEL = "del"
    DEL_ATOM_NAME = "name"

    REPLACEMENTS = "replacements"
    REP = "rep"
    REP_NEW_ELETYPE = "new_eletype"
    REP_ATOM_NAME = "name"
    REP_BY_NAME = "by"

    AXIS1 = "axis1"
    AXIS2 = "axis2"

    def __getattr__(self, name):
        if name in self:
            return name
        raise_with_logging_error(f"Attribute {name} is unknown.",
                                 logger=logger,
                                 exception_type=AttributeError)

    def __setattr__(self, name, value):
        raise_with_logging_warning("Do not attempt to set attributes for this class.",
                                   logger=logger,
                                   exception_type=Exception)
