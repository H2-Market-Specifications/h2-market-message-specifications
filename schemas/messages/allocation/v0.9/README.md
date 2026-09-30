# ALLOCATION Message v0.9

## 1. Purpose

The `ALLOCATION` message is used to transmit hydrogen quantities that are relevant for allocation, balancing and forecasting processes.

It supports data exchange between:

- Hydrogen Grid Operators (`WNB`)
- Hydrogen Market Area Manager (`WMGV`)
- Balancing Group Responsible Parties (`BKV`)

## 2. Message Subtypes

The `ALLOCATION` message supports three subtypes:

| Subtype | Data flows | Description |
|---|---|---|
| `Nomination` | `WNB` → `WMGV`<br>`WMGV` → `BKV` | Transmission of confirmed and allocated nomination quantities. |
| `QuantityDeclaration` | `WNB` → `WMGV`<br>`WMGV` → `BKV` | Transmission of quantity declarations and allocated quantity declaration data. |
| `Measurement` | `WMGV` → `BKV` | Transmission of measurements that have already been allocated to a balancing group. |

### `Nomination`

The `Nomination` subtype is used to transmit confirmed nomination quantities from the WNB to the WMGV and allocated nomination quantities from the WMGV to the BKV.

### `QuantityDeclaration`

The `QuantityDeclaration` subtype is used to transmit quantity declaration data from the WNB to the WMGV and allocated quantity declaration data from the WMGV to the BKV.

### `Measurement`

The `Measurement` subtype is used to transmit allocated preliminary or final measurement data from the WMGV to the BKV.

#### Distinction from the `MEASUREMENT` Message

The `ALLOCATION` and `MEASUREMENT` messages serve different purposes.

The `MEASUREMENT` message is used by the WNB to transmit measured data to the WMGV and, where applicable, to the TK. This data is transmitted before allocation to a balancing group and therefore does not constitute allocation data.

The `MEASUREMENT` message includes:

- Preliminary quarter-hourly measurements.
- Final hourly measurements.
- Measurement data before allocation to a balancing group.

The distinction is therefore:

| Message format | Main purpose | Typical sender | Typical recipient | Balancing group assignment |
|---|---|---|---|---|
| `MEASUREMENT` |Transmission of unallocated measurement data	| `WNB` | `WMGV` or `TK` | ✗ |
| `ALLOCATION` |Transmission of allocation-relevant data assigned to a balancing group | `WNB` or `WMGV` | 	`WMGV` or `BKV` | ✓ |


## 3. Message Structure

The `ALLOCATION` message consists of the following top-level objects:

- `message`
- `parties`
- `allocationData`

### `message`

The `message` object contains technical message metadata.
Every `ALLOCATION` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `ALLOCATION` |
| `subType` | - `Nomination`<br> - `QuantityDeclaration`<br> - `Measurement` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.<br>
`ALLOCATION` specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | - `HydrogenGridOperator`<br> - `HydrogenMarketAreaManager` |
| `recipient.partnerRole` | - `HydrogenMarketAreaManager`<br> - `BalancingGroupResponsibleParty` |

The common technical properties of `parties` are defined in the shared schemas.

### `allocationData`

The `allocationData` object defines the context for the allocation data transmitted in the message.

| Property | Description |
|---|---|
| `period` | Timeperiod covered by the message. |
| `asOfDate` | UTC timestamp representing the relevant data status. |
| `unit` | Quantity unit, typically `kWh`. |
| `granularity` | Timeseries granularity. |
| `allocations` | One or more allocation blocks, containing the allocation data. |


#### `allocations`

Each object in `allocationData.allocations` represents a network-point-specific allocation time series per
- balancing group,
- locationtype and 
- flow direction.

The `location` property uses the shared `location` schema and contains both the location identifier and the location type.

| Property | Description |
|---|---|
| `internalAccount` | Internal identifier of the balancing group to which the allocation is assigned |
| `location` | Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `flowDirection` | Direction of the allocated flow: `Entry` or `Exit` |
| `values` | Ordered time series of allocated quantities for the specified balancing group, location, location type and flow direction |

The combination of `internalAccount`, `location.locationType` and `flowDirection` defines the allocation context of the underlying time series.

#### `values`

`values` uses the shared `time-series-value` schema.<br>
It is an ordered time series containing one value for each consecutive time interval of the allocation block. The values must be provided in chronological order and must correspond to the declared period and granularity.
Each value contains the common time-series properties defined by the shared schema, including:

- `timestamp`
- `quantity`

A value may also contain:

- `quality`
- `status`

Both `quality` and `status` are required for the `Measurement` subtype but optional for the `Nomination` and `QuantityDeclaration` subtypes.

The `timestamp` identifies the beginning of the interval represented by the value and not the end of the interval.
The duration of the interval is defined by `allocationData.granularity`.

The end of an interval is calculated as:

```text
interval end = timestamp + granularity
```

The combination of `allocationData.period` and `allocationData.granularity` defines the complete time range and the expected number of intervals.

Examples:

| `allocationData.granularity` | `timestamp` | Applicable interval |
|---|---|---|
| `PT15M` | `2026-03-21T16:00:00Z` | `2026-03-21T16:00:00Z` – `2026-03-21T16:15:00Z` |
| `PT1H` | `2026-03-21T16:00:00Z` | `2026-03-21T16:00:00Z` – `2026-03-21T17:00:00Z` |

## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/allocation/v0.9/
  README.md
  allocation-message-base.schema.json
  components/
    allocation.schema.json
    allocationdata.schema.json
  measurement/
    measurement-allocation-message.schema.json
  nomination/
    nomination-allocation-message.schema.json
  quantitydeclaration/
    quantitydeclaration-allocation-message.schema.json
```
