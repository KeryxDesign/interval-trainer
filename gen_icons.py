#!/usr/bin/env python3
"""Icona Huermony: occhio (vista) + nota da ottavo come pupilla (udito),
monocromo bianco su fondo blu. Richiede Pillow."""
import math
from PIL import Image, ImageDraw, ImageChops

BLUE = (37, 99, 235)     # blu brand
WHITE = (255, 255, 255)

def render(size, ss=4):
    S = size * ss
    img = Image.new("RGB", (S, S), BLUE)
    d = ImageDraw.Draw(img)
    cx = cy = S / 2.0
    stroke = S * 0.034

    # --- occhio a mandorla: intersezione di due cerchi (contorno bianco) ---
    eye_w = S * 0.84
    lens_r = eye_w * 0.62
    off = math.sqrt(max(lens_r**2 - (eye_w/2)**2, 0))
    top_c = (cx, cy - lens_r + off)
    bot_c = (cx, cy + lens_r - off)
    def lens_mask(scale):
        rr = lens_r * scale
        tc = (cx, cy - rr + math.sqrt(max(rr**2-(eye_w*scale/2)**2,0)))
        bc = (cx, cy + rr - math.sqrt(max(rr**2-(eye_w*scale/2)**2,0)))
        ma = Image.new("L",(S,S),0); ImageDraw.Draw(ma).ellipse([tc[0]-rr,tc[1]-rr,tc[0]+rr,tc[1]+rr],fill=255)
        mb = Image.new("L",(S,S),0); ImageDraw.Draw(mb).ellipse([bc[0]-rr,bc[1]-rr,bc[0]+rr,bc[1]+rr],fill=255)
        return ImageChops.darker(ma,mb)
    outer = lens_mask(1.0)
    inner = lens_mask(1.0 - stroke/lens_r*2.0)
    ring = ImageChops.subtract(outer, inner)
    wimg = Image.new("RGB",(S,S),WHITE)
    img.paste(wimg, (0,0), ring)

    # --- iride: cerchio bianco di contorno ---
    ir = eye_w * 0.30
    bbox=[cx-ir,cy-ir,cx+ir,cy+ir]
    d.ellipse(bbox, outline=WHITE, width=int(stroke*0.8))

    # --- nota da ottavo bianca come pupilla ---
    nh = ir * 0.40
    head = (cx - ir*0.20, cy + ir*0.30)
    htmp = Image.new("RGBA",(S,S),(0,0,0,0))
    ImageDraw.Draw(htmp).ellipse([head[0]-nh*1.15,head[1]-nh*0.82,head[0]+nh*1.15,head[1]+nh*0.82], fill=WHITE+(255,))
    htmp = htmp.rotate(20, center=head, resample=Image.BICUBIC)
    img.paste(htmp,(0,0),htmp)
    stem_x = head[0] + nh*1.02
    stem_top = cy - ir*0.58
    d.rectangle([stem_x-ir*0.075, stem_top, stem_x+ir*0.075, head[1]], fill=WHITE)
    d.polygon([(stem_x+ir*0.05, stem_top),
               (stem_x+ir*0.05, stem_top+ir*0.46),
               (stem_x+ir*0.44, stem_top+ir*0.30),
               (stem_x+ir*0.42, stem_top+ir*0.02)], fill=WHITE)

    return img.resize((size,size), Image.LANCZOS)

for name,size in [("icon-512.png",512),("icon-192.png",192),("apple-touch-icon.png",180)]:
    render(size).save(name)
    print(name,"ok")
