"""Draws docs/images/lessons/coverage-map.png from the "Coverage by lesson" table in docs/lesson-plan.md.

Run: python3 docs/images/src/coverage_map.py   (needs matplotlib)
A benchmark segment ending in "(partly)" is drawn light, and one ending in "(not checked)" is drawn dashed.
"""
import os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "..", "..", "lesson-plan.md")
OUT = os.path.join(HERE, "..", "lessons", "coverage-map.png")
BENCH = ["Jump$tart", "SIFMA SMG", "investor.gov", "OIC", "FINRA SIE"]
DARK, LIGHT, EDGE, INK, MUTED, NEW = "#1d5fbf", "#b9d0f0", "#e1e1e1", "#141414", "#5a5a5a", "#b45014"

def rows():
    text = open(PLAN, encoding="utf-8").read()
    block = text[text.index("### Coverage by lesson"):text.index("### Gaps the check found")]
    new = set(re.findall(r"^### (\S+) .*\(new\)", text, flags=re.M))
    out = []
    for line in block.splitlines():
        m = re.match(r"\| ([\dI]\.\d+) \| (.+?) \| (.+) \|$", line)
        if not m: continue
        num, title, met = m.groups()
        cells = {}
        if met.strip() == "Not yet checked":
            cells = None
        else:
            for seg in met.split(" · "):
                for b in BENCH:
                    if seg.startswith(b):
                        end = seg.rstrip()
                        cells[b] = "unchecked" if end.endswith("(not checked)") else "partly" if end.endswith("(partly)") else "meets"
        out.append((num, title, cells, num in new))
    return out

def main():
    R = rows()
    W, row_h, top, bottom = 1624, 44, 184, 120
    H = top + row_h * len(R) + bottom
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    ax.text(32, 48, "Lesson coverage by benchmark", fontsize=26, fontweight="bold", color=INK, va="center")
    ax.text(32, 90, "Dark: meets  ·  Light: partly meets  ·  Blank: not covered  ·  Dashed: not yet checked  ·  New: added Nov 27 or 28",
            fontsize=15.5, color=MUTED, va="center")
    col_x = [640 + 192 * k for k in range(5)]
    for x, b in zip(col_x, BENCH):
        ax.text(x + 88, 157, b, fontsize=16, fontweight="bold", color=INK, ha="center", va="center")
    ax.plot([32, W - 32], [top, top], color="#787878", lw=1.5)
    prev = None
    for k, (num, title, cells, is_new) in enumerate(R):
        y = top + row_h * k
        group = num.split(".")[0]
        if prev is not None and group != prev:
            ax.plot([32, W - 32], [y, y], color="#787878", lw=1.5)
        prev = group
        label = f"{num}  {title}" + ("  (new)" if is_new else "")
        if len(label) > 44: label = label[:41].rstrip() + "…"
        ax.text(32, y + row_h / 2, label, fontsize=16.5, va="center",
                color=NEW if is_new else INK, fontweight="bold" if is_new else "normal")
        for x, b in zip(col_x, BENCH):
            if cells is None or cells.get(b) == "unchecked":
                ax.add_patch(Rectangle((x + 2, y + 7), 174, 30, facecolor="white", edgecolor="#9a9a9a", lw=1.4, ls=(0, (4, 3))))
            else:
                state = cells.get(b)
                ax.add_patch(Rectangle((x + 2, y + 7), 174, 30, lw=1.6, edgecolor=EDGE,
                                       facecolor=DARK if state == "meets" else LIGHT if state == "partly" else "white"))
    yb = top + row_h * len(R) + 44
    ax.text(32, yb, "Sources read Nov 27, 2026: Jump$tart 2021 Investing standards (grades 8 and 12), SIFMA Stock Market Game curriculum,",
            fontsize=14.5, color=MUTED, va="center")
    ax.text(32, yb + 32, "SEC investor.gov, Options Industry Council pages and courses, FINRA SIE content outline. Investing track checked Nov 28 (investor.gov pages found by hand).",
            fontsize=14.5, color=MUTED, va="center")
    fig.savefig(OUT, dpi=100, facecolor="white"); plt.close(fig)
    print("wrote", os.path.normpath(OUT), len(R), "rows")

if __name__ == "__main__":
    main()
