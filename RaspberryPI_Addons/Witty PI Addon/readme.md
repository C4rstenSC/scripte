# Witty Add-on 1.0.6

Version 1.0.6 · Build 2
Änderungen gegenüber 1.0.6 Build 1

GPS auf Raspberry Pi 4 mit USB-GPS und WURB
- Echte Empfängerzeit statt Raspberry-Systemzeit anzeigen. Ein fehlender GPS-Zeitstempel bleibt „Nicht verfügbar“ und darf keinen GPS-Zeitabgleich auslösen.
- Zeit, Position und verwendete Satelliten über eine zusätzliche Status-Abfrage aus WURBs vorhandenem GPS-Leser auslesen. USB-Port, Geräteauswahl, gpsd-Konfiguration und bestehende serielle Verarbeitung bleiben unverändert.
- Der vorhandene GPS-Boot-Zeitabgleich startet den WURB-Dienst im Hintergrund und aktiviert dessen GPS-Leser ohne Browser. Nach gültigem Fix werden Linux und Witty-RTC über den bestehenden Ablauf synchronisiert. Die Allsky-Ausnahme bleibt erhalten.
- Mehrfache Status-Abfragen und spätere Browseraufrufe verwenden denselben GPS-Leser. Veraltete Zeit-/Positionsdaten werden verworfen; das Alter aktueller GPS-Messwerte wird berücksichtigt.
