# Witty Add-on und Raspi-Scripte: Änderungen von 1.5.0 bis 1.6 Build 3

Stand: 20. November 2026. Für Carsten und Papa.

Dieser Bericht trennt veröffentlichte Änderungen, zurückgezogene Versuche, neu nachgewiesene Fehler und Prüfgrenzen. Grundlage sind die tatsächlichen Pakete 1.5.1/1.5.2, der veröffentlichte Quellinhalt von 1.5.3, die GitHub-Historie, die Release Notes und der entschlüsselte aktuelle GitHub-Stand. Build 3 basiert auf GitHub-Commit `4532f7ae4356915237bf4e1c75506ecaa97d6e1a`.

## 1. Aktuelles Ergebnis und die vier Korrekturen in Build 3

Carsten meldet am 20.11.2026, dass der aktuelle Stromverbrauch dem Vergleich mit der manuellen Installation entspricht. Das ist eine Messrückmeldung aus seinem Aufbau; eine eigene Messung oder eine allgemeine Garantie für andere Geräte ist damit nicht verbunden. Build 3 ändert weder den WURB-GPS-Empfangszyklus noch die USB-/Waveshare-Dienststruktur.

| Befund | Ursache bzw. nachgewiesener Codefehler | Änderung in Build 3 |
|---|---|---|
| Website V-IN 1,196 V, Terminal `wp5` 13,071 V | Add-on las V-IN aus Register 3/4. Diese gehören laut Hersteller zu V-USB. V-IN liegt auf 5/6. | Register für V-IN und V-USB richtig zugeordnet. V-OUT und I-OUT separat belassen. |
| Build 2 installiert, Build 1 als Update angeboten | Nach gleichem numerischem Vergleich wurden `1.6` und `1.6.0` noch als Text verglichen. Damit wurde die Buildprüfung übergangen. | Numerisch gleiche Versionen gelten als gleich; anschließend entscheidet die Buildrevision. Derselbe numerische Vergleich wird für allgemeine Windows-Updates verwendet. |
| GPS rot trotz Zeit, Position und 6 verwendeten Satelliten | GPS-Lampe bekam eine getrennte Dienst-/Geräteprüfung; Uhrzeit und Position kamen bereits aus dem WURB-Status. Diese Quellen konnten widersprüchlich sein. | `GPS_ACTIVE` verwendet den vorhandenen WURB-GPS-Status. Alte USB-GPSD-/Bridge-Dienste werden im direkten USB-Betrieb nicht vorausgesetzt. |
| `wp5` verlangt erneut `sudo` | Der bisherige Berechtigungshelfer wurde nur bei `WITTY_MODEL=5` ausgeführt. Bei alter/fehlender Modellauswahl konnte die Reparatur beim Update entfallen. Geräte- und Dateizugriff brauchen weiterhin passende Gruppenrechte. | Reparatur bei vorhandenem `wp5` unabhängig von dieser Konfigurationsauswahl. SSH-/WURB-Benutzer zur Gruppe `i2c`; Geräte- und Sperrdateirechte dauerhaft setzen. |

**Nach dem Update für `wp5`:** Eine bereits offene SSH-Sitzung einmal schließen und neu verbinden. Linux übernimmt hinzugefügte Gruppen bei einer neuen Anmeldung. Danach `wp5` ohne vorangestelltes `sudo` aufrufen. Der Herstellerdaemon bleibt aktiv; seine Sperrdateien werden nicht gelöscht.

## 2. Version 1.5.0 / 1.5 – 10.11.2026

### Gefunden und korrigiert

- Das Updatefenster konnte einen veralteten Versionsstand weiterverwenden. Jeder erneute Aufruf liest das Online-Manifest erneut, mit Cachevermeidung. Ein Programmneustart ist dafür nicht erforderlich.
- Fehlgeschlagene Versionsabfragen sollen nicht als erfolgreich gelesene alte Version erscheinen.
- Die Windows-Zeitplananzeige konnte nach Verbinden/Neuverbinden leer bleiben, während die Homepage den Zeitplan korrekt zeigte. Sie übernimmt den Zeitplan aus der bereits vorhandenen Homepage-Statusantwort. Die zusätzliche SSH-Abfrage `schedule-status` entfiel.
- Die erste Uhr-/Zeitplanabfrage erzwingt keine separate Hardwareabfrage; weitere Homepage-Antworten aktualisieren die Anzeige.

