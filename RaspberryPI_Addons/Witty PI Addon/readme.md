# Witty Add-on 0.8.5

Witty Add-on 0.8.5 | 13.10.2026
Änderungen gegenüber 0.8.4

Abschaltung nach der SD-Verkleinerung
- Der RAM-Wartungsmodus sendet den Hersteller-Heartbeat, beendet den Witty-Zustand STARTING und bedient den Watchdog während Dateisystemprüfung und Verkleinerung.
- Der Abschalthelfer prüft den Wechsel in STOPPING. Ein zurückgelesener Befehlswert wird nicht länger fälschlich als Abschaltbestätigung gewertet.
- Der Heartbeat endet vor der Abschaltmeldung. Die Bootpartition wird zuvor synchronisiert und ausgehängt.

Update-Ausgabe und Hilfe
- Das Terminal zeigt ausschließlich Änderungen seit der tatsächlich installierten Version und Build-Revision. Übersprungene Zwischenversionen werden berücksichtigt; bereits installierte Änderungen und spätere Builds entfallen.
- Bedienungsanleitung und README auf 0.8.5 aktualisiert. Release Notes sind nach Themen gegliedert.

Prüfstand
- Herstellerprotokoll mit STARTING, ignoriertem Abschaltbefehl und bestätigtem STOPPING in Softwaretests geprüft.
- Die tatsächliche Abschaltung von Pi und angeschlossenen Platinen erfordert einen Test an der Hardware.
