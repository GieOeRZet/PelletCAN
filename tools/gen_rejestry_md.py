#!/usr/bin/env python3
"""Generuje rejestry/REJESTRY.md z katalog-rejestrow.csv + panel-fw-parametry-FW2213TK.csv + panel-fw-mapa-indeks-id.csv.
Uruchom po tools/scal_nazwy_panela.py i tools/oznacz_uzycie.py."""
import csv, os, datetime
R = os.path.join(os.path.dirname(__file__), '..', 'rejestry')
norm = lambda k: '0x' + k.strip()[2:].upper()
cat = [r for r in csv.DictReader(open(os.path.join(R, 'katalog-rejestrow.csv'), encoding='utf-8-sig'))]
par = {norm(p['id_hex']): p for p in csv.DictReader(open(os.path.join(R, 'panel-fw-parametry-FW2213TK.csv'), encoding='utf-8'))}
mapa = {norm(l['index']): l for l in csv.DictReader(open(os.path.join(R, 'panel-fw-mapa-indeks-id.csv'), encoding='utf-8-sig'), delimiter=';')}
ACC = {'0': 'live (odczyt)', '1': 'komenda', '2': 'nastawa', '3': 'nastawa'}
def e(x): return (x or '').replace('|', '/').replace('\n', ' ').strip()
n4 = [r for r in cat if r['wezel'] == '4' and r['index'].startswith('0x')]
n86 = [r for r in cat if r['wezel'] == '86']
byidx = {norm(r['index']): r for r in n4}
used = [r for r in n4 if r['wykorzystany'] == 'TAK']
used_k = {norm(r['index']) for r in used}
bin_used = [k for k in par if k in used_k]
bin_rest = [k for k in par if k not in used_k]
ans = lambda k: {'TAK': 'tak', 'NIE': 'nie'}.get(mapa.get(k, {}).get('odpowiada_na_kotle_2026-11-06', ''), 'nie sprawdzono')
rest_boiler = [r for r in n4 if norm(r['index']) not in par and norm(r['index']) not in used_k]
def grp(r): return e(r['grupa adresowa']) or 'Inne'
out = []
w = out.append
w('# Rejestry kotła i firmware panela – pełna dokumentacja')
w('')
w('Plik **generowany** (`tools/gen_rejestry_md.py`) z `katalog-rejestrow.csv`, `panel-fw-parametry-FW2213TK.csv` i `panel-fw-mapa-indeks-id.csv`. Nie edytuj ręcznie – popraw CSV i uruchom skrypty (sekcja 7). Stan: %s, firmware PelletCAN 1.4.23.' % datetime.date.today().isoformat())
w('')
w('## 1. Liczby')
w('')
w('| Co | Ile |')
w('|---|---|')
w('| Parametry zarejestrowane w kodzie firmware panela FW2213TK (funkcja `0x0802143C`, ID parametru = indeks SDO) | **%d** |' % len(par))
w('| …z tego wykorzystane w naszym firmware ESPHome | %d |' % len(bin_used))
w('| …z tego jeszcze niewykorzystane | %d |' % len(bin_rest))
w('| Pary (indeks CANopen, ID panela) w tablicy @0x37576 | 420 wierszy, %d unikalnych indeksów (odpowiada na kotle: %d, nie: %d) |' % (len(mapa), sum(1 for v in mapa.values() if v['odpowiada_na_kotle_2026-11-06'] == 'TAK'), sum(1 for v in mapa.values() if v['odpowiada_na_kotle_2026-11-06'] == 'NIE')))
w('| Rejestry węzła 4 (kocioł) w katalogu | %d (w tym 593 odpowiada na skan, reszta to parametry znane tylko z firmware panela) |' % len(n4))
w('| Rejestry węzła 4 wykorzystane w naszym firmware (łącznie z niepanelowymi, np. alarmy 0x4010+) | %d |' % len(used))
w('| Wiersze węzła 86 (CAN IO BIG) | %d |' % len(n86))
w('')
w('Rodzaje parametrów panela: %s. Dostęp wg panela: 0 = odczyt na żywo, 1 = komenda, 2/3 = nastawa (3 – edytowalna z menu).' % ', '.join('%s: %d' % (t, sum(1 for p in par.values() if p['type'] == t)) for t in ['u8', 'u16', 's16', 'u32', 's32']))
w('')
w('## 2. Jak czytać wartości')
w('')
w('- Węzeł 4 = sterownik kotła, CANopen SDO, 125 kbit/s, **sub 1** (sub 0/2 nic nie zwracają). Węzeł 86 = CAN IO BIG. ESP = węzeł 90.')
w('- **flaga + bajt:** wiele parametrów jest zwracanych jako `256 + wartość` (np. surowe 276 = 20). W tabelach „kodowanie” opisuje przeliczenie.')
w('- **Temperatury** to zwykle `raw / 10 °C`; niektóre nastawy są w °C bez dzielenia.')
w('- **Poziom menu (PIN):** 0 = bez PIN-u, klucz 1 = PIN instalatora 0900, klucz 2 = PIN 0999 (wymagany m.in. do Testu wyjść).')
w('- **Status:** POTWIERDZONY = znaczenie sprawdzone na kotle; ODNALEZIONY – … = nazwa z firmware panela lub skan, nieprzetestowane; NIEZNANY = brak nazwy.')
w('')
w('## 3. Rejestry wykorzystywane w firmware / karcie (%d)' % len(used))
w('')
w('Opis każdego: co to jest, kodowanie, dostęp i **gdzie w firmware** (akcja `set_param` N, encja, ekran karty). Kolumna „Nazwa panela” to oryginalna angielska nazwa z firmware panela.')
w('')
groups = {}
for r in sorted(used, key=lambda r: int(r['index'], 16)): groups.setdefault(grp(r), []).append(r)
for g, rs in sorted(groups.items(), key=lambda kv: int(kv[1][0]['index'], 16)):
    w('### %s' % g)
    w('')
    w('| Rejestr | Nazwa | Nazwa panela | Typ | Zakres | Kodowanie / jednostka | Dostęp | PIN | Gdzie w firmware / karcie | Uwagi |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for r in rs:
        k = norm(r['index']); p = par.get(k)
        zak = '%s…%s' % (r['zakres min'], r['zakres max']) if r['zakres min'] or r['zakres max'] else ''
        gdzie = ' '.join(x for x in [e(r['gdzie w firmware']), e(r['uzycie w firmware / karcie'])] if x)
        uw = ' '.join(x for x in [e(r['opis / za co odpowiada']), e(r['jak potwierdzone / uwagi'])] if x)
        w('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, e(r['nazwa']) or '-', e(p['name']) if p else '-', e(r['typ']) or (p['type'] if p else ''), zak, e(r['skala / kodowanie / jednostka']), e(r['dostep']), e(r['poziom menu (PIN)']), gdzie, uw))
    w('')
w('## 4. Parametry z binarki panela, jeszcze niewykorzystane (%d)' % len(bin_rest))
w('')
w('Pełna lista z firmware panela FW2213TK. „Na kotle” = czy rejestr odpowiedział w skanie 6.11.2026 (sub 1). Wartość surowa tylko dla 197 rejestrów ze snapa bazowego. To jest **materiał do dalszej pracy**: wybierz pozycję, sprawdź na panelu, podepnij w firmware (instrukcja w [README.md](README.md)).')
w('')
base = {}
bp = os.path.join(R, 'snap-197-baseline-2026-11-06.csv')
if os.path.exists(bp):
    for l in csv.reader(open(bp, encoding='utf-8-sig'), delimiter=';'):
        if l and l[0].startswith('0x'): base[norm(l[0])] = l[3] if len(l) > 3 else ''
w('| Rejestr | ID | Nazwa z FW panela | Typ | Min | Max | Domyślna | Dostęp panela | Na kotle | Wartość surowa | Status w katalogu |')
w('|---|---|---|---|---|---|---|---|---|---|---|')
for k in sorted(bin_rest, key=lambda k: int(k, 16)):
    p = par[k]; r = byidx.get(k, {})
    w('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, p['id'], e(p['name']), p['type'], p['min'], p['max'], p['default'], ACC.get(p['access'], p['access']), ans(k), base.get(k, ''), e(r.get('status', '')).replace('ODNALEZIONY – ', '')))
w('')
w('## 5. Rejestry kotła, których nie ma w binarce panela i których nie używamy (%d)' % len(rest_boiler))
w('')
w('Odpowiadają na skan węzła 4, ale panel ich nie rejestruje (m.in. bloki harmonogramów, liczniki, kopie wartości). Opis jest automatyczny („auto”) – wartość i zakres z odczytu.')
w('')
w('| Rejestr | Nazwa | Status | Opis / wartość | Blok |')
w('|---|---|---|---|---|')
for r in sorted(rest_boiler, key=lambda r: int(r['index'], 16)):
    w('| `%s` | %s | %s | %s | %s |' % (norm(r['index']), e(r['nazwa']) or '-', e(r['status']), e(r['opis / za co odpowiada']), e(r['grupa adresowa'])))
w('')
w('## 6. Węzeł 86 – CAN IO BIG (CiA 401)')
w('')
if n86:
    w('| Rejestr | Nazwa | Status | Opis | Uwagi |')
    w('|---|---|---|---|---|')
    for r in n86:
        w('| `%s` | %s | %s | %s | %s |' % (e(r['index']), e(r['nazwa']) or '-', e(r['status']), e(r['opis / za co odpowiada']), e(r['jak potwierdzone / uwagi'])))
w('')
w('## 7. Jak kontynuować pracę')
w('')
w('1. **Znajdź rejestr pozycji menu:** wybierz wiersz z sekcji 4 (albo pozycję menu panela), w HA naciśnij **Snap A**, zmień JEDNĄ nastawę na panelu, naciśnij **Snap B** – lista `XXXX:stara>nowa` pokaże rejestr (szczegóły: [README.md](README.md), sekcja 3).')
w('2. **Podepnij w firmware:** dopisz `case 0x....:` w parserze, wpis w `set_param` (ix/lo/hi/lv) i encję w `esphome/PelletCAN_packages.yaml`; w karcie dodaj wiersz na ekranie (patrz CHANGELOG-firmware.md, np. v1.4.18–1.4.23 jako wzór).')
w('3. **Zaktualizuj dokumentację:** `python3 tools/oznacz_uzycie.py` (kolumna „wykorzystany”), popraw status/opis w `katalog-rejestrow.csv`, potem `python3 tools/gen_rejestry_md.py` (ten plik) i `python3 tools/gen_katalog_html.py docs/katalog.html`.')
w('4. **Nowa wersja panela:** po wczytaniu nowego FW panela odtwórz `panel-fw-parametry-*.csv` (rejestracja parametrów funkcją `0x0802143C`, baza ładowania `0x08010000`) i uruchom `python3 tools/scal_nazwy_panela.py`.')
w('5. **Zapisy na kotle** wykonuj ostrożnie: flaga `mirror`, wyłączniki `*_write`, poziom dostępu (klucz 1/2). Nowy zapis testuj na jednym rejestrze i porównaj z tym, co robi panel (`sniff: "true"` pokaże zapisy panela).')
w('')
w('Powiązane: [README.md](README.md) (skaner, metoda różnicowa), [PANEL-FW.md](PANEL-FW.md) (analiza firmware panela), [TODO.md](TODO.md), [katalog-rejestrow.csv](katalog-rejestrow.csv), [alarmy-kody.csv](alarmy-kody.csv), [strona katalogu](https://gieoerzet.github.io/PelletCAN/katalog.html).')
open(os.path.join(R, 'REJESTRY.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('used %d | bin %d (used %d, rest %d) | rest_boiler %d | n86 %d' % (len(used), len(par), len(bin_used), len(bin_rest), len(rest_boiler), len(n86)))
