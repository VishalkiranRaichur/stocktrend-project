from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import pandas as pd

from ..config import Config
from .data_fetch import RANGE_PRESETS

@dataclass
class CachedDataset:
    ticker: str
    range_key: str
    range_label: str
    rows: int
    fetched_at: datetime
    path: Path

def _csv_path(ticker: str, range_key: str) -> Path:
    """
    Return the canonical CSV path for a (ticker, range_key) pair.
    """
    return Config.DATA_DIR / f"{ticker.upper()}_{range_key}.csv"

def csv_exists(ticker: str, range_key: str) -> bool:
    """
    True if a cached CSV exists for this (ticker, range_key)
    """
    return _csv_path(ticker, range_key).exists()

def save_csv(ticker: str, range_key: str, df: pd.DataFrame) -> Path:
    """
    Write df to data/{TICKER}_{range_key}.csv. 
    Overwrites if exists.
    Returns the file path.
    """
    path = _csv_path(ticker, range_key)
    df.to_csv(path)
    return path

def load_csv(ticker: str, range_key: str) -> pd.DataFrame:
    """
    Read the cached CSV. Returns DataFrame with the same schema
    as fetch_stock_data() returns.
    Raises FileNotFoundError if missing.
    """
    path = _csv_path(ticker, range_key)
    if not path.exists():
        raise FileNotFoundError(f"No cached data for {ticker} ({range_key})")
    df = pd.read_csv(path, index_col = "Date", parse_dates = ["Date"])
    df["Volume"] = df["Volume"].astype("int64")
    return df

def delete_csv(ticker: str, range_key: str) -> bool:
    """
    Delete the cached CSV. Returns True if a file was delete,
    False if it didn't exist.
    """
    path = _csv_path(ticker, range_key)
    if path.exists():
        path.unlink()
        return True
    return False

def list_cached() -> list[CachedDataset]:
    """
    List all cached datasets, newest first.
    """
    results = []
    for path in Config.DATA_DIR.glob("*.csv"):
        stem = path.stem
        if "_" not in stem:
            continue

        ticker, range_key = stem.rsplit("_", 1)
        if range_key not in RANGE_PRESETS:
            continue

        with open(path, "r", encoding="utf-8") as f:
            row_count = sum(1 for _ in f) - 1

        results.append(CachedDataset(
            ticker = ticker,
            range_key = range_key,
            range_label=RANGE_PRESETS[range_key]["label"],
            rows=max(row_count, 0),
            fetched_at=datetime.fromtimestamp(path.stat().st_mtime),
            path= path,
        ))

    results.sort(key=lambda d: d.fetched_at, reverse = True)
    return results

