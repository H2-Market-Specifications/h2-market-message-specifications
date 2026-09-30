# Neue Nachricht hinzufügen

1. Neuen Ordner anlegen:

```text
schemas/messages/<messagetype-name>/v0.9/<messagesubtype-name>
examples/messages/<messagetype-name>/v0.9/<messagesubtype-name>
```

2. Ein Root-Schema erstellen:

```text
schemas/messages/<messagetype-name>/v0.9/<message-name>-message-base.schema.json
```

3. Schema für den messagesubtype erstellen:

```text
schemas/messages/<messagetype-name>/v0.9/<messagesubtype-name>/<messagesubtype-name>-message.schema.json
```

4. Schemata für nachrichtenspezifische Komponenten erstellen:

```text
schemas/messages/<messagetype-name>/v0.9/components/component.schema.json
```

5. Keine generischen Bausteine kopieren.

Nutze stattdessen direkte Referenzen auf:

- `schemas/_shared/message.schema.json`
- `schemas/_shared/measurement.schema.json`
- `schemas/_shared/measurements.schema.json`
- `schemas/_shared/parties.schema.json`
- `schemas/_shared/location.schema.json`

6. Nachricht im Katalog ergänzen:

```text
catalog/message-catalog.json
```

7. Validieren:

```powershell
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --require-manifest
```
