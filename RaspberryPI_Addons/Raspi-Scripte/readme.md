# Raspi-Scripte 0.9.0

Raspi-Scripte 0.9.0 | 13.10.2026
Änderungen gegenüber 0.8.9

SD-Karten und Abbilder
- Beim Wiederherstellen wird der Hostname aus /etc/hostname der ausgewählten IMG-Datei gelesen; der Dateiname und die vorhandene Zielkarte bestimmen diese Anzeige nicht.
- „Hostname setzen“ merkt den neuen Namen vor. Erst „Image schreiben und prüfen“ schreibt das Abbild und den einmaligen Auftrag für Hostname, /etc/hosts und vorhandene Installer-Hotspotnamen. WLAN-Passwörter, Profilkennungen und übrige Einstellungen bleiben erhalten.
- Vorbereitung und Prüfung erfolgen an einer temporären IMG-Kopie. Das ursprüngliche Abbild bleibt unverändert; eine gewünschte Erststart-Erweiterung bleibt mit der Hostnamenänderung kombinierbar.
- Alle drei SD-Bereiche besitzen einen Aktualisieren-Button. Die bisherige Karte bleibt gewählt, sofern sie noch vorhanden ist; sonst erscheint die erste gefundene Karte. Vorhandene Windows-Laufwerksbuchstaben werden angezeigt.
- Nach Expandieren wartet die automatische Wiederverbindung höchstens 50 Sekunden. Andere geplante Neustarts behalten drei Minuten.
- Nach einem neuen erfolgreichen Schrumpfauftrag bleibt die Karte bis zur Sicherung verkleinert. Beim nächsten normalen Raspberry-Start wird sie automatisch wieder erweitert. Der Prüf-/Abschaltstart erweitert sie nicht; unbestätigte Schrumpfergebnisse werden nicht automatisch weiterverarbeitet.

Updates und Herstellerinstallation
- Ein Programmupdate bricht eigene laufende SD-Aufträge und Image-Vorbereitungen ab und wartet auf deren vollständiges Ende. Neue SD-Aufträge bleiben währenddessen gesperrt. Eine teilweise beschriebene Karte muss erneut beschrieben werden.
- Weitere Instanzen aus demselben Programmordner werden vor dem Update erkannt. Der Updater beginnt erst nach Ende des ursprünglichen Prozesses; ein nach sauberem SD-Abbruch verbliebener ursprünglicher Prozess wird gezielt beendet.
- Fehler beim Dateiaustausch berücksichtigen auch die gerade geschriebene Datei bei der Rücksicherung. Updatefehler erscheinen als lesbare Meldung samt Protokollpfad.
- Der Hersteller-Manager wird auch bei Add-on-Updates nach /usr/local/sbin kopiert. Der Steuerbefehl kann zusätzlich die vorhandene Backend-Kopie verwenden. Dies behebt „Hersteller-Manager fehlt“ bei Witty-Nachinstallation.

Installation beschleunigen
- WURB/WIRC installieren die in ihren Quellanforderungen enthaltenen Entwicklerwerkzeuge black und pylint nicht mehr für den normalen Betrieb. Die Originalanforderungen bleiben unverändert.
- Auch die eigenen Nachinstallations- und Reparaturwege verzichten auf APT-Empfehlungen und behalten heruntergeladene Debian-Archive. Erforderliche Abhängigkeiten bleiben aktiv.
- Unbedingte pip-Selbstupdates bei Installation und Reparatur entfallen. Passende vorhandene Pakete werden wiederverwendet; beide Benutzerumgebungen nutzen denselben Paketcache.
- Der GPS-JSON-Zugriff verwendet einen eigenen kleinen Python-Standardbibliothek-Helfer. Das umfangreiche Paket gpsd-clients samt grafischen Diagnoseabhängigkeiten entfällt für unsere GPS-Funktionen.
- Die optionale GPS-Zeitzonendatenbank verwendet einen passenden Root-Cache und darf bereits vorhandene Systembibliotheken lesend mitbenutzen. Die gemeldete Cache-Deaktivierung und ein unnötiger separater NumPy-Download werden dadurch vermieden, sofern die Systemversion genügt.
- Eine doppelte Witty-Pi-4-Paketphase entfällt. Die Ausgabe der ausgewählten Paketliste wurde korrigiert.
- WIRC benötigt weiterhin OpenCV-Bild-/Videoverarbeitung und Picamera2. Deren erforderliche Bibliotheken werden nicht blind entfernt. Diese Bibliotheken bedeuten keine Installation eines Desktops.

Oberfläche
- Ein kräftiger grau-schwarzer Außenrahmen grenzt das Programmfenster vom Desktop ab.
- Weiße Auswahlfelder der SD-Kartenseite erhalten ein hellgraues Feld und eine ebenfalls graue Auswahlliste.
- Meldungen und Bestätigungen verwenden ein gemeinsames dunkles Fenster mit Programmfarben und lesbaren Schaltflächen statt der alten Windows-Meldungsboxen.
- Meldungsfenster gehören zum Hauptfenster und bleiben innerhalb der Software darüber. Beim Schrumpfstart erscheint der Hinweis, bis zum vollständigen Herunterfahren und Ausschalten zu warten.
- Die Partitionsanzeige erhält eine eigene Zeile ohne überdeckenden Schaltflächen. „Statusprüfung ausstehend“ wurde entfernt; während des Neustarts erscheint nur „Neustart …“.
- Aktiver Tab und Inhaltsbereich bilden einen durchgehenden Rahmen. Abstände zwischen den Tabs und die volle Inhaltsbreite bleiben erhalten.

Prüfung
- Reale FAT/ext4-Testabbilder, unveränderte IMG-Quelle, Hostnamen-/Erweiterungskombination, Abbruch und Kartenanzeige geprüft.
- GPS-JSON mit fragmentierten Daten, Satellitenwerten und Nachrichtenbegrenzung geprüft. Python-Paketauflösung prüft Entwicklerfilter und unveränderte Quellanforderungen.
- Automatische Erweiterung nur nach passendem verifiziertem Ergebnis, nur im normalen Boot und mit abschließender Dateisystemprüfung getestet. Wartungsstart und fehlerhafte/andere Kartenergebnisse bleiben geschützt.
- Hersteller-Manager und Wiederverbindung mit simulierten Diensten getestet. Windows-Anwendung und Updater werden vollständig gebaut. Laufzeit und Durchsatz auf echter Pi-/Windows-Hardware müssen anschließend bestätigt werden.
