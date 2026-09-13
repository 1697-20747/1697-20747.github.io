import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT_DIR = "/Users/bruceschultz/Documents/blog/169720747/static/images/comp-science"

INK = "#0b0b0b"
MUTED = "#898781"
GRID_C = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
RED = "#e34948"
GOOD = "#0ca30c"
BG = "#fcfcfb"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


# ---------- 1. Sample dataset grid ----------
def sample_dataset_grid():
    rng_cats = sorted(os.listdir(os.path.join(HERE, "data/train/cats")))[:4]
    rng_dogs = sorted(os.listdir(os.path.join(HERE, "data/train/dogs")))[:4]
    thumb = 140
    gap = 6
    cols = 4
    label_h = 34
    pad = 24
    panel_w = cols * thumb + (cols - 1) * gap
    canvas_w = pad * 2 + panel_w
    canvas_h = pad * 2 + label_h * 2 + thumb * 2 + gap
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw = ImageDraw.Draw(canvas)

    def row(files, folder, y, label, color):
        draw.text((pad, y), label, font=font([ARIAL_BOLD], 20), fill=INK)
        draw.rectangle([pad, y + 26, pad + 40, y + 30], fill=color)
        for i, fname in enumerate(files):
            img = Image.open(os.path.join(HERE, folder, fname)).convert("RGB")
            img = img.resize((thumb, thumb), Image.NEAREST)
            canvas.paste(img, (pad + i * (thumb + gap), y + label_h))

    row(rng_cats, "data/train/cats", pad, "Cats", BLUE)
    row(rng_dogs, "data/train/dogs", pad + label_h + thumb + gap, "Dogs", ORANGE)
    canvas.save(os.path.join(OUT_DIR, "nn-cats-dogs-sample-dataset.png"))
    print("Saved sample-dataset")


# ---------- 2. Confusion matrix heatmap ----------
def confusion_matrix_plot():
    cm = np.load(os.path.join(HERE, "confusion_matrix.npy"))
    labels = ["cat", "dog"]
    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=200, facecolor=BG)
    ax.set_facecolor(BG)
    vmax = cm.max()
    im = ax.imshow(cm, cmap=plt.cm.Blues, vmin=0, vmax=vmax * 1.15)

    for i in range(2):
        for j in range(2):
            val = cm[i, j]
            frac = val / vmax
            txt_color = "white" if frac > 0.55 else INK
            ax.text(j, i, f"{val}", ha="center", va="center",
                    fontsize=26, fontweight="bold", color=txt_color)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=12, color=INK)
    ax.set_yticklabels(labels, fontsize=12, color=INK)
    ax.set_xlabel("Predicted", fontsize=11, color=INK, labelpad=10)
    ax.set_ylabel("Actual", fontsize=11, color=INK, labelpad=10)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Confusion matrix, 120 held-out test images",
                  fontsize=12.5, color=INK, pad=14, loc="left", fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "nn-cats-dogs-confusion-matrix.png"), facecolor=BG)
    print("Saved confusion-matrix")


# ---------- 3. Loss curve ----------
def loss_curve_plot():
    loss = np.load(os.path.join(HERE, "loss_curve.npy"))
    val = None
    val_path = os.path.join(HERE, "val_curve.npy")
    if os.path.exists(val_path):
        val = np.load(val_path)
    epochs = np.arange(1, len(loss) + 1)

    fig, ax1 = plt.subplots(figsize=(7.2, 4.8), dpi=200, facecolor=BG)
    ax1.set_facecolor(BG)
    ax1.plot(epochs, loss, color=BLUE, linewidth=2.2, marker="o", markersize=5,
              markerfacecolor=BLUE, markeredgecolor=BG, markeredgewidth=1, zorder=3)
    ax1.set_yscale("log")
    ax1.set_xlabel("Epoch", fontsize=10.5, color=INK, labelpad=8)
    ax1.set_ylabel("Training loss (log scale)", fontsize=10.5, color=BLUE, labelpad=8)
    ax1.tick_params(axis="y", labelcolor=BLUE, labelsize=9.5)
    ax1.tick_params(axis="x", labelsize=9.5, colors=MUTED)
    ax1.grid(axis="y", color=GRID_C, linewidth=0.8, zorder=0)
    ax1.set_axisbelow(True)
    for spine in ("top", "right"):
        ax1.spines[spine].set_visible(False)
    ax1.spines["left"].set_color(BASELINE)
    ax1.spines["bottom"].set_color(BASELINE)

    if val is not None:
        ax2 = ax1.twinx()
        ax2.plot(epochs, val * 100, color=ORANGE, linewidth=1.8, linestyle="--",
                  marker="s", markersize=4, zorder=2)
        ax2.set_ylabel("Validation accuracy (%)", fontsize=10.5, color=ORANGE, labelpad=8)
        ax2.tick_params(axis="y", labelcolor=ORANGE, labelsize=9.5)
        ax2.set_ylim(85, 102)
        for spine in ("top", "left"):
            ax2.spines[spine].set_visible(False)
        ax2.spines["right"].set_color(BASELINE)

    ax1.set_title("Training loss falling over 17 epochs (early stopping)",
                   fontsize=12.5, color=INK, pad=14, loc="left", fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "nn-cats-dogs-loss-curve.png"), facecolor=BG)
    print("Saved loss-curve")


