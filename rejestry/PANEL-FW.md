# Firmware panelu IgneoTouch (FW2213TK.bin) – analiza

- STM32F4, TouchGFX, obraz surowy pod 0x08000000, teksty UTF-16 (PL/EN/CZ/RO/LT/EE/ES).
- Tablica par (indeks CANopen, ID parametru panela): 420 par, offset 0x37576-0x37C0A -> `panel-fw-mapa-indeks-id.csv`.
  Potwierdzone: 0x3708->ID 23, 0x2207->18, 0x216C->33, 0x3604->363.
- 74 indeksy, ktorych nie ma w naszym katalogu (status BRAK), sa dowodem, ze rejestr istnieje; nie znamy jeszcze nazw/zakresow.
- Laczenie ID -> tekst/zakres NIE znalezione (brak wprost wskaznikow w obrazie; teksty nie sa w kolejnosci ID).
- Teksty menu istnieja: Antylegionella, Alarm dzwiekowy, Histereza, Wymiennik, Rezerwa paliwa, Wybieg pompy [min] - bez powiazania z indeksem.
- Wniosek: nowe indeksy (np. 0x3721-0x3750, 0x228D-0x228F, 0x218A-0x218C) warto skanowac sdo_scan i badac metoda roznicowa.
