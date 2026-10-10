# Witty Add-on 0.7.3

Build 3 (20261010.3) – 10.10.2026

Witty Add-on 0.7.3 – Build 3 – 10.10.2026

- Phase-Uhr entfernt; Gesamtzeit direkt hinter Schrittzahl und Prozenten. Automatische Allsky-Phasen und Python-Paket n/N werden erkannt; der Balken bewegt sich innerhalb der Installerphase. Prozentwerte sind gewichtete Schrittanteile, keine Zeitprognose.
- Erfolgreicher finaler Allsky-Neustart erfolgt erst nach der Witty-Abschlussprüfung und deren Rückmeldung. Notwendige Locale-Neustarts bleiben erhalten.
- Nach Wiederverbinden wird der alte Installationsfortschritt ausgeblendet. Verbindungsabbruch-Warnung bleibt im Vordergrund bis OK; der Terminalfokus darf das Fenster nicht überdecken.
- Terminal vor dem ersten Allsky-Dialog vergrößern und tatsächliche Zeilen/Spalten an SSH senden, bevor der Installer startet.
- Allsky-Kopf, Status, Seitenmenü und Inhalt stehen unter der Witty-Leiste. Die Abstände passen sich Zeilenumbrüchen und GS-Warnung an.
- Alle bisherigen GPS-, Trixie-, GS-Kamera- und Backup-Korrekturen sowie beide archivierten Allsky-Stände bleiben enthalten.

Witty Add-on 0.7.3 – Build 3 – 10 October 2026

- Removed phase timer; elapsed time follows completed steps and percentage. Automatic Allsky phases and Python package n/N advance progress within the installer step; percentages are weighted step fractions, not a time estimate.
- Successful final Allsky reboot follows Witty final checks and completion feedback. Required locale reboots remain unchanged.
- Reconnecting hides previous installation progress. The connection warning stays in front until OK; terminal focus cannot cover it.
- Enlarge the terminal and send its real rows/columns to SSH before launching the first Allsky dialog.
- Allsky header, status, sidebar and content sit below the Witty bar, with offsets adapting to wrapped links and GS warning.
- Previous GPS, Trixie, GS-camera and backup fixes and both archived Allsky versions remain included.

Allsky-Ersteinrichtung: fehlendes lastchanged in settings.json wird als noch erforderliche Einrichtung erkannt. Erfolgreiche Installation erfordert dann keinen laufenden Kameradienst. Beim Windows-Dienststart erscheint ein verständlicher Hinweis mit Angebot, die Allsky Settings zu öffnen.
Allsky initial setup: a missing lastchanged value in settings.json indicates pending setup. Successful installation then does not require a running capture service. Starting the service from Windows explains the required setup and offers to open Allsky Settings.

Nachtrag 0.7.3 Build 3: Rückwechsel Witty → Allsky lädt die Hauptseite mit frischer URL. Allsky-PHP setzt Cache-Control no-store; Navigation richtet Kopf, Seitenmenü und Inhalt auch bei pageshow und erneut sichtbarer Seite neu aus. Gemeinsames Navigationsskript korrigiert außerdem die Anordnung älterer zwischengespeicherter Allsky-Seiten. Windows-Programm unverändert; nur Witty-Update erforderlich.
0.7.3 Build 3 follow-up: Returning from Witty to Allsky uses a fresh main-page URL. Allsky PHP sends Cache-Control no-store. Navigation reapplies header/sidebar/content offsets on pageshow and visibility changes. The shared navigation script also repairs older cached Allsky pages. Windows application unchanged; only the Witty update is needed.

- Einheitliche Schriftgröße und Buttonhöhe auf Witty Add-on, Allsky und Allsky-Setup. Bildspeicherort steht oberhalb der Allsky-Datensicherung.
- Dienststart auf beiden Webseiten prüft die Allsky-Ersteinrichtung vorab und bietet einen Link zu Allsky Settings; Hinweise auf Deutsch und Englisch statt langer Dienst-Fehlerprotokolle.
- Unified font size and button height across Witty Add-on, Allsky and Allsky Setup. Image storage appears above Allsky backup.
- Starting Allsky from either web page checks initial setup first and offers a link to Allsky Settings, with German and English guidance instead of long service error logs.

Update-Korrektur Build 3: nicht gesetzte Variable app in der Build-Ausgabe durch app_dir ersetzt. Versionsgleiche Build-Updates zeigen bei geänderter Revision die aktuellen Release Notes.
Build 3 update fix: use the installed app_dir for build metadata instead of the undefined app variable. Updates between builds of the same version show release notes when the revision changes.

CloudedBats-Logo ganz links auch in der originalen Allsky-Navigation ergänzt.
CloudedBats logo added at the far left of the original Allsky navigation.
