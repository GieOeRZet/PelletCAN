# Changelog – PelletCAN-card

Historia zmian firmware: [CHANGELOG-firmware.md](CHANGELOG-firmware.md).

## v1.32 – Opcje w edytorze i grafiki suwaka
- Grafiki: pelne – przełącznik Kocioł (OFF/ON) i uchwyt suwaków trybu (CO, CWU) z oryginalnych bitmap panela (184/185, 70). Edytor karty: nowe pola Grafiki panela (domyślne/pełne), Obraz kotła (11/12/13), Tryb lite i Tryb demo. Poprawka: przy grafiki: pelne bojler CWU wraca do własnego obrazu (img/bojler.png) zamiast sprite'a zbiornika.

## v1.31 – Opcje w edytorze
- Edytor karty: nowe pola Grafiki panela (domyślne/pełne), Obraz kotła (11/12/13), Tryb lite i Tryb demo. Poprawka: przy grafiki: pelne bojler CWU wraca do własnego obrazu (img/bojler.png) zamiast sprite'a zbiornika.

## v1.30 – Pakiet grafik
- Pakiet grafik panela (img/panel/, 188 plików) jest teraz w paczce karty – zbiornik paliwa działa od razu; resztę (wentylator, podajniki, zawór, grzałka, kocioł, palnik) włącza opcja grafiki: pelne.

## v1.29 – Animacja grzałki
- Grzałka zapalarki: animacja jak w panelu – klatki 65→66→67→66→65 (tam i z powrotem, 2 s) zamiast pulsowania z trzech klatek.

## v1.28 – Obraz bojlera w pakiecie
- Domyślny obraz bojlera CWU to teraz img/bojler.png (grafika z panelu w pełnej rozdzielczości); wektor bojler.svg zostaje jako zapasowy.

## v1.27 – Obraz bojlera
- Bojler CWU: własny obraz (img/bojler.png) nie rozciąga się już do ramki – zachowuje proporcje. Pełna rozdzielczość np. 3× (przeskalowany wektorowo-ostro) wskazana dla ekranów 2×.

## v1.26 – Test wyjść: wymiennik i mieszacze
- Test wyjść: aktywny wiersz Wymiennik (rejestr 0x2285), mieszacze CO1–CO4 działają przez rejestry testowe 0x214A–0x214D. Wymaga firmware ≥ 1.4.22.

## v1.25 – Tłumaczenia
- Tłumaczenia nowych napisów (nastawy i odczyty z kotła, krzywa wentylatora spalin, alarm/cisza, statystyki, paliwo) we wszystkich 11 językach.

## v1.24 – Odczyty i nastawy palnika z kotła
- Statystyki: **Moc palnika z kotła**, **Zużycie paliwa z kotła**, **Czas do czyszczenia rusztu**, **Wentylator spalin [%]**.
- Palnik → NASTAWY (klucz 1): **Moc nominalna**, **Dawka wstępna [g]**, **Min./Max. temp. spalin**, **Interwał czyszczenia wymiennika**. Wymaga firmware ≥ 1.4.21.

## v1.23 – Nastawy z firmware panela
- Menu Ciepła woda: **Temp. maksymalna** i **Antylegionella** (odczyt i zapis). Palnik → NASTAWY (klucz 1): **Wentylator spalin – krzywa 1–5**. Konfiguracja: **Alarm dźwiękowy**, **Cisza od / do** (dotąd atrapa). Wymaga firmware ≥ 1.4.18.
- Poprawka błędu z 1.22: przy obecnym pakiecie grafik zdarzenie `tekla-img` zapętlało się (przepełnienie stosu w konsoli).

## v1.22 – Pakiet grafik: domyślnie tylko zbiornik paliwa
- Z pakietu `img/panel/` karta domyślnie bierze tylko **zbiornik paliwa** w oknie Paliwo (pliki 48, 49, 50, 54). Wystarczy skopiować te 4 pliki; wentylator, podajniki, zawór, grzałka i obrazy kotła/palnika/bojlera pozostają wektorami.
- Opcja `grafiki: pelne` włącza cały pakiet jak w 1.20–1.21.

