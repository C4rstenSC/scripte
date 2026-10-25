# Raspi-Scripte und Witty Add-on 1.0.11 – technische Änderungen

Stand: 25.10.2026, Build 20261025.1. Windows-Programm und Witty-Add-on werden lokal gebaut und als verschlüsselte Updatepakete bereitgestellt. GitHub Actions wird nicht zum Bauen oder Veröffentlichen verwendet.

## 1. Basisinstallation und Linux-Paketstand

In `installer_addon.sh` findet die Aktualisierung der Paketlisten und der installierten Linux-Pakete jetzt vor den Aufrufen von `raspi-config` und der Einrichtung von Hardware und Anwendungen statt. Der Paketaufruf verwendet `apt-get upgrade --with-new-pkgs --no-install-recommends`; damit können notwendige neue Abhängigkeiten installiert werden. Es wird kein Distributionswechsel angefordert.

Die gemeinsame Installation der ausgewählten Basispakete verwendet nicht mehr `--no-upgrade`. Schon vorhandene, ältere Pakete können somit auf den verfügbaren Stand gebracht werden. Die bestehende Paketfortschrittsanzeige, die Wartezeit auf APT-Sperren und die Überprüfung des Rückgabewerts bleiben wirksam. Paketfehler führen weiterhin dazu, dass nachfolgende Installationsphasen nicht als erfolgreich ausgegeben werden.

Der Vergleich der vorherigen Pakete ergab: Der Basisinstaller selbst war zwischen 1.0.2 und 1.0.10 unverändert. Ein unveränderter Installer garantiert keinen unveränderten Zustand der Linux-Paketquellen. Der neue Ablauf berücksichtigt diesen Unterschied ausdrücklich.

## 2. PHP-Sicherheitsupdates für Allsky

Neu ist `installer/ensure_php_security.py`, installiert als `/usr/local/sbin/witty-ensure-php-security`. Die Routine prüft installierte, versionierte PHP-Laufzeitpakete wie `php8.4-fpm`, `php8.4-cgi`, `php8.4-cli` und `php8.4-common`. Eine reine Prüfung des Metapakets `php-fpm` genügt dafür nicht.

Für die Sicherheitskorrekturen vom 21.10.2026 werden die PHP-Zweige 8.2, 8.3, 8.4 und 8.5 gegen die korrigierten Upstreamstände 8.2.35, 8.3.36, 8.4.27 und 8.5.12 geprüft. Veraltete installierte Laufzeitpakete und ihre bereits installierten Erweiterungen werden über die konfigurierten APT-Paketquellen aktualisiert. Anschließend werden die Paketstände erneut gelesen und betroffene PHP-FPM-Dienste sowie ein laufender Lighttpd neu gestartet.

Die Prüfung ist in die Basisinstallation, Allsky-Installation beziehungsweise -Neuinstallation und das Add-on-Update bei vorhandenem Allsky eingebunden. Die Trixie-Vorbereitung ruft sie nach Einrichtung der PHP-Pakete auf. Sicherheitsprüfungen werden nicht abgeschaltet. Falls die benötigten Korrekturen in den eingetragenen Paketquellen fehlen, kann das Programm keinen korrigierten Paketstand behaupten.

