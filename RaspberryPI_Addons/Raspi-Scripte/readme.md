# Raspi-Scripte 1.4

Version 1.4 – 07.11.2026

- Allsky: Das Add-on-Update erneuert jetzt auch den global installierten Kamera-Helfer und prüft dessen Inhalt und Ausführbarkeit. Die Softwareverwaltung verwendet direkt den Patch aus dem aktuellen Add-on. Alte und neue Kameradateinamen werden berücksichtigt; die unnötige OV5647-Voraussetzung entfällt. Archiv und Herstellerdownload verwenden dieselbe Vorbereitung.
- Zeitzone: Abgeschlossene Installationssicherungen werden nach erfolgreicher Wiederherstellung entfernt. Alte Sicherungen ohne aktuelle Bootkennung ändern die gewählte Zeitzone nicht mehr. Ein fester Offset bleibt erhalten, statt durch alte regionale Sommerzeitregeln ersetzt zu werden.
- UTC-Auswahl: Der ausdrücklich ausgewählte feste Offset wird unverändert an alle Backends übertragen. Keine erneute Ableitung aus dem Sommerzeitstand eines Ortsnamens. Automatischer Modus und feste Auswahl bleiben getrennt.
- Homepage: Bei festem Modus wird der aktive Offset vor einem früher gespeicherten Ortsnamen ausgewählt. Neu geschriebene feste Zeitzonendateien werden ohne veralteten Python-Zeitzonencache gelesen.
- Windows, Inhaltspakete und eingebettetes Witty-Add-on tragen denselben Stand 1.4. Änderungen aus 1.3.9 einschließlich Livebild und November-Archiv bleiben enthalten.

Prüfung: Reale Allsky-Shellquellen zweier Generationen, andere Sensoreinträge, wiederholte Patchanwendung, Zeitzonensicherungen, alle drei Backends mit positiven/negativen und gebrochenen Offsets sowie JavaScript-Übertragung und aktive Auswahl geprüft. Windows-Build und gezielte Windows-Tests werden im Buildlauf geprüft. Kein physischer Raspberry-/Kamera-Installationstest auf Papas Gerät.
