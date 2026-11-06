# Changelog firmware (ESPHome PelletCAN)

Najnowsze na górze. Karta ma osobny plik: [CHANGELOG.md](CHANGELOG.md).

## v1.4.16
- **Statystyki**: nowe odczyty `0x3610` (średnia moc z 50 h, flaga+bajt), `0x3613–0x3616` (średni tlen 30/50/70/90 %, flaga+bajt), `0x3628` (energia całkowita kWh) – nazwy i typy z firmware panela FW2213TK. Encja „Statystyki kotla” ma teraz 14 liczb. Wymaga karty ≥ 1.19.

## v1.4.15
- **Raport diagnostyczny**: przycisk „Raport diagnostyczny (utworz)” → tekst „Raport diagnostyczny” (wersja, czas pracy, Wi-Fi dBm, CAN, liczniki SDO ok/abort, poziom, mirror, tank, zużycie) do wklejenia w Issue.
- **Skan różnicowy w ESP**: „Snap A (punkt odniesienia)” zapisuje 593 rejestry katalogu (~72 s), zmień ustawienie na panelu, „Snap B (pokaz zmiany)” – „Zmiany rejestrow (Snap)” podaje listę `XXXX:stara>nowa`. „Snap STOP” przerywa.
- **Prognoza paliwa**: co godzinę odczyt licznika zużycia (0x3507), sensory „Paliwo zuzycie 24h” [kg/dobę], „Paliwo prognoza” [dni] i „Paliwo rezerwa” (binary_sensor, włącza się gdy zasobnik ≤ Rezerwa paliwa stop). Powiadomienie: automatyzacja HA na stan „Paliwo rezerwa” = on (przykład w docs/DIAGNOSTYKA.md).
- Wymaga karty ≥ 1.18 do wyświetlania w Statystykach.

## v1.4.14
- **Czysty log**: wyłączone (domyślnie) wpisy diagnostyczne – NMT/heartbeat innych węzłów, `IDENT`, zmiany `PDO 0x456/0x356`, `FEED PDO 0x2D7`, raport `SKAN SIECI` – za nowym ustawieniem `diag_log: "false"` (`"true"` przywraca). `sniff` domyślnie `"false"`.
- Encje **CAN diag** i **CAN ID ramek** są `internal` (niewidoczne w HA).
- **Migawki wykomentowane**: akcje `sdo_snapshot_cat`, `sdo_snapshot_range` oraz przyciski „Migawka katalogowa”, „Migawka STOP”. Zostają narzędzia skanera: `sdo_scan`, `sdo_scan_stop`, `sdo_read`, `sdo_write` (+ `sdo_poll_add/clear`).
- **Skan pokazuje także rejestry znane firmware** (do tej pory trafiały tylko do własnych encji) – wynik zawsze w „SDO ostatni odczyt”.
- Dokumentacja: nowy folder [`rejestry/`](rejestry/README.md) – pełny katalog rejestrów (`katalog-rejestrow.csv`, ze zakresami, kodowaniem, R/W i oznaczeniem wykorzystania) i instrukcja skanera; `tools/oznacz_uzycie.py`; przepisany `docs/DIAGNOSTYKA.md`.

## v1.4.13
- **Kocioł NASTAWY**: `set_param` 64 = Wybieg pompy (0x3708, 0–120 min, flaga+bajt; znaleziony skanem po zmianie 0→13 na panelu: 256→269), 65 = Rezerwa paliwa stop (0x3604, 0–100 kg, liczba; 0→17). Encje „Kociol wybieg pompy”, „Kociol rezerwa paliwa stop”. Menu Kocioł NASTAWY kompletne.

## v1.4.12
- **Piny w substitutions**: `pin_spi_clk`, `pin_spi_mosi`, `pin_spi_miso`, `pin_can_cs`, `can_spi_rate`, `pin_rf_switch`, `pin_rf_antenna` (domyślnie XIAO ESP32-C6 + Seeed CAN Bus Breakout, jak dotąd). Użytkownik z innym ESP lub modułem MCP2515 zmienia je w `PelletCAN.yaml`, rdzeń zostaje bez zmian.
- **CO1 NASTAWY**: `set_param` 63 = Czujnik pokojowy (0x22A1: 0 brak, 1 CTP1, 2 CTP2, 3 videROOM, 4 termostat, 5 CAN); znaleziony zmianą termostat→brak na panelu (260→256). Encja „CO1 czujnik pokojowy”.

