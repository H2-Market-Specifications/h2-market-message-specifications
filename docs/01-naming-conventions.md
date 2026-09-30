# Naming Convention

This convention defines how JSON fields, message types, and domain-specific values should be named.

## JSON Fields

JSON fields **SHOULD** use `lowerCamelCase`.

```json
{
  "partnerRole": "HydrogenGridOperator",
  "locationType": "MarketLocation",
  "quantityType": "EnergyH2"
}
```

## Message Type and Subtype

Message types **MUST** always be written in `UPPERCASE`. The message subtype **MUST** be written in `PascalCase`.

```json
{
  "type": "MEASUREMENT",
  "subType": "Preliminary"
}
```

## Domain-Specific Enum and Constant Values

Custom domain-specific string values **SHOULD** be written in `PascalCase`.

```json
{
  "partnerRole": "HydrogenGridOperator",
  "locationType": "MarketLocation",
  "quantityType": "EnergyH2"
}
```

## Status and Quality

Custom domain-specific string values used for `status` and `quality` **SHOULD** be written in `camelCase`.

```json
{
  "quality": "preliminary",
  "status": "measured"
}
```

## Technical and External Codes

Technical, external, or standardized codes **MUST** remain unchanged.

Examples:

- Time intervals such as `PT15M` and `PT1H`
- Units such as `kWh`
- Standardized values such as `molPercent`
- 13-digit partner codes
- UUIDs
- Timestamps in RFC 3339 / JSON Schema `date-time` format

## Domain-Specific Codes and IDs

Domain-specific codes and identifiers **MUST** be represented exactly as defined by their source or domain. Do not change their casing, formatting, or structure.

Examples include:

- Internal account codes and IDs
- External account codes and IDs
- Location codes
- Cluster IDs
- Other business-specific codes or identifiers
