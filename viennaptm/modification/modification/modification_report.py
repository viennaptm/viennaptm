
class ModificationReport:
    """
    Report summarizing atomic modifications.

    This class tracks the number of atoms that were added, deleted,
    or renamed during a modification process. Reports can be combined
    using the addition operator.

    :param atoms_added: Number of atoms added.
    :type atoms_added: int
    :param atoms_deleted: Number of atoms deleted.
    :type atoms_deleted: int
    :param atoms_renamed: Number of atoms renamed.
    :type atoms_renamed: int

    :ivar atoms_added: Number of atoms added.
    :vartype atoms_added: int
    :ivar atoms_deleted: Number of atoms deleted.
    :vartype atoms_deleted: int
    :ivar atoms_renamed: Number of atoms renamed.
    :vartype atoms_renamed: int
    """

    def __init__(self, atoms_added=0, atoms_deleted=0, atoms_renamed=0):
        self.atoms_added = atoms_added
        self.atoms_deleted = atoms_deleted
        self.atoms_renamed = atoms_renamed

    def __add__(self, other):
        """Adds the modification (atoms added, deleted and renamed) to the modification report and returns an
        updated modification report :class:`ModificationReport`.

        :param other: Another modification report.
        :type other: ModificationReport
        :return: A new report with summed modification counts.
        :rtype: ModificationReport
        """

        return ModificationReport(atoms_added=self.atoms_added+other.atoms_added,
                                  atoms_deleted=self.atoms_deleted+other.atoms_deleted,
                                  atoms_renamed=self.atoms_renamed+other.atoms_renamed)

    def __str__(self):
        """Return a human-readable summary of the report.

        :return: Formatted string summarizing atom modifications.
        :rtype: str
        """

        return "Atoms added: \t{}\nAtoms deleted: \t{}\nAtoms renamed: \t{}".format(self.atoms_added,
                                                                                    self.atoms_deleted,
                                                                                    self.atoms_renamed)

