# NOMINATIONRESPONSE Message v0.9

## 1. Purpose

The `NOMINATIONRESPONSE` message is used to transmit the result of processing a nomination to the responsible Balancing Group Responsible Party (`BKV`).

It contains the quantities processed by the sender and, where applicable, by the counterpart, as well as the quantity confirmed after processing or matching.

The message supports two subtypes:

- `Physical`
- `VTP`

## 2. Message Subtypes

| Subtype | Data flow | Description |
|---|---|---|
| `Physical` | `WNB` → `BKV` | Transmission of the processed quantities and matching result for a physical nomination. |
| `VTP` | `WMGV` → `BKV` | Transmission of the  processed quantities and matching result for a VTP nomination. |

### `Physical`

The `Physical` subtype is used to respond to physical nominations at nomination-dependent network points. The WNB processes the nomination and, where applicable, matches its internally processed quantity with the quantity processed by the counterpart. 

The response may contain the quantity requested by the BKV, the quantity processed by the sender, the quantity processed by the counterpart and the confirmed quantity.

### `VTP`

The `VTP` subtype is used to respond to nominations at the Virtual Trading Point (`VHP`). The WMGV matches the submitted VTP nominations and communicates the result to the relevant BKV. 

The response may contain the quantity requested by the BKV, the quantity processed by the WMGV, the quantity processed by the counterpart and the confirmed quantity.

## 3. Message Structure

The `NOMINATIONRESPONSE` message consists of the following top-level objects:

- `message`
- `parties`
- `nominationResponseData`

### `message`

The `message` object contains technical message metadata.

Every `NOMINATIONRESPONSE` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `NOMINATIONRESPONSE` |
| `subType` | `Physical` or `VTP` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

The typical partner roles for each subtype are:

| Subtype | Property | Allowed value(s) |
|---|---|---|
| `Physical` | `sender.partnerRole` | `HydrogenGridOperator` |
| `Physical` | `recipient.partnerRole` | `BalancingGroupResponsibleParty` |
| `VTP` | `sender.partnerRole` | `HydrogenMarketAreaManager` |
| `VTP` | `recipient.partnerRole` | `BalancingGroupResponsibleParty` |

The common technical properties of `parties` are defined in the shared schemas.

### `nominationResponseData`

The `nominationResponseData` object defines the context for the nomination response.

| Property | Description |
|---|---|
| `location` | Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `period` | Period covered by the response. |
| `granularity` | Time-series granularity; currently `PT1H`. |
| `unit` | Unit of the response quantities; typically `kWh`. |
| `internalAccount` | Internal identifier of the balancing group. |
| `nominationResponses` | One or more response entries containing account-specific response data. |

For physical responses, `location` identifies the relevant nomination-dependent network point. For VTP responses, it identifies the VHP.


#### `nominationResponses`

Each object in `nominationResponses` represents a response for one external account or counterpart.

| Property | Description |
|---|---|
| `externalAccount` | External account, balancing group or counterpart identifier, as applicable to the subtype. |
| `timeSeries` | One or more response time series for the account or counterpart. |

#### `timeSeries`

Each object in `timeSeries` represents one quantity type for the specified account pair and response period.

| Property | Description |
|---|---|
| `quantityType` | Type of quantity represented by the time series. |
| `values` | Ordered series of values for the specified quantity type. |

The supported `quantityType` values are:

| `quantityType` | Description |
|---|---|
| `RequestedQuantity` | Quantity originally requested by the BKV or matching partner. |
| `InternallyProcessedQuantity` | Quantity processed internally by the sender. |
| `InternallyProcessedQuantityCounterpart` | Quantity processed internally by the counterpart. |
| `ConfirmedQuantity` | Quantity confirmed after processing or matching. |

#### `values`

`values` is an ordered time series containing values for the intervals covered by the response.

Each value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Quantity for the interval, expressed in the unit declared in `nominationResponseData.unit`. |
| `flowDirection` | Direction of the nominated or confirmed flow for the interval. |

The values must be provided in chronological order and correspond to the declared period and granularity.

The duration of each interval is defined by `nominationResponseData.granularity`. For example, with a granularity of `PT1H`, the timestamp `2026-03-21T23:00:00Z` represents the interval from `2026-03-21T23:00:00Z` to `2026-03-22T00:00:00Z`.

Quality and status values are not used in the nomination response time series.


## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/nominationresponse/v0.9/
  README.md
  nomination-response-message-base.schema.json
  components/
    nomination-response-data.schema.json
    nomination-response.schema.json
    nomination-response-time-series.schema.json
  physical/
    physical-nominationresponse-message.schema.json
  vtp/
    vtp-nominationresponse-message.schema.json
```