### Betroffene Dateien/Funktionen

- Windows `MainWindow.xaml.cs`: Updatefenster, Versionsanzeige, Verbinden/Neuverbinden, Zeitplanübernahme.
- Windows `Services/GitHubUpdateService.cs`: Manifestabruf und Cachevermeidung.
- Windows Uhr-/Statusdienste und Parser: Auswertung derselben Homepage-Statusantwort.
- `Content/VERSION`, `Content/BUILD_REVISION`, Update-Manifeste und eingebettetes Add-on: aufeinander abgestimmte Pakete.

## 3. Version 1.5.1 – 14.11.2026: erster Stromsparversuch

Diese Variante wurde veröffentlicht, später aber zurückgezogen. Die folgenden Einzelmaßnahmen sind deshalb keine Behauptung über den heutigen Dienstaufbau.

### Gefundene Lastquellen und Änderungen

- Zusätzlicher `witty-gps-watch`-Dienst entfernt: keine fortlaufende geografische Zeitzonenabfrage durch diesen Wächter ohne Bedienzugriff.
- Webserver versuchsweise durch einen systemd-Socket erst bei Zugriff auf Port 8081 starten; Ende nach etwa 30 Sekunden Leerlauf. Laufende Anfragen, Downloads, Installationen und Terminalverbindungen verhinderten einen vorzeitigen Stopp.
- Automatische Witty-Hardwareabfrage von 2 auf frühestens 15 Sekunden begrenzt; parallele Anfragen gebündelt.
- GPS-Anzeige mit Fix von 2 auf 5 Sekunden, ohne Fix von 1 auf 3 Sekunden verlangsamt. Verdeckte/offline Seiten pausierten ihre Abfragen.
- Virtueller GPS-Rohdatenverteiler konnte bei geschlossenem virtuellem Anschluss eine CPU-Dauerschleife auslösen. Fehlerpfad auf Warten/Wiederverbinden umgestellt.
- GPSD-NMEA-Brücke datengetrieben statt mit ständigem 0,5-Sekunden-Aufwachen.
- Zeitzonendatei nicht mehr alle 0,5 Sekunden vollständig lesen/haschen; leichte Metadatenprüfung und Neuaufbau nur bei tatsächlicher Änderung bzw. Tages-/Offsetwechsel.

### Dateien im damaligen Paket

- `install.sh`: Sicherung und gezielte Installation; AllSky-Installationen wurden ausgeschlossen.
- `witty_addon/web/server.py`: Socketstart, Leerlauf, Arbeits-/Verbindungsschutz und Statuscache.
- `witty_addon/web/index.html`, `web/assets/shutdown-nav.js`: langsamere bzw. pausierte Browserabfragen.
- `witty_addon/backend/witty-gps-raw-fanout`: Schutz gegen CPU-Schleifen.
- `witty_addon/backend/witty-gps-nmea-bridge`: datengetriebene Verarbeitung.
- `witty_addon/installer/witty_live_time.py`, `setup_live_clock.sh`: Zeit-/Zeitzonencache und Einbindung in WURB/WIRC.

### Damalige Beobachtung

Die damaligen Notizen nennen 1,33 A gegenüber 0,75 A als Vergleich. Das war eine Nutzermessung; aus CPU-Tests ließen sich keine eingesparten Milliampere ableiten. Stromwerte sind nur an derselben Messstelle und bei gleichem Aufbau vergleichbar.

## 4. Version 1.5.2 – 14.11.2026: Nachbesserung des Stromsparversuchs

Auch diese Variante wurde später zurückgezogen.

### Gefunden und korrigiert / ergänzt

