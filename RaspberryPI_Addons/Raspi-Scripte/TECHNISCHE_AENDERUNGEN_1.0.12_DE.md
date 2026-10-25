# Technische Änderungen 1.0.12 – 25.10.2026

## Fall 1: SD-Schrumpfung
Das Geräteprotokoll zeigt einen erfolgreichen Wartungsstart und einen erreichbaren Witty Pi 5. Der Abbruch erfolgt bei `resize2fs -M`, obwohl vorher `e2fsck -f -p` Erfolg meldete. Die Meldung über einen optional kürzeren Extent-Baum allein erklärt diesen Fehler nicht.

Der Abbruch wurde mit echtem e2fsprogs 1.47.2 nachgestellt: Eine RAM-Wartungsuhr nahe 1970 veranlasst e2fsck, den letzten Prüfzeitpunkt nicht zu aktualisieren. Dieser bleibt vor dem letzten Mount; resize2fs lehnt die Verkleinerung korrekt ab. Der frühe Wartungsstart hatte keine eigene Zeitsynchronisierung. Dass genau diese Uhrsituation auf dem betroffenen Gerät vorlag, kann das Foto ohne Uhrprotokoll nicht endgültig beweisen.

`witty-device-options` merkt jetzt den Unix-Zeitstempel der Vorbereitung vor. `witty-sd-offline-shrink` liest zusätzlich Erstellungs-, Mount-, Schreib- und Prüfzeit aus dem Superblock. Liegt die Wartungsuhr davor, wird nur die flüchtige Linux-Uhr im RAM auf einen plausiblen Zeitpunkt gesetzt. GNU date wird ausdrücklich ins Initramfs aufgenommen. Alle Berechnungen laufen mit UTC-Zeitstempeln. Witty-RTC und konfigurierter UTC-Offset werden nicht geändert; die PC-Uhr wird nicht abgefragt.

Danach läuft die echte Dateisystemprüfung. Vor `resize2fs -M` wird ausdrücklich geprüft, dass der Prüfzeitpunkt mindestens dem letzten Mount entspricht. Weder resize2fs -f noch gefälschte Prüfmarker werden eingesetzt. Die bestehende Partitionsverkleinerung mit 512 MiB Reserve, Hersteller-Abschaltung und Erweiterung beim normalen Boot bleiben erhalten.

## Fall 2: Größe und Events der Witty-Skripte
Die Herstellerlisten liefern Namen. Die bisherige Metadatenberechnung bearbeitete nur lokal gespeicherte WPI-Dateien. Deshalb konnten fünf Gerätedateien erscheinen, aber nur eine davon Größe und Events besitzen.

`cache_missing_schedule_metadata` prüft jetzt die Metadaten aller gelisteten Namen. Fehlende Originale werden in einer serialisierten Lesetransaktion vom Witty in ein temporäres Verzeichnis geladen. Erst ein erfolgreich beendeter Download mit nichtleerer regulärer Datei wird übernommen. Größe, vorhandene Eventberechnung und SHA-256 werden in `schedule-metadata.json` gespeichert. Bekannte Metadaten verhindern erneutes Herunterladen bei späteren Listenaufrufen. Lokale Upload-/Bearbeitungsvorgänge aktualisieren die vorhandenen Metadaten weiterhin. Änderungen direkt über fremde Herstellerwerkzeuge können ohne erneutes Lesen nicht allein am identischen Dateinamen erkannt werden.

Die Downloads aktivieren keinen Zeitplan. Bei Kommunikationsfehlern bleiben unvollständige Dateien aus dem Cache ausgeschlossen; spätere Abfragen dürfen erneut versuchen. Der Nachladevorgang hat einzelne Zeitlimits und ein Gesamtbudget. Beide Listenendpunkte nutzen dieselbe Routine.

## Prüfung
Gezielter Regressionstest: e2fsck-Erfolg plus resize2fs-Abbruch mit Uhr nahe 1970 reproduziert, danach korrigierte Routine erfolgreich ausgeführt. Reales ext4-Dateisystem verkleinert, Trägerdatei auf ausgerichtete Größe plus 512 MiB Reserve gekürzt, wieder erweitert, jeweils mit e2fsck und SHA-256-Datenvergleich. Zusätzlich Systemuhr eine Stunde vor und eine Stunde hinter der Referenz geprüft. Ein 128-GB-Kartenmodell mit 127322292224 Bytes Rootbereich wurde auf 1545601024 Bytes verkleinert und wieder erweitert.

Metadatentest: Drei Skripte mit unterschiedlichen Menüformaten vollständig eingelesen; zweiter Aufruf verursacht keinen weiteren Download. Ein abgebrochener Download veröffentlicht weder Teilkopie noch Metadaten.

Kein vollständiger Boot-/Partitionsgeräte-/Witty-Abschalttest auf dem betroffenen Raspberry Pi. Die neue Reproduktion erweitert ausdrücklich den bisherigen Testumfang; sie ersetzt keinen Hardwaretest.
