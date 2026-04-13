import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import scipy.signal as sig
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# COLOUR THEME
# ─────────────────────────────────────────────────────────────
DARK_BG  = "#0d1117"
PANEL_BG = "#161b22"
A1 = "#58a6ff"   # blue
A2 = "#3fb950"   # green
A3 = "#f78166"   # orange-red
A4 = "#d2a8ff"   # purple
A5 = "#e3b341"   # amber
TX = "#c9d1d9"   # body text
GR = "#21262d"   # grid lines

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

# ─────────────────────────────────────────────────────────────
# LTI SYSTEM CLASS
# ─────────────────────────────────────────────────────────────
class System:
    """Continuous-time LTI system via transfer function H(s)."""

    def __init__(self, num, den, name="H(s)"):
        self.sys  = sig.TransferFunction(num, den)
        self.name = name
        self.num  = np.atleast_1d(num).astype(float)
        self.den  = np.atleast_1d(den).astype(float)

    # ── Interconnections ──────────────────────────────────────
    def series(self, other):
        """H_eq = H1 * H2"""
        return System(np.polymul(self.num, other.num),
                      np.polymul(self.den, other.den),
                      f"{self.name}→{other.name}")

    def parallel(self, other):
        """H_eq = H1 + H2"""
        num = np.polyadd(np.polymul(self.num, other.den),
                         np.polymul(other.num, self.den))
        return System(num, np.polymul(self.den, other.den),
                      f"{self.name}‖{other.name}")

    def feedback(self, other=None, sign=-1):
        """H_eq = G / (1 ± G·H)"""
        if other is None:
            fb_num = self.num
            fn = np.polyadd if sign == -1 else np.polysub
            fb_den = fn(self.den, self.num)
            label = f"UF({self.name})"
        else:
            H1H2_num = np.polymul(self.num, other.num)
            H1H2_den = np.polymul(self.den, other.den)
            fb_num   = np.polymul(self.num, other.den)
            fn = np.polyadd if sign == -1 else np.polysub
            fb_den = fn(H1H2_den, H1H2_num)
            label  = f"FB({'neg' if sign==-1 else 'pos'})({self.name})"
        return System(fb_num, fb_den, label)

    # ── Responses ─────────────────────────────────────────────
    def bode(self, w):        return sig.bode(self.sys, w=w)
    def impulse_resp(self):   return sig.impulse(self.sys)
    def step_resp(self):      return sig.step(self.sys)
    def poles_zeros(self):    return np.roots(self.num), np.roots(self.den)


# ─────────────────────────────────────────────────────────────
# BLOCK-DIAGRAM DRAWING HELPERS
# ─────────────────────────────────────────────────────────────
def _arrow(ax, x1, y1, x2, y2, color):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

def _box(ax, cx, cy, label, color, w=1.5, h=0.58):
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.05",
        lw=1.8, edgecolor=color, facecolor=PANEL_BG))
    ax.text(cx, cy, label, ha="center", va="center",
            color=color, fontsize=7.5, fontweight="bold")

def _sumnode(ax, cx, cy, color, r=0.2):
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, color=color, lw=1.8))
    ax.text(cx, cy, "Σ", ha="center", va="center", color=color, fontsize=10)


def draw_series(ax):
    ax.set_xlim(0, 10); ax.set_ylim(-1.2, 1.2); ax.axis("off")
    ax.set_title("Series  H_eq = H₁ · H₂", color=A1, fontsize=9, fontweight="bold")
    c = A1
    ax.text(0.25, 0.18, "x(t)", color=TX, fontsize=8)
    _arrow(ax, 0.6,  0, 1.3, 0, c)
    _box(ax, 2.1, 0, "H₁(s)", c)
    _arrow(ax, 2.85, 0, 3.7, 0, c)
    ax.text(3.1, 0.18, "w(t)", color=TX, fontsize=8)
    _box(ax, 4.5, 0, "H₂(s)", c)
    _arrow(ax, 5.25, 0, 6.2, 0, c)
    ax.text(6.25, -0.05, "≡", color=A3, fontsize=14)
    _box(ax, 7.8, 0, "H_eq(s)\n=H₁·H₂", c, w=2.0)
    _arrow(ax, 8.8, 0, 9.5, 0, c)
    ax.text(9.55, -0.18, "y(t)", color=TX, fontsize=8)


