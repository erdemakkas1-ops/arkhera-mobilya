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
VASES = [(158, 560), (256, 560), (256, 650), (158, 650)]
PLANT = [(928, 590), (1078, 590), (1078, 768), (928, 768)]  # plant, pot and books
ARMCHAIR = [(90, 615), (128, 615), (128, 770), (90, 770)]   # its arm overlaps the cabinet's left end
BOOKS = [(934, 707), (1063, 714), (1065, 756), (932, 745)]  # dark spines too, so the whole stack
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
    # the things standing on or against the unit: cream vases, white pot and books, the armchair, the plant.
    # Everything else inside the wood zones is wood, its shadows, highlights and dark gaps included.
    # They are picked out only inside their own boxes, where anything not dark brown wood belongs to them.
    green = (g > r * 1.02) & (g > b) & (sat > .12)
    not_wood = ((mx > .42) & (sat < .34)) | green
    boxes = np.clip(poly(VASES) + poly(PLANT) + poly(ARMCHAIR), 0, 1)
    objects = not_wood * boxes

    frame = poly(FRAME, width=6)
    # the TV: its dark pixels inside a slightly larger outline, so the stone reaches right up to its edge,
    # then closed, so the window's reflection on the screen counts as TV too
    tv_zone = np.asarray(Image.fromarray((poly(TV) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)), dtype=np.float32) / 255
    dark = Image.fromarray((tv_zone * (mx < .3) * 255).astype(np.uint8))
    tv = np.asarray(dark.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.MinFilter(31)), dtype=np.float32) / 255 * tv_zone
    cab = poly(CABINET)
    wood_zone = np.clip(poly(SLATS_L) + poly(SLATS_R) + cab, 0, 1)
    # opening: thin bright slat edges inside the boxes drop out, the solid objects stay (and grow a little)
    obj_img = Image.fromarray((objects * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(9))
    obj = np.clip(np.asarray(obj_img, dtype=np.float32) / 255 * boxes + poly(BOOKS), 0, 1)
    wood = wood_zone * (1 - obj)
    # low saturation keeps the oak floor under the cabinet out of the stone
    stone = poly(STONE) * (1 - cab) * (1 - tv) * (1 - frame) * (mx > .42) * (sat < .32) * (1 - wood)
    # brass, measured against the marble beside it: warmer (r/b ≈ 1.21 against 1.09), more saturated, a little darker.
    # Where the light makes it pale this misses, so a line is fitted to each side's brass pixels and the frame is
    # drawn from those four lines: thin, continuous and exactly on the photo's brass.
    brass = frame * (1 - tv) * (sat > .14) * (r > b * 1.17) * (mx < .82) > .5
    ys_, xs_ = np.nonzero(brass)
    sides = []
    for k in range(4):
        (ax, ay), (bx, by) = FRAME[k], FRAME[(k + 1) % 4]
        nx_, ny_ = by - ay, ax - bx
        nl = np.hypot(nx_, ny_)
        dist = np.abs((xs_ - ax) * nx_ + (ys_ - ay) * ny_) / nl
        along = ((xs_ - ax) * (bx - ax) + (ys_ - ay) * (by - ay)) / nl ** 2
        sel = (dist < 6) & (along > .05) & (along < .95)
        px_, py_ = xs_[sel].astype(np.float64), ys_[sel].astype(np.float64)
        if abs(bx - ax) > abs(by - ay):  # mostly horizontal: y = a x + c
            a_, c_ = np.polyfit(px_, py_, 1); sides.append(('h', a_, c_))
        else:                            # mostly vertical: x = a y + c
            a_, c_ = np.polyfit(py_, px_, 1); sides.append(('v', a_, c_))

    def meet(s1, s2):
        h, v = (s1, s2) if s1[0] == 'h' else (s2, s1)
        # y = ah x + ch, x = av y + cv
        y = (h[1] * v[2] + h[2]) / (1 - h[1] * v[1])
        return (v[1] * y + v[2], y)

    corners = [meet(sides[k - 1], sides[k]) for k in range(4)]
    metal = poly([tuple(map(float, c)) for c in corners], width=4) * (1 - tv)

    # soften by a pixel so recoloured edges do not stair-step
    def soft(a):
        return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7)), dtype=np.uint8)

    Image.merge("RGB", [Image.fromarray(soft(m)) for m in (wood, stone, metal)]).save(os.path.join(IMG, "tasarla-mask.png"), optimize=True)

    # LED light: strongest just under the cabinet's lower edge, fading over ~150 px, weighted by warmth
    (x0, y0), (x1, y1) = CAB_BOTTOM
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = y0 + (xs - x0) * (y1 - y0) / (x1 - x0)
    below = ys - edge
    fall = np.where((below > -6) & (xs > x0 - 10), np.exp(-np.maximum(below, 0) / 170), 0)
    warmth = np.clip((r - b) * 2.6, 0, 1) * np.clip(mx * 1.4, 0, 1)
    table = ((xs - 258) / 214) ** 2 + ((ys - 860) / 70) ** 2 < 1  # the coffee table's top keeps its own light
    glow = np.clip(fall * (.35 + .65 * warmth), 0, 1) * (1 - cab) * (1 - table)
    glow_img = Image.fromarray((glow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    # G: the whole panel face (frame and edge pixels included), covered completely when the panel is slats
    panel = Image.fromarray(soft(poly(STONE) * (1 - cab) * (1 - tv)))
    Image.merge("RGB", [glow_img, panel, Image.new("L", (W, H))]).save(os.path.join(IMG, "tasarla-glow.png"), optimize=True)
    print("tasarla-mask.png, tasarla-glow.png")


if __name__ == "__main__":
    main()
