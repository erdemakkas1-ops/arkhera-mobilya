"""Masks for recolouring the unit photo (img/tasarla.webp) in the "Ünite tasarla" section.

  python tools/masks.py

Writes img/tasarla-mask.png (1200 × 900, opaque RGB):
  R = wood (both slat columns and the cabinet; the vases, plant and books are left out)
  G = stone panel (without the TV, the cabinet and the brass frame)
  B = brass frame
and img/tasarla-glow.png: R = how much of each pixel's light comes from the LED under the cabinet,
G = the whole panel face, which slats cover completely.
The polygons are traced on tasarla.webp; redo them if the photo changes (tools/stills.py).
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "img")
W, H = 1200, 900

SLATS_L = [(160, 176), (301, 150), (301, 785), (160, 765)]
SLATS_R = [(861, 44), (1152, 0), (1152, 900), (861, 900)]
STONE = [(301, 150), (861, 44), (861, 708), (301, 652)]  # down to the cabinet top; below it is floor and table
CABINET = [(106, 628), (1152, 734), (1152, 900), (1128, 900), (116, 745)]
TV = [(354, 349), (748, 329), (748, 602), (354, 575)]
FRAME = [(320, 176), (829, 95), (829, 668), (320, 613)]
# the cabinet's lower edge, from which the LED light falls on the floor and the stone
CAB_BOTTOM = [(116, 745), (1128, 897)]


def poly(points, width=0):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    if width:
        d.line(points + points[:1], fill=255, width=width, joint="curve")
    else:
        d.polygon(points, fill=255)
    return np.asarray(m, dtype=np.float32) / 255


def main():
    rgb = np.asarray(Image.open(os.path.join(IMG, "tasarla.webp")).convert("RGB").resize((W, H)), dtype=np.float32) / 255
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    # brown: red over green over blue, not bright, not grey; this keeps out the cream vases, white books and green plant
    brown = (r > g) & (g >= b * .92) & (mx < .72) & ((sat > .18) | (mx < .3))
    green = (g > r * 1.02) & (g > b)

    frame = poly(FRAME, width=7)
    # the TV is its dark pixels inside a slightly larger outline, so the stone reaches right up to its edge
    tv_zone = np.asarray(Image.fromarray((poly(TV) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)), dtype=np.float32) / 255
    tv = tv_zone * (mx < .3)
    cab = poly(CABINET)
    wood_zone = np.clip(poly(SLATS_L) + poly(SLATS_R) + cab, 0, 1)
    wood = wood_zone * brown * (1 - green)
    # low saturation keeps the oak floor under the cabinet out of the stone
    stone = poly(STONE) * (1 - cab) * (1 - tv) * (1 - frame) * (mx > .42) * (sat < .32) * (1 - wood)
    metal = frame * (1 - tv) * (sat > .08)

    # soften by a pixel so recoloured edges do not stair-step
    def soft(a):
        return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7)), dtype=np.uint8)

    Image.merge("RGB", [Image.fromarray(soft(m)) for m in (wood, stone, metal)]).save(os.path.join(IMG, "tasarla-mask.png"), optimize=True)

    # LED light: strongest just under the cabinet's lower edge, fading over ~150 px, weighted by warmth
    (x0, y0), (x1, y1) = CAB_BOTTOM
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = y0 + (xs - x0) * (y1 - y0) / (x1 - x0)
    below = ys - edge
    fall = np.where((below > -6) & (xs > x0 - 10), np.exp(-np.maximum(below, 0) / 120), 0)
    warmth = np.clip((r - b) * 2.2, 0, 1) * np.clip(mx * 1.3, 0, 1)
    table = ((xs - 258) / 222) ** 2 + ((ys - 850) / 78) ** 2 < 1  # the coffee table in front keeps its own light
    glow = np.clip(fall * (.35 + .65 * warmth), 0, 1) * (1 - cab) * (1 - table)
    glow_img = Image.fromarray((glow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    # G: the whole panel face (frame and edge pixels included), covered completely when the panel is slats
    panel = Image.fromarray(soft(poly(STONE) * (1 - cab) * (1 - tv)))
    Image.merge("RGB", [glow_img, panel, Image.new("L", (W, H))]).save(os.path.join(IMG, "tasarla-glow.png"), optimize=True)
    print("tasarla-mask.png, tasarla-glow.png")


if __name__ == "__main__":
    main()
