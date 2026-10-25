# Raspi-Scripte 1.0.11

Version 1.0.11 · Build 1

Basisinstallation und PHP
- Linux-Paketlisten und installierte Pakete vor der Systemeinrichtung aktualisieren; vorhandene Basispakete können aktualisiert werden.
- Versionierte PHP-Laufzeitpakete auf die Sicherheitskorrekturen vom 21.10.2026 prüfen und erforderliche Updates über APT installieren; laufende PHP-FPM-/Webserverdienste nach Paketwechsel erneuern.

Allsky von GitHub
- Direkten Git-Klon bei vorübergehenden Fehlern bis zu dreimal mit Zeitlimit wiederholen.
- Bestehende, dem Raspberry-Benutzer gehörende Allsky-Quellen mit begrenzter Git-Vertrauensfreigabe prüfen.
- Vollständige UTC-Sonnenberechnung, gewählter Witty-Zeitmodus und Mittag-bis-Mittag-Ordnerregel aus 1.0.10 enthalten.

Witty-Skripte
- Aktivierungs- und Downloadlisten mit längerer Wartezeit und Wiederholungen zusammenführen.
- Abgebrochene Geräteabfragen nicht mehr als erfolgreiche Liste aus nur lokalen Dateien ausgeben.
- Aktiven Skriptnamen anhand der Originalinhalte mit längeren Downloadfristen wiederherstellen.

SD-Schrumpfung
- Wartungskernel und Initramfs auf dieselbe Kernelversion abstimmen, auch nach Linux-Updates auf Pi 5.
- Falls zuerst der neue Kernel starten muss: Schrumpfauftrag nach automatischem Neustart auf derselben Karte einmalig fortsetzen.
- Gemeinsamen Wartungshelfer in Windows und Add-on aktualisiert; echte Partitions-/ext4-Prüfung vor kleinem IMG bleibt erhalten.
- Geprüfte Verkleinerung, Hersteller-Abschaltung und automatische Erweiterung beim nächsten normalen Start bleiben verbunden.

Windows
- Vorhandene 1.0.9-Korrekturen für GPS-Satelliten, optionalen Zeitabgleich und gemeinsame Versions-/Buildabfrage übernommen.
- Programm, Inhaltspaket, eingebettetes Witty-Paket und Versionsanzeigen auf 1.0.11 abgestimmt.

Prüfung
- Automatisierte Python-/Shell-, PHP-/Sonnenzeit-, Windows-SD- und Uhrzeittests sowie lokaler win-x64-Build. Prüfung ohne angeschlossenen Raspberry Pi oder die betroffene SD-Karte.
