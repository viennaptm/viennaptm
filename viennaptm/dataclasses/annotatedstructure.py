"""The annotated structure class ..."""

from Bio.PDB.Structure import Structure

class AnnotatedStructure(Structure):
    """The Structure class receives the original structure and then
    stores the modified version of it."""

    def __init__(self, id):
        """Initialize the class."""
        Structure.__init__(self, id)