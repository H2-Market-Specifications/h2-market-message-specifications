# QUANTITYDECLARATION Message v0.9

## 1. Purpose

The `QUANTITYDECLARATION` message is used by a Balancing Group Responsible Party (`BKV`) to report planned hydrogen quantities for non-nomination-dependent network points to the responsible Hydrogen Grid Operator (`WNB`).

Quantity declarations are used for planning and forecasting. For points where the applicable allocation method is “allocated as measured”, measured quantities—not the quantity declaration—are used to determine the balancing group balance. The quantity declaration may also be used to provide forecast or substitute values where measurement data is not available. 

## 2. Message Subtype

The `QUANTITYDECLARATION` message supports one subtype:

| Subtype | Data flow | Description |
|---|---|---|
| `Default` | `BKV` → `WNB` | Transmission of the BKV’s planned quantities for non-nomination-dependent network points. |

The WNB checks and processes the quantity declaration and may send a confirmation to the BKV. 

The WNB subsequently transmits the quantity declaration data to the WMGV for balancing and forecasting purposes. The WMGV uses the latest quantity declaration submitted by the BKV, not the quantity confirmed by the WNB, for the relevant forecasting process. 

## 4. Difference from the `NOMINATION` Message

The `QUANTITYDECLARATION` message is used for non-nomination-dependent network points. The `NOMINATION` message is used for nomination-dependent network points and for transfers between balancing groups at the VHP. 

| Message format | Network point or purpose | Role in balancing |
|---|---|---|
| `NOMINATION` | Nomination-dependent network points and VHP transfers. | Confirmed nominations are allocation-relevant at points where the applicable method is “allocated as nominated”. |
| `QUANTITYDECLARATION` | Non-nomination-dependent network points. | Used for forecasting; measured values are used for balancing where the applicable method is “allocated as measured”. |

## 3. Message Structure

The `QUANTITYDECLARATION` message consists of the following top-level objects:

- `message`
- `parties`
- `quantityDeclarationData`

### `message`

The `message` object contains technical message metadata.

Every `QUANTITYDECLARATION` `message` block must contain the following fixed values:

| Property | Allowed value(s) |
|---|---|
| `type` | `QUANTITYDECLARATION` |
| `subType` | `Default` |
| `version` | `0.9` |

The common technical properties of `message` are defined in the shared schemas.

### `parties`

The `parties` object identifies the sender and recipient.

`QUANTITYDECLARATION`-specific restrictions are:

| Property | Allowed value(s) |
|---|---|
| `sender.partnerRole` | `BalancingGroupResponsibleParty` |
| `recipient.partnerRole` | `HydrogenGridOperator` |

The common technical properties of `parties` are defined in the shared schemas.

### `quantityDeclarationData`

The `quantityDeclarationData` object defines the context for the declared quantities.

| Property | Description |
|---|---|
| `location` |  Network or trading location defined by the shared `location` schema; contains `locationCode` and `locationType` |
| `internalAccount` | Internal identifier of the balancing group. |
| `period` | Period covered by the quantity declaration. |
| `granularity` | Time-series granularity; currently `PT1H`. |
| `unit` | Unit of the declared quantities; typically `kWh`. |
| `values` | Ordered time series of declared quantities. |

#### `location`

The `location` object identifies the non-nomination-dependent network point for which the quantity is declared. It uses the shared `location` schema.

Quantity declarations apply in particular to:

- Exit points to end consumers.
- Entry points from domestic hydrogen production facilities. 

#### `internalAccount`

`internalAccount` identifies the balancing group for which the quantity declaration is submitted.

#### `values`

`values` is an ordered time series containing a value for each consecutive interval covered by the declaration.

Each value contains:

| Property | Description |
|---|---|
| `timestamp` | UTC timestamp identifying the beginning of the interval represented by the value. |
| `quantity` | Declared quantity for the interval, expressed in the unit declared in `quantityDeclarationData.unit`. |

The values must be provided in chronological order and correspond to the declared period and granularity. The duration of each interval is defined by `quantityDeclarationData.granularity`.

For example, with a granularity of `PT1H`, the timestamp `2026-03-21T23:00:00Z` represents the interval from `2026-03-21T23:00:00Z` to `2026-03-22T00:00:00Z`.

Quantity declarations are submitted as direction-specific, non-negative whole-number hourly values in `kWh/h`, or as `0`. The flow direction is determined by the network point. 


## 4. Schema Files

The format consists of the following schemas:

```text
schemas/messages/quantitydeclaration/v0.9/
  README.md
  quantitydeclaration-message-base.schema.json
  components/
    quantity-declaration-data.schema.json
  default/
    default-quantitydeclaration-message.schema.json
```
