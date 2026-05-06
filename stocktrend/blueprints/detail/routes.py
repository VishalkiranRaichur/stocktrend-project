from flask import Blueprint, render_template
from ...services.analysis import analyze_stock
from ...services.visualization import plot_stock
from ...services.plotly_chart import build_price_chart_html
from ...services.storage import list_cached, load_csv

detail_bp = Blueprint("detail", __name__)

@detail_bp.route("/detail/<ticker>/<range_key>")
def detail(ticker, range_key):
    cached = list_cached()

    entry = None
    for item in cached:
        if item.ticker == ticker and item.range_key == range_key:
            entry = item
            break

    if entry is None:
        return "File not found", 404

    df = load_csv(entry.ticker, entry.range_key)

    analysis = analyze_stock(df)
    # Keep matplotlib PNG generation as backup / static asset
    plot_stock(df, ticker)
    plot_chart_html = build_price_chart_html(df, ticker)

    return render_template(
        "detail.html",
        ticker=ticker,
        analysis=analysis,
        plot_chart_html=plot_chart_html,
    )
