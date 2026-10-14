# Witty Add-on 0.9.9

Version 0.9.9 · Build 1
Änderungen gegenüber 0.9.8 Build 3

Allsky-Update und Neustart
- Die feste 30-Sekunden-Pause nach dem Allsky-Update entfällt. Nach erfolgreicher Konfigurationswiederherstellung und Abschlussmeldung wird der reguläre Neustart direkt ausgelöst.
- Abschluss und erwarteter Neustart werden vor dem Neustartbefehl gemeldet, damit Windows die automatische Wiederverbindung vorbereiten kann. Ein fehlgeschlagener Neustartbefehl wird weiterhin als Warnung ausgegeben.

Windows nach der Wiederverbindung
- Nach erfolgreicher automatischer Wiederverbindung wird die abgeschlossene Installations- oder Update-Fortschrittsanzeige ausgeblendet und das SSH-Terminal eingeklappt.
- Auch eine erfolgreiche manuelle Neuverbindung setzt die Fortschrittsanzeige zurück und klappt das Terminal ein. Die normale Shell bleibt bei erneutem Aufklappen bedienbar.

Startpause und Scrollposition
- Nach erkanntem Neustart wartet Windows 20 Sekunden ohne Verbindungsprüfungen. Anschließend stehen 60 Sekunden für die automatische Wiederverbindung zur Verfügung; die Startpause wird nicht davon abgezogen.
- Beim Aufklappen des SSH-Terminals scrollt die Programmoberfläche ganz nach unten. Beim Einklappen, beim angekündigten Neustart und nach erfolgreicher Wiederverbindung scrollt sie nach oben. Andere Raspberry-Tabs werden dabei nicht umgescrollt.

Verbindungszustand im Pi-Status
- Während des angekündigten Neustarts und der Wiederverbindung liegt ein grauer Schleier über dem Pi-Status. Schrift wird schwarz, Statuspunkte werden grau und die Statusbedienung gesperrt. Nach aktiver Verbindung werden die Originalfarben wiederhergestellt.

Prüfung
- Der unmittelbare Neustartablauf wurde mit erfolgreichen und fehlgeschlagenen Befehlen sowie ohne benötigten Neustart getestet. Die Abschlussmeldung kommt vor dem Neustartbefehl; es wird kein Warte-Timer verwendet.
- Witty-Tests und nativer Windows-Build prüfen die Software. Die geänderte Anzeige nach Wiederverbindung benötigt den Bedienungstest unter Windows.
