# Raspi-Scripte 1.0.8

Version 1.0.8 · Build 1

Zeitprüfung bei Installation und Update
- Drei Möglichkeiten bei abweichenden Zeiten: Zeit abgleichen und fortfahren; ohne Zeitabgleich fortfahren; abbrechen. Ohne Zeitabgleich wird das Update mit den vorhandenen Zeiten versucht. Die feste Zeitzone bleibt erhalten.

Allsky: Aufnahmetag und feste Zeitzone
- Ganz oben auf Allsky - Setup stehen zwei getrennte Zeilen mit Button und aktuellem Status, auf Deutsch und Englisch.
- Optional alle neuen Aufnahmen nach der Mittagsgrenze 12:00 zuordnen. Morgenaufnahmen vor 12:00 gehören dadurch zum Ordner des Vortags. Ausschalten stellt die bisherige Allsky-Zuordnung wieder her. Vorhandene Dateien werden nicht verändert.
- Optional den bereits auf der Witty-Homepage gewählten festen UTC-Offset für den Allsky-Aufnahmeprozess übernehmen, etwa UTC+10:00 ohne Sommer-/Winterzeit. Ausschalten verwendet wieder die Systemzeitzone. Ein geänderter Witty-Offset kann erneut übernommen werden.
- Laufende Allsky-Dienste werden zur Übernahme kurz neu gestartet; gestoppte Dienste bleiben gestoppt. Bei einem fehlgeschlagenen Neustart werden die vorherigen Einstellungen wiederhergestellt. Die Mittagsanpassung wird nach Allsky-Updates beim Dienststart erneut angewendet; unbekannte Quellformate werden nicht blind verändert.
- Keine Änderung an GPS-Zugriff, WURB, WIRC, Systemzeit, RTC oder echten Standortkoordinaten. Eine Änderung der Längengrade als Zeitzonen-Umgehung wird nicht vorgenommen.

Prüfung
- Automatisierte Tests für Mittags-/Monats-/Jahres-/Schaltjahresgrenzen, feste positive und negative UTC-Offsets, Rücknahme nach Fehlern und Deutsch/Englisch im Browser. Windows-Anwendung und Updater lokal gebaut. Physischer Raspberry-Pi-Test steht noch aus.
