#!/usr/bin/env python3
"""Convierte un .md simple (titulos, listas, bloques con 4 espacios, tablas) a PDF con reportlab.
Uso: python tools/md2pdf.py docs/HISTORIA.md docs/Maospix-KDE-historia.pdf "Titulo" """
import re, sys, textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, ListFlowable, ListItem

src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Documento"
ss = getSampleStyleSheet()
B = ParagraphStyle('b', parent=ss['BodyText'], fontSize=10, leading=14)
H1 = ParagraphStyle('h1', parent=ss['Title'], fontSize=20, textColor=colors.HexColor('#2E3440'))
H2 = ParagraphStyle('h2', parent=ss['Heading1'], fontSize=15, textColor=colors.HexColor('#5E81AC'), spaceBefore=14)
H3 = ParagraphStyle('h3', parent=ss['Heading2'], fontSize=12, textColor=colors.HexColor('#2E3440'), spaceBefore=8)
C = ParagraphStyle('c', fontName='Courier', fontSize=8.5, leading=11, backColor=colors.HexColor('#ECEFF4'), leftIndent=6, borderPadding=4)
T = ParagraphStyle('t', parent=B, fontSize=8, leading=10)


def inl(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', s)


def wrap(line, width=96):
    ind = len(line) - len(line.lstrip())
    return textwrap.fill(line, width, subsequent_indent=' ' * (ind + 2), break_long_words=True) if len(line) > width else line


lines = open(src, encoding='utf-8').read().split('\n')
out, i = [], 0
while i < len(lines):
    l = lines[i]
    if l.startswith('# '):
        out.append(Paragraph(inl(l[2:]), H1))
    elif l.startswith('## '):
        out.append(Paragraph(inl(l[3:]), H2))
    elif l.startswith('### '):
        out.append(Paragraph(inl(l[4:]), H3))
    elif l.startswith('    '):
        blk = []
        while i < len(lines) and (lines[i].startswith('    ') or (not lines[i].strip() and i + 1 < len(lines) and lines[i + 1].startswith('    '))):
            blk.append(wrap(lines[i][4:]))
            i += 1
        out.append(Preformatted('\n'.join(blk), C))
        out.append(Spacer(1, 6))
        continue
    elif l.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            if not re.match(r'^\|[-| ]+\|$', lines[i]):
                rows.append([Paragraph(inl(c.strip()), T) for c in lines[i].strip('|').split('|')])
            i += 1
        t = Table(rows, colWidths=[5 * cm, 5.5 * cm, 6 * cm], repeatRows=1)
        t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D8DEE9')), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        out += [t, Spacer(1, 6)]
        continue
    elif re.match(r'^(- |\d+\. )', l):
        num = l[0].isdigit()
        items = []
        while i < len(lines) and re.match(r'^(- |\d+\. )', lines[i]):
            items.append(ListItem(Paragraph(inl(re.sub(r'^(- |\d+\. )', '', lines[i])), B)))
            i += 1
        out.append(ListFlowable(items, bulletType='1' if num else 'bullet', leftIndent=14))
        continue
    elif l.strip():
        out.append(Paragraph(inl(l), B))
    i += 1
SimpleDocTemplate(dst, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, title=title, author='Marcos Olmedo').build(out)
