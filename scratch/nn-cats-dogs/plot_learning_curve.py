import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, "learning_curve_results.json")) as f:
    results = json.load(f)

sizes = [r["n_train"] for r in results]
accs = [r["test_accuracy"] * 100 for r in results]

INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"
RED = "#e34948"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

fig, ax = plt.subplots(figsize=(7.5, 5), dpi=200, facecolor="#fcfcfb")
ax.set_facecolor("#fcfcfb")

ax.axhline(50, color=RED, linestyle=(0, (4, 3)), linewidth=1.4, zorder=1)
ax.text(sizes[-1], 50.8, "chance (50%)", color=RED, fontsize=9.5, va="bottom", ha="right")

ax.plot(sizes, accs, color=BLUE, linewidth=2.2, marker="o",
        markersize=7, markerfacecolor=BLUE, markeredgecolor="#fcfcfb",
        markeredgewidth=1.5, zorder=3)

for x, y in zip(sizes, accs):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                xytext=(0, 11), ha="center", fontsize=9.5, color=INK)

ax.set_xscale("log")
ax.xaxis.set_minor_locator(mticker.NullLocator())
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
ax.set_xticks(sizes)
ax.set_xticklabels([f"{s:,}" for s in sizes], fontsize=9.5, color=MUTED)

ax.set_ylim(35, 68)
ax.set_yticks(range(40, 70, 10))
ax.tick_params(axis="y", labelsize=9.5, colors=MUTED, length=0)
ax.tick_params(axis="x", length=0)

for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(BASELINE)

ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

ax.set_xlabel("Training images (log scale)", fontsize=10.5, color=INK, labelpad=10)
ax.set_ylabel("Test accuracy on the same 120 held-out photos (%)", fontsize=10.5, color=INK, labelpad=10)
ax.set_title("More real photos, same flatten-pixels MLP — does it help?",
              fontsize=13, color=INK, pad=16, loc="left", fontweight="bold")

fig.tight_layout()
out_path = "/Users/bruceschultz/Documents/blog/169720747/static/images/comp-science/nn-cats-dogs-learning-curve.png"
fig.savefig(out_path, facecolor=fig.get_facecolor())
print("Saved:", out_path)
