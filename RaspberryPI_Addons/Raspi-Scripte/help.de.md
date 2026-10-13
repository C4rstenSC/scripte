# Raspi-Scripte 0.9.2.1 – Bedienungsanleitung

Stand: 13.10.2026

## Verbinden und lokale Raspberries suchen

Hostname oder IP-Adresse, Benutzer und SSH-Zugangsdaten eintragen und verbinden. „Suche lokale Raspberries“ prüft mögliche Adressen im lokalen IPv4-Netz. Die Anzeige läuft auch während noch offener Prüfungen weiter. Das Schließen des Suchfensters beendet die Suche.

Bei einem vom Programm ausgelösten Neustart – beispielsweise nach einer GPS-Änderung – wird die Verbindung automatisch erneut aufgebaut. Die Prüfung endet nach drei Minuten ohne Rückkehr. Manuelles Trennen beendet die Wiederverbindung.

## Windows-Programm aktualisieren

Den Update-Knopf im Programm verwenden. Der Updater prüft und entschlüsselt das Paket, aktualisiert die Dateien und startet das Programm erneut. Persönliche Verbindungsprofile und Aktivierung bleiben erhalten. Programmänderungen benötigen das Programmupdate; Texte und andere Inhalte können über das Inhaltspaket aktualisiert werden.

## Witty Add-on aktualisieren

„Witty Addon Software update“ lädt das aktuelle Paket und aktualisiert die vorhandene Installation. Das Terminal zeigt Version und Build sowie nur Änderungen seit dem installierten Stand. Beim Überspringen mehrerer Versionen werden deren Änderungen mit angezeigt. Hersteller-Software und Witty-Firmware sind eigene Komponenten; die Add-on-Version ist keine Firmware-Version.

## SD-Karte mit neuem Abbild beschreiben

1. Raspberry-Modell und Betriebssystem auswählen. Offline- und Online-Version stehen mit ihrem Veröffentlichungsdatum in der Versionsauswahl.
2. Offline verwendet ein vorhandenes geprüftes Image. Online lädt den ausgewählten offiziellen Stand. „Linux-Image einbinden“ erlaubt ein eigenes IMG beziehungsweise unterstütztes komprimiertes Image.
3. Die Ziel-SD-Karte auswählen. Bei Unklarheiten „Laufwerke aktualisieren“ und erneut auswählen.
4. „Ausgewählte Konfig installieren“ öffnen und Hostname, Benutzerkonto, WLAN, SSH und Region einstellen.
5. Das richtige Ziel prüfen und das Löschen bestätigen. Windows fordert erhöhte Rechte für den Kartenworker an. Ein Administrator-Benutzer allein ersetzt diese UAC-Freigabe nicht.

Alle Daten auf dem Zielmedium werden überschrieben. Systemlaufwerke werden nicht angeboten. Raspberry Pi Imager ist nicht erforderlich.

Der neue Schreibablauf schreibt zuerst die Image-Daten und gibt die Partitionstabellen erst am Ende frei. Anschließend wird das komplette Image von der Karte zurückgelesen und verglichen. Fortschritt, Geschwindigkeit und Restzeit beziehen sich auf die tatsächliche Übertragung; fertig ist der Vorgang erst nach erfolgreicher Prüfung.

„Abbrechen“ beendet den Auftrag. Eine unterbrochene Zielkarte muss vollständig neu geschrieben werden. Bei einer erneut auftretenden Windows-Zugriffsverweigerung die genaue Meldung mit Byteposition und Fehlercode festhalten; ein erfolgreicher Softwaretest beweist noch keine Schreibfähigkeit des konkreten Kartenlesers.

## SD-Karte Abbild erstellen

Die Karte auswählen, ein Zielverzeichnis auf einem anderen Laufwerk und einen neuen IMG-Dateinamen angeben. Das Programm liest die Karte und vergleicht das Image danach mit dem Original. Unvollständige Sicherungen werden bei Abbruch entfernt; Status und Fortschritt des abgebrochenen Auftrags werden zurückgesetzt.

Eine bereits verkleinerte unterstützte MBR-Karte wird bis zum Ende ihrer letzten Partition gesichert. Ist die Partition weiterhin nahezu kartengroß, fragt das Programm vor einer vollständigen Sicherung nach. Es liest vorhandene Wartungsergebnisse und Fehlerprotokolle von der Bootpartition. Ein kleineres Dateisystem allein genügt nicht, um eine kleinere IMG-Sicherung zu erzeugen. Andere Layouts werden vollständig gesichert.

