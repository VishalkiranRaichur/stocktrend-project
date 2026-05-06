import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt

# Match dashboard-ish dark neutrals / accents (cyan close, soften MA hues)
_THEME = {
    "fig_bg": "#141414",
    "ax_bg": "#141414",
    "grid": "#3d3d3d",
    "label": "#d4d4d4",
    "title": "#ffffff",
    "tick": "#a3a3a3",
    "spine": "#333333",
    "close_line": "#5dceff",
    "ma_fast": "#f0a848",
    "ma_slow": "#7dd89f",
}


def plot_stock(df, ticker):
    plots_dir = Path(__file__).resolve().parent.parent / "static" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    filepath = plots_dir / f"{ticker}.png"

    plot_df = df.copy()
    plot_df["MA7"] = plot_df["Close"].rolling(7).mean()
    plot_df["MA30"] = plot_df["Close"].rolling(30).mean()

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=_THEME["fig_bg"])
    ax.set_facecolor(_THEME["ax_bg"])

    lw_close = 2.35
    lw_ma = 1.95

    ax.plot(
        plot_df["Close"],
        label="Close",
        color=_THEME["close_line"],
        linewidth=lw_close,
        solid_capstyle="round",
        antialiased=True,
        zorder=3,
    )
    ax.plot(
        plot_df["MA7"],
        label="7-day MA",
        color=_THEME["ma_fast"],
        linewidth=lw_ma,
        solid_capstyle="round",
        antialiased=True,
        alpha=0.92,
        zorder=2,
    )
    ax.plot(
        plot_df["MA30"],
        label="30-day MA",
        color=_THEME["ma_slow"],
        linewidth=lw_ma,
        solid_capstyle="round",
        antialiased=True,
        alpha=0.9,
        zorder=1,
    )

    ax.set_title(
        f"{ticker} — price trend",
        color=_THEME["title"],
        fontsize=14,
        fontweight="semibold",
        pad=14,
        loc="left",
    )

    ax.set_ylabel("Price (USD)", color=_THEME["label"], fontsize=10)
    ax.tick_params(axis="both", colors=_THEME["tick"], labelsize=9)
    ax.yaxis.label.set_color(_THEME["label"])

    ax.grid(
        True,
        linestyle="-",
        linewidth=0.55,
        color=_THEME["grid"],
        alpha=0.38,
        zorder=0,
    )
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(_THEME["spine"])
        ax.spines[side].set_linewidth(0.7)

    legend = ax.legend(
        loc="upper left",
        frameon=True,
        fancybox=False,
        framealpha=0.96,
        facecolor="#1f1f1f",
        edgecolor="#454545",
        fontsize=9,
        labelcolor="#e8e8e8",
    )
    legend.get_frame().set_linewidth(0.6)

    fig.tight_layout(pad=0.6)
    fig.savefig(
        filepath,
        dpi=120,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.08,
    )
    plt.close(fig)

    return f"plots/{ticker}.png"
