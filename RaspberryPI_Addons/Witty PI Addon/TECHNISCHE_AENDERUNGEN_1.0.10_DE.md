# Technische Änderungen in Witty Add-on 1.0.10

Ziel: Die echten Kamerakoordinaten und der gewählte Sonnenwinkel steuern weiterhin Tag/Nacht. Bei eingeschalteter Witty-Übernahme gilt der gewählte feste UTC-Offset ganzjährig; alternativ gelten die Regeln der ausdrücklich gewählten Zeitzone. Der Standort wählt keine Zeitzone.

## Geänderte Dateien innerhalb der Allsky-Installation

| Datei | Technische Änderung |
|---|---|
| `variables.sh` | Exportiert den gewählten `TZ`-Wert, aktiviert `WITTY_ALLSKY_SOLAR=1` und setzt das Allsky-eigene `.witty-bin` vor den übrigen Suchpfad. |
| `.witty-bin/sunwait` | Auf dem Pi gebaute, lokal begrenzte sunwait-Korrektur. Sowohl `poll` mit DAY/NIGHT-Rückgabecode als auch der neue JSON-Status verwenden denselben UTC-Zustandsalgorithmus. Das systemweite `/usr/bin/sunwait` wird nicht ersetzt. |
| `.witty-bin/manifest.json` | Prüfsummen für Quellen und ausgerollte Programme. Verhindert unnötige Neubauten und erkennt durch Allsky-Updates ersetzte Dateien. |
| `src/allsky_common.cpp` | In `day_night_timeSleep()` wird bei aktiver Witty-Regel `sleep(secsTillNext)` auf 1 bis 60 Sekunden begrenzt. Danach kehrt die bestehende Hauptschleife zur echten Tag-/Nacht-Prüfung zurück. Ohne Witty-Regel bleibt der ursprüngliche Wartepfad erhalten. |
| `bin/capture_RPi`, `bin/capture_ZWO` | Nur die tatsächlich installierten Aufnahmeprogramme werden mit dieser gemeinsamen C++-Änderung neu gebaut. Die Tag-/Nacht-Aufnahmeeinstellungen bleiben erhalten. |
| `html/includes/functions.php` | Lädt die lokale Witty-Zeitregel. `getDayNightStatus()` liefert bei eingeschalteter Übernahme den gemeinsamen absoluten Sonnenstatus; die bisherige PHP-Regel bleibt für Allsky-Standard erhalten. Andere PHP-sunwait-Aufrufe erhalten ebenfalls den lokalen Suchpfad. |
| `html/includes/witty-time-policy.php` | Liest den gewählten Offset bzw. die benannte Zeitzone, fragt den JSON-Sonnenstatus ab und formatiert dessen absolute Ereigniszeitpunkte in dieser Zeitbasis. Kein pauschales `+1 day` bei widersprüchlichem Zustand. |
| `html/includes/witty-time-policy.json` | Enthält Übernahme ein/aus, Zeitmodus, Offset/Zeitzone und den Pfad zur lokalen Sonnenberechnung. |
| `scripts/saveImage.sh` | Die bereits vorhandene Witty-Ergänzung ordnet neue Bilder bei eingeschalteter Ordnerregel von 12:00 bis vor 12:00 am Folgetag dem Startdatum zu. Sie verwendet dieselbe gewählte Ortszeit. |

Außerhalb des Allsky-Verzeichnisses ergänzt das Add-on `60-witty-capture-policy.conf` in den systemd-Drop-in-Verzeichnissen von `allsky.service` und – falls vorhanden – `allskyperiodic.service` sowie `allskyserver.service`. Darin stehen TZ, lokaler Programmsuchpfad, Aktivierungsflag und die Wiederherstellung vor einem Dienststart.

## Was an der Sonnenberechnung korrigiert wurde

Die astronomischen Formeln von Allskys sunwait-Untermodul bleiben unverändert. Geändert wurde die Verarbeitung ihrer Ergebnisse:

