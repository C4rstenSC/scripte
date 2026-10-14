# Witty Add-on 0.9.9

Version 0.9.9 · Build 2
Änderungen gegenüber 0.9.9 Build 1

Witty-Zeitplan in der Windows-Statuszeile
- Bei bestätigter montierter Hardware und installierter passender Hersteller-Software für Witty Pi 3, 4 oder 5 werden Zeitplan und Schalttermine angezeigt. Ohne Witty-Hardware bleibt die Anzeige verborgen.
- Nächstes Herunterfahren und nächstes Hochfahren stehen untereinander im Format HH:MM      DD.MM.YYYY. Darunter stehen die Minuten bis zum Shutdown.
- Die Zeitplandaten werden ausschließlich bei erfolgreicher Verbindung beziehungsweise Wiederverbindung gelesen. Der Minuten-Countdown wird anschließend lokal aus der Shutdownzeit und der aktuellen Windows-PC-Uhrzeit berechnet; dafür gibt es keine weiteren SSH- oder Witty-Abfragen.
- Aktuelle bereits von der Homepage gelesene Werte werden bis zu 30 Sekunden lang wiederverwendet. Falls kein aktueller Cache vorliegt, wird beim Verbinden einmalig der gemeinsame Witty-Status gelesen.
- Der Button „Zeitplan deaktivieren“ verwendet die gemeinsame Homepage-Backendfunktion. Erst nach bestätigtem Erfolg werden Termine und Countdown deaktiviert; gespeicherte Zeitplandateien bleiben erhalten.

Prüfung
- Softwaretests prüfen Witty 3/4/5, Hardware- und Installationsprüfung, Datumsformat, lokalen Countdown, inaktive Zeitpläne, erfolgreiche und fehlgeschlagene Deaktivierung sowie Cacheablage und Löschung.
- Der native Windows-Build prüft die Kompilierung. Die neue Statuszeile und die Schaltzeiten benötigen den Vergleich mit der Homepage am Gerät.
