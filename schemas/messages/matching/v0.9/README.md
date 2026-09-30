# MATCHING Message v0.9

## 1. Purpose

The `MATCHING` message is used to exchange nomination data between matching partners for a specific network location. Matching partners use the data to compare nominations and determine the confirmed quantities for each account pair, time interval and flow direction. 

The message supports two subtypes:

- `Request`
- `Response`

## 2. Message Subtypes

The `MATCHING` message supports three subtypes:

| Subtype | Data flow | Description |
|---|---|---|
| `Request` | Initiating matching partner → Counterpart matching partner | Sends the initiating partner’s matching data and requests the counterpart partner to perform matching. |
| `Response` | Counterpart matching partner → Initiating matching partner | Returns the counterpart’s matching data and, where applicable, the matching result and confirmed quantities. |

The sender and recipient are the matching partners responsible for the relevant network location. 

### `Request`

The `Request` subtype is used by the initiating matching partner to send its matching data to the counterpart matching partner and request a matching process. The request may contain the quantities processed internally by the initiating matching partner. 

### `Response`

The `Response` subtype is used by the counterpart matching partner to return its matching data to the initiating matching partner. Where applicable, the response also contains the matching result and confirmed quantities. 

## 3. Message Structure

The `MATCHING` message consists of the following top-level objects:

- `message`
- `parties`
- `location`
- `matchingData`

### `message`

The `message` object contains technical message metadata.

Every `MATCHING` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `MATCHING` |
| `subType` | `Request` or `Response` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

For the `MATCHING` message format, both `sender` and `recipient` must have the role:

- `HydrogenGridOperator`

The common technical properties of `parties` are defined in the shared schemas.


### `matchingData`

The `matchingData` object defines the context for the matching data transmitted in the message.

| Property | Description |
|---|---|
| `period` | Period covered by the matching data. |
| `granularity` | Time-series granularity; currently `PT1H`. |
| `unit` | Unit of the quantities; currently `kWh`. |
| `location` | Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `accountSpecificData` | One or more blocks of matching data grouped by account pair. |

#### `accountSpecificData`

Each object in `accountSpecificData` represents matching data for one internal account and one external account.

| Property | Description |
|---|---|
| `internalAccount` | Internal account or balancing group identifier. |
| `externalAccount` | External account or balancing group identifier. |
| `timeSeries` | One or more time series used in the matching process. |

#### `timeSeries`

Each object in `timeSeries` represents one quantity type for the specified account pair and matching period.

| Property | Description |
|---|---|
| `quantityType` | Type of quantity represented by the time series. |
| `values` | Ordered time series of values for the specified quantity type. |

The supported `quantityType` values are:

| `quantityType` | Description |
|---|---|
| `RequestedQuantity` | Quantity requested by the matching partner. |
| `InternallyProcessedQuantity` | Quantity processed internally by the sender. |
| `InternallyProcessedQuantityCounterpart` | Quantity processed internally by the counterpart matching partner. |
| `ConfirmedQuantity` | Quantity confirmed as the result of the matching process. |

#### `values`

Each time-series value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Quantity for the interval, expressed in the unit declared in `matchingData.unit`. |
| `flowDirection` | Direction of the quantity for the interval. |

The values must be provided in chronological order and correspond to the declared period and granularity.

The duration of each interval is defined by `matchingData.granularity`. For example, with a granularity of `PT1H`, the timestamp `2026-10-24T22:00:00Z` represents the interval from `2026-10-24T22:00:00Z` to `2026-10-24T23:00:00Z`.

## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/matching/v0.9/
  README.md
  matching-message-base.schema.json
  components/
    matching-data.schema.json
    matching-account-specific-data.schema.json
    matching-time-series.schema.json
  request/
    request-matching-message.schema.json
  response/
    response-matching-message.schema.json
```
