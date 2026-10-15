# Witty Add-on 1.0.1

Version 1.0.1 · Build 1

- Internet-Vorprüfung vor Basisinstallation, Linux-, Witty-, Hersteller-, GPS- und Softwareinstallationen/Updates.
- Internet am Windows-PC ODER Raspberry genügt. Sind beide offline, startet keine Installation und kein Update. Hotspot-Verbindung allein gilt nicht als Internetzugang.
- Ist nur Windows online, lädt der Raspberry Pakete und Abhängigkeiten über eine temporäre Downloadverbindung im bestehenden SSH-Kanal. Windows und SSH müssen bis zum Abschluss aktiv bleiben. HTTPS-Prüfung und Paketprüfsummen bleiben erhalten.
- Ist nur der Raspberry online, lädt er auch die vom Windows-Programm benötigten Pakete; die Übertragung zurück erfolgt über SFTP. Bei eigenem Internet lädt der Raspberry seine Abhängigkeiten direkt.
- Temporäre APT-/Proxy-Einstellungen werden nach Erfolg oder Fehler entfernt. Fehler beim Aktualisieren der Paketquellen werden nicht als Erfolg behandelt.
- Vorprüfung umfasst auch den Backend-Abgleich vor Allsky-/WURB-/WIRC-Aktionen. Deinstallation und lokale Dienstaktionen benötigen kein Internet.
- Installer nach Programmneustart und manuellem Neuverbinden vollständig zurücksetzen: Fortschritt, Fehlertext, Zeitmessung und alte Abschluss-/Versionsprüfungen. Keine laufenden Pi-Prozesse oder Paketsperren löschen.
- Flackern des Statusrahmens beim Vergrößern verringern: absolute statt kumulative Größenberechnung, gerundetes Layout und gebündelte Statusanzeige.