## v1.4.11
- **CO1 NASTAWY**: `set_param` 61 = Źródło (0x22D1, 0 Kocioł / 1 Bufor), 62 = Czujnik CO (0x22A5, 0/1); znalezione różnicą skanu po zmianie na panelu (Źródło Kocioł→Bufor: 0x22D1 256→257; Czujnik CO wł.→wył.: 0x22A5 257→256). Pozostaje Czujnik pokojowy (nieznany).

## v1.4.10
- **CO1 NASTAWY**: `set_param` 59 = Stała pompa (0x22F1, 0/1), 60 = Obniżenie Tco dla ochrony powrotu (0x22F9, 0/1); znalezione różnicą skanu po przełączeniu na panelu (257→256 i 256→257). Encje „CO1 stala pompa”, „CO1 obnizenie Tco ochrona powrotu”.

## v1.4.9
- **Ogrzewanie 1 (CO) → NASTAWY (poziom 1)**: `set_param` klucze 51–58: 51 Zwiększenie temp. źródła (0x22B1, 0–30 °C), 52 Temp. maksymalna (0x22D5, 30–80 °C), 53 Wsp. korekcji t. CO (0x22D9, 0–20), 54 MAX Tzew pomp komf. (0x22DD, 0–30 °C), 55 MAX Tzew pomp ekon. (0x22E1, 0–30 °C), 56 Obniżenie temperatury CO (0x22E5, 0–40 °C – potwierdzone zmianą 5→7), 57 MIN temperatura CO pomp (0x22E9, 20–60 °C), 58 Czas mieszacza (0x22B5, 60–360 s). Nowe encje „CO1 …”, odczyt po starcie i po PIN-ie. Rejestry znalezione zmianą wartości na panelu i skanem SDO.

## v1.4.8
- **Kocioł NASTAWY**: `set_param` klucz 48 = Minimalna temp. pomp (0x2207, 20–70 °C), 49 = Minimalna temp. powrotu (0x216C, 35–75 °C), 50 = Czas mieszacza (0x216E, 60–360 s); nowe encje „Kociol minimalna temp. pomp”, „Kociol minimalna temp. powrotu”, „Kociol czas mieszacza”, odczyt po starcie i po PIN-ie (poziom 1). Rejestry znalezione zmianą wartości na panelu i skanem SDO. Wybieg pompy i Rezerwa paliwa stop: rejestry nieznane.

## v1.4.7
- **Test wyjść: Pompa CWU** – wyjście nr 20, rejestr 0x2296 (256 = A, 257 = OFF, 258 = ON), znaleziony przez porównanie skanów 0x2270–0x22C4 z pompą na ON i na A. Stan wraca w „Test wyjsc stany” (21 wartości). Panel steruje tą pompą dalej przez PDO 0x256 bajt0 bit 0x10 (węzeł 86).

## v1.4.6
- **Paliwo w zbiorniku – zapis** (`set_param` klucz 47 = rejestr 0x3601, kg, 0…pojemność zbiornika; poziom 0). Pod przyciski + i − w oknie Paliwo karty. Procent zapełnienia liczony jak dotąd: kg / pojemność (0x3601 / 0x3600).

## v1.4.5
- **Podajnik palnika pracuje**: poprzednie źródło (PDO 0x456 bajt 0 bit 1) nigdy się nie ustawiało. Nowe: PDO 0x356 (węzeł 86) bajt 2 bit 0 – z logów rośnie dokładnie w tej samej chwili co podajnik główny (cykl 20 s, różnica rzędu ms), a opada po kilku sekundach. Do potwierdzenia testem wyjść „Podajnik palnika”.

## v1.4.4
- Nowe ustawienie `can_product` (kod produktu 0x1018 sub2, dziesiętnie, domyślnie 1). Panel w zakładce Sieć rozpoznaje urządzenia wyłącznie po tym kodzie (CAN IO BIG = 65538). Pozwala sprawdzić, jaki kod pokaże nazwę/wersję.
- Ustalone w 1.4.2–1.4.3: panel skanuje węzły 1–127 cyklicznie, pyta tylko o 0x1018 sub2 i widzi ESP jako węzeł 90.

