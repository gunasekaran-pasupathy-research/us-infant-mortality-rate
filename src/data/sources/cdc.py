"""CDC / NCHS — Infant Mortality Rates, by Race: United States, 1915-2013."""
import numpy as np
import pandas as pd

from src.config import CDC_CSV_URL
from src.data.sources._base import cached

RAW = "cdc_nchs_by_race.csv"


def load():
    return cached(RAW, lambda: pd.read_csv(CDC_CSV_URL))


def tidy(raw=None):
    df = load() if raw is None else raw.copy()
    df["race"] = df["race"].str.strip()  # raw has both 'Black' and 'Black '
    out = pd.DataFrame({
        "source": "CDC/NCHS",
        "entity": df["race"],
        "iso3": "USA",
        "entity_type": "us_race",
        "year": df["year"].astype(int),
        "imr": df["infant_mortality_rate"].astype(float),
        "imr_low": np.nan,
        "imr_high": np.nan,
    })
    return out.sort_values(["entity", "year"]).reset_index(drop=True)


# --- race-disparity helpers (this source only) ---
def to_wide(tidy_df):
    return tidy_df.pivot(index="year", columns="entity", values="imr")


def black_white_gap(tidy_df):
    wide = to_wide(tidy_df)
    return pd.DataFrame({
        "white": wide["White"],
        "black": wide["Black"],
        "difference": wide["Black"] - wide["White"],
        "ratio": wide["Black"] / wide["White"],
    })
