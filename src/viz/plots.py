import matplotlib.pyplot as plt

from src.config import RATE_COL


def plot_trend(df, ax=None):
    """Infant mortality rate over time, one line per race."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))
    for race, group in df.groupby("race"):
        ax.plot(group["year"], group[RATE_COL], marker=".", label=race)
    ax.set_xlabel("year")
    ax.set_ylabel("deaths per 1,000 live births")
    ax.set_title("U.S. infant mortality rate, 1915–2013")
    ax.legend()
    return ax


def plot_gap(gap, ax=None):
    """Black-minus-White gap in the infant mortality rate over time."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))
    ax.plot(gap.index, gap["difference"], color="firebrick")
    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xlabel("year")
    ax.set_ylabel("Black − White (per 1,000)")
    ax.set_title("Black–White infant mortality gap")
    return ax
