"""Our World in Data — long historical series. Value is a percent, so x10 -> per 1,000."""
import numpy as np
import pandas as pd

from src.config import OWID_URL
from src.data.sources._base import cached

RAW = "owid.csv"


def load():
    return cached(RAW, lambda: pd.read_csv(OWID_URL))


def tidy(raw=None):
    df = load() if raw is None else raw.copy()
    df = df.rename(columns={"Entity": "entity", "Code": "iso3", "Year": "year"})
    rate_col = next(c for c in df.columns if "mortality" in c.lower())
    df = df.dropna(subset=["iso3"])
    df = df[df["iso3"].str.len() == 3]   # drops OWID region codes (e.g. OWID_WRL)
    out = pd.DataFrame({
        "source": "Our World in Data",
        "entity": df["entity"],
        "iso3": df["iso3"],
        "entity_type": "country",
        "year": df["year"].astype(int),
        "imr": df[rate_col].astype(float) * 10.0,   # percent of live births -> per 1,000
        "imr_low": np.nan,
        "imr_high": np.nan,
    })
    return out.sort_values(["entity", "year"]).reset_index(drop=True)
