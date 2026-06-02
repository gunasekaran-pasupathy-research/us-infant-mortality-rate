import pandas as pd

from src.data.clean import clean, to_wide, black_white_gap


def _raw():
    # mimics the raw CDC quirk: 'Black' and 'Black ' are the same group
    return pd.DataFrame({
        "race": ["Black", "Black ", "White", "White"],
        "year": ["1915", "1916", "1915", "1916"],
        "infant_mortality_rate": ["195.2", "184.3", "98.6", "99.0"],
    })


def test_clean_strips_race_whitespace():
    out = clean(_raw())
    assert set(out["race"].unique()) == {"Black", "White"}


def test_clean_fixes_types():
    out = clean(_raw())
    assert out["year"].dtype.kind == "i"
    assert out["infant_mortality_rate"].dtype.kind == "f"


def test_to_wide_shape():
    wide = to_wide(clean(_raw()))
    assert list(wide.columns) == ["Black", "White"]
    assert list(wide.index) == [1915, 1916]


def test_black_white_gap():
    gap = black_white_gap(clean(_raw()))
    assert gap.loc[1915, "difference"] == 195.2 - 98.6
    assert round(gap.loc[1915, "ratio"], 3) == round(195.2 / 98.6, 3)
