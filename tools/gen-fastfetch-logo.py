#!/usr/bin/env python3
"""Genera fastfetch-logo.ans (half-blocks truecolor, 40x20) desde maospix-logo.svg.
Uso: python tools/gen-fastfetch-logo.py  (requiere rsvg-convert y Pillow)"""
import subprocess, io
from PIL import Image
R = "archiso/airootfs/usr/share/maospix/"
png = subprocess.run(["rsvg-convert", "-w", "320", "-h", "320", R + "maospix-logo.svg"],
                     capture_output=True, check=True).stdout
img = Image.open(io.BytesIO(png)).convert("RGBA").resize((40, 40), Image.BOX)
px = img.load()
def get(x, y):
    r, g, b, a = px[x, y]
    return (r, g, b) if a >= 128 else None
out = []
for y in range(0, 40, 2):
    row = ""
    for x in range(40):
        t, b = get(x, y), get(x, y + 1)
        if t and b:
            row += "\x1b[38;2;%d;%d;%dm\x1b[48;2;%d;%d;%dm▀\x1b[0m" % (*t, *b)
        elif t:
            row += "\x1b[38;2;%d;%d;%dm▀\x1b[0m" % t
        elif b:
            row += "\x1b[38;2;%d;%d;%dm▄\x1b[0m" % b
        else:
            row += " "
    out.append(row)
open(R + "fastfetch-logo.ans", "w").write("\n".join(out) + "\n")
