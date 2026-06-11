#!/usr/bin/env python3
"""Icona Huermony: occhio (vista) con iride a 12 colori (spettro) e una nota
da ottavo come pupilla (udito). Vista + suono = sinestesia. Richiede Pillow."""
import colorsys, math
from PIL import Image, ImageDraw

HUES = [(0,75,48),(22,85,45),(40,90,43),(55,75,41),(78,60,42),(135,55,36),
        (172,80,32),(196,85,38),(222,70,50),(252,58,56),(285,55,49),(320,70,48)]
BG = (20, 21, 26)
DARK = (16, 17, 22)

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return (int(r*255), int(g*255), int(b*255))

COLS = [hsl(*x) for x in HUES]

def render(size, ss=4):
    S = size * ss
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    cx = cy = S / 2.0

    # --- occhio a mandorla: intersezione di due cerchi (sopra e sotto) ---
    eye_w = S * 0.86
    lens_r = eye_w * 0.62          # raggio dei due cerchi
    off = math.sqrt(max(lens_r**2 - (eye_w/2)**2, 0))  # curvatura verticale
    top_c = (cx, cy - lens_r + off)
    bot_c = (cx, cy + lens_r - off)
    ma = Image.new("L", (S, S), 0); ImageDraw.Draw(ma).ellipse(
        [top_c[0]-lens_r, top_c[1]-lens_r, top_c[0]+lens_r, top_c[1]+lens_r], fill=255)
    mb = Image.new("L", (S, S), 0); ImageDraw.Draw(mb).ellipse(
        [bot_c[0]-lens_r, bot_c[1]-lens_r, bot_c[0]+lens_r, bot_c[1]+lens_r], fill=255)
    from PIL import ImageChops
    lens = ImageChops.darker(ma, mb)            # bianco solo dove dentro entrambi

    # sclera (bianco dell'occhio)
    white = Image.new("RGB", (S, S), (236, 238, 242))
    img.paste(white, (0, 0), lens)

    # --- iride: 12 spicchi di spettro ---
    ir = eye_w * 0.30
    iris = Image.new("RGB", (S, S), BG)
    di = ImageDraw.Draw(iris)
    bbox = [cx-ir, cy-ir, cx+ir, cy+ir]
    for k in range(12):
        a0 = -90 + k*30 - 0.5
        di.pieslice(bbox, a0, a0+31, fill=COLS[k])
    irism = Image.new("L", (S, S), 0)
    ImageDraw.Draw(irism).ellipse(bbox, fill=255)
    irism = ImageChops.darker(irism, lens)      # iride tagliata dalle palpebre
    img.paste(iris, (0, 0), irism)

    # anello scuro sottile attorno all'iride
    d.ellipse(bbox, outline=DARK, width=max(2, int(S*0.006)))

    # --- nota da ottavo come pupilla (scura) ---
    nh = ir * 0.42                              # raggio testa nota
    head = (cx - ir*0.22, cy + ir*0.28)
    # testa (ellisse leggermente inclinata)
    htmp = Image.new("RGBA", (S, S), (0,0,0,0))
    ImageDraw.Draw(htmp).ellipse(
        [head[0]-nh*1.15, head[1]-nh*0.82, head[0]+nh*1.15, head[1]+nh*0.82], fill=DARK+(255,))
    htmp = htmp.rotate(20, center=head, resample=Image.BICUBIC)
    img.paste(htmp, (0,0), htmp)
    # gambo
    stem_x = head[0] + nh*1.02
    stem_top = cy - ir*0.62
    d.rectangle([stem_x-ir*0.07, stem_top, stem_x+ir*0.07, head[1]], fill=DARK)
    # bandierina
    d.polygon([(stem_x+ir*0.05, stem_top),
               (stem_x+ir*0.05, stem_top+ir*0.46),
               (stem_x+ir*0.42, stem_top+ir*0.30),
               (stem_x+ir*0.40, stem_top+ir*0.02)], fill=DARK)

    return img.resize((size, size), Image.LANCZOS)

for name, size in [("icon-512.png",512), ("icon-192.png",192), ("apple-touch-icon.png",180)]:
    render(size).save(name)
    print(name, "ok")
