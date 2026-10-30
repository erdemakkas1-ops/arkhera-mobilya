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

- The frames are Gemini images (see `GEMINI.md` for the prompts and order). Until they arrive,
  placeholders rendered from the earlier three.js scene (commit bc9c9c6) fill `img/film/`.
  `py -3 tools/keyframes.py [folder]` crops and converts a set (default folder `gemini/`).
- The whole stage pushes in slightly (scale 1.07 → 1). Chapter captions use `data-from`/`data-to`
  in film seconds; annotation tags use `data-d` / `data-m`, a point on the desktop / phone image as
  fractions of its width and height. Re-place them when the images change.
- No WebGL in the opener: three.js loads only when the configurator is ~600 px away.
- `prefers-reduced-motion`, no JS, or `?still` show the dusk frame and the four chapters as text.

## Other sections

- Stüdyo, Projeler (sideways scroll on wide screens with a mouse, native swipe elsewhere),
  Hizmetler (the row in the middle of the screen lights up and swaps the picture).
- **Ünite tasarla**: the opener's TV unit in 3D (`buildWallUnit`) with width 180–440 cm,
  body, centre panel, metal and LED options. "Teklif al" opens WhatsApp with the configuration.
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
- The configurator dimensions are illustrative (cabinet 36 × 42 cm, 262 cm height).
