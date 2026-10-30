"""Build the static site into dist/.

  python tools/build.py [https://site-url]

arkhera.html is the single source (it is also what the claude.ai artifact publishes, which wraps
it in its own document). This script wraps it in a full HTML document, adds the favicon and the
share image, and copies img/. With a site URL it also writes absolute canonical/og URLs.
"""
import os
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SITE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ""

# the Arkhera mark (circle, peak, three columns) in bone on espresso
FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    '<rect width="100" height="100" rx="14" fill="#14100d"/>'
    '<g transform="translate(6 2) scale(.88)" fill="#f1ebe2" stroke="#f1ebe2">'
    '<circle cx="50" cy="57" r="36" fill="none" stroke-width="4"/>'
    '<path d="M24 92 50 6l26 86" fill="none" stroke-width="5"/>'
    '<rect x="40" y="58" width="5" height="30" stroke="none"/>'
    '<rect x="47.5" y="44" width="5" height="44" stroke="none"/>'
    '<rect x="55" y="58" width="5" height="30" stroke="none"/></g></svg>'
)


def share_image(dst):
    # the last film keyframe (finished room at dusk), cropped to 1200 × 630
    src = Image.open(os.path.join(ROOT, "img", "film", "4-teslim.webp")).convert("RGB")
    w, h = 1200, 630
    scale = max(w / src.width, h / src.height)
    src = src.resize((round(src.width * scale), round(src.height * scale)), Image.LANCZOS)
    left, top = (src.width - w) // 2, (src.height - h) // 2
    src.crop((left, top, left + w, top + h)).save(dst, "JPEG", quality=84, optimize=True, progressive=True)


def main():
    os.makedirs(DIST, exist_ok=True)
    for name in os.listdir(DIST):
        if name == ".vercel":
            continue
        path = os.path.join(DIST, name)
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

    with open(os.path.join(ROOT, "arkhera.html"), encoding="utf-8") as f:
        src = f.read()
    cut = src.index("</style>") + len("</style>")
    head, body = src[:cut], src[cut:].lstrip("\n")

    # relative, so the site also works from a sub-path such as <user>.github.io/arkhera-mobilya/
    extra = ['<link rel="icon" href="favicon.svg" type="image/svg+xml">']
    if SITE:
        extra += [
            f'<link rel="canonical" href="{SITE}/">',
            f'<meta property="og:url" content="{SITE}/">',
            f'<meta property="og:image" content="{SITE}/og.jpg">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]

    page = (
        '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + "\n".join(extra) + "\n" + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(DIST, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)
    if os.path.exists(os.path.join(ROOT, "img", "film", "4-teslim.webp")):
        share_image(os.path.join(DIST, "og.jpg"))
    shutil.copytree(os.path.join(ROOT, "img"), os.path.join(DIST, "img"))
    shutil.copy(os.path.join(ROOT, "vercel.json"), DIST)

    size = sum(os.path.getsize(os.path.join(d, n)) for d, _, ns in os.walk(DIST) for n in ns)
    print(f"dist/ built, {size / 1e6:.2f} MB" + (f", site {SITE}" if SITE else ""))


if __name__ == "__main__":
    main()
