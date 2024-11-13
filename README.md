# endmembers

Inferring End-members from Geoscience Data using Simplex Projected Gardient Descent-Archetypal Analysis

## Usage
1. `git clone` the repo, or download and unzip
2. `cd` the root directory of the project
3. create a Python virtual environment
4. `pip install -e .` to install the current project and the module `endmember_utils`
5. Now you can run scripts or notebooks with the current virtualenv

## Project Organization
```bash
.
├── LICENSE
├── README.md
├── data # synthetic and real datasets
│   ├── jasper_ridge
│   │   ├── README.md
│   │   ├── end4.mat # Jasper end-members
│   │   ├── jasperRidge2_R198.hdr # Jasper metadata
│   │   └── jasperRidge2_R198.img # Jasper image array
│   ├── nazca
│   │   ├── Dymond1981_endmember_fraction.csv
│   │   ├── Dymond1981_endmember_ratio.csv
│   │   ├── LP1984_endmember_fraction.csv
│   │   ├── LP1984_endmember_ratio.csv
│   │   ├── README.md
│   │   ├── ggge20247-sup-001a-supinfo1a.xlsx # Nazca Dataset
│   │   ├── ggge20247-sup-001b-supinfo1b.xlsx # Unused
│   │   └── ggge20247-sup-001c-supinfo1c.xlsx # Unused
│   ├── panola
│   │   ├── README.md
│   │   ├── panola_data.csv
│   │   ├── panola_end_members.csv
│   │   └── xufei2022_endmembers.csv
│   └── synthetic
│       ├── endmembers.csv
│       ├── mixing_proportions.csv # apply for both noise-free and noisy data
│       ├── noisefree_samples.csv
│       └── noisy_samples.csv
├── examples
│   └── demo.ipynb # demonstrates how to use SPGD-AA to analyze these datasets
├── images
│   ├── aa_basic_concepts.pdf
│   ├── jasper_results.pdf
│   ├── nazca_results.pdf
│   ├── panola_results.pdf
│   ├── synthetic_mixing_proportions.pdf
│   └── synthetic_results.pdf
├── pyproject.toml
├── results # end-members inferred using SPGD-AA
│   ├── jasper_ridge
│   │   ├── endmembers_fitted.csv
│   │   ├── endmembers_fitted.npy
│   │   ├── endmembers_fitted_normalized.csv
│   │   └── endmembers_fitted_normalized.npy
│   ├── nazca
│   │   └── endmembers_fitted.csv
│   ├── panola
│   │   └── endmembers_fitted.csv
│   └── synthetic # Also other two methods
│       ├── AA_noisefree_endmembers.csv
│       ├── AA_noisefree_mixing_proportions.csv
│       ├── AA_noisy_endmembers.csv
│       ├── AA_noisy_mixing_proportions.csv
│       ├── CHEMMA_noisefree_endmembers.csv
│       ├── CHEMMA_noisefree_endmembers_raw_output.csv
│       ├── CHEMMA_noisy_endmembers.csv
│       ├── CHEMMA_noisy_endmembers_raw_output.csv
│       ├── NMF_noisefree_endmembers.csv
│       ├── NMF_noisefree_mixing_proportions.csv
│       ├── NMF_noisy_endmembers.csv
│       └── NMF_noisy_mixing_proportions.csv
├── scripts # scripts used to pre- and post- processing data, and make some plots
│   ├── data
│   │   ├── chemma_results_postprocessing.py
│   │   ├── generate_synthetic_data.py
│   │   └── print_synthetic_endmember_error.py
│   └── plots
│       ├── plot_aa_basic_concepts.py
│       ├── plot_synthetic_data_results.py
│       └── plot_synthetic_mixing_proportions.py
└── src # source code to help the analysis
    └── endmember_utils
        ├── __init__.py
        ├── analysis.py
        ├── plot.py
        └── synthetic.py
```