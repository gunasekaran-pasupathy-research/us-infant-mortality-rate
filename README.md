# U.S. Infant Mortality Rate — A Multi-Source Analysis

A statistical analysis of infant mortality rates (IMR — deaths before age one per
1,000 live births), combining **five public data sources**. A companion project to
the AAI-500 coursework, applying the probability-and-statistics toolkit
(descriptive statistics, estimation, significance testing, and regression) to the
U.S. by-race history *and* the U.S. in global context.

## Data sources

Each source has its own loader under `src/data/sources/`. Every loader pulls from
a public endpoint (no API key needed), caches the raw file in `data/raw/`, and
tidies to a common schema. `src/data/harmonize.py` stacks them into one panel.

| Source | Module | Coverage | Notes |
|---|---|---|---|
| **CDC / NCHS** | `cdc.py` | U.S. by race, 1915–2013 | the Black–White disparity series |
| **World Bank** (WDI) | `world_bank.py` | ~200 countries, 1960–2024 | `SP.DYN.IMRT.IN` |
| **WHO** (GHO) | `who.py` | ~200 countries, 1932–2023 | carries uncertainty bounds |
| **Our World in Data** | `owid.py` | global, long historical | value is a percent → ×10 |
| **UN IGME** (UNICEF) | `un_igme.py` | ~200 countries, 1931–2024 | the canonical UN estimates + bounds |

**Common tidy schema** (`src.config.TIDY_COLUMNS`):

```
source, entity, iso3, entity_type, year, imr, imr_low, imr_high
```

`entity_type` is `country` for the global sources and `us_race` for CDC.

**Known data-quality issues**

- CDC spells one group two ways — `"Black"` and `"Black "` (trailing space);
  `cdc.tidy()` strips the whitespace so it is not split in two.
- The global sources include regional/income aggregates ("World", etc.); each
  loader keeps only real countries (ISO-3 codes).
- The four country-level sources largely derive from UN IGME, so their close
  agreement is **consistency, not independent corroboration**.

## What the analysis covers

1. **Cross-source validation** — do the sources agree on the U.S. rate where they
   overlap? (notebook 05)
2. **U.S. in global context** — the U.S. ranks ~47th of ~196 countries despite its
   wealth. (notebook 05)
3. **Long-run global trend** — the century-plus worldwide decline. (notebook 05)
4. **The Black–White disparity** — quantified and tested on the CDC series.
   (notebooks 01, 03, 04)

## Repository Structure

```
.
├── data/{raw,interim,processed}/     # raw cache is untracked
├── notebooks/
│   ├── 01_eda.ipynb                  # CDC: trend by race
│   ├── 02_cleaning.ipynb             # CDC: fix labels, save tidy tables
│   ├── 03_statistical_testing.ipynb  # CDC: test the Black–White disparity
│   ├── 04_modeling.ipynb             # CDC: regress the decline (linear + log)
│   └── 05_multisource.ipynb          # all sources: validation, global context, trend
├── src/
│   ├── config.py                     # paths, endpoints, tidy schema
│   ├── data/
│   │   ├── sources/                  # one loader per source
│   │   └── harmonize.py              # stack sources into one panel
│   └── viz/plots.py
├── reports/                          # tracked figures, tables, write-ups
├── tests/
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Each source is pulled automatically on first use (public endpoints, no keys):

```python
from src.data import harmonize
panel = harmonize.load_all()          # all five sources, tidy
harmonize.us_across_sources(panel)    # U.S. rate by year and source
```

Or one source at a time:

```python
from src.data.sources import cdc, world_bank
cdc.tidy()            # U.S. by race
world_bank.tidy()     # all countries
```

## Running the Analysis

```bash
jupyter notebook
```

Run the notebooks in order (01–04 are the CDC deep dive; 05 is the multi-source
comparison).

## Testing

```bash
pytest
```

The tests exercise each loader's `tidy()` on small fixtures (no network), covering
the whitespace fix, the percent→per-1,000 conversion, and aggregate filtering.

## Limitations (working list)

- Aggregate national rates — no individual-level covariates.
- CDC's historical series covers only Black and White.
- Yearly rates are autocorrelated; simple regressions understate the uncertainty.
- The global sources are not independent, so cross-source agreement is expected.
- Coursework-style analysis, not a demographic research product.

## References

- CDC / NCHS, *Infant Mortality Rates, by Race: United States, 1915–2013*.
- World Bank, *World Development Indicators* (`SP.DYN.IMRT.IN`).
- WHO, *Global Health Observatory* (`MDG_0000000001`).
- UN IGME / UNICEF, *Child Mortality Estimates* (`CME_MRY0`).
- Our World in Data, *Infant Mortality*.
