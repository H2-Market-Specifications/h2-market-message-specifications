# Validierung unter Windows

## Voraussetzung

Python 3 installieren.

## Optionale Zusatzpakete

Der Validator läuft ohne externe Pakete mit einer eingebauten Fallback-Validierung. Für strengere JSON-Schema- und YAML-Prüfung können optional die Entwicklungsabhängigkeiten installiert werden:

```powershell
python -m pip install -r requirements-dev.txt
```

## Alles prüfen

```powershell
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --require-manifest
```

## Was wird geprüft?

- JSON-Syntax aller `*.json` Dateien ohne `node_modules/`.
- Doppelte JSON-Keys.
- JSON-Schema-Selbstvalidierung; mit optional installiertem `jsonschema` gegen den passenden JSON-Schema-Draft.
- Lokale `$ref`-Auflösung ohne Remote-Fetch.
- Valide und invalide Beispiele aus `validation/validation-manifest.yml`.
- JSON-Dateien mit lokal auflösbarem `$schema`-Verweis.

## Windows-Hinweis zu `$ref`

In JSON Schema werden Pfade und URIs immer mit `/` geschrieben, nicht mit `\`.

Richtig:

```json
{
  "$ref": "https://h2-market.example/message-specifications/schemas/_shared/v0.9/market-partner.schema.json"
}
```

Falsch:

```json
{
  "$ref": "schemas\_shared\market-partner.schema.json"
}
```
