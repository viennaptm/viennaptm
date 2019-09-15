import modification.modification as Mod


class ModLibrary:
    def __init__(self, last_update_date=None, version=None):
        self._library = []
        self._last_update_date = last_update_date
        self._version = version

    def add_modification(self, modification):
        if not isinstance(modification, Mod.modification):
            raise TypeError("A library may only contain modification entries.")
        self._library.append(modification)

    def get_modification(self, initial_abbreviation, target_abbreviation=None, modification_name=None):
        # get the input
        if target_abbreviation is None and modification_name is None:
            raise AttributeError("Function needs the initial residue abbreviation and either the target abbreviation or the modification specifier.")
        if target_abbreviation is not None and modification_name is not None:
            print( "Both target abbreviation and modification name specified - the latter will be ignored.")
            modification_name = None

        # TODO: actually get modification required

    @property
    def length(self):
        return len(self._library)

    @length.setter
    def length(self, inp):
        raise Exception("Method \"length()\" is read-only.")