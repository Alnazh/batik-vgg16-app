# Script sekali jalan untuk membuat ilustrasi pola PNG tiap motif batik (dipakai di dashboard)
import os
import math
from PIL import Image, ImageDraw

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img", "motif")
UKURAN = (480, 320)

WARNA_SOGAN = (161, 92, 43)
WARNA_SOGAN_MUDA = (201, 138, 79)
WARNA_INDIGO = (31, 45, 80)
WARNA_GOLD = (201, 162, 39)
WARNA_KRIM = (246, 239, 224)


def buat_kawung():
    img = Image.new("RGB", UKURAN, WARNA_SOGAN)
    draw = ImageDraw.Draw(img)
    langkah = 70
    for y in range(-langkah, UKURAN[1] + langkah, langkah):
        for x in range(-langkah, UKURAN[0] + langkah, langkah):
            offset = langkah // 2 if (y // langkah) % 2 else 0
            draw.ellipse([x + offset - 24, y - 24, x + offset + 24, y + 24], fill=WARNA_KRIM)
    return img


def buat_mega_mendung():
    img = Image.new("RGB", UKURAN, WARNA_INDIGO)
    draw = ImageDraw.Draw(img)
    for i in range(6):
        warna = tuple(int(a + (b - a) * i / 5) for a, b in zip(WARNA_INDIGO, WARNA_SOGAN_MUDA))
        y = 40 + i * 45
        draw.arc([-60 + i * 30, y - 40, 260 + i * 30, y + 40], start=200, end=340, fill=warna, width=10)
        draw.arc([180 + i * 20, y - 30, 500 + i * 20, y + 50], start=200, end=340, fill=warna, width=10)
    return img


def buat_parang():
    img = Image.new("RGB", UKURAN, WARNA_KRIM)
    draw = ImageDraw.Draw(img)
    lebar_garis = 22
    jarak = 42
    total = UKURAN[0] + UKURAN[1]
    for offset in range(-UKURAN[1], total, jarak):
        draw.line([(offset, 0), (offset + UKURAN[1], UKURAN[1])], fill=WARNA_SOGAN, width=lebar_garis)
    return img


def buat_truntum():
    img = Image.new("RGB", UKURAN, WARNA_INDIGO)
    draw = ImageDraw.Draw(img)
    langkah = 34
    for y in range(langkah, UKURAN[1], langkah):
        for x in range(langkah, UKURAN[0], langkah):
            r = 4
            draw.ellipse([x - r, y - r, x + r, y + r], fill=WARNA_GOLD)
    return img


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    gambar_per_motif = {
        "kawung": buat_kawung(),
        "mega_mendung": buat_mega_mendung(),
        "parang": buat_parang(),
        "truntum": buat_truntum(),
    }
    for nama, gambar in gambar_per_motif.items():
        gambar.save(os.path.join(OUTPUT_DIR, f"{nama}.png"))
        print(f"[INFO] Tersimpan: {nama}.png")
