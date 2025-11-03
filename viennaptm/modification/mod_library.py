from viennaptm.modification.modification import Modification


class ModLibrary:
    def __init__(self, last_update_date=None, version=None):
        self._library = []
        self._last_update_date = last_update_date
        self._version = version

    def add_modification(self, new_modification):
        if not isinstance(new_modification, Modification):
            raise TypeError("A library may only contain modification entries.")
        self._library.append(new_modification)

    def get_modification(self, initial_abbreviation, target_abbreviation=None, modification_name=None):
        # get the input
        if target_abbreviation is None and modification_name is None:
            raise AttributeError("Function needs the initial residue abbreviation and either the target abbreviation or the modification specifier.")
        if target_abbreviation is not None and modification_name is not None:
            print("Both target abbreviation and modification name specified - the former will be ignored.")
            target_abbreviation = None

        for modi in self._library:
            if initial_abbreviation == modi.initial_abbreviation:
                if target_abbreviation is None and modification_name == modi.modification_name:
                    return modi
                elif modification_name is None and target_abbreviation == modi.target_abbreviation:
                    return modi
        raise Exception("Could not find requested modification in library.")

    def __len__(self):
        return len(self._library)
