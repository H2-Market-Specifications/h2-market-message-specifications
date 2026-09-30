# NOMINATION Message v0.9

## 1. Purpose

The `NOMINATION` message is used to transmit planned hydrogen quantities for nomination-dependent network points and for transfers between balancing groups at the Virtual Trading Point (`VTP`). 

The message supports two subtypes:

- `Physical`
- `VTP`

## 2. Message Subtypes

| Subtype | Data flow | Description |
|---|---|---|
| `Physical` | `BKV` → `WNB` | Submission of physical nominations for nomination-dependent network points. |
| `VTP` | `BKV` → `WMGV` | Submission of VTP nominations to transfer quantities between balancing groups. |

### `Physical`

The `Physical` subtype is used by the BKV to nominate the intended use of booked entry or exit capacity at nomination-dependent points. 

Physical nominations apply to border crossing points, storage connection points and entry points from hydrogen terminals. 

Physical nominations are generally submitted as Double Sided Nominations (`DSN`) and are matched with the corresponding nomination submitted to the matching partner. 

The WNB transfers the relevant confirmed nomination quantities to the WMGV for balancing and forecasting purposes. 

### `VTP`

The `VTP` subtype is used to submit nominations for virtual transfers between balancing groups at the VTP. 

VTP nominations are generally submitted as Double Sided Nominations (`DSN`); Single Sided Nominations (`SSN`) may be used where permitted by the applicable contractual or process rules. 

## 3. Message Structure

The `NOMINATION` message consists of the following top-level objects:

- `message`
- `parties`
- `nominationData`

### `message`

The `message` object contains technical message metadata.

Every `NOMINATION` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `NOMINATION` |
| `subType` | `Physical` or `VTP` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

The typical partner roles for each subtype are:

| Subtype | Party | Allowed role |
|---|---|---|
| `Physical` | `sender.partnerRole` | `BalancingGroupResponsibleParty` |
| `Physical` | `recipient.partnerRole` | `HydrogenGridOperator` |
| `VTP` | `sender.partnerRole` | `BalancingGroupResponsibleParty` or `HydrogenMarketAreaManager` |
| `VTP` | `recipient.partnerRole` | `HydrogenMarketAreaManager` |

The common technical properties of `parties` are defined in the shared schemas.

### `nominationData`

The `nominationData` object defines the context for the nomination data transmitted in the message.

| Property | Description |
|---|---|
| `location` |  Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `internalAccount` | Internal identifier of the balancing group. |
| `period` | Period covered by the nomination. |
| `granularity` | Time-series granularity; currently `PT1H`. |
| `unit` | Unit of the nomination quantities; typically `kWh`. |
| `nominations` | One or more nomination blocks containing the nomination data. |

Physical nominations are direction-specific and are submitted for a network point and balancing group. 

For physical nominations, the `location` identifies the nomination-dependent network point. 

For VTP nominations, the `location` identifies the VTP. 

The `location` property uses the shared `location` schema.

#### `nominations`

Each object in `nominations` contains the external account or counterpart identifier and the corresponding nomination values.

| Property | Description |
|---|---|
| `externalAccount` | External account, balancing group or counterpart identifier, as applicable to the subtype. |
| `values` | Ordered time series of nomination values for the relevant account or counterpart. |

#### `values`

`values` uses the shared time-series-value schema. It is an ordered time series containing one value for each consecutive interval covered by the nomination block.

Each value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Nomination quantity for the interval, expressed in the unit declared in `nominationData.unit`. |
| `flowDirection` | Direction of the nominated flow. |

The values must be provided in chronological order and correspond to the declared period and granularity.

The duration of each interval is defined by `nominationData.granularity`. For example, with a granularity of `PT1H`, the timestamp `2026-03-21T23:00:00Z` represents the interval from `2026-03-21T23:00:00Z` to `2026-03-22T00:00:00Z`.

Nomination values are non-negative whole numbers; the flow direction is specified separately. 

Physical nominations are submitted for a complete calendar day, with the number of hourly values adjusted for daylight-saving-time changes. 

Quantity declarations are submitted for a complete calendar day as direction-specific, non-negative whole-number hourly values in `kWh/h`, or as `0`, with the number of hourly values adjusted for daylight-saving-time changes. 


## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/nomination/v0.9/
  README.md
  nomination-message-base.schema.json
  components/
    nomination-data.schema.json
    nomination.schema.json
  physical/
    physical-nomination-message.schema.json
  vtp/
    vtp-nomination-message.schema.json
```
