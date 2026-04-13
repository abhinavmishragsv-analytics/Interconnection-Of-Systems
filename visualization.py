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

def plot_bode(systems):
    w = np.logspace(-2, 3, 800)
    fig, (ax_mag, ax_ph) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Bode Plot", color=A1, fontsize=12, fontweight="bold")
    
    ax_mag.grid(True, which="both", linestyle="--", alpha=0.35)
    ax_ph.grid(True, which="both", linestyle="--", alpha=0.35)
    
    for i, s in enumerate(systems):
        wo, mag, ph = s.bode(w)
        c = COLORS[i % len(COLORS)]
        ax_mag.semilogx(wo, mag, color=c, lw=1.8, label=s.name)
        ax_ph.semilogx(wo, ph,  color=c, lw=1.8, label=s.name)

    ax_mag.set_ylabel("Magnitude (dB)")
    ax_mag.legend(fontsize=7, loc="lower left")

    ax_ph.set_ylabel("Phase (\u00b0)")
    ax_ph.set_xlabel("\u03c9 (rad/s)")
    ax_ph.legend(fontsize=7, loc="lower left")
    
    plt.tight_layout()
    plt.show()

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
    plt.show()

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
    plt.show()

def plot_pz(system):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.axhline(0, color=GR, lw=1)
    ax.axvline(0, color=GR, lw=1)
    fig.suptitle(f"Pole-Zero Map - {system.name}", color=A4, fontsize=12, fontweight="bold")
    
    ax.set_xlabel("\u03c3 (Real)")
    ax.set_ylabel("j\u03c9 (Imag)")
    
    zeros, poles = system.poles_zeros()
    ax.scatter(poles.real, poles.imag, marker="x", s=90, color=A3, linewidths=2.2, zorder=5)
    ax.scatter(zeros.real, zeros.imag, marker="o", s=70, facecolors="none", edgecolors=A1, linewidths=2.2, zorder=5)
    
    handles = [
        Line2D([0],[0], color=A3, marker="x", lw=0, markersize=8, markeredgewidth=2, label="Poles"),
        Line2D([0],[0], color=A1, marker="o", lw=0, markersize=8, markerfacecolor="none", markeredgewidth=2, label="Zeros")
    ]
    ax.legend(handles=handles, fontsize=8, loc="upper right")
    plt.tight_layout()
    plt.show()

def plot_nyquist(system):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.axhline(0, color=GR, lw=1)
    ax.axvline(0, color=GR, lw=1)
    fig.suptitle(f"Nyquist Plot - {system.name}", color=A5, fontsize=12, fontweight="bold")
    
    w = np.logspace(-2, 3, 800)
    w, h = sig.freqresp(system.sys, w=w)
    
    ax.plot(h.real, h.imag, color=A1, lw=1.8, label="w > 0")
    ax.plot(h.real, -h.imag, color=A1, lw=1.8, ls="--", label="w < 0")
    
    ax.scatter(-1, 0, color="red", marker="+", s=100, zorder=5, label="(-1, 0)")
    
    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.show()