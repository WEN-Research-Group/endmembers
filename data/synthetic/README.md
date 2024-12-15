# Files

``endmembers.csv``: values of 8 features (A to H) of 4 end-members (EM1 to EM4).

``mixing_proportions.csv``: mixing proportions of 4 end-members (EM1 to EM4) in 1000 samples, applied to both noise-free and noisy datasets. Mixing proportions are generated from a flat dirichlet distribution.

``noisefree_samples.csv``: values of 8 features (A to H) of 1000 samples, each of which is a strict mixtures of EM1 to EM4.

``noisy_endmembers.csv``: values of 8 features (A to H) of 1000 samples. In each of the dataset, we add a Gaussian noise (sigma=0.1) to each end-member, and mix these end-members up, then add a Gaussian noise (sigma=0.1) to the mixed samples.

# Source

All the files in this directory are generated using [scripts/data/generate_synthetic_data.py](/scripts/data/generate_synthetic_data.py).