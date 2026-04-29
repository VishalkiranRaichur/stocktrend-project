from flask import Blueprint, render_template

detail_bp = Blueprint("detail", __name__, url_prefix = "/detail")

@detail_bp.route("/<ticker>/<range_key>")
def detail(ticker, range_key):
    return render_template(
        "detail.html",
        ticker = ticker.upper(),
        range_key=range_key,
    )