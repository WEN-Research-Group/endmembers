"""
Plot the Nazca endmember data in 3D PCA space from different perspectives.
"""

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import seaborn as sns

from endmember_utils.plot import Scatter

# Change default behavior of matplotlib
plt.rcParams["font.family"] = "Arial"
plt.rcParams["savefig.format"] = "pdf"
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["legend.frameon"] = False
# plt.rcParams["axes.labelsize"] = "large"

default_palette = sns.color_palette("colorblind")

nazca = pd.read_excel(
    "data/nazca/ggge20247-sup-001a-supinfo1a.xlsx", usecols="B:I", header=1
)
endmember_lp = pd.read_csv("data/nazca/LP1984_endmember_fraction.csv", index_col=0)

endmember_dymond = pd.read_csv(
    "data/nazca/Dymond1981_endmember_fraction.csv", index_col=0
)
endmembers_fitted = pd.read_csv("results/nazca/endmembers_fitted.csv", index_col=0)

nazca_normalized = normalize(
    nazca, norm="l1", axis=1
)  # convert (divide by sum of total 8 elements)
nazca_normalized = pd.DataFrame(
    nazca_normalized, columns=endmember_lp.columns, index=nazca.index
)

ndim = 3
pca = PCA(n_components=ndim)

pca_nazca = pca.fit_transform(nazca_normalized)
pca_endmembers_dymond = pca.transform(endmember_dymond)
pca_endmembers_fitted = pca.transform(endmembers_fitted)
pca_endmembers_lp = pca.transform(endmember_lp)

titles = ["Dymond", "SPGD-AA", "QFA"]

endmember_names = ["D", "H", "B", "A", "R"]

fig, axs = plt.subplots(1,2, figsize=(7.4, 5.18), layout="constrained", subplot_kw={"projection": "3d"})

azims = [-85, 44.5]
elevs = [40, 84]

for i in range(2):
    ax = axs[i]

    scatter = Scatter(ax, ndim=ndim)

    sample_line = scatter.scatter(
        pca_nazca,
        color=default_palette[4],
        s=32,
        edgecolors="none",
        label="Samples",
        zorder=5,
    )

    ax.add_artist(
        ax.legend(
            handles=[sample_line],
            loc="upper left",
            bbox_to_anchor=(0.3, 1),
            markerscale=1.8,
            handletextpad=0.3,
            #    frameon=True,
        )
    )

    colors = [default_palette[i] for i in [3, 0, 2, 1, 8]]
    colors[3] = sns.color_palette("bright")[9]

    # Define the markers, labels, endmember data, and markersizes
    markers = ["*", "^", "X"]
    labels = [endmember_names, [" "] * 5, [" "] * 5]
    endmember_data = [pca_endmembers_dymond, pca_endmembers_fitted, pca_endmembers_lp]
    markersizes = [10, 8, 8]

    # Plot each endmember using a for loop and zip
    lines = []
    for marker, label, em, markersize in zip(markers, labels, endmember_data, markersizes):
        line = scatter.plot_each_endmember(
            em,
            marker=marker,
            markersize=markersize,
            markeredgecolor="black",
            markeredgewidth=0.5,
            colors=colors,
            labels=label,
            zorder=6,
        )
        lines.extend(line)

    # scatter.stem_samples(pca_nazca)
    scatter.stem_samples(pca_endmembers_dymond)
    scatter.stem_samples(pca_endmembers_fitted)
    scatter.stem_samples(pca_endmembers_lp)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.view_init(azim=azims[i], elev=elevs[i])

    if i == 0:
        ax.set_xlabel("PC1", labelpad=0)

    if i == 1:
        ax.set_zticks([0.3])

    fig.legend(
        handles=lines,
        ncols=3,
        title=" Dymond  SPGD-AA   QFA",
        loc="outside upper center",
        handletextpad=0.6,
        #borderaxespad=0,
        #borderpad=0.8,
        columnspacing=1.4,
        markerfirst=False,
        # edgecolor="none",
        frameon=True,
        framealpha=1,
    )


for label, ax in zip("ab", axs):
    ax.annotate(
        label,
        (0.0, 1),
        xycoords="axes fraction",
        xytext=(-0.0, 0.0),
        textcoords="offset fontsize",
        fontsize=16,
        verticalalignment="top",
        fontweight="bold",
    )

plt.show()

fig.savefig(
    "images/nazca_other_perspectives.pdf",
    #bbox_inches="tight",
    #bbox_extra_artists=[axs[0].xaxis.label],
)
