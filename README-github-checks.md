# GitHub Checks for JSON and JSON Schemas

This package adds GitHub Actions checks to a repository for:

- valid JSON syntax in all `*.json` files
- detection of duplicate JSON keys
- JSON Schema self-validation
- local `$ref` resolution without remote fetching
- positive and negative example validation via `validation/validation-manifest.yml`
- automatic validation of JSON files with a local `$schema` reference

## Installation

Unpack and commit into the target repository:

```bash
unzip h2-market-message-github-checks.zip -d .
git add .github/workflows/validate-json-and-schemas.yml tools/validate_json_schemas.py validation/validation-manifest.yml requirements-dev.txt
git commit -m "ci: validate JSON messages and schemas"
git push
```

## Local testing

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml
```

## Manifest example

```yaml
validations:
  - schema: schemas/preliminaryMeasurementMessage.schema.json
    valid:
      - examples/preliminaryMeasurement/valid/*.json
    invalid:
      - examples/preliminaryMeasurement/invalid/*.json
```

Recommended folder structure:

```text
schemas/
  preliminaryMeasurementMessage.schema.json
examples/
  preliminaryMeasurement/
    valid/
      valid-message.json
    invalid/
      missing-sender.json
validation/
  validation-manifest.yml
```