## v1.4.3
- Raport `SKAN SIECI` obejmuje też zapytania/odpowiedzi 0x1001 i 0x100A (wersja softu) – sprawdzamy, skąd panel bierze „SW v…” węzła 86.

## v1.4.2
- Raport `SKAN SIECI` wysyłany także podczas ciągłego skanu (co 20 s), nie tylko po ciszy – w v1.4.1 raport nie pojawiał się, gdy panel skanuje bez przerwy.

## v1.4.1 – Raport skanu sieci
- Po każdym skanie tożsamości przez panel (np. po restarcie ESP) ESP wysyła do „CAN diag” i „SDO ostatni odczyt” jedną linię `SKAN SIECI: …` – ile węzłów panel zapytał (zakres), ile razy zapytał ESP (węzeł 90), jakie węzły odpowiedziały i z jakim kodem produktu (`R86:1018.2=00010002`), oraz każde inne zapytanie niż kod produktu (`Q…`). Pozwala sprawdzić zakładkę Sieć bez patrzenia na panel.
- Wersja 1.4.1 (poprawka numeracji: `fw_version`).

## v1.4 – ESP jako węzeł w zakładce Sieć
- ESP ma teraz własny numer węzła **90** (86 = CAN IO BIG, 87 = urządzenie kotła – zajęte, stąd „Unknown”). Wysyła boot-up + heartbeat NMT (0x790, co 1 s) i odpowiada na zapytania tożsamości – panel w Menu → Sieć powinien pokazać „PelletCAN  Node ID=90  SW v1.4”.
- Domyślnie `can_heartbeat: "true"`, `can_node_id: "90"` (zmiana względem 1.3 – wymień swój PelletCAN.yaml lub ustaw ręcznie).
- Wersja softu raportowana jako `v<wersja>`.
- „CAN diag” zapisuje zawartość heartbeatów/NMT wszystkich węzłów (0x700–0x77F) i ponawia wpis co 5 min – widać, kto wysyła 0x757.
- Niesprawdzone kompilacją ESPHome (składnia YAML sprawdzona).

## v1.3 – Diagnostyka magistrali
- **Encja „CAN diag”**: podsłuch magistrali trafia do HA (historia = log) – zapisy panelu i innych węzłów (`ZAPIS id=… 0xIDX.sub dane=…`), nowe i zmienione rejestry SDO, zmiany bajtów PDO. Wstrzymana w czasie skanu i migawki. Dzięki niej rejestry zmieniane na panelu (np. Temp. maksymalna CWU, ustawienia kotła i CO) znajdujemy bez czytania logów ESPHome.
- **Encja „CAN ID ramek”**: lista unikalnych ID ramek widzianych na magistrali (do 60).
- **Tożsamość węzła (zakładka Sieć panelu)**: ESP odpowiada jako węzeł `can_node_id` (domyślnie 87) na zapytania SDO 0x1000, 0x1001, 0x1008 (nazwa „PelletCAN”, transfer segmentowany), 0x100A (wersja softu) i 0x1018. Wyłączenie: `can_identity: "false"`. Opcjonalny heartbeat NMT: `can_heartbeat: "true"`. **Niesprawdzone na kotle** – nie wiadomo, pod jakim numerem i w jaki sposób panel wylicza węzły.
- Nowe substitutions w `PelletCAN.yaml`: `can_node_id`, `can_identity`, `can_heartbeat`. Instrukcja szukania rejestrów: [docs/DIAGNOSTYKA.md](docs/DIAGNOSTYKA.md).
- Niesprawdzone kompilacją ESPHome (składnia YAML sprawdzona).

