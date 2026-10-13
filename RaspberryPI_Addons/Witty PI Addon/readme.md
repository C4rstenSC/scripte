# Witty Add-on 0.8.4

Witty Add-on 0.8.4 – 13.10.2026

- Witty Pi 5 wird im Offline-Wartungsmodus vor dem Verkleinern direkt auf I2C-Erreichbarkeit geprüft.
- Eigener Abschalthelfer sendet die Hersteller-Abschaltmeldung und prüft die Rückmeldung. Der bisherige alleinige wp5d-Aufruf konnte einen fehlgeschlagenen I2C-Zugriff nicht zuverlässig melden.
- Wartungsimage enthält I2C-Werkzeuge, Controller-Module, Sperrverzeichnisse und den Abschalthelfer. Rechte und Aufruf des über Windows übertragenen Helfers werden ausdrücklich vorbereitet.
- Windows-Backup kann Schrumpfergebnis und Fehlerprotokoll von der Bootpartition auslesen und anzeigen.
- Bisherige GPS-, Installations-, Firmware- und Neustartkorrekturen unverändert enthalten.
- Bestätigte, abgewiesene und nicht bestätigte Abschaltmeldungen im Test geprüft; tatsächliche Abschaltung und Wartungsboot sind hardwareabhängig zu testen.
