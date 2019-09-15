class atom_addition:
    def __init__(self, inp):
        self.name = ""
        self.eletype = ""
        self.xcoorr = ""
        self.ycoorr = ""
        self.zcoorr = ""
        self.tempfactor = ""


class atom_deletion:
    def __init__(self, inp):
        self.name = ""


class atom_replacement:
    def __init__(self, inp):
        self.name = ""
        self.by = ""


class modification:
    def __init__(self, xml_entry):
        # initialize data structures: names
        self._initial_abbreviation = ""
        self._initial_name = ""
        self._modification_name = ""
        self._target_abbreviation = ""
        self._target_name = ""

        # initialize data structures: axes
        self._axis1 = {}
        self._axis2 = {}

        # initialize data structures: atom manipulations
        self._atom_additions = []
        self._atom_deletions = []
        self._atom_replacements = []
