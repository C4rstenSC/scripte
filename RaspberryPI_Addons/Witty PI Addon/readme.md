# Witty Add-on 0.6.27

Release: 23.09.2026

- Das Update von älteren Raspberry-Pi-4-Installationen bricht nicht mehr ab,
  wenn `/etc/witty-addon.conf` noch fehlt. Die notwendige Konfiguration wird
  aus Raspberry-Modell und vorhandener Witty-Herstellersoftware ergänzt.
- Ist der bisherige GPS-Modus nicht dokumentiert, bleiben der funktionierende
  WURB-GPS-Pfad und die Zeiteinstellungen unverändert.
- Danach werden der unabhängige Add-on-Webdienst auf Port 8081 und der Link
  „Witty Addon“ in der vorhandenen WURB-Navigation verbindlich repariert.
- Ein unerwarteter Skriptabbruch nennt künftig Zeile, Befehl und Exit-Code,
  statt lediglich mit einem nicht erklärten Exit-Code 2 zu enden.

- Port 8081 und der sichtbare „Witty Addon“-Link werden in allen Varianten
  installiert: „Kein Witty“, Witty Pi 4 und Witty Pi 5.
- Die unterschiedliche Herstellersoftware bleibt getrennt: Witty Pi 4 nutzt
  `wittypi.service`, Witty Pi 5 nutzt `wp5d.service`, und ohne Platine wird
  keiner der beiden Dienste vorausgesetzt.
- WURB- und WIRC-Homepagepatches werden anhand ihrer unterschiedlichen
  HTML-Strukturen verbindlich geprüft; Patchfehler werden nicht mehr ignoriert.

- Auf Raspberry Pi 4 ohne Witty-Hardware wird die Add-on-Webseite auf Port
  8081 jetzt vor allen optionalen WURB-/WIRC-/GPS-Prüfungen gestartet.
- Der Webserver wartet nicht mehr auf `wp5d.service`. Bei einem Startfehler
  erscheinen systemd-Status und die letzten Journalzeilen direkt im Terminal.

- Beim Wiederherstellen einer ALLSKY-Sicherung bleibt Lighttpd online, damit
  die Browser-Verbindung nicht unterbrochen wird.
- Der vorherige Lighttpd-Zustand wird zuverlässig wiederhergestellt und bis zu
  15 Sekunden geprüft. Bei einem echten Fehler erscheint jetzt das Journal des
  betroffenen Dienstes statt der langen ALLSKY-Kameraausgabe.

- Nach einer Änderung an der WURB- oder WIRC-Navigation wird ausschließlich
  der betroffene Dienst neu gestartet und anschließend auf Port 8080
  beziehungsweise 8082 geprüft. Der Link „Witty Addon“ ist dadurch sofort
  sichtbar.

- Das Update prüft und aktiviert den Add-on-Webdienst nun bei jedem Lauf; ein
  vorhandener Programmordner gilt nicht mehr als Nachweis eines laufenden
  Dienstes.
- Ein fehlender, deaktivierter oder nicht antwortender Webserver wird neu
  eingerichtet und auf Port 8081 geprüft.
- WURB- und WIRC-Navigation werden erneut ergänzt und danach verbindlich auf
  den Link „Witty Addon“ geprüft.
- Eine unvollständige Erstinstallation wechselt automatisch in die
  Grundinstallation; optionale GPS-/Zeitfehler blockieren die Webreparatur
  nicht mehr.
- ALLSKY-Installationsabbrüche geben die vorhandenen offiziellen Protokolle
  künftig direkt im SSH-Terminal aus.

Auf GitHub liegt ausschließlich das verschlüsselte Paket
`witty_addon.zip.enc`; eine unverschlüsselte `witty_addon.zip` wird nicht
veröffentlicht.