Referenzen: [PHP Foundation, 21.10.2026](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/), [Debian CVE-2026-109618](https://security-tracker.debian.org/tracker/CVE-2026-109618), [Debian CVE-2026-109619](https://security-tracker.debian.org/tracker/CVE-2026-109619).

## 3. Direkte Allsky-Installation von GitHub

`prepare_allsky_source.py` wiederholt einen fehlgeschlagenen oder zeitlich abgebrochenen Git-Klon bis zu dreimal. Jeder Klonversuch hat ein Zeitlimit von 15 Minuten. Unvollständige temporäre Klone werden vor dem nächsten Versuch entfernt; das eigentliche Zielverzeichnis wird dabei nicht gelöscht.

Die Prüfung eines bestehenden Allsky-Repositorys verwendet jetzt wie der archivierte Installationsweg einen ausdrücklich auf dieses Verzeichnis begrenzten `safe.directory`-Eintrag. Dadurch kann die mit Root-Rechten laufende Vorbereitung ein Repository des Benutzers `wurb` prüfen, ohne an Git-Eigentümerprüfungen zu scheitern.

Die Auswahl „Aktuell von GitHub“ lädt weiterhin den aktuellen Standardbranch des Herstellerprojekts einschließlich Untermodulen. Der konkrete Commit wird gespeichert. Ein vorhandenes Verzeichnis mit anderem Commit wird weiterhin nicht stillschweigend überschrieben; reguläre Allsky-Updates verwenden den vorhandenen Sicherungs- und Wiederherstellungsablauf.

## 4. Witty Pi 5: vollständige Skriptliste und Lesen des aktiven Skripts

In `backend/witty_backend.sh` werden Dateilisten über eine eigene `schedule_menu_output`-Routine abgefragt. Sie verwendet bis zu 45 Sekunden pro Herstelleraufruf und bis zu drei Versuche. Ein Timeout mit nur teilweise ausgegebener Liste zählt nicht als erfolgreiche Antwort. Der Herstellerdienst wird für die jeweilige Transaktion angehalten und anschließend wieder freigegeben.

Aktivierungs- und Downloadliste werden zusammengeführt, da die Aktivierungsliste ein aktives Skript ausblenden kann. Die Dateinamen werden mit den lokalen WPI-Dateien vereinigt. Ein fehlgeschlagener Geräteaufruf wird nicht mehr als erfolgreiche, scheinbar vollständige Liste aus nur einer lokalen Datei behandelt.

Die Zuordnung eines bereits aktiven Skripts nach Neuinstallation liest die Originaldateien mit längeren Downloadfristen und vergleicht ihre Inhalte. Ein Name wird weiterhin nur bei einer eindeutigen Übereinstimmung übernommen. Beim Lesen wird kein anderer Zeitplan aktiviert. Unvorhergesehene Shellabbrüche liefern zusätzlich die betroffene Backendzeile statt ausschließlich „Code 1“.

## 5. SD-Karte auf Raspberry Pi 5 schrumpfen

Der eigenständige Wartungshelfer und der Add-on-Helfer werden aus denselben Quelldateien erzeugt. Die Korrektur erreicht deshalb auch die Schrumpffunktion des Windows-Programms ohne installierte Homepage.

Vor dem Wartungsstart ermittelt `witty-device-options` die laufende Kernelversion und eine dazu passende Kerneldatei. Der Wartungsstart erhält eine eigene Kopie dieser Kerneldatei und das genau für diese Version erzeugte Initramfs. In der nur für den Wartungsstart verwendeten Bootkonfiguration werden beide Dateien ausdrücklich ausgewählt. Das verhindert die Kombination eines alten Wartungs-Initramfs mit einer durch ein Linux-Update bereits ersetzten `kernel_2712.img`.

Falls ein Kernelupdate die Dateien oder Module des noch laufenden Kernels schon entfernt hat, merkt der Helfer die SD-Kartenidentität vor und richtet einen einmaligen Fortsetzungsdienst ein. Nach einem automatischen Neustart wird derselbe Schrumpfauftrag ohne erneuten Windows-Klick fortgesetzt. Die Fortsetzung prüft Root- und Boot-UUID und ist gegen eine endlose Neustartschleife begrenzt. Bereits im Wartungsordner liegende Hilfsdateien werden wiederverwendet; dadurch entsteht bei der Fortsetzung beziehungsweise einer späteren Erweiterung kein Kopierfehler durch identische Quell- und Zieldateien.

Die eigentliche Verkleinerung findet weiterhin vor dem Einhängen der Rootpartition statt: Dateisystemprüfung, `resize2fs -M`, Reduktion der Partitionsgrenze mit 512 MiB Reserve, erneute Größenprüfung und abschließende Dateisystemprüfung. Ein Erfolg wird erst nach Prüfung der wirklichen Geometrie gespeichert. Der anschließende Witty-Hersteller-Abschaltweg und die automatische Erweiterung beim nächsten normalen Start bleiben erhalten. Der Abschlussstart darf die Karte noch nicht wieder erweitern.

Windows erstellt das kleine IMG anhand der tatsächlichen Partitionsgrenzen und der ext4-Größe. Der Test umfasst jetzt ausdrücklich auch eine SD-Karte mit 32 Milliarden Bytes Kapazität. Eine weiterhin volle oder widersprüchliche Partition wird nicht durch bloßes Setzen eines Erfolgsmarkers als geschrumpft ausgegeben.

## 6. Vorherige Änderungen bleiben im neuen Paket enthalten

Der neue Windows-Quellstand wurde mit dem tatsächlich veröffentlichten 1.0.9-Programm abgeglichen. Die unabhängige Aktualisierung verwendeter und sichtbarer Satelliten, das Verfallen veralteter GPS-Werte, die Möglichkeit zum Fortfahren ohne Zeitabgleich und die gemeinsame GitHub-Versions-/Buildabfrage sind übernommen.

Das Witty-Paket enthält weiterhin den vollständigen Stand 1.0.10 mit gemeinsamer UTC-Sonnenberechnung für Aufnahmeprogramme und PHP-Anzeige. Der gewählte feste UTC-Offset beziehungsweise die ausdrücklich gewählte Zeitzone bleibt die Zeitbasis. Reale Koordinaten und der eingestellte Sonnenwinkel steuern den Tag-/Nachtmodus. Die Mittag-bis-Mittag-Zuordnung neuer Bilderordner und die GPS-Korrekturen bleiben enthalten.

## 7. Prüfung und Grenzen

Die Freigabe umfasst automatisierte Python-/Shelltests für Paketlogik, PHP-Versionsprüfung, vollständige Skriptlisten, Kernelzuordnung, einmalige Fortsetzung und bestehende Allsky-/GPS-/Abschaltfunktionen. Zusätzlich werden die Windows-SD- und Uhrzeitprüfungen ausgeführt, das Windows-Programm und der Updater lokal für win-x64 gebaut und die erzeugten Archive nach dem Verschlüsseln erneut entschlüsselt und auf Inhalt sowie Prüfsummen geprüft.

Die Prüfung erfolgt in der Buildumgebung. Es besteht kein direkter Zugriff auf die betroffene 32-GB-SD-Karte, den Raspberry Pi oder dessen Witty-Platine. Der konkrete bisherige Fehler auf dieser Hardware ist deshalb nicht durch ein Geräteprotokoll bewiesen; die genannten Korrekturen und Tests ersetzen keinen vollständigen Gerätetest.