Ausreichend Platz bereitstellen. FAT32 kann Dateien über 4 GiB nicht aufnehmen; hierfür NTFS, exFAT oder ein geeignetes Netzlaufwerk verwenden.

## SD-Karte am Raspberry verkleinern oder erweitern

„Micro SD Karten Optionen“ prüft Partition und ext4-Dateisystem getrennt. Beim Verkleinern startet der Raspberry in einen RAM-Wartungsmodus. Das Root-Dateisystem bleibt ausgehängt. Nach Prüfung, Verkleinerung und erneuter Prüfung bleibt eine Reserve von 512 MiB. Anschließend wird die normale Bootkonfiguration wiederhergestellt und die Bootpartition synchronisiert und ausgehängt.

Bei Witty Pi 5 hält ein Hersteller-Heartbeat den Witty während der Wartung im Betriebszustand. Nach verifizierter Verkleinerung startet ein eigener Abschlussmodus mit den installierten Herstellerdiensten. Dieser prüft erneut UUID und Partitionsgröße und fordert anschließend die Hersteller-Abschaltung an. Anwendungs- und bekannte Erweiterungsdienste bleiben bei diesem Abschlussstart gesperrt. Ein bloß zurückgelesener Befehlswert gilt nicht als Bestätigung für die aktivierte Stromabschaltung. Tatsächlicher Stromabschluss und Kartenverkleinerung müssen am Gerät bestätigt werden.

Bei einem Fehler wird das Wartungsprotokoll auf der Bootpartition gespeichert. Vor einem neuen Versuch das Ergebnis prüfen. Expandieren verwendet bei unterstützten Images einen einmaligen Bootauftrag; Benutzerkonto und Netzwerke werden dabei nicht neu eingerichtet.

## Witty, GPS und Uhren

Die Statusanzeige trennt Add-on, Hersteller-Software und tatsächliche Witty-Firmware. Die Firmware-Abfrage benötigt keinen GPS-Fix. Der aktive GPS-Empfänger wird unabhängig von der Auswahl für eine zukünftige Installation angezeigt.

„Kein GPS“, USB-GPS und Waveshare-L76X sind getrennte Konfigurationen. GPS-Koordinaten und Zeit werden nur bei gültigen Daten übernommen. WURB und Witty können dieselbe GPS-Quelle verwenden. Explizite RTC-Aktionen übertragen die Zeit in die jeweils angegebene Uhr.

„Herunterfahren“ verwendet bei eingerichteter Witty-Software den Hersteller-Abschaltdienst. Ein verschwundener SSH-Zugang bedeutet nur, dass der Pi nicht mehr erreichbar ist; er bestätigt keine getrennte Stromversorgung.

## WURB, WIRC und Allsky

Software über die Windows-Menüs installieren, aktualisieren oder deinstallieren. Die Basisinstallation richtet die gewählten Komponenten auf einem neuen Raspberry ein. Fortschritt und notwendige Rückfragen erscheinen im SSH-Terminal. Die Webseiten bieten die Bedienung vorhandener Dienste.

Allsky kann aus den angebotenen archivierten Ständen oder der offiziellen Online-Version installiert werden. Konfiguration vor Änderungen sichern. Wiederherstellung benötigt dieselbe Softwareversion und denselben Git-Stand wie die Sicherung.

Für die IMX296-GS-Kamera die entsprechende Option auswählen. Manuelle und automatische Tag-/Nacht-Belichtungen lassen sich getrennt einstellen; die Grenze liegt bei 15 Sekunden. „Allsky – Setup“ verwaltet auch Sicherungen und den Bildspeicherort.

## Hilfe und Release Notes

Die Hilfe zeigt die aktuelle Programmversion. Die aktuelle Änderungsübersicht ist nach Themen gegliedert; ältere Versionsstände stehen in der Versionshistorie. Die Witty-Webseite bietet eine eigene Bedienungsanleitung für Zeitpläne, Dienste und Aufnahmen.

## Änderungen am Ablauf in 0.8.6

