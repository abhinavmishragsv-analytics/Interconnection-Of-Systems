import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.signal as sig

# Colours
DARK_BG  = "#0d1117"
PANEL_BG = "#161b22"
A1 = "#58a6ff"   # blue
A2 = "#3fb950"   # green
A3 = "#f78166"   # orange-red
A4 = "#d2a8ff"   # purple
A5 = "#e3b341"   # amber
TX = "#c9d1d9"   # body text
GR = "#21262d"   # grid lines

COLORS = [A1, A2, A3, A4, A5]

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    PANEL_BG,
    "axes.edgecolor":    GR,
    "axes.labelcolor":   TX,
    "axes.titlecolor":   TX,
    "xtick.color":       TX,
    "ytick.color":       TX,
    "grid.color":        GR,
    "text.color":        TX,
    "legend.facecolor":  PANEL_BG,
    "legend.edgecolor":  GR,
    "font.family":       "monospace",
    "font.size":         8,
})


def plot_step(systems):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.suptitle("Step Response", color=A2, fontsize=12, fontweight="bold")
    
    for i, s in enumerate(systems):
        c = COLORS[i % len(COLORS)]
        try:
            ts, ys = s.step_resp()
            ax.plot(ts, ys, color=c, lw=1.8, label=s.name)
        except Exception:
            pass
        
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend(fontsize=7)
    plt.tight_layout()
    return fig

def plot_impulse(systems):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.suptitle("Impulse Response", color=A3, fontsize=12, fontweight="bold")
    
    for i, s in enumerate(systems):
        c = COLORS[i % len(COLORS)]
        try:
            ti, yi = s.impulse_resp()
            ax.plot(ti, yi, color=c, lw=1.8, label=s.name)
        except Exception:
            pass
        
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend(fontsize=7)
    plt.tight_layout()
    return fig