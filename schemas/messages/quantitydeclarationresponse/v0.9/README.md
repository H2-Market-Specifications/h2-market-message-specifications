# QUANTITYDECLARATIONRESPONSE Message v0.9

## 1. Purpose

The `QUANTITYDECLARATIONRESPONSE` message is used by the Hydrogen Grid Operator (`WNB`) to return the result of processing a quantity declaration to the Balancing Group Responsible Party (`BKV`). 

The response can include the quantity submitted by the BKV, the quantity confirmed by the WNB, the booked capacity, a status for the confirmed quantity and an indication of whether it is a dispatch instruction. 

## 2. Message Subtype

The `QUANTITYDECLARATIONRESPONSE` message supports one subtype:

| Subtype | Data flow | Description |
|---|---|---|
| `Default` | `WNB` → `BKV` | Transmission of the WNB’s processing result for a quantity declaration. |

The WNB sends a response after checking the quantity declaration. 

## 3. Message Structure

The `QUANTITYDECLARATIONRESPONSE` message consists of the following top-level objects:

- `message`
- `parties`
- `quantityDeclarationResponseData`

### `message`

The `message` object contains technical message metadata.

Every `QUANTITYDECLARATIONRESPONSE` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `QUANTITYDECLARATIONRESPONSE` |
| `subType` | `Default` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

`QUANTITYDECLARATIONRESPONSE`-specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | `HydrogenGridOperator` |
| `recipient.partnerRole` | `BalancingGroupResponsibleParty` |

The common technical properties of `parties` are defined in the shared schemas.

### `quantityDeclarationResponseData`

The `quantityDeclarationResponseData` object defines the context for the response.

| Property | Description |
|---|---|
| `location` |  Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `internalAccount` | Internal identifier of the balancing group. |
| `period` | Period covered by the response. |
| `timeSeries` | One or more time series containing the response quantities. |

The `location` object identifies the non-nomination-dependent network point for which the quantity declaration was processed. Quantity declarations apply in particular to exit points to end consumers and entry points from domestic hydrogen production facilities. 

The `internalAccount` identifies the balancing group for which the quantity declaration was submitted and processed.

#### Time Series

Each element in `timeSeries` represents one quantity type for the specified location, balancing group and period.

| Property | Description |
|---|---|
| `quantityType` | Type of quantity represented by the time series. |
| `unit` | Unit of the quantity. |
| `granularity` | Time-series granularity. |
| `values` | Ordered time series of values for the specified quantity type. |

The supported `quantityType` values are:

| `quantityType` | Unit | Description |
|---|---|---|
| `RequestedQuantity` | `kWh/h` | Quantity submitted by the BKV. |
| `ConfirmedQuantity` | `kWh/h` | Quantity confirmed by the WNB. |
| `BookedCapacity` | `kW` | Capacity booked for the relevant location and balancing group. |

Quantity declarations are submitted as direction-specific hourly values in `kWh/h`; the applicable network point determines the flow direction. 

The `RequestedQuantity` and `BookedCapacity` time series do not contain a status or dispatch instruction.

The `ConfirmedQuantity` time series contains a status and a dispatch instruction for each value.

#### values

`values` is an ordered time series containing one value for each consecutive interval covered by the time series.

Each value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Quantity for the interval, expressed in the unit declared for the time series. |

Each value in a `ConfirmedQuantity` time series additionally contains:

| Property | Description |
|---|---|
| `status` | Status of the confirmed quantity. |
| `dispatchInstruction` | Indicates whether the confirmed quantity is a binding operational instruction. |

The values must be provided in chronological order and correspond to the declared period and granularity.

The duration of each interval is defined by the `granularity` of the time series. For example, with a granularity of `PT1H`, the timestamp `2026-03-22T15:00:00Z` represents the interval from `2026-03-22T15:00:00Z` to `2026-03-22T16:00:00Z`.

The following status values are supported for `ConfirmedQuantity`:

| Value | Description |
|---|---|
| `requestedQuantityConfirmed` | The requested quantity is confirmed as submitted. |
| `capacityExceeded` | The requested quantity exceeds the available or booked capacity. |
| `supplyBottleneck` | The quantity has been reduced or interrupted because of a supply bottleneck. |

If a quantity is reduced or interrupted because of a supply bottleneck, the status `supplyBottleneck` is used. 

If a quantity exceeds the applicable booked capacity, the WNB may reduce the confirmed quantity to the booked capacity and use the status `capacityExceeded`. 

If both a capacity exceedance and a supply bottleneck apply, `supplyBottleneck` takes precedence. 

`dispatchInstruction` indicates whether the confirmed quantity is a binding operational instruction that must be followed by the receiving market participant.

Before the end of the capacity booking period, a confirmed quantity is generally not a dispatch instruction unless a supply bottleneck requires a reduction or interruption. 

After the end of the capacity booking period, the confirmed quantity is treated as a dispatch instruction. 

In the event of a supply bottleneck, any reduced or interrupted quantity is always treated as a dispatch instruction. 

## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/quantitydeclarationresponse/v0.9/
  README.md
  quantitydeclarationresponse-message-base.schema.json
  components/
    quantitydeclarationresponse-data.schema.json
    time-series-item.schema.json
  Default/
    Default-quantitydeclarationresponse-message.schema.json
```
