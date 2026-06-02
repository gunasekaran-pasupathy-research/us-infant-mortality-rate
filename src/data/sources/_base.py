import json
import urllib.request

import pandas as pd

from src.config import RAW_DIR


def cached(filename, fetch):
    """Read data/raw/<filename>, calling fetch() to download + cache it if absent."""
    path = RAW_DIR / filename
    if not path.exists():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        fetch().to_csv(path, index=False)
    return pd.read_csv(path)


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)
