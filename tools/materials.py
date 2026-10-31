"""Surfaces for the "Ünite tasarla" 3D unit.

  python tools/materials.py

- img/mat/mermer.webp: one generated Calacatta slab, large enough to cover the panel without repeating.
- img/mat/traverten.webp: generated, tileable: soft horizontal bands and many fine, short pores.
- img/tex/floor-*.webp: Poly Haven herringbone_parquet (CC0, textures-raw/), lightened to the
  honey oak of the opening room. img/tex/oak-*.webp are oak_veneer_01 (CC0), as in the Maviron demo.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "mat")


def ramp(gray, dark, light):
    t = np.asarray(gray, dtype=np.float32) / 255
    d, l = np.array(dark, np.float32), np.array(light, np.float32)
    return Image.fromarray((d + (l - d) * t[..., None]).clip(0, 255).astype(np.uint8))


def marble(w=1024, h=1240, seed=5):
    """One Calacatta slab, sized to cover the whole panel (no repeats): a warm white ground, a few broad
    soft grey veins running diagonally, sharper thin veins beside them and a little gold."""
    rng = np.random.default_rng(seed)
    base = Image.new("RGB", (w, h), (241, 238, 233))
    cloud = Image.fromarray((rng.random((h // 16, w // 16)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    base = Image.composite(Image.new("RGB", (w, h), (230, 226, 219)), base, cloud.point(lambda v: int(v * .5)))

    def vein(layer, width, blur, colour, alpha, start, drift):
        # a slow random walk of the heading gives the long, gently wandering line of a real vein
        d = ImageDraw.Draw(layer)
        x, y = start
        heading = np.arctan2(1, drift)
        turn = 0.0
        wd = width
        base = heading
        while y < h + 60 and -200 < x < w + 200:
            # mostly straight, with a slow sway back towards its course and a fine crackle along the edge
            turn = turn * .9 + rng.normal(0, .012) + (base - heading) * .01
            heading += turn
            jit = rng.normal(0, 1.1)
            nx = x + np.cos(heading) * 4 - np.sin(heading) * jit
            ny = y + np.sin(heading) * 4 + np.cos(heading) * jit
            wd = np.clip(wd + rng.normal(0, width * .08), width * .3, width * 1.6)
            d.line([(x, y), (nx, ny)], fill=colour + (alpha,), width=max(1, int(round(wd))))
            x, y = nx, ny
        return layer.filter(ImageFilter.GaussianBlur(blur))

    out = base.convert("RGBA")
    starts = [(rng.random() * w * .9, -40) for _ in range(4)]
    for sx, sy in starts:
        drift = .55 + rng.random() * .5
        seed_state = rng.bit_generator.state
        out = Image.alpha_composite(out, vein(Image.new("RGBA", (w, h)), 30, 16, (160, 156, 150), 38, (sx, sy), drift))
        rng.bit_generator.state = seed_state  # the sharp vein follows the same course as its soft halo
        out = Image.alpha_composite(out, vein(Image.new("RGBA", (w, h)), 3.2, 1.1, (112, 108, 103), 175, (sx, sy), drift))
        if rng.random() < .5:
            out = Image.alpha_composite(out, vein(Image.new("RGBA", (w, h)), 1.6, .7, (176, 140, 84), 140, (sx + 24, sy), drift))
    for _ in range(5):
        out = Image.alpha_composite(out, vein(Image.new("RGBA", (w, h)), 1.1, .5, (134, 130, 124), 95, (rng.random() * w, rng.random() * h * .6 - 40), .5 + rng.random() * .9))
    return out.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    marble().save(os.path.join(OUT, "mermer.webp"), "WEBP", quality=86, method=6)
    floor = Image.open(os.path.join(ROOT, "textures-raw", "parquet-Diffuse.jpg")).convert("RGB")
    floor = ImageEnhance.Brightness(floor).enhance(1.35)
    ImageEnhance.Color(floor).enhance(.68).save(os.path.join(ROOT, "img", "tex", "floor-diff.webp"), "WEBP", quality=80, method=6)
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
    print("mermer.webp, traverten.webp, floor-diff.webp")


if __name__ == "__main__":
    main()
