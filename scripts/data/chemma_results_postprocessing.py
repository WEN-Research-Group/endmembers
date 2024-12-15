"""
Match CHEMMA endmembers to the field endmembers.
"""

import numpy as np
import pandas as pd
from endmember_utils import match_endmembers

endmembers = pd.read_csv("data/synthetic/endmembers.csv", index_col=0)
for dataset_name in ("noisefree", "noisy"):
    chemma_endmembers = np.loadtxt(
        f"results/synthetic/CHEMMA_{dataset_name}_endmembers_raw_output.csv", delimiter=","
    )
    matched_endmembers = match_endmembers(endmembers, chemma_endmembers)
    matched_endmembers.to_csv(
        f"results/synthetic/CHEMMA_{dataset_name}_endmembers.csv"
    )
