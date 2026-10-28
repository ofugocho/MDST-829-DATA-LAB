"""
A consistent, publication-ready figure style.

    from src.plotting import set_publication_style, save_figure
    set_publication_style()
    fig, ax = plt.subplots()
    ...
    save_figure(fig, "fig1_yield_by_seed")   # -> figures/fig1_yield_by_seed.png and .pdf
"""

from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "figures"

# Colour-blind-safe palette (Okabe & Ito)
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]


def set_publication_style(font_size: int = 11) -> None:
    plt.rcParams.update({
        "figure.figsize": (6.5, 4.0),   # fits a single journal column / A4 thesis page
        "figure.dpi": 110,
        "savefig.dpi": 300,             # most journals ask for at least 300 dpi
        "savefig.bbox": "tight",
        "font.size": font_size,
        "axes.titlesize": font_size + 1,
        "axes.labelsize": font_size,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "legend.frameon": False,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
    })


def save_figure(fig, name: str, formats=("png", "pdf")) -> list[Path]:
    """Save a figure in several formats: PNG for Word, PDF (vector) for LaTeX."""
    FIGURES_DIR.mkdir(exist_ok=True)
    paths = []
    for fmt in formats:
        path = FIGURES_DIR / f"{name}.{fmt}"
        fig.savefig(path)
        paths.append(path)
    return paths