## v1.2 – Podajnik palnika
- Stały adres IP: zwykły blok `wifi: manual_ip` w `PelletCAN.yaml` (DHCP = usuń blok). Przełącznik `static_ip` przez Jinja w `packages` nie działa w ESPHome 2025.7 (próby: pakiet warunkowy i nazwa pliku z wyrażeniem) – wycofany. `refresh: 0s` – rdzeń zawsze świeży z GitHuba.
- **Nowe nazwy plików**: `esphome/PelletCAN.yaml` (Twój plik, dawniej `tekla-estyma.yaml`) i `esphome/PelletCAN_packages.yaml` (rdzeń, dawniej `tekla-estyma-core.yaml`). Nazwa urządzenia (`name: tekla-estyma`) bez zmian, więc encje w HA zostają.
- **Nowy podział plików (UWAGA: wymień swój plik `tekla-estyma.yaml`)**: plik użytkownika zawiera teraz wszystkie ustawienia (`substitutions`) oraz bloki `esphome` (nazwa), `esp32`, `logger`, `web_server`, `captive_portal`, `api` (klucz szyfrowania, `reboot_timeout`) i `packages`. Rdzeń `tekla-estyma-core.yaml` (CAN, encje, usługi `api: actions`, `ota`, `wifi`, skrypty) jest niezmienny i pobiera się z GitHuba przy każdej kompilacji; bloki są scalane przez ESPHome. Od teraz zmiany (nowe rejestry, poprawki) trafiają tylko do rdzenia – plik użytkownika zmieniasz wyłącznie dla swoich ustawień.
- **Test wyjść: 19. wyjście „Podajnik palnika”** (rejestr 0x2295, zapis U16: 256 = A, 257 = OFF, 258 = ON; potwierdzone testem na panelu 21.10). `set_output` przyjmuje teraz `out` 0–17 i 19 (18 = suwak WentWyc, `set_output_pct`); „Test wyjsc stany” ma 20 liczb (indeks 18 = suwak, 19 = Podajnik palnika). Brak rejestru poleceń nadal tylko dla Pompy CWU i Wymiennika.
- **Nowa encja „Podajnik palnika pracuje”** (ikona „2” na ekranie Palnik) z PDO modułu CAN IO BIG 0x456. **Bit jest hipotezą (bajt 0, bit 1)** – surowe bajty PDO 0x456 trafiają przy każdej zmianie do „SDO ostatni odczyt” (`PDO 0x456: …`), do potwierdzenia po wgraniu.
- **Stan mieszaczy** (cykliczny odczyt 0x22B9 i 0x216D): nowe sensory „Mieszacz CO1 stan” i „Mieszacz powrotu stan” (0 = stoi, 1 = zamyka, 2 = otwiera). Sterownik ustawia 257/258 sam, gdy zawór pracuje (potwierdzone na panelu 21.10: ikona zaworu ze strzałką). Dotyczy ikony zaworu na ekranie Kocioł.
- **CWU klucz 1 z zapisem**: `set_param` 44 Źródło (0x2214, 0 = Kocioł / 1 = Bufor), 45 Zwiększenie temp. źródła (0x2216, 5–20), 46 Delta załączenia pompy (0x2218, 2–20); zapis U16 = 256 + wartość. Nowe sensory „CWU zrodlo”, „CWU zwiekszenie temp. zrodla”, „CWU delta zalaczenia pompy”. Temp. maksymalna: rejestr nieznany.
- **Poziomy**: `set_param` 10–18 (histerezy kotła, histereza/kalibracja/tryb/temp. ręczna/krzywa CO1) wymagają teraz poziomu 0 (zgodnie z panelem; wcześniej 1).
- Niesprawdzone kompilacją ESPHome (składnia YAML sprawdzona).

## v1.1 – Test wyjść
- **Test wyjść z karty**: nowe akcje `set_output` (wyjście 0–17, tryb 0 = A, 1 = OFF/CLOSE, 2 = ON/OPEN) i `set_output_pct` (suwak WentWyc 0–100 %). Wymagany **poziom dostępu 2** (PIN klucza 2); blokuje je `mirror: true` albo `output_test_write: "false"`.
- **18 wyjść z rejestrami** (zapis U16: 256 = A, 257 = OFF/CLOSE, 258 = ON/OPEN): Podajnik 0x2259, Dmuchawa 0x2283, Zapalarka 0x2284, Pompa kotłowa 0x2286, Pompa solarna 0x311F, Pompy CO1–CO4 0x229D–0x22A0, Mieszacze CO1–CO4 0x22B9–0x22BC, Mieszacz powrotu 0x216D, Magazyn paliwa transporter 0x351E i podajnik 0x351F, Ruszt 0x2279, WentWyc tryb 0x2293 i suwak 0x2298 (256 + %). Rejestry wyznaczone testem na panelu 21.10. Brak rejestru (prawdopodobnie węzeł 86): Pompa CWU (polecenie), Wymiennik, Podajnik palnika.
- **Bezpieczeństwo**: wyjście ustawione na OFF/ON samo wraca na Automat po `test_revert_s` sekundach (domyślnie 120, 0 = wyłączone); akcja `test_reset` (bez PIN-u) wraca wszystkie od razu.
- **Stany**: akcja `test_refresh` czyta 19 rejestrów, wynik w nowym diagnostycznym sensorze „Test wyjsc stany” (19 liczb po spacji).
- **Plik użytkownika `tekla-estyma.yaml`** zawiera teraz wszystkie substitutions (Wi‑Fi, IP, PIN-y, flagi zapisu, CAN, diagnostyka) z domyślnymi wartościami i opisami – wszystko do zmiany w jednym miejscu.
- **Stały adres IP bez Jinja**: usunięty pakiet `network_ip` i substitution `static_ip` (ESPHome 2025.7 nie składał konfiguracji: „Platform missing”). Stały adres to teraz zwykły blok `wifi: manual_ip` w pliku użytkownika (DHCP = zakomentuj blok).
- Niesprawdzone kompilacją ESPHome (składnia YAML sprawdzona).