1. Referenztage und Ereignisse werden direkt als UTC-Zeitpunkte behandelt. Die Berechnung führt keinen UTC-Zeitstempel mehr durch eine lokale `mktime()`-Interpretation.
2. Halbe und Viertelstunden werden bei der Offset-Ermittlung nicht auf ganze Stunden abgeschnitten.
3. Jeder Ereigniszeitpunkt wird erst danach in den gewählten Offset bzw. die gewählte Zeitzone umgerechnet. Bei fester Abweichung gibt es keine Sommerzeitumschaltung.
4. Die aktuelle Phase und der nächste tatsächliche Gegenwechsel stammen aus derselben Berechnung. Nach der Abendgrenze ist die Phase Nacht; das nächste Ereignis ist der Morgen.
5. Der Countdown berechnet die Differenz absoluter Zeitstempel. Er verschiebt eine vergangene Abend-Uhrzeit nicht einfach auf den nächsten Abend.
6. Zusätzlich verhindert die begrenzte Kamera-Wartepause, dass ein alter oder widersprüchlicher Zustand das Aufnahmeprogramm 23 Stunden schlafen lässt.

## Zuständige Add-on-Dateien

- `installer/allsky_capture_policy.py`: gespeicherte Schalter, TZ/PATH, PHP-Einrichtung, systemd und Wiederherstellung/Rollback.
- `installer/allsky_solar_runtime.py`: Bau und Prüfung des lokalen Sonnenprogramms sowie vorbereiteter Bau der vorhandenen Aufnahmeprogramme.
- `installer/sunwait-utc/`: mitgelieferte Quellen einschließlich GPL-Lizenz; Herkunft risacher/sunwait, Revision `151d8340a748a4dac7752ebcd38983b2887f5f0c`.
- `installer/allsky_time_policy.php`: Vorlage der Allsky-PHP-Ergänzung.
- `install.sh`, `manager/software_manager.sh`, `installer/finalize_allsky.sh`: Einrichtung bei Add-on-Update, Allsky-Installation und nach einem installerbedingten Neustart.
- `web/server.py`: Diagnose verwendet ebenfalls die lokale Sonnenberechnung und meldet deren absolute Zeitstempel.

## Referenzfall und Grenzen der Prüfung

Für 33.73304S / 151.09081E, Angle -6 und festen UTC+10-Offset liegt die Abendgrenze am 23./24. Oktober ungefähr bei 18:40 Uhr. Um 19 Uhr muss Nacht erkannt werden; der nächste Wechsel ist am Morgen. Die Testreihe prüft diesen Fall einschließlich Allskys tatsächlicher extrahierter C++-Steuerfunktionen, Übergangssekunden, australischer Zeitzonen, Zeitumstellungen und Datumsgrenzen.

Die komplette Kamerasoftware wird beim Anwenden auf dem Pi für dessen Architektur gebaut. Ein tatsächlicher Kameratest auf Papas Pi liegt noch nicht vor. Der Code stellt die Systemuhr nicht eigenmächtig um; die zugrunde liegende UTC-Zeit muss stimmen. Echte Koordinaten wiederherstellen, falls zuvor 135E als Ausgleich eingetragen wurde.

## Gewünschter Aufnahmeablauf bei festem UTC+10

| Zeitpunkt | Aufnahmemodus nach Sonnenwinkel | Ordner für neue Bilder |
|---|---|---|
| 23.10., 17 Uhr | Tag, solange die Sonne über -6 Grad steht | `20261023` |
| 23.10., nach der abendlichen -6-Grad-Grenze | Nacht | `20261023` |
| 24.10., nach der morgendlichen -6-Grad-Grenze | Wieder Tag | `20261023` |
| 24.10., 08 Uhr | Tag | `20261023` |
| 24.10., bis 11:59:59 Uhr | Nach aktuellem Sonnenstand | `20261023` |
| 24.10., ab 12:00 Uhr | Nach aktuellem Sonnenstand | `20261024` |
| 24.10., beispielsweise 17 Uhr | Wieder Tag, solange die Sonne über der Grenze steht | `20261024` |

17 und 08 Uhr sind Beispiele für das Aufnahmefenster, keine fest programmierten Tag-/Nacht-Umschaltzeiten. Vorhandene Witty-Start-/Stopppläne und die Allsky-Auswahl für Tag-/Nachtaufnahmen werden nicht überschrieben. Die neue Ordnerregel wirkt auf tatsächlich neu gespeicherte Bilder.
