# Raspi-Scripte 0.7.1 – Bedienungsanleitung (09.10.2026)

## Windows-Programm aktualisieren
Im Programm den Update-Knopf verwenden. Das kleine Programmupdate enthält EXE-Starter, DLLs, Updater, Anleitungen und das aktuelle Witty-Paket. Beim Aktualisieren das Programm und den Raspberry eingeschaltet lassen; der separate Updater startet das Programm anschließend neu. Verbindungsprofile und vorhandene Aktivierung bleiben erhalten.

Das Programm verwendet modular-update-manifest.json. Programmdateien kommen aus Raspi-Scripte-Programm.zip.enc; reine Inhalte aus Raspi-Scripte-Modular-Content.zip.enc. Download, Entschlüsselung, ZIP-Prüfung und SHA-256-Abgleich erfolgen automatisch ohne Paketpasswort. Ein Programmupdate ist bei geändertem Programmcode erforderlich; ein reines Inhaltsupdate ersetzt keine DLL.

Ältere Einzel-EXE-Installationen müssen einmalig auf das kleine Paket umgestellt werden: ZIP vollständig in einen beschreibbaren Ordner entpacken, START.cmd starten und vorhandene Profile weiterverwenden. START.cmd installiert bei Bedarf die .NET-8-Desktop-Laufzeit. Danach sind normale kleine Programmupdates möglich.

## Witty Add-on aktualisieren
Zuerst verbinden. Die Witty-Add-on-Zeile zeigt den installierten Stand und den verfügbaren GitHub-Stand. Witty über den zugehörigen Update-Knopf aktualisieren; alternativ die Update-Funktion der Witty-Homepage verwenden. Das veröffentlichte Paket ist witty_addon.zip.enc, Version 0.7.0. Die Updates enthalten sämtliche Änderungen bis 0.6.62 und ersetzen keine WURB-, WIRC- oder Allsky-Neuinstallation.

## Basisinstallation und Allsky-Version
Auf dem neuen Raspberry über Windows verbinden und Basis Installation öffnen. Erkanntes Raspberry-Modell, Witty-Modell, Land, Zeitzone, Tastatur, GPS und Anwendungen prüfen. Deutschland verwendet Europe/Berlin; Australien schlägt Australia/Sydney vor. Für andere australische Zeitzonen die Zeitzone entsprechend ändern.

Unter Allsky installieren erscheint die Auswahl Aktuelle Version – 01.10.2026 (v2026.10.01) oder Vorherige Version – 06.12.2024 (Revision 06, v2024.12.06_06). Die Auswahl wird nur bei aktivierter Allsky-Installation bedienbar. Beide Versionen kommen als verschlüsselte Originalarchive vom eigenen GitHub. Die aktuelle Version besteht wegen der Dateigrößenbegrenzung aus mehreren Teilen; Zusammensetzen und Entschlüsseln erfolgen automatisch.

Die Archive werden anhand ihrer Prüfsummen und des Original-Git-Commits geprüft. Anschließend startet der offizielle Allsky-Installer als letzte Installationsphase. Internetzugang für zusätzliche Pakete und eine von Allsky unterstützte, angeschlossene Kamera bleiben erforderlich. Diese Versionsauswahl gilt für den Basisinstaller; die separate Allsky-Softwareverwaltung bleibt bestehen.

Ein vorhandener abweichender Allsky-Stand wird nicht überschrieben. Vor einem Versionswechsel Konfiguration sichern, Allsky über die Softwareverwaltung deinstallieren und den gewünschten Stand bei der Basisinstallation wählen. Ist der Basisinstaller auf dem eingerichteten System deaktiviert, ist dieser Weg erst bei einer Neuinstallation verfügbar. Sicherungen zwischen verschiedenen Allsky-Versionen nicht als garantiert kompatibel betrachten.

## GPS auf Raspberry Pi 4 und 5
USB-Maus, Waveshare L76X oder Kein GPS im Programm auswählen. Die USB-Erkennung wird auch ohne angeschlossenen Empfänger vorbereitet. Auf Pi 4 liest WURB die USB-Maus direkt; auf Pi 5 verteilt gpsd die Daten über die NMEA-Bridge. Waveshare verwendet seinen eigenen Hardwarepfad. Keine zusätzlichen USB-Treiber sind für diese Änderungen vorgesehen.

