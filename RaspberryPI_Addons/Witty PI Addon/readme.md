# Witty Add-on 0.6.39

Release: 26.09.2026

**Update-Reihenfolge:** Zuerst Raspi-Scripte für Windows 0.6.29 aus dem Entwicklerpaket kompilieren und installieren. Windows 0.6.28 sendet die für `update.sh` benötigte einmalige Startfreigabe nicht und kann dieses Add-on daher nicht installieren.

- Auf Raspberry Pi 4 wird Witty Pi 5 vor einer Witty-Pi-4-Herstellerinstallation anhand der I2C-Hardware erkannt.
- ALLSKY-Sicherungen führen Overlay-Layouts im Manifest; nach dem Einspielen werden die aktiven JSON-Layouts geprüft.
- Zweisprachige Add-on-Release-Notes werden beim Update nur auf Deutsch ausgegeben.

## Bisherige Änderungen (0.6.38)

- `installer.sh` akzeptiert Basisinstallationen ausschließlich mit der
  einmaligen Startfreigabe aus Raspi-Scripte für Windows. Manuelle Aufrufe über
  PuTTY, SSH oder andere Konsolen werden vor jeder Systemänderung beendet.
- Raspberry Pi 4/4B/4B+ und Raspberry Pi 5 werden im Windows-Programm direkt
  vor dem Start erneut ausgelesen und verbindlich mit der Auswahl verglichen.
- Hotspot-Name und SSID werden erst nach der WURB-/WIRC-/ALLSKY-Auswahl
  festgelegt. Ein Hostname wie `wurbi-n8` wird nicht mehr vorzeitig als
  `allskywifi-wurbi-n8` angezeigt.
- Abschlussmeldungen behandeln WURB und WIRC nur noch dann als Prüfpunkt, wenn
  diese Komponenten tatsächlich ausgewählt wurden.
- Ein Add-on-Update ersetzt auch den vorhandenen Starter `~/installer.sh`,
  damit bestehende Installationen die Konsolensperre erhalten.
- „USB GPS“ lässt sich auch ohne angeschlossene GPS-Maus vollständig
  installieren. Pi 4 bereitet WURBs direkten Gerätezugriff, Pi 5 gpsd/udev
  für späteres Hot-Plug vor; fehlende Hardware ist kein Installationsfehler.
- Auf Pi 4 verlangt die Add-on-Prüfung keine absichtlich deaktivierte
  ttyUSB9-Bridge und überschreibt WURBs direkte USB-Geräteliste nicht.

- ALLSKY-Speichertransfers zeigen verarbeitete Dateien, Gesamtzahl und
  Prozentwert in einem Fortschrittsbalken.
- Der Fortschritt wird serverseitig geführt und läuft nach dem Neuladen der
  Homepage am aktuellen Stand weiter.
- Alle Aktionsknöpfe bleiben sichtbar, werden während des Vorgangs gemeinsam
  ausgegraut und nach Abschluss automatisch wieder freigegeben.
- Der Abschlussabgleich kopiert nur neue oder zwischenzeitlich geänderte
  Dateien.

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
