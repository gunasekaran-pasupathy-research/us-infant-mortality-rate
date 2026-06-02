"""WHO — Global Health Observatory (MDG_0000000001). Carries uncertainty bounds."""
import pandas as pd

from src.config import WHO_GHO_URL
from src.data.sources._base import cached, get_json

RAW = "who_gho.csv"


def _fetch():
    records = get_json(WHO_GHO_URL)["value"]
    cols = ["SpatialDimType", "SpatialDim", "Dim1", "TimeDim", "NumericValue", "Low", "High"]
    return pd.DataFrame(records)[cols]


def load():
    return cached(RAW, _fetch)


def tidy(raw=None):
    df = load() if raw is None else raw.copy()
    # keep country rows for both sexes combined
    df = df[(df["SpatialDimType"] == "COUNTRY") & (df["Dim1"] == "SEX_BTSX")]
    out = pd.DataFrame({
        "source": "WHO GHO",
        "entity": df["SpatialDim"],   # ISO3 code (names not in this response)
        "iso3": df["SpatialDim"],
        "entity_type": "country",
        "year": df["TimeDim"].astype(int),
        "imr": df["NumericValue"].astype(float),
        "imr_low": df["Low"],
        "imr_high": df["High"],
    })
    return out.dropna(subset=["imr"]).sort_values(["iso3", "year"]).reset_index(drop=True)
