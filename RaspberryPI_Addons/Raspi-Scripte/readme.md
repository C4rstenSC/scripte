# Raspi-Scripte 0.6.23

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
