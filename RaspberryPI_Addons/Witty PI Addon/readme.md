# Witty Add-on 0.6.24

Release: 23.09.2026

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
