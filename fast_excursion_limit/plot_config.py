from pathlib import Path

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib import font_manager

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"
FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

for _font in FONTS_DIR.glob("*.otf"):
    font_manager.fontManager.addfont(str(_font))

TWO_PANEL_FIGSIZE = (6.5, 3.5)

COLORS = ["#29a6a6", "#6829a6", "#2949a6", "#a62987"]


def set_style() -> None:
    plt.style.use(
        {
            "axes.grid": True,
            "axes.labelsize": 9,
            "axes.prop_cycle": cycler(color=COLORS),
            "axes.titlesize": 9,
            "figure.dpi": 150,
            "font.family": ["Latin Modern Roman"],
            "font.size": 9,
            "grid.alpha": 0.5,
            "grid.linewidth": 0.5,
            "legend.fontsize": 8,
            "legend.frameon": False,
            "lines.linewidth": 0.6,
            "mathtext.fontset": "cm",
            "savefig.bbox": "tight",
            "savefig.dpi": 300,
            "savefig.format": "pdf",
            "xtick.direction": "in",
            "xtick.labelsize": 8,
            "xtick.top": True,
            "ytick.direction": "in",
            "ytick.labelsize": 8,
            "ytick.right": True,
        }
    )
