# Raspi-Scripte 1.0

Version 1.0 · Build 1
Erste Vollversion – Änderungen gegenüber 0.9.9 Build 4

- Mittiger Statusblock mit Überschrift Aktuelle Witty Konfiguration und schmalem Rahmen um Angaben und Zeitplan-deaktivieren-Button.
- Geladenes Script mit Skriptnamen aus derselben Verbindungsabfrage wie auf der Homepage.
- Hochfahren steht über Herunterfahren; beide Zeitangaben sind in einer gemeinsamen Spalte exakt untereinander ausgerichtet. Format HH:MM      DD.MM.YYYY. Darunter stehen die Minuten bis zum Shutdown.
- Zeitplandaten beim Neuverbinden oder nach erfolgreicher Zeitplan-Aktivierung auf der Homepage aktualisieren. Der Countdown läuft lokal mit der Windows-PC-Uhr weiter, ohne zusätzliche Witty-Abfragen.
- Alle Korrekturen aus 0.9.9 Build 4 bleiben enthalten.
- Die Homepage benachrichtigt verbundene Windows-Sitzungen nach erfolgreicher Aktivierung mit den frisch eingelesenen Zeitplandaten. Nur Skriptname, Schaltzeiten und Countdown werden aktualisiert; keine zusätzliche SSH-/Witty-Abfrage und kein Neuaufbau der Verbindung.
