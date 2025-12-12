from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd

def plot_timeseries(df: pd.DataFrame, x: str, y: str, title: str = "", xlabel: str = "", ylabel: str = "", outfile: str | None = None):
    fig, ax = plt.subplots()
    ax.plot(df[x].values, df[y].values)
    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.grid(True, alpha=0.25)
    if outfile:
        fig.savefig(outfile, dpi=200, bbox_inches="tight")
    return fig, ax
