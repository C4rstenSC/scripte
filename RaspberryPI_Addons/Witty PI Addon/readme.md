# Witty Add-on 0.8.6

Witty Add-on 0.8.6 | 13.10.2026
Änderungen gegenüber 0.8.5

Verkleinern und vollständig abschalten
- Neuer Abschlussweg nach erfolgreicher Offline-Verkleinerung: Neustart in ein eigenes systemd-Ziel mit der installierten Witty-Herstellersoftware, anschließend shutdown -h now über den Hersteller-Abschaltdienst.
- Vor der Abschaltung werden Boot-/Root-UUID und tatsächliche Partitionsgröße mit dem Wartungsergebnis verglichen. Fehlerhafte oder ungeprüfte Ergebnisse werden nicht als erfolgreicher Abschluss behandelt.
- WURB, WIRC und Allsky werden im eigenen Abschlussziel nicht gestartet. Bekannte automatische Erweiterungsdienste werden für diesen einen Start maskiert; die ursprüngliche Kommandozeile wird vor dem Abschalten wiederhergestellt.
- Vorhandene init-/systemd-Erststartaufträge werden vor der Vorbereitung erkannt und abgewiesen.

I2C und Diagnose
- Kombinierte I2C-Transfers entsprechen dem Herstellerzugriff. Die Firmware-Version erscheint im Wartungsprotokoll.
- Ungültige Zustände, einschließlich des gemeldeten Werts 10, werden nicht als ON ausgelegt. Laut Herstellerprotokoll sind nur 0 bis 3 gültig.
- Abschlussanforderung und Abschlussfehler stehen getrennt vom Schrumpfergebnis im Bootprotokoll. Eine angeforderte Abschaltung beweist noch keinen tatsächlichen Stromabschluss.

Dokumentation
- Anleitung und Release Notes beschreiben den neuen Ablauf und die Grenzen des Softwaretests. Terminal-Ausgabe bleibt auf Änderungen seit dem installierten Stand begrenzt.

Prüfstand
- I2C- und Abschlussabläufe mit simulierten Geräten geprüft. Hersteller-Abschluss, tatsächliche Stromabschaltung und das Verhalten bei der gemeldeten ungültigen Antwort benötigen den Test am Gerät.
