"""Turn the film captures in tools/frames/ into the site's posters.

  python tools/posters.py

Capture first: serve dist/, open /?capture at 1600 × 1000, call __film.seek(t) and screenshot
t=0 (poster.png), t=12 (still.png), t=6.15 (split.png); then at 390 × 844, t=0 (poster-m.png).
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR = os.path.join(ROOT, "tools", "frames")
IMG = os.path.join(ROOT, "img")


def save(name, out, size=None, box=None):
    im = Image.open(os.path.join(FR, name)).convert("RGB")
    if box:
        im = im.crop(box)
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(os.path.join(IMG, out), "WEBP", quality=80, method=6)
    print(out, im.size)


save("poster.png", "film-poster.webp", (1600, 1000))
save("poster-m.png", "film-poster-m.webp")
save("still.png", "film-still.webp", (1600, 1000))
# the clay / material seam sits near the middle of the frame at t = 6.15
save("split.png", "render-split.webp", (900, 1100), (380, 0, 1198, 1000))
