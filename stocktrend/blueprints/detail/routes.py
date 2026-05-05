from flask import Blueprint, render_template
import pandas as pd
from ...services.analysis import analyze_stock
from ...services.visualization import plot_stock
from ...services.storage import list_cached

detail_bp = Blueprint("detail", __name__)

@detail_bp.route("/detail/<ticker>")
def detail(ticker):
    cached = list_cached()

    # find matching file
    file = None
    for entry in cached:
        if entry.ticker == ticker:
            file = entry.path
            break

    if not file:
        return "File not found", 404

    df = pd.read_csv(file)

    analysis = analyze_stock(df)
    plot_path = plot_stock(df, ticker)

    return render_template(
        "detail.html",
        ticker=ticker,
        analysis=analysis,
        plot_path=plot_path
    )