# BALANCING Message v0.9

## 1. Purpose

The `BALANCING` message is used by the Hydrogen Market Area Manager (`WMGV`) to transmit balancing figures to the Balancing Group Responsible Party (`BKV`).

It supports:

- Continuous balancing, including preliminary, closed and forecast balancing figures.
- The post-monthly balancing mechanism, including post-monthly balances and difference quantities.

The message does not change completed balancing results or the Overall Network Status retroactively.

## 2. Message Subtypes

The `BALANCING` message supports two subtypes:

| Subtype | Data flow | Description |
|---|---|---|
| `ContinuousBalancing` | `WMGV` → `BKV` | Transmission of balancing figures for continuous balancing, including preliminary, closed and prognosis values. |
| `DifferenceQuantities` | `WMGV` → `BKV` | Transmission of post-monthly balances and difference quantities for the relevant delivery month. |

### `ContinuousBalancing`

The `ContinuousBalancing` subtype is used to transmit balancing figures for a balancing group. Depending on the data available and the point in time, these may include preliminary, closed and prognosed values.

### `DifferenceQuantities`

The `DifferenceQuantities` subtype is used to transmit post-monthly balancing figures calculated using final measurement data and final allocations. It includes the difference between the post-monthly final BGBalance and the closed BGBalance.

The post-monthly process does not retroactively change closed balancing results or the Overall Network Status.


## 3. Message Structure

The `BALANCING` message consists of the following top-level objects:

- `message`
- `parties`
- `balancingData`

### `message`

The `message` object contains technical message metadata.
Every `BALANCING` `message` block must contain the following fixed values:

| Property | Description |
|---|---|
| `type` | `BALANCING`. |
| `subType` | `ContinuousBalancing` or `DifferenceQuantities`. |
| `version` | `0.9`. |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.
`BALANCING` specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | `HydrogenMarketAreaManager` |
| `recipient.partnerRole` | `BalancingGroupResponsibleParty` |

The common technical properties of `parties` are defined in the shared schemas.

### `balancingData`

The `balancingData` object defines the context for the balancing figures transmitted in the message.

| Property | Description |
|---|---|
| `clusterId` | Name or identifier of the cluster the balancing group is assigned to. |
| `internalAccount` | Internal identifier of the balancing group. |
| `unit` | Unit of the balancing quantities; typically `kWh`. |
| `asOfDate` | UTC timestamp identifying the data status used to create the message. |
| `balancingFigures` | One or more balancing-number time series. |

The `asOfDate` identifies the point in time up to which data was retrieved from or available in the source system.

#### `balancingFigures`

Each element in `balancingFigures` identifies a balancing quantity through its `quantityType` and contains one or more period values.

| Property | Description |
|---|---|
| `quantityType` | Identifier of the transmitted type of balancing figure. |
| `values` | Ordered time series of allocated quantities for the specified balancing group, location, location type and flow direction |

#### `quantityType`

Transmitted balancing figures are:

| `quantityType` | Description | Transmitted via `ContinuousBalancing` | Transmitted via `DifferenceQuantities` |
|---|---|---|---|
| `BGBalance` | Balancing group balance for the specified interval, calculated as Entry minus Exit. | ✓ | ✓ |
| `BGBalanceCumulative` | Cumulative balancing group balance of the internal balancing group. | ✓ | ✗ |
| `BGBalanceCumulativeExternal` | Cumulative balancing group balance of an external balancing group associated with the internal balancing group. | ✓ | ✗ |
| `OverallNetworkStatus` | Cumulative balancing status of the relevant cluster. | ✓ | ✗ |
| `BGBalanceDifference` | Difference between the post-monthly final balance and the closed balance for the specified interval. | ✗ | ✓ |
| `BGBalancePostmonthly` | Balancing group balance calculated after the delivery month using final measurement data and final allocations. | ✗ | ✓ |

#### `values`

`values` uses the `balancing-period-value` schema.<br> 
It is an ordered series of values for the relevant `quantityType`.

In general each balancing period value contains:

| Property | Description |
|---|---|
| `periodStart` | Inclusive start of the balancing interval. |
| `periodEnd` | Exclusive end of the balancing interval. |
| `quantity` | Balancing quantity in the unit declared in `balancingData.unit`; positive and negative values are permitted. |
| `quality` | Quality of the balancing quantity. |
| `helperCauser` | Helper or Causer designation, where applicable to cumulative balancing values. |

The combination of `periodStart` and `periodEnd` defines the interval explicitly.

The supported qualities are:

- `preliminary`
- `prognosis`
- `closed`
- `final`

The `helperCauser` property is used only for:

- `BGBalanceCumulative`
- `BGBalanceCumulativeExternal`

The Helper/Causer designation is determined using the relevant cumulative balance and Overall Network Status. A zero cumulative balance is treated as Helper.


## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/balancing/v0.9/
  README.md
  balancing-message-base.schema.json
  continuousbalancing/
    continuousbalancing-balancing-message.schema.json
  differencequantities/
    differencequantities-balancing-message.schema.json
  components/
    balancing-data.schema.json
    balancing-number.schema.json
    balancing-period-value.schema.json
```
