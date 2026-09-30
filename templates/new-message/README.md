# Vorlage: neue Nachricht

Beim Anlegen einer neuen Nachricht diese Struktur verwenden:

```text
schemas/messages/<message-id>/v0.9/
├─ README.md
└─ <message-id>-message.schema.json

examples/messages/<message-id>/v0.9/
└─ <MESSAGE_ID>.valid.json
```

Danach `catalog/message-catalog.json` erweitern und lokal validieren:

```powershell
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --require-manifest
```

Empfohlene `message-id`:

- Englisch,
- fachlich eindeutig,
- kebab-case,
- ohne Versionsnummer.

Beispiele:

- `preliminary-measurement`
- `final-measurement`
- `nomination`
- `balancing-statement`
