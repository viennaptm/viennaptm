
class ModificationReport:
    def __init__(self, atoms_added=0, atoms_deleted=0, atoms_renamed=0):
        self.atoms_added = atoms_added
        self.atoms_deleted = atoms_deleted
        self.atoms_renamed = atoms_renamed

    def __add__(self, other):
        return ModificationReport(atoms_added=self.atoms_added+other.atoms_added,
                                  atoms_deleted=self.atoms_deleted+other.atoms_deleted,
                                  atoms_renamed=self.atoms_renamed+other.atoms_renamed)

    def __str__(self):
        return "Atoms added: \t{}\nAtoms deleted: \t{}}\nAtoms renamed: \t{}}".format(self.atoms_added,
                                                                                      self.atoms_deleted,
                                                                                      self.atoms_deleted)
