# Raspi-Scripte 1.0.3

Version 1.0.3 · Build 1
Änderungen gegenüber 1.0.2

Zeitprüfung im Windows-Programm
- Vor Installation und Updates werden Linux-Systemzeit und die vorhandene Witty-RTC geprüft. Bei einer Abweichung fragt das Programm ausdrücklich nach, ob die angezeigte Windows-PC-Zeit übernommen werden soll.
- Nach Zustimmung wird Linux gesetzt und die vorhandene Witty-RTC über den Herstellerpfad synchronisiert und zurückgelesen. Ohne Zustimmung oder bei fehlgeschlagener Prüfung wird der Vorgang abgebrochen. GPS wird dafür nicht verwendet.

Firmware-Download
- Neben einer verfügbaren neuen Witty-Pi-5-Firmware erscheint ein Downloadbutton mit Speicherdialog für den Windows-PC. Die Original-UF2-Datei für HAT+ wird über die Internetverbindung des PCs vom Hersteller geladen.
- Dateigröße, UF2-Struktur und vorhandene Hersteller-Prüfsumme werden vor dem Speichern geprüft. Eine vorhandene Zieldatei wird erst nach erfolgreicher Prüfung ersetzt. Die Mini-Firmware wird nicht als HAT+-Firmware angeboten.

Homepage-Datumsanzeige
- Zeitplantermine und laufende Uhren verwenden explizite numerische Datumsfelder. Unvollständige oder ungültige Termine werden nicht mit vom Browser ergänzten Monats- oder Jahreswerten angezeigt. Die Geräte-Zeitzone bleibt maßgeblich.
- Der Datumsparser wird mit einer Versionskennung geladen; Datumsfelder sind von automatischer Browser-Übersetzung ausgenommen. Gültige vom Gerät gemeldete Jahreszahlen werden unverändert angezeigt.
- Pi-RTC-Deaktivierung, Allsky-Zeitabgleich aus der Witty-RTC und USB-Mount-Nachrüstung aus 1.0.2 bleiben enthalten.
