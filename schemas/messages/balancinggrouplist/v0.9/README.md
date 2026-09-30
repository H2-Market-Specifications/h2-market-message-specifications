# BALANCINGGROUPLIST Message v0.9

## 1. Purpose

The `BALANCINGGROUPLIST` message is used by the Hydrogen Market Area Manager (`WMGV`) to provide Hydrogen Grid Operators (`WNB`) with the current list of valid balancing groups. 

The message contains the balancing group identifier, its assigned cluster and validity period, and information about the responsible market partner, including that partner’s validity period. 


## 2. Message Subtypes

The `BALANCINGGROUPLIST` message supports only the default subtype:

| Subtype | Data flow | Description |
|---|---|---|
| `Default` | `WMGV` → `WNB` | Transmission of the current balancing group list, including newly created balancing groups and changes to existing balancing group data. |


## 3. Message Structure

The `BALANCINGGROUPLIST` message consists of the following top-level objects:

- `message`
- `parties`
- `balancingGroupList`

### `message`

The `message` object contains technical message metadata.

Every `BALANCINGGROUPLIST` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `BALANCINGGROUPLIST` |
| `subType` | `Default` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

`BALANCINGGROUPLIST`-specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | `HydrogenMarketAreaManager` |
| `recipient.partnerRole` | `HydrogenGridOperator` |

The common technical properties of `parties` are defined in the shared schemas.

### `balancingGroupList`

The `balancingGroupList` property contains one or more balancing group entries.

Each entry describes a balancing group, its assigned cluster, its validity period and its responsible market partner. 

| Property | Description |
|---|---|
| `internalAccount` | Internal identifier of the balancing group. |
| `clusterId` | Unique identifier (name or ID) of the cluster assigned to the balancing group. |
| `from` | Start of the balancing group’s validity period. |
| `to` | End of the balancing group’s validity period. |
| `marketPartner` | Information about the market partner responsible for the balancing group. |

#### `marketPartner`

The `marketPartner` object contains information about the market partner responsible for the balancing group.

| Property | Description |
|---|---|
| `marketPartnerCode` | Identifier of the market partner. |
| `marketPartnerName` | Name of the market partner. |
| `marketPartnerFrom` | Start of the market partner’s validity period. |
| `marketPartnerTo` | End of the market partner’s validity period. |

All date-time values must be provided in UTC using ISO 8601 date-time notation.

## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/balancinggrouplist/v0.9/
  README.md
  balancinggrouplist-message-base.schema.json
  components/
    balancinggrouplist-entry.schema.json
    operating-market-partner.schema.json
  Default/
    Default-balancinggrouplist-message.schema.json
```
