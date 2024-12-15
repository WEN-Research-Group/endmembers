"""
Plot the basic concepts of archetypal analysis (AA) using synthetic data.
"""

import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import seaborn as sns
from archetypes import AA
from endmember_utils.synthetic import synthetic
from endmember_utils.plot import Scatter

colors = sns.color_palette("colorblind")

# endmembers and synthetic samples
endmembers = np.array(
    [
        [1.0, 2.0],
        [2.0, 1.0],
        [3.0, 3.0],
    ]
)

# endmember_uncertainty = endmembers * 0.05

synthetic_samples, _ = synthetic(
    50,
    endmembers=endmembers,
    # endmember_uncertainty=endmember_uncertainty,
    # sample_noise=0.05,
    random_state=42,
)

# Do archetypal analysis
n_archetypes = 3
aa = AA(
    n_archetypes,
    n_init=10,
    init="furthest_sum",
    method="pgd",
    tol=1e-8,
    max_iter=1000,
    method_kwargs={"max_iter_optimizer": 20},
)
mixing_proportions = aa.fit_transform(synthetic_samples)
endmembers_fitted = aa.archetypes_
reconstruction_loss = aa.rss_
fitted_samples = mixing_proportions @ endmembers_fitted

# Evaluate the convex hull of synthetic samples
convex_hull = ConvexHull(synthetic_samples)

# Plot
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.labelsize"] = 12
markersize = 14
fig, ax = plt.subplots(figsize=(5.8, 5.4), constrained_layout=True)
ax.set_prop_cycle(color=colors)

scatter = Scatter(ax, axis_names=["Feature 1", "Feature 2"])
scatter.plot_samples(
    synthetic_samples, color=colors[0], markersize=markersize - 4,  label="True data points"
)
scatter.plot_samples(
    fitted_samples,
    color=colors[0],
    markersize=markersize + 4,
    markerfacecolor="none",
    label="Represented data points",
)
scatter.plot_endmembers(
    endmembers,
    marker="*",
    plot_ploygon=True,
    polygon_kwargs={"linestyle": "dotted", "edgecolor": "lightgray"},
    color="lightgray",
    markersize=markersize+2,
    label="True end-members",
)
scatter.plot_endmembers(
    endmembers_fitted,
    plot_ploygon=True,
    polygon_kwargs={"linestyle": "dashed", "edgecolor": colors[1]},
    marker="*",
    markersize=markersize+2,
    color = colors[1],
#    markerfacecolor="none",
#    markeredgecolor=colors[1],
#    markeredgewidth=3,
    label="Fitted archetypes and\nprincipal convex hull",
    zorder=3,
)
scatter.link_observed_vs_fitted(
    synthetic_samples, fitted_samples, color="C3", label="Residuals"
)
scatter.plot_convex_hull(
    synthetic_samples,
    linestyle=(convex_hull_linestyle := "dashdot"),
    edgecolor=(convex_hull_edgecolor := "dimgray"),
)

# Add some legends
ax.plot(
    [endmembers[0, 0]],
    [endmembers[0, 1]],
    linestyle=convex_hull_linestyle,
    color=convex_hull_edgecolor,
    label="Data convex hull",
)
ax.set_aspect("equal", adjustable="box")
ax.legend(prop={"size": 12}, frameon=False)
ax.set_xticks([])
ax.set_yticks([])

fig.savefig("images/aa_basic_concepts.pdf", bbox_inches="tight")
plt.show()
