# RF/XAI Versions

- **V0**: RF/XAI without gauge-based precipitation-error predictors.
  - **Inputs**: Noah-MP/SMAP DA monthly pixel dataset, static predictors, OPL dynamic predictors, seasonal predictors.
  - **Excludes**: in-situ precipitation-error predictors.
  - **Reason**: available station coverage must be checked before use.
- **V1 planned**: RF/XAI with precipitation-error predictors if station data cover 2016–2020.
