# Raspi-Scripte 1.5 – Bedienungsanleitung

Stand: 10.11.2026 · Windows-Programm und Witty-Homepage

## Verbinden und Gerät auswählen

Hostname oder IP-Adresse, Benutzer und SSH-Zugangsdaten eingeben. Die lokale Suche bietet erreichbare Raspberry-Geräte an. Bei Auswahl einer IP verwendet die Verbindung diese IP; nach erfolgreicher Anmeldung wird der tatsächliche Hostname aktualisiert. Das ist insbesondere nach einem SD-Kartenwechsel wichtig. Gespeicherte Zugänge für unterschiedliche Benutzer bleiben getrennt.

Nach einem vom Programm angeforderten Neustart wird automatisch erneut verbunden. Manuelles Trennen beendet die Wiederverbindung. Ein laufender Auftrag, Fortschritt und Fehler bleiben im Terminal nachvollziehbar.

## Windows und Witty Add-on aktualisieren

Zuerst das Windows-Programm auf 1.5 aktualisieren, danach das Witty Add-on. Das vollständige Programmupdate enthält Programm, Updater, Inhalte und passendes eingebettetes Add-on. Hersteller-Software und Witty-Firmware besitzen eigene Versionsnummern und sind getrennte Aktualisierungen.

Die Updateanzeige berücksichtigt installierte Version und Build und zeigt die seitdem hinzugekommenen Änderungen. Ein unbekannter oder fehlgeschlagener Gerätestatus ist kein Nachweis einer erfolgreichen Aktualisierung. Nach dem Update neu verbinden und die gemeldeten Versionsstände prüfen.

Vor Basisinstallation und Witty-Update wird die PC-Systemzeit nur bei mehr als 48 Stunden Abweichung automatisch auf die Raspberry-Systemuhr übertragen. Diese Vorprüfung ändert weder Zeitzone noch RTCs. Der ausdrücklich betätigte PC-Zeitbutton ist eine eigene Aktion.

## Zeiteinstellungen im Windows-Programm

Das UTC-Feld links neben „Fester UTC-Offset“ passt sich seinem Inhalt an. Es enthält ausschließlich:

UTC 00:00, UTC +01:00, UTC +02:00, UTC +06:30, UTC +07:00, UTC +08:00, UTC +08:45, UTC +09:30, UTC +10:00, UTC +10:30, UTC +11:00, UTC +12:00

+06:30 gilt für die Kokosinseln, +07:00 für die Weihnachtsinsel, +08:00 für Westaustralien, +08:45 für Eucla, +09:30 für Northern Territory/South Australia, +10:00 für die östlichen Bundesstaaten, +10:30 für South Australia im Sommer beziehungsweise Lord Howe im Winter, +11:00 für die östliche Sommerzeit/Lord Howe im Sommer und Norfolk im Winter, +12:00 für Norfolk im Sommer. Mehrfach verwendete Offsets erscheinen nur einmal.

Die Pfeile markieren +01:00, +02:00, +10:00 und +11:00 als Orientierung. Sie zeigen nicht den aktiven Zeitmodus an. Einen Offset auswählen und mit „Fester UTC-Offset“ übernehmen. Feste Offsets gelten ganzjährig ohne automatische Umstellung.

„Sommer-/Winterzeit automatisch“ öffnet die Regionsauswahl. Zum Beispiel Australia/Sydney für NSW oder Australia/Adelaide für South Australia wählen. Die Region bestimmt die Umstellung; im festen Modus bleibt der ausdrücklich gewählte Offset maßgeblich. Ein GPS-Vorschlag ersetzt keinen aktiven festen Offset.

Der bestätigte aktive Modus wird grün angezeigt. Bei unbekanntem oder veraltetem Status bleiben die Buttons neutral. Bei Verbindung wird ein unterstützter gemeldeter Offset vorausgewählt. Wiederholte unveränderte Statusabfragen überschreiben eine noch nicht übernommene Auswahl nicht. Meldet ein älterer Raspberry einen ausgeschlossenen Offset, bleibt die Auswahl leer, bis ausdrücklich ein Eintrag gewählt wird; die laufende Zeitzone wird dabei nicht geändert.

„Systemzeit => RPI und Witty RTC“ überträgt den aktuellen UTC-Zeitpunkt des PCs mit Prüfung auf Raspberry und Witty. Die eingestellten Zeitzonenregeln bleiben bestehen. Eine korrekt eingestellte PC-Uhr ist Voraussetzung.

## Homepage: Status, Uhren und GPS

Die Homepage zeigt Linux-Systemzeit, Witty-RTC und bei Verfügbarkeit interne Pi-RTC, GPS-Zeit, Position und Satelliten. Empfängeraktivität ohne Positionsfix ist von einem gültigen Fix zu unterscheiden. Ein sichtbarer GPS-Zeitwert garantiert keine gültige Position für Sonnenberechnung.

„GPS => Systemzeit + Witty-PI RTC“ und „GPS => Witty-PI RTC“ benötigen gültige aktuelle GPS-Zeit. Beim Witty Pi 5 führt das aktuelle Backend beide Aktionen als geprüften gemeinsamen Abgleich von Linux und Witty aus; eine aktive interne Pi-RTC wird mit abgeglichen. Die zweite Beschriftung bedeutet dort daher keine ausschließlich isolierte RTC-Korrektur. Die Rückmeldung nennt die tatsächlich abgeglichenen Uhren. Im Allsky-Betrieb bleibt Witty beim automatischen Start die Zeitquelle; eine manuelle GPS-Aktion ist davon getrennt.

