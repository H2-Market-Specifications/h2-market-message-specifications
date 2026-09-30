# Repository Structure

Die Struktur trennt strikt zwischen wiederverwendbaren Shared-Schemas und konkreten Nachrichten.

```text
schemas/
  _shared/
    message.schema.json
    time-series-value.schema.json
    market-partner.schema.json
    location.schema.json
  messages/
    <message-name>/
      v<major.minor>/
        <message-name>-message-base.schema.json
        README.md
        subtype1/
          <messagesubtype-name>-message.schema.json
        components/
          component1.schema.json
```

## Regel

Nachrichtenordner enthalten keine Kopien generischer Bausteine wie `message.schema.json`.

Das Root-Schema einer Nachricht referenziert die Shared-Schemas. Das Schema eines Subtypes einer Nachricht fügt nur die fachlich notwendigen Spezialisierungen inline hinzu, zum Beispiel `message.subType` oder `measurements[].granularity`.
