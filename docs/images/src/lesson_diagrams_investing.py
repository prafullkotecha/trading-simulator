"""Draws the six investing-track lesson diagrams (I.1 to I.6) as 640x340 PNGs.

Run from anywhere: python3 docs/images/src/lesson_diagrams_investing.py
Needs matplotlib. Numbers are worked examples, as the lesson plan's notes say.
Colors are the US pack's: blue for gain, orange for loss.
"""
import math, os, random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lessons")
BLUE, ORANGE = "#1f62c9", "#c2510c"
BLUE_SOFT, ORANGE_SOFT = "#dfe9f7", "#f7e6db"
INK, MUTED, GRID = "#111827", "#4b5563", "#e3e8ef"
MONO = "DejaVu Sans Mono"

def new_fig():
    fig = plt.figure(figsize=(6.4, 3.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 640); ax.set_ylim(340, 0); ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=100, facecolor="white")
    plt.close(fig)

def text(ax, x, y, s, color=MUTED, size=15, weight="normal", ha="left", va="center", family=MONO):
    ax.text(x, y, s, color=color, fontsize=size, fontweight=weight, ha=ha, va=va, family=family)

def title(ax, s):
    ax.text(60, 22, s, color=INK, fontsize=15.5, fontweight="bold", ha="left", va="center", family="DejaVu Sans")

def bar(ax, x, y0, y1, w, color):
    top, bottom = min(y0, y1), max(y0, y1)
    if bottom - top < 1: return
    ax.add_patch(FancyBboxPatch((x, top), w, bottom - top, boxstyle="round,pad=0,rounding_size=4",
                                linewidth=0, facecolor=color))

# I.1 Goals and time horizon: the range of yearly results narrows with time held
def i1():
    fig, ax = new_fig()
    title(ax, "Best and worst yearly result, by years held")
    data = [("1 year", 47, -39), ("5 years", 28, -3), ("10 years", 19, -1), ("20 years", 17, 6)]
    zero, scale = 188, 2.25         # y of 0%, pixels per percentage point
    ax.plot([60, 620], [zero, zero], color=GRID, lw=1.5)
    text(ax, 52, zero, "0%", ha="right")
    for k, (lab, hi, lo) in enumerate(data):
        x = 95 + k * 135
        if lo < 0:
            bar(ax, x, zero + 1, zero - lo * scale, 70, ORANGE)
            bar(ax, x, zero - 1, zero - hi * scale, 70, BLUE)
        else:
            bar(ax, x, zero - lo * scale, zero - hi * scale, 70, BLUE)
        text(ax, x + 35, zero - hi * scale - 13, f"+{hi}%", color=BLUE, weight="bold", ha="center")
        lo_y = zero - lo * scale + 14 if lo < 0 else zero + 14
        text(ax, x + 35, lo_y, (f"−{-lo}%" if lo < 0 else f"+{lo}%"),
             color=ORANGE if lo < 0 else BLUE, weight="bold", ha="center")
        text(ax, x + 35, 326, lab, color=INK, ha="center", weight="bold", size=13.5)
    save(fig, "lesson-I-1.png")

# I.2 Bonds and cash: price of a 10-year 4% bond as rates move
def bond_price(rate, coupon=40.0, years=10, face=1000.0):
    return sum(coupon / (1 + rate) ** t for t in range(1, years + 1)) + face / (1 + rate) ** years

def i2():
    fig, ax = new_fig()
    title(ax, "A 10-year bond paying 4%, as rates move")
    x0, x1, ytop, ybot = 110, 600, 60, 270
    pmin, pmax = 700, 1300
    X = lambda r: x0 + (r - 0.01) / 0.07 * (x1 - x0)
    Y = lambda p: ybot - (p - pmin) / (pmax - pmin) * (ybot - ytop)
    for p in (800, 1000, 1200):
        ax.plot([x0, x1], [Y(p), Y(p)], color=GRID, lw=1.5)
        text(ax, x0 - 8, Y(p), f"${p:,}", ha="right")
    rs = [0.01 + i * 0.0005 for i in range(141)]
    ax.plot([X(r) for r in rs], [Y(bond_price(r)) for r in rs], color=INK, lw=3, solid_capstyle="round")
    for r, col, dx, dy, ha in ((0.04, INK, 12, -14, "left"), (0.06, ORANGE, 12, -12, "left"), (0.02, BLUE, 14, 0, "left")):
        p = bond_price(r)
        ax.plot([X(r)], [Y(p)], "o", ms=10, color=col, mec="white", mew=2, zorder=5)
        text(ax, X(r) + dx, Y(p) + dy, f"${p:,.0f}", color=col, weight="bold", ha=ha)
    for r in (0.02, 0.04, 0.06, 0.08):
        text(ax, X(r), 292, f"{int(r * 100)}%", ha="center")
    text(ax, x1, 322, "interest rate →", ha="right")
    save(fig, "lesson-I-2.png")

