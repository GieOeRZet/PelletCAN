#!/usr/bin/env python3
"""Wpisuje do rejestry/katalog-rejestrow.csv nazwy i parametry z firmware panela (panel-fw-parametry-FW2213TK.csv):
- wiersze wezla 4 bez nazwy dostaja nazwe z FW panela (status 'ODNALEZIONY – NAZWA Z FW PANELA'), opis jest dopisywany;
- parametry, ktorych nie ma w katalogu, sa dodawane jako nowe wiersze ('ODNALEZIONY – TYLKO W FW PANELA').
Wiersze juz nazwane (POTWIERDZONY itd.) nie sa zmieniane. Uruchom potem tools/oznacz_uzycie.py."""
import csv, os
R = os.path.join(os.path.dirname(__file__), '..', 'rejestry')
cat = os.path.join(R, 'katalog-rejestrow.csv')
rows = list(csv.reader(open(cat, encoding='utf-8-sig', newline='')))
h = rows[0]; ix = {c: i for i, c in enumerate(h)}
par = {p['id_hex'].upper().replace('0X', '0x'): p for p in csv.DictReader(open(os.path.join(R, 'panel-fw-parametry-FW2213TK.csv'), encoding='utf-8'))}
ans = {}
for l in csv.DictReader(open(os.path.join(R, 'panel-fw-mapa-indeks-id.csv'), encoding='utf-8-sig'), delimiter=';'):
    ans[l['index'].upper().replace('0X', '0x')] = l['odpowiada_na_kotle_2026-11-06']
ACC = {'0': 'odczyt na zywo', '1': 'komenda', '2': 'nastawa', '3': 'nastawa'}
def info(p):
    s = 'FW panela: %s; typ %s, zakres %s…%s' % (p['name'], p['type'], p['min'], p['max'])
    if p['default'] != '': s += ', domyslna %s' % p['default']
    return s + ', dostep: %s' % ACC.get(p['access'], p['access'])
have = set(); fill = 0
for r in rows[1:]:
    if r[ix['wezel']] != '4': continue
    k = r[ix['index']].upper().replace('0X', '0x'); have.add(k)
    if k in par and not r[ix['nazwa']].strip():
        p = par[k]
        r[ix['nazwa']] = p['name'] + ' (FW panela)'
        r[ix['status']] = 'ODNALEZIONY – NAZWA Z FW PANELA'
        r[ix['opis / za co odpowiada']] = (r[ix['opis / za co odpowiada']] + ' | ' + info(p)).strip(' |')
        fill += 1
new = []
for k, p in par.items():
    if k in have: continue
    r = [''] * len(h)
    r[ix['wezel']] = '4'; r[ix['index']] = k; r[ix['sub']] = '1'
    r[ix['nazwa']] = p['name'] + ' (FW panela)'
    r[ix['status']] = 'ODNALEZIONY – TYLKO W FW PANELA'
    r[ix['opis / za co odpowiada']] = info(p) + '; na kotle: ' + {'TAK': 'odpowiada', 'NIE': 'nie odpowiada (inna konfiguracja?)'}.get(ans.get(k, ''), 'nie skanowano')
    r[ix['typ']] = p['type'].upper(); r[ix['wykorzystany']] = 'NIE'
    new.append(r)
body = rows[1:]
def key(r):
    try: return (0 if r[0] == '4' else 1, int(r[1], 16))
    except ValueError: return (2, 0)
body = sorted(body + new, key=key)
with open(cat, 'w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerows([h] + body)
print('nazwy uzupelnione: %d, nowe wiersze: %d, razem wierszy: %d' % (fill, len(new), len(body)))
