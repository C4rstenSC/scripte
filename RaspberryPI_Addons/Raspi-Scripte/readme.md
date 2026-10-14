# Raspi-Scripte 0.9.5

Version 0.9.5 · Build 20261014.2
Änderungen gegenüber 0.9.4

Allsky- und Softwareupdates – Build 20261014.2
- Allsky zeigt beim Update und bei der Neuinstallation die Auswahl der drei Quellen. Der Updatebutton bleibt auch bei gleichem GitHub-Stand für einen Versionswechsel anwählbar. Bestehende Kameraeinstellungen werden beim Update übernommen.
- Der Raspberry-Steuerbefehl akzeptiert die Auswahl auch für reinstall. Vor Erfolg und Konfigurationsmigration wird die tatsächliche Git-Revision gegen die gewählte Archiv-/Herstellerquelle geprüft.
- Die bestätigte Update-Migration darf die gesicherte Konfiguration des vorherigen Softwarestands übernehmen. Normale Wiederherstellungen behalten die strenge Versions-/Git-Prüfung. Neue options-/Kameraschemata bleiben erhalten.
- Updates bestehender Allsky-Installationen außerhalb /home/wurb erhalten den bisherigen Projektordner für die Herstellermigration. Archivupdates werden nach dem Neustart gegen die ausgewählte Archivrevision geprüft; die installierte Release-Version wird zusätzlich zum Git-Stand angezeigt.
- Der Backend-Abgleich erkennt ausführbare Skripte anhand ihrer Shebang. Fehlende Ausführungsrechte werden auch bei identischen Dateien repariert; dies behebt den Softwaremanager-Fehler für WURB, WIRC und Allsky. Vor dem Start prüft Windows die einsatzbereite Softwareverwaltung.
- WURB-/WIRC-Gitupdates, Updatebefehle, Versionsauswahl, Konfigurationsmigration und Rechtekorrektur geprüft. Tatsächliche Hersteller-/Linux-Paketupdates und Kameraaufnahme benötigen weiterhin den Test am jeweiligen Pi.
