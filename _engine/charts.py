#!/usr/bin/env python3
"""charts.py -- palette-driven matplotlib figures for kr-brand-decks.

Every color comes from the palette dict passed in, so each company's charts are
automatically on-brand. Self-contained: no repo paths, no hardcoded interpreter,
KR font auto-detected across platforms (falls back gracefully).

Only used by the optional chart slides (kpi / roadmap). If matplotlib or a KR font
is unavailable, the caller degrades to a text slide.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm


def _kr_font():
    cands = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        os.path.expanduser("~/Library/Fonts/Pretendard-Regular.otf"),
        os.path.expanduser("~/.fonts/Pretendard-Regular.otf"),
        os.path.expanduser("~/.fonts/Pretendard-Bold.otf"),
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/pretendard/Pretendard-Regular.otf",
    ]
    for p in cands:
        if os.path.exists(p):
            try:
                fm.fontManager.addfont(p)
                return fm.FontProperties(fname=p).get_name()
            except Exception:
                pass
    return None


_KR = _kr_font()
if _KR:
    plt.rcParams["font.family"] = _KR
plt.rcParams["axes.unicode_minus"] = False


def _c(h):
    """Normalize a hex string to matplotlib form (leading #)."""
    h = str(h).strip()
    return h if h.startswith("#") else "#" + h


def kpi_bars(metrics, out, ink="#1A1A1A", sub="#555555", muted="#9A9AA0",
             accent="#1428A0", line="#E6E8EC"):
    """metrics: list of (title, cur_label, tgt_label, cur_val, tgt_val)."""
    ink, sub, muted, accent, line = map(_c, (ink, sub, muted, accent, line))
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(2.9 * n, 3.35), dpi=200)
    if n == 1:
        axes = [axes]
    fig.patch.set_facecolor("white")
    for ax, (title, blab, alab, bv, av) in zip(axes, metrics):
        ax.set_facecolor("white")
        ax.bar([0], [bv], width=0.56, color=muted, zorder=3)
        ax.bar([1], [av], width=0.56, color=accent, zorder=3)
        top = max(bv, av) or 1
        ax.text(0, bv + top * 0.04, blab, ha="center", color=sub, fontsize=10)
        ax.text(1, av + top * 0.04, alab, ha="center", color=accent,
                fontsize=11.5, fontweight="bold")
        ax.set_xticks([0, 1]); ax.set_xticklabels(["현재", "목표"], color=sub, fontsize=10)
        ax.set_yticks([]); ax.set_ylim(0, top * 1.3)
        ax.set_title(title, color=ink, fontsize=12, fontweight="bold", pad=10)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(line); ax.tick_params(length=0)
    fig.tight_layout(pad=1.0)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def roadmap(phases, out, ink="#1A1A1A", sub="#555555", muted="#9A9AA0",
            accent="#1428A0", line="#E6E8EC", panel="#F5F6F8"):
    """phases: list of (label, start, end). Simple on-brand gantt band chart."""
    ink, sub, muted, accent, line, panel = map(_c, (ink, sub, muted, accent, line, panel))
    n = len(phases)
    fig, ax = plt.subplots(figsize=(11.4, 4.4), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    lo = min(p[1] for p in phases); hi = max(p[2] for p in phases)
    for i, (label, s, e) in enumerate(phases):
        y = n - 1 - i
        ax.text(s, y + 0.30, label, va="bottom", ha="left", color=ink,
                fontsize=11.5, fontweight="bold", zorder=4)
        ax.barh(y, e - s, left=s, height=0.34, color=accent, edgecolor="none", zorder=3)
    ax.set_xlim(lo - (hi - lo) * 0.02, hi + (hi - lo) * 0.02)
    ax.set_ylim(-0.6, n + 0.05); ax.set_yticks([])
    xt = sorted({int(round(v)) for _, s, e in phases for v in (s, e)})
    ax.set_xticks(xt); ax.set_xticklabels([str(t) for t in xt], color=sub, fontsize=11)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(line); ax.tick_params(length=0)
    ax.grid(axis="x", color=line, linewidth=0.8, zorder=1)
    fig.tight_layout(pad=0.4)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def trend_dual(labels, revenue, op, out, ink="#1A1A1A", sub="#555555", muted="#9A9AA0",
               accent="#1428A0", line="#E6E8EC", rev_name="매출", op_name="영업이익",
               unit="조원"):
    """Revenue bars (left axis) + operating-profit line (right axis) over periods.
    The classic quarterly revenue/profit chart. Values in `unit`."""
    ink, sub, muted, accent, line = map(_c, (ink, sub, muted, accent, line))
    import numpy as np
    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(11.4, 4.5), dpi=200)
    fig.patch.set_facecolor("white"); ax1.set_facecolor("white")
    bars = ax1.bar(x, revenue, width=0.52, color=accent, zorder=3, label=rev_name)
    rmax = max(revenue) or 1
    for xi, v in zip(x, revenue):
        ax1.text(xi, v + rmax * 0.03, f"{v:g}", ha="center", color=ink, fontsize=10.5,
                 fontweight="bold")
    ax1.set_ylim(0, rmax * 1.25)
    ax2 = ax1.twinx()
    ax2.plot(x, op, color=ink, marker="o", markersize=6, linewidth=2.2, zorder=4, label=op_name)
    omax = max(op) or 1
    omin = min(op)
    for xi, v in zip(x, op):
        ax2.text(xi, v + (omax - omin + 1) * 0.06, f"{v:g}", ha="center", color=ink,
                 fontsize=10, fontweight="bold")
    ax2.set_ylim(min(0, omin) * 1.2 if omin < 0 else 0, omax * 1.4)
    ax1.set_xticks(x); ax1.set_xticklabels(labels, color=sub, fontsize=11)
    ax1.set_yticks([]); ax2.set_yticks([])
    for ax in (ax1, ax2):
        for sp in ("top", "left", "right"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(line); ax.tick_params(length=0)
    ax1.legend(loc="upper left", frameon=False, fontsize=10.5,
               labelcolor=sub, bbox_to_anchor=(0.0, 1.08))
    ax2.legend(loc="upper left", frameon=False, fontsize=10.5,
               labelcolor=sub, bbox_to_anchor=(0.16, 1.08))
    ax1.text(1.0, -0.16, f"단위: {unit}", transform=ax1.transAxes, ha="right",
             color=muted, fontsize=9)
    fig.tight_layout(pad=0.6)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def hbars(labels, values, out, ink="#1A1A1A", sub="#555555", muted="#9A9AA0",
          accent="#1428A0", line="#E6E8EC", unit="조원"):
    """Horizontal bars for a segment / breakdown (e.g. operating profit by division)."""
    ink, sub, muted, accent, line = map(_c, (ink, sub, muted, accent, line))
    import numpy as np
    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(11.2, 4.2), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    vmax = max(abs(v) for v in values) or 1
    ax.barh(y, values, height=0.55, color=accent, zorder=3)
    for yi, lab, v in zip(y, labels, values):
        ax.text(-vmax * 0.02, yi, lab, ha="right", va="center", color=ink, fontsize=12,
                fontweight="bold")
        ax.text(v + (vmax * 0.02 if v >= 0 else -vmax * 0.02), yi, f"{v:g}",
                ha="left" if v >= 0 else "right", va="center", color=ink,
                fontsize=11.5, fontweight="bold")
    ax.set_xlim(min(0, min(values)) * 1.15, vmax * 1.22)
    ax.set_yticks([]); ax.set_xticks([])
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.axvline(0, color=line, lw=1)
    ax.text(1.0, -0.08, f"단위: {unit}", transform=ax.transAxes, ha="right",
            color=muted, fontsize=9)
    fig.tight_layout(pad=0.6)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def comparison_table(headers, rows, out, ink="#1A1A1A", sub="#555555", muted="#9A9AA0",
                     accent="#1428A0", line="#E6E8EC", panel="#F5F6F8"):
    """headers: [col0, col1, col2]. rows: [[c0, c1, c2], ...]. Up to 3 columns.
    First column bold ink; middle column sub-gray; last column ink (the 'to-be')."""
    ink, sub, muted, accent, line, panel = map(_c, (ink, sub, muted, accent, line, panel))
    ncol = len(headers)
    xs = [0.015, 0.20, 0.60][:ncol] if ncol == 3 else [0.015, 0.52][:ncol]
    fig, ax = plt.subplots(figsize=(11.6, 5.0), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white"); ax.axis("off")
    y0 = 0.93
    for x, h in zip(xs, headers):
        ax.text(x, y0, h, ha="left", va="center", color=ink, fontsize=13.5,
                fontweight="bold", transform=ax.transAxes)
    ax.plot([0.008, 0.992], [y0 - 0.055, y0 - 0.055], color=accent, lw=2.2,
            transform=ax.transAxes)
    n = len(rows)
    rh = (y0 - 0.10) / n
    for i, row in enumerate(rows):
        yc = y0 - 0.10 - (i + 0.5) * rh
        cols = [ink, sub, ink]
        weights = ["bold", "normal", "normal"]
        for j, cell in enumerate(row):
            ax.text(xs[j], yc, cell, ha="left", va="center",
                    color=cols[j] if j < 3 else sub, fontsize=11,
                    fontweight=weights[j] if j < 3 else "normal",
                    transform=ax.transAxes, linespacing=1.45)
        yl = y0 - 0.10 - (i + 1) * rh
        ax.plot([0.008, 0.992], [yl, yl], color=line, lw=0.9, transform=ax.transAxes)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    plt.close(fig)