Kein GPS, USB-GPS und Waveshare L76X werden getrennt eingerichtet. Die Auswahl für die nächste Installation und der aktuell aktive Empfänger sind unterschiedliche Angaben. Bei fehlendem Fix zuerst Empfang und Quelle prüfen. Ein fester UTC-Offset wird nicht automatisch durch GPS auf Sommerzeit umgestellt.

Die zusätzlichen Witty-Einstellungen enthalten Start bei Stromzufuhr, bevorzugten Stromanschluss, elektrische Statuswerte und die interne Raspberry-RTC. „RPI - reboot“ und „RPI - herunterfahren“ stehen am Ende. Ein verlorener SSH-Zugang bestätigt allein keine abgeschaltete Stromversorgung.

## Zeitpläne und Skripteditor

Aktives oder gespeichertes WPI-Skript direkt in den Editor laden. Laden und Bearbeiten ändern den laufenden Zeitplan nicht. BEGIN, END, Dateiname, Vorschau und Größenprüfung kontrollieren. Ein Upload ist eine eigene Aktion und aktiviert das Skript nicht automatisch. Vor dem Ersetzen einer aktiven gleichnamigen Datei wird diese deaktiviert.

Nach einem abgelaufenen END-Datum wird „Aktivieren“ ausgeblendet; hierfür ist die Witty-RTC maßgeblich. Die Datei kann weiterhin geladen oder gelöscht werden. Nach Aktivierung oder Deaktivierung die bestätigte Rückmeldung und nächste Start-/Abschaltzeit prüfen. Fehlertexte nicht als Erfolg behandeln.

## WURB, WIRC und Aufnahmen

Installations-, Update-, Deinstallations- und Homepagebuttons beziehen sich auf die jeweilige Anwendung. Witty-Navigation ergänzt deren Originalseiten. WURB verwendet Port 8080, Witty 8081, WIRC 8082. Bei manuellen Koordinaten werden Dezimalkomma sowie N/S/E/W unterstützt. Speichern abwarten und zurückgelesene Position prüfen; Positionsquelle und Startprofil können getrennte Einstellungen sein.

In Recordings öffnen und schließen Ordnersymbol und Name den Ordner. Die Dateiauswahl und der ZIP-Download bleiben getrennte Aktionen. Vor dem Löschen die ausgewählten Dateien und Ordner prüfen.

## Allsky: Installation und Livebild

Die Basisinstallation bietet die archivierten Quellen und die aktuelle Herstellerversion. Quelle vor dem Start wählen. Ein abgebrochener Installer ist keine fertige Installation; die konkrete Fehlermeldung im Terminal prüfen. Bestehende Einstellungen vor Softwarewechsel sichern.

„Live Video Bild“ im Allsky-Setup öffnet das Kamerabild zum manuellen Fokussieren. Der Ablauf koordiniert den Kamerazugriff mit Allsky. Popup nach dem Fokussieren schließen und kontrollieren, ob der zuvor laufende Allsky-Dienst wieder gestartet ist. Ein zuvor gestoppter Dienst soll gestoppt bleiben. Keine zweite Kameraanwendung gleichzeitig starten.

Auf Allsky-Installationen ist Englisch die Vorgabe für die mobile Seite. Eine ausdrücklich gewählte deutsche Sprache wird gespeichert. Bei festem UTC-Offset bleibt dieser maßgeblich; die automatische Sommerzeit gilt erst nach Auswahl des automatischen Modus.

## SD-Karte schreiben, sichern und verkleinern

Beim Schreiben Modell, Betriebssystem/IMG, Zielmedium und Konfiguration prüfen. Das Zielmedium wird überschrieben; Windows kann dafür erhöhte Rechte verlangen. Nach dem Schreiben den vollständigen Lesevergleich abwarten. Eine unterbrochene Karte neu schreiben.

Für ein Abbild ein anderes ausreichend großes Ziellaufwerk verwenden. FAT32 unterstützt keine Dateien über 4 GiB. Beim Verkleinern arbeitet der Raspberry im RAM-Wartungsmodus mit ausgehängtem Root-Dateisystem. Dateisystem und Partition werden geprüft. Ein kleines Dateisystem allein macht noch kein kleines Kartenabbild. Wartungsabschluss und tatsächliche Abschaltung am Gerät kontrollieren. Nach dem Wiedereinsetzen den vorgesehenen normalen Start beziehungsweise Expandierauftrag abwarten.

## Sicherungen, Updates und Fehler

Anwendungseinstellungen vor größeren Änderungen sichern. Allsky-Sicherungen enthalten Versionsinformationen; eine Wiederherstellung kann denselben Quellstand erfordern. „Update-Sicherungen“ zeigt vorhandene Sicherungen und alte Installationen; nur ausdrücklich ausgewählte und bestätigte Einträge löschen. „Allsky-OLD löschen“ entfernt auch dort enthaltene alte Aufnahmen und Einstellungen.

Bei einem Fehler die letzten vollständigen Terminalzeilen mit Version, Aktion und Meldung festhalten. Keine parallelen Installations-/Updateaufträge starten. Die SSH-Konsole bleibt nach dem Update verfügbar und kann eingeklappt werden. „Clear Terminal“ leert nur die Anzeige. Softwareprüfungen ersetzen keinen Test mit dem angeschlossenen Raspberry, Witty, GPS-Empfänger oder Windows-Kartenleser.

## Release Notes

Die aktuelle Version ist 1.5 vom 10.11.2026. Die getrennten deutschen und australisch-englischen Release Notes enthalten die Änderungen pro Version/Build. Die Homepage führt eine Versionshistorie, das Windows-Hilfefenster bietet die passenden Änderungsinformationen. Die UTC-Einschränkung dieser Version betrifft das Windows-Auswahlfeld.
