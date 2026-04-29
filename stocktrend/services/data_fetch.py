from datetime import date, timedelta
import requests
import pandas as pd

from ..config import Config

API_URL = "https://api.twelvedata.com/time_series"
TIMEOUT_SECONDS = 15

RANGE_PRESETS = {
    "5d":   {"label": "5 days",       "days_back": 7},
    "1mo":  {"label": "1 month",      "days_back": 30},
    "3mo":  {"label": "3 months",     "days_back": 90},
    "6mo":  {"label": "6 months",     "days_back": 180},
    "ytd":  {"label": "Year to date", "days_back": "ytd"},
    "1y":   {"label": "1 year",       "days_back": 365},
    "2y":   {"label": "2 years",      "days_back": 730},
    "5y":   {"label": "5 years",      "days_back": 1825},
    "10y":  {"label": "10 years",     "days_back": 3650},
    "max":  {"label": "Max",          "days_back": "max"},
}

class FetchError(Exception):
    """Raisen when fetching from TwelveData fails for any reason"""

def _start_date_for(range_key: str) -> date:
    """Convert a range_key into the earliest date to request"""
    today = date.today()
    spec = RANGE_PRESETS[range_key]["days_back"]
    if spec == "ytd":
        return date(today.year, 1, 1)
    if spec == "max":
        return date(2000, 1, 1)
    return today - timedelta(days=spec)

def fetch_stock_data(ticker: str, range_key: str) -> pd.DataFrame:
    """
    Fetcj historical daily OHLCV from Twelve Data.

    Returns a DataFrame with DatetimeIndex name 'Date'
    """
    if range_key not in RANGE_PRESETS:
        raise ValueError(f"Unknown range_key: {range_key!r}")
    
    if not Config.TWELVEDATA_API_KEY:
        raise FetchError("API key invalid or missing.")
    
    ticker = ticker.strip().upper()
    if not ticker:
        raise FetchError("Ticker is empty.")

    params = {
        "symbol": ticker,
        "interval": "1day",
        "start_date": _start_date_for(range_key).isoformat(),
        "end_date": date.today().isoformat(),
        "apikey": Config.TWELVEDATA_API_KEY,
        "outputsize": 5000,
    }
    try:
        response = requests.get(API_URL, params=params, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        raise FetchError("Request to Twelve Data timed out. Try again.")
    except requests.exceptions.RequestException as e:
        raise FetchError(f"Network error: {e}") from e
    
    if response.status_code == 401:
        raise FetchError("API key invalid or missing.")
    if response.status_code == 429:
        raise FetchError("Rate limit exceeded - try again in a minute.")
    if response.status_code >= 500:
        raise FetchError(f"Twelve Data server error ({response.status_code}). Try again later.")
    
    try:
        data = response.json()
    except ValueError:
        raise FetchError("Could not parse response from Twelve Data")
    
    if isinstance(data,dict) and data.get("status") == "error":
        code = data.get("code")
        message = data.get("message", "Unknown error")
        if code == 401:
            raise FetchError("API key invalid or missing.")
        if code == 429:
            raise FetchError("Rate limit exceeded - try again in a minute.")
        if code == 400:
            raise FetchError(f"Could not find data for ticker '{ticker}'.")
        raise FetchError(message)

    values = data.get("values")
    if not values:
        raise FetchError(f"No data returned for {ticker} in range {range_key}.")
    
    
    df = pd.DataFrame(values)
    required = {"datetime", "open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns):
        raise FetchError("Response from Twelve Data is missing expected fields.")

    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("int64")
    df = df.dropna(subset=["open", "high", "low", "close"])

    df = df.rename(columns={
        "datetime": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    })

    df = df.set_index("Date").sort_index()
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    return df