"""Make the two section photos from the opener's Gemini frames (gemini/2-proje, gemini/3-uretim).

  python tools/stills.py

- img/tasarla.webp (4:3) and img/tasarla-m.webp (1:1): the TV wall of the finished room, shown
  beside the unit options.
- img/render-split.webp (900 × 1100): the same view, left half white model, right half finished,
  split by the brass line the opener uses. Shown with "İç mimari proje ve 3D tasarım".
Crop boxes are in the 2000 × 1116 frames; adjust them if the frames are regenerated.
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "gemini")
IMG = os.path.join(ROOT, "img")


def frame(name):
    for ext in (".jpg", ".png", ".jpeg", ".webp"):
        path = os.path.join(SRC, name + ext)
        if os.path.exists(path):
            return Image.open(path).convert("RGB").resize((2000, 1116), Image.LANCZOS)
    raise SystemExit(f"missing {name} in {SRC}")


def main():
    done = frame("3-uretim")
    clay = frame("2-proje")
    done.crop((880, 160, 1900, 925)).resize((1200, 900), Image.LANCZOS).save(os.path.join(IMG, "tasarla.webp"), "WEBP", quality=82, method=6)
    done.crop((960, 110, 1880, 1030)).resize((900, 900), Image.LANCZOS).save(os.path.join(IMG, "tasarla-m.webp"), "WEBP", quality=82, method=6)
    box = (700, 0, 1613, 1116)  # 913 × 1116 ≈ 900 × 1100, centred on the TV wall
    split = done.crop(box)
    cut = (box[2] - box[0]) // 2
    split.paste(clay.crop(box).crop((0, 0, cut, 1116)), (0, 0))
    ImageDraw.Draw(split).rectangle((cut - 1, 0, cut + 1, 1116), fill=(233, 200, 143))
    split.resize((900, 1100), Image.LANCZOS).save(os.path.join(IMG, "render-split.webp"), "WEBP", quality=82, method=6)
    print("tasarla.webp, tasarla-m.webp, render-split.webp")


if __name__ == "__main__":
    main()
