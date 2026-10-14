# Raspi-Scripte 0.9.8

Version 0.9.8 · Build 3
Änderungen gegenüber 0.9.8 Build 2

Ethernet-Freigabe nach dem Start
- Die Freigaberoutine setzt eth0 ausdrücklich administrativ auf UP. Die NetworkManager-Verwaltung allein ließ den Port im gemeldeten Boot auf DOWN stehen.
- Das von unserer Verzögerungsregel gespeicherte Ethernet-Profil erhält Autoconnect, damit NetworkManager es auch nach später abgeschlossener Link-Aushandlung aktiviert.
- Ein noch nicht verfügbarer Link wird nicht mehr fälschlich als fehlendes Kabel gemeldet. Es gibt keine zusätzliche feste Startpause; die automatische Verbindung erfolgt bei verfügbarem Link. Allsky, WURB, WLAN und Hotspot werden dadurch nicht auf Ethernet warten gelassen.
- Der separate Ethernet-Timer bleibt unverändert. Die Terminalkorrekturen aus Build 2 bleiben enthalten.

Release Notes im Update-Terminal
- Der Update-Starter verwendet vollständig geschlossene WITTY-CONTROL-Blöcke. Dadurch werden die folgenden Release Notes und Update-Ausgaben auch vom älteren Windows-Filter nicht verschluckt.

Prüfung
- Der manuelle Vergleich am gemeldeten Pi ergab nach dem Hochsetzen von eth0 einen Link nach rund vier Sekunden und anschließend die Ethernet-Adresse 192.168.178.181.
- Softwaretests prüfen einen zunächst DOWN stehenden Port, ausstehende Link-Aushandlung, eine bestehende Verbindung und die Profilaktivierung. Der automatische Ablauf nach dem nächsten Boot benötigt weiterhin den Test am Pi.
- Die Ursache der zusätzlich gemeldeten Hotspot-SSH-Abbrüche ist noch offen.
