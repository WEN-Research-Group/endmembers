import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
plt.rcParams["savefig.format"] = "pdf"
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["legend.frameon"] = False

colors = sns.color_palette("colorblind")

fig, axes = plt.subplots(1, 2, figsize=(6.1, 3), constrained_layout=True)

true_proportions = pd.read_csv("data/synthetic/mixing_proportions.csv")
n_endmembers = len(true_proportions.columns)

dataset_names = ("noisefree", "noisy")
titles = ("Noise-free", "Noisy")
labels = ("a", "b")

for i in range(2):
    fitted_proportions = pd.read_csv(
        f"results/synthetic/AA_{dataset_names[i]}_mixing_proportions.csv"
    )

    ax = axes[i]
    ax.set_prop_cycle(color=colors)
    lines = ax.plot(
        true_proportions.values,
        fitted_proportions.values,
        marker=".",
        markeredgewidth=0,
        linestyle="",
        alpha=0.6,
    )

    ax.plot([0, 1], [0, 1], color="black", linestyle="--")
    ax.set_xlabel("True Mixing Proportions")
    ax.set_ylabel("SPGD-AA Fitted Mixing Proportions")
    ax.legend(lines, true_proportions.columns, loc="upper left", handletextpad=0.1, borderaxespad=0.1)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.set_title(titles[i])

    ax.annotate(
        labels[i],
        (0.0, 1),
        xycoords="axes fraction",
        xytext=(-1.2, 1.3),
        textcoords="offset fontsize",
        fontsize="x-large",
        verticalalignment="top",
        fontweight="bold",
    )

    print(f"Dataset: {dataset_names[i]}",
          "Linear regression:",
          repr(linregress(true_proportions.values.ravel(), fitted_proportions.values.ravel())),
          sep="\n")




plt.savefig("images/synthetic_mixing_proportions.pdf")

plt.show()