# shared synthetic paths (seeded, so the pictures never change)
def crash_path(n=380, seed=8):
    rnd = random.Random(seed); p = [100.0]
    for t in range(1, n):
        if t < 60: mu, vol = 0.0004, 0.008
        elif t < 250: mu, vol = -0.0038, 0.022
        else: mu, vol = 0.0030, 0.014
        p.append(p[-1] * math.exp(mu + vol * rnd.gauss(0, 1)))
    return p

def max_drawdown(v):
    peak, dd = v[0], 0.0
    for x in v:
        peak = max(peak, x); dd = min(dd, x / peak - 1)
    return dd

# I.3 Asset allocation: three splits through one crash
def i3():
    fig, ax = new_fig()
    title(ax, "Three splits through one crash")
    stock = crash_path(); n = len(stock)
    bond = [100 * math.exp(0.00022 * t) for t in range(n)]
    def mix(w):
        v = [100.0]
        for t in range(1, n):
            v.append(v[-1] * (w * stock[t] / stock[t - 1] + (1 - w) * bond[t] / bond[t - 1]))
        return v
    series = [("all stocks", mix(1.0), INK, "-", 3), ("60/40", mix(0.6), BLUE, "-", 3), ("20/80", mix(0.2), MUTED, (0, (5, 3)), 2.2)]
    x0, x1, ytop, ybot = 60, 440, 50, 292
    lo = min(min(v) for _, v, *_ in series) - 4; hi = max(max(v) for _, v, *_ in series) + 3
    X = lambda t: x0 + t / (n - 1) * (x1 - x0)
    Y = lambda v: ybot - (v - lo) / (hi - lo) * (ybot - ytop)
    ax.plot([x0, x1], [Y(100), Y(100)], color=GRID, lw=1.5)
    text(ax, x0, 318, "each starts at $10,000", size=12.5)
    ends = []
    for name, v, col, ls, lw in series:
        ax.plot([X(t) for t in range(n)], [Y(x) for x in v], color=col, lw=lw - 0.5, ls=ls, solid_capstyle="round")
        ends.append([Y(v[-1]), name, max_drawdown(v), col])
    ends.sort()
    for k in range(1, len(ends)):               # keep the end labels 44 px apart
        ends[k][0] = max(ends[k][0], ends[k - 1][0] + 44)
    for y, name, dd, col in ends:
        text(ax, x1 + 12, y - 9, name, color=col if col != MUTED else INK, weight="bold")
        text(ax, x1 + 12, y + 11, f"worst drop −{-dd * 100:.0f}%", color=ORANGE, size=12.5)
    save(fig, "lesson-I-3.png")

# I.4 Investing a little every month: fixed dollars buy more shares when the price is low
def i4():
    fig, ax = new_fig()
    title(ax, "$100 a month for a year")
    prices = [50, 44, 37, 30, 25, 22, 25, 30, 37, 44, 50, 54]
    shares = sum(100 / p for p in prices)
    avg_cost = 100 * len(prices) / shares
    avg_price = sum(prices) / len(prices)
    x0, x1, ytop, ybot = 70, 445, 62, 285
    X = lambda m: x0 + m / 11 * (x1 - x0)
    Y = lambda p: ybot - (p - 18) / (58 - 18) * (ybot - ytop)
    ax.plot([X(m) for m in range(12)], [Y(p) for p in prices], color=INK, lw=3, solid_capstyle="round")
    for m, p in enumerate(prices):
        ax.plot([X(m)], [Y(p)], "o", ms=9, color=INK, mec="white", mew=2, zorder=5)
    ax.plot([x0, x1 + 10], [Y(avg_price), Y(avg_price)], color=MUTED, lw=1.8, ls=(0, (5, 3)))
    ax.plot([x0, x1 + 10], [Y(avg_cost), Y(avg_cost)], color=BLUE, lw=2.2, ls=(0, (5, 3)))
    text(ax, x1 + 18, Y(avg_price) - 30, f"${avg_price:.2f}", color=INK, weight="bold")
    text(ax, x1 + 18, Y(avg_price) - 11, "average price", size=12.5)
    text(ax, x1 + 18, Y(avg_cost) + 12, f"${avg_cost:.2f}", color=BLUE, weight="bold")
    text(ax, x1 + 18, Y(avg_cost) + 31, "what you paid", color=BLUE, size=12.5)
    text(ax, X(5), Y(22) + 22, "more shares here", size=12.5, ha="center")
    text(ax, x0, 318, "month 1", size=13); text(ax, x1, 318, "month 12", size=13, ha="right")
    save(fig, "lesson-I-4.png")