## v1.21 – Grzałka pulsuje
- Ikona grzałki zapalarki animowana jak na panelu: 65→66→67→65 (gdy `Palnik zapalarka` > 0).

## v1.20 – Pakiet oryginalnych grafik panela
- Opcjonalny katalog `img/panel/NNN.png` (numery jak w tablicy bitmap panela; generator: `python3 tools/pakiet_grafik.py FW2213TK.bin`). Z pakietem: animowany wentylator (8–10), podajniki 1/2 (36–38 / 40–42), zasobnik 48/49 z suwakiem 50 i korpusem 54, zawór mieszacza 105 ze strzałkami 106/107, grzałka zapalarki 65–67, kocioł 11–13 (`boiler_image`), palnik 17, bojler 14. Bez pakietu działają wektory. Grafiki są własnością Estymy – katalog jest w `.gitignore`.
- Grzałka zapalarki wymaga firmware ≥ 1.4.17.

## v1.19 – Statystyki: średnia moc, tlen, energia
- Statystyki pokazują **Średnią moc z 50 h**, **Średni tlen** (30/50/70/90 %) i **Energię całkowitą [kWh]**; wartość 0 (brak sondy lambda / licznika energii) = „-”. Wymaga firmware ≥ 1.4.16.

## v1.18 – Statystyki: prognoza paliwa, tryb demo
- Statystyki: **Zużycie paliwa 24 h [kg]** i **Paliwo wystarczy na [dni]** (z ESP, „-” gdy brak danych). Wymaga firmware ≥ 1.4.15.
- **Tryb demo**: `demo: true` w konfiguracji karty pokazuje dane przykładowe bez ESP i HA (zrzuty do README, test wyglądu). Strona `docs/demo.html`.

## v1.17 – Kocioł NASTAWY: Wybieg pompy i Rezerwa paliwa stop
- Menu → Kocioł → NASTAWY (od poziomu 1): **Wybieg pompy** (0–120 min) i **Rezerwa paliwa stop** (0–100 kg) odczytywane i zapisywane. Menu Kocioł NASTAWY ma teraz wszystkie pozycje. Wymaga firmware ≥ 1.4.13.

## v1.16 – Ogrzewanie 1: Czujnik pokojowy
- NASTAWY CO (od poziomu 1): **Czujnik pokojowy** (brak / CTP1 / CTP2 / videROOM / termostat / CAN) odczytywany i zmieniany. Menu CO ma teraz wszystkie pozycje. Wymaga firmware ≥ 1.4.12.

## v1.15 – Ogrzewanie 1: Źródło i Czujnik CO
- NASTAWY CO (od poziomu 1): **Źródło** (Kocioł / Bufor) i **Czujnik CO** są przełączane i odczytywane. Czujnik pokojowy nadal „-”. Wymaga firmware ≥ 1.4.11.

## v1.14 – Ogrzewanie 1: przełączniki
- NASTAWY CO (od poziomu 1): **Stała pompa** i **Obniżenie Tco dla ochrony powrotu** są przełączane i odczytywane. Wymaga firmware ≥ 1.4.10.

## v1.13 – Ogrzewanie 1: NASTAWY (klucz 1)
- Menu → Ogrzewanie 1 → NASTAWY (od poziomu 1): odczyt i zapis **Zwiększenie temp. źródła**, **Temp. maksymalna**, **Wsp. korekcji t. CO**, **MAX Tzew pomp komf./ekon.**, **Obniżenie temperatury CO**, **MIN temperatura CO pomp** i **Czas mieszacza**. Pozostałe (Źródło, Czujnik pokojowy, Czujnik CO, Stała pompa, Obniżenie Tco dla ochrony powrotu) nadal „-”. Wymaga firmware ≥ 1.4.9.

## v1.12 – Kocioł NASTAWY: pompy, powrót, mieszacz
- Menu → Kocioł → NASTAWY (od poziomu 1): **Minimalna temp. pomp** (20–70 °C), **Minimalna temp. powrotu** (35–75 °C) i **Czas mieszacza** (60–360 s) są teraz odczytywane i zapisywane. **Wybieg pompy** i **Rezerwa paliwa stop** nadal „-” (rejestry nieznalezione). Wymaga firmware ≥ 1.4.8.

