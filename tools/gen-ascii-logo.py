#!/usr/bin/env python3
"""Genera el logo de fastfetch en texto (estilo Arch) a partir del escudo SVG.
Cada trazo se dibuja con / \\ | - _ segun su direccion. Colores: $1 borde, $2 gatito, $3 ojos/V, $4 nariz/boca.
Uso: python tools/gen-ascii-logo.py   (requiere numpy, Pillow, rsvg-convert)"""
import io, math, re, subprocess
import numpy as np
from PIL import Image

OUT = "archiso/airootfs/usr/share/maospix/fastfetch-logo.txt"
ROWS, CW, CH = 24, 8, 16
VB = (70, 24, 372, 468)          # x, y, ancho, alto del recuadro del escudo en el SVG
COLS = round(ROWS * CH * VB[2] / VB[3] / CW)
W, H = COLS * CW, ROWS * CH

LAYERS = [  # (color, trazos del SVG)  de mayor a menor prioridad
    (4, ['<path d="m239 316 17 12 17-12" stroke-width="11"/>']),
    (3, ['<path d="M197 264 223 281 191 288 M315 264 289 281 321 288" stroke-width="12"/>',
         '<path d="M205 213 256 257 307 213" stroke-width="15"/>']),
    (2, ['<path d="M149 214 147 139 207 177 Q255 161 305 177 L365 139 363 215 Q378 259 351 322 Q330 364 256 378 Q182 364 161 322 Q134 259 149 214Z" stroke-width="12"/>']),
    (1, ['<path d="M256 37 428 113v156q-4 129-172 210Q88 398 84 269V113Z" stroke-width="14"/>']),
]


def thin(p):
    """Trazo fino (≈0.55 de ancho) para que cada linea ocupe una sola letra."""
    return re.sub(r'stroke-width="(\d+)"', lambda m: 'stroke-width="%d"' % round(int(m.group(1)) * 0.55), p)


def render(paths):
    paths = [thin(p) for p in paths]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%d %d %d %d" width="%d" height="%d">'
           '<g fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
           % (*VB, W, H, "".join(paths)))
    png = subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H)], input=svg.encode(), capture_output=True, check=True).stdout
    return np.array(Image.open(io.BytesIO(png)).convert("RGBA").getchannel("A"), dtype=np.float32) / 255


def glyph(cell):
    cov = cell.mean()
    if cov < 0.18:
        return None
    ys, xs = np.mgrid[0:CH, 0:CW]
    m = cell.sum()
    cx, cy = (cell * xs).sum() / m, (cell * ys).sum() / m
    # los pixeles de la celda son 1:2, se corrige para medir el angulo en proporcion real
    dx, dy = (xs - cx), (ys - cy)
    cxx, cyy, cxy = (cell * dx * dx).sum() / m, (cell * dy * dy).sum() / m, (cell * dx * dy).sum() / m
    ang = math.degrees(0.5 * math.atan2(2 * cxy, cxx - cyy))   # 0 horizontal, 90 vertical, y hacia abajo
    if cov < 0.30 and abs(abs(ang) - 45) > 20:
        return "'" if cy < CH / 2 else "."
    a = abs(ang)
    if a < 25:
        return "-" if abs(cy - CH / 2) < 4 else ("'" if cy < CH / 2 else "_")
    if a > 65:
        return "|"
    return "\\" if ang > 0 else "/"


# Gatito dibujado a mano (22 de ancho). Contorno en $2; la "V" y los ojos en $3; la boca en $4.
CAT = [
    ' /\\                /\\ ',
    '/  \\              /  \\',
    '|   \\____________/   |',
    '|       \\    /       |',
    '|  >-    \\  /    -<  |',
    '|         \\/         |',
    '|                    |',
    ' \\        vv        / ',
    '  \\________________/  ',
]
CAT_W = 22
assert all(len(_r) == CAT_W for _r in CAT)


def cat_color(i, j, ch):
    if ch == "v":
        return 4
    if (i, j) in {(4, 3), (4, 4), (4, 17), (4, 18)} or (i in (3, 4, 5) and 8 <= j <= 13 and ch in "\\/"):
        return 3
    return 2


def main():
    grid = [[None] * COLS for _ in range(ROWS)]
    a = render(LAYERS[-1][1])                  # solo el escudo, el gatito va a mano
    for r in range(ROWS):
        for c in range(COLS):
            g = glyph(a[r * CH:(r + 1) * CH, c * CW:(c + 1) * CW])
            if g:
                grid[r][c] = "$1" + g
    r0, c0 = 7, (COLS - CAT_W) // 2
    for i, row in enumerate(CAT):
        for j, ch in enumerate(row):
            grid[r0 + i][c0 + j] = ("$%d%s" % (cat_color(i, j, ch), ch)) if ch != " " else None
    lines = ["".join(x or " " for x in row).rstrip() for row in grid]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("\n".join(re.sub(r"\$\d", "", l) for l in lines))


main()