# I.5 Rebalancing: a 60/40 account drifts to 75/25, then is reset
def i5():
    fig, ax = new_fig()
    title(ax, "A 60/40 plan drifts, then is reset")
    cols = [("Start", 60), ("After a rally", 75), ("Rebalanced", 60)]
    ybot, h = 288, 216
    for k, (lab, s) in enumerate(cols):
        x = 75 + k * 185
        ys = ybot - h * s / 100
        bar(ax, x, ybot, ys + 1, 120, BLUE)                       # stocks
        bar(ax, x, ys - 1, ybot - h, 120, "#c9d3e0")              # bonds
        text(ax, x + 60, (ybot + ys) / 2, f"stocks {s}%", color="white", weight="bold", ha="center", size=13)
        text(ax, x + 60, (ys + ybot - h) / 2, f"bonds {100 - s}%", color=INK, weight="bold", ha="center", size=13)
        text(ax, x + 60, 312, lab, color=INK, weight="bold", ha="center", size=13.5)
        if k < 2:
            ax.annotate("", xy=(x + 178, 178), xytext=(x + 128, 178),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.8))
    text(ax, 75 + 120 + 32, 52, "stocks rise", size=11.5, ha="center")
    text(ax, 75 + 185 + 120 + 32, 52, "sell stocks, buy bonds", size=11.5, ha="center")
    save(fig, "lesson-I-5.png")

# I.6 Time in the market: twenty years with and without the ten best days
def i6():
    fig, ax = new_fig()
    title(ax, "$10,000 over 20 years")
    rnd = random.Random(190); days = 252 * 20; r = []; stress = 0
    for t in range(days):
        if stress == 0 and rnd.random() < 0.0016: stress = 45      # a stormy stretch
        vol = 0.034 if stress else 0.0075
        stress = max(0, stress - 1)
        r.append(vol * rnd.gauss(0, 1))
    shift = (math.log(6.4) - sum(r)) / days                       # end near $64,000
    r = [x + shift for x in r]
    best = set(sorted(range(days), key=lambda t: r[t])[-10:])
    full, miss = [10000.0], [10000.0]
    for t in range(days):
        full.append(full[-1] * math.exp(r[t]))
        miss.append(miss[-1] * (1.0 if t in best else math.exp(r[t])))
    x0, x1, ytop, ybot = 60, 410, 60, 290
    top = max(full) * 1.04
    X = lambda t: x0 + t / days * (x1 - x0)
    Y = lambda v: ybot - v / top * (ybot - ytop)
    step = 12
    ax.plot([x0, x1], [Y(10000), Y(10000)], color=GRID, lw=1.5)
    ax.plot([X(t) for t in range(0, days + 1, step)], [Y(full[t]) for t in range(0, days + 1, step)], color=BLUE, lw=2.6)
    ax.plot([X(t) for t in range(0, days + 1, step)], [Y(miss[t]) for t in range(0, days + 1, step)], color=ORANGE, lw=2.6)
    yf, ym = Y(full[-1]), Y(miss[-1])
    if ym - yf < 46: ym = yf + 46
    text(ax, x1 + 12, yf - 9, f"${full[-1]:,.0f}", color=BLUE, weight="bold")
    text(ax, x1 + 12, yf + 11, "stayed invested", color=BLUE, size=11.5)
    text(ax, x1 + 12, ym - 9, f"${miss[-1]:,.0f}", color=ORANGE, weight="bold")
    text(ax, x1 + 12, ym + 11, "missed 10 best days", color=ORANGE, size=11.5)
    text(ax, x0, 318, "year 0", size=13); text(ax, x1, 318, "year 20", size=13, ha="right")
    save(fig, "lesson-I-6.png")

if __name__ == "__main__":
    for f in (i1, i2, i3, i4, i5, i6):
        f()
    print("wrote 6 diagrams to", os.path.normpath(OUT))
