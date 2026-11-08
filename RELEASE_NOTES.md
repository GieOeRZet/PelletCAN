# obraz kotła dobierany z panela
## Co nowego
- **Firmware 1.4.24:** odczyt rejestru `0x370A` („Boiler image selector”) w encji „Konfiguracja kotla”. Wymaga wgrania firmware do ESP.
- **Karta 1.43:** przy `grafiki: pelne` obraz kotła (11–13) wybierany automatycznie jak na panelu; `boiler_image` w YAML nadal ma pierwszeństwo.

Szczegóły: [CHANGELOG.md](CHANGELOG.md), [CHANGELOG-firmware.md](CHANGELOG-firmware.md).
