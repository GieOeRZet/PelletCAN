# Diagnostyka (firmware ≥ 1.4.14)

Od wersji 1.4.14 firmware jest domyślnie „cichy”: nie ma migawek (`sdo_snapshot_*`) ani widocznych w HA encji „CAN diag” i „CAN ID ramek”. Do szukania rejestrów służy skaner opisany w **[rejestry/README.md](../rejestry/README.md)** (akcje `sdo_scan`, `sdo_read`, `sdo_write`, `sdo_scan_stop`, wyniki w encji „SDO ostatni odczyt”).

## Przełączniki w `PelletCAN.yaml`
| Ustawienie | Domyślnie | Działanie |
|---|---|---|
| `diag_log` | `"false"` | `"true"`: do logu ESPHome i „SDO ostatni odczyt” trafiają dodatkowe wpisy: `NMT` (heartbeat/boot-up innych węzłów), `IDENT` (zapytania panelu o tożsamość węzłów, zakładka Sieć), zmiany `PDO 0x456/0x356`, raport `SKAN SIECI`, ramki `FEED PDO 0x2D7`. |
| `sniff` | `"false"` | `"true"`: podsłuch SDO innych węzłów w logu ESPHome – m.in. **zapisy panelu** (`SNIFF ZAPIS … id=0x604 0xIDX.sub dane=CS IL IH SUB V0 V1 V2 V3`; CS 2F = 1 B, 2B = 2 B, 23 = 4 B; indeks = IL + IH w odwróconej kolejności, wartość = V0 V1… młodszy bajt pierwszy). Przydatne, gdy chcesz zobaczyć, który rejestr zapisuje panel po zmianie nastawy. |
| `can_debug` | `"false"` | `"true"`: log wszystkich odebranych ramek CAN. Tylko do diagnozy. |
| `can_node_id`, `can_identity`, `can_heartbeat` | `90`, `"true"`, `"true"` | ESP jako węzeł na magistrali (zakładka Sieć panelu: „PelletCAN”, wersja softu). 86 i 87 są zajęte przez urządzenia kotła. |

Po diagnozie przywróć `"false"`.

## Typowe zadania
1. **Rejestr nastawy zmienianej na panelu** – metoda różnicowa ze skanerem ([rejestry/README.md, sekcja 3](../rejestry/README.md#3-jak-znaleźć-rejestr-brakującej-pozycji-menu-metoda-różnicowa)). Pomocniczo `sniff: "true"` pokaże zapis panelu.
2. **Wymiennik / węzeł 86** – skan węzła 86: `sdo_scan` z `from_index: 25088`, `to_index: 25632` (0x6200–0x6420), `sub: 1`, `node: 86`; przerwanie `sdo_scan_stop`.
3. **Zakładka Sieć panelu** – po wgraniu firmware wejdź w Menu → Sieć; gdy nadal „Unknown”, włącz `diag_log: "true"` i sprawdź wpisy `IDENT …` (jakie węzły i indeksy pyta panel).
