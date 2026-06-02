from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# CDC / NCHS "Infant Mortality Rates, by Race: United States, 1915-2013".
# Pulled from the data.cdc.gov Socrata API (no key needed for this volume).
CDC_DATASET_ID = "ddsk-zebd"
CDC_CSV_URL = f"https://data.cdc.gov/resource/{CDC_DATASET_ID}.csv?$limit=50000"
RAW_FILENAME = "nchs_infant_mortality_by_race.csv"

RATE_COL = "infant_mortality_rate"  # deaths per 1,000 live births
RANDOM_STATE = 42
