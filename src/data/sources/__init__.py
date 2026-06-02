"""One module per data source. Each exposes load() (raw, cached) and tidy()."""
from src.data.sources import cdc, world_bank, who, owid, un_igme

ALL = {
    "cdc": cdc,
    "world_bank": world_bank,
    "who": who,
    "owid": owid,
    "un_igme": un_igme,
}
