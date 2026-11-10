#!/usr/bin/env python3
"""Erzeugt die Grafiken und die Walk-Box-Datei für den Strand von Ape Island.

Alles wird prozedural gezeichnet, damit die Assets reproduzierbar bleiben.
Aufruf:  python3 game/tools/gen_assets.py <pfad/zu/scummc/examples/road>

Übernommen aus dem road-Beispiel (GPL, Alban Bedel) werden die Schriften
vera*.bmp, der Cursor und der Teufel-Costume (devil.scost + devil/).
In vera.bmp hat der Rahmen um die Glyphe "µ" einen Knick, den ScummCs
char-Tool als zusätzliche (leere) Glyphe zählt - dadurch wären alle Zeichen
ab "Æ" um eins verschoben (ß würde als Þ erscheinen). Das wird hier repariert.

Die Raumpalette übernimmt die Einträge 0-79 und 192-255 aus dem Road-Beispiel
von ScummC: dort liegen die Farben, die der Teufel-Costume (16-47), der
Cursor und die GUI (VAR_GUI_COLORS) verwenden. Unsere eigenen Farben belegen
die Indizes 80-191.

Ergebnis (in game/assets/):
  beach.bmp          Hintergrund 320x144
  beach.box          Walk-Box (ein großes Rechteck über den Sand)
  nut_top.bmp        Palmkrone ohne lose Kokosnuss (Objektzustand nach dem Fall)
  nut_ground.bmp     Kokosnuss im Sand
  chest_closed.bmp   Truhe zu
  chest_open.bmp     Truhe offen mit Gold
  monkey_angry.bmp   Affe bewacht die Truhe
  monkey_happy.bmp   Affe sitzt und futtert
  inv_coconut.bmp    Inventar-Icon 40x16
"""
import math
import os
import shutil
import struct
import sys

from PIL import Image, ImageDraw

W, H = 320, 144
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# --- Palette ---------------------------------------------------------------
C = {}
_own = []


def col(name, rgb):
    C[name] = 80 + len(_own)
    _own.append(rgb)


for i in range(8):  # Himmel: oben tiefblau, zum Horizont hell
    t = i / 7
    col(f"sky{i}", (int(40 + 120 * t), int(90 + 120 * t), int(190 + 55 * t)))
col("sun", (255, 230, 90))
col("sun2", (255, 250, 180))
col("cloud", (250, 250, 255))
col("cloud2", (205, 220, 240))
col("sea0", (20, 70, 140))
col("sea1", (30, 110, 170))
col("sea2", (60, 160, 200))
col("foam", (225, 245, 250))
col("isle", (60, 100, 110))
col("sand0", (240, 215, 150))
col("sand1", (225, 195, 125))
col("sand2", (200, 165, 100))
col("wet", (190, 160, 110))
col("trunk0", (90, 55, 25))
col("trunk1", (140, 90, 45))
col("trunk2", (180, 125, 70))
col("leaf0", (20, 90, 30))
col("leaf1", (40, 140, 45))
col("leaf2", (110, 195, 70))
col("nut0", (70, 40, 20))
col("nut1", (120, 75, 35))
col("rock0", (90, 90, 95))
col("rock1", (135, 135, 140))
col("fur0", (60, 35, 20))
col("fur1", (105, 65, 35))
col("face", (215, 170, 120))
col("eye", (15, 10, 10))
col("mouth", (190, 40, 40))
col("white", (255, 255, 255))
col("wood0", (80, 45, 20))
col("wood1", (135, 80, 35))
col("gold0", (170, 120, 20))
col("gold1", (230, 185, 40))
col("gold2", (255, 240, 140))
col("shadow", (185, 150, 95))
col("grass", (90, 150, 50))
assert 80 + len(_own) <= 192


def make_palette(road_bmp):
    base = Image.open(road_bmp).getpalette()
    pal = list(base[: 256 * 3])
    for i, rgb in enumerate(_own):
        pal[(80 + i) * 3: (80 + i) * 3 + 3] = list(rgb)
    return pal


# --- Zeichenhilfen ---------------------------------------------------------
def new(w, h, fill=0):
    im = Image.new("P", (w, h), fill)
    return im, ImageDraw.Draw(im)


