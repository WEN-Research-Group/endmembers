"""
Utilities for generating synthetic data.
"""

from typing import Iterable
import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
from sklearn.utils import check_random_state


def synthetic(
    n_samples: int,
    *,
    endmembers: ArrayLike,
    endmember_uncertainty: ArrayLike | None = None,
    untertainty_type: str = "normal",
    dirichlet_alpha: float = 1,
    sample_noise: float | ArrayLike = 0,
    random_state: int | np.random.RandomState | None = None,
):
    """
    Generate synthetic data with noise.

    Parameters
    ----------
    n_samples : int, default=None
        Number of samples generated. If None, numbers are inferred from ``proportions``.
    endmembers : array-like of shape (n_endmembers, n_features)
        Endmembers.
    endmember_uncertainty : array-like of shape (n_endmembers, n_features), default=None
        Uncertainty of endmembers. No uncertainty by default.
    untertainty_type : str, default='normal'
        Type of endmember uncertainty. 'normal' or 'uniform'.
        if 'normal', endmembers are sampled from a normal distribution with
        mean ``endmembers`` and standard deviation ``endmember_uncertainty``.
        if 'uniform', endmembers are sampled from a uniform distribution between
        ``endmembers - endmember_uncertainty`` and ``endmembers + endmember_uncertainty``.
    proportions : array-like of shape (n_samples, n_endmembers), default=None
        Mixing proportions. If None, random proportions are generated from a dirichlet distribution.
    dirichlet_alpha : float, default=None
        Concentration parameter of the Dirichlet distribution, applied to each features.
        Higher values will make the proportions more concentrated towards
        (1/n_endmembers, ..., 1/n_endmembers).
        When alpha = 1, the proportions are uniformly distributed in the probability simplex.
    sample_noise : float or array-like of shape (n_features,), default=0
        Standard deviation of Gaussian noise added to each sample.
        If array-like, each feature has its own noise level.
    random_state : int or RandomState or None, default=None
        Random seed or random number generator.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features) or pandas.DataFrame
        Synthetic data.
    proportions : ndarray of shape (n_samples, n_endmembers) or pandas.DataFrame
        Mixing proportions.
    endmembers_noisy : ndarray of shape (n_endmembers, n_features) or pandas.DataFrame
        Endmembers of each synthetic sample with noise.
        If ``endmember_uncertainty`` is None, this is the same as ``endmembers``.
    """
    results_to_dataframe = False
    if isinstance(endmembers, pd.DataFrame):
        results_to_dataframe = True
        feature_names = endmembers.columns
        endmember_names = endmembers.index

    rng = check_random_state(random_state)

    endmembers = np.asarray(endmembers, dtype=float)
    n_endmembers = endmembers.shape[0]

    proportions = rng.dirichlet(np.ones(n_endmembers) * dirichlet_alpha, n_samples)

    if endmember_uncertainty is None:
        X = proportions @ endmembers
    else:
        endmember_uncertainty = np.asarray(endmember_uncertainty)
        if untertainty_type == "uniform":
            endmembers_noisy = rng.uniform(
                endmembers - endmember_uncertainty,
                endmembers + endmember_uncertainty,
                (n_samples, *endmembers.shape),
            )
        elif untertainty_type == "normal":
            endmembers_noisy = rng.normal(
                endmembers, endmember_uncertainty, (n_samples, *endmembers.shape)
            )
        else:
            raise ValueError("Invalid uncertainty type.")

        X = np.einsum("ij,ijk->ik", proportions, endmembers_noisy)

    noise = rng.normal(0, sample_noise, X.shape)
    X += noise

    if results_to_dataframe:
        X = pd.DataFrame(data=X, columns=feature_names)
        proportions = pd.DataFrame(data=proportions, columns=endmember_names)

    return X, proportions
