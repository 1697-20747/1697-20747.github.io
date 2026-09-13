"""
make_collage.py
----------------
Builds a single-frame collage of 25 random cat photos and 25 random
dog photos, sampled from the actual Oxford-IIIT Pet Dataset images
this project trained and tested every model on (both the train and
test pools, so the sample represents the real dataset, not just the
held-out slice). Purely illustrative -- no model, no inference, just
what the real photographs behind every number in this post actually
look like.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "data")
RANDOM_STATE = 42
N_PER_CLASS = 25
GRID = 5  # 5x5
THUMB = 140
GAP = 4
LABEL_H = 46
TITLE_H = 60
MARGIN = 30
PANEL_GAP = 40

INK = (11, 11, 11)
MUTED = (137, 135, 129)
BG = (252, 252, 251)
BLUE = (42, 120, 214)
ORANGE = (235, 104, 52)


def font(path_options, size):
    for p in path_options:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


BOLD = font(["/System/Library/Fonts/Supplemental/Arial Bold.ttf"], 30)
LABEL_FONT = font(["/System/Library/Fonts/Supplemental/Arial Bold.ttf"], 22)
SUB_FONT = font(["/System/Library/Fonts/Supplemental/Arial.ttf"], 16)


def gather(label):
    paths = []
    for split in ("train", "test"):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            paths.append(os.path.join(folder, fname))
    return paths


def square_thumb(path, size):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    return img.resize((size, size), Image.LANCZOS)


def build_panel(paths, size):
    panel_w = GRID * size + (GRID - 1) * GAP
    panel = Image.new("RGB", (panel_w, panel_w), BG)
    for i, p in enumerate(paths):
        thumb = square_thumb(p, size)
        r, c = divmod(i, GRID)
        x = c * (size + GAP)
        y = r * (size + GAP)
        panel.paste(thumb, (x, y))
    return panel


def main():
    rng = random.Random(RANDOM_STATE)
    cat_paths = rng.sample(gather("cats"), N_PER_CLASS)
    dog_paths = rng.sample(gather("dogs"), N_PER_CLASS)

    cat_panel = build_panel(cat_paths, THUMB)
    dog_panel = build_panel(dog_paths, THUMB)
    panel_w = cat_panel.width

    canvas_w = MARGIN * 2 + panel_w * 2 + PANEL_GAP
    canvas_h = MARGIN + TITLE_H + LABEL_H + panel_w + MARGIN
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw = ImageDraw.Draw(canvas)

    title = "50 real photos from the Oxford-IIIT Pet Dataset used throughout this post"
    draw.text((MARGIN, MARGIN), title, font=BOLD, fill=INK)
    subtitle = "25 random cats, 25 random dogs -- no cropping or curation beyond a centre square crop"
    draw.text((MARGIN, MARGIN + 40), subtitle, font=SUB_FONT, fill=MUTED)

    top_y = MARGIN + TITLE_H + LABEL_H
    cat_x = MARGIN
    dog_x = MARGIN + panel_w + PANEL_GAP

    label_y = MARGIN + TITLE_H + 6
    draw.text((cat_x, label_y), f"Cats (n={N_PER_CLASS})", font=LABEL_FONT, fill=INK)
    draw.rectangle([cat_x, label_y + 30, cat_x + 46, label_y + 34], fill=BLUE)
    dog_label = f"Dogs (n={N_PER_CLASS})"
    dog_label_w = draw.textlength(dog_label, font=LABEL_FONT)
    draw.text((dog_x, label_y), dog_label, font=LABEL_FONT, fill=INK)
    draw.rectangle([dog_x, label_y + 30, dog_x + 46, label_y + 34], fill=ORANGE)

    canvas.paste(cat_panel, (cat_x, top_y))
    canvas.paste(dog_panel, (dog_x, top_y))

    out_path = "/Users/bruceschultz/Documents/blog/169720747/static/images/comp-science/nn-cats-dogs-real-photo-collage.png"
    canvas.save(out_path)
    print("Saved:", out_path, canvas.size)


if __name__ == "__main__":
    main()
