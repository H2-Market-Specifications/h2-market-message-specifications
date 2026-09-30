# Changelog

## 0.6.0

 - Ordner Struktur angepasst
 - Bausteine, die nur für einen einzigen Nachrichtentyp genutzt werden, befinden sich jetzt in einem eigenen Ordner "components" pro Nachrichtentyp.


## 0.5.0

- Redundante nachrichtenspezifische `message.schema.json`, `measurement.schema.json` und `measurements.schema.json` entfernt.
- Identische Parteien-Schemas aus den Nachrichtenordnern entfernt.
- Wiederverwendbare Bausteine konsequent unter `schemas/_shared/` zentralisiert.
- Nachrichtenspezifische Constraints werden jetzt direkt in den Root-Schemas verdrahtet.
- Vorläufige und finale Messwertnachricht verwenden dieselbe Root-Struktur: `message`, `parties`, `location`, `measurements`.

## 0.4.0

- Vorläufige Messwerte auf die gemeinsame `measurements[]`-Struktur umgestellt.
- Finale Messwerte ergänzt.

## 0.1.0

- Initiale Repository-Struktur für H2-Marktnachrichten.
