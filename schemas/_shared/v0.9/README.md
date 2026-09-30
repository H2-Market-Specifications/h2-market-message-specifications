# Shared Schemas v0.9

This directory contains reusable JSON Schemas shared by multiple H2 market message formats.

## Included Schemas

| Schema | Purpose |
|---|---|
| `message.schema.json` | Common technical metadata of a message |
| `parties.schema.json` | Sender and recipient of a message |
| `market-partner.schema.json` | Market partner identifier and market role |
| `location.schema.json` | Network or trading location reference |
| `time-series-value.schema.json` | Reusable entry for timestamp-based time series |

## `message.schema.json`

The `message` object contains common technical message metadata.

| Property | Description |
|---|---|
| `type` | Message type identifier |
| `subType` | Message subtype identifier |
| `version` | Message format version |
| `documentNumber` | Sender-specific business reference for the message |
| `creationDateTime` | UTC timestamp at which the message was created |

Message-specific schemas use this shared schema and add constraints for the permitted message type, subtype and version.

## `parties.schema.json`

The `parties` object identifies both the sender and the recipient of a message.

| Property | Description |
|---|---|
| `sender` | Market partner sending the message |
| `recipient` | Market partner receiving the message |

Both parties use the shared `market-partner.schema.json`.

## `market-partner.schema.json`

The `marketPartner` object identifies a market participant and its role in the message exchange.

| Property | Description |
|---|---|
| `partnerCode` | Identifier of the market partner |
| `partnerRole` | Market role of the partner |

Supported market roles are:







- `HydrogenGridOperator`: Operator of a hydrogen transport or distribution network. The Hydrogen Grid Operator provides network access and capacity, operates the hydrogen network and supplies measurement and network data for balancing and market access processes.
- `HydrogenMarketAreaManager`: Market Area Manager responsible for central balancing and settlement functions in the hydrogen market area, including continuous balancing, calculation and provision of balancing group balances, operation of the Virtual Trading Point and operation of the Data Hub.
- `BalancingGroupResponsibleParty`: Market participant responsible towards the Hydrogen Market Area Manager for the management and balancing of a balancing group, including the submission of nominations and quantity declarations and the settlement of difference quantities.
- `TransportCustomer`: Market participant that requests hydrogen transport, concludes entry and exit contracts, books network capacity and transports hydrogen into or out of the hydrogen network.
- `DataHub`: Central technical communication and data exchange platform for market communication between the participating market roles.

## `location.schema.json`

The `location` object identifies a network or trading location.

| Property | Description |
|---|---|
| `locationCode` | Identifier of the network or trading location |
| `locationType` | Type of the identified location |

Supported location types are:

- `EntryPointProductionFacility`: Entry point from a hydrogen production facility (e.g. electrolyser) into the hydrogen network.
- `ExitPointEndConsumer`: Exit point at which hydrogen is withdrawn from the hydrogen network for delivery to an end consumer.
- `StorageConnectionPoint`: Connection point to a hydrogen storage facility.
- `TerminalConnectionPoint`: Connection point to a hydrogen terminal facility.
- `InterconnectionPoint`: Border crossing or interconnection point between hydrogen networks or market areas.
- `ClusterExchangePoint`: Point used for the exchange or transport of hydrogen between clusters.
- `VirtualTradingPoint`: Virtual tradingpoint at which hydrogen quantities can be transferred virtually between balancing groups.

## `time-series-value.schema.json`

The `timeSeriesValue` object represents one value in a timestamp-based time series.

Each value contains:

- `timestamp`
- `quantity`

The following optional properties may be used where required by the relevant message format:

- `quality`
- `status`
- `flowDirection`
- `dispatchInstruction`

### `timestamp`

The `timestamp` identifies the beginning of the interval represented by the value and not the end of the interval.
The duration and end of the interval are defined by the granularity specified in the containing message or data structure.

The end of an interval is calculated as:

```text
interval end = timestamp + granularity
```

Examples:
| `allocationData.granularity` | `timestamp` | `Applicable interval` |
|---|---|---|
|`PT15M`|2026-03-21T16:00:00Z|2026-03-21T16:00:00Z – 2026-03-21T16:15:00Z|
|`PT1H`|2026-03-21T16:00:00Z|2026-03-21T16:00:00Z – 2026-03-21T17:00:00Z|

All timestamps must be provided as UTC date-time values in ISO 8601 format.

The values in a time-series array must be ordered chronologically and must correspond to the granularity and period defined by the containing message or data structure.

### `quantity`

The `quantity` represents the numerical value for the relevant interval.
The unit is defined by the message or data structure containing the time series.
Decimal values are permitted.
The permitted value range and whether negative values are allowed are defined by the relevant message format.

### `quality`

The `quality` property describes the quality, maturity or finality of the value.

Supported values are:

| Value | Description |
|---|---|
| `preliminary` | The value is provisional and may be updated during the relevant process period |
| `prognosis` | The value represents a forecast or expected value |
| `closed` | The value has been completed or fixed for the relevant process period |
| `final` | The value is final and is not expected to change within the relevant process |

The exact meaning and permitted use of each quality value depend on the relevant message format and business process.

### `status`

The `status` property describes the origin or processing status of the value.

Supported values are:

| Value | Description |
|---|---|
| `measured` | The value originates from an actual measurement |
| `estimated` | The value was estimated or calculated |
| `replaced` | The original value was unavailable, invalid or unusable and was replaced by the quantity declaration. |
| `missing` | No valid value is available for the interval |
| `requestedQuantityConfirmed` | The requested quantity was confirmed by the responsible market role |
| `capacityExceeded` | The requested quantity exceeds the booked or available capacity |
| `supplyBottleneck` | The quantity was reduced or interrupted because of a supply or network bottleneck |

The exact meaning and permitted combinations of status values depend on the relevant message format and business process.

### `flowDirection`

The `flowDirection` property identifies the direction of the flow associated with the time-series value.

| Value | Description |
|---|---|
| `entry` | Flow into the relevant network, system or balancing group |
| `Exit` | Flow out of the relevant network, system or balancing group |

The precise interpretation depends on the message type and the containing data structure.

### `dispatchInstruction`

The `dispatchInstruction` property indicates whether the quantity is a binding operational instruction that must be followed by the receiving market participant. This property is only applicable in the `QUANTITYDECLARATIONRESPONSE` message.

## Usage

Message-specific schemas reference these shared schemas using their canonical `$id` URLs.

Example:

```json
{
  "$ref": "https://h2-market.example/message-specifications/schemas/_shared/v0.9/message.schema.json"
}
```

The shared schemas define common structures only.

Message-specific requirements, such as fixed message types, subtypes, sender and recipient roles, units, granularities, mandatory qualifiers and permitted property combinations, must be defined in the respective message schema.

## Structure

```text
schemas/
└── _shared/
    └── v0.9/
        ├── README.md
        ├── location.schema.json
        ├── market-partner.schema.json
        ├── message.schema.json
        ├── parties.schema.json
        └── time-series-value.schema.json
```
