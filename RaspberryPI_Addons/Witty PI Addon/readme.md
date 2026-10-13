# Witty Add-on 0.9.3

Witty Add-on 0.9.3 | 13.10.2026
Änderungen gegenüber 0.9.2.1

Gemeinsame SD-Wartung
- Windows-Updates ohne vorhandene Basisinstallation brechen mit „Bitte zuerst Basisinstallation ausführen“ vor der Paketinstallation ab. Grundinstallation wird ausschließlich über den passenden Installationsweg gestartet.
- Witty Pi 4 und Witty Pi 5 werden anhand vorhandener Herstellerdienste auch ohne Add-on-Konfiguration erkannt; die passende Wartungsabschaltung bleibt erhalten.
- Fehlende Linux-Wartungswerkzeuge werden nur bei einem Schrumpfauftrag nachinstalliert. Es werden weder Homepage-Module noch Herstellerpakete automatisch installiert.
- Die automatische Erweiterung nach geprüfter Schrumpfung verwendet dauerhaft gespeicherte Helfer statt eines vorausgesetzten globalen Add-on-Befehls. UUID-/Ergebnisprüfung und Trennung vom Abschaltstart bleiben erhalten.
- Windows 0.9.3 enthält diese Helfer zusätzlich als separates sd-maintenance.sh in seinen verschlüsselten Updates. Kartenwartung ist damit auch ohne vorherige Add-on-Installation möglich.
- Windows-Korrekturen: Partitionsstatus in derselben Zeile, frisches Terminal nach Hostnameänderung, neuer Sicherungsname nach Kartenabfrage und angepasster Auswurf nach Abbildsicherung.

Prüfung
- Herstellererkennung ohne Add-on und dauerhafte Erweiterungshelfer in Softwaretests geprüft. Abschaltung und Auswurf benötigen den anschließenden Test auf der jeweiligen Hardware.
