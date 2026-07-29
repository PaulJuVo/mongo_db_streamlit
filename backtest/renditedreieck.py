import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from typing import Optional
from pathlib import Path


def plot_renditedreieck(
    df_long: pd.DataFrame,
    sektor: str,
    strategie: str,
    titel: Optional[str] = None,
    label: Optional[str] = None,
    vmin: float = -15,
    vmax: float = 30,
    annot: bool = True,
    save_path: Optional[str] = None
):
    """
    Plottet ein einzelnes Renditedreieck für einen gegebenen Sektor und Score.

    Parameter
    ----------
    df_long    : DataFrame mit Spalten [buyyear, sellyear, sector, rendite, strategy]
    sektor     : Sektorname z.B. "Utilities"
    strategie  : strategy-Wert z.B. "value_score" oder "momentum_score"
    label      : Anzeigetitel (default: strategie)
    vmin       : Untere Grenze der Farbskala (%)
    vmax       : Obere Grenze der Farbskala (%)
    annot      : Zellwerte anzeigen
    save_path  : Wenn angegeben, wird die Grafik gespeichert z.B. "output/utilities.png"
    """

    label = label or strategie

    # ── Farbskala: Rot → Weiß → Grün ───────────────────────────────────────
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "rdwgn",
        [
            (0.0,  "#C0182A"),
            (0.35, "#F4A7A7"),
            (0.5,  "#FFFFFF"),
            (0.65, "#A8D5A2"),
            (1.0,  "#1A7A34"),
        ]
    )

    # ── Pivot ───────────────────────────────────────────────────────────────
    subset = df_long[
        (df_long["sector"]   == sektor) &
        (df_long["strategy"] == strategie)
    ]
    pivot = subset.pivot(index="buyyear", columns="sellyear", values="rendite")

    # ── Plot ─────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 9))

    sns.heatmap(
        pivot.round(2),
        cmap=cmap,
        center=0,
        annot=annot,
        fmt=".1f",
        linewidths=0.5,
        linecolor="white",
        vmin=vmin,
        vmax=vmax,
        mask=pivot.isna(),
        cbar=True,
        cbar_kws={
            "label": "CAGR (%)", 
            "shrink": 0.75, 
            "pad": 0.08        # mehr Abstand zur Heatmap
        },
        annot_kws={"size": 9},
        ax=ax
    )

    ax.set_title(label, fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Verkaufsjahr", fontsize=11, labelpad=8)
    ax.set_ylabel("Kaufjahr",     fontsize=11, labelpad=8)

    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.yaxis.set_ticks_position("right")
    ax.yaxis.set_label_position("right")

    plt.xticks(rotation=45, ha="left", fontsize=9)
    plt.yticks(rotation=0,             fontsize=9)

    ax.set_facecolor("#F7F7F7")

    if not titel:
        titel = "Renditedreieck"

    fig.suptitle(
        f"{titel} — {sektor}  |  CAGR in %",
        fontsize=15,
        fontweight="bold",
        y=1.02
    )

    plt.tight_layout()
    fig.subplots_adjust(top=0.88)

    if save_path:
        output_dir = Path(save_path) / sektor.lower().replace(" ", "_")
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / f"{strategie}_{titel}.png"
        fig.savefig(file_path, dpi=150, bbox_inches="tight")

    print(f"Gespeichert: {file_path}")

    plt.close(fig)       # kein plt.show() — Jupyter zeigt fig automatisch beim return
    return fig