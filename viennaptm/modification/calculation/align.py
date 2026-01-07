import numpy as np
from scipy.spatial.transform import Rotation
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def compute_alignment_transform(coord_reference: np.ndarray, coord_template: np.ndarray, weights: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the roto-translational transform (with weights!) that aligns coord_template to coord_reference.

    :param coord_reference: Reference coordinates (anchor atoms from input residue).
    :type coord_reference: (N, 3) array

    :param coord_template: Template coordinates to be aligned (anchor atoms from template residue).
    :type coord_template: (N, 3) array

    :param weights: Weights for centroid and rotation calculation.
    :type weights: List[float]

    :return M_rotation: Rotation matrix.
    :rtype: (3, 3) ndarray

    :return v_translation: Translation vector.
    :rtype: (3,) ndarray
    """

    # centroids (weighted)
    cog_reference = np.average(coord_reference, axis=0, weights=weights)
    cog_template = np.average(coord_template, axis=0, weights=weights)

    # centered coordinates
    coord_centered_reference = coord_reference - cog_reference
    coord_centered_template = coord_template - cog_template

    # optimal rotation (maps coord_centered_template onto coord_centered_reference)
    rotation, _ = Rotation.align_vectors(coord_centered_reference,
                                         coord_centered_template,
                                         weights=weights)
    M_rotation = rotation.as_matrix()

    # since M_rotation * cog_template + V_translation = cog_reference
    v_translation = cog_reference - M_rotation @ cog_template

    logger.debug(f"M_rotation: {M_rotation}")
    logger.debug(f"v_translation: {v_translation}")
    return M_rotation, v_translation


def apply_transform(coords: np.ndarray, M_rotation: np.ndarray, v_translation: np.ndarray) -> np.ndarray:
    """
    Apply a roto-translational transform to a set of points, i.e. the atomic positions of atoms that are to be added
    from the template to the original reference frame.

    :param coords: Points to transform.
    :type coords: (M, 3) array

    :param M_rotation: Rotation matrix.
    :type M_rotation: (3, 3) array

    :param v_translation: Translation vector.
    :type v_translation: (3,) array

    :return v_transformed: Returns the transformed coordinates: M_rotation @ coords + v_translation.
    :rtype: (M, 3) array
    """
    return (M_rotation @ coords.T).T + v_translation
