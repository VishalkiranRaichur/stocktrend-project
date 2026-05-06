import pandas as pd

def analyze_stock(df):
    result = {}

    # Basic stats
    result["latest_price"] = round(df["Close"].iloc[-1], 2)
    result["avg_price"] = round(df["Close"].mean(), 2)
    result["max_price"] = round(df["Close"].max(), 2)
    result["min_price"] = round(df["Close"].min(), 2)

    # Percentage change
    start = df["Close"].iloc[0]
    end = df["Close"].iloc[-1]
    result["percent_change"] = round(((end - start) / start) * 100, 2)

    # Daily returns
    df["daily_return"] = df["Close"].pct_change()
    result["avg_daily_return"] = round(df["daily_return"].mean() * 100, 2)

    # Volatility
    result["volatility"] = round(df["daily_return"].std() * 100, 2)

    # Trend
    if result["percent_change"] > 2:
        result["trend"] = "Uptrend 📈"
    elif result["percent_change"] < -2:
        result["trend"] = "Downtrend 📉"
    else:
        result["trend"] = "Sideways ➡️"

    return result