- Der alte Dienstname `wittypi5-webserver.service` musste für die Windows-Knöpfe Start/Stopp/Status erhalten bleiben. Er wurde als oneshot mit `RemainAfterExit` geführt; der Socket startete einen getrennten Worker.
- Entwickleranmeldung und fertige Terminalausgaben mussten einen Worker-Leerlaufstopp überleben. Private Zustandsdateien unter `/run` eingeführt; abgelaufene Anmeldungen wurden nicht wiederbelebt.
- Neue Vorprüfung lud den Webprozess gegen die vorhandenen Python-Abhängigkeiten, bevor Dateien und Dienste geändert wurden.
- Wiederholte Homepagezugriffe sollten dieselbe WURB-GPS-Aufgabe benutzen und keinen weiteren Leser starten oder Fixzähler zurücksetzen.
- Der zusätzliche 0,5-Sekunden-Kontrollloop wurde durch Verbindungsverlust-Callback und eine erneuerbare Drei-Sekunden-Datenfrist ersetzt.
- Ohne Empfänger: erneute Verbindungsversuche mit 1, 2, 4, 8, 16, höchstens 30 Sekunden Abstand. Deaktiviertes GPS sollte nicht weiter nach seriellen Geräten suchen.
- Nur eindeutig erkannte alte Add-on-RTC-Timer deaktiviert.
- Optionales Bluetooth-Abschalten mit `rfkill`, `bluetooth` und `hciuart`; vorherigen Zustand sichern, kein zusätzlicher Dauerprozess. Kein Abschalten von WLAN und keine Device-Tree-/UART-Umstellung.
- Socketumstellung erst nach den übrigen Updatearbeiten einplanen, damit der eigene Webprozess das Update nicht abbricht.

### Zusätzliche Dateien

- `installer/preflight_power_update.py`: Abhängigkeits-/Ladbarkeitsprüfung.
- `installer/witty_gps_power.py`: GPS-Kontrollloop und Datenfrist.
- `backend/witty-bluetooth-off`: Bluetoothzustand sichern/abschalten.
- Außerdem die unter 1.5.1 genannten Web-/GPS-/Zeitdateien und `install.sh`.

Die damaligen Notizen nennen eine Rückmeldung von etwa 1,33 A auf etwa 1,0 A, mit verbleibendem Abstand zur manuellen Installation. Das war keine bestätigte vollständige Behebung.

## 5. Version 1.5.3 – 18.11.2026: damaliger direkter GPS-Pfad

### Ergänzungen im damaligen Versuch

- Auf Pi 5 sollte WURB den seriellen Anschluss direkt besitzen; GPSD, NMEA-Übersetzer und virtuelle Anschlüsse entfielen in diesem Modus.
- Ein separater Ersatzleser sollte bei gestopptem/nicht installiertem WURB übernehmen. Sperren und geordneter Besitzerwechsel sollten zwei gleichzeitige Leser verhindern.
- Status aus dem Speicher des Lesers über lokalen Unix-Socket statt je Statusabfrage einen neuen Leser zu starten.
- Explizite Erkennung u-blox 6 `1546:01a6`, weiterer u-blox-Kennungen und BU-353 `067b:2303`; keine beliebige Auswahl bei mehreren uneindeutigen Geräten.
- Direkter Waveshare-UART-Versuch mit 4800/9600/38400/115200 Baud.
- NMEA-GGA/RMC/ZDA/GSV, Prüfsummen, Süd-/Westkoordinaten, Satellitenzahlen, Fixverlust, Abziehen und fortschreitende GPS-Zeit geprüft.
- Datenfrist zwölf Sekunden, um langsamere Empfänger zu berücksichtigen; Wiederholversuche ohne Gerät bis 30 Sekunden Abstand.

### Dateien des historischen 1.5.3-Pakets

