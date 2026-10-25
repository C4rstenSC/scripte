# Raspi-Scripte – Inhaltsupdate 1.0.13

Programmdateien: 1.0.12. Aktualisierter Inhalt und Wartungshelfer: 1.0.13.

Für dieses reine Inhaltsupdate den Entwicklermodus ausschalten. Dann das Programmupdate ausführen und nach dem Programmneustart das Witty-Add-on aktualisieren. Danach den vorhandenen Schrumpfauftrag einmal über „Partitionen schrumpfen“ erneut anstoßen; der neue Helfer prüft und repariert den vorbereiteten Auftrag.

Version 1.0.13 – SD-Wartungsstart und automatische Diagnose

- Ursache des nicht gestarteten Schrumpfens behoben: Eine Bash-Prozesssubstitution bestand die sh-Syntaxprüfung des Initramfs-Generators nicht. Der Helfer lag im Image, fehlte aber in der Startreihenfolge.
- Wartungsimage vor jedem Neustart zusätzlich auf den tatsächlichen Eintrag des Schrumpfhelfers in scripts/local-premount/ORDER prüfen. Bei fehlendem Eintrag kein Wartungsneustart.
- Vorbereitete, noch nicht ausgeführte Aufträge können nach Prüfung von UUIDs, Partitionsgeometrie, Kernel und unveränderter Bootkonfiguration repariert werden. Die Reparatur selbst verändert keine Partition.
- Bei jedem Schrumpfauftrag automatisch witty-sd-diagnose.log anlegen: Vorbereitung, Befehle, Ausgaben, Fehlercodes, Laufzeiten, Offline-Schrumpfen und Hersteller-Abschluss. Während längerer Befehle alle 15 Sekunden einen Laufhinweis speichern.
- Protokoll auf der Bootpartition erhalten; bei neuem Auftrag den vorherigen Lauf archivieren. Bei einem Kernel-Zwischenneustart das laufende Protokoll fortsetzen.
- Diagnoseausgaben während der Vorbereitung zusätzlich auf stdout ausgeben; der vorhandene Windows-Build sammelt diese noch bis zum Befehlsende. Live-Anzeige, Fortschrittsbalken und Restzeit im Windows-Fenster sind in diesem Sofortfix noch nicht enthalten.

Prüfung: Fehler mit Debians Initramfs-Startlistengenerator reproduziert; korrigierten Eintrag geprüft. Shell-Syntax, Diagnoseverhalten und SD-Regressionen geprüft. Physischer Boot-/Abschalttest auf Raspberry Pi noch offen.
