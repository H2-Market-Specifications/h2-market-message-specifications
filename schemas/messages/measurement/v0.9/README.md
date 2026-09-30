# MEASUREMENT Message v0.9

## 1. Purpose

The `MEASUREMENT` message is used by Hydrogen Grid Operators (`WNB`) to transmit measured hydrogen quantities to the Hydrogen Market Area Manager (`WMGV`) and, where applicable, to the Transport Customer (`TK`). 

The message contains measurement data before allocation to a balancing group and therefore does not itself constitute allocation data. 

The message supports preliminary and final measurement data, including values that are measured, estimated, replaced or missing, where applicable. 

## 2. Message Subtypes and Data Flows

The `MEASUREMENT` message supports two subtypes:

| Subtype | Data flow | Description |
|---|---|---|
| `Preliminary` | `WNB` → `WMGV` | Transmission of preliminary measurement values for continuous balancing. |
| `Final` | `WNB` → `WMGV`<br>`WNB` → `TK` | Transmission of final measurement values for balancing and billing-related processes. |

### `Preliminary`

The `Preliminary` subtype is used by the WNB to transmit preliminary measurement values to the WMGV for continuous balancing. 

Preliminary measurements:

- Have a granularity of `PT15M`. 
- Use the unit `kWh` for hydrogen energy quantities. 
- May be measured or represented by a substitute value where needed. 
- May be corrected during the current one-hour balancing period, subject to the applicable correction deadline. 

The WNB must transmit the values no later than six minutes after the end of the relevant quarter-hour. 

### `Final`

The `Final` subtype is used by the WNB to transmit final measurement data to the WMGV and, where applicable, to the TK. 

Final measurements:

- Have a granularity of `PT1H`. 
- Include the final hydrogen energy quantity and the billing-relevant hydrogen content, where applicable. 
- May include substitute values where valid measured values are unavailable or unusable. 
- Are used for final balancing and billing-related processes. 

Final measurements must be transmitted no later than `M+10WT`, meaning ten working days after the end of the delivery month. 

### Distinction from the `ALLOCATION` Message

The `MEASUREMENT` message contains measurement data before allocation to a balancing group. 

The `ALLOCATION` message is used separately for allocation-relevant data assigned to a balancing group. 

| Message format | Main purpose | Balancing group assignment |
|---|---|---|
| `MEASUREMENT` | Transmission of measurement data from the WNB before allocation. | ✗ |
| `ALLOCATION` | Transmission of allocation-relevant data assigned to a balancing group. | ✓ |

The WNB uses the `MEASUREMENT` message to transmit preliminary and final measurement data. 

The WMGV uses a separate allocation process to assign measurement values to balancing groups. 

## 3. Message Structure

The `MEASUREMENT` message consists of the following top-level objects:

- `message`
- `parties`
- `measurementData`

### `message`

The `message` object contains technical message metadata.

Every `MEASUREMENT` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `MEASUREMENT` |
| `subType` | `Preliminary` or `Final` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

`MEASUREMENT`-specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | `HydrogenGridOperator` |
| `recipient.partnerRole` | `HydrogenMarketAreaManager` or, where applicable, `TransportCustomer` |

The common technical properties of `parties` are defined in the shared schemas.

### `measurementData`

The `measurementData` object defines the context for the measurement data transmitted in the message.

| Property | Description |
|---|---|
| `period` | Period covered by the measurement data. |
| `granularity` | Time-series granularity. |
| `location` | Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `measurements` | One or more measurement blocks containing measurement data. |


#### `measurements`

Each object in `measurements` identifies a measured quantity by its unit and `quantityType`, and contains its time-series values.

| Property | Description |
|---|---|
| `unit` | Unit of the measured quantity. |
| `quantityType` | Type of measured quantity. |
| `values` | Ordered time series of measurement values. |

The supported units are:

| Value | Description |
|---|---|
| `kWh` | Hydrogen energy quantity. |
| `molPercent` | Hydrogen content. |

The supported `quantityType` values are:

| `quantityType` | Description |
|---|---|
| `EnergyH2` | Energy quantity of the hydrogen. |
| `HydrogenContent` | Hydrogen content of the measured gas, if supported by the applicable subtype schema. |

#### `values`

`values` is an ordered time series containing values for the measurement intervals covered by the message.

Each value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Measurement value for the interval, expressed in the unit declared for the measurement. |
| `status` | Status identifying the origin or processing state of the value. |

The values must be provided in chronological order and correspond to the declared period and granularity.

The duration of each interval is defined by `measurementData.granularity`. For example, with a granularity of `PT15M`, the timestamp `2026-03-22T15:00:00Z` represents the interval from `2026-03-22T15:00:00Z` to `2026-03-22T15:15:00Z`.

The `status` property describes the origin or processing status of a measurement value.

The supported status values are:

| Value | Description |
|---|---|
| `measured` | The value originates from an actual measurement. |
| `estimated` | The value was estimated or calculated because no directly usable measurement was available. |
| `replaced` | The original value was unavailable, invalid or unusable and was replaced by a substitute value. |
| `missing` | No valid value is available for the relevant interval. |

For preliminary measurements, the WNB performs plausibility checks and may create substitute values before transmitting the data to the WMGV. 

The WMGV uses the received preliminary measurements for continuous balancing and allocates them to the relevant balancing groups in a separate process. 

The WNB is responsible for plausibility checks on the measurement values before transmission; the WMGV processes the values received from the WNB. 

## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/measurement/v0.9/
  README.md
  measurement-message-base.schema.json
  components/
    measurement-data.schema.json
    measurement.schema.json
  preliminary/
    preliminary-measurement-message.schema.json
  final/
    final-measurement-message.schema.json
```
