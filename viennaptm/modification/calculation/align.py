import numpy as np
from scipy.spatial.transform import Rotation
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def compute_alignment_transform(coord_reference: np.ndarray, coord_template: np.ndarray, weights: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the roto-translational transform (with weights!) that aligns coord_template to coord_reference.

    Parameters
    ----------
    coord_reference : (N, 3) array
        Reference coordinates (anchor atoms from input residue).
    coord_template : (N, 3) array
        Template coordinates to be aligned (anchor atoms from template residue).
    weights : List[float]
        Weights for centroid and rotation calculation.

    Returns
    -------
    M_rotation : (3, 3) ndarray
        Rotation matrix.
    V_translation : (3,) ndarray
        Translation vector.
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

    Parameters
    ----------
    coords : (M, 3) array
        Points to transform.
    M_rotation : (3, 3) array
        Rotation matrix.
    v_translation : (3,) array
        Translation vector.

    Returns
    -------
    v_transformed : (M, 3) array
        Transformed coordinates: M_rotation @ coords + v_translation.
    """
    return (M_rotation @ coords.T).T + v_translation
