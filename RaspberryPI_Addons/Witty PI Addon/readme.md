# Witty Add-on 0.6.36

Release: 23.09.2026

- Der überflüssige zusätzliche Download-Button unterhalb der Datensicherung
  auf ALLSKY-SETUP wurde vollständig entfernt. Sein Platzhalterziel führte nur
  auf `allsky-setup#`.
- Neu erstellte TAR.GZ-Sicherungen werden weiterhin automatisch
  heruntergeladen. Gespeicherte Sicherungen bleiben in der separaten Liste
  verfügbar.

- ALLSKY-SETUP zeigt Standort, GPS-Position und Sonnenberechnung in einem
  eigenen gerahmten Bereich.
- Datensicherung und Wiederherstellung stehen davon getrennt in einem eigenen
  Kasten; Status- und Fehlermeldungen erscheinen oben auf der Seite.
- Lange Bildübertragungen laufen bei aktivem ALLSKY. Nur Abschlussabgleich und
  Pfadwechsel halten den Dienst kurz an; danach wird sein vorheriger Zustand
  verbindlich wiederhergestellt und geprüft.
- Eine laufende Übertragung bleibt nach einem Neuladen sichtbar und verhindert
  widersprüchliche Parallelvorgänge.
- Die normale Updateausgabe zeigt nur Änderungen seit der installierten
  Version, Warnungen, Fehler und das Endergebnis. Vollständige technische
  Diagnosen sind mit `WITTY_UPDATE_VERBOSE=1` verfügbar.

Auf GitHub liegt ausschließlich das verschlüsselte Paket
`witty_addon.zip.enc`; eine unverschlüsselte `witty_addon.zip` wird nicht
veröffentlicht.