def draw_parallel(ax):
    ax.set_xlim(0, 10); ax.set_ylim(-1.5, 1.5); ax.axis("off")
    ax.set_title("Parallel  H_eq = H₁ + H₂", color=A2, fontsize=9, fontweight="bold")
    c = A2
    ax.text(0.2, 0.18, "x(t)", color=TX, fontsize=8)
    _arrow(ax, 0.5, 0, 1.2, 0, c)
    ax.plot([1.2, 1.2], [-0.9, 0.9], color=c, lw=1.5, ls="--")
    _arrow(ax, 1.2,  0.9, 2.5,  0.9, c)
    _arrow(ax, 1.2, -0.9, 2.5, -0.9, c)
    _box(ax, 3.4,  0.9, "H₁(s)", c)
    _box(ax, 3.4, -0.9, "H₂(s)", c)
    _arrow(ax, 4.15,  0.9, 5.2,  0.9, c)
    _arrow(ax, 4.15, -0.9, 5.2, -0.9, c)
    _sumnode(ax, 5.45, 0, c)
    ax.plot([5.45, 5.45], [ 0.2,  0.9], color=c, lw=1.5)
    ax.plot([5.45, 5.45], [-0.2, -0.9], color=c, lw=1.5)
    _arrow(ax, 5.65, 0, 6.8, 0, c)
    _box(ax, 7.8, 0, "H_eq(s)\n=H₁+H₂", c, w=2.0)
    _arrow(ax, 8.8, 0, 9.5, 0, c)
    ax.text(9.55, -0.18, "y(t)", color=TX, fontsize=8)


def draw_feedback(ax):
    ax.set_xlim(0, 10); ax.set_ylim(-1.7, 1.2); ax.axis("off")
    ax.set_title("Feedback  H_eq = G / (1 + GH)", color=A3, fontsize=9, fontweight="bold")
    c = A3
    ax.text(0.1, 0.18, "r(t)", color=TX, fontsize=8)
    _arrow(ax, 0.5, 0, 1.1, 0, c)
    _sumnode(ax, 1.35, 0, c)
    _arrow(ax, 1.55, 0, 2.4, 0, c)
    ax.text(1.7, 0.18, "e(t)", color=TX, fontsize=8)
    _box(ax, 3.2, 0, "G(s)", c)
    _arrow(ax, 4.0, 0, 5.2, 0, c)
    _box(ax, 6.0, 0, "Plant", c)
    _arrow(ax, 6.75, 0, 9.5, 0, c)
    ax.text(9.55, -0.18, "y(t)", color=TX, fontsize=8)
    # feedback path
    ax.plot([8.3, 8.3, 1.35], [0, -1.2, -1.2], color=c, lw=1.6)
    _arrow(ax, 1.35, -1.2, 1.35, -0.2, c)
    _box(ax, 5.0, -1.2, "H(s)", c)
    ax.plot([6.5, 5.8], [-1.2, -1.2], color=c, lw=1.6)
    ax.plot([4.2, 1.35], [-1.2, -1.2], color=c, lw=1.6)
    ax.text(1.1,  0.38, "+", color=A2, fontsize=11)
    ax.text(1.1, -0.45, "–", color=A3, fontsize=11)


