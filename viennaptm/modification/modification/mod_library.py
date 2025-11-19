import logging

from viennaptm.modification.modification.modification import Modification
from viennaptm.utils.error_handling import raise_with_logging_error, raise_with_logging_warning

logger = logging.getLogger(__name__)

class ModLibrary:
    def __init__(self, last_update_date=None, version=None):
        self._library = []
        self._last_update_date = last_update_date
        self._version = version

    def add_modification(self, new_modification):
        if not isinstance(new_modification, Modification):
            raise_with_logging_error("A library may only contain modification entries.",
                                     logger=logger,
                                     exception_type=TypeError)

        self._library.append(new_modification)

    def get_modification(self, initial_abbreviation, target_abbreviation=None, modification_name=None):
        # get the input
        if target_abbreviation is None and modification_name is None:
            raise_with_logging_error("Function needs the initial residue abbreviation and either the target "
                                     "abbreviation or the modification specifier.",
                                     logger=logger,
                                     exception_type=ValueError)

        if target_abbreviation is not None and modification_name is not None:
            target_abbreviation = None
            logger.warning("Both target abbreviation and modification name specified - the former will be ignored.")

        for modi in self._library:
            if initial_abbreviation == modi.initial_abbreviation:
                if target_abbreviation is None and modification_name == modi.modification_name:
                    return modi
                elif modification_name is None and target_abbreviation == modi.target_abbreviation:
                    return modi

        raise_with_logging_error("Could not find requested modification in library.",
                                 logger=logger,
                                 exception_type=ValueError)

    def __len__(self):
        return len(self._library)
