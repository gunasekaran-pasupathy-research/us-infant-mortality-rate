"""UN IGME via the UNICEF SDMX API (CME_MRY0). Carries uncertainty bounds."""
import pandas as pd

from src.config import UN_IGME_URL
from src.data.sources._base import cached

RAW = "un_igme.csv"


def load():
    return cached(RAW, lambda: pd.read_csv(UN_IGME_URL))


def tidy(raw=None):
    df = load() if raw is None else raw.copy()
    df = df[df["REF_AREA"].str.len() == 3]   # countries only (drops UN IGME aggregates)
    out = pd.DataFrame({
        "source": "UN IGME",
        "entity": df["Geographic area"],
        "iso3": df["REF_AREA"],
        "entity_type": "country",
        "year": df["TIME_PERIOD"].astype(int),
        "imr": df["OBS_VALUE"].astype(float),
        "imr_low": df["LOWER_BOUND"],
        "imr_high": df["UPPER_BOUND"],
    })
    return out.dropna(subset=["imr"]).sort_values(["entity", "year"]).reset_index(drop=True)
