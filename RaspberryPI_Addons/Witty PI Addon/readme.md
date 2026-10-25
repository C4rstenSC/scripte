# 1.0.15

Version 1.0.15 – SD-Wartungsstand, messbare Zeiten und Windows-Module

- Den gemeldeten tune2fs-Zeitstempel vor dem Datumsaufruf in ein eindeutiges ISO-Format umwandeln. Wochentag und Monatsname werden nicht mehr an den Datumsparser übergeben. Fester UTC-Offset, Sommerzeitwahl und Witty-RTC bleiben erhalten.
- Im fertigen Wartungsimage den ausführenden Schrumpfhelfer und den privaten GNU-Datumsleser bytegenau mit den aktuellen Quelldateien vergleichen. Abweichende Images werden nicht gestartet. Build, Prüfsummen und eindeutige Auftragskennung im Protokoll festhalten.
- Das Add-on-Update aktualisiert auch einen vorhandenen unabhängigen Windows-Wartungsordner. Die neue Windows-DLL stellt den aktuellen Wartungshelfer vor einer Aktion erneut bereit.
- Windows-Programm, Inhalt, Fensterüberschrift und Witty Add-on gemeinsam auf 1.0.15 setzen. Das normale Windows-Komplettupdate enthält mit ausdrücklicher Freigabe auch die EXE.
- Neue Windows-DLL: aktueller Schritt, Fortschrittsbalken und tatsächlich gemessene Zeiten innerhalb des roten SD-Rahmens. Keine Restzeitschätzung. Offline-Dauer und letzter Schritt werden nach Auslesen des Berichts angezeigt.
- Beim Schrumpfen bleibt die Geräteansicht trotz SSH-Ausfall erhalten. Erst ein manueller Klick auf Verbindung trennen beendet die Anzeige. Weder Verbindungsabbruch noch Zeitablauf werden als Schrumpferfolg gewertet. Ein alter Bericht darf einen neuen Auftrag nicht abschließen.
- Nach Einlegen der Karte am Windows-PC werden Ergebnisbericht, Dateisystemgröße und Partitionsgrenze gemeinsam geprüft. Fehler bleiben sichtbar; Erfolg erfordert den passenden verifizierten Auftrag.

Prüfung: 32 SD-Regressionen, Windows-Modelltests und bestehende Abbildtests; Windows-x64-Module kompiliert. Kein nativer Windows-Oberflächentest und kein physischer Raspberry-Schrumpf-/Abschalttest. Die genaue Ursache dafür, dass nach 1.0.13.2 erneut der frühere Parserfehler erschien, ist ohne das vollständige Geräteprotokoll nicht abschließend belegt. Allsky 1.0.14 bleibt separate Folgearbeit.

Windows-Komplettupdate über die normale Updatefunktion; EXE mit ausdrücklicher Freigabe enthalten.
