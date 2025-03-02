"""
Visualize the results of the synthetic data experiments, comparing the endmembers estimated by SPGD-AA, NMF, and CHEMMA with the true endmembers in 3D PC space.
"""

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
from endmember_utils.plot import Scatter


# Change default behavior of matplotlib
plt.rcParams["font.family"] = "Arial"
plt.rcParams["savefig.format"] = "pdf"
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["legend.frameon"] = False

default_palette = sns.color_palette("colorblind")


def plot_endmember_as_lines(
    axes, endmembers, **kwargs
):
    for ax, (em_name, em) in zip(
        axes, endmembers.iterrows()
    ):
        ax.plot(
            em.index, em.values, **kwargs
        )

    return 


# Panel a
fig = plt.figure(figsize=(5.7*1.07, 6.8*1.02))
gs = fig.add_gridspec(2, 2, height_ratios=[0.36, 1], hspace=1.5)

for i in range(2):
    # Upper Panel
    dataset_name = ["noisefree", "noisy"][i]

    synthetic_samples = pd.read_csv(f"data/synthetic/{dataset_name}_samples.csv")
    endmembers = pd.read_csv("data/synthetic/endmembers.csv", index_col=0)
    endmembers_AA = pd.read_csv(
        f"results/synthetic/AA_{dataset_name}_endmembers.csv", index_col=0
    )
    endmembers_NMF = pd.read_csv(
        f"results/synthetic/NMF_{dataset_name}_endmembers.csv", index_col=0
    )
    endmembers_CHEMMA = pd.read_csv(
        f"results/synthetic/CHEMMA_{dataset_name}_endmembers.csv", index_col=0
    )
    endmembers_EDAA = pd.read_csv(
        f"results/synthetic/EDAA_{dataset_name}_endmembers.csv", index_col=0
    )

    inner_gs = gs[0, i].subgridspec(2, 2, hspace=0, wspace=0)
    (ax1, ax2), (ax3, ax4) = inner_gs.subplots(sharex=True, sharey=True)
    axes = [ax1, ax2, ax3, ax4]

    ax1.set_ylabel("Values")
    ax3.set_xlabel("Features")

    upper_legend_elements = []
    for em, color, linestyle, alpha, label in zip(
        [endmembers, endmembers_AA, endmembers_NMF, endmembers_CHEMMA, endmembers_EDAA],
        linecolors:=["gray", default_palette[1], default_palette[2], default_palette[0], default_palette[4]],
        linestyles:=["-", "-.", "--", ":", (0, (3, 1, 1, 1, 1, 1))],
        alphas:=[0.6, 1, 0.8, 1, 0.9],
        labels:=["True", "SPGD-AA", "NMF", "CHEMMA", "EDAA"],
    ):
        plot_endmember_as_lines(axes, em, color=color, linestyle=linestyle, linewidth=1, alpha=alpha)
        upper_legend_elements.append(
            Line2D([], [], color=color, linestyle=linestyle, linewidth=1, alpha=alpha, label=label)
        )

    for ax, title in zip(axes, endmembers.index):
        ax.set_title(title, y=0.68)

    for ax in axes:
        ax.label_outer()
        ax.set_ylim(0, 2.3)

    fig.legend(
        handles=upper_legend_elements,
        ncols=2,
        bbox_to_anchor=(0.04, 0.6),
        loc="center left",
        frameon=True,
    )

    # Lower Panel

    ndim = 3
    pca = PCA(n_components=ndim)

    ax = fig.add_subplot(gs[1, i], projection="3d")
    scatter = Scatter(ax, ndim=ndim)
    scatter.scatter(
        pca.fit_transform(synthetic_samples),
        color=default_palette[4],
        s=8,
        label="Samples",
        edgecolors="none",
    )

    if i == 0:
        ax.legend(
            loc="upper right",
            markerscale=3.0,
            handletextpad=0.4,
            borderpad=0,
            borderaxespad=0,
        )

    n_endmembers = len(endmembers)

    lines = []

    for em, marker, labels in zip(
        [endmembers, endmembers_AA, endmembers_NMF, endmembers_CHEMMA, endmembers_EDAA],
        ["*", "^", "P", "X", "d"],
        [
            endmembers.index,
            [" "] * n_endmembers,
            [" "] * n_endmembers,
            [" "] * n_endmembers,
            [" "] * n_endmembers,
        ],
    ):
        em_lines = scatter.plot_each_endmember(
            pca.transform(em),
            marker=marker,
            colors=default_palette,
            markeredgecolor="black",
            markersize=10 if marker == "*" else 8,
            markeredgewidth=0.5,
            labels=labels,
        )
        lines.extend(em_lines)

    ax.view_init(azim=73, elev=43)
    ax.set_ylabel("PC2", labelpad=6)
    ax.set_zlabel("PC3", labelpad=6)

for label, i in zip(["a", "b", "c", "d"], [0, 4, 5, 9]):
    ax = fig.axes[i]
    ax.annotate(
        label,
        (0.0, 1),
        xycoords="axes fraction",
        xytext=(-0.9, 1.2) if (i == 0 or i == 5) else (-1.2, -0.5),  # TODO
        textcoords="offset fontsize",
        fontsize=16,
        verticalalignment="top",
        fontweight="bold",
    )

fig.legend(
    handles=lines,
    ncols=5,
    title="          True SPGD-AA NMF CHEMMA EDAA",
    markerfirst=False,
    loc="center right",
    bbox_to_anchor=(0.99, 0.58),
    handletextpad=0.4,
    columnspacing=0.9,
    labelspacing=0.3,
    frameon=True,
)

gs.tight_layout(fig)
fig.savefig("images/synthetic_results.pdf")
plt.show()
