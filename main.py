import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

EEG_CHANNELS = [
    "Fp1",
    "Fp2",
    "F3",
    "F4",
    "F7",
    "F8",
    "Fz",
    "C3",
    "C4",
    "Cz",
    "P3",
    "P4",
    "Pz",
    "O1",
    "O2",
    "T3",
    "T4",
    "T5",
    "T6",
    "A1",
    "A2",
]

ECG_CHANNELS = ["X1:LEOG", "X2:REOG"]
TIME_COLUMN = "Time"
CM_COLUMN = "CM"


def load_data(path: str) -> pd.DataFrame:
    """Read the QUASAR CSV, ignoring comments"""
    return pd.read_csv(path, comment="#")


def make_plot(df: pd.DataFrame, out_html: str = "plot.html"):
    """Plot EEG + ECG + CM in stacked panes"""

    # How many rows? (EEG/ECG always; CM optional)
    has_cm = CM_COLUMN in df.columns
    rows = 3 if has_cm else 2
    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2] if rows == 3 else [0.75, 0.25],
    )

    # EEG (top)
    for ch in EEG_CHANNELS:
        if ch in df.columns:
            fig.add_trace(
                go.Scattergl(
                    x=df[TIME_COLUMN],
                    y=df[ch],
                    mode="lines",
                    name=f"EEG {ch} (µV)",
                    hovertemplate=f"{ch}=%{{y:.2f}} µV<extra></extra>",
                ),
                row=1,
                col=1,
            )
    fig.update_yaxes(title_text="EEG (µV)", row=1, col=1)

    # ECG (middle)
    for ch in ECG_CHANNELS:
        if ch in df.columns:
            fig.add_trace(
                go.Scattergl(
                    x=df[TIME_COLUMN],
                    y=df[ch],
                    mode="lines",
                    name=f"ECG {ch} (mV)",
                    hovertemplate=f"{ch}=%{{y:.3f}} mV<extra></extra>",
                ),
                row=2,
                col=1,
            )
    fig.update_yaxes(
        title_text="ECG (mV)",
        row=2,
        col=1,
    )

    # CM (bottom)
    if has_cm:
        fig.add_trace(
            go.Scattergl(
                x=df[TIME_COLUMN],
                y=df[CM_COLUMN],
                mode="lines",
                name="CM (reference)",
                line=dict(dash="dot"),
                hovertemplate="CM=%{y:.2f}<extra></extra>",
            ),
            row=3,
            col=1,
        )
        fig.update_yaxes(title_text="CM (arb. units)", row=3, col=1)

    t0 = float(df[TIME_COLUMN].min())
    t1 = float(df[TIME_COLUMN].max())
    span = t1 - t0

    def xr(p_start, p_end):
        """Convert start/end percentages (0..1) into absolute x ranges."""
        return [t0 + p_start * span, t0 + p_end * span]

    # Interactivity
    fig.update_layout(
        title="QUASAR EEG + ECG Viewer",
        xaxis3=dict(
            title="Time (s)",
            rangeslider=dict(visible=True, thickness=0.08),
            type="linear",
        ),
        hovermode="x unified",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1,
                y=1.1,
                buttons=[
                    dict(
                        label="Q1",
                        method="relayout",
                        args=[{"xaxis.range": xr(0.00, 0.25)}],
                    ),
                    dict(
                        label="Q2",
                        method="relayout",
                        args=[{"xaxis.range": xr(0.25, 0.50)}],
                    ),
                    dict(
                        label="Q3",
                        method="relayout",
                        args=[{"xaxis.range": xr(0.50, 0.75)}],
                    ),
                    dict(
                        label="Q4",
                        method="relayout",
                        args=[{"xaxis.range": xr(0.75, 1.00)}],
                    ),
                    dict(
                        label="All", method="relayout", args=[{"xaxis.autorange": True}]
                    ),
                ],
            )
        ],
    )

    fig.write_html(out_html, include_plotlyjs="cdn", full_html=True)
    fig.show()
    print(f"✅ Plot saved to {out_html}")


df = load_data("EEG and ECG data_02_raw.csv")
make_plot(df)
