# Smart Life Desktop 0.2.5

Deutscher Windows-Client für Smart Life mit direktem Zugriff auf ein verknüpftes Tuya-Cloud-Projekt.

[Windows-Setup herunterladen](downloads/SmartLife-Desktop-0.2.5-Setup.zip). ZIP entpacken und `Installieren.cmd` starten. Vorhandene Installationen erhalten das App-Paket über den Update-Button. Updates werden beim Start und alle 60 Sekunden geprüft. Rote Schrift erscheint nur bei einer neueren Version.

## Änderungen in 0.2.5

### FRITZ!Box im Heimnetz

Die Spalte „IP-Adresse (Tuya)“ entfällt. Geräte und Räume zeigen stattdessen **Lokale IP-Adresse** und **FRITZ!Box-Hostname**. Unter **FRITZ!Box anmelden** die lokale Adresse (standardmäßig `fritz.box`), den FRITZ!Box-Benutzer und dessen Kennwort eingeben. „Anmelden und Netzwerk lesen“ liest die Netzwerkgeräteliste über die lokale, dokumentierte TR-064-Schnittstelle mit HTTP-Digest-Anmeldung. In den Netzwerkeinstellungen der FRITZ!Box muss „Zugriff für Anwendungen zulassen“ aktiviert sein. Der Benutzer benötigt die passenden Leserechte. Der Vorgang liest nur Netzwerkdaten und ändert keine Routereinstellungen oder DHCP-Reservierungen. Die Anmeldung wird auf Wunsch auf Windows mit DPAPI bzw. später unter macOS im Schlüsselbund geschützt gespeichert; keine Routerkennwörter in GitHub.

Automatische Zuordnung erfolgt ausschließlich anhand einer eindeutigen MAC-Adresse. Fehlende MAC-Adressen werden für geladene Geräte über Tuyas dokumentierte Factory-Info-Abfrage in Gruppen von höchstens 20 ermittelt. Namen oder gemeinsame öffentliche IP-Adressen werden nicht als Identitätsbeweis verwendet. Unklare Zuordnungen bleiben leer. Geräte hinter einem Gateway erhalten keine erfundene Gateway-IP. Nicht aktive FRITZ!Box-Einträge erhalten keine als aktuell dargestellte lokale Adresse. Wenn Tuya keine passende MAC liefert, kann im FRITZ!Box-Dialog ein Gerät bewusst einem Netzwerk-MAC-Eintrag zugeordnet werden. Die Zuordnung wird bei geschützter Speicherung mitgesichert.

Netzwerkdaten aktualisieren sich nach Anmeldung alle 60 Sekunden sowie auf „Netzwerk aktualisieren“. Nach Geräteänderungen wird, soweit zugeordnet, nur der betreffende Routereintrag nachgelesen. Der FRITZ!Box-Zugriff hat eine eigene Warteschlange; er verwendet keine Tuya-Cloud-Brücke. Unveränderte Smart-Life-Steuerungen bleiben cloudbasiert. Der lokale Programmstart allein macht Tuya-Steuerbefehle nicht zu lokalen Befehlen.

### Bearbeitung während Hintergrundabfragen

Die globale „Bitte warten“-Meldung wurde auch für Szenen, Automationen und Raumverwaltung entfernt. Die vorhandenen Daten können geöffnet werden; neue periodische Abfragen pausieren während der Bearbeitung. Eine laufende Geräteabfrage gibt die Warteschlange zwischen Geräten frei. Ein bereits gesendeter HTTP-Aufruf kann bis zu seinem Timeout noch laufen. Die Bandbreite des Internetanschlusses verhindert solche Serverwartezeiten nicht.

### Aussagekräftige Umbenennungsfehler

Die ursprüngliche PUT-Anfrage zum Umbenennen bleibt gleich. Fehlermeldungen unterscheiden nun „Speichern von Tuya abgelehnt“ von „angenommen, aber Rücklesen fehlgeschlagen“. Code 60001001 wird als Problem des Kontingents für steuerbare Geräte eingeordnet. Ein ausgeschöpftes Cloud-Projektkontingent wird durch dieses Update nicht aufgehoben; es wird keine lokale Umbenennung als erfolgreiche Cloud-Änderung ausgegeben.

113 lokale Tests bestanden: TR-064-Nachrichten, Digest-Konfiguration, lokale Zieladressen, XML-Schutz, Fehlerfälle, eindeutige MAC-Zuordnung, fehlende/mehrdeutige Zuordnung, Geräte ohne eigene IP, gezielte MAC-Abfrage, Netzwerkspalten und Bearbeitungsdialoge bei aktiven Hintergrundabfragen. FRITZ!Box-Dialog und Spalten unter Qt dargestellt. Keine echte FRITZ!Box oder Tuya-Kontingentfreigabe aus dieser Entwicklungsumgebung getestet.

