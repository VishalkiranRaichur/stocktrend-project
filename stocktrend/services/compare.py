"""
Helpers to compare two cached stock datasets (align dates or recent rows, normalize to 100).
"""

from __future__ import annotations

import pandas as pd


def parse_stock_key(raw: str) -> tuple[str, str] | None:
    """
    Form value is "TICKER|range_key" (range_key has no pipe).
    """
    if not raw or "|" not in raw:
        return None
    ticker, range_key = raw.split("|", 1)
    ticker = ticker.strip().upper()
    range_key = range_key.strip()
    if not ticker or not range_key:
        return None
    return ticker, range_key


def align_closes(df_a: pd.DataFrame, df_b: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Return merged frame with columns close_a, close_b and alignment mode.

    1) Inner-join on the Date index (calendar overlap).
    2) If fewer than 2 rows, align by taking the last min(len) rows from each
       (positional / “recent overlap”) — useful when date ranges never meet.
    """
    a = df_a[["Close"]].copy()
    b = df_b[["Close"]].copy()
    a.columns = ["close_a"]
    b.columns = ["close_b"]

    merged = a.join(b, how="inner")
    if len(merged) >= 2:
        return merged, "calendar"

    m = min(len(df_a), len(df_b))
    if m < 2:
        return pd.DataFrame(), "none"

    tail_a = df_a["Close"].iloc[-m:].reset_index(drop=True)
    tail_b = df_b["Close"].iloc[-m:].reset_index(drop=True)
    merged_pos = pd.DataFrame({"close_a": tail_a, "close_b": tail_b})
    return merged_pos, "position"


def normalize_to_100(close: pd.Series) -> pd.Series:
    """Rebase series so its first value is 100."""
    first = close.iloc[0]
    if first == 0 or pd.isna(first):
        return close * 0 + 100.0  # degenerate fallback
    return (close / first) * 100.0


def comparison_insight(
    ticker_a: str,
    ticker_b: str,
    norm_last_a: float,
    norm_last_b: float,
) -> str:
    """Short winner / tie sentence based on normalized end values."""
    diff = norm_last_a - norm_last_b
    if abs(diff) < 0.2:
        return (
            f"{ticker_a.upper()} and {ticker_b.upper()} finished about tied "
            f"after normalizing both series to start at 100."
        )
    if norm_last_a > norm_last_b:
        return (
            f"{ticker_a.upper()} outperformed {ticker_b.upper()} over this aligned window "
            f"(normalized close ended higher)."
        )
    return (
        f"{ticker_b.upper()} outperformed {ticker_a.upper()} over this aligned window "
        f"(normalized close ended higher)."
    )
