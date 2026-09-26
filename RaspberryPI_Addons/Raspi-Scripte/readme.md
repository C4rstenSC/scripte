# Raspi-Scripte 0.6.31

- Die integrierte Hilfe und die herunterladbaren Release Notes benennen Witty Add-on 0.6.42 und die aktuellen Änderungen korrekt.
- Das Inhaltspaket 0.6.32 enthält die aktualisierten Release Notes für das Windows-Programm.
## Frühere Änderungen

- Die Basisinstallation erzeugt eine einmalige Startfreigabe und überträgt sie
  zusammen mit der Konfiguration. Der Raspberry verbraucht sie vor jeder
  Änderung; kopierte oder manuelle Konsolenaufrufe funktionieren nicht erneut.
- Das Raspberry-Pi-Modell wird direkt aus `/proc/device-tree/model` gelesen.
  Eine Pi-5-Auswahl wird auf einem Pi 4B Rev 1.5 bereits vor dem Upload beendet.
- Veraltete lokale Installer ohne gesicherten Windows-Start werden abgewiesen.
- Enthält Witty Add-on 0.6.38 mit korrigierter Hotspotbenennung und
  komponentenabhängigen Abschlussprüfungen.
- Die Auswahl „USB GPS“ funktioniert bei der Installation auch ohne momentan
  angeschlossene Maus und wird beim späteren Einstecken automatisch aktiv.

- Das dauerhafte ALLSKY-Dateilesen aktualisiert die geöffnete Liste nach jedem
  erfolgreichen Abruf. Hostname und IP-Adresse verwenden denselben aktuellen
  Cache.
- Ist der Raspberry erreichbar, aber SSH oder das Dateilesen schlägt fehl,
  wird nach einer Minute erneut versucht. Nach Erfolg gilt wieder der
  Fünf-Minuten-Abstand.
- Der gesamte SSH-Terminalbereich besitzt einen weißen Außenrahmen. Der Inhalt
  belegt ungefähr 75 Prozent der Breite; rechts bleibt Platz zum Scrollen der
  Hauptseite.
- Enthält Witty Add-on 0.6.37 mit einem beim Neuladen erhaltenen
  Fortschrittsbalken für ALLSKY-Speichertransfers. Alle Aktionsknöpfe bleiben
  sichtbar, werden gemeinsam deaktiviert und danach wieder freigegeben. Der
  überflüssige `allsky-setup#`-Link ist entfernt.

- Der SSH-Terminalbereich besitzt wieder den äußeren Rahmen und zusätzlich
  einen eigenen Rahmen um Überschrift und Ein-/Ausklappknopf.
- Das Terminal bleibt beim normalen Verbinden eingeklappt, öffnet sich nur bei
  Installation oder Software-Update automatisch und wird ohne Verbindung
  vollständig geleert.
- Das Dateienlesen-Popup gruppiert ALLSKY-Bilder nach Tagesordnern, sortiert sie
  innerhalb der Ordner und blendet sämtliche Thumbnails aus.
- Enthält Witty Add-on 0.6.35 mit kurzer Updateausgabe, getrennten
  ALLSKY-SETUP-Bereichen und repariertem Speicherwechsel.

- Enthält Witty Add-on 0.6.33 mit geprüftem ALLSKY-Speicherortwechsel.
- ALLSKY-Setup zeigt die Installationsposition und schreibt Änderungen an
  Breitengrad und Längengrad in die ALLSKY-Sonnenwinkelberechnung.
- Ausgewählter USB-Mount und erzeugte PHP-/Lighttpd-Bildpfade werden geprüft;
  Kopieren, Verschieben und Belassen wurden separat getestet.

- Nach jedem Updateknopf werden Firmware- und Softwarestände automatisch mit
  Wiederholungen neu eingelesen; ein Trennen und erneutes Verbinden ist nicht
  mehr erforderlich.
- Webserver starten/stoppen befindet sich jetzt in der Zeile „Witty Addon
  Script“ und bleibt auch bei „Kein Witty“ verfügbar.
- Das SSH-Terminal besitzt wieder einen vollständigen Rahmen und bleibt
  standardmäßig eingeklappt; Installation und Update klappen es bei Bedarf auf.
- Enthält Witty Add-on 0.6.32 mit einheitlichem Navigationsnamen „Witty Addon“
  auf ALLSKY, WURB, WIRC und den Zusatzseiten.
- Die ALLSKY-Webanmeldung mit `admin`/`secret` wird bereits während der
  Installation deaktiviert und bleibt auch nach Update und Restore aus.

- ALLSKY-Konfiguration herunterladen und hochladen verwendet dieselben
  geprüften Web-Endpunkte wie die ALLSKY-SETUP-Seite.
- Nach einem Witty-Addon-Update wartet die Statusanzeige auf die tatsächlich
  installierte Zielversion und aktualisiert sich ohne neues Verbinden.
- Die Titelleiste übernimmt die Version direkt aus der laufenden EXE.
- Hauptprogramm und Updater sind mit SHA-256 Authenticode als
  `Carsten Schulte` signiert.
- Das öffentliche selbstsignierte Zertifikat wird beim ersten Start für den
  aktuellen Windows-Benutzer in `Root` und `TrustedPublisher` hinterlegt.
  Danach werden spätere Pakete mit demselben Zertifikat lokal erkannt.

## Zertifikat

Das öffentliche Zertifikat `Carsten-Schulte-CodeSigning.cer` enthält keinen
privaten Schlüssel. Eine selbstsignierte Signatur ist nicht öffentlich durch
Microsoft bestätigt. Auf einem neuen Rechner kann beim ersten Start daher
noch eine Warnung erscheinen. Eine kostenlose weltweit vertrauenswürdige
Microsoft-Herausgeberbestätigung gibt es nicht.

Der private Schlüssel ist absichtlich nicht in diesem öffentlichen Repository
enthalten.
