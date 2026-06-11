#!/usr/bin/env python3
"""Genera le icone PWA di Huermony: anello dei 12 colori su sfondo scuro. Solo stdlib."""
import zlib, struct, math, colorsys

HUES = [(0,75,48),(22,85,45),(40,90,43),(55,75,41),(78,60,42),(135,55,36),
        (172,80,32),(196,85,38),(222,70,50),(252,58,56),(285,55,49),(320,70,48)]
BG = (20, 21, 26)

def hsl_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return (int(r*255), int(g*255), int(b*255))

DOTS = [hsl_rgb(*x) for x in HUES]

def render(size):
    cx = cy = size / 2.0
    ring = size * 0.30
    rad = size * 0.062
    centers = []
    for k in range(12):
        a = math.radians(-90 + k * 30)
        centers.append((cx + ring * math.cos(a), cy + ring * math.sin(a)))
    rows = []
    for y in range(size):
        row = bytearray()
        row.append(0)
        for x in range(size):
            px = list(BG)
            for (dx, dy), col in zip(centers, DOTS):
                d = math.hypot(x + 0.5 - dx, y + 0.5 - dy)
                if d < rad + 1.0:
                    cov = min(1.0, max(0.0, rad + 0.5 - d))
                    px = [int(c * cov + b * (1 - cov)) for c, b in zip(col, px)]
                    break
            row += bytes(px)
        rows.append(bytes(row))
    raw = b"".join(rows)
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

for name, size in [("icon-512.png", 512), ("icon-192.png", 192), ("apple-touch-icon.png", 180)]:
    with open(name, "wb") as f:
        f.write(render(size))
    print(name, "ok")
