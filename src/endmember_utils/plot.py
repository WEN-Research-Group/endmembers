"""
Utilities for plotting.
"""

from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import seaborn as sns
import numpy as np
from numpy.typing import ArrayLike


class EndmemberHeatmap:
    """
    Plot a heatmap of endmember chemistry.

    Attributes
    ----------
    ax: matplotlib.axes.Axes
        The axes object to use for plotting.
        If not provided, the current axes will be used.
    """

    def __init__(self, ax=None) -> None:
        if ax is None:
            ax = plt.gca()
        self.ax = ax

    def plot(self, data: ArrayLike, annot=True, cmap="YlGnBu", **kwargs) -> None:
        """
        Plot the heatmap.

        Parameters
        ----------
        data: ArrayLike
            The data to be plotted as a heatmap.
        **kwargs
            Additional keyword arguments to be passed to the seaborn heatmap function.

        Returns
        -------
        None
        """
        sns.heatmap(data, annot=annot, cmap=cmap, ax=self.ax, **kwargs)


class Scatter:
    """
    Scatter plot samples in 2D or 3D space.
    Also plot endmembers.

    default axis names are PC1, PC2, PC3
    """

    def __init__(self, ax=None, ndim=2, axis_names=None) -> None:
        if ax is None:
            ax = plt.gca()
        self.ax = ax
        self.ndim = ndim
        if ndim == 2:
            if axis_names is None:
                axis_names = ("PC1", "PC2")
            else:
                assert len(axis_names) == 2, "axis_names must have 2 elements."
            ax.set(xlabel=axis_names[0], ylabel=axis_names[1])
        elif ndim == 3:
            if axis_names is None:
                axis_names = ("PC1", "PC2", "PC3")
            else:
                assert len(axis_names) == 3, "axis_names must have 3 elements."
            ax.set(xlabel=axis_names[0], ylabel=axis_names[1], zlabel=axis_names[2])
        else:
            raise ValueError("d must be 2 or 3.")

    def plot_samples(self, X: ArrayLike, marker=".", **kwargs):
        """
        Scatter plot samples with dots.

        Parameters
        ----------
        X: (N, 2) or (N,3) ArrayLike
            The samples to be plotted.
        marker: str, optional
            The marker to use for the scatter plot. Default is ".".
        **kwargs
            Additional keyword arguments to be passed to the `axes.plot` function,
            e.g. `color`, `markersize`, `label`, etc.
        """
        X, ax = self._validate_data(X)
        (line,) = ax.plot(
            *(X[:, i] for i in range(self.ndim)), marker=marker, linestyle="", **kwargs
        )
        return line
    
    def scatter(self, X: ArrayLike, marker=".", **kwargs):
        """
        Scatter plot samples with dots using Matplotlib's scatter function.

        Parameters
        ----------
        X: (N, 2) or (N, 3) ArrayLike
            The samples to be plotted.
        marker: str, optional
            The marker to use for the scatter plot. Default is ".".
        **kwargs
            Additional keyword arguments to be passed to the `axes.scatter` function,
            e.g. `color`, `s` (size), `label`, `c` (color mapping), etc.
        """
        X, ax = self._validate_data(X)
        scatter = ax.scatter(
            *(X[:, i] for i in range(self.ndim)), marker=marker, **kwargs
        )
        return scatter

    def stem_samples(self, X: ArrayLike, linewidth=1, **kwargs):
        """
        add stem lines to the scatter plot of samples.

        Parameters
        ----------
        X: (N, 2) or (N,3) ArrayLike
            The samples to be plotted.
        **kwargs
            Additional keyword arguments to be passed to the `axes.stem` function,
            e.g. `linefmt`, `markerfmt`, `basefmt`, `label`, etc.
        """
        X, ax = self._validate_data(X)
        markerline, stemlines, baseline = ax.stem(
            *(X[:, i] for i in range(self.ndim)),
            bottom=ax.get_zbound()[0],
            linefmt="lightgray",
            markerfmt="",
            basefmt="",
            **kwargs,
        )
        markerline.remove()
        baseline.remove()
        stemlines.set_linewidth(linewidth)
        stemlines.set_zorder(-1)

        return stemlines

    def plot_endmembers(
        self,
        endmembers: ArrayLike,
        marker,
        plot_ploygon=False,
        polygon_kwargs=None,
        **kwargs
    ):
        """
        Plot endmembers with a same marker, using `axes.plot`.

        Parameters
        ----------
        endmembers: (N, 2) or (N,3) ArrayLike
            The endmembers to be plotted.
        marker: str
            The marker to use for the scatter plot.
        plot_ploygon: bool, optional
            Whether to plot a polygon connecting the endmembers. Default is False.
            Ignored if ndim is 3.
        polygon_kwargs: dict, optional
            when self.ndim == 2,
            Keyword arguments to be passed to the `matplotlib.patches.Polygon` constructor.
            e.g. `edgecolor`, `linewidth`, `linestyle`.
            If 3D, they should be `edgecolors`, `linewidths`, `linestyles`, and
            passed to the `Poly3DCollection` constructor.
        **kwargs
            Additional keyword arguments to be passed to the `axes.plot` function,
            e.g. `markersize`, `label`.
        """
        endmembers, ax = self._validate_data(endmembers)

        if plot_ploygon:
            endmember_polygon = self.plot_polygon(endmembers, polygon_kwargs)

        label = kwargs.pop("label", None)

        (line,) = ax.plot(
            *(endmembers[:, i] for i in range(self.ndim)),
            marker=marker,
            linestyle="",
            **kwargs,
        )

        if label:
            (line,) = ax.plot(  # only for legend
                *([endmembers[0, i]] for i in range(self.ndim)),
                linestyle=endmember_polygon.get_linestyle() if plot_ploygon else "",
                color=endmember_polygon.get_edgecolor() if plot_ploygon else None,
                linewidth=endmember_polygon.get_linewidth() if plot_ploygon else None,
                marker=line.get_marker(),
                markersize=line.get_markersize(),
                markerfacecolor=line.get_markerfacecolor(),
                markeredgecolor=line.get_markeredgecolor(),
                markeredgewidth=line.get_markeredgewidth(),
                label=label,
            )
        return line

    def plot_each_endmember(
        self,
        endmembers: ArrayLike,
        marker,
        colors,
        labels,
        plot_ploygon=False,
        polygon_kwargs=None,
        **kwargs
    ):
        """
        Plot each endmember with a different color, using `axes.plot` repeatedly.

        Parameters
        ----------
        endmembers: (N, 2) or (N,3) ArrayLike
            The endmembers to be plotted.
        marker: str
            The marker to use for the plot.
        colors: list
            The colors to use for each endmember.
        labels: list
            The labels for each endmember.
        **kwargs
            Additional keyword arguments to be passed to the `axes.plot` function,
        """
        endmembers, ax = self._validate_data(endmembers)
        if plot_ploygon:
            endmember_polygon = self.plot_polygon(endmembers, polygon_kwargs)

        lines = []
        for i, endmember in enumerate(endmembers):
            (line,) = ax.plot(
                *([endmember[i]] for i in range(self.ndim)),
                color=colors[i],
                marker=marker,
                linestyle="",
                label=labels[i],
                **kwargs,
            )
            lines.append(line)

        return lines

    def link_observed_vs_fitted(self, observed: ArrayLike, fitted: ArrayLike, **kwargs):
        """
        Link observed and fitted data points.

        Parameters
        ----------
        observed: (N, 2) or (N, 3) ArrayLike
            The observed data points.
        fitted: (N, 2) or (N, 3) ArrayLike
            The fitted data points.
        **kwargs
            Additional keyword arguments to be passed to the
            `matplotlib.collections.LineCollection` constructor.
            e.g. `colors`, `linestyles`, `linewidths`.
        """
        observed, ax = self._validate_data(observed)
        fitted, ax = self._validate_data(fitted)
        assert (
            observed.shape == fitted.shape
        ), "observed and fitted must have the same shape."
        lines = np.stack(
            [observed, fitted], axis=1
        )  # shape (N, 2, 2), N lines, 2 points per line, 2/3 coordinates per point
        if self.ndim == 2:
            lines = LineCollection(lines, **kwargs)
            ax.add_collection(lines)
        elif self.ndim == 3:
            lines = Line3DCollection(lines, **kwargs)
            ax.add_collection3d(lines)
        return lines

    def plot_convex_hull(self, X, **kwargs):
        """
        Plot the convex hull of the samples.
        only in 2D.

        Parameters
        ----------
        X: (N, 2) ArrayLike
            The samples to compute the convex hull.
        **kwargs
            Keyword arguments to be passed to the `matplotlib.patches.Polygon` constructor.
            e.g. `edgecolor`, `linewidth`, `linestyle`.
        """
        X, ax = self._validate_data(X)
        assert self.ndim == 2, "only 2D scatter plots are supported."
        convex_hull = ConvexHull(X)
        vertices = X[convex_hull.vertices]
        hull_polygon = Polygon(vertices, closed=True, fill=None, **kwargs)
        ax.add_patch(hull_polygon)
        return hull_polygon

    def plot_polygon(self, endmembers, polygon_kwargs):
        endmembers, ax = self._validate_data(endmembers)
        polygon_kwargs = {} if polygon_kwargs is None else polygon_kwargs
        if self.ndim == 2:
            endmember_polygon = Polygon(
                endmembers, closed=True, fill=None, **polygon_kwargs
            )
            ax.add_patch(endmember_polygon)
        elif self.ndim == 3:
            hull = ConvexHull(endmembers)
            simplices = hull.simplices
            facets = [endmembers[simplex] for simplex in simplices]

            endmember_polygon = Poly3DCollection(facets, **polygon_kwargs)
            ax.add_collection3d(endmember_polygon)
        return endmember_polygon

    def _validate_data(self, data):
        data = np.asarray(data)
        data.ndim == 2, "values must be 2D."
        ax = self.ax
        assert (
            data.shape[1] == self.ndim
        ), "data must have the same dimension as the scatter plot."
        return data, ax
