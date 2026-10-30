"""Turn the four film keyframes into the site's images (img/film/).

  python tools/keyframes.py [folder]        # default folder: gemini/

The folder holds 1-kesif, 2-proje, 3-uretim, 4-teslim (desktop, landscape) and optionally the same
names with -m (phone, portrait), as .png, .jpg, .jpeg or .webp.

Gemini's edits drift by a percent or so, which shows as ghosting in the cross-fades, so every
frame is first aligned to 3-uretim (uniform scale and shift that best match the edges). Then each
is cropped to 16:9 / 9:16 and saved as WebP: 1920 × 1080 and 1080 × 1920. Without -m files the
phone frames are cut from the desktop ones around FOCUS_X, the TV wall.
The printed match is the edge similarity to 3-uretim: around 0.6 or more is the same camera;
well below 0.5 means Gemini moved the camera and the frame should be redone.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "gemini")
OUT = os.path.join(ROOT, "img", "film")
NAMES = ["1-kesif", "2-proje", "3-uretim", "4-teslim"]
REF = "3-uretim"
FOCUS_X = .62  # where the phone crop is centred on a desktop frame (0 = left edge, 1 = right)


def find(name):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(SRC, name + ext)
        if os.path.exists(path):
            return path
    return None


def edges(im, w):
    small = im.convert("L").resize((w, round(w * im.height / im.width)))
    return np.asarray(small.filter(ImageFilter.FIND_EDGES), dtype=np.float32)


def align(im, ref):
    """Scale and shift im so its edges best match ref's; the gaps at the border are filled from im itself."""
    im = im.resize(ref.size)
    W = 500
    A = edges(ref, W)
    H = A.shape[0]
    best = (-1, 1.0, 0, 0)
    for s in np.arange(.97, 1.0301, .0025):
        w, h = round(W * s), round(H * s)
        B = edges(im.resize((w, h)), w) if w != W else edges(im, W)
        B = B[:h, :w]
        for dx in range(-10, 11):
            for dy in range(-8, 9):
                x0, y0 = (W - w) // 2 + dx, (H - h) // 2 + dy
                xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
                a, b = A[ya:yb, xa:xb], B[ya - y0:yb - y0, xa - x0:xb - x0]
                score = float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))
                if score > best[0]:
                    best = (score, s, dx, dy)
    score, s, dx, dy = best
    k = ref.width / W
    w, h = round(ref.width * s), round(ref.height * s)
    out = im.copy()  # background for the border, in case the frame shrinks
    out.paste(im.resize((w, h), Image.LANCZOS), ((ref.width - w) // 2 + round(dx * k), (ref.height - h) // 2 + round(dy * k)))
    return out, f"scale {s:.4f}, shift {round(dx * k)},{round(dy * k)} px, match {score:.2f}"


def crop(im, w, h, fx=.5):
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = min(max(0, round(im.width * fx - w / 2)), im.width - w)
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    paths = {n: find(n) for n in NAMES}
    missing = [n for n, p in paths.items() if not p]
    if missing:
        sys.exit(f"missing {', '.join(missing)} in {SRC}")
    ref = Image.open(paths[REF]).convert("RGB")
    ref_m = find(REF + "-m")
    ref_m = Image.open(ref_m).convert("RGB") if ref_m else None
    for name in NAMES:
        im = Image.open(paths[name]).convert("RGB")
        note = "reference"
        if name != REF:
            im, note = align(im, ref)
        crop(im, 1920, 1080).save(os.path.join(OUT, name + ".webp"), "WEBP", quality=80, method=6)
        phone = find(name + "-m")
        if phone and ref_m:
            pm = Image.open(phone).convert("RGB")
            if name != REF:
                pm, _ = align(pm, ref_m)
            crop(pm, 1080, 1920).save(os.path.join(OUT, name + "-m.webp"), "WEBP", quality=78, method=6)
        else:
            crop(im, 1080, 1920, FOCUS_X).save(os.path.join(OUT, name + "-m.webp"), "WEBP", quality=78, method=6)
        print(name, note, "| phone:", "own image" if phone and ref_m else f"cut from desktop at x={FOCUS_X}")


if __name__ == "__main__":
    main()
