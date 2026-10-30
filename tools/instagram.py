"""Make the site's photos from Arkhera's own Instagram posts (instagram-raw/, 640 px thumbnails).

  python tools/instagram.py

Each entry: post shortcode -> output name, crop box (left, top, right, bottom) in source pixels or None.
The crops cut away the text panels and logo strips the posts carry.
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "instagram-raw")
OUT = os.path.join(ROOT, "img")

PHOTOS = {
    "Dc6APMMjQem": ("fener-bey", None),               # Fener Bey Villaları, Gölbaşı
    "DdOkF23DQ3z": ("royal-mersin", None),            # Royal Projesi, Mersin
    "DcjwMBZjSZX": ("lodumlu", None),                 # Lodumlu villa, Çankaya
    "DbqFLzYDfC1": ("incek", None),                   # İncek anahtar teslim tadilat
    "Db-aqjTDYJv": ("savunma-ofis", (0, 0, 392, 300)),  # left of the text panel, above the logo strip
    "DcJzGtdNrvx": ("sema-hanim", None),              # Sema Hanım'ın evi
    "Dbsbhr0tLwF": ("banyo", (0, 0, 360, 512)),       # above the logo
    "DcJzwOUt9nV": ("dresuar", (0, 150, 360, 490)),   # between the black title bars
    "DbsF5Y4tG_t": ("kapi", (0, 40, 360, 600)),       # entrance door with the engraved mark
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for code, (name, box) in PHOTOS.items():
        im = Image.open(os.path.join(RAW, code + ".jpg")).convert("RGB")
        if box:
            im = im.crop(box)
        im.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=84, method=6)
        print(name, im.size)


if __name__ == "__main__":
    main()