## v1.0 – pierwsze oficjalne wydanie
Wszystko, co powstało w wersjach roboczych, jest stanem v1.0:
- **Komunikacja z kotłem** po CAN (CANopen SDO, węzeł 4, 125 kbit/s) na XIAO ESP32-C6 + MCP2515: odczyt cykliczny parametrów pracy, zapis nastaw z karty (`set_param` 0–44), odczyt ustawień na żądanie (`param_refresh`).
- **Encje**: temperatury (kocioł, powrót, CO, CWU, zewnętrzna), stany palnika i pomp, moc [kW] i spalanie [kg/h] liczone w ESP, jasność płomienia, czas podawania, zasobnik, harmonogramy tygodniowe, historia alarmów (20 wpisów), zakaz rozpalenia, wersja firmware, poziom dostępu.
- **Poziomy dostępu PIN** (użytkownik, klucz 1, klucz 2) po stronie ESP; `set_param` odrzuca zapis parametru wyższego poziomu.
- **Tryb mirror** (`mirror`) – podgląd bez zapisów; opcja `dwa_obiegi_co`.
- **Sieć**: stały adres IP albo DHCP (`static_ip`), awaryjny punkt dostępu Wi‑Fi, hasła w `secrets.yaml`, uporządkowane substitutions (Wi‑Fi, API, OTA, `dwa_obiegi_co`, reszta).
- **Podział**: branch `main` – mały plik użytkownika `tekla-estyma.yaml` + rdzeń `tekla-estyma-core.yaml` pobierany z GitHuba przez `packages`; branch `test` – jeden pełny plik.
- **Diagnostyka**: skan i odczyt rejestrów SDO (`sdo_read`, `sdo_scan`, encja „SDO ostatni odczyt”), podsłuch IDENT/NMT.

<details><summary>Historia robocza przed v1.0 (numeracja wewnętrzna 2.x i wcześniejsza)</summary>

- **v2.32:** podział firmware: plik użytkownika `tekla-estyma.yaml` (substitutions, hasła z secrets, packages) i rdzeń `tekla-estyma-core.yaml` pobierany z GitHuba przy kompilacji (`packages: url/ref: main`). Branch `test` zawiera jeden pełny plik (v2.31). Niesprawdzone kompilacją ESPHome.

- **v2.31:** porządek w substitutions: najpierw Wi‑Fi i adres IP, potem klucz API i hasło OTA, potem `dwa_obiegi_co`, na końcu reszta; `static_ip` domyślnie `"true"`.

- **v2.30:** substitution `static_ip: "true"/"false"` przełącza stały adres IP (z `device_ip/device_gateway/device_subnet`) albo DHCP; realizowane pakietem `packages: network_ip` (Jinja) dodającym `wifi.manual_ip`. Wymaga ESPHome z obsługą Jinja w packages; niesprawdzone kompilacją.

- **v2.29:** adres IP domyślnie z DHCP – `device_ip/device_gateway/device_subnet` i blok `manual_ip` w wifi zakomentowane (stały adres opcjonalny; instrukcja w README, bez secrets).

- **v2.28:** hasło awaryjnej sieci `Tekla-Estyma Fallback` (`ap_pass`) przeniesione z secrets do `substitutions` (jawne, domyślnie 11223344); wpis `ap_pass` w secrets.yaml nie jest już potrzebny.

