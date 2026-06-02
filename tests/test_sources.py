import numpy as np
import pandas as pd

from src.config import TIDY_COLUMNS
from src.data.sources import cdc, world_bank, owid, nber_microdata


def test_cdc_tidy_strips_whitespace_and_schema():
    raw = pd.DataFrame({
        "race": ["Black", "Black ", "White"],   # note the trailing space
        "year": ["1915", "1916", "1915"],
        "infant_mortality_rate": ["195.2", "184.3", "98.6"],
    })
    out = cdc.tidy(raw)
    assert list(out.columns) == TIDY_COLUMNS
    assert set(out["entity"].unique()) == {"Black", "White"}   # not split in two
    assert out["year"].dtype.kind == "i" and out["imr"].dtype.kind == "f"
    assert (out["iso3"] == "USA").all()


def test_cdc_black_white_gap():
    raw = pd.DataFrame({
        "race": ["Black", "White"],
        "year": ["1915", "1915"],
        "infant_mortality_rate": ["195.2", "98.6"],
    })
    gap = cdc.black_white_gap(cdc.tidy(raw))
    assert round(gap.loc[1915, "difference"], 1) == round(195.2 - 98.6, 1)


def test_owid_converts_percent_to_per_1000():
    raw = pd.DataFrame({
        "Entity": ["United States", "World"],
        "Code": ["USA", "OWID_WRL"],       # region code is dropped (len != 3)
        "Year": [1960, 1960],
        "Infant mortality rate": [2.6, 12.0],   # percent
    })
    out = owid.tidy(raw)
    assert list(out["iso3"]) == ["USA"]
    assert round(out.iloc[0]["imr"], 1) == 26.0   # 2.6% -> 26 per 1,000


def test_world_bank_drops_aggregates():
    raw = pd.DataFrame({
        "entity": ["United States", "World"],
        "iso3": ["USA", "WLD"],
        "year": [2000, 2000],
        "imr": [6.9, 52.0],
        "is_country": [True, False],
    })
    out = world_bank.tidy(raw)
    assert list(out["iso3"]) == ["USA"]
    assert list(out.columns) == TIDY_COLUMNS


def test_nber_microdata_decodes_codes():
    raw = pd.DataFrame({
        "dbwt": [3500, 9999],          # 9999 = unknown -> NaN
        "combgest": [39, 99],          # 99 = unknown -> NaN
        "mager41": [28, 33],
        "dplural": [1, 2],
        "sex": ["M", "F"],
        "precare": [2, 99],
        "uprevis": [12, 99],
        "meduc": [6, 9],               # 9 = unknown -> NaN
        "mracehisp": [6, 1],           # 6 = NH White, 1 = Hispanic (Mexican)
        "cig_rec": ["N", "Y"],
        "died": [0, 1],
        "year": [2013, 2013],
    })
    out = nber_microdata.tidy(raw)
    assert np.isnan(out.loc[1, "birthweight_g"])
    assert np.isnan(out.loc[1, "gestation_wks"])
    assert np.isnan(out.loc[1, "mother_educ"])
    assert list(out["mother_race_hisp"]) == ["White (NH)", "Hispanic"]
    assert list(out["smoker"]) == [0, 1]
    assert out["died"].tolist() == [0, 1]
