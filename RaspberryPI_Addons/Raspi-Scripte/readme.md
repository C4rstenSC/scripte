# Raspi-Scripte 1.0.4

Version 1.0.4 · Build 1
Änderungen gegenüber 1.0.3

Zeiten im Windows-Programm
- Zwischen „Aktuelle Witty Konfiguration“ und den Neustart-/Herunterfahren-Buttons werden Raspberry-Systemzeit und Witty-Pi-Zeit mit Datum und Sekunden angezeigt.
- Unter den Uhrzeiten werden – sofern vorhanden – GPS-Position mit Breitengrad/Längengrad und die verwendeten/sichtbaren Satelliten aus der Homepage angezeigt. Fehlende Angaben werden nicht als Null dargestellt.
- Eine gültige GPS-Zeit wird als dritte Zeile eingeblendet. Ohne verfügbaren GPS-Zeitwert bleibt diese Zeile verborgen.
- Die Werte werden aus derselben Homepage-Schnittstelle wie die Geräte-Webseite gelesen. Die Zeitzone des Raspberry bleibt erhalten; Windows-PC-Zeit und Windows-Zeitzone ersetzen die Gerätewerte nicht.
- Die Sekunden laufen zwischen den Abfragen mit einer monotonen Zeitmessung weiter. Messzeitstempel gleichen das Alter der einzelnen Quellen aus. Raspberry-/Witty-Werte werden regelmäßig neu gelesen, GPS wird unabhängig abgefragt.
- Fehlgeschlagene oder veraltete Messwerte werden nicht unbegrenzt weitergezählt. Beim Trennen, Schließen eines Host-Tabs und geplanten Neustart werden die Abfragen beendet. Nach Wiederverbindung wird die Anzeige neu eingelesen.
- Jede Raspberry-Verbindung besitzt eigene Uhrwerte und Abfragen. Die Beschriftung folgt der gewählten Sprache.

Die Funktionen aus 1.0.3 – PC-Zeitabgleich, Original-Firmwaredownload und Datumsparser – bleiben enthalten.
