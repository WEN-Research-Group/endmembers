"""
Utilities for data analysis and AA.
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import Iterable, Literal
from numpy.typing import ArrayLike
from archetypes import AA


def multi_AA(data: ArrayLike, archetype_numbers: Iterable[int], **aa_kwargs):
    """
    Run a series of AA with multiple numbers of archetypes and return the results.

    Parameters
    ----------
    data : array-like
        The data to be decomposed.
    archetype_numbers : iterable of int
        The numbers of archetypes to use.
    aa_kwargs : dict
        Keyword arguments to pass to the AA constructor.

    Returns
    -------
    aa_list : list of AA
        The AA objects fitted to the data.
    transformed_data_list : list of array-like
        The transformed data for each AA object.
    """
    aa_list: list[AA] = []
    transformed_data_list: list[np.ndarray] = []
    for n_archetypes in archetype_numbers:
        aa = AA(n_archetypes, **aa_kwargs)
        transformed_data = aa.fit_transform(data)
        aa_list.append(aa)
        transformed_data_list.append(transformed_data)

    return aa_list, transformed_data_list


def normalize_losses(losses):
    losses = [rss / losses[0] for rss in losses]
    return losses


def spectral_angle_distances(x, y, output: Literal["rad", "deg"] = "rad") -> float:
    """
    Calculate the spectral angle distance between two arrays.

    Parameters
    ----------
    x : array-like
        The first array.
    y : array-like
        The second array.
    output : str
        The units of the output. Either "rad" for radians or "deg" for degrees.

    Returns
    -------
    distance : float
        The spectral angle distance between the two arrays.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    dot_product = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    distance = np.arccos(dot_product / (norm_x * norm_y))
    if output == "deg":
        distance = np.degrees(distance)
    elif output != "rad":
        raise ValueError("output must be either 'rad' or 'deg'")
    return distance


def match_endmembers(endmembers, endmembers_fitted, mixing_proportions=None):
    """
    Match the fitted endmembers to the true endmembers, based on cosine similarity.

    Parameters
    ----------
    endmembers: array-like, shape (n_endmembers, n_features)
        The true (referential) endmembers.
    endmembers_fitted: array-like, shape (n_endmembers, n_features)
        The fitted endmembers.
    mixing_proportions: array-like, shape (n_samples, n_endmembers), optional
        The mixing proportions to be matched. If provided, they will be rearranged
        to match the new order of fitted endmembers.

    Returns
    -------
    rearranged_endmembers: array-like, shape (n_endmembers, n_features)
        The fitted endmembers with rows rearranged to match `endmembers`.
    rearranged_mixing_proportions: array-like, shape (n_samples, n_endmembers)
        The rearranged mixing proportions. Only returned if `mixing_proportions` is provided.
    """
    new_index = cosine_similarity(endmembers, endmembers_fitted).argmax(axis=1)
    assert np.unique(new_index).size == new_index.size, "One-to-one mapping not found"
    endmembers_rearranged = np.asarray(endmembers_fitted)[new_index]
    if isinstance(endmembers, pd.DataFrame):
        endmembers_rearranged = pd.DataFrame(
            endmembers_rearranged,
            index=(
                endmembers.index
            ),
            columns=endmembers.columns,
        )

    if mixing_proportions is not None:
        mixing_proportions = mixing_proportions[:, new_index]
        if isinstance(endmembers, pd.DataFrame):
            mixing_proportions = pd.DataFrame(
                mixing_proportions,
                columns=endmembers.index,
            )
        return endmembers_rearranged, mixing_proportions

    return endmembers_rearranged 