Nach erfolgreichem Schreiben und Prüfen fordert das Programm Windows zum sicheren Auswerfen auf und setzt bei Erfolg die Anzeige zurück. Wird das Auswerfen verweigert, die Karte über Windows sicher entfernen. Beim IMG-Erstellen wird der tatsächliche Hostname von der Karte gelesen. Neue Konfigurationen schlagen wurbi-neu und wURbi vor; beide Vorgaben sind änderbar.

Nach einer bestätigten Verkleinerung übernimmt ein eigener Abschlussstart den installierten Witty-Herstellerdienst. WURB/WIRC/Allsky werden dabei nicht gestartet. Bekannte Erweiterungsdienste sind für diesen Start gesperrt; vorhandene spezielle Erststartaufträge verhindern schon die Vorbereitung. Vor der Abschaltung werden UUID und tatsächliche Partitionsgröße erneut geprüft. Das Ergebnisprotokoll unterscheidet verifiziertes Schrumpfen, angeforderte Abschaltung und Abschaltfehler. Ein ungültiger Witty-Wert 10 gilt weiterhin als Fehler und darf nicht als ON behandelt werden.

## Ablauf ab 0.8.8

IMG-Sicherungen lesen die Karte einmal und erfassen dabei SHA-256. Danach wird die gespeicherte Datei unabhängig zurückgelesen und mit dieser Prüfsumme verglichen. Die Prüfung schreibt nichts auf die Karte. Nach dem Auslesen des Hostnamens lautet der Vorschlag Datum-Hostname.img; eigene Dateinamen bleiben erhalten.

Die Basisinstallation verarbeitet nur die gewählten Module und ihre gemeinsamen Voraussetzungen. Ohne Witty und GPS werden nur Homepage-/Update-/Hotspot-Funktionen eingerichtet; Witty-Hardware- und Zeitänderungen entfallen. Für eine Stromabschaltung über Witty muss dessen Herstellerdienst installiert sein. Ein zusätzlicher Prüfhelfer kontrolliert nach dem Hersteller-Abschaltaufruf STOPPING und kann einen wirkungslosen Aufruf durch eine bestätigte I2C-Meldung ergänzen. Die tatsächliche Stromabschaltung ist am Gerät zu prüfen.

Partitionszustand und aktuelle Wartung werden getrennt angezeigt. Alte oder kopierte Wartungsberichte ohne passende Gerätekennung erscheinen nur als historische Information im Hinweis.

## Erweitern, Abbrechen und Deinstallieren

Erweitern verändert nur die letzte Partitionsgröße und vergrößert anschließend ext4. Kann der laufende Kernel die neue Grenze nicht übernehmen, erledigt ein einmaliger Dienst die Dateisystemarbeit nach dem Neustart. Der Witty-Neustarthook löst bei diesem Wartungsneustart keinen zusätzlichen Stromzyklus aus. Ein bereits fehlgeschlagener Boot benötigt eine Prüfung der Bootdateien und des Geräteprotokolls; die LED allein liefert keine Ursache.

„Abbrechen“ neben „Warte auf Raspberry“ beendet die Wiederverbindung und schließt die Verbindung. WURB/WIRC-Deinstallation läuft nach einer Backend-Aktualisierung sichtbar im Terminal und kann auch unvollständige Installationen entfernen. Projektordner werden gesichert; Einstellungen außerhalb dieser Ordner bleiben erhalten.

## Neu in 0.8.8: spätere Witty-Installation und SD-Abschluss

Wenn die Basisinstallation ohne Witty ausgeführt wurde, bleibt die Herstellerzeile sichtbar. Witty Pi 4/5 wählen und „Software installieren“ drücken. Der Manager aktiviert I2C, prüft die Hardware und installiert ausschließlich passende Herstellerkomponenten. Auf einem Pi 5 ist Witty Pi 4 nicht unterstützt; ein erkannter Witty Pi 5 korrigiert die Auswahl. Während eines anschließenden Neustarts wartet Windows bis zu drei Minuten und verbindet sich erneut. Ohne Witty erfolgt normales Linux-Herunterfahren.

Erfolgreiches Schreiben, IMG-Erstellen und Hostnamen-Vorbereiten schließen die Kartenhandles und werfen die Karte automatisch aus. Fortschritt und Laufwerksauswahl werden zurückgesetzt; Abschlussmeldungen stehen im Fenster ohne Popup. Lehnt Windows das Auswerfen weiterhin ab, wird das ausdrücklich angezeigt. Nicht allein anhand einer Erfolgsmeldung der Datenübertragung abziehen. Schreibdiagnosen liegen unter `%LOCALAPPDATA%/Raspi-Scripte/SdJobs/Logs`.

