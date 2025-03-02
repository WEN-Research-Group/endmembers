"""
Compute the error between the true endmembers and the fitted endmembers for the synthetic datasets.
"""

import numpy as np
import pandas as pd

np.set_printoptions(precision=3)

true_endmembers = pd.read_csv("data/synthetic/endmembers.csv", index_col=0)

for dataset_name in ("noisefree", "noisy"):
    for method in ("AA", "NMF", "CHEMMA", "EDAA"):
        endmembers_fitted = pd.read_csv(
            f"results/synthetic/{method}_{dataset_name}_endmembers.csv", index_col=0
        )
        distance = np.linalg.norm(
            true_endmembers.values - endmembers_fitted.values,
            axis=1,
        )
        print(
            f"Dataset: {dataset_name}, Method: {method}",
            distance,
            sep="\n" 
        )
