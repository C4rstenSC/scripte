# Witty Add-on 0.9.7.1

Version 0.9.7.1 · Build 3
Änderungen gegenüber 0.9.7.1 Build 2

Erweiterte Startdiagnose
- Der Beobachter startet im frühen normalen Systemstart nach Root-Remount und Journald, ohne auf die FAT-Bootpartition zu warten oder Herstellerdienste aufzuhalten. Er bleibt auch nach stabiler Bereitschaft aktiv und dokumentiert den nächsten Neustart beziehungsweise Abbruch.
- Journal, sekündliche Lebenszeichen und Stoppsignale werden kontinuierlich aufgezeichnet. Dienst-/HTTP-Statusabfragen laufen getrennt und blockieren die Logaufzeichnung nicht.
- Jeder Boot erhält ein dauerhaftes Linux-Protokoll. diagnose.txt wird auf die Bootpartition gespiegelt; bei fehlendem oder schreibgeschütztem FAT bleibt die Linux-Sicherung aktiv. Frühere Bootversuche werden beim nächsten verfügbaren FAT-Zugriff wiederhergestellt.
- Zustandsaufnahmen enthalten alle Systemdienste mit Start-/Endzeiten und Rückgabestatus, laufende Prozesse, Startaufträge, Einhängungen, SD-Kartenkennungen, Spannungs-/Drosselungszustand und verfügbare PMIC-/Bootloaderwerte. Gespeicherte Kernel-Crashprotokolle werden übernommen, falls vorhanden.
- Der Bootsektor und die FAT-Clean-/Fehlerkennzeichen werden ausschließlich lesend erfasst. Die Diagnose repariert und mountet keine Karte. D-Bus-Abschalt-/Neustartanforderungen sowie verfügbare PID-/Dienstinformationen der Aufrufer werden protokolliert.
- Das Systemjournal bleibt größenbegrenzt dauerhaft gespeichert und wird schneller synchronisiert. Linux-/FAT-Protokolle werden begrenzt rotiert. Unbekannte oder nicht verfügbare Sensoren werden nicht als Messwerte erfunden.

Windows und Allsky
- Die normale Allsky-Installation über install erhält jetzt denselben Neustart-Kontext wie reinstall. Der empfangene Neustartmarker kann damit die hostbezogene Meldung auslösen.
- Beide eigenen Offline-Allsky-Versionen zeigen keine technischen Entschlüsselungs-, Klon-, Branch- oder Checkout-Hinweise mehr. Die sichtbaren Installationsschritte und echte Fehler bleiben erhalten; Archiv-/Git-Prüfungen laufen weiterhin.

- Die ältere eigene Allsky-Archiv-Auswahl heißt jetzt 25.07.2025. Archiv, Quellkennung und Prüfsumme bleiben unverändert.

- Windows unterscheidet Softwareinstallation, Softwareupdate und Softwaredeinstallation in der Fortschrittsanzeige. Backend-Abgleich zeigt die laufenden Ausgaben, Paketübertragung, Dateiübernahme und Steuerbefehlsprüfung statt einer unveränderten Sammelmeldung. Ein erfolgreicher Vorgang beendet die unbestimmte Fortschrittsanzeige.
- Während eines Bestätigungsdialogs werden Terminal-Eingabe und automatisches Zurückholen des Fokus unterbrochen; verschachtelte Dialoge geben den Terminal-Fokus erst nach dem letzten Schließen frei.

Prüfgrenzen
- Prozesstest prüft weiterlaufende Journalaufzeichnung bei blockierter Statusprüfung, Root-/FAT-Sicherung und SIGTERM-Abschluss. Tests prüfen FAT-Ausfall, Wiederherstellung früherer Boots und ausschließlich lesende Bootsektoraufnahme.
- Die tatsächliche Ursache des reproduzierbaren Bootabbruchs ist noch nicht bewiesen. Die erweiterten Protokolle sollen Strom-/Dateisystemfehler von ausgelösten Neustarts oder Abschaltungen unterscheiden. Ein vollständiger Stromverlust vor Linux-Start kann nicht durch einen Linux-Dienst aufgezeichnet werden.
