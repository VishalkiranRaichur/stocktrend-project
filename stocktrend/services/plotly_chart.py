"""
Interactive Plotly chart for the detail page.
Matplotlib PNG export remains in visualization.py as a fallback / backup asset.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def build_price_chart_html(df, ticker: str) -> str:
    """
    Return an HTML fragment (div + script) for embedding in Jinja via |safe.

    Matches dashboard colors: cyan close, orange MA7, green MA30.
    """
    plot_df = df.copy()
    plot_df["MA7"] = plot_df["Close"].rolling(7).mean()
    plot_df["MA30"] = plot_df["Close"].rolling(30).mean()
    dates = plot_df.index

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=plot_df["Close"],
            mode="lines",
            name="Close",
            line={"color": "#5dceff", "width": 2.6},
            hovertemplate="%{x|%Y-%m-%d}<br><b>Close</b>: $%{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=plot_df["MA7"],
            mode="lines",
            name="7-day MA",
            line={"color": "#f0a848", "width": 2},
            hovertemplate="%{x|%Y-%m-%d}<br><b>7-day MA</b>: $%{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=plot_df["MA30"],
            mode="lines",
            name="30-day MA",
            line={"color": "#7dd89f", "width": 2},
            hovertemplate="%{x|%Y-%m-%d}<br><b>30-day MA</b>: $%{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",
        font={"color": "#d4d4d4", "family": "Plus Jakarta Sans, system-ui, sans-serif"},
        title={
            "text": f"{ticker.upper()} — price trend",
            "x": 0,
            "xanchor": "left",
            "font": {"size": 16, "color": "#ffffff"},
        },
        margin={"l": 56, "r": 24, "t": 48, "b": 48},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "bgcolor": "rgba(31,31,31,0.85)",
            "bordercolor": "#454545",
            "borderwidth": 1,
        },
        xaxis={
            "showgrid": True,
            "gridcolor": "rgba(61,61,61,0.6)",
            "linecolor": "#333333",
            "zeroline": False,
        },
        yaxis={
            "title": "Price (USD)",
            "showgrid": True,
            "gridcolor": "rgba(61,61,61,0.6)",
            "linecolor": "#333333",
            "zeroline": False,
        },
        hovermode="x unified",
        autosize=True,
        height=460,
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "responsive": True,
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
    )


def build_compare_normalized_chart_html(
    merged: pd.DataFrame,
    ticker_a: str,
    ticker_b: str,
    norm_a: pd.Series,
    norm_b: pd.Series,
    align_mode: str,
) -> str:
    """
    Two normalized close lines (start at 100). merged index: DatetimeIndex or integer steps.
    """
    x = merged.index
    if align_mode == "position":
        x = pd.RangeIndex(stop=len(merged))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=norm_a.values,
            mode="lines",
            name=ticker_a.upper(),
            line={"color": "#5dceff", "width": 2.6},
            hovertemplate=(
                "%{x}<br><b>"
                + ticker_a.upper()
                + "</b>: %{y:.2f} (index)<extra></extra>"
                if align_mode == "position"
                else "%{x|%Y-%m-%d}<br><b>"
                + ticker_a.upper()
                + "</b>: %{y:.2f}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=norm_b.values,
            mode="lines",
            name=ticker_b.upper(),
            line={"color": "#f0a848", "width": 2.6},
            hovertemplate=(
                "%{x}<br><b>"
                + ticker_b.upper()
                + "</b>: %{y:.2f} (index)<extra></extra>"
                if align_mode == "position"
                else "%{x|%Y-%m-%d}<br><b>"
                + ticker_b.upper()
                + "</b>: %{y:.2f}<extra></extra>"
            ),
        )
    )

    x_title = "Date" if align_mode == "calendar" else "Session (recent rows aligned)"

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",
        font={"color": "#d4d4d4", "family": "Plus Jakarta Sans, system-ui, sans-serif"},
        title={
            "text": "Normalized close (start = 100)",
            "x": 0,
            "xanchor": "left",
            "font": {"size": 16, "color": "#ffffff"},
        },
        margin={"l": 56, "r": 24, "t": 48, "b": 48},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "bgcolor": "rgba(31,31,31,0.85)",
            "bordercolor": "#454545",
            "borderwidth": 1,
        },
        xaxis={
            "title": x_title,
            "showgrid": True,
            "gridcolor": "rgba(61,61,61,0.6)",
            "linecolor": "#333333",
            "zeroline": False,
        },
        yaxis={
            "title": "Indexed level (100 = start)",
            "showgrid": True,
            "gridcolor": "rgba(61,61,61,0.6)",
            "linecolor": "#333333",
            "zeroline": False,
        },
        hovermode="x unified",
        autosize=True,
        height=460,
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "responsive": True,
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
    )
