#!/usr/bin/env python3
"""Regenera los 4 wallpapers: borra el bloque de texto original, lo vuelve a pegar
mas a la derecha (libre del dock en pantallas 16:10 o 4:3) y agrega el escudo encima.
Uso: python tools/gen-wallpapers.py  (requiere numpy, opencv-python-headless, Pillow, rsvg-convert)"""
import io, subprocess
import numpy as np, cv2
from PIL import Image, ImageFilter

SRC = "assets/wallpapers-src/Maospix%s.png"
DST = "archiso/airootfs/usr/share/wallpapers/Maospix%s/contents/images/1920x1080.png"
SHIELD = "assets/logo/maospix-escudo.svg"
BOX = (80, 390, 800, 780)          # x0, y0, x1, y1 del bloque de texto con su brillo
BOX_MAIN_X1 = 758                  # en el principal, las lineas del gato empiezan en x=745
SCALE, NEWX, NEWY = 0.72, 215, 490  # tamaño y posicion nuevos del bloque
SH_H, SH_Y = 190, 255              # alto y posicion del escudo


def low_fill(a, robust=False):
    """Fondo suave sin texto: por cada fila se interpola entre los bordes limpios del bloque."""
    x0, y0, x1, y1 = BOX
    f = cv2.GaussianBlur(a, (0, 0), 3).astype(np.float32)
    left = f[y0:y1, x0 - 14:x0 - 4].mean(1, keepdims=True)
    right = f[y0:y1, x1 + 4:x1 + 14].mean(1, keepdims=True)
    if robust:  # el borde derecho tiene detalles (lineas del gato): se usa la diferencia mediana
        right = left + np.median(right - left, axis=0, keepdims=True)
    t = np.linspace(0, 1, x1 - x0, dtype=np.float32)[None, :, None]
    fill = left * (1 - t) + right * t
    # suaviza verticalmente para que no queden rayas por el ruido de cada fila
    return cv2.GaussianBlur(fill, (0, 0), sigmaX=0.1, sigmaY=6)


def clean(a, grid):
    x0, y0, x1, y1 = BOX
    fill = low_fill(a, robust=not grid)
    if grid:
        # cuadricula de 80 px: se copia el detalle fino de un parche con la misma fase
        hf = a.astype(np.float32) - cv2.GaussianBlur(a, (0, 0), 6).astype(np.float32)
        mid = 590
        det = np.concatenate([hf[y0 - 320:mid - 320, x0:x1], hf[mid + 240:y1 + 240, x0:x1]])
        fill = fill + det
    # bordes suaves para que el parche no se note; el texto original siempre se reemplaza
    m = np.ones((y1 - y0, x1 - x0), np.float32)
    ramp = np.linspace(0, 1, 40, dtype=np.float32)
    m[:, :40] *= ramp
    r = 40 if grid else 60
    m[:, -r:] *= np.linspace(1, 0, r, dtype=np.float32)
    if not grid:
        m[:40] *= ramp[:, None]
        m[-40:] *= ramp[::-1, None]
        reg = a[y0:y1, x0:x1].astype(np.float32)
        txt = ((reg - fill).sum(2) > 60).astype(np.uint8)
        txt = cv2.dilate(txt, np.ones((3, 3), np.uint8), iterations=10)
        txt = cv2.GaussianBlur(txt.astype(np.float32), (0, 0), 5)
        m = np.maximum(m, np.clip(txt * 1.5, 0, 1))
    m = m[..., None]
    out = a.copy().astype(np.float32)
    out[y0:y1, x0:x1] = fill * m + out[y0:y1, x0:x1] * (1 - m)
    return np.clip(out, 0, 255).astype(np.uint8)


def shield_img():
    png = subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", SHIELD], capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    return im.resize((round(im.width * SH_H / im.height), SH_H), Image.LANCZOS)


def build(name, grid):
    global BOX
    BOX = (80, 390, 800 if grid else BOX_MAIN_X1, 780)
    orig = np.array(Image.open(SRC % name).convert("RGB"))
    clean_img = clean(orig, grid)
    x0, y0, x1, y1 = BOX
    delta = orig[y0:y1, x0:x1].astype(np.int16) - clean_img[y0:y1, x0:x1].astype(np.int16)
    w, h = round((x1 - x0) * SCALE), round((y1 - y0) * SCALE)
    delta = cv2.resize(delta.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
    out = clean_img.astype(np.float32)
    out[NEWY:NEWY + h, NEWX:NEWX + w] += delta
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    sh = shield_img()
    sx = NEWX + round((140 - x0 + 80) * 0) + 40   # alineado con el borde del texto
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow.paste(sh, (sx, SH_Y), sh)
    g = glow.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img.convert("RGBA"), g)
    img = Image.alpha_composite(img, glow)
    img.convert("RGB").save(DST % name, optimize=True)


if __name__ == "__main__":
    build("", False)
    for n in ("-Nord", "-Grafito", "-Negro"):
        build(n, True)
