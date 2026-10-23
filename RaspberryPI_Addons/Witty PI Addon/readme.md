# Witty Add-on 1.0.7

Version 1.0.7 · Build 1
Änderungen gegenüber 1.0.6 Build 2

GPS-Satelliten
- Auf Raspberry Pi 4 mit USB-GPS zusätzlich sichtbare Satelliten aus den GSV-Meldungen des vorhandenen WURB-Lesers auslesen. Kein zweiter USB-Leser und keine Änderung der Geräte- oder gpsd-Konfiguration.
- Mehrteilige GSV-Meldungen und mehrere Signalarten nicht doppelt zählen; veraltete Werte und fehlerhafte Prüfsummen verwerfen. Ohne aktuelle GSV-Daten bleibt die Zahl unbekannt.
- Raspberry-Pi-5-Pfad mit USB und Waveshare bleibt bei gpsd. Parallele Abfragen sowie GPS- und Stromanzeige wurden mit simulierten Gerätedaten getestet.

Zeiten und GPS Position
- Gemeinsamer Rahmen mit Überschrift im Stil der Witty-Konfiguration. Einheitliche Schriftgröße und Schriftart sowie automatisch ausgerichtete Wertespalten. Drei geschützte Leerzeichen hinter Raspberry-Systemzeit.
- Beim Pi 5 die interne RTC direkt unter der Systemzeit anzeigen. Bei aktiver RTC ihre eigene Zeit sekundengenau fortschreiben, bei deaktivierter RTC „Deaktiviert“ anzeigen. Bei fehlenden Daten „Nicht verfügbar“; beim Pi 4 keine zusätzliche RTC-Zeile.
- Softwaretests bestanden; kein neuer Hardwaretest am Raspberry durchgeführt.

Installation und Update
- Mittiger Button „Zur Witty Homepage“ öffnet die Add-on-Homepage des verbundenen Raspberry im Standardbrowser.
