# Raspi-Scripte 0.7.0

Windows und Witty Add-on: **0.7.0**, korrigierter Stand 09.10.2026, Build-Revision 20261009.4.

**Vorhandene Windows-Versionen aktualisieren sich über den bisherigen Update-Knopf auf 0.7.0.** Der alte Updatepfad und der kleine modulare Updatepfad liefern passende verschlüsselte Pakete mit SHA-256-Manifesten. Ein manueller ZIP-Umstieg ist nicht erforderlich. Das Kompatibilitätsupdate enthält die Windows-Laufzeit; anschließend verwendet das Programm den kleinen modularen Updatekanal.

Der Basisinstaller bietet drei Allsky-Quellen: v2024.12.06_06 und v2026.10.01 als vollständige verschlüsselte Originalarchive aus diesem Repository, oder die aktuelle Version direkt vom Allsky-GitHub. Kamera-/Trixie-/Navigationsanpassungen gelten für alle Quellen. Die gewählte Quelle bleibt bei Softwareupdates erhalten. Die beiden Archive enthalten auch Sunwait und Zusatzmodule und benötigen das Hersteller-GitHub für die Allsky-Quellen nicht. Betriebssystem- und Python-Paketquellen bleiben erforderlich.

Bei abgezogenem USB-GPS erhält WURB einen ungültigen Fix, verwirft die zwischengespeicherten GPS-Koordinaten und löst seine vorhandene Positionsumschaltung aus. Die gespeicherte manuelle Position bleibt erhalten. Wiederanstecken liefert Position und echte Satellitenzahl. WURBs Einstellungen zur Ersatzposition bleiben bestehen.

Allsky-Backups lassen sich ausschließlich auf dieselbe Version und denselben Git-Stand zurückspielen. Fehlermeldungen zeigen die Backup-Version und die installierte Version. Das gilt im Windows-Programm, auf der Witty-Webpage und für automatische Wiederherstellung. Alte Backups ohne Versionsangabe werden vor Änderungen abgewiesen.

Micro SD Karten Optionen: Ampel für Partitionsstatus, Ja/Nein vor Schrumpfen/Expandieren. Schrumpfen erfolgt über einen einmaligen Offline-Wartungsstart und anschließendes Herunterfahren; Expandieren nutzt die Basisinstaller-Methode mit Neustart. Nur Standard-Micro-SD (FAT-Boot + letzte ext4-Root-Partition) wird verändert. Einstellungen anpassen ändert Hostname und bestehende Hotspot-SSID nach der Installationsregel. Aktiver GPS-Empfänger wird hellgrün angezeigt. GPS-Synchronisation verwendet fortschreitende Live-Daten; Uhren werden danach frisch gelesen.

Release Notes und Bedienungsanleitungen im Programm sind aktualisiert. Lokale Build-, GPS-Verbindungs-, Paket- und Sicherungsprüfungen bestanden; native Windows-/Raspberry-Hardwaretests stehen aus.
