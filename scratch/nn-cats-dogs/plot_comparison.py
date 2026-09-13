import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"      # slot 1: from-scratch, raw pixels, no convolution
ORANGE = "#eb6834"    # slot 2: pretrained CNN, zero training on this data
RED = "#e34948"

labels = ["Linear SVM\n(raw pixels)", "MLP\n(raw pixels)", "YOLO26n\n(pretrained CNN,\nzero-shot)"]
values = [46.7, 55.0, 91.7]
colors = [BLUE, BLUE, ORANGE]

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

fig, ax = plt.subplots(figsize=(7.5, 5.3), dpi=200, facecolor="#fcfcfb")
ax.set_facecolor("#fcfcfb")

x = range(len(labels))
bars = ax.bar(x, values, width=0.55, color=colors, zorder=3,
               edgecolor="#fcfcfb", linewidth=2)

ax.axhline(50, color=RED, linestyle=(0, (4, 3)), linewidth=1.4, zorder=1)
ax.set_xlim(-0.65, 2.65)
ax.text(-0.6, 51.5, "chance (50%)", color=RED, fontsize=9.5, va="bottom", ha="left")

for xi, v in zip(x, values):
    ax.annotate(f"{v:.1f}%", (xi, v), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=12, color=INK, fontweight="bold")

ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=10, color=INK)
ax.tick_params(axis="x", length=0, pad=10)

ax.set_ylim(0, 105)
ax.set_yticks(range(0, 101, 20))
ax.tick_params(axis="y", labelsize=9.5, colors=MUTED, length=0)

for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(BASELINE)

ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

ax.set_ylabel("Test accuracy, same 120 held-out photos (%)", fontsize=10.5, color=INK, labelpad=10)
ax.set_title("Same photos, three models: raw pixels vs. a pretrained CNN",
              fontsize=13, color=INK, pad=16, loc="left", fontweight="bold")

fig.tight_layout()
out_path = "/Users/bruceschultz/Documents/blog/169720747/static/images/comp-science/nn-cats-dogs-model-comparison.png"
fig.savefig(out_path, facecolor=fig.get_facecolor())
print("Saved:", out_path)
