# Witty Add-on 1.0.10

Version 1.0.10 · Build 2

Allsky: echte Tag-/Nacht-Steuerung und gemeinsame Zeitbasis
- Die Allsky-Aufnahmeprogramme und die Webseite verwenden bei eingeschalteter Witty-Zeitübernahme dieselbe lokale Sonnenberechnung. Tag/Nacht wird weiterhin aus den tatsächlichen Koordinaten und dem eingestellten Sonnenwinkel bestimmt.
- Sonnenereignisse und der aktuelle Zustand werden anhand absoluter UTC-Zeitpunkte berechnet. Der gewählte feste UTC-Offset bzw. die ausdrücklich gewählte Zeitzone wird zur Darstellung verwendet. Eine GPS-Position aktiviert keine andere Sommerzeitregel.
- Korrekturen an sunwait: UTC-Tagesgrenzen ohne lokale mktime-Umwege, vollständige Stunden-/Minutenabweichung ohne Abschneiden von halben oder Viertelstunden und Umrechnung jedes Ereignisses mit seinem eigenen Sommerzeitstatus. Die ursprünglichen Sonnenformeln bleiben unverändert.
- Der PHP-Countdown bekommt Zustand und nächsten Wechsel gemeinsam als absolute Zeitstempel. Eine bereits vergangene Uhrzeit wird bei aktiver Witty-Regel nicht mehr pauschal auf morgen verschoben.
- In der Allsky-Aufnahmesteuerung wird die Wartepause bei aktivierter Witty-Zeitregel auf maximal 60 Sekunden begrenzt. Danach prüft das Aufnahmeprogramm den tatsächlichen Tag-/Nacht-Zustand erneut; eine fehlerhafte Zeitdifferenz führt nicht mehr zu einer 23-stündigen Wartepause.
- Die benötigten lokalen Programme werden vor dem Austausch gebaut und geprüft. Bei Buildfehlern bleiben die bisherigen Kamera-Dateien erhalten. Die Korrektur wird nach Neuinstallation und Allsky-Updates wieder angewendet; Allsky-Standard bleibt separat auswählbar.
- Die bestehende Mittag-bis-Mittag-Regel für neue Bilderordner bleibt erhalten und verwendet die gewählte Witty-Ortszeit. Bestehende Bilder, tatsächliche Koordinaten, Belichtungseinstellungen und die Systemuhr werden nicht umgestellt.

Prüfung
- 95 automatisierte Allsky-Tests, davon 94 bestanden und ein optionaler Browsertest mangels Playwright übersprungen; zusätzlich 5 Satelliten-Regressionsprüfungen bestanden.
- Unter anderem 1.680 Zeitzonenvergleiche, australische Sommerzeitwechsel, halbe/Viertelstunden, Dämmerungsgrenzen, Mitternacht, Jahres-/Schaltjahreswechsel, PHP-Anzeige und die echten extrahierten Allsky-C++-Steuerfunktionen geprüft.
- Referenzfall: 19 Uhr fest UTC+10 bei 33.73304S / 151.09081E und Angle -6 ergibt Nacht und als nächsten Wechsel den Morgen, nicht den nächsten Abend.
- Auf dem betroffenen Raspberry Pi noch nicht geprüft. Eine falsch gestellte tatsächliche UTC-Systemuhr kann nicht ohne verlässliche Zeitreferenz automatisch korrigiert werden.

Nach dem Update
- Einen als Übergangslösung auf 135 Grad Ost verschobenen Längengrad wieder auf den tatsächlichen Kamerastandort zurückstellen.
- Beim ersten Anwenden werden die vorhandenen Allsky-Aufnahmeprogramme auf dem Raspberry Pi neu gebaut; das kann einige Minuten dauern.

[Technische Änderungen und Aufnahmeablauf](TECHNISCHE_AENDERUNGEN_1.0.10_DE.md)
