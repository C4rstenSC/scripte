# Witty Add-on 0.6.22

Release: 23.09.2026

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