- `installer/witty_direct_gps.py`: damalige direkte Verarbeitung.
- `installer/configure_direct_gps.py`: Umstellung und Besitzerwechsel.
- `backend/witty-direct-gps-client`: Statuszugriff.
- `backend/witty-gps-manager` und `witty-gps-manager-legacy`: neuer bzw. übernommener Pfad.
- `backend/witty-wurb-gps-api`, WURB-Dateien `wurb_api/record.py` und `wurb_core/record/gps_reader.py`: Integration in WURB.
- `backend/witty_backend.sh`, Web-/Installationsdateien: Anbindung.

### Was die Simulation wirklich aussagte

Der gesonderte Bericht vom 18.11. nennt 18 ergänzende Fälle mit Linux-PTYs, Datenverlust, Wiederverbinden, langsamen Daten und Besitzerwechsel. Das war ein Intel-Prüfhost, kein Raspberry. Die CPU-Zeiten und vorgegebenen Stromregisterwerte bewiesen keine elektrische Ersparnis.

## 6. Rücknahme der Versuche – 18.11.2026

GitHub-Commit `8c46ca8b932dfcbb730414f7285ca64f007729c7` zog die Änderungen 1.5.1 bis 1.5.3 zurück und stellte den 1.5.0-Baum wieder her. Deshalb dürfen der damalige Ersatzleser, Unix-Socket, Bluetoothhelfer und Socket-Webserver nicht als heute neu enthaltene Funktionen aufgelistet werden.

Für 1.5.4 bis 1.5.8 ist in der geprüften Versionsdatei-Historie kein eigener veröffentlichter Stand nachgewiesen. Ein separat erwähnter installierter 1.5.8-Quellstand liegt nicht vor; ihm werden hier keine erfundenen Änderungen zugeordnet.

## 7. Version 1.5.9 – 19.11.2026: Herstellerkompatibilität und Firmware-DST

### Neue Funktionen

- Vorgesehene Kombinationen: Herstellersoftware 5.3.1 mit Firmware 1.7 sowie Software 5.4.0 mit Firmware 1.8. Keine automatische Hersteller-/Firmwareaktualisierung.
- Button für Sommer-/Winterzeit der Witty-Firmware unter weiteren Einstellungen, nur bei Firmware 1.8. Einschalten bei festem UTC-Offset gesperrt; grüner Zustand nach Rückmeldung.
- Zeitregeln aus der tatsächlichen Linux-Zeitzone, unter anderem Sydney/Adelaide/Hobart/Melbourne und Lord Howe mit 30 Minuten Umstellung.
- Aktive Zeitpläne nach Regeländerung erneut aktivieren; bei unbekannter aktiver Zeitplanidentität Änderung vorab ablehnen.
- Bei aktiver Firmware-Automatik zusätzlichen Add-on-DST-Timer pausieren; bei Deaktivierung regionale Add-on-Regel wieder übernehmen. Fester Offset bleibt ohne Sommerzeit.

### Technische Dateien

- `backend/witty-wp5-compat`: Menüfolge für Software 5.4.0; `dst-enable`/`dst-disable`, Ermittlung wiederkehrender Regeln aus tzdata.
- `backend/witty-pi5-read-status`: direkte Statusregister, Firmwarefähigkeiten und Messwerte.
- `backend/witty_backend.sh` (installiert als `backend/witty5_backend.sh`): Parser, Status-JSON, Menüaktionen und Zeitplanbehandlung.
- `installer/sydney_time_rules.py`, `witty_live_time.py`, `setup_live_clock.sh` und bestehende Zeithelfer: regionale Zeitlogik und Einbindung.
- `web/index.html`: getrennte Messwertzeilen und Firmware-DST-Schalter.
- `tests/test_wp5_compatibility.py`, `.js`, `tests/fixtures/wp5/wp5dst.c/.h`: Regel- und Oberflächenprüfung mit Herstellerprüflogik.

### Wichtige Korrektur zur damaligen Beschreibung

Die Release Notes von 1.5.9 behaupteten bereits eine richtige V-IN/V-USB-Zuordnung. Im jetzt geprüften tatsächlichen Statusleser waren die Register dennoch vertauscht; auch der damalige Test hatte die falsche Zuordnung als Vorgabe. Diese Aussage war dadurch nicht ausreichend abgesichert. Build 3 korrigiert Code und Test anhand der Herstellerdefinition, ausdrücklich mit Carstens Beispiel 13,071 V gegen 1,196 V.

