# Smart Life Desktop 0.2.0

Deutscher Windows-Client für Smart Life mit direktem Zugriff auf ein verknüpftes Tuya-Cloud-Projekt.

[Windows-Setup herunterladen](downloads/SmartLife-Desktop-0.2.0-Setup.zip). ZIP entpacken und `Installieren.cmd` starten. Vorhandene Installationen erhalten das App-Paket über den Update-Button. Updates werden beim Start und alle 60 Sekunden geprüft. Rote Schrift erscheint nur bei einer neueren Version.

## Direkten Cloudzugriff einrichten

1. Im Tuya-Cloud-Projekt das Smart-Life-Konto unter Devices mit Automatic Link verknüpfen.
2. Unter Service API die erforderlichen Dienste autorisieren. Das Projekt benötigt Zugriff auf Geräte sowie die verwendeten Zuhause-, Raum- und Szenen-APIs.
3. Unter Overview Access ID und Access Secret ablesen. Die UID des verknüpften App-Kontos steht unter Devices / Link Tuya App Account.
4. Im Desktop-Programm „Direkter Cloudzugriff“ öffnen, die Angaben und das zum Konto passende Datenzentrum eintragen. Für das eingerichtete Konto: Mitteleuropa / Central Europe.
5. „Prüfen und verbinden“ anklicken. Der Verbindungstest liest nur Daten.

Schlüssel nur im Programm eingeben. Die Anmeldung wird unter Windows mit DPAPI für den aktuellen Benutzer geschützt gespeichert. Die QR-Anmeldung bleibt als eingeschränkter alternativer Zugang verfügbar.

## Funktionen in 0.2.0

- Direkte Cloud-Anmeldung, Zuhause und Räume einschließlich leerer Räume, Geräte und Original-Szenen laden.
- Gerätemodelle und Datenpunkte abfragen, einschließlich des Rohmodells und gemeldeter Schattenwerte; unterstützte Steuerungen aus den tatsächlichen Schreibrechten ableiten.
- Rollladen: gelieferte Istposition getrennt vom Sollwert anzeigen; angebotene Öffnen-/Stoppen-/Schließen- und Positionsfunktionen bedienen. Keine Position schätzen.
- Original-Cloud-Szenen mit Geräteaktionen am PC erstellen und bearbeiten. Speichern führt die Szene nicht aus. Fremde oder nicht unterstützte Aktionen bleiben erhalten und werden schreibgeschützt angezeigt. Vor Überschreiben wird auf zwischenzeitliche Änderungen geprüft.
- Geräte umbenennen und vorhandenen Räumen zuweisen. Räume erstellen, umbenennen und löschen; nur leere Räume können gelöscht werden.
- Übersicht nur mit Temperatursensoren und Luftfeuchte. Raum-Tabs per Maus verschieben; Reihenfolge lokal speichern.
- Eigene Batteriespalte. Ohne gemeldete Batterie keine Batterieanzeige. Nicht gelieferte Werte und leere Werteblöcke bleiben ausgeblendet. Ein tatsächlicher Wert 0 wird angezeigt.
- Deutsche bekannte Funktions- und Auswahlbezeichnungen; unbekannte Herstellerfunktionen behalten ihre eindeutige Bezeichnung und ihren Code.

## Verschlüsselter Zugang für einen weiteren Rechner

Nach erfolgreicher Verbindung unter „Direkter Cloudzugriff“ → „Zugang verschlüsselt sichern“ eine `.enc`-Datei exportieren. Ein separates Kennwort mit mindestens zwölf Zeichen schützt die Datei mit Scrypt und AES-256-GCM. Das Kennwort wird nicht mitgespeichert. Nur diese verschlüsselte Datei darf ins Repository, niemals die unverschlüsselten Projektdaten. Zum Import auf einem weiteren Rechner wird das Kennwort einmalig benötigt. Ein Mac-Paket ist noch nicht veröffentlicht. Dieses Repository enthält bisher keine persönliche Zugangsdatei.

## Prüfung und Grenzen

55 lokale Modell-, Protokoll-, Verschlüsselungs- und Oberflächentests bestanden; Qt-Dialoge unter Linux geprüft. Windows-Laufzeit, echter Projektzugriff, konkrete Rollladen-Datenpunkte und Änderungen im Benutzerkonto müssen auf dem Ziel-PC bestätigt werden. Die direkte Cloud-Anbindung ist eine neue Funktion und keine Zusage vollständiger iOS-Funktionsgleichheit. Bearbeitbare Geräteaktionen verwenden Boolean-, Enum- und Integer-Datenpunkte; komplexe JSON-Aktionen und Automationsbedingungen werden nicht vollständig editiert. API-Berechtigungen und Cloud-Abonnements bestimmen den verfügbaren Zugriff. Ein fehlgeschlagener Abruf wird als Fehler gemeldet.

SmartScreen lässt sich ohne geeignete Herausgebersignatur und Reputation nicht zuverlässig vermeiden. Die Installation deaktiviert keine Windows-Schutzfunktionen. Der macOS-Kanal bleibt nicht freigegeben.

## Quellcode und Updates

`app/` enthält den Python-/Qt-Client, `tests/` die Tests, `updates/windows.json` das Manifest und `updates/windows/` die versionierten App-Pakete. `runtime-lock.json` legt die offiziellen Laufzeitquellen und SHA-256-Werte fest. Das kleine Setup lädt diese Abhängigkeiten bei Bedarf einmalig herunter. Die Updateinstallation prüft die Prüfsumme und behält Anmeldung und Laufzeit.

Tests: `python -m unittest discover -s tests -v`. Vorschau: `python app/main.py --demo`.

## Hinweise zu Fremdsoftware

Unabhängiges Projekt ohne Zugehörigkeit zu Tuya oder Home Assistant. Tuya Device Sharing SDK (MIT): https://github.com/tuya/tuya-device-sharing-sdk . Referenz der öffentlichen QR-Registrierung: https://github.com/home-assistant/core/tree/dev/homeassistant/components/tuya . Python: PSF-Lizenz. PySide6/Qt: LGPLv3/GPLv3 oder kommerzielle Lizenz; Hinweise liegen den Abhängigkeiten bei. Dynamische Qt-Bibliotheken bleiben austauschbar. Weitere Pakete behalten ihre jeweiligen Lizenzdateien.
