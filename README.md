# endmembers

## Introduction

This repo is affiliated with the manuscript "**Inferring End-members from Geoscience Data using Simplex Projected Gardient Descent-Archetypal Analysis**" submitted to _JGR: Machine Learning and Computation_" in Dec, 2024. More information will be avaliable soon.

Geological and environmental samples often reflect the integrated results of multiple sources and/or processes. When each source/process has its unique features, we conceptualize them as "end-members", and model samples as mixtures of end-members, and evaluate their mixing proportions to quantitatively estimate the contributions of different sources. This technqiue has been widely used in many fields like hydrogeochemistry ([_e. g._ Hooper 1990](https://doi.org/10.1016/0022-1694(90)90131-G)), sedimentology ([_e. g._  Vandenberghe 2013](https://doi.org/10.1016/j.earscirev.2013.03.001)) and remote sensing ([_e. g._  Bioucas-Dias et al 2012](https://doi.org/10.1109/JSTARS.2012.2194696)). This is sometimes called end-member mixing analysis (EMMA).

Conventional supervised EMMA relies on known end-member properties, but often we have little or no information about them. Many existing unsupervised EMMA approaches that infer end-members from data like NMF ([_e. g._  Shaughnessy et al 2021](https://doi.org/10.5194/hess-25-3397-2021)) are often less accessible and interpretable. We developed Simplex Projected Gardient Descent-Archetypal Analysis (SPGD-AA) to overcome these challenges. SPGD-AA is based on archetypal analysis (AA) ([Cutler and Breiman, 1994](https://doi.org/10.1080/00401706.1994.10485840) and [Mørup and Hansen, 2012](https://doi.org/10.1016/j.neucom.2011.06.033)) and fast unit simplex projection ([Condat 2016](https://doi.org/10.1007/s10107-015-0946-6)).

We apply SPGD-AA to synthetic and real-world datasets. Demo code is in [examples/demo.ipynb](/examples/demo.ipynb). Real world datasets including Panola Mountain stream chemistry ([Hooper 1990](https://doi.org/10.1016/0022-1694(90)90131-G)), Nazca Plate deep-sea sediment ([Dymond 1981](https://doi.org/10.1130/MEM154-p133)) and Jasper Ridge hyperspectral image ([Zhu 2017](https://arxiv.org/abs/1708.05125)). More details are available in the [data/](/data/) folder, especially the README files.

The end-members inferred using SPGD-AA of these datasets are stored in the [results/](/results/) folder. We compared them with end-members in previous studies, proving SPGD-AA's capability. You can find some visualizations of our results in the [images/](/images/) folder.

**This repo is for demonstration of SPGD-AA applications only. The source code SPGD-AA is hosted in GitHub repo [aleixalcacer/archetypes](https://github.com/aleixalcacer/archetypes).**

## Installation
Requires: Python 3.12
1. `git clone` the repo, or download and unzip
2. `cd` the root directory of the project
3. create and activate a Python virtual environment
4. `pip install -e .[jupyter]` to install the current project, which comes with a module `endmember_utils`. This should install all the dependencies automatically.

## Usage
After installation, the `endmember_utils` package, and some other necessary packages like ``archetypes`` will be available in the current python virtual environment. You can now run the **demo.ipynb** notebook (or other scripts, which are independent, given that the result files are already avaliable).

## Project Organization

Real-world examples are in [examples/demo.ipynb](/examples/demo.ipynb).

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
│   │   ├── Dymond1981_endmember_fraction.csv # Dymond end-members
│   │   ├── Dymond1981_endmember_ratio.csv
│   │   ├── LP1984_endmember_fraction.csv # Leinen and Pisias end-members
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
│       ├── README.md
│       ├── noisefree_samples.csv
│       └── noisy_samples.csv
├── examples
│   └── demo.ipynb # demonstrates how to use SPGD-AA to analyze these datasets
├── images # figures in the manuscript, generated using scripts/plots
│   ├── aa_basic_concepts.pdf
│   ├── jasper_results.pdf
│   ├── nazca_results.pdf
│   ├── panola_results.pdf
│   ├── nazca_other_perspectives.pdf
│   ├── synthetic_mixing_proportions.pdf
│   └── synthetic_results.pdf
├── pyproject.toml # project metadata
├── results # end-members inferred using SPGD-AA, output of examples/demo.ipynb
│   ├── jasper_ridge # both .csv and .npy foramts are provided
│   │   ├── endmembers_fitted.csv
│   │   ├── endmembers_fitted.npy 
│   │   ├── endmembers_fitted_normalized.csv # l1 normalized
│   │   └── endmembers_fitted_normalized.npy
│   ├── nazca
│   │   └── endmembers_fitted.csv
│   ├── panola
│   │   └── endmembers_fitted.csv
│   └── synthetic # also with results coming from other two methods CHEMMA and NMF (raw and processed)
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
├── scripts # scripts used to pre- and post- processing data, and make some plots. Read the docstrings in these files for more info.
│   ├── data
│   │   ├── chemma_results_postprocessing.py
│   │   ├── generate_synthetic_data.py
│   │   └── print_synthetic_endmember_error.py
│   └── plots
│       ├── plot_aa_basic_concepts.py
│       ├── plot_nazca_other_perspectives.py
│       ├── plot_synthetic_data_results.py
│       └── plot_synthetic_mixing_proportions.py
└── src # source code to help the analysis: the `endmember_utils` package. Read source code and docstrings for more details
    └── endmember_utils
        ├── __init__.py
        ├── analysis.py
        ├── plot.py
        └── synthetic.py
```

## Contributing

This repo is not intended to be a community-driven python project. Rather, it is created to demonstrate some simple examples and applications of SPGD-AA in EMMA. **We recommend those who are interested to join us to contribute to the `archetypes` package.** However, if you do see any deficiencies or have any suggestions in this repo, issues and pull requests are welcome :)