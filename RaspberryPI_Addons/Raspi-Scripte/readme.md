# Raspi-Scripte 1.0.1

Version 1.0.1 · Build 4

- Nach Neuinstallation die aktive interne schedule.wpi mit den benannten WPI-Skripten vergleichen, auch wenn die Quelldateien nur auf dem Witty gespeichert sind.
- Bei genau einem inhaltsgleichen Treffer den ursprünglichen Skriptnamen speichern und auf Homepage sowie im Windows-Programm anzeigen. Unterschiedliche Zeilenenden werden beim Vergleich berücksichtigt; bei mehreren identischen Skripten wird kein Name geraten.
- Die Skriptliste, das Lesen des aktiven Skripts und die einmalige Windows-Verbindungsabfrage können eine fehlende Zuordnung wiederherstellen. Fehlgeschlagene Downloads sperren weitere Versuche nicht mehr bis zum nächsten Boot.
- Unvollständige Downloads führen zu keiner Zuordnung. Die Wiederherstellung aktiviert keinen Zeitplan und ändert dessen Schaltzeiten nicht.
- Homepage: erkanntes aktives Skript grün markieren; nur sein Aktivieren-Button zeigt Aktiv. Die übrigen Skripte bleiben aktivierbar.
- Ein wiederhergestellter Name wird mit den bereits gelesenen, noch aktuellen Zeitplandaten an verbundene Windows-Sitzungen weitergegeben; dafür ist keine zusätzliche Zeitabfrage erforderlich.
