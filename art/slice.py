#!/usr/bin/env python3
"""Gemini'den gelen yeşil fonlu sprite sayfasını şeffaf PNG'lere böler.

Kullanım:
    python3 slice.py <girdi.jpeg> <sutun> <satir> <cikti_klasoru> <isim1,isim2,...>
"""
import sys, os
import numpy as np
from PIL import Image


def key_green(img):
    """Yeşil fonu şeffaf yapar + kenardaki yeşil taşmayı temizler."""
    a = np.array(img.convert("RGBA")).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]

    # 1) tam yeşil bölge -> şeffaf
    is_bg = (g > 90) & (g > r + 40) & (g > b + 40)
    a[..., 3] = np.where(is_bg, 0, 255)

    # 2) yarı yeşil kenarlar (JPEG bulaşması) -> yumuşak alfa + yeşili bastır
    spill = (~is_bg) & (g > np.maximum(r, b) + 12)
    cap = np.maximum(r, b) + 12
    a[..., 1] = np.where(spill, np.minimum(g, cap), g)

    return Image.fromarray(a.astype(np.uint8), "RGBA")


def trim(img, pad=6):
    bbox = img.split()[3].getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(img.width, x1 + pad); y1 = min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


def fit(img, w, h):
    """Şeffaf w x h tuvale, alta hizalı, oranı bozmadan yerleştirir."""
    s = min(w / img.width, h / img.height)
    n = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(n, ((w - n.width) // 2, h - n.height), n)
    return canvas


def main():
    src, cols, rows, outdir, names = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    names = names.split(",")
    os.makedirs(outdir, exist_ok=True)

    sheet = key_green(Image.open(src))
    cw, ch = sheet.width // cols, sheet.height // rows

    # her hücreyi kırp, kırp-temizle, ortak ölçüye getir
    cells = []
    for ry in range(rows):
        for cx in range(cols):
            cell = sheet.crop((cx * cw, ry * ch, (cx + 1) * cw, (ry + 1) * ch))
            cells.append(trim(cell))

    # en yüksek karakteri referans al -> hepsi aynı ölçekte kalsın
    tall = max(c.height for c in cells)
    for cell, name in zip(cells, names):
        s = 300 / tall
        w = max(1, int(cell.width * s))
        h = max(1, int(cell.height * s))
        out = cell.resize((w, h), Image.LANCZOS)
        out = fit(out, 200, 300)
        out.save(os.path.join(outdir, name + ".png"))
        print(name, out.size)


if __name__ == "__main__":
    main()