Die Pi-5-Bridge leitet vollständige NMEA-Sätze mit ursprünglicher Satellitenzahl, HDOP und Fixqualität weiter. gpsd arbeitet für USB im Nur-Lese-Modus. Nach einem gpsd-Neustart verbindet sich die Bridge erneut. Die Homepage unterscheidet keine Empfängerdaten, empfangene Daten ohne Positionsfix und gültigen Fix. Sichtbare Satelliten bedeuten noch keinen gültigen Positionsfix.

Fehlen Koordinaten, Satelliten oder Zeit, die GPS-Diagnose verwenden und Ausgabe im Terminal prüfen. Ein fehlender Datenstrom auf Papas Raspberry wurde durch Simulationen noch nicht abschließend als behoben nachgewiesen. Die aktuelle Version enthält die Korrekturen, ersetzt aber keine Prüfung am angeschlossenen Empfänger.

## Zeit und RTC
GPS-Synchronisierung nur mit gültiger GPS-Zeit beziehungsweise Fix verwenden. Bei vorhandener aktiver Pi-5-RTC wird diese in den Abgleich einbezogen; ohne aktive interne RTC bleiben Systemzeit und Witty-RTC maßgeblich. Manuelles Setzen der Systemzeit und vollständiger GPS-Abgleich sind unterschiedliche Aktionen. Gegebenenfalls benötigtes hwclock wird durch die Paketvorbereitung bereitgestellt; APT-/dpkg-Fehler erscheinen mit Ursache im Terminal.

## Herstelleranzeige und Bedienung
Witty Add-on und Witty-Herstellersoftware sind getrennte Statuszeilen. Installierte Witty-Pi-4-Software wird als Witty Pi 4 angezeigt, auch bei unbekannter Versionsnummer. WP5 wird auch außerhalb von PATH erkannt. Eine unbekannte Version bedeutet nicht, dass die Software fehlt. Die installierte Software und das Hardwaremodell werden getrennt erkannt.

Das Statusfeld und die Installationsknöpfe werden bei bestehender Verbindung angezeigt. Die GPS-Ampel steht links neben der GPS-Zeile; Variantenwahl und Deinstallation sind rechts angeordnet. Das SSH-Terminal lässt sich über den Knopf neben der Überschrift ein- und ausblenden.

## Sicherung und Wiederherstellung
Vor Neuinstallationen die Sicherungsfunktion für die betroffene Anwendung verwenden. Allsky-Sicherungen enthalten Einstellungen, Overlaylayouts, Modul- und Websitekonfigurationen sowie Speicherpfadangaben. Aufnahmen, Darkframes und Programmdateien sind kein Bestandteil dieser Konfigurationssicherung. Nach Wiederherstellung Overlayeditor, Speicherpfad und Dienst prüfen.

## Release Notes und Diagnose
Die Hilfe enthält deutsche Release Notes für Windows und Witty, einschließlich der GPS-Korrekturen und der Allsky-Versionsauswahl. Die Witty-Historie wird als eigene Versionsliste geladen und ist auch aus dem mitgelieferten Inhaltspaket verfügbar. Hinweise von WURB, WIRC, Allsky und Witty-Herstellersoftware bleiben getrennt. Neue, noch nicht übersetzte Herstellerversionen werden mit Quellenhinweis angezeigt.

Entschlüsselung, ZIP-Prüfung, beide Allsky-Originalstände und Windows-x64-Kompilierung wurden geprüft. Ein nativer Windows-Starttest und Tests auf Raspberry-Pi-Hardware stehen aus; neue Hauptprogrammdateien sind unsigniert.

## Verbindliche Versionsprüfung bei Allsky-Backups
Neue Sicherungen speichern die Allsky-Version und den Original-Git-Stand. Wiederherstellung ist nur auf exakt denselben Softwarestand möglich. Bei Abweichung werden beide Versionen beziehungsweise Git-Stände angezeigt und vor Dateiänderungen oder Dienststopps abgebrochen. Alte Backups ohne Versionsangabe werden als Version unbekannt abgelehnt. Das gilt in Windows, auf der Witty-Webseite und für automatische Wiederherstellungen nach Updates. Nach einem Allsky-Versionswechsel eine neue Sicherung erstellen; ein Backup der vorherigen Version kann erst auf deren gleichem Stand wiederhergestellt werden.

Standalone-Allsky: Sunwait und die Zusatzmodule sind ebenfalls als verschlüsseltes Zusatzpaket im eigenen Repository enthalten. Der Installer verwendet lokale Git-Quellen; Raspberry-Pi-OS- und Python-Paketquellen bleiben erforderlich.

