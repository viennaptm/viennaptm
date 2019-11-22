import numpy as np
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from Bio.PDB.vectors import Vector
from modification.modification import Modification


class AtomPositionCalculator:
    """Class to obtain a relative coordinate system and map new atoms to this system accoding to specifications.
       The constructor will initialize the coordinates """

    def __init__(self, anchor_coordinates: Vector, vector_1: Vector, vector_2: Vector):
        # extract anchor point which will lie at the origin (0, 0, 0) of the relative coordinate system
        self._anchor_coordinates = anchor_coordinates

        # set three internal, normalized and orthogonal vectors as the relative coordinate system applied to the anchor
        self._axis_1, self._axis_2, self._axis_3 = self._initialize_relative_coordinate_system(vector_1, vector_2)

    @staticmethod
    def _get_orthogonal_component(axis_1: Vector, help_axis: Vector) -> Vector:
        # extract the orthogonal component of the help axis in respect to the first and return it
        scalar = help_axis * axis_1
        return Vector(*(scalar * axis_1.get_array()))

    @staticmethod
    def _get_orthogonal_vector_to_plane(axis_1: Vector, axis_2: Vector) -> Vector:
        axis_1_arr = axis_1.get_array()
        axis_2_arr = axis_2.get_array()
        return Vector(*(axis_1_arr[1] * axis_2_arr[2] - axis_1_arr[2] * axis_2_arr[1],
                        axis_1_arr[2] * axis_2_arr[0] - axis_1_arr[0] * axis_2_arr[2],
                        axis_1_arr[0] * axis_2_arr[1] - axis_1_arr[1] * axis_2_arr[0]))

    def _initialize_relative_coordinate_system(self, vector_1: Vector, vector_2: Vector):
        # get both vectors defining the 3D plane (note: NOT orthogonal), axis 1 is the first vector taken as
        # is (and orthogonal component of axis 2 is extracted and applied); this structure is mainly
        # due to backward compatibility issues
        axis_1 = vector_1.normalized()
        help_axis = vector_2.normalized()
        orthogonal_component = self._get_orthogonal_component(axis_1=axis_1,
                                                              help_axis=help_axis)
        axis_2 = Vector(*(help_axis - orthogonal_component)).normalized()

        # calculate the third vector, defining the axis orthogonal to the plane
        axis_3 = self._get_orthogonal_vector_to_plane(axis_1=axis_1,
                                                      axis_2=axis_2).normalized()

        return axis_1, axis_2, axis_3

    def project_coordinates(self, coordinates: np.array) -> np.array:
        pass
