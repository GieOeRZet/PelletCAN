#!/usr/bin/env python3
"""Uzupelnia w rejestry/katalog-rejestrow.csv kolumny 'wykorzystany' i 'gdzie w firmware' na podstawie
esphome/PelletCAN_packages.yaml (odczyt: 'case 0x....' i listy odpytywania, zapis: tablica ix[] = set_param).
Uruchom po dodaniu rejestru do firmware:  python3 tools/oznacz_uzycie.py"""
import csv, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
fw = (root / 'esphome' / 'PelletCAN_packages.yaml').read_text(encoding='utf-8')
hx = lambda s: int(s, 16)
ix = max(re.findall(r'static const uint16_t ix\[\] = \{([^}]*)\}', fw), key=len)
writes = {hx(t): k for k, t in enumerate(re.findall(r'0x([0-9A-Fa-f]{4})', ix))}
reads = set(hx(t) for t in re.findall(r'case 0x([0-9A-Fa-f]{4}):', fw))
l1 = set()
for m in re.finditer(r'static const uint16_t l1\[\] = \{([^}]*)\}', fw):
    l1 |= set(hx(t) for t in re.findall(r'0x([0-9A-Fa-f]{4})', m.group(1)))
# rejestry ustawiane osobnymi akcjami (testy wyjsc, tryby, harmonogramy, paliwo)
other = {0x2259:'Test wyjsc / Podajnik', 0x2283:'Test wyjsc / Dmuchawa', 0x2284:'Test wyjsc / Zapalarka', 0x2295:'Test wyjsc / Podajnik palnika', 0x2296:'Test wyjsc / Pompa CWU',
         0x2005:'power_switch', 0x2002:'set_boiler_mode', 0x2064:'tryb CO', 0x2014:'tryb CWU', 0x2003:'set_setpoint', 0x2010:'set_setpoint', 0x2012:'set_setpoint',
         0x2032:'set_setpoint', 0x2048:'set_setpoint', 0x3601:'zapis paliwa (przyciski +/-)'}
for d in range(7):
    other[0x2126 + 4 * d] = 'set_schedule CO'; other[0x2154 + d] = 'set_schedule CWU'; other[0x2209 + d] = 'set_schedule kociol'
p = root / 'rejestry' / 'katalog-rejestrow.csv'
rows = list(csv.reader(open(p, encoding='utf-8-sig')))
h = rows[0]
for c in ('wykorzystany', 'gdzie w firmware'):
    if c not in h: h.append(c)
iw, ig, ii, in_ = h.index('wykorzystany'), h.index('gdzie w firmware'), h.index('index'), h.index('wezel')
out = [h]
n_used = 0
for r in rows[1:]:
    r += [''] * (len(h) - len(r))
    r[iw] = r[ig] = ''
    if r[in_] == '4' and re.fullmatch(r'0x[0-9A-Fa-f]{4}', r[ii]):
        i = hx(r[ii][2:])
        g = []
        if i in writes: g.append('zapis: set_param %d' % writes[i])
        elif i in other: g.append('zapis: ' + other[i])
        if i in reads or i in l1: g.append('odczyt')
        elif 0x4010 <= i <= 0x404D: g.append('odczyt (historia alarmow)')
        if g: r[iw], r[ig] = 'TAK', ', '.join(g); n_used += 1
        else: r[iw] = 'NIE'
    out.append(r)
with open(p, 'w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerows(out)
print('wiersze: %d, wykorzystane (wezel 4): %d' % (len(out) - 1, n_used))
