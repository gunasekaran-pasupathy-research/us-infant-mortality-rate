"""NCHS Period Linked Birth/Infant Death microdata (record level), via NBER.

Unlike the aggregate rate sources, this is the *raw* data: one row per birth,
with the infant-death outcome and birth-certificate covariates. It supports
individual risk modeling (what makes a birth more likely to end in death)
instead of trend analysis.

Each year ships as two files: a denominator (all live births) and a numerator
(infant deaths linked to their birth certificate). We stack them with a `died`
flag. Because the linked deaths are also present among the births, this stack
double-counts deaths by ~0.6% (deaths / births); negligible for modeling, but
documented here for honesty.
"""
import zipfile

import numpy as np
import pandas as pd

from src.config import MICRODATA_YEARS, NBER_LINKED_URL, RAW_DIR

# Birth-certificate covariates we model on (present in both num and den files).
KEEP = ["dbwt", "combgest", "mager41", "dplural", "sex",
        "precare", "uprevis", "meduc", "mracehisp", "cig_rec"]

# mracehisp recode (verified against mbrace x umhisp): 1-5 are Hispanic
# subgroups, 6 = NH White, 7 = NH Black, 8 = NH other races, 9 = unknown.
RACE_HISP = {
    1: "Hispanic", 2: "Hispanic", 3: "Hispanic", 4: "Hispanic", 5: "Hispanic",
    6: "White (NH)", 7: "Black (NH)", 8: "Other (NH)",
}


def _download(year, kind):
    """Download a num/den zip to data/raw/ and return its path."""
    path = RAW_DIR / f"linkpe{year}us{kind}.csv.zip"
    if not path.exists():
        import urllib.request
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(NBER_LINKED_URL.format(year=year, kind=kind), path)
    return path


def _read(path, usecols):
    """Read selected columns from a zipped CSV (only those that actually exist)."""
    with zipfile.ZipFile(path) as z:
        inner = z.namelist()[0]
        header = pd.read_csv(z.open(inner), nrows=0).columns
        cols = [c for c in usecols if c in header]
        return pd.read_csv(z.open(inner), usecols=cols, low_memory=False)


def load_year(year):
    """All births (died=0) stacked with linked infant deaths (died=1) for one year."""
    den = _read(_download(year, "den"), KEEP)
    den["died"] = 0
    num = _read(_download(year, "num"), KEEP)
    num["died"] = 1
    out = pd.concat([den, num], ignore_index=True)
    out["year"] = year
    return out


def load_raw(years=MICRODATA_YEARS):
    return pd.concat([load_year(y) for y in years], ignore_index=True)


def tidy(raw=None, years=MICRODATA_YEARS):
    """Decode the raw codes into a clean record-level modeling frame."""
    df = load_raw(years) if raw is None else raw.copy()
    out = pd.DataFrame({
        "year": df["year"],
        "died": df["died"].astype(int),
        "birthweight_g": df["dbwt"].replace(9999, np.nan),
        "gestation_wks": df["combgest"].replace(99, np.nan),
        "mother_age": df["mager41"],
        "plurality": df["dplural"],
        "infant_sex": df["sex"],
        "prenatal_care_month": df["precare"].replace(99, np.nan),
        "prenatal_visits": df["uprevis"].replace(99, np.nan),
        "mother_educ": df["meduc"].replace(9, np.nan),
        "mother_race_hisp": df["mracehisp"].map(RACE_HISP),
        "smoker": df["cig_rec"].map({"Y": 1, "N": 0}),
    })
    return out.reset_index(drop=True)
