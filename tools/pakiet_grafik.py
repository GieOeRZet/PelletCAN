#!/usr/bin/env python3
"""Wypakowuje grafiki panela z wlasnego pliku FW2213TK.bin do dist/img/panel/NNN.png (pakiet "oryginalow" dla karty).
Uzycie: python3 tools/pakiet_grafik.py FW2213TK.bin [katalog_wyjsciowy]
Pliki to wlasnosc Estymy - tylko do uzytku prywatnego, katalog jest w .gitignore (nie commituj, nie publikuj).
Format: tablica touchgfx::BitmapData @0x54450, 188 wpisow po 20 B (data, alpha, w, h, ...), RGB565 LE + opcjonalna maska A8, baza ladowania 0x08010000."""
import os, struct, sys
import numpy as np
from PIL import Image
raw = open(sys.argv[1], 'rb').read()
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist', 'img', 'panel')
os.makedirs(out, exist_ok=True)
BASE, TAB = 0x08010000, 0x54450
CLEAN = {14, 15, 17, 8, 9, 10, 36, 37, 38, 40, 41, 42, 65, 66, 67, 105}   # bitmapy bez maski: usuniecie jednolitego tla od krawedzi
for i in range(188):
    d, a, w, h = struct.unpack('<IIHH', raw[TAB + i * 20:TAB + i * 20 + 12])
    o = d - BASE
    if not (0 <= o < len(raw)) or w * h == 0: continue
    v = np.frombuffer(raw[o:o + w * h * 2], '<u2').reshape(h, w).astype(np.uint32)
    rgb = np.stack([(v >> 11 & 31) * 255 // 31, (v >> 5 & 63) * 255 // 63, (v & 31) * 255 // 31, np.full((h, w), 255)], -1).astype(np.uint8)
    if a:
        rgb[..., 3] = np.frombuffer(raw[a - BASE:a - BASE + w * h], 'u1').reshape(h, w)
    elif i in CLEAN:
        bg = rgb[0, 0, :3].astype(int); close = np.abs(rgb[..., :3].astype(int) - bg).sum(-1) <= 30
        seen = np.zeros((h, w), bool); st = [(y, x) for y in range(h) for x in (0, w - 1)] + [(y, x) for x in range(w) for y in (0, h - 1)]
        while st:
            y, x = st.pop()
            if 0 <= y < h and 0 <= x < w and not seen[y, x] and close[y, x]:
                seen[y, x] = True; st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        rgb[seen, 3] = 0
    Image.fromarray(rgb).save(os.path.join(out, f'{i:03d}.png'))
print('gotowe:', out)
