# Raspi-Scripte 1.0.9

Version 1.0.9 · Build 1

Allsky: Bilderordner und Witty-Zeitmodus
- Verständliche Ein-/Aus-Anzeigen mit Beispiel: 23.10., 17 Uhr bis 24.10., 8 Uhr → alle neuen Bilder im Ordner 20261023.
- Bei eingeschalteter Ordnerregel beginnt der Aufnahmetag um 12 Uhr mittags und endet vor 12 Uhr am Folgetag, auch an Tagen mit Zeitumstellung. Vorhandene Bilder werden nicht verschoben.
- Der zweite Schalter übernimmt den auf Witty gewählten Zeitmodus: feste UTC-Abweichung ohne Sommer-/Winterzeit oder die gewählte Zeitzone mit deren Sommer-/Winterzeitregeln. Die GPS-Position wählt keinen anderen Zeitmodus.
- Änderungen des Witty-Zeitmodus werden bei eingeschalteter Übernahme auch für Allsky angewendet. Nur laufende Allsky-Dienste werden dazu neu gestartet.

Windows: GPS-Anzeige
- Satellitenzahlen zusätzlich aus geprüften NMEA-GGA/GSV-Daten über gpsd lesen, wenn JSON-SKY-Daten fehlen. GPS-Zeit und Position bleiben unabhängig davon.
- Letzte noch aktuelle GPS-Werte bei kurzen Daten-/Verbindungslücken erhalten; ausdrücklich gemeldeter Fixverlust und veraltete Messwerte werden ausgeblendet.
- Position und Satellitenwerte getrennt aktualisieren; kürzere Statusabfrage verhindert unnötige Anzeigelücken.
- Feste Breite des Zeit-/GPS-Rahmens: Die Witty-Konfiguration springt bei fehlender GPS-Position nicht mehr seitlich.
- GitHub-Version und Buildnummer gemeinsam aus einer Versionsdatei lesen.

Prüfung
- Automatisierte Tests für Ordnerzuordnung, beide Zeitmodi, deutsche/englische Texte, verzögerte Satellitendaten und NMEA-Prüfsummen. Kein Test an physischer Raspberry-Pi-Hardware.
