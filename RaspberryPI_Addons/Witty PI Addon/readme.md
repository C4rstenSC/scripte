# Witty Add-on 0.8.7

Witty Add-on 0.8.7 | 13.10.2026
Änderungen gegenüber 0.8.6

Pakete nach Auswahl
- Die Basisinstallation bildet eine einzige, eindeutige Paketliste aus WURB, WIRC, Allsky, GPS und Witty. Gemeinsame Pakete stehen darin nur einmal.
- Ohne Module werden nur Homepage-/Update-/Hotspot-Voraussetzungen verarbeitet. Audio-, Video-, GPS- und Entwicklungsstacks entfallen.
- Die GPS-Zeitzonendatenbank wird nur bei ausgewähltem GPS installiert. Ohne Witty/GPS bleiben RTC und Zeitdienste unverändert.
- I2C und Witty-Sperrdateien werden nur für ausgewählten Witty eingerichtet. Ungewählte bestehende Anwendungen werden im Basislauf nicht repariert oder umkonfiguriert.
- Allsky-Basispakete werden in der gemeinsamen Paketphase berücksichtigt. Gemeinsamer pip-Cache und erhaltene APT-Archive vermeiden erneute Downloads derselben bereits verfügbaren Pakete.

Witty-Abschaltung
- Bereits installierte Herstellersoftware wird auch berücksichtigt, wenn die Homepage aktuell auf „Kein Witty“ eingestellt ist. Die reine Homepage-Installation installiert weiterhin keine Herstellerpakete.
- Hersteller-Abschluss fordert shutdown now an. Ein zusätzlicher Schritt nach wp5d --poweroff prüft den tatsächlichen Zustand STOPPING.
- Falls der Herstelleraufruf ohne Abschaltwirkung zurückkehrt und Witty weiterhin ON ist, sendet der kombinierte I2C-Helfer die Abschaltmeldung und prüft sie erneut.
- „Kein Witty“ installiert keinen Herstellerdienst; damit kann der Pi allein herunterfahren, aber keine Witty-Stromabschaltung auslösen.

Status und Oberfläche
- Neue Wartungsprotokolle enthalten Hostname und Partitions-UUIDs. Alte oder kopierte Protokolle werden nicht als aktuelle Wartungsfehler eines anderen Geräts behandelt.
- Aktive Homepage-Buttons sind dunkler und besitzen sichtbare Ränder, Hover- und Tastaturfokuszustände. Deaktivierte Buttons bleiben heller.

Erweitern und Deinstallieren
- Partitionsvergrößerung setzt nur die neue Größe der letzten Partition. Vorhandene Kennungen bleiben erhalten; ext4 wird online oder über einen verifizierten einmaligen Bootdienst erweitert.
- Der Witty-Hersteller-Neustarthook wird während Wartungsneustarts nur im aktuellen Laufzeitsystem maskiert. Dadurch wird kein zusätzlicher Stromzyklus während Dateisystemarbeiten angefordert.
- Deinstallation wird auch bei unvollständiger Installation ausgeführt. Projektordner unter mehreren Benutzern werden gesichert und bereinigt; externe Einstellungen bleiben erhalten.

Prüfstand
- Auswahlkombinationen und Abschaltbestätigung in Softwaretests geprüft. Erfolgreiche Verkleinerung wurde am Gerät gemeldet; tatsächliche Stromabschaltung benötigt weiterhin den Hardwaretest.
