# U.S. Infant Mortality Rate (1915–2013)

A statistical analysis of historical U.S. infant mortality rates (IMR) by race,
using CDC / NCHS data. A companion project to the AAI-500 coursework, applying
the same probability-and-statistics toolkit (descriptive statistics, estimation,
significance testing, and regression) to a long historical time series.

## Project Overview

Infant mortality — deaths before age one per 1,000 live births — is a core
population-health indicator. The U.S. rate fell dramatically over the twentieth
century, but a persistent gap between Black and White infants did not close.
This project documents and quantifies those two stories.

**Objectives**

1. Pull and validate the CDC/NCHS historical series.
2. Describe the distribution and the long-run trend of the rate.
3. Quantify and test the Black–White disparity over time.
4. Model the decline (e.g., regression on year, including a log scale) and
   clearly document limitations.

## Dataset

**Source.** CDC / NCHS — *Infant Mortality Rates, by Race: United States,
1915–2013*, served from the [data.cdc.gov Socrata API](https://data.cdc.gov/National-Center-for-Health-Statistics/NCHS-Infant-Mortality-Rates-by-Race-United-States-/ddsk-zebd)
(dataset id `ddsk-zebd`). No API key is required at this volume. The raw CSV is
**not** committed — `src.data.load.load_raw()` pulls it on first use and caches a
copy in `data/raw/`.

| Column | Description |
|---|---|
| `race` | Black or White (the raw data also contains a stray `"Black "` with a trailing space) |
| `year` | calendar year, 1915–2013 |
| `infant_mortality_rate` | deaths before age 1 per 1,000 live births |

198 rows (2 race groups × 99 years).

**Known data-quality issues**

- The same group is spelled two ways: `"Black"` and `"Black "` (trailing space).
  `src/data/clean.py` strips the whitespace so the group is not split in two.

## Repository Structure

```
.
├── data/
│   ├── raw/         # untracked — CDC pull cached here
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_statistical_testing.ipynb
│   └── 04_modeling.ipynb
├── src/
│   ├── config.py    # paths, dataset id, constants
│   ├── data/        # load (CDC pull) and clean
│   └── viz/         # plotting helpers
├── reports/         # tracked figures, tables, and write-ups
├── tests/           # pytest unit tests for src/
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The dataset is pulled automatically the first time `load_raw()` runs (it just
reads the public CDC API — no credentials needed):

```bash
python -c "from src.data.load import load_raw; print(load_raw().shape)"
```

The notebooks add the project root to `sys.path`, so `from src.config import ...`
works without an editable install.

## Running the Analysis

```bash
jupyter notebook
```

| # | Notebook | Purpose |
|---|---|---|
| 01 | `01_eda.ipynb` | Load the data, summarize the rate, plot the long-run trend by race. |
| 02 | `02_cleaning.ipynb` | Fix the race-label whitespace, set types, save the cleaned/ wide tables. |
| 03 | `03_statistical_testing.ipynb` | Quantify and test the Black–White disparity; correlate year with the rate. |
| 04 | `04_modeling.ipynb` | Regress the rate on year (linear and log scale) to characterize the decline. |

## Testing

```bash
pytest
```

## Methodology Notes

- **Reproducibility.** The CDC pull is cached locally and the dataset id is
  pinned in `src/config.py`.
- **Aggregate data.** These are published yearly rates, not individual records,
  so the analysis is descriptive and trend-focused; group comparisons treat the
  paired yearly rates rather than patient-level observations.

## Limitations (working list)

- Aggregate national rates only — no individual-level covariates.
- Race is limited to Black and White in this historical series.
- Rates across years are not independent observations (autocorrelation), which a
  simple regression does not fully account for.
- This is a coursework-style analysis, not a demographic research product.

## References

- CDC / NCHS, *Infant Mortality Rates, by Race: United States, 1915–2013*.
- University of San Diego, AAI-500 *Probability and Statistics for AI*.