## v1.11 – Pompa CWU w Teście wyjść
- **Pompa CWU** w Teście wyjść jest teraz aktywna (A / OFF / ON), rejestr 0x2296 znaleziony różnicowo 22.10 (ON = 258, A = 256). Stan Podajnika palnika w Teście wyjść jest odczytywany (karta czyta 21 wartości zamiast 19). Wymaga firmware ≥ 1.4.7.

## v1.10 – Konfiguracja
- Przywrócona pozycja **Konfiguracja** w menu (od poziomu 1, przed Testem wyjść). Ekran pokazuje: Język, Alarm dźwiękowy (przełącznik jak na panelu, bez rejestru), Tryb pracy karty (sterowanie / lustro), Węzeł ESPHome, Poziom menu, wersje firmware i karty.

## v1.9 – Przyciski + / − w oknie Paliwo
- Przyciski + i − zmieniają ilość paliwa w zbiorniku o 1 kg (przytrzymanie: powtarzanie). Wartość i zapełnienie (kg / pojemność) pokazują się od razu, zapis do kotła (rejestr 0x3601) idzie po 0,6 s od ostatniego kliknięcia. W trybie lustra nieaktywne. Wymaga firmware ≥ 1.4.6.

## v1.8 – Drobne poprawki paska
- Napis MENU jest częścią ikony: ma dokładnie szerokość trzech linii (niezależnie od czcionki), a odstęp od dolnej linii jest taki jak odstęp między liniami.
- Ilość paliwa (np. „81kg") większą czcionką, górna krawędź napisu bez zmian.

## v1.7 – Ikony dolnego paska jak w panelu
- Ikony dolnego paska (zasobnik, płomień, grzejnik, kran, power, menu) mają kształty prześledzone ze zdjęcia panelu zamiast poprzednich uproszczonych; napis MENU pogrubiony, ilość paliwa wąską czcionką jak na panelu. Zasobnik wypełnia się nadal procentowo (5 rzędów kropek).

## v1.6 – Dolny pasek jak w panelu
- Dolny pasek odwzorowany 1:1 ze zdjęcia panelu: rozmiary i położenie ikon, napis MENU (mniejszy, pod liniami), czcionka ilości paliwa, wysokość i szerokość wskaźników. Ikona zasobnika wraca do poprzedniego rozmiaru i jest nieco obniżona; wypełnienie procentowe bez zmian.
- **Wskaźnik nad palnikiem**: zielony; pulsuje przy rozpalaniu i rozżarzaniu, świeci ciągle przy modulacji (jak dioda na obudowie), poza tym zgaszony.
- **Wskaźniki nad CO i CWU**: zielone, gdy pracuje odpowiednia pompa; gdy nie – zgaszone.

## v1.5 – Poprawki wyglądu
- **Okno Paliwo**: licznik sekund przy przycisku podajnika pokazuje 30 s (przy wyłączonym kotle 600 s). Po naciśnięciu przycisku odlicza co 1 s; po ponownym naciśnięciu (stop) lub końcu odliczania wraca do wartości początkowej. Przycisk uruchamia podajnik (encja „Podajnik: Podaj paliwo”), w trybie lustra nieaktywny.
- **Dolny pasek**: napis MENU ma dolną krawędź na wysokości dołu ikony grzejnika; ikona zasobnika powiększona do tej samej wysokości.
- **Przycisk MENU**: zamiast zielonej kropki pulsujący zielony wskaźnik (jak nad przyciskiem power), gdy jest dostępna aktualizacja.
- **Test wyjść**: tło i wiersze w stylu pozostałych ekranów (gradient, delikatne separatory), pola wyboru w kolorze strzałek z historii alarmów; mniejsze podpisy CLOSE/OPEN.

## v1.4 – Tłumaczenia
- **Języki interfejsu**: PL, EN, DK, DE, SE, LT, SK, CZ, ES, RO, EST. Wybór w edytorze karty (pole „Język / Language”, także „Auto” = język Home Assistant) albo w YAML: `language: en` (kody: `pl en da de sv lt sk cs es ro et`; aliasy `dk se cz est`).
- Nowy plik `dist/pelletcan-lang.js` (generowany z `docs/lang/pelletcan-lang.txt` skryptem `tools/gen_lang.py`) – ~245 tekstów × 10 języków (ekrany, NASTAWY, statystyki, test wyjść, alarmy, nazwy dni). Brak tłumaczenia = tekst polski. Dopisanie/poprawka tłumaczenia: edytuj plik .txt i uruchom `python3 tools/gen_lang.py`.
- Wiersz „Język” w menu pokazuje aktualny język. Z menu usunięto pozycję „Konfiguracja” (decyzja: za dużo rzeczy, które mogą coś namieszać).
- Wymaga wgrania obu plików: `pelletcan-card.js` i `pelletcan-lang.js` (HACS robi to sam).

## v1.3 – Podajnik palnika
- Wersja karty 1.3 wymaga firmware ≥ 1.2 (karta bez zmian względem firmware 1.3) (nowe encje: Podajnik palnika pracuje, stany mieszaczy, CWU Źródło/Zwiększenie/Delta). Bez nich pozycje pokazują „-”.
- **Ekran Palnik: ikona „2”** (podajnik palnika) na dolnym pasku obok ikon wentylatora i podajnika „1” (kolejność jak na panelu). Encja „Podajnik palnika pracuje” z firmware ≥ 1.2.
- **NASTAWY przebudowane według zdjęć panelu** (poziomy tylko 0 i 1; poziom 2 w tych menu nie występuje): Kocioł (poziom 0: Temperatura zadana, Histereza załączenia/wyłączenia; klucz 1: Minimalna temp. pomp, Wybieg pompy, Minimalna temp. powrotu, Czas mieszacza, Rezerwa paliwa stop), Ogrzewanie 1 (histereza, kalibracja, tryb, krzywa pogodowa na poziomie 0; reszta pod kluczem 1), Woda (klucz 1: Źródło, Zwiększenie temp. źródła, Delta załączenia pompy – z zapisem; Temp. maksymalna bez rejestru). Pozycje bez znanego rejestru są przyciemnione i pokazują „-”.
- Histerezy kotła i ustawienia CO1 są teraz dostępne bez PIN-u (poziom 0), zgodnie z panelem.
- **Ekran Kocioł: ikona zaworu (mieszacza)** pojawia się tylko gdy mieszacz pracuje, ze strzałką w lewo (zamyka) lub w prawo (otwiera), jak na panelu; dane z firmware ≥ 1.2 („Mieszacz CO1 stan”, „Mieszacz powrotu stan”).
- **Test wyjść: Podajnik palnika sterowalny** (wyjście 19, rejestr 0x2295) – już nie tylko podgląd.
- **Edytor karty**: YAML odzwierciedla edytor (wykryte encje wpisują się automatycznie do `entities:`; zmiana urządzenia/prefiksu wykrywa je od nowa).
- Czas podawania na ekranie Palnik zaokrąglony do 1 miejsca (wcześniej surowa liczba zmiennoprzecinkowa nachodziła na obraz).

## v1.2 – Test wyjść 1:1 z panelem
- Ekran Test wyjść przerysowany według zdjęć panelu (perspektywa wyprostowana, wymiary w % szerokości ekranu): wiersz 10,55, pola wyboru 6,2 × 6,2, kolumny A/OFF/ON co 8,3, niebieskie tło listy, cyjanowe separatory, żółto-zielony ptaszek, biała gałka suwaka.
- Wszystkie 21 pozycji w kolejności panelu, w tym suwak „Dm.” (pokazany, bez rejestru – nieaktywny) i suwak „WentWyc” (rejestr 0x2298). Bez dodatkowych lampek i wierszy; pozycje bez znanego rejestru są przyciemnione.
- Nagłówek pokazuje bieżący poziom dostępu (jak ikona klucza na panelu).

## v1.1 – Test wyjść
- **Ekran Test wyjść jak na panelu Igneo Touch**: 21 pozycji w kolejności z panelu, A/OFF/ON i A/CLOSE/OPEN (ruszt, mieszacze), suwak WentWyc, zaznaczenie stanu odczytanego z kotła. Sterowanie tylko na poziomie 2 (PIN klucza 2); na poziomie 1 podgląd.
- Wyjścia wracają na Automat po wyjściu z ekranu (i po 2 min w firmware). Pompa CWU, Wymiennik i Podajnik palnika są tylko do podglądu (rejestr nieznany).
- Wymaga firmware ≥ 1.1 (akcje `set_output`, `set_output_pct`, `test_refresh`, `test_reset`, sensor „Test wyjsc stany”).

## v1.0 – pierwsze oficjalne wydanie
Wszystko, co powstało w wersjach roboczych, jest stanem v1.0:
- **Wierna replika panelu Igneo Touch** (typ `custom:pelletcan-card`; stary `custom:tekla-panel-card` działa dalej): ekran główny, Ogrzewanie, Woda, Kocioł, Palnik, Menu, Historia alarmów, Informacje o programie, harmonogramy tygodniowe (paski, edycja), Test wyjść i Statystyki (poziom 1).
- **Ustawienia (NASTAWY)** kotła, palnika (22 parametry), CO obwód 1 i CWU z oknami edycji (suwak, +/–, przełączniki); zapis przez usługi ESPHome.
- **Poziomy dostępu z PIN** (użytkownik / klucz 1 / klucz 2), blokada po bezczynności; tryb `lite: true` (zawsze poziom 0, bez PIN-u).
- **Automatyczne wykrywanie encji** po prefiksie nazwy (brak encji = „-”), wizualny edytor karty.
- **Historia alarmów** czytana z bufora kotła (20 wpisów), przewijanie strzałkami, potwierdzanie alarmu.
- **Ekran INFO**: autor, wersje firmware i karty, zielona dioda i changelog przy dostępnej aktualizacji (z `version.json` w repo), „Odrzuć aktualizację”, dyskretny przycisk wsparcia.
- **Grafiki** kotła, palnika i bojlera z folderu `img/` (można podmienić).
- **Instalacja przez HACS** (repozytorium niestandardowe, kategoria Dashboard), jeden zasób; ścieżki względne.

<details><summary>Historia robocza przed v1.0 (numeracja wewnętrzna 9.x i wcześniejsza)</summary>

- **v9.6** – projekt nazywa się teraz **PelletCAN** (nowe repozytorium `GieOeRZet/PelletCAN`): plik karty `pelletcan-card.js`, katalog HACS `pelletcan`, dodatkowy alias typu `custom:pelletcan-card` (typ `custom:tekla-panel-card` działa dalej); nazwa karty: **PelletCAN-card**.
- **igneo-card v9.5** – instalacja przez HACS (katalog `dist/`, `hacs.json`); karta sama wykrywa swój katalog (rdzeń i grafiki ładowane z tego samego miejsca).
- **igneo-card v9.4** – dyskretny przycisk wsparcia na dole ekranu INFO.
- **igneo-card v9.3** – informacja o aktualizacjach: zielona dioda przy ikonie menu i zielony napis „Informacje o programie”, gdy `version.json` w repo ma nowszą wersję firmware lub karty; ekran INFO przebudowany (autor, wersje, changelog aktualizacji, przycisk „Odrzuć aktualizację”, zapamiętany w przeglądarce); nowa rola encji `fw_ver` (Wersja firmware).
- **igneo-card v9.2** – automatyczne wykrywanie wszystkich encji po prefiksie (brak encji = „-”, bez błędów); tryb `lite: true/false` w jednej karcie (poziom 0, bez „Poziom menu”); nowy edytor wizualny podzielony wg ekranów i menu; osobny plik lite usunięty (typ `tekla-panel-card_lite` zostaje jako alias).
- **igneo-card v9.1** – historia alarmów z kotła (encje „Alarm wpis 1..20”, firmware ≥ 2.25); rekorder HA tylko jako zapas.
- igneo-card v9.0 – wszystkie poprawki i moduły scalone w jeden plik wejściowy (zamiast łańcucha plików v78–v86); lite wydzielone do `igneo-card-lite.js`.
- v8.6 – linia autora na ekranie INFO.
- v8.5 – grafiki kotła, palnika i bojlera z plików w `img/`.
- v8.4 – historia alarmów z historii HA, przycisk POTWIERDŹ.
- v8.0–v8.3 – poziomy dostępu z ESP (PIN), menu wg poziomu, nastawy palnika/CO/CWU.

</details>
