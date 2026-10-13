# Witty Add-on 0.9.0

Witty Add-on 0.9.0 | 13.10.2026
Änderungen gegenüber 0.8.9

Schrumpfen und nächster Start
- Neue Schrumpfaufträge merken die automatische Erweiterung beim nächsten normalen Pi-Start vor. Vor der Abbildsicherung nicht erneut im Pi starten: Die ausgeschaltete Karte bleibt verkleinert, der nächste normale Start erweitert sie wieder.
- Der Wartungs-/Abschaltstart führt diese Erweiterung nicht aus. Nur ein bestätigtes Schrumpfergebnis mit passenden Root-/Boot-UUIDs wird verarbeitet. Erst nach erfolgreicher Dateisystemprüfung wird die Vormerkung gelöscht.
- Bestehende ältere Schrumpfaufträge werden nicht nachträglich verändert. Die Hersteller-Abschaltung und die normale Bootwiederherstellung aus 0.8.9 bleiben erhalten.

Witty nachinstallieren
- Der Hersteller-Manager wird bei Updates auch als ausführbarer globaler Befehl installiert. Der Steuerbefehl kann die vorhandene Backend-Kopie nutzen. Dies behebt „Hersteller-Manager fehlt“ beim Windows-Installationsbutton.
- Hardwareerkennung, getrennte Hersteller-/Homepage-Installation und die vorhandenen GPS-Einstellungen bleiben erhalten.

Paketinstallation
- WURB/WIRC verwenden eine temporäre Laufzeitliste ohne black und pylint. Originalanforderungen bleiben unverändert; passende bereits installierte Pakete und Downloadcaches werden wiederverwendet.
- Eigene Nachinstallations-/Reparaturwege installieren keine APT-Empfehlungen und behalten passende Debian-Archive. Pflichtabhängigkeiten bleiben erhalten.
- Unbedingte pip-Selbstupdates entfallen. Die bereits gemeinsame Debian-Paketliste bleibt nach Auswahl gefiltert und enthält gemeinsame Pakete nur einmal.
- Eigene GPS-JSON-Abfragen benötigen gpsd-clients mit seinen Grafik-/Diagnoseabhängigkeiten nicht mehr. Ein kleiner Standardbibliothek-Helfer liest GPSD-Daten, Satelliten- und Zeitwerte direkt. Der GPS-NMEA-Datenweg bleibt erhalten.
- Die optionale GPS-Zeitzonendatenbank verwendet einen getrennten Root-Cache und vorhandene passende Systembibliotheken. Das behebt die im Protokoll beobachtete Cache-Deaktivierung.
- Die zusätzliche Witty-Pi-4-Paketphase und der printf-Fehler bei der Paketlistenanzeige entfallen.
- Erforderliche WIRC-Bild-/Videobibliotheken bleiben erhalten; es wird kein Desktop eingerichtet.

Prüfung
- Paketauflösung, Entwicklerfilter, wiederholte Installation ohne neue Paketinstallation, Hersteller-Manager und normaler Start nach Schrumpfung in Softwaretests geprüft.
- GPS-JSON mit fragmentierten Nachrichten und Satellitenwerten getestet. Wartungsstart, fehlerhafte Schrumpfergebnisse und andere Karten werden nicht automatisch erweitert.
- Durchsatz, Gesamtinstallationsdauer und der nächste automatische Erweiterungsstart sind anschließend auf echter Raspberry-Hardware zu prüfen.
