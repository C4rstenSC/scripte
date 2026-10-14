# Witty Add-on 0.9.7.1

Version 0.9.7.1 · Build 6
Änderungen gegenüber 0.9.7.1 Build 5

GPS-Zeitdienst beim Start
- Der GPS-Zeitdienst wartet vor dem automatischen Abgleich 20 Sekunden. Der Nutzer meldete damit einen erfolgreichen Neustart nach zuvor reproduzierten Bootabbrüchen. Die genaue Ursache ist noch nicht bewiesen.
- Basisinstallation, Add-on-Update und Nachinstallation der Herstellersoftware verwenden dieselbe verzögerte Dienstdefinition. Das Startlimit berücksichtigt die zusätzliche Wartezeit; der manuelle Zeitabgleich bleibt unverzögert.
- Der exakt passende startup-test.conf-Override aus dem gemeinsamen Test wird bei der Übernahme entfernt. Die Verzögerung wird damit nicht doppelt ausgeführt. Andere benutzerdefinierte Overrides bleiben erhalten.

Zeitkonfiguration
- Bereits ausgeschaltete Netzwerk-Zeitsynchronisierung und bereits dauerhaft maskierte Zeitdienste werden nicht erneut eingerichtet.
- Änderungen an Zeitdiensten werden ohne einzelne automatische systemd-Neuladungen gebündelt; nur bei tatsächlichen Änderungen wird abschließend einmal explizit neu geladen. Auch noch nicht installierte Zeitdienste bleiben für spätere Paketinstallationen dauerhaft gesperrt.
- Vorhandene veraltete Zeitdienstdateien werden gezielt entfernt. Unveränderte Zustände verursachen keine erneute Dienstneuladung.

Diagnosestand
- Die Logs zeigen Bootabbrüche nach etwa 9–10 Sekunden und einen erfolgreichen Kaltstart mit laufendem GPS-Zeitdienst. Unterspannung wurde sowohl beim erfolgreichen als auch bei fehlgeschlagenen Starts erfasst.
- Der manuelle GPS-Zeitabgleich war erfolgreich. Die Startverzögerung ist eine anhand des Nutzertests übernommene Maßnahme, kein Nachweis für die vollständige Ursache oder den Ausschluss von Versorgungsproblemen.
