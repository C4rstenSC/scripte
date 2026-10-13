# Raspi-Scripte 0.8.7

Raspi-Scripte 0.8.7 | 13.10.2026
Änderungen gegenüber 0.8.6

IMG-Sicherung und Prüfung
- Die SD-Karte wird einmal gelesen. Dabei entsteht eine SHA-256-Prüfsumme ihrer kopierten Daten. Nach dem Schließen und Flush der Zieldatei wird das gespeicherte IMG erneut geöffnet, vollständig gelesen und gegen diese Prüfsumme geprüft.
- Die Prüfung benötigt keinen zweiten Rohzugriff auf die Karte. Beschädigte, verkürzte und abgebrochene Sicherungen werden nicht als fertig ausgegeben.
- Nach erfolgreicher Hostname-Abfrage lautet der vorgeschlagene Dateiname Datum-Hostname.img, beispielsweise 2026-10-13-wurbi-n99.img. Eigene Dateinamen werden erhalten.

Partitionsstatus
- Neue Wartungsberichte sind an Hostname und Boot-/Root-UUID gebunden. Alte oder kopierte Berichte gelten nicht automatisch als aktueller Fehler eines anderen Raspberry.
- Expandiert, verkleinert und der Zustand einer tatsächlich zugeordneten Wartung werden getrennt angezeigt. Ältere nicht zuordenbare Protokolle bleiben im Hinweis verfügbar.

Installation und Homepage
- Enthält die Auswahloptimierung des Witty Add-ons: gemeinsame Paketliste aus den gewählten Modulen, GPS nur bei GPS-Auswahl, Witty-Hardwareänderungen nur bei gewähltem Witty.
- Reine Homepage-Installation erhält keinen Audio-, Video-, GPS- oder Compiler-Gesamtumfang und keine Witty-Zeitpolitik.
- Aktive Homepage-Buttons sind dunkler und deutlicher umrandet; deaktivierte Buttons bleiben heller.

Abschaltung
- Bereits installierte Herstellersoftware wird auch berücksichtigt, wenn die Homepage aktuell auf „Kein Witty“ eingestellt ist. Die reine Homepage-Installation installiert weiterhin keine Herstellerpakete.
- Der Wartungsabschluss verwendet shutdown now. Nach dem Hersteller-Aufruf wird STOPPING geprüft; bei einem ignorierten Herstellerbefehl sendet der geprüfte I2C-Helfer die Abschaltmeldung.
- Ohne installierte Witty-Herstellersoftware kann ein normaler Raspberry-Shutdown keine Witty-Stromabschaltung auslösen.

Erweiterung und Wiederverbindung
- Erweiterung verändert gezielt die Größe der letzten Partition und erhält deren übrige Felder. ext4 wächst direkt online oder über einen geprüften einmaligen Dienst nach dem Kernel-Neustart.
- Zurückgebliebene eigene Wartungs-Bootoptionen werden bereinigt. Ein zusätzlicher Witty-Stromzyklus während des Wartungsneustarts wird durch eine nur für den aktuellen Start gültige Sperre des Hersteller-Neustarthooks verhindert.
- „Abbrechen“ neben „Warte auf Raspberry“ stoppt die Wiederverbindung und schließt die Verbindung. Der Button ist nur während des Wartens sichtbar.

Deinstallation
- WURB/WIRC-Deinstallation aktualisiert zuerst das Backend und läuft sichtbar im SSH-Terminal.
- Die Erkennung „nicht vollständig installiert“ blockiert das Entfernen nicht mehr. Auch unvollständige Projektordner unter anderen Benutzern werden berücksichtigt, gesichert und anschließend aus den aktiven Installationspfaden entfernt.
- Befehlsfehler enthalten ihre tatsächliche Ausgabe statt nur einer Exit-Code-Zahl.

Tabs und mSD-Karten-Seite
- mSD-Reiter erhält die Logozeile mit passenden Texten. Die Tabs besitzen sichtbare Rahmen, eine erkennbare Auswahl und etwa 4 mm Abstand.

Prüfstand
- Softwaretests für 96 Auswahlkombinationen, Prüfsummenfehler, Dateinamen-/Oberflächenabläufe und Witty-Abschaltbestätigung durchgeführt.
- Verkleinerung am Gerät vom Nutzer bestätigt. Die vollständige Stromabschaltung bleibt am angeschlossenen Witty zu überprüfen.
