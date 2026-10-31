"""The travertine laid onto the photo's panel in "Ünite tasarla" (img/mat/traverten.webp).

  python tools/materials.py

Generated, tileable: soft horizontal bands and many fine, short pores, as in Roman travertine. The page
multiplies it by the light measured on the marble, so it only carries colour and texture.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "mat")


def ramp(gray, dark, light):
    t = np.asarray(gray, dtype=np.float32) / 255
    d, l = np.array(dark, np.float32), np.array(light, np.float32)
    return Image.fromarray((d + (l - d) * t[..., None]).clip(0, 255).astype(np.uint8))


def main():
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(7)
    w = h = 768
    y = np.arange(h)[:, None]
    x = np.arange(w)[None, :]
    bands = sum(a * np.sin(y * f * 2 * np.pi / h + p + .5 * np.sin(x * 2 * np.pi / w * k)) for a, f, p, k in
                [(.045, 3, 0, 1), (.03, 8, 1.3, 2), (.02, 19, 2.1, 1), (.012, 37, .4, 3)])
    noise = np.asarray(Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4)), np.float32) / 255
    lum = np.clip(.84 + bands + (noise - .5) * .05, 0, 1)
    img = ramp(Image.fromarray((lum * 255).astype(np.uint8)), (172, 152, 120), (236, 225, 204))
    pores = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(pores)
    for _ in range(900):
        cx, cy, ln, th = rng.random() * w, rng.random() * h, 1.5 + rng.random() ** 2 * 9, .5 + rng.random() * .7
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                d.ellipse((cx + dx - ln, cy + dy - th, cx + dx + ln, cy + dy + th), fill=int(40 + rng.random() * 70))
    pores = pores.filter(ImageFilter.GaussianBlur(.6))
    Image.composite(Image.new("RGB", (w, h), (168, 146, 112)), img, pores).save(os.path.join(OUT, "traverten.webp"), "WEBP", quality=86, method=6)
    print("traverten.webp")


if __name__ == "__main__":
    main()
