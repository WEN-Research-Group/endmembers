import pandas as pd
from archetypes import AA
from endmember_utils.analysis import match_endmembers

random_state = 42

# global parameters passed to all `archetypes.AA` in this notebook
global_aa_params = {
    "n_init": 10,  # number of initializations
    "max_iter": 2000,  # maximum number of iterations
    "tol": 1e-10,  # tolerance for convergence
    "method_kwargs": {
        "max_iter_optimizer": 25
    },  # parameters for the optimization method
    "init": "furthest_sum",  # efficient initialization by Morup and Hansen (2012)
    "method": "pgd",  # NOTE: this option is necessary to use the SPGD method
    "random_state": random_state,  # for reproducibility
}

alpha_list = [2, 4]
for i in range(2):
    alpha = alpha_list[i]
    dataset_name = f"alpha={alpha}" # or "alpha={alpha}_shifted" for shifted data

    synthetic_samples = pd.read_csv(f"data/synthetic/{dataset_name}_samples.csv")
    endmembers = pd.read_csv("data/synthetic/endmembers.csv", index_col=0)
    aa = AA(4, **global_aa_params)
    mixing_proportions = aa.fit_transform(synthetic_samples)
    endmembers_AA = pd.DataFrame(aa.archetypes_, columns=endmembers.columns)
    endmembers_AA, mixing_proportions = match_endmembers(endmembers, endmembers_AA, mixing_proportions)

    endmembers_AA.to_csv(f"results/synthetic/AA_{dataset_name}_endmembers.csv")
    mixing_proportions.to_csv(
        f"results/synthetic/AA_{dataset_name}_mixing_proportions.csv",
        index=False,
    )



