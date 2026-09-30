# H2 Market Message Specifications v0.9

This repository contains JSON Schemas, examples and validation rules for hydrogen market messages.

The repository is intentionally organization- and repository-agnostic: it does not contain a hard-coded GitHub organization or repository URL.

For the **English and German terminology**, see `H2MarketMessageTerminologyEnglishGerman.md`.

## Published Message Formats in this Repository

| Message | Version | Subtypes | Purpose |
|---|---:|---|---|
| `ALLOCATION` | `0.9` | `Nomination`, `QuantityDeclaration`, `Measurement` | Transmission of allocation data for nominations, quantity declarations and allocated measurements. |
| `BALANCING` | `0.9` | `ContinuousBalancing`, `DifferenceQuantities` | Transmission of balancing figures for continuous balancing and the post-monthly balancing mechanism. |
| `BALANCINGGROUPLIST` | `0.9` | `Default` |	Transmission of balancing group information from the WMGV to WNBs. |
| `MATCHING` | `0.9` | `Request`, `Response` | 	Transmission of matching requests and results as part of physical nominations. |
| `MEASUREMENT` | `0.9` | `Preliminary`, `Final` | 	Transmission of (non-allocated) measurement data. |
| `NOMINATION` | `0.9` | `Physical`, `VTP` | Submission of nominations to the WMGV at the VHP or to a WNB. |
| `NOMINATIONRESPONSE` | `0.9` | `Physical`, `VTP` | 	Transmission of responses to or confirmations of nominations from the WMGV or a WNB to the BKV. |
| `QUANTITYDECLARATION` | `0.9` | `Default` | Submission of quantity declarations to a WNB. |
| `QUANTITYDECLARATIONRESPONSE` | `0.9` | `Default` | 	Transmits responses to or confirmations of quantity declarations from a WNB to the BKV. |


## Repository Structure and Architecture

```text
schemas/
  _shared/
  messages/
    message-type/
      version/
        type-message-base.schema.json
        components/
        message-subtype/
          type-subtype-message.schema.json
examples/
  messages/
    message-type/
      version/
        message-subtype/
          valid-example.valid.json
          invalid/
            invalid-example.invalid-message.json
catalog/
  message-catalog.json
```

Reusable components shared by multiple message types are stored in schemas/_shared/.
Each message-type directory contains the message’s base schema and a concise README. It also contains the following subdirectories:

### `components`
Contains components used by this message type that are not general-purpose shared components.

### One directory per message subtype
Contains the JSON Schema for the relevant message subtype, including any subtype-specific constraints. Examples include:

message.subType must be Preliminary or Final.
measurements[ ].granularity must be PT15M or PT1H.


## Message Format Documentation

The repository contains format-specific READMEs, JSON Schemas and examples in the following locations:

- Format-specific README: schemas/messages/`<message-type>`/`<version>`/README.md
- Message-type base schema: schemas/messages/`<message-type>`/`<version>`/`<message-type>-message-base.schema.json
- Message-specific components: schemas/messages/`<message-type>`/`<version>`/components/
- Subtype schemas: schemas/messages/`<message-type>`/`<version>`/`<message-subtype>`/
- Valid examples: examples/messages/`<message-type>`/`<version>`/`<message-subtype>`/
- Invalid examples: examples/messages/`<message-type>`/`<version>`/`<message-subtype>`/invalid/
- Shared schemas used by multiple message types: schemas/_shared/


Replace `<message-type>`, `<version>` and `<message-subtype>` with the corresponding directory names.

## Use of AI

Codex AI assisted with the creation and maintenance of this repository.

## Validation

Validation is performed by two checks in GitHub Actions. Once the workflow file is on the default branch, these checks run for subsequent pushes, pull requests, merge queue runs and manual `workflow_dispatch` runs:

- `Repository standards`: Checks JSON syntax, JSON Schema standards, local references, declared `$schema` references, and catalog schema and example references.
- `Message examples`: Validates positive and negative examples against the appropriate message schemas and checks that the manifest covers catalog examples.
The same checks can be run locally. You may first install `jsonschema`, `referencing` and `PyYAML` from `requirements-dev.txt`. If these packages are not installed, the validator uses a built-in fallback validator for the schema keywords used in this repository.

```powershell
python -m pip install -r requirements-dev.txt
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --standards-only
python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --examples-only --require-manifest
```

## Naming Conventions

| Category | Rule | Example |
|---|---|---|
| JSON fields | JSON field names **SHOULD** use `lowerCamelCase`. | `"partnerRole"`: "HydrogenGridOperator" |
| Message Type and Subtype | Message types **MUST** always be written in `UPPERCASE`.<br>The message subtype **MUST** be written in `PascalCase`. | `{"type": "MEASUREMENT", "subType": "Preliminary"}` |
| Domain-Specific Enum and Constant Values | Custom domain-specific string values **SHOULD** be written in `PascalCase`. | "partnerRole": `"HydrogenGridOperator"` |
| Status and Quality | Custom domain-specific string values used for `status` and `quality` **SHOULD** be written in `camelCase`. | `"quality": "preliminary"` |
| Technical and External Codes | Technical, external, or standardized codes **MUST** remain unchanged. | - Time intervals: `PT15M`, `PT1H`<br>- Units: `kWh`<br>- UUIDs<br>- Timestamps in RFC 3339 / JSON Schema<br>- `date-time` format |
| Domain-Specific Codes and IDs | Domain-specific codes and identifiers **MUST** be represented exactly as defined by their source or domain. Do not change their casing, formatting, or structure. | - Internal account codes and IDs<br>- External account codes and IDs<br>- Location codes |


## Timestamps and Timeseries Periods

All timestamps must be provided as **UTC date-time values in ISO 8601 format**. <br>A timestamp identifying the beginning of an interval is therefore expressed in UTC, even when the interval is defined according to local time.


For timeseries data, `P1D` represents *one complete local calendar day* in the `Europe/Berlin` time zone. `P1D` is a calendar period and **MUST NOT** be interpreted as a fixed 24-hour elapsed duration. Consequently, the elapsed duration of a `P1D` period may be 23, 24 or 25 hours due to daylight-saving time changes.

The period 
- begins at *00:00:00 local time* and 
- ends at *00:00:00 on the following local calendar day*. 

The `Europe/Berlin` time zone observes daylight-saving time:
- During standard time (**CET**), the local time offset is **UTC+01:00**.
- During daylight-saving time (**CEST**), the local time offset is **UTC+02:00**.

The applicable offset depends on the date. Use the `Europe/Berlin` time zone to determine it rather than applying a fixed UTC offset. For example, local midnight in Berlin corresponds to `23:00:00Z` on the previous day during CET and `22:00:00Z` on the previous day during CEST.

Because of the **daylight-saving time changes**, the absolute duration of a `P1D` period may be 23, 24 or 25 hours. The start and derived end timestamps are expressed in UTC.


## Daily Period Examples with Hourly Granularity

Each period represents one complete local calendar day in the `Europe/Berlin` time zone. The timestamps below are the start times of `PT1H` intervals. Local timestamps include the applicable UTC offset: `+01:00` for CET and `+02:00` for CEST. Ellipses (`…`) indicate omitted intervals.

### 11 November 2025 - CET (UTC+01:00)

**Period:** `2025-11-10T23:00:00Z/P1D` · **Granularity:** `PT1H` · **Duration:** `24 hours`

| UTC timestamp | Local timestamp (CET) |
|---|---|
| `2025-11-10T23:00:00Z` | `2025-11-11T00:00:00+01:00` |
| `2025-11-11T00:00:00Z` | `2025-11-11T01:00:00+01:00` |
| `2025-11-11T01:00:00Z` | `2025-11-11T02:00:00+01:00` |
| … | … |
| `2025-11-11T11:00:00Z` | `2025-11-11T12:00:00+01:00` |
| … | … |
| `2025-11-11T20:00:00Z` | `2025-11-11T21:00:00+01:00` |
| `2025-11-11T21:00:00Z` | `2025-11-11T22:00:00+01:00` |
| `2025-11-11T22:00:00Z` | `2025-11-11T23:00:00+01:00` |

### 13 June 2025 - CEST (UTC+02:00)

**Period:** `2025-06-12T22:00:00Z/P1D` · **Granularity:** `PT1H` · **Duration:** `24 hours`

| UTC timestamp | Local timestamp (CEST) |
|---|---|
| `2025-06-12T22:00:00Z` | `2025-06-13T00:00:00+02:00` |
| `2025-06-12T23:00:00Z` | `2025-06-13T01:00:00+02:00` |
| `2025-06-13T00:00:00Z` | `2025-06-13T02:00:00+02:00` |
| … | … |
| `2025-06-13T10:00:00Z` | `2025-06-13T12:00:00+02:00` |
| … | … |
| `2025-06-13T19:00:00Z` | `2025-06-13T21:00:00+02:00` |
| `2025-06-13T20:00:00Z` | `2025-06-13T22:00:00+02:00` |
| `2025-06-13T21:00:00Z` | `2025-06-13T23:00:00+02:00` |


### 30 March 2025 - Start of Daylight-Saving Time (CET to CEST)

The local clock jumps forward from `01:59:59+01:00` to `03:00:00+02:00`. The day lasts 23 hours.

**Period:** `2025-03-29T23:00:00Z/P1D` · **Granularity:** `PT1H` · **Duration:** `23 hours`

| UTC timestamp | Local timestamp (CET/CEST) |
|---|---|
| `2025-03-29T23:00:00Z` | `2025-03-30T00:00:00+01:00` |
| `2025-03-30T00:00:00Z` | `2025-03-30T01:00:00+01:00` |
| `2025-03-30T01:00:00Z` | `2025-03-30T03:00:00+02:00` |
| `2025-03-30T02:00:00Z` | `2025-03-30T04:00:00+02:00` |
| `2025-03-30T03:00:00Z` | `2025-03-30T05:00:00+02:00` |
| … | … |
| `2025-03-30T11:00:00Z` | `2025-03-30T13:00:00+02:00` |
| … | … |
| `2025-03-30T19:00:00Z` | `2025-03-30T21:00:00+02:00` |
| `2025-03-30T20:00:00Z` | `2025-03-30T22:00:00+02:00` |
| `2025-03-30T21:00:00Z` | `2025-03-30T23:00:00+02:00` |

### 26 October 2025 - End of Daylight-Saving Time (CEST to CET)

The local hour from `02:00:00` to `02:59:59` occurs twice: first with offset `+02:00`, then with offset `+01:00`. The day lasts 25 hours.

**Period:** `2025-10-25T22:00:00Z/P1D` · **Granularity:** `PT1H` · **Duration:** `25 hours`

| UTC timestamp | Local timestamp (CEST/CET) |
|---|---|
| `2025-10-25T22:00:00Z` | `2025-10-26T00:00:00+02:00` |
| `2025-10-25T23:00:00Z` | `2025-10-26T01:00:00+02:00` |
| `2025-10-26T00:00:00Z` | `2025-10-26T02:00:00+02:00` |
| `2025-10-26T01:00:00Z` | `2025-10-26T02:00:00+01:00` |
| `2025-10-26T02:00:00Z` | `2025-10-26T03:00:00+01:00` |
| … | … |
| `2025-10-26T10:00:00Z` | `2025-10-26T11:00:00+01:00` |
| … | … |
| `2025-10-26T20:00:00Z` | `2025-10-26T21:00:00+01:00` |
| `2025-10-26T21:00:00Z` | `2025-10-26T22:00:00+01:00` |
| `2025-10-26T22:00:00Z` | `2025-10-26T23:00:00+01:00` |

All UTC timestamps are the start times of hourly intervals. The local timestamps show the corresponding time in `Europe/Berlin`, including the applicable offset.