- **v2.27:** DIAGNOSTYKA zakladki Siec panelu: ESP loguje (ESP_LOGW "IDENT ..." i encja "SDO ostatni odczyt") kazda nowa ramke SDO o indeksach 0x1000/0x1008/0x1018 (zapytania i odpowiedzi dowolnego wezla) oraz nowe ramki NMT/heartbeat/emergency (0x000, 0x080-0x0FF, 0x700-0x77F), zeby ustalic jak panel pobiera nazwy urzadzen (cel: nazwa "CAN (ESPHome)" zamiast unknown). Skan wezla != 4 (sdo_scan z parametrem node) publikuje teraz odpowiedzi (takze abort i segmentowane) do "SDO ostatni odczyt". Bez wysylania czegokolwiek na CAN poza skanem.

- **v2.26:** AWARYJNY AP + captive_portal (brak sieci Wi-Fi -> siec "Tekla-Estyma Fallback", haslo w secrets: ap_pass, strona 192.168.4.1 do wpisania danych sieci); karta v9.2: autowykrywanie encji, tryb lite w jednej karcie.

- **v2.25:** HISTORIA ALARMOW Z KOTLA: ESP czyta caly bufor 20 alarmow kotla (kod 0x4010+i, poczatek 0x4024+i, koniec 0x4038+i; po starcie, przy nowym alarmie i akcja alarm_refresh) i publikuje 20 diagnostycznych text_sensorow "Alarm wpis 1..20" w formacie "kod N (opis)|poczatek unix|koniec unix" (pusty = "-"); karta nie korzysta juz z rekordera HA.

- **v2.24:** ODCZYT USTAWIEN: po starcie wszystkie ustawienia (najpierw poziom 0, potem klucz 1 i 2); poziom 0 (0x2270/0x2271/0x2273/0x2212/0x2210/0x300D) czytany tez cyklicznie; klucz 1 i 2 na zadanie - po wpisaniu PIN-u (automatycznie, akcja unlock) i po param_refresh.

- **v2.23:** MIGAWKA KATALOGOWA rozszerzona z 538 do 593 rejestrow (dodane 55 rejestrow wezla 4 znalezionych od v2.20: m.in. 0x2116, 0x2151, 0x2216, 0x2260, 0x226E-0x2271, 0x2296, 0x2999, 0x300F, 0x3524-0x3526, 0x3701, 0x7D1-0x7E1, 0xBB9-0xBBB); lista CAT = suma rejestrow z katalogu docs/rejestry (wezel 4).

- **v2.22:** sygnatura konfiguracji - ukryty diagnostyczny text_sensor "Sygnatura konfiguracji" (autor: Roman Gorz); tekst zlozony z 3 kawalkow zaszyfrowanych XOR, skladany dopiero w kodzie; encja domyslnie wylaczona (disabled_by_default) i w kategorii diagnostic.

- **v2.21:** usunieta "CWU antylegionella" (rejestr 0x216F okazal sie NIE antylegionella: odczyt 256 przy wlaczonej na panelu, zapis 257 bez efektu) - sensor, odczyt (boot, param_refresh), set_param key 44 (klucze 0..43). Prawdziwy rejestr antylegionelli nieznany (moze byc tylko w panelu); w karcie "-".

