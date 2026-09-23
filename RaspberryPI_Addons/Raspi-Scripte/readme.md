# Raspi-Scripte 0.6.24

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
