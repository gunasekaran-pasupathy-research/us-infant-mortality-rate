from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Infant mortality rate = deaths before age 1 per 1,000 live births.
# Every source loader tidies to this common schema:
TIDY_COLUMNS = ["source", "entity", "iso3", "entity_type", "year", "imr", "imr_low", "imr_high"]

# --- Source endpoints (all public, no API key needed) ---
# CDC / NCHS — Infant Mortality Rates, by Race: United States, 1915-2013
CDC_CSV_URL = "https://data.cdc.gov/resource/ddsk-zebd.csv?$limit=50000"
# World Bank — World Development Indicators, all countries 1960-present
WORLD_BANK_URL = (
    "https://api.worldbank.org/v2/country/all/indicator/"
    "SP.DYN.IMRT.IN?format=json&per_page=20000"
)
# WHO — Global Health Observatory (carries uncertainty bounds)
WHO_GHO_URL = "https://ghoapi.azureedge.net/api/MDG_0000000001"
# Our World in Data — long historical series (value is a percent; x10 -> per 1,000)
OWID_URL = "https://ourworldindata.org/grapher/infant-mortality.csv?csvType=full"
# UN IGME via the UNICEF SDMX API (carries uncertainty bounds)
UN_IGME_URL = (
    "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/"
    "UNICEF,CME,1.0/.CME_MRY0._T._T?format=csv"
)

# NCHS Period Linked Birth/Infant Death microdata (record level), hosted by NBER.
# This is the raw data behind the rates: one row per birth, with the infant-death
# outcome and birth-certificate covariates — used for individual risk modeling.
NBER_LINKED_URL = "https://data.nber.org/linkpe/{year}/linkpe{year}us{kind}.csv.zip"
MICRODATA_YEARS = [2011, 2012, 2013]

RANDOM_STATE = 42
