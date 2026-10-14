# Witty Add-on 0.9.7.1

Version 0.9.7.1 · Build 5
Änderungen gegenüber 0.9.7.1 Build 4

Windows-Oberfläche
- Beim Öffnen und Schließen von Meldungsfenstern wird die Maussteuerung freigegeben und ein sichtbarer Mauszeiger wiederhergestellt. Auch bei Rückkehr in das Hauptfenster und Mausbewegungen wird ein von WebView2 verborgen gebliebener Zeiger wieder eingeblendet. Die Windows-Mauseinstellungen werden nicht verändert.
- Bestätigungsdialoge sperren Terminaleingabe und automatische Fokusübernahme direkt in der Anwendung und im Terminal. Das eingebettete Terminalfenster wird dafür nicht mehr deaktiviert und erneut aktiviert.
- Der Witty-Add-on-Updatebutton ist abgedunkelt und nicht anklickbar, wenn keine neuere Version beziehungsweise kein neuerer Build verfügbar ist. Fehlende Basisinstallation und laufende Vorgänge sperren ihn weiterhin.

Diagnosestand
- Laut Nutzer bootet der Pi ohne Ethernet. Mit Ethernet und blockiertem GPS-Zeitdienst war ein Neustart ebenfalls erfolgreich. Ein einzelner erfolgreicher Vergleich beweist die Ursache noch nicht; der GPS-/RTC-Zeitpfad wird weiter isoliert geprüft.
- Build 5 verändert die GPS-Zeitroutine nicht. Die zehnsekündige Wiederverbindungspause und die gezielten Update-Schritte aus Build 4 bleiben enthalten.
