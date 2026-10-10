# Witty Add-on 0.7.4

Build 2 (20261010.2) – 10.10.2026

Witty Add-on 0.7.4 – Build 2 – 10.10.2026

- Hintergrund-GPS-Abfragen sperren den Ladebutton in Allsky-Setup nicht mehr. Ein Klick nutzt eine laufende Abfrage mit und wartet auf deren Ergebnis.
- Kurze GPS-Aussetzer lassen den Button nicht flackern. Ausblenden erst nach drei aufeinanderfolgenden Fehlabfragen und mindestens 15 Sekunden seit dem letzten gültigen Fix; deaktiviertes GPS wirkt sofort.
- Koordinaten werden ausschließlich aus einer aktuellen gültigen Antwort übernommen. Ohne aktuellen Fix erscheint ein Hinweis; bereits eingetragene Koordinaten bleiben erhalten.
- Alle Änderungen aus 0.7.3 Build 3 bleiben enthalten: Allsky-Logo, einheitliche Navigation, Ersteinrichtungshinweise, GPS-Übernahme, kompakte Felder und 0,5-Sekunden-Raster mit freien manuellen Eingaben.
- Windows-Programm unverändert; nur Witty Add-on aktualisieren.

English

- Background GPS polling no longer disables the receiver button in Allsky Setup. A click joins an in-flight request and waits for its result.
- Short GPS dropouts do not flicker the button. It hides only after three consecutive failed reads and at least 15 seconds since the last valid fix; disabled GPS takes effect immediately.
- Only a current valid response supplies coordinates. Without a current fix, a message appears and existing inputs remain unchanged.
- All 0.7.3 Build 3 improvements are retained. Windows application unchanged; update Witty Add-on only.


0.7.4 Build 2 – Allsky-Speicherort
- Automatische Auswahl der installierten Allsky-Methode: 2024 nutzt die bisherige PHP-Konfiguration; ab 2026 wird variables.json mit dem offiziellen Generator neu erstellt und der Web-Bildalias angepasst. Trixie/PHP-FPM bleibt erhalten.
- USB/SD-Wechsel, Verschieben/Kopieren/Belassen und Rückrollen bei Fehlern geprüft. Wiederherstellung aktualisiert auch veraltete 2026-Pfaddaten; Softwarestandprüfung bleibt erhalten.
- Webseite zeigt die zur Allsky-Version passende Speicher-Konfiguration auf Deutsch und Englisch.
- Backup und Wiederherstellung über Webseite und Windows verwenden dieselben geprüften Schnittstellen: Speicherpfad und Benutzereinstellungen werden gesichert; die passende Web-Konfiguration wird nach Wiederherstellung erzeugt. Aufnahmen bleiben unberührt; Wiederherstellung erfordert denselben Allsky-Softwarestand.

English – 0.7.4 Build 2 storage update
- Automatically use the installed Allsky format: legacy PHP defines for 2024, regenerated variables.json and image alias for 2026 onward. Existing Trixie PHP-FPM configuration is preserved.
- USB/SD changes, move/copy/leave semantics and rollback tested. Restore refreshes stale 2026 path data; exact software version validation remains in place.

- Web and Windows backup/restore share validated endpoints, preserving storage settings and regenerating the release-specific web configuration. Captured images are untouched; restoring requires the same Allsky software build.
