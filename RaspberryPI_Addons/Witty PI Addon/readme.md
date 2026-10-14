# Witty Add-on 0.9.8

Version 0.9.8 · Build 2
Änderungen gegenüber 0.9.8 Build 1

SSH-Terminal nach Witty-Update
- Der Ausgabefilter unterscheidet einzeilige Witty-Kontrollmeldungen des Update-Starters von mehrzeiligen Kontrollblöcken. Die einzeilige Meldung hatte bisher sämtliche folgenden Ausgaben einschließlich Shell-Prompt verborgen.
- Normale Update-Ausgaben, Eingaben und Antworten bleiben sichtbar. Interne Befehlszeilen und Kontrollmeldungen werden weiterhin nur für die Darstellung ausgeblendet; die Abschlussprüfung wertet sie unverändert aus.
- Jede neue Terminalverbindung setzt den Filter zurück, damit ein zuvor unvollständiger Kontrollblock die neue Sitzung nicht verbirgt.

Prüfung
- Der tatsächliche Meldungsablauf des Witty-Starters einschließlich nachfolgender Shell-Eingabe und Antwort wurde an allen Byte-Aufteilungen geprüft. Ein neuer Terminalstart nach einem unvollständigen Kontrollblock wurde ebenfalls geprüft.
- Die Kompilierung von Windows-Anwendung und Updater wird im nativen Build geprüft. Der Bedienungstest über den Pi-Hotspot bleibt erforderlich.
