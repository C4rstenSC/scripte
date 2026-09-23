# Raspi-Scripte 0.6.22

- Ohne Witty-Hardware werden die Witty-Hardware- und Herstellerzeilen
  ausgeblendet; Betriebssystem und Witty Addon Script bleiben sichtbar.
- Sicheres Herunterfahren nutzt ohne Witty den Linux-Poweroff-Pfad und weist
  auf das anschließende manuelle Einschalten hin.
- Enthält Witty Add-on 0.6.30 mit repariertem Backend-Dispatcher, sichtbarer
  USB-GPS-Auswahl und ausgeblendeter Next-Shutdown-Anzeige ohne Witty-Platine.

- Die Überschrift des einklappbaren Bereichs heißt wieder „SSH Terminal“ und
  zeigt nicht mehr `System.Windows.Controls.StackPanel` an.
- Das Terminal startet eingeklappt und bleibt auch beim normalen Verbinden
  geschlossen, bis es manuell geöffnet wird.
- Bei Installationen und Software-Updates wird es automatisch ausgeklappt und
  fokussiert.

- Raspberry-Modell, Neustart und sicheres Herunterfahren stehen gemeinsam in
  einer Zeile; Witty-Hardware und Firmware folgen direkt darunter.
- Das Betriebssystem besitzt oberhalb des Witty Addon Script eine eigene
  gerahmte Zeile mit Versionsinformationen, Linux-Update und Release Notes.
- Release-Notes-Knöpfe springen zuverlässig zum richtigen Abschnitt.
- Anleitung und Änderungsbeschreibungen lassen sich markieren und kopieren.
- Enthält Witty Add-on 0.6.27 mit der verpflichtenden Add-on-Homepage für
  Raspberry Pi 4 auch ohne Witty-Platine und der Migration alter
  Installationen ohne `/etc/witty-addon.conf`.
