# Raspi-Scripte 0.8.6 – Bedienungsanleitung

Stand: 13.10.2026

## Verbinden und lokale Raspberries suchen

Hostname oder IP-Adresse, Benutzer und SSH-Zugangsdaten eintragen und verbinden. „Suche lokale Raspberries“ prüft mögliche Adressen im lokalen IPv4-Netz. Die Anzeige läuft auch während noch offener Prüfungen weiter. Das Schließen des Suchfensters beendet die Suche.

Bei einem vom Programm ausgelösten Neustart – beispielsweise nach einer GPS-Änderung – wird die Verbindung automatisch erneut aufgebaut. Die Prüfung endet nach drei Minuten ohne Rückkehr. Manuelles Trennen beendet die Wiederverbindung.

## Windows-Programm aktualisieren

Den Update-Knopf im Programm verwenden. Der Updater prüft und entschlüsselt das Paket, aktualisiert die Dateien und startet das Programm erneut. Persönliche Verbindungsprofile und Aktivierung bleiben erhalten. Programmänderungen benötigen das Programmupdate; Texte und andere Inhalte können über das Inhaltspaket aktualisiert werden.

## Witty Add-on aktualisieren

„Witty Addon Software update“ lädt das aktuelle Paket und aktualisiert die vorhandene Installation. Das Terminal zeigt Version und Build sowie nur Änderungen seit dem installierten Stand. Beim Überspringen mehrerer Versionen werden deren Änderungen mit angezeigt. Hersteller-Software und Witty-Firmware sind eigene Komponenten; die Add-on-Version ist keine Firmware-Version.

## SD-Karte beschreiben

1. Raspberry-Modell und Betriebssystem auswählen. Offline- und Online-Version stehen mit ihrem Veröffentlichungsdatum in der Versionsauswahl.
2. Offline verwendet ein vorhandenes geprüftes Image. Online lädt den ausgewählten offiziellen Stand. „Linux-Image einbinden“ erlaubt ein eigenes IMG beziehungsweise unterstütztes komprimiertes Image.
3. Die Ziel-SD-Karte auswählen. Bei Unklarheiten „Laufwerke aktualisieren“ und erneut auswählen.
4. „Ausgewählte Konfig installieren“ öffnen und Hostname, Benutzerkonto, WLAN, SSH und Region einstellen.
5. Das richtige Ziel prüfen und das Löschen bestätigen. Windows fordert erhöhte Rechte für den Kartenworker an. Ein Administrator-Benutzer allein ersetzt diese UAC-Freigabe nicht.

Alle Daten auf dem Zielmedium werden überschrieben. Systemlaufwerke werden nicht angeboten. Raspberry Pi Imager ist nicht erforderlich.

Der neue Schreibablauf schreibt zuerst die Image-Daten und gibt die Partitionstabellen erst am Ende frei. Anschließend wird das komplette Image von der Karte zurückgelesen und verglichen. Fortschritt, Geschwindigkeit und Restzeit beziehen sich auf die tatsächliche Übertragung; fertig ist der Vorgang erst nach erfolgreicher Prüfung.

„Abbrechen“ beendet den Auftrag. Eine unterbrochene Zielkarte muss vollständig neu geschrieben werden. Bei einer erneut auftretenden Windows-Zugriffsverweigerung die genaue Meldung mit Byteposition und Fehlercode festhalten; ein erfolgreicher Softwaretest beweist noch keine Schreibfähigkeit des konkreten Kartenlesers.

## mSD-Karten IMG erstellen

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
