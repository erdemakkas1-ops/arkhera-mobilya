# Arkhera Mobilya & Dekorasyon — scroll film demo

One-page demo for Arkhera Mobilya & Dekorasyon (@arkhera_mobilya, Ankara; Mimar Yasemin Kara):
interior architecture, 3D design and render, custom-made furniture, turnkey renovation. Same family
as the Oha Burger and Maviron Çelik demos: the hero is a film scrubbed by page scroll.

Live: https://erdemakkas1-ops.github.io/arkhera-mobilya/ (GitHub Pages, repo `erdemakkas1-ops/arkhera-mobilya`,
branch `gh-pages`; `*.vercel.app` is blocked on some Turkish networks, so the demo lives on Pages).
`pages/` is a checkout of `gh-pages` (kept out of git). To update the live site:

```bash
py -3 tools/build.py https://erdemakkas1-ops.github.io/arkhera-mobilya
cp -r dist/index.html dist/favicon.svg dist/og.jpg dist/img pages/
cd pages && git add -A && git commit -m "Update site" && git push
```

## The film

Four keyframes of one room from one camera (`img/film/`, 1920 × 1080 and 1080 × 1920 for phones),
scrubbed by scroll over film seconds 0–12, telling Arkhera's own process:

1. **Keşif & metraj** — the empty, unfinished room (`1-kesif`).
2. **Proje & 3D** — fades to the same room as a white clay model (`2-proje`).
3. **Özel üretim** — a brass scan line wipes right to left, revealing the finished room (`3-uretim`).
4. **Anahtar teslim** — fades to dusk with the LEDs on (`4-teslim`); closing call to action.

- The frames are Gemini images (see `GEMINI.md` for the prompts and order; originals in `gemini/`,
  kept out of git). `py -3 tools/keyframes.py [folder]` aligns them to `3-uretim`, crops and converts
  them; a printed match well below 0.5 means Gemini moved the camera and the frame should be redone.
- The whole stage pushes in slightly (scale 1.07 → 1). Chapter captions use `data-from`/`data-to`
  in film seconds; annotation tags use `data-d` / `data-m`, a point on the desktop / phone image as
  fractions of its width and height. Re-place them when the images change.
- The site loads no 3D library: the opener is images, the unit section an SVG drawing.
- `prefers-reduced-motion`, no JS, or `?still` show the dusk frame and the four chapters as text.

## Other sections

- Stüdyo, Projeler (sideways scroll on wide screens with a mouse, native swipe elsewhere),
  Hizmetler (the row in the middle of the screen lights up and swaps the picture).
- **Ünite tasarla**: the opener's TV wall as a scaled front elevation (SVG, 1 unit = 1 cm, drawn in
  `arkhera.html`) and a material board, both drawn from the options: width 180–440 cm, body, centre
  panel, metal, LED. Material changes wipe in behind the opener's brass line; width changes ease.
  On phones and tablets the drawing stays pinned above the options. The "Örnek uygulama" tab shows
  the real photo (`img/tasarla.webp`, from `tools/stills.py`). "Teklif al" opens WhatsApp with the choice.
- Material samples (`img/mat/`, `tools/materials.py`): oak veneer from Poly Haven (oak_veneer_01,
  CC0), also mapped to walnut tones; Calacatta and travertine are generated.
- "İç mimari proje ve 3D tasarım" shows the white model and the finished room split down the middle
  (`img/render-split.webp`, `tools/stills.py`).
- Contact form writes a WhatsApp message (no server).

## Build and preview

```bash
py -3 tools/instagram.py      # only after changing photos (needs instagram-raw/)
py -3 tools/build.py [https://site-url]
node tools/serve.js           # dist/ on http://localhost:5521
```

`arkhera.html` has no `<html>`/`<head>`: the claude.ai artifact wraps it itself, and `build.py`
wraps it for the real site (favicon, share image, canonical/og URLs with a site URL).

## Content sources

- Bio, services, phone numbers, project names, places and descriptions: Arkhera's Instagram
  profile and captions (October 2026).
- Project photos: 640 px thumbnails of their own posts (`instagram-raw/`, kept out of git), each
  card links to the original post. They are renders/photos the company published.

## Before going live

- Ask Arkhera for full-resolution project images and a vector logo (the mark in the header is
  redrawn from the 150 px profile picture).
- Confirm: which number is on WhatsApp (assumed 0555 752 47 19, the one most captions give),
  that 0531 837 56 06 is the office line, the "ücretsiz keşif ve metraj" offer, and the service area.
- The unit dimensions are illustrative (270 cm high, cabinet 32 × 42 cm, a drawer per ~60 cm).
