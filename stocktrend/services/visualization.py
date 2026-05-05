import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

def plot_stock(df, ticker):
    os.makedirs("stocktrend/static/plots", exist_ok=True)

    filepath = f"stocktrend/static/plots/{ticker}.png"

    plt.figure(figsize=(10,5))
    plt.plot(df["Close"], label="Close Price")

    # Moving averages
    df["MA7"] = df["Close"].rolling(7).mean()
    df["MA30"] = df["Close"].rolling(30).mean()

    plt.plot(df["MA7"], label="7-day MA")
    plt.plot(df["MA30"], label="30-day MA")

    plt.title(f"{ticker} Stock Trend")
    plt.legend()

    plt.savefig(filepath)
    plt.close()

    return f"plots/{ticker}.png"