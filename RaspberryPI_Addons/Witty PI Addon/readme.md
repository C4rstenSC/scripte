# Witty Add-on 1.0.2

Version 1.0.2 · Build 1
Änderungen gegenüber 1.0.1 Build 5

- Die interne Raspberry-Pi-5-RTC wird bei jeder Installation und beim Add-on-Update deaktiviert, unabhängig vom GPS-Modus. Die Bootkonfiguration erhält die Einstellung ausdrücklich im globalen [all]-Abschnitt. Nach einer Änderung ist ein Neustart erforderlich.
- Vor dem ersten Start der Allsky-Dienste pro Boot wird die Witty-RTC in die Linux-Systemzeit übernommen und beim Witty Pi 5 zurückgelesen. Bei fehlgeschlagenem Abgleich oder mehr als zehn Sekunden Abweichung startet Allsky nicht mit unbestätigter Zeit.
- Allsky, Allsky-Periodik und der zugehörige Timer erhalten eine verbindliche Startabhängigkeit zum einmaligen Zeitabgleich. Ein normaler Dienstneustart löst keine wiederholte Uhrzeitänderung aus.
- Allsky nutzt ausschließlich die Witty-RTC als Zeitquelle. Automatische GPS-Zeitübernahme und GPS-DST-Zeitjobs werden für Allsky unterbunden. GPS als Zeitquelle bleibt für Installationen ohne Allsky separat verfügbar.
- Nachinstallation, Neuinstallation, Herstellerinstallation und Add-on-Update richten denselben Boot-Zeitpfad ein. Ohne konfigurierte Witty-Hardware wird keine Abhängigkeit auf eine nicht verfügbare Witty-Uhr gesetzt.
- USB-Mount-Nachrüstung und Zeitschutz der Herstellerinstallation aus 1.0.1 Build 5 bleiben enthalten.