„Hostname setzen“ im Kartenbereich bereitet eine einmalige Änderung beim nächsten Pi-Start vor. Vorhandene WURB-, Allsky- und Basis-Hotspots erhalten den passenden Installer-Präfix vor dem neuen Hostnamen; Passwörter und übrige Verbindungsdaten bleiben bestehen. Ein Hostname darf zusammen mit dem Hotspot-Präfix höchstens 32 Zeichen lang sein.

Bei erneut auftretenden Abschaltproblemen kann vor weiterer Schrumpfung `sudo bash witty-shutdown-diagnose.sh` ausführen und die erzeugte `.tar.gz` sichern. Nach der Wartung `witty-sd-result.json`, `witty-sd-result.txt` und – falls vorhanden – `witty-sd-poweroff.log` von der Bootpartition sichern. Das Abschaltprotokoll bestätigt nur die beobachtete Hersteller/I2C-Rückmeldung; LEDs oder 5V-Versorgung müssen am Gerät geprüft werden.

## Start nach Schrumpfung (Korrektur 0.8.9)

Nach erfolgreicher Dateisystemprüfung beendet der RAM-Wartungsmodus den Witty-Heartbeat vor dem Aushängen der Bootpartition. Ein später Abschalt- oder Aushängefehler wird getrennt vom bereits geprüften Dateisystem protokolliert. Bei bestätigter Geometrie stellt der Hersteller-Abschlussmodus die normale Bootzeile vor den Herstellerprüfungen wieder her. Die Karte kann danach normal starten, ohne Wartungsparameter manuell zu entfernen.

Für eine bereits betroffene ältere Karte zeigt `systemd.unit=witty-sd-finalise.target` in `cmdline.txt` zusammen mit dem Fehler an `umount /run/witty-boot` den vorliegenden Abschlussfehler. Nur nach Prüfung der zugehörigen Protokolle und Partitionskennung die eigene Wartungs-Bootoption und deren Masken entfernen. Die erzeugte Reparaturdatei für wurbi-n94 erhält PARTUUID und alle übrigen Bootparameter. Die ursprüngliche `config.txt` war bereits korrekt wiederhergestellt.

## Bedienung ab 0.9.0

**Abbild wiederherstellen:** IMG auswählen. Der angezeigte Hostname stammt aus dem Dateisystem im Abbild. „Hostname setzen“ merkt einen anderen Namen vor; die Karte bleibt dabei unverändert. Erst „Image schreiben und prüfen“ schreibt und prüft die vorbereitete Kopie. Der Pi setzt beim ersten Start den neuen Hostnamen samt den vorhandenen Installer-Hotspotnamen (wifi4bats-, allskywifi- oder wifi-). Das Original-IMG und WLAN-Passwörter bleiben erhalten.

**Karten auswählen:** „Laufwerke aktualisieren“ gibt es in jedem der drei SD-Bereiche. Eine vorhandene Auswahl bleibt erhalten; andernfalls wird die erste gefundene Karte angezeigt. Vor einem Schreibauftrag die angezeigte Karte genau prüfen. Bei mehreren Windows-Partitionen werden deren Laufwerksbuchstaben gemeinsam angezeigt.

**Schrumpfen und Sichern:** Den Schrumpfauftrag starten und den Hinweis abwarten. Stromversorgung und Karte bis zum vollständigen Ausschalten angeschlossen lassen. Danach die Karte für „SD-Karte Abbild erstellen“ am PC anschließen. Beim nächsten normalen Pi-Start expandiert ein ab 0.9.0 vorbereiteter und erfolgreich geprüfter Auftrag automatisch wieder. Vor der Sicherung deshalb nicht erneut im Pi starten. Ältere Schrumpfaufträge erhalten diese neue Vormerkung nicht rückwirkend.

**Expandieren:** Der manuelle Vorgang verbindet nach dem Neustart höchstens 50 Sekunden lang automatisch neu. Bei längerer Bootdauer danach manuell verbinden. Installationen und andere geplante Neustarts verwenden weiterhin drei Minuten.

