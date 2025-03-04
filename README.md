# endmembers

## Introduction

This repo is affiliated with the manuscript "**Inferring End-members from Geoscience Data using Simplex Projected Gradient Descent-Archetypal Analysis**" submitted to _JGR: Machine Learning and Computation_" in Dec, 2024. More information will be avaliable soon.

In this work, we developed Simplex Projected Gardient Descent-Archetypal Analysis (SPGD-AA) to infer end-members from geoscience data of mixed materials. SPGD-AA is based on archetypal analysis (AA) ([Cutler and Breiman, 1994](https://doi.org/10.1080/00401706.1994.10485840) and [Mørup and Hansen, 2012](https://doi.org/10.1016/j.neucom.2011.06.033)) and fast unit simplex projection ([Condat 2016](https://doi.org/10.1007/s10107-015-0946-6)).

We apply SPGD-AA to synthetic and real-world datasets. Demo code is in [examples/demo.ipynb](/examples/demo.ipynb). Real world datasets including Panola Mountain stream chemistry ([Hooper 1990](https://doi.org/10.1016/0022-1694(90)90131-G)), Nazca Plate deep-sea sediment ([Dymond 1981](https://doi.org/10.1130/MEM154-p133)) and Jasper Ridge hyperspectral image ([Zhu 2017](https://arxiv.org/abs/1708.05125)). More details are available in the [data/](/data/) folder, especially the README files.

The end-members of these datasets inferred using SPGD-AA and other methods are stored in the [results/](/results/) folder. We compared them with end-members determined in previous studies, proving SPGD-AA's capability. Some visualizations of our results in the manuscript are in the [images/](/images/) folder. These figures, along with some numerical results shown in the manuscript, are generated using scripts in the [scripts/](/scripts/) folder. The [src/](/src/) folder contains the source code of the `endmember_utils` package, which is used in much of the analysis.

**This repo is for demonstration of SPGD-AA applications only. The source code SPGD-AA is hosted in GitHub repo [aleixalcacer/archetypes](https://github.com/aleixalcacer/archetypes).**

## Installation

Requires: Python 3.12

1. `git clone` the repo, or download and unzip
2. `cd` the root directory of the project
3. create and activate a Python virtual environment
4. `pip install -e .[jupyter]` to install the current project, which comes with a module `endmember_utils`. This should install all the dependencies automatically.

## Usage

After installation, the `endmember_utils` package, and some other necessary packages like ``archetypes`` will be available in the current python virtual environment. You can now run the **demo.ipynb** notebook (or other scripts, which are independent, given that the result files are already avaliable).

## Contributing

This repo is not intended to be a community-driven python project. Rather, it is created to demonstrate some simple examples and applications of SPGD-AA in end-member mixing analysis. **We recommend those who are interested to join us to contribute to the `archetypes` package.** However, if you do see any deficiencies in the repo or have any suggestions, issues and pull requests are welcome :)