# ─────────────────────────────────────────────────────────────
# POLE-ZERO SUBPLOT HELPER
# ─────────────────────────────────────────────────────────────
def _pz_plot(ax, systems, colors, title):
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.axhline(0, color=GR, lw=1)
    ax.axvline(0, color=GR, lw=1)
    ax.set_title(title, color=A4, fontsize=8, fontweight="bold")
    ax.set_xlabel("σ  (Real)")
    ax.set_ylabel("jω  (Imag)")
    handles = []
    for sys_obj, col in zip(systems, colors):
        zeros, poles = sys_obj.poles_zeros()
        ax.scatter(poles.real, poles.imag, marker="x", s=90,
                   color=col, linewidths=2.2, zorder=5)
        ax.scatter(zeros.real, zeros.imag, marker="o", s=70,
                   facecolors="none", edgecolors=col, linewidths=2.2, zorder=5)
        handles += [
            Line2D([0],[0], color=col, marker="x", lw=0,
                   markersize=8, markeredgewidth=2,
                   label=f"{sys_obj.name} poles"),
            Line2D([0],[0], color=col, marker="o", lw=0, markersize=8,
                   markerfacecolor="none", markeredgewidth=2,
                   label=f"{sys_obj.name} zeros"),
        ]
    ax.legend(handles=handles, fontsize=6.5, loc="upper right")