def disc(d, x, y, r, c):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def draw_background(d, with_loose_nut=True):
    # Himmel
    for y in range(56):
        d.line([(0, y), (W - 1, y)], fill=C[f"sky{min(7, y * 8 // 56)}"])
    disc(d, 268, 22, 13, C["sun"])
    disc(d, 266, 20, 8, C["sun2"])
    for cx, cy in ((150, 14), (190, 26)):
        for dx, dy, r in ((0, 0, 7), (9, -3, 8), (18, 0, 6), (8, 3, 6)):
            disc(d, cx + dx, cy + dy, r, C["cloud"])
        d.line([(cx - 5, cy + 6), (cx + 23, cy + 6)], fill=C["cloud2"])
    # Meer mit ferner Insel
    d.rectangle([0, 56, W - 1, 80], fill=C["sea1"])
    d.polygon([(120, 57), (135, 50), (150, 48), (165, 52), (178, 57)], fill=C["isle"])
    d.rectangle([0, 56, W - 1, 58], fill=C["sea0"])
    for y in range(60, 80, 4):
        for x in range((y * 7) % 23, W, 23):
            d.line([(x, y), (x + 6, y)], fill=C["sea2"])
    # Brandung
    for x in range(0, W, 2):
        y = 80 + int(2 * math.sin(x / 9.0))
        d.line([(x, y - 1), (x + 1, y - 1)], fill=C["foam"])
    # Sand
    for y in range(81, H):
        for x in range(W):
            n = (x * 73 + y * 151 + (x * y) % 17) % 29
            if y < 87:
                c = C["wet"] if n > 3 else C["sand2"]
            else:
                c = C["sand0"] if n > 6 else (C["sand1"] if n > 1 else C["sand2"])
            d.point((x, y), fill=c)
    for x, y in ((12, 132), (110, 96), (300, 138), (180, 140)):
        for k in (-2, 0, 2):
            d.line([(x + k, y), (x + k * 2, y - 4)], fill=C["grass"])
    # Felsen hinter dem Affen
    d.polygon([(286, 112), (292, 96), (306, 90), (318, 98), (319, 116)], fill=C["rock0"])
    d.polygon([(292, 104), (298, 94), (308, 92), (314, 100)], fill=C["rock1"])
    # Palme: Stamm
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((52 + 20 * t + 7 * math.sin(math.pi * t), 116 - 86 * t))
    d.ellipse([38, 113, 70, 120], fill=C["shadow"])
    for i, (x, y) in enumerate(pts):
        r = 4.5 - 1.5 * i / 40
        c = C["trunk1"] if (i // 3) % 2 else C["trunk2"]
        d.ellipse([x - r, y - 1.5, x + r, y + 1.5], fill=c)
        d.point((int(x - r), int(y)), fill=C["trunk0"])
    # Palme: Wedel
    cx, cy = 74, 28
    for ang, ln, droop in ((-170, 30, 14), (-140, 24, 10), (-100, 18, 6), (-60, 22, 8),
                           (-20, 30, 13), (10, 26, 15), (160, 26, 15)):
        a = math.radians(ang)
        prev = (cx, cy)
        for s in range(1, ln + 1):
            t = s / ln
            x = cx + math.cos(a) * s
            y = cy + math.sin(a) * s + droop * t * t
            d.line([prev, (x, y)], fill=C["leaf1"], width=3)
            if s % 3 == 0:
                d.line([(x, y), (x + 2 * math.cos(a + 1.4), y + 4)], fill=C["leaf0"])
                d.line([(x, y), (x + 2 * math.cos(a - 1.4), y + 4)], fill=C["leaf0"])
            prev = (x, y)
        d.line([(cx, cy), prev], fill=C["leaf2"])
    # Kokosnüsse in der Krone (die rechte fällt später herunter)
    for nx in ((68, 76) if with_loose_nut else (68,)):
        disc(d, nx, 32, 3, C["nut0"])
        d.point((nx - 1, 31), fill=C["nut1"])


def draw_nut_ground(d):
    d.ellipse([43, 130, 54, 133], fill=C["shadow"])
    disc(d, 48, 128, 3, C["nut0"])
    d.point((47, 127), fill=C["nut1"])
    d.point((46, 128), fill=C["nut1"])


CHEST = (200, 92, 32, 32)  # x, y, w, h


def draw_chest(d, opened):
    x, y = CHEST[0], CHEST[1]
    d.ellipse([x - 2, y + 27, x + 33, y + 32], fill=C["shadow"])
    d.rectangle([x + 2, y + 14, x + 29, y + 29], fill=C["wood1"], outline=C["wood0"])
    for yy in (y + 19, y + 24):
        d.line([(x + 3, yy), (x + 28, yy)], fill=C["wood0"])
    if opened:
        d.rectangle([x + 3, y + 1, x + 28, y + 12], fill=C["wood0"], outline=C["wood0"])
        d.rectangle([x + 5, y + 3, x + 26, y + 11], fill=C["wood1"])
        for gx in range(x + 4, x + 28, 3):
            disc(d, gx, y + 14 + (gx % 2), 2, C["gold1"])
        for gx in (x + 8, x + 16, x + 23):
            d.point((gx, y + 12), fill=C["gold2"])
            d.line([(gx - 2, y + 10), (gx + 2, y + 10)], fill=C["gold2"])
    else:
        d.pieslice([x + 2, y + 6, x + 29, y + 22], 180, 360, fill=C["wood1"], outline=C["wood0"])
        d.line([(x + 2, y + 14), (x + 29, y + 14)], fill=C["wood0"])
    for bx in (x + 6, x + 25):
        d.line([(bx, y + 9 if not opened else y + 14), (bx, y + 29)], fill=C["gold0"])
    d.rectangle([x + 14, y + 14, x + 17, y + 18], fill=C["gold1"], outline=C["gold0"])


MONKEY = (248, 72, 40, 48)


def draw_monkey(d, happy):
    x, y = MONKEY[0], MONKEY[1]
    d.ellipse([x + 6, y + 43, x + 34, y + 47], fill=C["shadow"])
    if not happy:
        # steht aufrecht, Arme drohend erhoben
        d.line([(x + 30, y + 40), (x + 37, y + 36), (x + 36, y + 28)], fill=C["fur0"], width=2)
        d.ellipse([x + 12, y + 18, x + 28, y + 38], fill=C["fur1"], outline=C["fur0"])
        d.ellipse([x + 15, y + 24, x + 25, y + 35], fill=C["face"])
        d.line([(x + 15, y + 36), (x + 14, y + 45)], fill=C["fur0"], width=3)
        d.line([(x + 25, y + 36), (x + 26, y + 45)], fill=C["fur0"], width=3)
        d.line([(x + 13, y + 22), (x + 5, y + 14), (x + 4, y + 6)], fill=C["fur1"], width=3)
        d.line([(x + 27, y + 22), (x + 35, y + 14), (x + 36, y + 6)], fill=C["fur1"], width=3)
        hx, hy = x + 20, y + 11
        disc(d, hx, hy, 8, C["fur1"])
        disc(d, hx - 8, hy, 3, C["face"])
        disc(d, hx + 8, hy, 3, C["face"])
        d.ellipse([hx - 6, hy - 3, hx + 6, hy + 7], fill=C["face"])
        d.line([(hx - 5, hy - 3), (hx - 1, hy - 1)], fill=C["eye"])
        d.line([(hx + 5, hy - 3), (hx + 1, hy - 1)], fill=C["eye"])
        d.point((hx - 3, hy), fill=C["eye"])
        d.point((hx + 3, hy), fill=C["eye"])
        d.ellipse([hx - 3, hy + 3, hx + 3, hy + 6], fill=C["mouth"])
        d.line([(hx - 2, hy + 3), (hx + 2, hy + 3)], fill=C["white"])
    else:
        # sitzt zufrieden und hält die Kokosnuss
        d.line([(x + 30, y + 42), (x + 38, y + 40), (x + 38, y + 33), (x + 34, y + 32)],
               fill=C["fur0"], width=2)
        d.ellipse([x + 9, y + 24, x + 31, y + 45], fill=C["fur1"], outline=C["fur0"])
        d.ellipse([x + 14, y + 30, x + 26, y + 43], fill=C["face"])
        d.ellipse([x + 6, y + 39, x + 16, y + 45], fill=C["fur0"])
        d.ellipse([x + 24, y + 39, x + 34, y + 45], fill=C["fur0"])
        disc(d, x + 20, y + 29, 4, C["nut0"])
        d.point((x + 19, y + 27), fill=C["nut1"])
        d.line([(x + 11, y + 28), (x + 16, y + 30)], fill=C["fur1"], width=3)
        d.line([(x + 29, y + 28), (x + 24, y + 30)], fill=C["fur1"], width=3)
        hx, hy = x + 20, y + 17
        disc(d, hx, hy, 8, C["fur1"])
        disc(d, hx - 8, hy, 3, C["face"])
        disc(d, hx + 8, hy, 3, C["face"])
        d.ellipse([hx - 6, hy - 3, hx + 6, hy + 7], fill=C["face"])
        d.line([(hx - 4, hy - 1), (hx - 2, hy - 2)], fill=C["eye"])
        d.line([(hx + 2, hy - 2), (hx + 4, hy - 1)], fill=C["eye"])
        d.arc([hx - 4, hy + 1, hx + 4, hy + 6], 20, 160, fill=C["eye"])


def crop(im, rect, path, pal):
    x, y, w, h = rect
    o = im.crop((x, y, x + w, y + h))
    o.putpalette(pal)
    o.save(path)


def write_box(path, boxes):
    """boxd-Datei im Format von ScummCs boxedit (benannt, mit BOXM und SCAL)."""
    body = b""
    for name, pts in boxes:
        nm = name.encode()
        body += bytes([len(nm)]) + nm
        for px, py in pts:  # ul, ur, lr, ll
            body += struct.pack("<hh", px, py)
        body += struct.pack("<BBH", 0, 0, 255)  # mask, flags, scale
    data = b"boxd" + struct.pack(">I", 8 + len(body)) + body

    # Box 0 ist mit nichts verbunden. Bei nur rechteckigen, sich an Kanten
    # berührenden Boxen genügt hier die einfache Nachbarschaftsprüfung.
    n = len(boxes) + 1

    def neighbors(a, b):
        if not a or not b:
            return False
        (ax0, ay0), (ax1, _), (_, ay1), _ = boxes[a - 1][1]
        (bx0, by0), (bx1, _), (_, by1), _ = boxes[b - 1][1]
        if ax1 == bx0 or bx1 == ax0:
            return not (ay1 < by0 or by1 < ay0)
        if ay1 == by0 or by1 == ay0:
            return not (ax1 < bx0 or bx1 < ax0)
        return False

    dist = [[0 if i == j else (1 if neighbors(i, j) else 255) for j in range(n)] for i in range(n)]
    nxt = [[j if (i == j or dist[i][j] == 1) else 255 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    m = b""
    for i in range(n):
        m += b"\xff"
        j = 0
        while j < n:
            v = nxt[i][j]
            if v == 255:
                j += 1
                continue
            s = j
            while j + 1 < n and nxt[i][j + 1] == v:
                j += 1
            m += bytes([s, j, v])
            j += 1
    m += b"\xff"
    data += b"BOXM" + struct.pack(">I", 8 + len(m)) + m
    data += b"SCAL" + struct.pack(">I", 40) + bytes(32)
    with open(path, "wb") as f:
        f.write(data)


def copy_road_assets(road):
    for name in ("vera.bmp", "vera-gui.bmp", "vera-small.bmp", "cursor.bmp", "devil.scost"):
        shutil.copy(os.path.join(road, name), os.path.join(OUT, name))
    shutil.rmtree(os.path.join(OUT, "devil"), ignore_errors=True)
    shutil.copytree(os.path.join(road, "devil"), os.path.join(OUT, "devil"))

    font = Image.open(os.path.join(OUT, "vera.bmp"))
    px = font.load()
    if px[398, 176] == 4 and px[398, 177] == 4:  # Rahmenknick an der µ-Glyphe
        px[398, 176] = px[398, 177] = 0
    font.save(os.path.join(OUT, "vera.bmp"))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    road = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    copy_road_assets(road)
    pal = make_palette(os.path.join(road, "road.bmp"))

    bg, d = new(W, H)
    draw_background(d)
    draw_chest(d, opened=False)
    bg.putpalette(pal)
    bg.save(os.path.join(OUT, "beach.bmp"))

    # Objektbilder werden aus der fertig gezeichneten Szene ausgeschnitten,
    # damit sie nahtlos auf dem Hintergrund liegen.
    scene, d = new(W, H)
    draw_background(d, with_loose_nut=False)
    crop(scene, (64, 24, 16, 16), os.path.join(OUT, "nut_top.bmp"), pal)

    scene, d = new(W, H)
    draw_background(d)
    draw_nut_ground(d)
    crop(scene, (40, 120, 16, 16), os.path.join(OUT, "nut_ground.bmp"), pal)

    for opened, name in ((False, "chest_closed"), (True, "chest_open")):
        scene, d = new(W, H)
        draw_background(d)
        draw_chest(d, opened)
        crop(scene, CHEST, os.path.join(OUT, name + ".bmp"), pal)

    for happy, name in ((False, "monkey_angry"), (True, "monkey_happy")):
        scene, d = new(W, H)
        draw_background(d)
        draw_monkey(d, happy)
        crop(scene, MONKEY, os.path.join(OUT, name + ".bmp"), pal)

    inv, d = new(40, 16)
    disc(d, 20, 8, 6, C["nut0"])
    d.ellipse([15, 4, 19, 7], fill=C["nut1"])
    for px, py in ((18, 9), (21, 9), (20, 12)):
        d.point((px, py), fill=C["eye"])
    inv.putpalette(pal)
    inv.save(os.path.join(OUT, "inv_coconut.bmp"))

    write_box(os.path.join(OUT, "beach.box"),
              [("sand", [(0, 90), (319, 90), (319, 143), (0, 143)])])

    # Optionale Vorschau als PNG (z.B. PREVIEW=/tmp/beach.png)
    if os.environ.get("PREVIEW"):
        prev = bg.copy()
        pd = ImageDraw.Draw(prev)
        draw_monkey(pd, False)
        prev.putpalette(pal)
        prev.convert("RGB").resize((W * 3, H * 3), Image.NEAREST).save(os.environ["PREVIEW"])


if __name__ == "__main__":
    main()
