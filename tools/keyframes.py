"""Turn the four film keyframes into the site's images (img/film/).

  python tools/keyframes.py [folder]        # default folder: gemini/

The folder holds 1-kesif, 2-proje, 3-uretim, 4-teslim (desktop, landscape) and optionally the same
names with -m (phone, portrait), as .png, .jpg, .jpeg or .webp. Each image is cropped to 16:9
(or 9:16) around its centre and saved as WebP: 1920 × 1080 and 1080 × 1920. Without -m files the
phone frames are cut from the middle of the desktop ones, which only works if the room's focal
point (the TV wall) is near the centre.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "gemini")
OUT = os.path.join(ROOT, "img", "film")
NAMES = ["1-kesif", "2-proje", "3-uretim", "4-teslim"]


def find(name):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(SRC, name + ext)
        if os.path.exists(path):
            return path
    return None


def cover(im, w, h):
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in NAMES:
        desk = find(name)
        if not desk:
            sys.exit(f"missing {name} in {SRC}")
        im = Image.open(desk).convert("RGB")
        cover(im, 1920, 1080).save(os.path.join(OUT, name + ".webp"), "WEBP", quality=78, method=6)
        phone = find(name + "-m")
        pm = Image.open(phone).convert("RGB") if phone else im
        cover(pm, 1080, 1920).save(os.path.join(OUT, name + "-m.webp"), "WEBP", quality=76, method=6)
        print(name, "desktop", im.size, "phone", pm.size if phone else "cut from desktop")


if __name__ == "__main__":
    main()
