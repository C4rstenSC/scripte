# Witty Add-on 0.6.55

Release: 07.10.2026

Witty Add-on 0.6.55 – 06.10.2026
=================================

- GPS-Hintergrundabfragen blockieren die gemeinsame Witty-Hardwaresperre nicht mehr. GPS wartet unabhängig auf einen aktuellen Fix; Witty-Bedienung und Seitenstart bleiben verfügbar.
- Die schnelle Startabfrage wartet auch auf Raspberry Pi 4 und Witty Pi 4 nicht auf GPS. Die bestehende parallele GPS-Nutzung durch WURB und Witty bleibt erhalten.

- Die hwclock-Paketinstallation erhält zehn Minuten für die abschließende Paketverarbeitung. Zeitüberschreitungen und APT-/dpkg-Fehler nennen nun den tatsächlichen Abbruchgrund; Signaturfehler in den Paketlisten stoppen mit einem Hinweis zur Systemzeit.