## 8. Version 1.5.9.1 – 20.11.2026: Update-Hotfix

- Updateabbruch bei Release Notes beseitigt: alte Listen und neue Sprachobjekte akzeptieren; eine defekte Änderungsübersicht soll den eigentlichen Updatevorgang nicht verhindern.
- Alte Socket-/Worker-Definitionen der zurückgezogenen Pakete vor Wiederherstellen des normalen Webdienstes entfernen, um Portkonflikte/Neustartschleifen zu verhindern. Nur erkannte Add-on-Dateien werden nach Sicherung entfernt; unbekannte Anpassungen führen zum Abbruch.
- Doppelten GPS-Zeitwächter entfernen; begrenzten Startabgleich und DST-Termin beibehalten.
- Windows-Inhalt und eingebettetes Add-on gemeinsam aktualisiert. Damals war die Stromdifferenz weiterhin offen.

Dateien: `update_addon.sh` (Release-Notes-/Updatefluss), `install.sh` und `installer/remove_legacy_socket.py` (Rückbau alter Webaktivierung), GPS-/Zeitdienst-Installationspfade sowie Paket-/Versionsdateien. Die tatsächlichen Helfernamen sind im Quellkorrekturpaket bzw. Add-on-Archiv nachlesbar.

## 9. Version 1.6 / 1.6.0 Build 1 – 20.11.2026

### Aktueller GPS-Grundaufbau

- Direkte USB-GPS-Maus auf Pi 4 und Pi 5: ausschließlich der vorhandene WURB-Leser. Keine zusätzliche USB-GPSD-/Socat-/PTY-Kette.
- Witty liest GPS-Zeit, Position und Satelliten über `http://127.0.0.1:8080/record/witty-gps-status/` aus WURB bei Bedienzugriff bzw. angefordertem Zeitabgleich.
- WURB benutzt wieder seinen normalen USB-Lesezyklus; zusätzliche Pi-5-Halbesekundenkontrolle entfernt.
- Alte USB-Hotplug-/Bridge-/GPSD-Aktivierung und virtuelle Ports bei Migration zurückbauen. GPSD-Socket gegen Wiederaktivierung im USB-/Kein-GPS-Modus sperren.
- Bei aktivierter Waveshare-Option bleibt die benötigte GPSD-/Bridge-Anbindung für WURB bestehen; beim Wechsel entsprechend sperren/entsperren.
- Fester UTC-Offset und regionale Zeitzone bleiben gespeichert. Begrenzter GPS-Startabgleich und DST-Termin bleiben vorhanden.

### Betroffene Dateien

- `backend/witty-gps-manager`: Moduswechsel und Altlasten-Migration.
- `backend/witty-wurb-gps-api`: Statusroute und beobachtende Ergänzungen am vorhandenen WURB-Leser.
- Auf dem Pi ergänzte WURB-Dateien `wurb_api/record.py`, `wurb_core/record/gps_reader.py`: Status, GPS-Zeit, Fixgültigkeit und Satelliten; kein zweiter serieller Leser.
- `backend/witty_backend.sh`, außerdem die 3-/4-/Kein-Witty-Backends: GPS aus WURB statt separater USB-Kette.
- `install.sh`, `installer_addon.sh`: Installation/Migration.
- `automation/windows_control.sh`: Build-1-Erkennung direkten USB-GPS-Betriebs auch auf Pi 5; damals noch über Dienst-/Geräteprüfung.
- `tests/test_gps_direct_v16.py`, `check_migration_v16.py`: Direktbetrieb und zwölf simulierte Pi-4-/Pi-5-Moduswechsel.

Build 2 ist auf Carstens Screenshot installiert. Ein eigenes veröffentlichtes Build-2-Paket ist in der geprüften GitHub-Historie nicht vorhanden. Deshalb wird dessen vollständiger Inhalt hier nicht aus der Bildschirmversion abgeleitet.

