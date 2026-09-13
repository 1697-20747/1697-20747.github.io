"""
generate_dataset.py
--------------------
Builds a small, fully-reproducible "cats vs dogs" image folder using only
Pillow (the open-source Python Imaging Library fork). Every image is a
procedurally-drawn silhouette, not a photograph -- see the blog post's
"About the images" section for why, and for the two-line swap to real
photographs instead.
"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw

RNG_SEED = 42
IMG_SIZE = 48          # pixels, square, RGB
N_TRAIN_PER_CLASS = 260
N_TEST_PER_CLASS = 60
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")


def _jitter(value, spread):
    return value + random.uniform(-spread, spread)


def draw_cat(draw, size):
    cx, cy = size / 2, size * 0.58
    body_w, body_h = size * 0.5, size * 0.42
    colour = random.choice([(60, 60, 60), (120, 90, 60), (200, 170, 110), (30, 30, 30)])
    colour = tuple(int(np.clip(_jitter(c, 15), 0, 255)) for c in colour)

    head_r = size * random.uniform(0.22, 0.27)
    hx, hy = _jitter(cx, 3), _jitter(size * 0.32, 3)
    draw.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=colour)

    # ears: triangular, pointy, sit on top of the head
    ear_h = head_r * random.uniform(0.9, 1.3)
    for side in (-1, 1):
        ex = hx + side * head_r * 0.55
        ey = hy - head_r * 0.5
        draw.polygon(
            [
                (ex - head_r * 0.28, ey + head_r * 0.15),
                (ex + head_r * 0.28, ey + head_r * 0.15),
                (ex + side * head_r * 0.12, ey - ear_h * 0.7),
            ],
            fill=colour,
        )

    # body: shorter, rounder than a dog's
    draw.ellipse(
        [cx - body_w / 2, cy - body_h / 2, cx + body_w / 2, cy + body_h / 2],
        fill=colour,
    )

    # tail: thin curved-ish line to one side
    tail_side = random.choice([-1, 1])
    tx0, ty0 = cx + tail_side * body_w * 0.45, cy + body_h * 0.1
    tx1 = tx0 + tail_side * size * 0.18
    ty1 = ty0 - size * 0.18
    draw.line([(tx0, ty0), (tx1, ty1)], fill=colour, width=max(2, int(size * 0.03)))

    # whiskers: thin light lines from the head
    whisker_colour = (min(255, colour[0] + 120),) * 3
    for i in range(3):
        yoff = hy + head_r * (0.05 * i - 0.05)
        draw.line([(hx - head_r * 0.9, yoff), (hx - head_r * 1.6, yoff - 3)], fill=whisker_colour, width=1)
        draw.line([(hx + head_r * 0.9, yoff), (hx + head_r * 1.6, yoff - 3)], fill=whisker_colour, width=1)


def draw_dog(draw, size):
    cx, cy = size / 2, size * 0.58
    body_w, body_h = size * 0.6, size * 0.36
    colour = random.choice([(150, 110, 60), (90, 60, 30), (210, 190, 150), (70, 70, 70)])
    colour = tuple(int(np.clip(_jitter(c, 15), 0, 255)) for c in colour)

    head_r = size * random.uniform(0.20, 0.26)
    hx, hy = _jitter(cx, 3), _jitter(size * 0.30, 3)

    # ears: floppy (rounded, not pointy) blobs, positioned above the head
    ear_w, ear_h = head_r * 0.6, head_r * 1.1
    for side in (-1, 1):
        ex = hx + side * head_r * 0.6
        ey = hy - head_r * 0.65
        draw.ellipse([ex - ear_w / 2, ey - ear_h * 0.3, ex + ear_w / 2, ey + ear_h * 0.7], fill=colour)

    # head
    draw.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=colour)

    # snout: protrudes sideways from the head, at head height -- the key
    # geometric difference from the cat template
    snout_side = random.choice([-1, 1])
    snout_len, snout_h = head_r * 0.7, head_r * 0.55
    sx0 = hx + snout_side * head_r * 0.7
    sx1 = hx + snout_side * (head_r * 0.7 + snout_len)
    x_lo, x_hi = sorted([sx0, sx1])
    draw.rectangle([x_lo, hy - snout_h / 2, x_hi, hy + snout_h / 2], fill=colour)

    # body: longer, flatter than a cat's
    draw.ellipse(
        [cx - body_w / 2, cy - body_h / 2, cx + body_w / 2, cy + body_h / 2],
        fill=colour,
    )

    # tail: short and thick, wagging up
    tail_side = random.choice([-1, 1])
    tx0, ty0 = cx + tail_side * body_w * 0.48, cy
    tx1 = tx0 + tail_side * size * 0.10
    ty1 = ty0 - size * 0.14
    draw.line([(tx0, ty0), (tx1, ty1)], fill=colour, width=max(3, int(size * 0.045)))


def make_image(label, size=IMG_SIZE):
    bg = tuple(random.randint(200, 245) for _ in range(3))
    img = Image.new("RGB", (size, size), color=bg)
    draw = ImageDraw.Draw(img)
    (draw_cat if label == "cat" else draw_dog)(draw, size)

    arr = np.asarray(img).astype(np.int16)
    noise = np.random.normal(0, 8, arr.shape)          # camera-sensor-noise stand-in
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def build_dataset():
    random.seed(RNG_SEED)
    np.random.seed(RNG_SEED)
    for split, n in (("train", N_TRAIN_PER_CLASS), ("test", N_TEST_PER_CLASS)):
        for label in ("cats", "dogs"):
            folder = os.path.join(OUT_DIR, split, label)
            os.makedirs(folder, exist_ok=True)
            singular = "cat" if label == "cats" else "dog"
            for i in range(n):
                make_image(singular).save(os.path.join(folder, f"{singular}_{i:04d}.png"))
    print("Dataset written to", OUT_DIR)


if __name__ == "__main__":
    build_dataset()