Quellen: FRITZ! TR-064 Hosts https://fritz.support/resources/TR-064_Hosts.pdf ; TR-064-Anmeldung https://fritz.support/schnittstellen/TR-064_first_steps.pdf ; Tuya Factory-Informationen https://developer.tuya.com/en/docs/cloud/device-management?id=K9g6rfntdz78a .

## Änderungen in 0.2.4

Gerätenamen und Raumzuordnungen aktualisieren die Anzeige gezielt. Nach einer Namensänderung wird das ausgewählte Gerät über die Gerätedetails zurückgelesen und der Name geprüft. Eine bloße Schreibbestätigung reicht nicht mehr; bei abweichendem Rücklesewert gibt es keine Erfolgsmeldung. Nur die Leseprüfung wird bei Bedarf wiederholt, nicht der Schreibvorgang. Der neue Name wird danach im Dialog, in Liste, Detailansicht und den gerätebezogenen Szenen-/Automationsdarstellungen übernommen. Bereits bestätigte Namen werden während derselben Sitzung auch bei explizitem Neuladen aus den Gerätedetails gelesen, damit ein alter Name aus einer Zuhause-Liste sie nicht direkt zurücksetzt.

Nach der Änderung werden ausschließlich dieses Gerät, seine betroffenen Raumzuordnungen und bereits geladene Automationen mit Bezug auf seine Kennung nachgelesen. Andere Geräte, ganze Zuhause, Raumlisten und vollständige Automationslisten werden nicht erneut abgefragt. Raumzählungen und Anzeigen werden aus den vorhandenen Daten neu berechnet; Szenen verwenden weiterhin dieselbe Gerätekennung. Nicht geladene Regeln können dadurch nicht entdeckt werden.

Die Gerätebearbeitung öffnet sich auch bei einer laufenden Statusabfrage. Die Abfrage pausiert zwischen Geräten; ein bereits laufender HTTP-Aufruf darf zuerst abschließen. Während der Bearbeitung startet keine neue periodische Abfrage. Der Dialog zeigt Speichern und Rücklesen sichtbar an; nach Erfolg bleibt er mit bestätigtem Namen und Erfolgstext geöffnet. Ein vollständiges Neuladen nach dem Schließen entfällt.

91 lokale Tests bestanden, darunter tatsächlicher Klick auf den Speicherbutton, bestätigter und nicht bestätigter Name, gezielte Raum-/Automationsabfragen, erhaltene andere Gerätedaten und Öffnen während einer Hintergrundabfrage. Der ursprüngliche Fehler auf dem Benutzerkonto ist ohne dessen Antworten nicht nachgestellt; echte Tuya-Berechtigungen und Bestätigungen werden zur Laufzeit geprüft.

## Änderungen in 0.2.3

Durchsicht der normalen Geräte-, Raum-, Szenen- und Automationsansichten sowie der Verwaltungsdialoge. Anzeige und Bedienung verwenden ausschließlich zugeordnete deutsche Funktionsbezeichnungen; fremdsprachige Herstellerbezeichnungen bleiben im technischen Bericht und werden nicht mehr als normaler Ersatztext eingesetzt. Nicht zugeordnete Zusatzfunktionen werden in der normalen Bedienansicht ausgeblendet, ohne Gerätedaten oder Einstellungen in der Cloud zu löschen. Unbekannte Auswahlwerte werden nicht als mehrere scheinbar gleichwertige Bedieneinträge angeboten. Vorhandene unbekannte Szenenaktionen bleiben erhalten.

Ergänzte Übersetzungen betreffen unter anderem den Schutz vor unerwartetem Einschalten nach Stromausfall, Luftfeuchte- und Temperaturkorrekturen, externe Fühlertemperatur, Meldeintervalle, Meldeschwellen, Farbtemperatur und Kontrollleuchten. Nicht gelieferte Temperaturwerte erhalten auch kein leeres Einheitensuffix. Komplexe Rohdaten werden nicht als unlesbare JSON-Blöcke in den normalen Wertelisten dargestellt.

Alle Tabellen einschließlich Raumverwaltung und Szenen-/Automationseditor bemessen jede Spalte nach dem breitesten Zellinhalt oder Spaltenkopf plus rund einem Zentimeter Reserve anhand der logischen Bildschirmauflösung. Die Berechnung erfolgt nach dem Füllen; feste Standardbreiten entfallen. Ein horizontaler Scrollbalken erscheint bei Bedarf. Scrollleisten haben eine helle Spur, einen dunklen Schieber und 20 logische Pixel Breite/Höhe; beim Darüberfahren wird der Schieber blau. Auswahl und Detailansicht werden beim Ansichtswechsel konsistent gehalten.

