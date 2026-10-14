# Raspi-Scripte 0.9.7.1

Version 0.9.7.1 · Build 7
Änderungen gegenüber 0.9.7.1 Build 6

Ethernet und lokaler Start
- Beim Raspberry Pi 5 wird Ethernet über einen eigenen Timer frühestens 15 Sekunden nach Bootbeginn und nach den eingeordneten lokalen Startdiensten freigegeben. Der Timer hält multi-user.target nicht auf; Allsky darf davor starten.
- Ohne Netzwerkkabel wird keine Verbindung mit langer Wartezeit erzwungen. Nach der Freigabe übernimmt NetworkManager wieder die Verwaltung; spätes Einstecken bleibt mit automatisch verbindenden Profilen möglich. WLAN und Hotspot werden nicht verzögert.
- Der exakt passende manuelle 20-Sekunden-Testdienst wird übernommen und dessen Ethernet-Profil wieder auf automatische Verbindung gestellt. Die laufende SSH-Verbindung wird beim Update nicht getrennt; die neue Regel gilt beim nächsten Boot. Andere Profilentscheidungen bleiben erhalten.

Windows-Oberfläche
- Terminal-Größenänderungen übertragen die SSH-Fenstergröße im Hintergrund und bündeln aufeinanderfolgende Änderungen. Ein langsamer SSH-Schreibvorgang blockiert dadurch nicht mehr den UI-Thread beim Verkleinern des Fensters.
- Auch das Allsky-Auswahlfenster unterbricht Terminal-Eingabe und automatische Fokusübernahme. Inaktive oder durch Dialoge gesperrte Hauptfenster erhalten keinen automatischen Terminal-Fokus; Tastatureingaben bleiben beim Dialog.

Prüfgrenzen
- Der Nutzer bestätigte einen Neustart nach Allsky-Installation mit der bisherigen Ethernet-Verzögerung. Der kürzere Timer und die Windows-Korrekturen benötigen den anschließenden Test am Gerät. Die Ursache des Bootabbruchs und des beobachteten Rahmenblinkens ist weiterhin nicht bewiesen.
