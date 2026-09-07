# Sprint 2: Units and Variable Mapping

## Objective
Document the mapping between the raw Noah-MP LIS output variables and the final variables used in the Q1 paper for hydrological responses.

## Variable Mapping

| Original LIS Variable | Script Variable | Final Unit | Conversion Applied | Aggregation Period |
| --- | --- | --- | --- | --- |
| `Rainf_tavg` | `P` | mm/day | Divided by number of days in the month | Monthly -> Seasonal/Annual |
| `Evap_tavg` | `ET` | mm/day | Divided by number of days in the month | Monthly -> Seasonal/Annual |
| `Qs_tavg` | `Qs` (Surface Runoff) | mm/day | Divided by number of days in the month | Monthly -> Seasonal/Annual |
| `Qsb_tavg` | `Qsb` (Baseflow) | mm/day | Divided by number of days in the month | Monthly -> Seasonal/Annual |
| `Qs_tavg` + `Qsb_tavg` | `Qtotal` (Total Runoff)| mm/day | Divided by number of days in the month | Monthly -> Seasonal/Annual |
| `SSM` (Layer 1 SMC) | `SSM` | m³/m³ | None (State variable) | Monthly -> Seasonal/Annual |
| `RZSM` (Layers 1-4) | `RZSM` | m³/m³ | None (State variable) | Monthly -> Seasonal/Annual |

## Notes
- Original LIS output: kg m-2 s-1 or equivalent water flux where applicable.
- Monthly processed dataset: monthly accumulated water depth in mm/month.
- Figure unit: converted to mm/day by dividing by the exact number of days per month.
- Soil moisture states remain m3/m3.
- The `precipitation_model` source is formally confirmed as **IMERG** via the LIS overlay forcing configuration.
