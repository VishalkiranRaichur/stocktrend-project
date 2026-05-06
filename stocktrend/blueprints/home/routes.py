from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...services.analysis import analyze_stock
from ...services.compare import (
    align_closes,
    comparison_insight,
    normalize_to_100,
    parse_stock_key,
)
from ...services.data_fetch import fetch_stock_data, FetchError, RANGE_PRESETS
from ...services.plotly_chart import build_compare_normalized_chart_html
from ...services.storage import load_csv, save_csv, list_cached, delete_csv

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template(
        "home.html",
        cached=list_cached(),
        range_presets=RANGE_PRESETS,
    )

@home_bp.route("/fetch", methods=["POST"])
def fetch():
    ticker = (request.form.get("ticker") or "").strip().upper()
    range_key = request.form.get("range_key", "")

    if not ticker:
        flash("Please enter a ticker symbol.", "error")
        return redirect(url_for("home.home"))
    
    if range_key not in RANGE_PRESETS:
        flash("Invalid date range.", "error")
        return redirect(url_for("home.home"))
    
    try:
        df = fetch_stock_data(ticker, range_key)
        save_csv(ticker, range_key, df)
        label = RANGE_PRESETS[range_key]["label"]
        flash(f"Saved {ticker} ({label}) - {len(df)} rows.", "success")
    except FetchError as e:
        flash(str(e), "error")
    except OSError:
        flash("Could not save data file. Check disk space.", "error")

    return redirect(url_for("home.home"))


def _cache_entry_exists(ticker: str, range_key: str):
    ticker = ticker.upper()
    for item in list_cached():
        if item.ticker.upper() == ticker and item.range_key == range_key:
            return item
    return None


@home_bp.route("/compare", methods=["POST"])
def compare_view():
    """Compare two cached datasets (normalized close chart + side-by-side stats)."""
    raw_a = (request.form.get("stock_a") or "").strip()
    raw_b = (request.form.get("stock_b") or "").strip()
    parsed_a = parse_stock_key(raw_a)
    parsed_b = parse_stock_key(raw_b)
    if not parsed_a or not parsed_b:
        flash("Pick two datasets from your cache.", "error")
        return redirect(url_for("home.home"))

    ta, ra = parsed_a
    tb, rb = parsed_b
    if ta.upper() == tb.upper() and ra == rb:
        flash("Choose two different datasets to compare.", "error")
        return redirect(url_for("home.home"))

    entry_a = _cache_entry_exists(ta, ra)
    entry_b = _cache_entry_exists(tb, rb)
    if entry_a is None or entry_b is None:
        flash("One or both selections are missing from cache.", "error")
        return redirect(url_for("home.home"))

    try:
        df_a = load_csv(entry_a.ticker, entry_a.range_key)
        df_b = load_csv(entry_b.ticker, entry_b.range_key)
    except FileNotFoundError:
        flash("Could not read a cached CSV file.", "error")
        return redirect(url_for("home.home"))

    merged, align_mode = align_closes(df_a, df_b)
    if merged.empty or len(merged) < 2 or align_mode == "none":
        flash("Not enough overlapping rows to compare these two caches.", "error")
        return redirect(url_for("home.home"))

    norm_a = normalize_to_100(merged["close_a"])
    norm_b = normalize_to_100(merged["close_b"])

    analysis_a = analyze_stock(df_a)
    analysis_b = analyze_stock(df_b)

    insight = comparison_insight(ta, tb, float(norm_a.iloc[-1]), float(norm_b.iloc[-1]))

    if align_mode == "calendar":
        align_note = (
            f"Aligned on {len(merged)} trading days where both series share a date."
        )
    else:
        align_note = (
            f"No shared dates in range; using the last {len(merged)} rows from each "
            f"cache (positional alignment)."
        )

    plot_chart_html = build_compare_normalized_chart_html(
        merged, ta, tb, norm_a, norm_b, align_mode
    )

    return render_template(
        "compare.html",
        ticker_a=entry_a.ticker,
        ticker_b=entry_b.ticker,
        range_label_a=entry_a.range_label,
        range_label_b=entry_b.range_label,
        analysis_a=analysis_a,
        analysis_b=analysis_b,
        insight=insight,
        align_note=align_note,
        plot_chart_html=plot_chart_html,
    )


@home_bp.route("/delete/<ticker>/<range_key>", methods=["POST"])
def delete(ticker, range_key):
    ticker = ticker.upper()
    if delete_csv(ticker, range_key):
        flash(f"Deleted {ticker} ({range_key}).", "success")
    else:
        flash(f"No cached data for {ticker} ({range_key}).", "error")
    return redirect(url_for("home.home"))

@home_bp.route("/refresh/<ticker>/<range_key>", methods=["POST"])
def refresh(ticker, range_key):
    ticker = ticker.upper()
    if range_key not in RANGE_PRESETS:
        flash("Invalid date range.", "error")
        return redirect(url_for("home.home"))
    
    try:
        df = fetch_stock_data(ticker, range_key)
        save_csv(ticker, range_key, df)
        label = RANGE_PRESETS[range_key]["label"]
        flash(f"Refreshed {ticker} ({label}) - {len(df)} rows.", "success")
    except FetchError as e:
        flash(str(e), "error")
    except OSError:
        flash("Could not save data file. Check disk space.", "error")
    
    return redirect(url_for("home.home"))