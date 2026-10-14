# Witty Add-on 0.9.7.1

Version 0.9.7.1 · Build 2
Änderungen gegenüber 0.9.7

- Ohne Basisinstallation werden auch die GPS-Auswahlbuttons ausgeblendet. Micro-SD-Wartung bleibt verfügbar; Host-Tabs behalten ihre getrennten Zustände.
- Allsky-Einstellungssicherungen werden auch zwischen RAM-Dateisystem und Sicherungsverzeichnis sicher übertragen: geprüftes Kopieren, Synchronisieren und atomisches Veröffentlichen. Bei Fehlern bleibt das Original erhalten.
- Allsky zeigt keine Git-Standardbranch-Hinweise oder redundanten Paket-Auswahlzeilen mehr. Fehler, Download-/Installationsfortschritt und vollständige Herstellerlogs bleiben erhalten.
- Erfolgreich geplante Allsky-Neustarts werden Windows ausdrücklich gemeldet. Ein hostbezogenes Fenster informiert über den Neustart und die Wiederverbindung.
- Vor Softwareinstallationen und Updates wird diagnose.txt auf der Bootpartition angelegt. Der normale Start wird durch einen unabhängigen Dienst beobachtet; Diagnoseprotokolle bleiben auch nach einem erfolgreichen Start erhalten und werden größenbegrenzt rotiert.
- Frühere Startprotokolle werden zusätzlich dauerhaft mit begrenztem Speicher gespeichert. Die Diagnose enthält Bootparameter, Dateisystemeinbindung, Datenträger, Kernelmeldungen, Dienstfehler und Witty-Dienstneustarts sowie Start-/Endzeiten, Rückgabestatus und Neustartanzahl aller Systemdienste. Linuxupdates ohne Basisinstallation laden nur den Diagnosehelfer.
- Der alte systemd.run-Diagnosestart wird nur mit exakt passender Original-Sicherung auf normale Bootparameter zurückgeführt. Fremde Wartungsaufträge und abweichende Sicherungen werden nicht überschrieben.

- Die Basisinstallation ordnet Raspberry-/Witty-Modelle absteigend, übernimmt die erkannte Hardware und sperrt beide Modellauswahlen. Unsichere Witty-Erkennung aktiviert keine Herstellerinstallation. Allsky steht mit zwei Leerzeilen Abstand unter WIRC.

- Die Netzwerksuche verwendet eine konsistente Momentaufnahme für die Fortschrittsanzeige. Dies behebt den im wiederholten Windows-Test beobachteten Absturz bei gleichzeitigen Geräteänderungen.

Prüfgrenzen
- Softwaretests prüfen Sicherung/Migration, Startdiagnose, Windows-Host-Isolation und Neustartmeldung. Die Ursache des gemeldeten Bootabbruchs ist nicht bestätigt; insbesondere wird keine automatische Dateisystemreparatur auf einer eingebundenen Karte ausgeführt. Der echte Neustart mit Witty und die Kamera benötigen den Gerätetest.
