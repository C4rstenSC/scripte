# 1.0.25

Version 1.0.25 – 25.10.2026

- Update-Schaltflächen nach dem Allsky-Neustart: Die Download-Sitzung wird auch dann freigegeben, wenn der Raspberry vor der letzten Terminal-Abschlussmeldung neu startet. Anschließende Linux-, Allsky- und andere Software-Updates werden nicht mehr durch die alte Sitzung blockiert.
- Verbindung trennen räumt die lokale Download-Sitzung und die alte Bedienungssperre auf. Der Trennknopf sendet keinen Neustart- oder Abschaltbefehl. Verspätete Ausgaben eines bereits geschlossenen Terminals werden ignoriert.
- Wenn tatsächlich noch ein Vorgang läuft, erscheint beim erneuten Update-Aufruf ein verständlicher Hinweis und das SSH-Terminal wird geöffnet.
- Linux-Update meldet den erfolgreichen Abschluss sichtbar. Nach bestätigtem Erfolg und erfolgreichem Statusabgleich wird das Terminal wie bei den anderen Updates eingeklappt und die Raspberry-Ansicht nach oben gescrollt. Bei einem Fehler bleibt die Ausgabe offen.
- Dasselbe Abschlussverhalten gilt für das Linux-Update eines frischen Images ohne bereits installiertes Witty-Add-on.
- Die Allsky-Installations-, Wiederaufnahme-, Datums- und SD-Fortschrittskorrekturen aus 1.0.24 bleiben enthalten.
