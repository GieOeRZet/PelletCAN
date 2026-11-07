Nastawy z panela, odczyty palnika, test wyjść i grafiki
## Co nowego
- **Karta v1.30:** nastawy CWU (temp. max, antylegionella), krzywa wentylatora spalin, alarm dźwiękowy i cisza, odczyty i nastawy palnika z kotła (moc, zużycie, dawka wstępna, temp. spalin, interwał wymiennika), tłumaczenia nowych napisów (11 języków), obraz bojlera CWU, animacja grzałki zapalarki, pakiet grafik panela w `img/panel/`.
- **Firmware v1.4.22:** zapis antylegionelli bez PIN-u, cykliczny odczyt nastaw co 60 s, test wyjść: wymiennik (0x2285) i mieszacze CO1–CO4 przez rejestry testowe 0x214A–0x214D (do sprawdzenia na kotle).
- Wymień pliki ESPHome (`PelletCAN_packages.yaml`) na nowe i zaktualizuj kartę w HACS.

Szczegóły: [CHANGELOG.md](CHANGELOG.md) i [CHANGELOG-firmware.md](CHANGELOG-firmware.md).
