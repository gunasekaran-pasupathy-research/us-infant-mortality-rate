"""Stack every source into one tidy panel and pull cross-source views."""
import pandas as pd

from src.config import TIDY_COLUMNS
from src.data.sources import ALL


def load_all():
    """Tidy panel of all sources: columns = TIDY_COLUMNS."""
    frames = [module.tidy() for module in ALL.values()]
    return pd.concat(frames, ignore_index=True)[TIDY_COLUMNS]


def us_across_sources(panel=None):
    """U.S. infant mortality by year and source (country-level sources only)."""
    panel = load_all() if panel is None else panel
    us = panel[(panel["iso3"] == "USA") & (panel["entity_type"] == "country")]
    return us.pivot_table(index="year", columns="source", values="imr")


def country_year(panel=None, source="World Bank"):
    """One source's countries as a year x country matrix (for ranking/comparison)."""
    panel = load_all() if panel is None else panel
    one = panel[panel["source"] == source]
    return one.pivot_table(index="year", columns="iso3", values="imr")