## 10. Build 3: genaue Dateiliste der jetzigen Korrektur

Alle Add-on-Pfade beziehen sich auf das oberste Archivverzeichnis `witty_addon/`. Installationsort ist üblicherweise `/home/wurb/wittypi5-webserver/`.

| Datei | Konkrete Änderung |
|---|---|
| `backend/witty-pi5-read-status` | V-IN aus 5/6; V-USB aus 3/4. Jeweils `(((MSB & 0x7f) << 8) OR LSB) / 1000`. V-OUT bleibt 7/8, I-OUT bleibt 9/10. |
| `web/index.html` | Fehlenden V-IN nicht durch allgemeines Feld `voltage` ersetzen: dieses bezeichnet den aktiven Eingang und kann USB sein. I-OUT als Ausgangsstrom auf der 5-V-Seite kennzeichnen. |
| `automation/windows_control.sh`, `show_status()` | WURB-GPS-Status einmal mit 1,5 s Timeout lesen. Aktiver Reader/empfangene Daten/gültiger Fix ergeben `GPS_ACTIVE=yes`; ausdrücklich inaktiver Status `no`; Ausfall/ungültige Antwort `unknown`. Fallback für ältere WURB-Versionen; keine GPS-Dienste starten. |
| `install.sh` | `setup_wp5_permissions.sh` bei gefundenem Herstellerkommando `wp5` auch bei fehlender/alter Modellauswahl ausführen. |
| `installer/setup_wp5_permissions.sh` | SSH-Benutzer und vorhandenen Benutzer `wurb` zu `i2c` hinzufügen; `/dev/i2c-1` und beide Herstellerlocks auf Gruppe `i2c`, Modus `0660`; udev-Regel für dauerhafte Geräterechtsetzung; vorhandene tmpfiles-Regel für Locks beibehalten. |
| `/etc/udev/rules.d/70-wittypi5-i2c.rules` | Vom Helfer erzeugt: I²C-Gerät 1 erhält Gruppe `i2c`, Modus `0660`. |
| `/etc/tmpfiles.d/wittypi5-app-lock.conf` | Locks `/run/lock/wittypi5_app.lock` und `/run/lock/wittypi5_i2c.lock` persistent anlegen/reparieren, ohne Sperrinode zu löschen. |
| Windows `Raspi-Scripte.dll` | `MainWindow.CompareAddonVersions` und `GitHubUpdateService.IsNewer` auf gemeinsamen numerischen Vergleich umgestellt; fehlende Endkomponenten gelten als 0. Versions-/Buildkonstanten und User-Agent auf neuen Stand. |
| `Build3-Windowskorrektur/Program.cs`, `patcher.csproj` im verschlüsselten Quellkorrekturpaket | Reproduzierbares Mono.Cecil-Werkzeug für die gezielte Änderung der bestehenden veröffentlichten Windows-DLL. Kein Neuaufbau des Gesamtprogramms aus dem älteren 1.3.8-Quellarchiv. Originale WPF-Ressourcen und übrige Funktionen werden übernommen. |
| `tests/test_wp5_compatibility.py` | Falsche Testregistervorgabe korrigiert; Beispiel V-IN 13,071 V/V-USB 1,196 V und separate Ausgangswerte, Firmware 1.7/1.8, beide Eingangsquellen. |
| `tests/test_build3_status.py` | GPS-Statusfälle einschließlich gültigem Fix, aktivem Reader, Daten ohne Fix, beendetem Reader und nicht erreichbarer API; kein V-IN-Ersatz durch aktive USB-Spannung. |
| `VERSION`, `BUILD_REVISION`, `PACKAGE_REVISION`, Windows-Content und alle Update-Manifeste | Einheitlich `1.6.0`, Buildrevision `20261120.1600.3`, sichtbare Bezeichnung 1.6 Build 3; Archive und SHA-256-Prüfsummen gemeinsam erneuert. |

### Richtige elektrische Zuordnung

