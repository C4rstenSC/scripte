# Witty Add-on 1.0.1

Version 1.0.1 · Build 5

- Gemeinsame USB-Mount-Einrichtung für WURB und alle angebotenen Allsky-Versionen. Basis + Allsky ohne WURB installiert ebenfalls pmount und die Mount-Regeln; kein zusätzliches WURB-Repository für Mount-Dateien nötig.
- USB-Datenträger erscheinen nach WURB-Konvention unter /media/USB-<Gerät>, zum Beispiel /media/USB-sda1. Hotplug, Neustart und bereits eingesteckte Sticks werden berücksichtigt.
- Ein Witty-Add-on-Update rüstet die USB-Einrichtung auch bei unveränderter vorhandener Allsky-/WURB-Installation nach. Bereits eingehängte Datenträger bleiben unverändert; interne Datenträger und Partitionen ohne unterstütztes Dateisystem werden nicht eingebunden.
- Allsky-Nachinstallation, Versionswechsel, Neuinstallation und Erststart nach automatischem Installer-Neustart verwenden denselben Mount-Weg.
- Witty-Pi-5-Herstellerinstallation und Herstellerupdate sichern zuvor Linux-Zeit und Zeitzone. Eine durch die Installation verschobene Uhr wird mit der gesicherten Ausgangszeit plus verstrichener Laufzeit wiederhergestellt; danach wird System → Witty-RTC synchronisiert und geprüft.
- Keine pauschale Stundenkorrektur und keine neue periodische Zeitsynchronisation. Ausgangspunkt ist die vor der Herstellerinstallation vorhandene Linux-Zeit.
