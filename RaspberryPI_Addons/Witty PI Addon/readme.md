# Inhaltsupdate 1.0.13.1

Version 1.0.13.1 – vorbereiteten Schrumpfauftrag nach RTC-Konfiguration reparieren

- Den gemeldeten Fehlalarm nachgestellt: Das Add-on-Update setzt seinen RTC-Abschnitt ans Dateiende. Der vorbereitete Wartungsblock steht danach vor diesem Abschnitt statt ganz am Ende.
- Den vollständigen Wartungsblock genau einmal erkennen, unabhängig von dieser Position. Nach Entfernen des Blocks müssen sämtliche übrigen nichtleeren Zeilen weiterhin mit der gesicherten Konfiguration in derselben Reihenfolge übereinstimmen. Hinter dem Block ausschließlich den bekannten RTC-Abschaltabschnitt zulassen.
- Fehlende, veränderte oder doppelte Wartungsblöcke sowie andere neue Bootoptionen weiterhin ablehnen. Vor dem Ersetzen des geprüften Images erneut auf zwischenzeitliche Konfigurationsänderungen prüfen.
- Die gesicherte normale Bootkonfiguration aus der geprüften aktuellen Fassung übernehmen, damit der deaktivierte interne RTC-Zustand beim Wartungsstart erhalten bleibt.
- Der Status „Wartung ausstehend“ bleibt bis zur tatsächlichen Ausführung des Auftrags korrekt bestehen. Reparatur oder Verbindungsverlust allein werden nicht als erfolgreiches Schrumpfen gewertet.

Update: Entwicklermodus ausschalten, oben im Windows-Programm das Inhaltsupdate 1.0.13.1 installieren, neu verbinden und das Witty-Add-on auf 1.0.13.1 aktualisieren. Danach einmal „Partitionen schrumpfen“ drücken. Keine manuellen Änderungen an config.txt und kein Löschen des Wartungsauftrags erforderlich.

Prüfung: Gemeldete Abschnittsanordnung, bisherige Anordnung und Ablehnung fremder/duplizierter Bootoptionen getestet. Physischer Schrumpf-/Abschalttest auf dem betroffenen Raspberry noch offen. Windows-EXE bleibt unverändert auf 1.0.12; Fortschritts-UI und Allsky-Aktualisierung stehen noch aus.
