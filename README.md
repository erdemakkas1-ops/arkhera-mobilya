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

A live three.js (r180, from jsDelivr) living room built in code inside `arkhera.html`. It tells
Arkhera's own process in four chapters:

1. **Keşif & metraj** — top-down floor plan; walls and dimensions plot in on load, furniture
   footprints draw as you scroll.
2. **Proje & 3D** — the camera tilts down into the room while everything extrudes out of the plan
   as a white clay model (a clipping plane rising in Y).
3. **Özel üretim** — a scan line sweeps right to left, turning clay into finished materials
   (walnut slats, Calacatta marble, travertine, bouclé, chevron oak). Annotations name the parts.
4. **Anahtar teslim** — daylight turns to dusk, the hidden LED ceiling, unit LEDs and the arc lamp
   come on; closing call to action.

- Scroll position → film seconds 0–12; the film eases towards the scroll target and only renders
  when something changed. Chapter captions use `data-from`/`data-to` in film seconds; annotation
  tags use `data-at` (a 3D point in metres).
- Materials are procedural canvas textures (no image downloads). Phones get pixel ratio 1.25 and
  a 1024 shadow map.
- `prefers-reduced-motion`, no WebGL2, or `?still` show a still closing frame and the four chapters
  as text; three.js still loads for the configurator only.
- `?capture` hides the overlays and exposes `__film.seek(t)`. Posters in `img/` (`film-poster*.webp`,
  `film-still.webp`, `render-split.webp`) are captures: screenshot into `tools/frames/` as described in
  `tools/posters.py`, then run it. Re-capture after changing the scene.

## Other sections

- Stüdyo, Projeler (sideways scroll on wide screens with a mouse, native swipe elsewhere),
  Hizmetler (the row in the middle of the screen lights up and swaps the picture).
- **Ünite tasarla**: the film's TV unit (`buildWallUnit`, shared with the film) with width 180–440 cm,
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
