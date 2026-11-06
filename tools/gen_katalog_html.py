#!/usr/bin/env python3
"""Generuje docs/katalog.html z rejestry/katalog-rejestrow.csv (strona katalogu rejestrow, GitHub Pages)."""
import csv, html, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
src = root / 'rejestry' / 'katalog-rejestrow.csv'
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'docs' / 'katalog.html'
rows = list(csv.DictReader(open(src, encoding='utf-8-sig')))
COLS = [('index', 'Rejestr'), ('wezel', 'Węzeł'), ('nazwa', 'Nazwa'), ('status', 'Status'), ('opis / za co odpowiada', 'Opis'),
        ('zakres min', 'Min'), ('zakres max', 'Max'), ('skala / kodowanie / jednostka', 'Kodowanie'), ('dostep', 'Dostęp'),
        ('wykorzystany', 'W firmware')]
def e(x): return html.escape((x or '').strip())
th = ''.join(f'<th>{n}</th>' for _, n in COLS)
body = []
for r in rows:
    st = (r.get('status') or '').strip()
    cls = 'ok' if st.startswith('POTW') else 'mid' if st.startswith(('ODNAL', 'PRAWD')) else 'no'
    tds = ''.join(f'<td>{e(r.get(k))}</td>' for k, _ in COLS)
    body.append(f'<tr class="{cls}">{tds}</tr>')
n_ok = sum(1 for r in rows if (r.get('status') or '').startswith('POTW'))
page = f'''<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PelletCAN – katalog rejestrów</title>
<style>
:root{{--bg:#fff;--fg:#1c1c1c;--mut:#666;--ln:#ddd;--ok:#e6f6e6;--mid:#fff6dc}}
@media(prefers-color-scheme:dark){{:root{{--bg:#151515;--fg:#e8e8e8;--mut:#9a9a9a;--ln:#333;--ok:#1d3320;--mid:#3a3318}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif}}
h1{{font-size:20px;margin:0 0 4px}} p{{color:var(--mut);margin:0 0 12px}}
input,select{{font:inherit;padding:6px 8px;margin:0 8px 12px 0;background:var(--bg);color:var(--fg);border:1px solid var(--ln);border-radius:6px}}
.w{{overflow:auto}} table{{border-collapse:collapse;width:100%;min-width:900px}}
th,td{{border-bottom:1px solid var(--ln);padding:5px 8px;text-align:left;vertical-align:top}}
th{{position:sticky;top:0;background:var(--bg)}} tr.ok{{background:var(--ok)}} tr.mid{{background:var(--mid)}}
td:first-child{{font-family:ui-monospace,monospace;white-space:nowrap}}
</style></head><body>
<h1>PelletCAN – katalog rejestrów kotła Tekla/Estyma Igneo Touch</h1>
<p>{len(rows)} rejestrów, w tym {n_ok} potwierdzonych. Wygenerowano z <code>rejestry/katalog-rejestrow.csv</code>. <a href="https://github.com/GieOeRZet/PelletCAN">Repozytorium</a></p>
<input id="q" placeholder="Szukaj (hex, nazwa, opis)…" size="32">
<select id="s"><option value="">Wszystkie statusy</option><option value="ok">Potwierdzone</option><option value="mid">Do potwierdzenia</option><option value="no">Nieznane</option></select>
<div class="w"><table id="t"><thead><tr>{th}</tr></thead><tbody>
{chr(10).join(body)}
</tbody></table></div>
<script>
const q=document.getElementById('q'),s=document.getElementById('s'),rs=[...document.querySelectorAll('#t tbody tr')];
function f(){{const t=q.value.toLowerCase();rs.forEach(r=>{{r.hidden=!((!t||r.textContent.toLowerCase().includes(t))&&(!s.value||r.classList.contains(s.value)))}})}}
q.oninput=s.onchange=f;
</script></body></html>
'''
out.write_text(page, encoding='utf-8')
print(f'{out}: {len(rows)} wierszy')