Die dritte Allsky-Quelle „Aktuelle Version direkt vom Allsky-GitHub“ lädt den beim Installieren aktuellen Standardzweig einschließlich Sunwait. Sie benötigt das Hersteller-GitHub; die zwei verschlüsselten Archive bleiben davon unabhängig. Alle Quellen durchlaufen dieselben Kamera-, Trixie-, Navigations- und Erststart-Anpassungen. Die Softwareverwaltung behält die gewählte Quelle bei.

GPS auf Pi 5: Beim Abziehen oder Verlust des Fixes schaltet WURB auf die unter „Default position“ gespeicherte manuelle Position zurück. Bei erneutem gültigem Fix übernimmt WURB automatisch GPS und die echte Satellitenzahl. Die manuelle Position bleibt gespeichert.

## Micro SD Karten Optionen und Hostname

Der rot umrahmte Bereich befindet sich unter den beiden Installations-/Updatebuttons. Die Ampel zeigt Grün für expandierte und Rot für geschrumpfte Partitionen; Grau bedeutet unbekannt oder nicht unterstützte Aufteilung. Der Text erklärt den Status. Die Buttons stehen in Flucht mit den Status-Aktionsbuttons.

„Partitionen schrumpfen“ fragt Ja/Nein. Ja bereitet ein geprüftes RAM-Wartungsimage vor und startet den Pi einmal in diesen Wartungsmodus. Der Neustart beendet Witty Add-on, GPS, Herstellersoftware, WURB, WIRC und Allsky. Das nicht eingehängte ext4-Dateisystem wird zuerst verkleinert, anschließend die Root-Partition; 512 MiB freier Platz bleiben erhalten. Danach fährt der Pi herunter. Währenddessen nicht stromlos machen. Protokoll und ursprüngliche Partitionstabelle liegen auf der Bootpartition (`witty-sd-result.txt`, `witty-sd-partitions.before`). Normale Bootkonfiguration wird vor Änderungen wiederhergestellt. Nur Standard-Micro-SD mit genau FAT-Boot und letzter ext4-Root-Partition wird unterstützt; USB/NVMe/LVM/verschlüsselte Root-Systeme werden abgewiesen. `initramfs-tools`, `e2fsprogs`, `util-linux` und `fdisk` müssen vorhanden sein; fehlende Werkzeuge führen zu einer Fehlermeldung vor Änderungen. Eine aktuelle Sicherung sollte vorhanden sein.

„Partitionen expandieren“ fragt Ja/Nein, erweitert per `raspi-config` wie der Basisinstaller und startet den Pi neu. Nach dem erneuten Verbinden zeigt die Ampel den tatsächlichen Zustand.

„Einstellungen anpassen“ zeigt den aktuellen Hostnamen neben dem Eingabefeld. „Änderungen übernehmen“ setzt Hostname und bestehende verwaltete Hotspots: WURB `wifi4bats-<Hostname>`, Allsky `allskywifi-<Hostname>`, sonst `wifi-<Hostname>`. WLAN-Passwort und übrige Netzwerkdaten bleiben erhalten. Ein aktiver Hotspot übernimmt den Namen verzögert; WLAN/SSH können kurz abbrechen. „Abbruch“ verändert nichts.

Im GPS-Bereich ist der tatsächlich aktive Empfänger hellgrün hinterlegt, unabhängig von der Auswahl für eine künftige Installation.


GPS-Abgleich korrigiert: Beide GPS-Buttons synchronisieren Linux, Witty-RTC und eine aktive Pi-RTC über denselben geprüften Ablauf. Die Witty-Uhr wird beim tatsächlichen Auslesen zeitlich erfasst; kein pauschaler Sekundenoffset.


## Änderungen in 0.7.1
Bei Allsky stehen zwei verschlüsselte Archive (Carsten Github) und die aktuelle Version (Github ALLSKY) zur Auswahl. Diese Auswahl erscheint sowohl im Basisinstaller als auch unter „Raspberry Scripte → Allsky → Software installieren“. Die Archive enthalten die vollständigen Allsky-Quellen; Betriebssystempakete benötigen weiterhin Internetzugang.
Die Allsky-Paketphase läuft ohne Debian-Rückfragen. Allsky-eigene Kamera- und Konfigurationsdialoge bleiben im SSH-Terminal bedienbar.
Software wird ausschließlich über Windows installiert und deinstalliert. Die Witty-Webseite zeigt nur installierte Dienste und bietet deren Start-/Stopp-Schaltflächen.