# ─────────────────────────────────────────────────────────────
# MAIN — SINGLE FIGURE
# ─────────────────────────────────────────────────────────────
def run_simulation():

    # ── Define systems ────────────────────────────────────────
    H1 = System([1],    [1, 2],    name="H₁(LPF)")   # 1st-order LP
    H2 = System([1, 0], [1, 3, 9], name="H₂(BPF)")   # 2nd-order BP
    H3 = System([5],    [1],       name="K=5")         # gain block

    H_ser  = H1.series(H2)
    H_par  = H1.parallel(H2)
    H_fb_n = H1.feedback(H3, sign=-1)   # negative feedback
    H_fb_p = H1.feedback(H3, sign=+1)   # positive feedback
    H_fb_u = H2.feedback()              # unity negative feedback

    w = np.logspace(-2, 3, 800)

    # ── Build figure ──────────────────────────────────────────
    fig = plt.figure(figsize=(21, 14), facecolor=DARK_BG)
    fig.suptitle(
        "INTERCONNECTION OF SYSTEMS  ——  Signals & Systems Simulator",
        fontsize=15, color=A1, fontweight="bold", y=0.985
    )

    outer = gridspec.GridSpec(
        4, 1, figure=fig,
        height_ratios=[2.0, 2.6, 2.6, 1.1],
        hspace=0.55
    )

    # ── ROW 0 : Block Diagrams ────────────────────────────────
    bd = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[0], wspace=0.06)
    draw_series(   fig.add_subplot(bd[0]) )
    draw_parallel( fig.add_subplot(bd[1]) )
    draw_feedback( fig.add_subplot(bd[2]) )

    # ── ROW 1 : Bode + Impulse + Step (H1, H2, series, parallel) ──
    r1 = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=outer[1], wspace=0.40)
    ax_bm = fig.add_subplot(r1[0])
    ax_bp = fig.add_subplot(r1[1])
    ax_ir = fig.add_subplot(r1[2])
    ax_sr = fig.add_subplot(r1[3])

    r1_sys = [H1, H2, H_ser, H_par]
    r1_col = [A1, A2, A3, A4]

    for ax in [ax_bm, ax_bp, ax_ir, ax_sr]:
        ax.grid(True, which="both", linestyle="--", alpha=0.35)

    for s, c in zip(r1_sys, r1_col):
        wo, mag, ph = s.bode(w)
        ax_bm.semilogx(wo, mag, color=c, lw=1.8, label=s.name)
        ax_bp.semilogx(wo, ph,  color=c, lw=1.8, label=s.name)
        ti, yi = s.impulse_resp()
        ax_ir.plot(ti, yi, color=c, lw=1.8, label=s.name)
        ts, ys = s.step_resp()
        ax_sr.plot(ts, ys, color=c, lw=1.8, label=s.name)

    ax_bm.set_title("Bode — Magnitude", color=A1, fontsize=8, fontweight="bold")
    ax_bm.set_ylabel("Magnitude (dB)"); ax_bm.set_xlabel("ω (rad/s)")
    ax_bm.legend(fontsize=7, loc="lower left")

    ax_bp.set_title("Bode — Phase", color=A1, fontsize=8, fontweight="bold")
    ax_bp.set_ylabel("Phase (°)"); ax_bp.set_xlabel("ω (rad/s)")
    ax_bp.legend(fontsize=7, loc="lower left")

    ax_ir.set_title("Impulse Response  h(t)", color=A2, fontsize=8, fontweight="bold")
    ax_ir.set_xlabel("Time (s)"); ax_ir.set_ylabel("Amplitude")
    ax_ir.legend(fontsize=7)

    ax_sr.set_title("Step Response  y(t)", color=A2, fontsize=8, fontweight="bold")
    ax_sr.set_xlabel("Time (s)"); ax_sr.set_ylabel("Amplitude")
    ax_sr.legend(fontsize=7)

    # ── ROW 2 : Feedback Step + Pole-Zero Series + Pole-Zero FB ──
    r2 = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[2], wspace=0.40)
    ax_fbs = fig.add_subplot(r2[0])
    ax_pz1 = fig.add_subplot(r2[1])
    ax_pz2 = fig.add_subplot(r2[2])

    # Feedback step responses
    ax_fbs.grid(True, linestyle="--", alpha=0.35)
    fb_sys = [H1, H_fb_n, H_fb_p, H_fb_u]
    fb_col = [A1, A2, A3, A4]
    fb_lbl = ["H₁ open-loop", "Neg. FB (K=5)", "Pos. FB (K=5)", "Unity FB (H₂)"]
    for s, c, l in zip(fb_sys, fb_col, fb_lbl):
        try:
            ts, ys = s.step_resp()
            ax_fbs.plot(ts, ys, color=c, lw=1.8, label=l)
        except Exception:
            pass
    ax_fbs.set_title("Step Response — Feedback Configurations", color=A3,
                     fontsize=8, fontweight="bold")
    ax_fbs.set_xlabel("Time (s)"); ax_fbs.set_ylabel("Amplitude")
    ax_fbs.set_ylim(-0.5, 2.3)
    ax_fbs.legend(fontsize=7)

    _pz_plot(ax_pz1, [H1, H2, H_ser], [A1, A2, A3],
             "Pole-Zero Map — Series Interconnection")
    _pz_plot(ax_pz2, [H1, H_fb_n, H_fb_p], [A1, A2, A3],
             "Pole-Zero Map — Feedback Configurations")

    # ── ROW 3 : Key Observations ──────────────────────────────
    ax_txt = fig.add_subplot(outer[3])
    ax_txt.axis("off")

    notes = (
        "KEY OBSERVATIONS\n"
        "SERIES:    H_eq = H₁·H₂  │  poles = union  │  zeros = union  │  phase = sum of phases\n"
        "PARALLEL:  H_eq = H₁+H₂  │  common denominator  │  used in filter banks & redundancy\n"
        "NEG. FB:   H_eq = G/(1+GH)  →  reduced gain, wider BW, improved stability (poles → LHP)\n"
        "POS. FB:   H_eq = G/(1−GH)  →  possible instability (poles → RHP); used in oscillators"
    )
    ax_txt.text(
        0.01, 0.95, notes,
        transform=ax_txt.transAxes,
        color=TX, fontsize=8, va="top", ha="left",
        linespacing=1.7,
        bbox=dict(boxstyle="round,pad=0.55", facecolor=PANEL_BG,
                  edgecolor=GR, alpha=0.92)
    )

    items = [
        (A1, "H₁ — LPF  1/(s+2)"),
        (A2, "H₂ — BPF  s/(s²+3s+9)"),
        (A3, "Series H₁→H₂"),
        (A4, "Parallel H₁‖H₂"),
        (A5, "K=5  gain block"),
    ]
    xpos = 0.55
    for col, lbl in items:
        ax_txt.add_patch(plt.Rectangle(
            (xpos, 0.3), 0.013, 0.45,
            transform=ax_txt.transAxes,
            color=col, clip_on=False
        ))
        ax_txt.text(xpos + 0.016, 0.53, lbl,
                    transform=ax_txt.transAxes,
                    color=TX, fontsize=7.5, va="center")
        xpos += 0.09

    print("\033[1;92m\n  ✔  Single-window figure ready.\n  Close the window to exit.\033[0m\n")
    plt.show()


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_simulation()