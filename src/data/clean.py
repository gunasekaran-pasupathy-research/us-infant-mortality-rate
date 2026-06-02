import pandas as pd

from src.config import RATE_COL


def clean(df):
    """Tidy up the raw CDC pull.

    The raw data has the same race spelled two ways ('Black' and 'Black ' with a
    trailing space), so the first thing we do is strip the whitespace before it
    splits one group into two.
    """
    df = df.copy()
    df["race"] = df["race"].str.strip()
    df["year"] = df["year"].astype(int)
    df[RATE_COL] = df[RATE_COL].astype(float)
    return df.sort_values(["race", "year"]).reset_index(drop=True)


def to_wide(df):
    """Pivot to one row per year with a column per race - handy for comparisons."""
    return df.pivot(index="year", columns="race", values=RATE_COL)


def black_white_gap(df):
    """Black minus White rate, and the ratio, per year."""
    wide = to_wide(df)
    gap = pd.DataFrame({
        "white": wide["White"],
        "black": wide["Black"],
        "difference": wide["Black"] - wide["White"],
        "ratio": wide["Black"] / wide["White"],
    })
    return gap