- **v2.20:** MENU PALNIKA (potwierdzone zmianami wartosci na panelu): odczyt i zapis 22 parametrow (set_param key 22..43): 22 wstepna dawka paliwa 0x2256 (0..200 s), 23 podawanie max 0x2257 (1,0..15,0 s, raw/10), 24 prog foto 0x226A (5..100), 25 moc dmuchawy rozpalanie 0x2289, 26 rozzarzanie 0x3704, 27 wygaszanie 0x300C (0..100 %), 28 czas rozzarzania 0x2290 (0..20 min, flaga+bajt; potwierdzone: 2->7 = raw 258->263), 29 rozzarzanie paliwo 0x299A (20..100 %), 30 czas wygaszania 0x226B (1..15 min), 31 sterowanie lambda 0x3605 (0/1; czujnik nie zamontowany), 32/33 tlen dla mocy 30/100 % 0x214E/0x2152 (5,0..15,0 %), 34 liczba czyszczen rusztu 0x2258 (0..10), 35 odstep czyszczenia 0x2999 (1..12 h), 36 czas pauzy 0x3715 (0..60 min), 37 moc w pauzie 0x3716 (5..30 %), 38 dmuchawa w pauzie 0x3717 (10..50 %), 39 bezwladnosc palnika 0x2153 (1..60 min), 40 czas ruchu rusztu 0x3003 (0..60 s, raw/10), 41 podawanie palnika 0x370B (50..300 % podajnika zasobnika), 42 okres podajnika zasobnika 0x3700 (5..180 s), 43 minimalne obroty dmuchawy 0x300E (0..5 x100). Nowe odczyty na zywo: "Palnik jasnosc plomienia" 0x2250 (%), "Palnik czas podawania paliwa" 0x226D (raw/10 s). Liczone w ESP (bez szablonow w HA): "Palnik moc" [kW] = test paliwa x podawanie max / okres x wartosc opalowa x sprawnosc_kw (0,90) x moc palnika % (potwierdzone na panelu: 7,5/8,0/9,4 kW) oraz "Palnik spalanie" [kg/h] = kW / (wartosc opalowa x 0,85) - wspolczynnik 0,85 EMPIRYCZNY (dopasowanie do panelu, niewyjasniony; substitution burner_eff_fuel). Poprawka migawek: rejestry obslugiwane w switch (case) trafiaja podczas migawki rowniez do "SDO ostatni odczyt". ODCZYT USTAWIEN NA ZADANIE: ustawienia (menu palnika, moc min/max, korekta powietrza, krzywa dmuchawy, histerezy kotla/CWU, CO1 krzywa/tryb/histereza/kalibracja, zagrzej teraz, priorytet CWU) NIE sa juz czytane cyklicznie - czytane raz po starcie (poziom 0), po zapisie (odczyt zwrotny) oraz po unlock / akcji param_refresh (patrz POZIOMY DOSTEPU). Cyklicznie (na zywo) zostaja wartosci z ekranow glownych: temperatury, tryby, stany, zbiornik, alarmy, moc palnika, jasnosc plomienia, czas podawania + 0x2272/0x2292/0x2257/0x3700 do liczenia mocy kW. POZIOMY DOSTEPU: substitutions pin_installer1 (klucz 1) i pin_installer2 (klucz 2); akcja unlock {pin} ustawia poziom (kazdy inny PIN = 0 = uzytkownik), czujnik "Poziom dostepu" (0/1/2); set_param odrzuca zapis parametru wyzszego poziomu niz biezacy (poziomy wg menu panelu: 0 = moc min/max, wartosc opalowa, korekta powietrza, test paliwa, CWU; 1 = klucz 1: krzywa dmuchawy, podawanie max, wstepna dawka, prog foto, moce dmuchawy, rozzarzanie, wygaszanie, lambda, tlen, czyszczenia, odstep czyszczenia, pauza, histerezy kotla, CO1; 2 = klucz 2: bezwladnosc, czas ruchu rusztu, pod. palnika, okres podajnika, min. obroty dmuchawy). Po starcie odczytywany tylko poziom 0; po unlock i akcji param_refresh (bez parametrow; karta: klik w nazwe dnia tygodnia) odczyt ustawien do biezacego poziomu; po zapisie odczyt zwrotny parametru. Poziom resetuje sie po restarcie ESP oraz po ${pin_autolock_min} min bezczynnosci (substitution pin_autolock_min, domyslnie 5; bezczynnosc = brak unlock/set_param/param_refresh); karta dodatkowo blokuje po 5 min bezczynnosci i przy odswiezeniu strony (unlock z pustym PIN). ANTYLEGIONELLA: "CWU antylegionella" 0x216F (256 wyl. / 257 wl.; wykryte roznica migawek wl./wyl.), set_param key 44 (0/1), czytane przy param_refresh group 1. Krzywa "wentylator wspomagajacy" - rejestry niepotwierdzone, brak zapisu.

- **v2.19:** diagnostyka harmonogramu kotla: odczyt 0x2209..0x220F (takze reczny sdo_read) trafia do "SDO ostatni odczyt" (surowa wartosc + bajty ramki), zeby sprawdzic czemu wychodzi FFFFFF (panel pokazuje 5-21).

