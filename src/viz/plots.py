import matplotlib.pyplot as plt


def plot_trend(tidy_df, ax=None, title="Infant mortality rate"):
    """One line per entity (race or country) of IMR over time."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))
    for entity, group in tidy_df.groupby("entity"):
        ax.plot(group["year"], group["imr"], marker=".", label=entity)
    ax.set_xlabel("year")
    ax.set_ylabel("deaths per 1,000 live births")
    ax.set_title(title)
    ax.legend()
    return ax


def plot_gap(gap, ax=None):
    """Black-minus-White gap over time (expects the cdc.black_white_gap frame)."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))
    ax.plot(gap.index, gap["difference"], color="firebrick")
    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xlabel("year")
    ax.set_ylabel("Black − White (per 1,000)")
    ax.set_title("Black–White infant mortality gap")
    return ax