**Programmupdate:** Eigene SD-Aufträge werden abgebrochen; das Update wartet auf das Ende aller Kartenzugriffe. Ein teilweise geschriebenes Abbild muss neu geschrieben werden. Weitere Programminstanzen aus demselben Ordner müssen ihre Vorgänge ebenfalls beenden und geschlossen werden. Wenn das sichere Beenden nicht gelingt, wird das Update nicht installiert.

**Pakete:** Nur die ausgewählten Komponenten erhalten ihre Paketliste. APT und pip prüfen vorhandene Pakete und verwenden passende Downloads erneut. WURB und WIRC besitzen getrennte Laufzeitumgebungen mit gemeinsamem Benutzer-Cache. Entwicklerwerkzeuge black und pylint gehören nicht zur normalen Installation. Grafikfreie GPS-Abfragen benötigen keine grafischen Diagnoseprogramme; die WIRC-Kamera benötigt weiterhin Bild-/Videobibliotheken.

## Kartenabfrage ab 0.9.1

Beim Öffnen des SD-Tabs findet keine automatische Kartenabfrage statt. Den passenden Button „Laufwerke aktualisieren“ im gewünschten Bereich drücken. Nur dieser Bereich wird aktualisiert. Bei „SD-Karte Abbild erstellen“ wird dabei auch der Hostname der ausgewählten Karte gelesen. Nach einem manuellen Auswahlwechsel erneut aktualisieren, um den Hostnamen einzulesen.

Die Laufwerksbuchstaben stehen am Anfang der Anzeige. „Ohne Laufwerksbuchstaben“ bedeutet, dass Windows keine Partition mit einem Buchstaben eingebunden hat. „USB-Datenträger“ wird verwendet, wenn der Kartenleser oder das USB-Gerät keinen eindeutigen Typ meldet. Geräteart und Größe vor dem Schreiben prüfen.

Ein kurzzeitig verweigerter Schreibzugriff wird begrenzt wiederholt. Erst das vollständige Zurücklesen und der Vergleich erlauben eine Erfolgsmeldung. Bei einem endgültigen Fehler die Karte erneut vollständig beschreiben; eine unvollständige Karte ist nicht startfähig.

Die Fortschrittszeile mit Phase, Prozent, Geschwindigkeit und Restzeit steht innerhalb jedes SD-Bereichs unmittelbar über seinem Fortschrittsbalken.

## Fortschritt und Vorbereitung ab 0.9.2

Vor dem Schreiben wird die ausgewählte Karte mit einem kurzen Lesetest gemessen. Der Test liest bis zu 32 MiB an mehreren Stellen der Karte und verändert keine Kartendaten. Erst danach beginnt der freigegebene Schreibauftrag. Die Anzeige verwendet IMG-Größe und gemessene Leserate; die aktuelle Schreibrate wird beim Schreiben ergänzt. Fortschritt und Restzeit werden anhand des verbleibenden geschätzten Zeitaufwands berechnet. Es gibt keine feste 50/50- oder 80/20-Aufteilung.

Die Vorbereitung zeigt ihren konkreten Schritt. Große Dateiprüfungen laufen im Hintergrund. Schreiben und vollständige Rückleseprüfung arbeiten direkt mit sektorausgerichteten Puffern. Eine Erfolgsmeldung erfordert die vollständig bestandene Prüfung.

Kurzzeitige Zugriffssperren werden begrenzt wiederholt. Dauerhafte Windows-Sperren bleiben ein Fehler. Der neue native Schreibweg und detailliertere Protokolle müssen auf dem betroffenen PC bestätigt werden; aus früheren Fehlerprotokollen lässt sich der konkret blockierende Treiber nicht sicher bestimmen.

## Status und Vorbereitung ab 0.9.2.1

Die voreingestellten OS-Versionen werden beim Start geladen. „Laufwerke aktualisieren“ bleibt für die Kartenabfrage erforderlich. Bei einem vorhandenen offiziellen IMG wird die vollständige Quellprüfung mit dem Kopieren für die gewählten Einstellungen verbunden. Beschädigte Daten werden vor dem Kartenschreiben zurückgewiesen.

Die Fortschrittsanzeige ist vom Ergebnis des Kartenzugriffs getrennt. Eine kurzzeitig blockierte Statusdatei beendet den Datentransfer nicht; die separate Ergebnisdatei bestätigt den abgeschlossenen Vorgang. Erfolg setzt weiterhin die vollständige Rückleseprüfung voraus.
