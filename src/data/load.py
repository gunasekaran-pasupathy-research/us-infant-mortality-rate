import pandas as pd

from src.config import CDC_CSV_URL, RAW_DIR, RAW_FILENAME


def download_raw():
    """Pull the dataset from the CDC Socrata API and cache it in data/raw/."""
    df = pd.read_csv(CDC_CSV_URL)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dest = RAW_DIR / RAW_FILENAME
    df.to_csv(dest, index=False)
    return dest


def load_raw():
    path = RAW_DIR / RAW_FILENAME
    if not path.exists():
        path = download_raw()
    return pd.read_csv(path)