| Messgröße | Bedeutung | Beispiel |
|---|---|---|
| V-IN | Eingang am Akku-/VIN-Anschluss | 13,071 V beim 12-V-Akku |
| V-USB | separater USB-C-Eingang | kein Ersatz für V-IN |
| V-OUT | Ausgang zum Raspberry | ungefähr 5 V |
| I-OUT | Strom auf dieser Ausgangsseite | mit V-OUT zu kombinieren |

Die Ausgangsleistung wäre `P_out = V-OUT × I-OUT`. Aus `V-IN × I-OUT` lässt sich die Akkueingangsleistung nicht korrekt berechnen. Für einen Akku-Eingangsstrom müssten unter anderem Reglerwirkungsgrad und Eigenverbrauch bekannt sein. Build 3 erfindet dafür keine Messwerte und fügt keine Leistungsrechnung hinzu.

## 11. Prüfung und Grenzen

Für Build 3 wurden 40 gezielte Python-Testmethoden bestanden, darunter Register-/Firmware-, GPS-, Update- und neue Statusprüfungen. Der tatsächliche in die Windows-DLL übernommene Vergleichscode bestand zwölf ausführbare Fälle, darunter `1.6 = 1.6.0`, ältere/neuere/gleiche Builds und alte Datumsversionen. Zusätzlich bestanden 16 DOM-Kombinationen und zwölf Modusmigrationen. Syntax, ZIP-Integrität, AES-GCM-Rückprüfung und Paketgleichheit wurden geprüft; das maschinenlesbare Ergebnis liegt der Veröffentlichung bei.

Es wurde kein physischer Pi-/Witty-/GPS-Test und kein nativer Windows-WPF-Oberflächentest durchgeführt. Der Test mit vorgegebenen Messregistern ist keine Strommessung. Die aktuelle Verbrauchsrückmeldung stammt von Carsten.

## 12. Update für Papa

1. Im Windowsprogramm zuerst das Programmupdate laden, damit auch der korrigierte Versionsvergleich ankommt.
2. Danach am verbundenen Raspberry „Witty Addon Software update“ ausführen. Das Standalone-Add-on und die im Windowspaket enthaltenen Kopien müssen denselben Build 3 enthalten.
3. Eine bereits offene Terminal-/SSH-Sitzung einmal neu verbinden; dann `wp5` ohne `sudo` öffnen.

Für eine alte Installation ist die vorhandene Migration im Update enthalten. Die Herstellerkombinationen bleiben 5.3.1/1.7 und 5.4.0/1.8. Es ist keine Neuinstallation der SD-Karte vorgesehen.

## 13. Nachprüfbare Grundlagen

- Repository: https://github.com/C4rstenSC/scripte
- 1.5: Commit `1ec60820be56e31a7f251d150533abf650070153`
- 1.5.1: `74d8a8799bcc134fbe9b42cd296df74ed37fbde0`
- 1.5.2: `56f304c8033ffb447baf511f5f325ad79a37312e`
- 1.5.3: `744b280ff31793afc18d0029f68fc6a3c41717de`
- Rücknahme: `8c46ca8b932dfcbb730414f7285ca64f007729c7`
- 1.5.9: `022b10615485f53680243d885408c3b6e9c88843`
- 1.5.9.1: `06fdee0ea6307ac20223ea6285932cef9bb24d28`
- 1.6: `bb1da8033ececa151a85550535cbbef18344e73c`
- 1.6.0 Build 1: `4532f7ae4356915237bf4e1c75506ecaa97d6e1a`
- Herstellerdefinition: https://github.com/uugear/Witty-Pi-5-Software/blob/main/wp5lib.h — `I2C_VUSB_MV_*`, `I2C_VIN_MV_*`, `I2C_VOUT_MV_*`, `I2C_IOUT_MA_*`.

Die Versionsgeschichte und zurückgezogenen Ansätze sind enthalten, damit nicht frühere Versuche versehentlich mit dem heute veröffentlichten Aufbau verwechselt werden.
