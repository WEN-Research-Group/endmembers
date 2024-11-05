import numpy as np
import pandas as pd
from endmember_utils.synthetic import synthetic
from pathlib import Path

# Define file paths
data_dir = Path("data/synthetic")
data_dir.mkdir(parents=True, exist_ok=True)

# Define endmembers
endmembers = np.array(
    [
        [1.3, 1.2, 1.0, 0.6, 0.3, 0.2, 0.2, 0.1],
        [0.3, 0.4, 0.9, 1.3, 1.0, 0.5, 0.4, 0.2],
        [0.2, 0.8, 1.2, 0.4, 0.3, 1.2, 0.9, 0.3],
        [0.2, 0.3, 0.1, 0.2, 0.5, 0.9, 1.4, 1.0],
    ]
)

endmembers = pd.DataFrame(
    data=endmembers,
    columns=[letter for letter in "ABCDEFGH"],
    index=[f"EM{i+1}" for i in range(len(endmembers))],
)

endmembers.to_csv(data_dir / "endmembers.csv")

# Generate synthetic samples (parameters)
random_state = 42
n_samples = 1000

## Noise-free samples
synthetic_samples, mixing_proportions = synthetic(
    n_samples,
    endmembers=endmembers,
    random_state=random_state,
)
synthetic_samples.to_csv(data_dir / "noisefree_samples.csv", index=False)
mixing_proportions.to_csv(data_dir / "mixing_proportions.csv", index=False)

## Noisy samples
endmember_noise_level = 0.1
sample_noise_level = 0.1

synthetic_samples, mixing_proportions = synthetic(
    n_samples,
    endmembers=endmembers,
    endmember_uncertainty=np.full_like(endmembers, endmember_noise_level),
    random_state=random_state,
    sample_noise=sample_noise_level,
)
synthetic_samples[synthetic_samples < 0] = 0
synthetic_samples.to_csv(data_dir / "noisy_samples.csv", index=False)
# No mixing proportions for noisy samples, as they are the same as the noise-free ones.
