# Witty Add-on 0.8.3

Witty Add-on 0.8.3 – 13.10.2026

- Eigene kurze Firmware-Abfrage liest die Witty-Pi-5-Versionsregister beziehungsweise die Witty-Pi-4-Firmwarekennung. Keine GPS-Abfrage und kein Stoppen des Herstellerdienstes erforderlich; Buszugriffe verwenden Sperren und Zeitlimits.
- Windows-Status nutzt die kurze Firmware-Abfrage statt des vollständigen GPS-/Witty-Status. Tatsächliche Firmware wird nicht durch die GitHub-Version ersetzt.
- Sicheres Herunterfahren prüft die Witty-Herstellerdienste und verwendet shutdown -h now mit dem Witty-Pi-5-Abschaltdienst.
- Offline-SD-Wartung zeigt bestätigte Partitionsverkleinerung, ausstehende Ausführung und fehlgeschlagene Wartung getrennt. Witty Pi 5 erhält vor der Wartungsabschaltung die Herstellermeldung.
- Geplante automatische Neustarts werden an das Windows-Programm gemeldet, damit es nach dem Neustart erneut verbinden kann.
- Alle bisherigen Installations-, Paketcache-, GPS-, Trixie- und Backup-Korrekturen enthalten.
- Softwaretests und ext4-Test bestanden; der reale Raspberry-Wartungsboot ist weiterhin auf Hardware zu prüfen.
