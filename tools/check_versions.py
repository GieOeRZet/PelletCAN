#!/usr/bin/env python3
"""Kontrola spojnosci wersji: version.json <-> fw_version w YAML <-> CARD_VER w karcie <-> pierwszy wpis w changelogach. Kod wyjscia 1 przy bledzie."""
import json, pathlib, re, sys
r = pathlib.Path(__file__).resolve().parent.parent
v = json.load(open(r / 'version.json', encoding='utf-8'))
fw, card = v['firmware']['version'], v['card']['version']
err = []
m = re.search(r'fw_version:\s*"([^"]+)"', (r / 'esphome/PelletCAN_packages.yaml').read_text(encoding='utf-8'))
if not m or m.group(1) != fw: err.append(f'fw_version w YAML = {m and m.group(1)}, version.json = {fw}')
m = re.search(r"CARD_VER = '([^']+)'", (r / 'dist/pelletcan-card.js').read_text(encoding='utf-8'))
if not m or m.group(1) != card: err.append(f'CARD_VER w karcie = {m and m.group(1)}, version.json = {card}')
m = re.search(r'^## v([\d.]+)', (r / 'CHANGELOG-firmware.md').read_text(encoding='utf-8'), re.M)
if not m or m.group(1) != fw: err.append(f'CHANGELOG-firmware.md: najnowszy wpis v{m and m.group(1)}, oczekiwano v{fw}')
m = re.search(r'^## v([\d.]+)', (r / 'CHANGELOG.md').read_text(encoding='utf-8'), re.M)
if not m or m.group(1) != card: err.append(f'CHANGELOG.md: najnowszy wpis v{m and m.group(1)}, oczekiwano v{card}')
for k in ('firmware', 'card'):
    if not v[k].get('changelog'): err.append(f'version.json: pusty changelog ({k})')
print('\n'.join(err) if err else f'OK: firmware {fw}, karta {card}')
sys.exit(1 if err else 0)
