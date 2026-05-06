from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...services.data_fetch import fetch_stock_data, FetchError, RANGE_PRESETS
from...services.storage import save_csv, list_cached, delete_csv

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