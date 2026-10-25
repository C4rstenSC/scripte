# 1.0.28

Version 1.0.28 – Änderungen gegenüber 1.0.27

- Allsky-Installation und Softwareupdate aus Windows: Die aktuelle PC-Zeit wird vorübergehend nur auf die Raspberry-Systemuhr übernommen. Dadurch können Debian-Signaturen und HTTPS mit korrekter absoluter Zeit geprüft werden, auch wenn Witty absichtlich anders läuft.
- Die Witty-RTC wird dabei nicht mit der PC-Zeit überschrieben. Zum Abschluss wird die weitergelaufene Witty-Zeit wieder auf den Raspberry übernommen. Dies gilt auch bei regulärem Installationsfehler/Abbruch und vor den über den Witty-Adapter ausgelösten Neustarts. Vor Allsky-Start bleibt Witty der Master.
- Fester UTC-Offset, aktive Zeitzone und Sommer-/Winterzeitmodus bleiben erhalten. Festes UTC+10 wird in Sydney nicht automatisch in Sommerzeit umgewandelt. Ohne verfügbare Witty wird die zuvor gesicherte Linux-Zeit einschließlich tatsächlich verstrichener Dauer wiederhergestellt.
- Signierte Debian-Paketlisten werden vor dem Verschieben oder Stoppen der Allsky-Installation geprüft. Auch teilweise fehlgeschlagene Listenaktualisierungen gelten als Fehler. Ein solcher Vorabfehler lässt keine neue ausstehende Allsky-Wiederherstellung zurück; das Sicherungsarchiv bleibt erhalten.
- GPS-Zeitzonenerkennung: Add-on-Updates reparieren nun ebenfalls die fehlende oder defekte Offline-Zeitzonendatenbank. Neuinstallation und Update verwenden dieselbe Einrichtung und prüfen echte Koordinaten für Berlin und Sydney. Die Homepage startet mit der passenden Python-Umgebung; unnötige Numba-JIT-Kompilierung ist abgeschaltet.
- GPS-Vorschlag und aktiver Zeitmodus werden getrennt: Auch bei erkannter Sydney-Zeitzone zeigt die Auswahl weiterhin den tatsächlich aktivierten festen UTC+10-Offset. Ein GPS-Fix ändert weder Witty-Uhr noch Zeitmodus automatisch.
- Fehlt die Offline-Datenbank weiterhin, nennt die Homepage diese Ursache statt nur „Zeitzonenermittlung nicht möglich“. Ein defektes optionales Python-Modul legt nicht den gesamten Webserver lahm.
- Die Bootdatei-Korrektur aus 1.0.27 bleibt enthalten: keine automatische Wiederherstellung einer leeren Startzeile.

Installation: zuerst Windows 1.0.28, danach Witty Add-on 1.0.28. Erst anschließend Allsky installieren/aktualisieren. Die vorübergehende PC-Zeit setzt eine korrekt eingestellte PC-Uhr voraus. Eine Installation direkt von der Witty-Webseite besitzt keine PC-Zeitquelle.
Prüfung: Windows/Updater gebaut; automatische Tests für Rückstellung bei Erfolg und Fehler sowie für GPS Sydney mit festem UTC+10. Offline-Koordinatenabfragen mit timezonefinder 9.0.0 und echter Datenbank erfolgreich. Kein physischer Test des neuen temporären Zeitpfads auf dem Raspberry.