# ---------- 4. Sample predictions grid ----------
def sample_predictions_grid():
    with open(os.path.join(HERE, "sample_predictions.json")) as f:
        samples = json.load(f)
    thumb = 160
    gap = 14
    cols = 4
    rows = 2
    label_h = 40
    pad = 24
    panel_w = cols * thumb + (cols - 1) * gap
    panel_h = rows * (thumb + label_h) + (rows - 1) * gap
    canvas_w = pad * 2 + panel_w
    canvas_h = pad * 2 + 50 + panel_h
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((pad, pad), "Eight held-out test images, real predictions", font=font([ARIAL_BOLD], 20), fill=INK)

    top = pad + 50
    for i, s in enumerate(samples):
        r, c = divmod(i, cols)
        x = pad + c * (thumb + gap)
        y = top + r * (thumb + label_h + gap)
        correct = s["true"] == s["pred"]
        border = GOOD if correct else RED
        img = Image.open(s["path"]).convert("RGB").resize((thumb, thumb), Image.NEAREST)
        framed = Image.new("RGB", (thumb + 8, thumb + 8), border)
        framed.paste(img, (4, 4))
        canvas.paste(framed, (x - 4, y - 4))
        label = f"true: {s['true']}  pred: {s['pred']}"
        lcolor = INK if correct else RED
        draw.text((x, y + thumb + 8), label, font=font([ARIAL], 15), fill=lcolor)

    canvas.save(os.path.join(OUT_DIR, "nn-cats-dogs-sample-predictions.png"))
    print("Saved sample-predictions")


# ---------- 5. Network architecture diagram ----------
def network_diagram():
    W, H = 1500, 780
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = font([ARIAL_BOLD], 24)
    label_font = font([ARIAL_BOLD], 16)
    small_font = font([ARIAL], 13)

    draw.text((30, 24), "One image's forward pass through the network", font=title_font, fill=INK)

    # Sample input image, downsampled to 8x8 preview
    cat_path = sorted(os.listdir(os.path.join(HERE, "data/test/cats")))[0]
    img = Image.open(os.path.join(HERE, "data/test/cats", cat_path)).convert("RGB")
    preview = img.resize((8, 8), Image.LANCZOS).resize((176, 176), Image.NEAREST)
    img_x, img_y = 40, 260
    canvas.paste(preview, (img_x, img_y))
    draw.rectangle([img_x, img_y, img_x + 176, img_y + 176], outline=INK, width=2)
    draw.text((img_x, img_y + 186), "input image", font=small_font, fill=MUTED)
    draw.text((img_x, img_y + 206), "(8x8 preview of 48x48)", font=small_font, fill=MUTED)

    layers = [
        {"x": 330, "n": 10, "shown": 10, "label": "input layer", "sub": "6,912 pixel values", "color": INK},
        {"x": 640, "n": 128, "shown": 9, "label": "hidden layer 1", "sub": "128 neurons, ReLU", "color": BLUE},
        {"x": 950, "n": 64, "shown": 7, "label": "hidden layer 2", "sub": "64 neurons, ReLU", "color": BLUE},
        {"x": 1280, "n": 2, "shown": 2, "label": "output layer", "sub": "P(cat), P(dog)", "color": ORANGE},
    ]

    node_r = 9
    top_margin, bottom_margin = 145, 700
    span = bottom_margin - top_margin

    def node_positions(shown):
        if shown == 1:
            return [(top_margin + bottom_margin) // 2]
        return [int(top_margin + span * i / (shown - 1)) for i in range(shown)]

    layer_nodes = []
    for layer in layers:
        ys = node_positions(layer["shown"])
        layer_nodes.append(ys)

    # connections (drawn faint, behind nodes)
    for li in range(len(layers) - 1):
        x0, x1 = layers[li]["x"], layers[li + 1]["x"]
        for y0 in layer_nodes[li]:
            for y1 in layer_nodes[li + 1]:
                draw.line([(x0, y0), (x1, y1)], fill=(225, 224, 217), width=1)

    for li, layer in enumerate(layers):
        x = layer["x"]
        ys = layer_nodes[li]
        for y in ys:
            draw.ellipse([x - node_r, y - node_r, x + node_r, y + node_r],
                         fill="white", outline=layer["color"], width=2)
        if layer["n"] > layer["shown"]:
            draw.text((x - 8, ys[-1] + 22), "...", font=font([ARIAL_BOLD], 22), fill=MUTED)
        draw.text((x - 55, top_margin - 55), layer["label"], font=label_font, fill=INK)
        draw.text((x - 55, top_margin - 32), layer["sub"], font=small_font, fill=MUTED)

    # output labels
    out_x = layers[-1]["x"]
    out_ys = layer_nodes[-1]
    draw.text((out_x + 24, out_ys[0] - 10), "P(cat)", font=label_font, fill=ORANGE)
    draw.text((out_x + 24, out_ys[1] - 10), "P(dog)", font=label_font, fill=ORANGE)

    # arrow from image to input layer
    draw.line([(img_x + 176 + 10, img_y + 88), (layers[0]["x"] - 20, (top_margin + bottom_margin) // 2)],
               fill=INK, width=2)
    draw.text((img_x + 176 + 30, img_y + 40), "flatten()", font=font([ARIAL_BOLD], 15), fill=INK)

    caption = ("Every line is one learned weight. 6,912x128 weights connect the input layer to hidden layer 1 alone --\n"
               "drawn schematically here (only a handful of nodes per layer, marked '...') at a small fraction of true density.")
    draw.text((30, 730), caption, font=small_font, fill=MUTED)

    canvas.save(os.path.join(OUT_DIR, "nn-cats-dogs-network-architecture.png"))
    print("Saved network-architecture")


if __name__ == "__main__":
    sample_dataset_grid()
    confusion_matrix_plot()
    loss_curve_plot()
    sample_predictions_grid()
    network_diagram()
