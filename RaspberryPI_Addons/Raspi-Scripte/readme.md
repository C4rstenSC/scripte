# Raspi-Scripte 0.8.8

Raspi-Scripte 0.8.8 | 13.10.2026
Änderungen gegenüber 0.8.7

SD-Karte schreiben und sicher auswerfen
- Alte Partitionstabelle mit einem eigenen Vorbereitungshandle entfernen. Dieser wird vor dem Öffnen des neuen Schreibhandles geschlossen; die Hardwarekennung wird erneut geprüft.
- Schreibphasen, Bytebereiche und Windows-Fehler werden unter %LOCALAPPDATA%/Raspi-Scripte/SdJobs/Logs protokolliert. Die vollständige Prüfung der geschriebenen Karte bleibt erhalten.
- Bei Auswurf-Veto 8 wird nur der unmittelbar zugehörige USB-Kartenleser angefordert, wenn er ausschließlich diese Karte enthält. USB-Hubs und andere Geräte werden nicht mit ausgeworfen.
- Vorübergehende offene Windows-Zugriffe werden begrenzt abgewartet. Abschlüsse erscheinen im Fenster ohne Popup. Eine abgelehnte Auswurfanforderung wird getrennt vom erfolgreichen Schreiben angezeigt.
- Erfolgreiche IMG-Erstellung und Hostnamenänderung werfen ebenfalls sicher aus und setzen Fortschritt und Laufwerksauswahl zurück. Das Backup-Zielverzeichnis bleibt erhalten; ein freier Folgedateiname wird vorgeschlagen.

Hostname und Hotspot
- Nach Hostnamenänderung am verbundenen Pi werden Geräteinformationen, IP-Adresse und Verbindungsliste neu eingelesen.
- Im Bereich „SD-Karte von Abbild beschreiben“ erscheint der ausgelesene Hostname über den Buttons. Ein offline vorbereiteter neuer Name wird als für den nächsten Pi-Start vorbereitet gekennzeichnet.
- Hostnamenänderungen beim Schreiben passen vorhandene Installer-Hotspotprofile auf wifi4bats-, allskywifi- bzw. wifi- plus Hostname an. Passwörter, UUIDs, normale WLAN-Profile und weitere Einstellungen bleiben erhalten.
- Zu lange Hotspotnamen werden vor Änderung der Bootdateien abgelehnt.

Basisinstallation, Updates und Witty
- Wiederverbindung auch bei verlorener Neustartmeldung während Basisinstallation oder Update. Lange Installationen verbrauchen nicht die Drei-Minuten-Frist; diese beginnt beim Verbindungsabbruch. Abbrechen schließt die Sitzung.
- Witty-Herstellersoftware kann nach einer Basisinstallation mit „Kein Witty“ nachinstalliert werden. Die Zeile bleibt sichtbar und bietet Witty Pi 4/5 sowie einen Installationsbutton.
- Installation prüft die angeschlossene Hardware, korrigiert WP4-Auswahl bei erkanntem WP5 und richtet Hersteller-, Abschalt-, I2C- und Zeitdienste gezielt ein. Andere Module werden nicht erneut installiert.
- Hersteller-Deinstallation entfernt ausschließlich die Herstellerkomponente und lässt Add-on-Homepage und Anwendungen bestehen.
- Ohne installierten Witty bleibt der normale Linux-Abschaltweg verfügbar. Wartung verwendet ohne Witty keinen Hersteller-Abschlussmodus.

Oberfläche
- Beide Tabs besitzen einen dickeren schwarzen Rahmen und gleiche Innenabstände.
- „Ausgewählte Konfig installieren“ steht direkt links neben „Abbrechen“.
- Überschriften: „SD-Karte mit neuem Abbild beschreiben“, „SD-Karte Abbild erstellen“ und „SD-Karte von Abbild beschreiben“.
- Während Erweiterung und Neustart wird der alte Partitionszustand nicht als aktuell angezeigt; der tatsächliche Zustand wird nach Wiederverbindung gelesen.

Prüfstand und offene Hardwareprüfung
- Lokale Software-, Dateisystem-, Übertragungs- und Wiederverbindungstests erfolgreich. Der zweite Schreibversuch wurde am Gerät als erfolgreich gemeldet; die neue Handle-Trennung benötigt noch den Gerätetest.
- Korrekte Witty-Abschaltung wurde nachfolgend vom Nutzer am Gerät bestätigt. Abschaltdienst muss im poweroff.target eingebunden sein; sein Protokoll wird auf der Bootpartition gespeichert. Diagnoseskript liest Herstellerdienste, Firmware, Witty-Zustand und Abschaltverzögerung ohne Abschaltung.
