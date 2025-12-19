import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class AtomAddition:
    def __init__(self, name, eletype, xcoorr,
                 ycoorr, zcoorr, tempfactor):
        self.name = name
        self.eletype = eletype
        self.xcoorr = xcoorr
        self.ycoorr = ycoorr
        self.zcoorr = zcoorr
        self.tempfactor = tempfactor


class AtomDeletion:
    def __init__(self, name):
        self.name = name
        logger.debug(f"Deleted Atom: {self.name}.")

class AtomReplacement:
    def __init__(self, name, by, new_eletype):
        self.name = name
        self.by = by
        self.new_eletype = new_eletype
        logger.debug(f"Atom {self.name} replaced with {self.new_eletype}.")

class Axis:
    def __init__(self, number, p1, p2):
        self.number = number
        self.p1 = p1
        self.p2 = p2

@dataclass
class Modification:
    def __init__(self, initial_abbreviation, initial_name, modification_name,
                 target_abbreviation, target_name, anchor,
                 axis1, axis2, atom_additions,
                 atom_deletions, atom_replacements):

        # initialize data structures: names
        self._initial_abbreviation = initial_abbreviation
        self._initial_name = initial_name
        self._modification_name = modification_name
        self._target_abbreviation = target_abbreviation
        self._target_name = target_name
        logger.debug(f"{self._initial_name} ({self._initial_abbreviation}) modified with "
                     f"{self._modification_name} "
                     f"to target {self._target_name} ({self._target_abbreviation}).")

        # initialize data structures: anchor and axes
        self._anchor = anchor
        self._axis1 = axis1
        self._axis2 = axis2
        logger.debug(f"Anchor: {self._anchor},"
                     f"Axis_1: {self._axis1},"
                     f"Axis_2: {self._axis2}")

        # initialize data structures: atom manipulations
        self._atom_additions = atom_additions
        self._atom_deletions = atom_deletions
        self._atom_replacements = atom_replacements
        logger.debug(f"Atom additions: {self._atom_additions}, "
                     f"Atom deletions: {self._atom_deletions},"
                     f"Atom replacements: {self._atom_replacements}.")

    @property
    def initial_abbreviation(self):
        return self._initial_abbreviation

    @property
    def initial_name(self):
        return self._initial_name

    @property
    def modification_name(self):
        return self._modification_name

    @property
    def target_abbreviation(self):
        return self._target_abbreviation

    @property
    def target_name(self):
        return self._target_name

    @property
    def anchor(self):
        return self._anchor

    @property
    def axis1(self):
        return self._axis1

    @property
    def axis2(self):
        return self._axis2

    @property
    def atom_additions(self):
        return self._atom_additions

    @property
    def atom_deletions(self):
        return self._atom_deletions

    @property
    def atom_replacements(self):
        return self._atom_replacements

    def __str__(self):
        return "{} ---{}---> {}".format(self._initial_abbreviation,
                                        self._modification_name,
                                        self._target_abbreviation)