- **v2.18:** CO obwod 1 i CWU - odczyty i zapis (potwierdzone zmianami na panelu): "CO1 histereza" 0x22BD (flaga+bajt, 256+10*C, 0..5 C), "CO1 kalibracja czujnika" 0x22C1 (int16 /10, -3..3 C), "CO1 tryb pracy" 0x2142 (256 reczny / 257 pogodowy), temperatura reczna 0x2146 (POPRAWKA: flaga+bajt = raw-256 w C, nie /10; 20..80), krzywa pogodowa -20/0/+10 C = 0x22C5/0x22C9/0x22CD (flaga+bajt, 20..80), "CWU histereza" 0x2212 (0..20), "CWU zagrzej teraz" 0x2210 (256/257), "CWU priorytet" 0x300D (256/257). set_param key 12..21. Antylegionella - rejestr nie znaleziony.

- **v2.17:** Nowe odczyty: "Temperatura powrotu" 0x4000 (raw/10 C, potwierdzone porownaniem z panelem: 51,4/51,9/52/52,1/52,3), "Histereza zalaczenia kotla" 0x2208 i "Histereza wylaczenia kotla" 0x2291 (zwykle liczby calkowite 0..20 C, potwierdzone zmiana na panelu 15->16 i 5->6). set_param: key 10 = histereza zalaczenia, key 11 = histereza wylaczenia (0..20 C).

- **v2.16:** MIRROR WYLACZONY (mirror: "false") - jedyna blokada zapisu to substitution mirror (mirror: true blokuje wszystkie zapisy poza wlacz/wylacz i potwierdzeniem alarmu, rowniez sdo_write). Nowa akcja "set_param" (key, value): zapis ustawien palnika z limitami: 0 Moc min 0x2270 (30..100 %), 1 Moc max 0x2271 (30..100 %, >= min), 2 Wartosc opalowa 0x2292 (2,0..10,0 kWh/kg), 3 Korekta powietrza 0x2273 (-10..40 %), 4 Ilosc paliwa test 0x2272 (5..100 kg/h), 5..9 krzywa dmuchawy 0x2261..0x2265 (0..100 %, punkty mocy kotla 20/40/60/80/100 %). Nowe odczyty "Dmuchawa modulacja 20/40/60/80/100 %". Odczyty: "Moc min" 0x2270 i "Moc max" 0x2271 [%] (flaga 0x01 + bajt, 30..100, potwierdzone zdjeciami panelu), "Wartosc opalowa" 0x2292 [kWh/kg] (raw-256 = kWh/kg x10; potwierdzone testem zmiany na panelu 4,6 -> 4,7; 0x2289 sie nie zmienia

- **v2.15:** substitution "mirror" (true = karta tylko jako lustro Igneo Touch; zapis tylko wlacz/wylacz kociol + potwierdzenie alarmu; encje zapisu - selecty trybow CO/CWU oraz przyciski podajnika/dmuchawy - sa internal, czyli niewidoczne w HA; akcje set_* odrzucaja zapis; false = pelne sterowanie wg flag *_write); binary_sensor "Tryb mirror"; text_sensor "Wersja firmware" (substitution fw_version).

- **v2.14:** statystyki kotla jako JEDEN tekstowy sensor "Statystyki kotla": 8 liczb po spacji (rozpalenia, sr. czas rozpalania s, podajnik1 h, podajnik2 h, paliwo kg, czyszczenia, przegrzania, zaniki zasilania; "--" = brak odczytu)

- **v2.13:** sdo_scan z parametrem node (skan innego wezla CANopen, np. 86 = modul CAN IO BIG; zadania 0x600+node, odpowiedzi 0x580+node); reszta jak v2.12

- **v2.12:** statystyki kotla 0x3608/0x3609/0x3611/0x3612/0x3507/0x3618/0x3619/0x362A (czytane przy schedule_refresh); zapis z karty: harmonogramy (CWU/CO/kociol), zadane komfort/eco CO i CWU, tryb zadawania kotla (0x2002) + reczna zadana (0x2003).
  Flagi: schedule_write, setpoint_write (w substitutions; "false" = sam podglad). Harmonogramy czytane na zadanie (akcja schedule_refresh), nie cyklicznie.

- **v2.11:** harmonogramy (odczyt co ~2 min, surowe rejestry CWU 0x2154-0x2159,0x2160 i CO 0x2126-0x2141 jako tekst heksadecymalny)

- **v2.10:** wejscia 0x2006 (zakaz rozpalenia) i 0x2301 (zgoda regulatora) tylko jako czujniki (odczyt; zapis przez SDO nie dziala - usuniety)

</details>
