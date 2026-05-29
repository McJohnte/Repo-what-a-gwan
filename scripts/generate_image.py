#!/usr/bin/env python3
"""Generate a banner PNG for the repository.

Usage:
    python scripts/generate_image.py [output_path]

Requires Pillow:
    pip install Pillow
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630  # standard social/banner size

# Jamaican-flag inspired palette (a nod to "what a gwan")
GREEN = (0, 154, 68)
GOLD = (254, 209, 0)
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _load_font(size):
    """Try a few common font paths, falling back to Pillow's default."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_centered(draw, text, font, y, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) / 2, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def generate(output_path: Path) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Vertical gradient background: green -> black
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        draw.line([(0, y), (WIDTH, y)], fill=_lerp(GREEN, BLACK, t))

    # Gold diagonal accent stripes (top-left and bottom-right corners)
    draw.polygon([(0, 0), (220, 0), (0, 220)], fill=GOLD)
    draw.polygon(
        [(WIDTH, HEIGHT), (WIDTH - 220, HEIGHT), (WIDTH, HEIGHT - 220)],
        fill=GOLD,
    )

    # Title + subtitle
    title_font = _load_font(96)
    sub_font = _load_font(40)
    h = _draw_centered(draw, "Repo-what-a-gwan", title_font, 230, WHITE)
    _draw_centered(draw, "what a gwan?", sub_font, 230 + h + 40, GOLD)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Wrote {output_path} ({WIDTH}x{HEIGHT})")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/banner.png")
    generate(out)


if __name__ == "__main__":
    main()
