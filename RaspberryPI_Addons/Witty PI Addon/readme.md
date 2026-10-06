# Witty Add-on 0.6.54

Release: 06.10.2026

- GPS-Daten werden bei USB GPS und Waveshare wiederholt abgefragt, auch auf Raspberry Pi 4 und ohne Witty. Ein ausbleibender Fix oder eine fehlgeschlagene Abfrage verhindert spätere Aktualisierungen nicht.
- GPS-Statusleuchten folgen jeder Abfrage; ungültige Positionen werden ausgeblendet. Windows zeigt GPS-Variante und Aktivzustand.
- Allsky v2026.10.01: Witty-Navigation wird nach Updates erneut in die Hersteller-Homepage eingefügt. Die vorherige Installation bleibt für die Herstellermigration erhalten.
- Konfigurationssicherungen enthalten neue Module, Zustandsdateien und Datenbanken. SQLite wird konsistent einschließlich bestätigter WAL-Daten gesichert.
- Wiederherstellung berücksichtigt allskyserver und erhält neue Optionsdefinitionen sowie neue Einstellungsfelder. Eine durch Neustart unterbrochene Update-Wiederherstellung wird beim Start fortgesetzt.

Detaillierte deutsche Änderungen stehen in RELEASE_NOTES_0.6.54.txt und release-notes.json sowie im Windows-Programm. Hardware-Laufzeittests bleiben ausstehend.

## Frühere Änderungen

Release: 06.10.2026

Die Homepage-Anleitung zeigt die Änderungen der Versionen 0.6.43, 0.6.42, 0.6.41 und 0.6.40.

**Update-Reihenfolge:** Zuerst Raspi-Scripte für Windows 0.6.29 oder neuer installieren. Windows 0.6.28 sendet die für `update.sh` benötigte einmalige Startfreigabe nicht.

- Raspberry Pi 5: GPS-Maus wird nach jedem USB-Portwechsel am aktuellen seriellen Anschluss an gpsd angebunden. WURB erhält einen gültigen Positionsfix auch vor der ersten SKY-Meldung.
- Raspberry Pi 4: Der direkte GPS-Datenweg bleibt unverändert.

## Bisherige Änderungen (0.6.42)

- Die Anleitung zeigt den aktuellen und drei vorangegangene Stände.

## Bisherige Änderungen (0.6.41)

- „Weitere Einstellungen“ steht vor der Eingangsspannung und ist standardmäßig eingeklappt; Neustart und sicheres Herunterfahren bleiben sichtbar. Die hibernationMode-Zeile entfällt.

## Bisherige Änderungen (0.6.40)

- ALLSKY-Sicherungen enthalten Benutzervariablen und Modulkonfiguration, wenn die ALLSKY-Version dafür eigene Pfade vorgibt; die Wiederherstellung spielt sie wieder ein.
- Ein erkannter Witty Pi 5 verhindert die versehentliche Witty-Pi-4-Herstellerinstallation auch auf Raspberry Pi 5.

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
