#!/usr/bin/env python3
"""
graph_helper.py — Drop this in your site root.
Import it in any analysis script to save graphs directly to static/images/.

Usage in your post scripts:
    from graph_helper import save_fig
    import matplotlib.pyplot as plt

    plt.plot([1, 2, 3], [4, 5, 6])
    save_fig("my-chart")   # saves to static/images/my-chart.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle

# Point to your site's static/images directory
STATIC_IMAGES = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(STATIC_IMAGES, exist_ok=True)


def dark_style():
    """Apply a dark matplotlib style consistent with the site theme."""
    plt.rcParams.update({
        "figure.facecolor":  "#1a1a2e",
        "axes.facecolor":    "#16213e",
        "axes.edgecolor":    "#444",
        "axes.labelcolor":   "#ccc",
        "xtick.color":       "#999",
        "ytick.color":       "#999",
        "text.color":        "#eee",
        "grid.color":        "#333",
        "grid.linestyle":    "--",
        "grid.alpha":        0.5,
        "lines.linewidth":   2.0,
        "font.family":       "monospace",
    })


def save_fig(name: str, dpi: int = 150) -> str:
    """
    Save the current matplotlib figure to static/images/<name>.png.
    Returns the markdown image tag to paste into your post.
    """
    out = os.path.join(STATIC_IMAGES, f"{name}.png")
    plt.tight_layout()
    plt.savefig(out, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: static/images/{name}.png")
    print(f"   Markdown: ![{name}](/images/{name}.png)")
    return f"![{name}](/images/{name}.png)"


# Example usage when run directly
if __name__ == "__main__":
    import numpy as np

    dark_style()
    x = np.linspace(0, 4 * np.pi, 300)
    plt.figure(figsize=(10, 4))
    plt.plot(x, np.sin(x), color="#4f8ef7", label="sin(x)")
    plt.plot(x, np.cos(x), color="#f7944f", label="cos(x)")
    plt.title("Example Graph — Dark Mode")
    plt.legend()
    plt.grid(True)
    save_fig("example-graph")
