# Witty Add-on 1.0.9.1

Version 1.0.9.1 · Build 1

Allsky: Zeitbasis für Aufnahme und Countdown angleichen
- Die Allsky-Webseite verwendet bei eingeschalteter Witty-Zeitübernahme jetzt denselben Zeitmodus wie die Aufnahmedienste und sunwait.
- Feste UTC-Offsets werden in PHP ausdrücklich als feste Abweichung verarbeitet. Die eigene Zone Witty/FixedOffset muss PHP dafür nicht kennen; eine alte PHP-Sommerzeitzone wird nicht mehr ersatzweise verwendet.
- Der Aufruf von sunwait aus der Webseite erhält denselben UTC-Offset bzw. dieselbe gewählte Zeitzone. Countdown, Umschaltuhrzeit und Sonnenzustand verwenden damit dieselbe Zeitbasis.
- Falls vorhanden, wird auch allskyserver.service in die Zeitvorgabe einbezogen. Zuvor gestoppte Dienste bleiben gestoppt.
- Nach Witty-Update, Allsky-Neuinstallation oder Allsky-Update wird die PHP-Korrektur zusammen mit den gespeicherten Ordner-/Zeitregeln wieder eingerichtet. Beim Ausschalten der Witty-Zeitübernahme gilt wieder die bisherige Allsky-Webseitenregel.
- Keine pauschale Stundenverschiebung und keine Änderung der GPS-Koordinaten oder Systemuhr. Einen vorübergehend auf 135 Grad Ost verschobenen Längengrad bitte wieder auf den tatsächlichen Kamerastandort zurückstellen.

Geprüfter Fehlerfall
- 24.10.2026, 33.73304S / 151.09081E, Angle -6, fester Offset UTC+10: Umschaltzeit etwa 18:40 Uhr. Um 16:46 Uhr zeigt der korrigierte Countdown 1h 54m statt 54m.
- Echte PHP-/sunwait-Tests mit eingefrorenem Zeitpunkt, unterschiedlichen PHP-Standardzeitzonen, festen positiven/negativen UTC-Offsets und automatischer Sommer-/Winterzeit; zusätzlich Wiederherstellung und Rücknahme bei Fehlern geprüft.
- Kein Test auf dem betroffenen Raspberry Pi. Eine falsch laufende UTC-Systemuhr wird durch dieses Update nicht automatisch verstellt.