84 lokale Tests bestanden. Hauptansichten sowie Raum-, Cloud-, Szenen- und Automationsdialoge unter Qt dargestellt und geprüft. Keine neue Behauptung zur vollständigen Geräte- oder KI-Unterstützung; die Einschränkungen aus 0.2.2 bleiben bestehen.

## Änderungen in 0.2.2

**Automationseditor:** „Automationen“ → Regel auswählen → „Automation bearbeiten“. Vollständige Details werden vor dem Bearbeiten zusätzlich abgefragt. Name, Gerätebedingungen, Vergleiche, Grenzwerte und Geräteaktionen lassen sich ändern; Bedingungen können ergänzt und entfernt werden. Auch neue Automationen mit Gerätebedingungen sind möglich. Beliebige/eine oder alle Bedingungen sowie eigene logische Verknüpfungen werden unterstützt. Vorhandene besondere Bedingungen und Aktionen sowie Zeitfenster werden unverändert erhalten; besondere Wetter-/Zeitbedingungen sind noch nicht über einen eigenen Editor bearbeitbar. Vor dem Schreiben werden die ursprünglichen Daten erneut gelesen; bei zwischenzeitlicher Änderung wird nicht überschrieben. Fehlen vollständige Originalbedingungen, wird keine bestehende Regel überschrieben. Das ist insbesondere bei den noch ungeklärten Kontoantworten zu prüfen; bloße Listenabfragen reichen nicht mehr.

**Updateprüfung:** Der aktuelle Hauptzweig wird über GitHubs Git-Referenzabfrage ermittelt (Serverantwort: no-cache, max-age=0, must-revalidate). Manifest und ZIP werden danach über denselben unveränderlichen Commit geladen. Schlägt die Referenzprüfung fehl, erscheint ein Fehler statt „aktuell“. Die vorher installierte Version behält ihren alten Prüfweg bis zur ersten Installation dieses Updates. Die neue Prüfung benötigt kein Git-Programm und keinen GitHub-Schlüssel.

78 lokale Tests bestanden. Zusätzlich wurde der Qt-Editor mit geänderter Bedingung und Aktion bis zum erzeugten PUT-Aufruf getestet; Zeitfenster blieben erhalten. Die Git-Referenzabfrage wurde am öffentlichen Repository geprüft. Echtes Speichern mit dem Benutzerkonto ist ohne Zugriff auf dieses Konto nicht verifiziert. Die unbekannte `lightBase`-Aktion und KI-Funktionen bleiben ungelöst; diese Version behauptet keine vollständige iOS-Parität.

## Änderungen in 0.2.1

Eigene Ansicht **Automationen**: im Konto gelieferte Regeln mit Auslösern, Vergleichswerten, Geräteaktionen und Gültigkeitszeiten lesen. Beispielsweise lassen sich Strom- oder Leistungsbedingungen des TVs und das Schalten einer Hintergrundbeleuchtung nachvollziehen. Fehlgeschlagene Abfragen werden angezeigt. Die Ansicht ist schreibgeschützt; Bearbeiten oder Erstellen von Automationen und die KI-Funktionen der iOS-App sind weiterhin nicht implementiert.

Szenen verwenden bevorzugt die dokumentierte v1.1-Abfrage mit v1.0-Rückfall. JSON-kodierte Aktionsparameter und eindeutige numerische Datenpunkte aus dem Gerätemodell werden erkannt. Nicht zugeordnete Originalaktionen erhalten keine erfundene Gerätezuordnung und wählen im Editor kein zufälliges Gerät vor. Die Bedeutung des im Benutzerkonto beobachteten `lightBase`-Formats ist noch nicht bestätigt. Unter der Szene kann ein **Szenenbericht** mit Aktionsstruktur und Geräteschemata gespeichert werden; er enthält keine Kontoanmeldung oder Netzadressen. Erst dieser Bericht ermöglicht bei weiterhin unbekannten Aktionen eine konkrete Zuordnung.

`switch_type_1/2` und `single_click` werden als **Tastenereignis 1/2** und **Einfacher Tastendruck** übersetzt. Die Seitenleiste bemisst sich nach dem längsten Buttontext. Der zusätzliche Fokusrahmen in Tabellen entfällt bei erhaltener Zeilenauswahl und Tastaturbedienung. 66 lokale Tests bestanden; Automationsdarstellung und Szenenauswahl mit Qt geprüft. Echte Kontoantworten bleiben auf dem Ziel-PC zu bestätigen.

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
