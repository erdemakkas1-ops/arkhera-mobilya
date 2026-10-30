# Açılış filmi için Gemini görselleri

Açılış, aynı odanın aynı kameradan çekilmiş 4 karesiyle oynuyor. Kaydırdıkça sırayla:

| Sıra | Dosya adı | Ne görünüyor | Geçiş |
|---|---|---|---|
| 1 | `1-kesif` | Boş, sıvasız oda | Açılış karesi |
| 2 | `2-proje` | Aynı oda, beyaz 3D maket | Yumuşak geçişle gelir |
| 3 | `3-uretim` | Bitmiş salon, gündüz | Sağdan sola pirinç bir tarama çizgisiyle açılır |
| 4 | `4-teslim` | Aynı salon, akşam, LED'ler yanık | Yumuşak geçişle gelir |

Geçişlerin çalışması için **4 karede de kamera, pencere, tavan ve duvarlar aynı yerde** olmalı.
Bunu sağlamanın yolu: önce 3. kareyi üret, diğer üçünü **o görseli Gemini'de düzenleterek** yap
(yeni görsel ürettirme; aksi halde oda her seferinde değişir).

## Sıra ve promptlar

İngilizce prompt Gemini'de daha tutarlı çalışıyor. Görsel oranını **16:9 (yatay)** seç.

**1) Önce `3-uretim` (bitmiş salon, gündüz)**
İstersen Arkhera'nın İncek salonu paylaşımını referans görsel olarak ekle; sonuç onların işine benzer.

> Photorealistic interior photograph of a modern luxury living room in an Ankara apartment, eye-level camera at 1.5 m standing in the back corner, 24 mm lens, 16:9. Centre-right: a full-height TV wall with vertical walnut wood slats, a central Calacatta marble panel with thin brass edges, a wall-mounted TV and a long floating walnut cabinet with handle-less doors and a hidden LED strip underneath. Left: floor-to-ceiling black-framed windows with sheer white curtains and a city view. Foreground: cream bouclé L-shaped sofa, round travertine coffee table on a walnut base, beige rug, chevron oak parquet. Dropped ceiling with a perimeter cove. Soft natural daylight, warm neutral palette of cream, walnut and brass. Architectural photography, no people, no text, no logos.

**2) `4-teslim`** — 3. görseli yükle ve şunu yaz:

> Edit this image. Keep the same room, the same camera angle and every object exactly where it is. Change the time to dusk: purple-orange sky with lit city windows outside, warm hidden LED light glowing along the ceiling cove and under the floating cabinet, a warm lamp on. Cosy evening mood, photorealistic.

**3) `2-proje`** — yine 3. görseli yükle:

> Edit this image. Keep the same room, the same camera angle and the same shapes. Turn everything into an untextured white clay architectural 3D model: furniture, walls, floor and ceiling all in matte white and light grey, no materials or colours, soft shadows. The window stays bright. It should look like an architect's white massing model render.

**4) `1-kesif`** — yine 3. görseli yükle:

> Edit this image. Keep the same camera angle, the same window and the same ceiling shape. Remove all furniture, curtains, the TV and all wall finishes: an empty unfinished room with raw grey plastered walls, a bare concrete floor and daylight through the window. Add a laser level on a tripod projecting a thin red line across the walls, and a tape measure on the floor.

Sonucu 3. kareyle üst üste koyup hızlıca karşılaştır: pencere ve tavan kayıyorsa o kareyi yeniden düzenlet.

## Telefon için (isteğe bağlı ama önerilir)

Telefonda ekran dikey olduğu için yatay görselin ortası kesilir. Daha iyi sonuç için: 3. görseli
**9:16 (dikey)** olarak genişlettir (*"Extend this image to a vertical 9:16 frame, keep the TV wall
centred"*), sonra aynı 3 düzenlemeyi bu dikey görsel üzerinde tekrarla. Adlar: `1-kesif-m`,
`2-proje-m`, `3-uretim-m`, `4-teslim-m`. Yapmazsan telefon karesi yatay görselin ortasından kesilir.

## Teslim

Görselleri (png, jpg ya da webp) proje içindeki `gemini/` klasörüne yukarıdaki adlarla koy. Sonra:

```bash
py -3 tools/keyframes.py
```

Bu komut görselleri 1920 × 1080 ve 1080 × 1920 WebP'ye çevirip `img/film/` altına yazar. Etiketlerin
(“Ceviz çıta panel”, “Gizli LED tavan” vb.) yerleri yeni görsele göre `arkhera.html` içindeki
`data-d` / `data-m` değerlerinden ayarlanır.