### Global-Shutter-Kamera (IMX296)
GS-Kamera vor der Installation anschließen und „GS-Kamera (IMX296): maximal 15 Sekunden Belichtung“ auswählen. Der Haken steht sowohl im Basisinstaller als auch im einzelnen Allsky-Installationsdialog zur Verfügung. Alle drei Allsky-Versionen erhalten das benötigte IMX296-Kameraprofil; eine Ersatzkamera für die Installation ist nicht erforderlich.
Bei gewähltem Haken werden Tag-/Nacht-Autobelichtung sowie manuelle Startwerte auf höchstens 15.000 ms (= 15 Sekunden) begrenzt; kürzere Werte bleiben erhalten. Allsky verwendet seine eigene automatische Belichtungsregelung innerhalb dieser Grenzen.
Auf „Allsky - Setup“ lässt sich die gleiche GS-Einstellung für die bereits ausgewählte GS-Kamera übernehmen. Die Seite zeigt die tatsächlichen maximalen Tag-/Nachtwerte in Sekunden. Allsky wird bei laufendem Dienst kurz angehalten und mit den neuen Werten gestartet. Ausschalten behält die aktuellen Belichtungswerte bei. Manuelle Änderungen in Allsky werden nicht im Hintergrund zurückgesetzt und bleiben beim Allsky-Update erhalten.

### Belichtungszeiten auf Allsky - Setup
Die vier Felder zeigen die tatsächlichen Allsky-Werte für manuelle/Startbelichtung und maximale Autobelichtung, jeweils für Tag und Nacht. Alle Eingaben sind in Sekunden. Separate Haken schalten die automatische Belichtung für Tag und Nacht ein oder aus. „Belichtungszeiten übernehmen“ speichert die Werte in Allsky, liest sie zur Bestätigung zurück und startet einen vorher laufenden Dienst mit diesen Werten neu. Ein gestoppter Dienst bleibt gestoppt. Bei Startfehlern werden die vorherigen Werte wiederhergestellt.
Bei einer GS-Kamera erscheint der rote Hinweis „Maximal 15 Sekunden Belichtungszeit empfohlen“, auch auf der Allsky-Homepage. Die GS-Voreinstellung begrenzt beide Automatikwerte auf 15 Sekunden. Der standort-/sonnenwinkelabhängige Wechsel zwischen Tag und Nacht und Allskys Helligkeitsregelung verwenden diese Grenzen. Spätere bewusste Änderungen sind möglich, soweit das Kameraprofil sie erlaubt.
Alle vier Belichtungswerte, die Automatik-Auswahl und die GS-Kennzeichnung werden gemeinsam mit settings.json/options.json gesichert und über Website oder Windows wiederhergestellt. Auch die Update-Wiederherstellung erhält sie. Backups können weiterhin ausschließlich auf denselben Allsky-Softwarestand zurückgespielt werden.

## Paketinstallation / Package installation

Grundinstallation: ursprünglicher direkter APT-/Konsolendialog-Ablauf wiederhergestellt; keine globale erzwungene nichtinteraktive Paketkonfiguration und kein Prozessgruppenwechsel über timeout in der Basis-Paketphase. Paketfehler bleiben Abbruchgründe. Alle 20 Sekunden sichtbarer Prozessstatus statt einer stillstehenden Anzeige. Allsky-/Trixie-/GS-Anpassungen bleiben erhalten. Ursache auf Papas Pi ohne Prozessdaten noch nicht bestätigt.

Micro-SD-Status prüft Partition und ext4-Dateisystem getrennt. Grün erscheint nur, wenn beide den vorhandenen Platz nutzen. Linux-Update auf einem frischen Image läuft direkt im SSH-Terminal, ohne vorher Witty zu installieren.

Verbindung zum Raspberry Pi wird alle 5 Sekunden per SSH geprüft. Bei Ausfall wird die Anzeige rot; eine einmalige Warnung muss mit OK bestätigt werden, danach wird getrennt. Über dem SSH-Terminal zeigt die Basisinstallation den aktuellen Schritt, konfigurierte Gesamtanzahl und den Paketdownload einschließlich Abhängigkeiten. Prozentwerte beziehen sich auf abgeschlossene Schritte, nicht auf die verbleibende Zeit.
