"""World Bank — World Development Indicators (SP.DYN.IMRT.IN), all countries."""
import numpy as np
import pandas as pd

from src.config import WORLD_BANK_URL
from src.data.sources._base import cached, get_json

RAW = "world_bank_wdi.csv"
COUNTRY_META = "https://api.worldbank.org/v2/country?format=json&per_page=400"


def _fetch():
    # the indicator endpoint mixes real countries with aggregates (World, regions,
    # income groups); use the country metadata to flag which rows are countries.
    meta = get_json(COUNTRY_META)[1]
    real = {m["id"] for m in meta if m["region"]["value"] != "Aggregates"}
    records = get_json(WORLD_BANK_URL)[1]
    return pd.DataFrame([{
        "entity": d["country"]["value"],
        "iso3": d["countryiso3code"],
        "year": d["date"],
        "imr": d["value"],
        "is_country": d["countryiso3code"] in real,
    } for d in records])


def load():
    return cached(RAW, _fetch)


def tidy(raw=None):
    df = load() if raw is None else raw.copy()
    df = df[df["is_country"]].dropna(subset=["imr"])
    out = pd.DataFrame({
        "source": "World Bank",
        "entity": df["entity"],
        "iso3": df["iso3"],
        "entity_type": "country",
        "year": df["year"].astype(int),
        "imr": df["imr"].astype(float),
        "imr_low": np.nan,
        "imr_high": np.nan,
    })
    return out.sort_values(["entity", "year"]).reset_index(drop=True)
