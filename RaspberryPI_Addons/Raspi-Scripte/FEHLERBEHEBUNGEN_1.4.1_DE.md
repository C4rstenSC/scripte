# Fehler und Korrekturen in Version 1.4.1

Für Papa – Stand 9. November 2026

| Fehler / Beobachtung | Festgestellte Ursache | Korrektur in 1.4.1 |
|---|---|---|
| Sydney bleibt bei UTC+10, obwohl automatische Sommer-/Winterzeit eingeschaltet ist. | Die bisherige Offset-Auswahl transportiert einen Ortsnamen. Der Eintrag +10 kann Lindeman repräsentieren; dort gibt es keine Sommerzeit. Beim Rückwechsel wurde dieser Name statt Sydney angewendet. | Region und festen Offset getrennt speichern. Für Papa Australia/Sydney wählen; diese Region bleibt auch ohne GPS gespeichert. Eine vorhandene ursprüngliche Regionskonfiguration wird übernommen. |
| UTC+10 muss in Sydney manuell auf +11 umgestellt werden. | Ein fester Offset und eine regionale Sommerzeitregel wurden vermischt. | Automatik verwendet die Region und das Datum. Fester Offset bedeutet dagegen immer genau den gewählten Wert. |
| Der feste Allsky-Offset beeinflusst die Rückkehr von WURB/WIRC zur Automatik. | Systemregel und Allsky-Folgeregel waren gekoppelt. | Ein zuvor gespeicherter fester Allsky-Offset bleibt bestehen, wenn die Systemregel wieder automatisch wird. Die Allsky-Berechnungen verwenden ihre gespeicherte Regel. |
| WURB zeigt nach einer Änderung erst nach Dienstneustart die richtige Ortszeit. | Im geprüften Code fehlt ein explizites Nachladen der Zeitregeln. Zusätzlich verwendet WURB einen Solar-Cache ohne Zeitzone und ein beim Programmstart festgelegtes Standarddatum. Der genaue Ablauf auf Papas Pi ist noch nicht protokolliert. | WURB und WIRC laden geänderte Systemregeln während des Betriebs nach. WURB verwirft betroffene Sonnenzeit-Caches und verwendet das aktuelle Berechnungsdatum. |
| Die Homepage wartet lange oder meldet Witty beschäftigt. | Status und Bedienaktionen teilen sich Sperren und Browser-Warteschlangen. Auch die GPS-Suche hielt bereits die globale Sperre. | GPS erst außerhalb der Sperre prüfen; kurze Sperre nur zum Schreiben. Statusabfragen bündeln und unabhängig von der Klick-Warteschlange bearbeiten. Erfolgreiche Aktionen sofort bestätigen und Status danach aktualisieren. |
| GPS wird erst später angesteckt oder bekommt erst später Empfang. | Der bisherige Startauftrag gab nach mehreren Versuchen auf. WIRC konnte danach ohne WURB-eigenen Zeitabgleich bei der alten Uhrzeit bleiben. | Eigenständiger Hintergrunddienst wartet auch später auf einen gültigen, fortschreitenden Fix und synchronisiert bei Bedarf Linux und Witty. Er ändert die gespeicherte Region nicht. |
| Sommer-/Winterzeitwechsel ohne GPS. | Der bisherige Umschaltauftrag verlangte erneut GPS-Zeit. | Linux wendet die Regionsregel an; der Umschaltauftrag aktualisiert die lokale Witty-RTC aus Linux und plant den nächsten Wechsel. |
| Im Terminal ist wieder sudo wp5 nötig. | Die Basiseinrichtung gab bisher nur die App-Sperrdatei frei; der Add-on-Updatepfad führte diese Reparatur nicht erneut aus. Root-Zugriffe oder Herstellerinstallationen können ungeeignete Rechte hinterlassen. Der tatsächliche Dateizustand auf Papas Pi ist nicht ausgelesen. | App- und I2C-Sperrdatei werden ohne Löschen oder Aufbrechen laufender Sperren auf root:i2c und 0660 gesetzt. Der Benutzer wird der i2c-Gruppe zugeordnet. Nach einer Gruppenänderung Terminal neu verbinden. |
| PC-Zeit lässt sich im Windows-Programm nicht direkt auf beide Geräte übertragen. | Ein eigener Bedienknopf fehlte. | Neuer Button Systemzeit => RPI und Witty RTC. Er überträgt einen UTC-Zeitpunkt statt deutscher/australischer Uhrzeitzeichenfolgen, erkennt die PC-Zeitzone und prüft Linux/Witty anschließend. Die Geräte behalten ihre eingestellte Regionsregel. |

## Lokale Zehnjahresdatei und GPS

Die Datei sydney-dst-2026-2036.json enthält 22 Zeitwechsel von 2026 bis einschließlich 2036. Die Berechnung folgt den derzeitigen Regeln und deckt damit die nächsten zehn Jahre ab. Bei einer gesetzlichen Regeländerung müssen Datei und Zeitzonendaten aktualisiert werden. Im automatischen Modus wird bei einem aktuellen GPS-Fix die Region aus den Koordinaten ermittelt; ohne Fix bleibt die gespeicherte Region aktiv. Im festen Modus wird keine GPS-Region angewendet.

## Bedienung für Sydney

Für WURB/WIRC im neuen Regionsfeld **Australia/Sydney** wählen und **Automatische Sommer-/Winterzeit** übernehmen. Im Sommer zeigt Sydney UTC+11, im Winter UTC+10. Ein fehlender GPS-Empfänger verhindert diese Regel nicht; GPS liefert bei gültigem Empfang den UTC-Zeitpunkt. Ein fester Offset bleibt ganzjährig fest.

Ein bereits gespeicherter fester Allsky-Offset bleibt beim Rückwechsel der Systemregel auf Automatik erhalten. Die PC-Zeitübertragung ändert keine Regionsregel. Nach dem ersten Update müssen die Programmdienste einmal neu geladen werden, um den neuen Code zu verwenden; spätere Zeitregeländerungen benötigen keinen Dienstneustart.

## Prüfstand und Grenzen

Die Korrekturen sind im Code und durch gezielte Softwaretests geprüft. Windows wurde für win-x64 kompiliert. Für GPS wurden gültige/ungültige und fortschreitende gpsd-Daten beider Anschlussarten simuliert; die zwei echten Mäuse wurden hier nicht angeschlossen. Die tatsächliche Laufzeitverkürzung, das Verhalten der Witty-Firmware sowie ein ausgeschalteter Raspberry über einen kompletten Zeitumstellungstermin sind auf den Geräten noch nicht physisch geprüft.
