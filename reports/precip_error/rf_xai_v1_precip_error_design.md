# RF/XAI V1 Precipitation Error Design

## A. Scientific objective
The primary goal of the V1 extension is to diagnose whether the addition of gauge-based precipitation-error predictors helps explain DA-induced responses, particularly:
- `increment_SSM_DA_NoCDF`
- `delta_DA_NoCDF_minus_OPL_RZSM`
- `delta_DA_NoCDF_minus_OPL_ET`
- `delta_DA_NoCDF_minus_OPL_runoff` / `baseflow`
- `delta_increment_NoCDF_minus_CDF_SSM`

By separating precipitation forcing errors from structural errors, we can better attribute the source of the SMAP increments.

## B. New predictors
If a sufficiently dense gauge network is provided, the following predictors will be added:
- `precip_bias_monthly` (IMERG - Gauge)
- `precip_abs_error_monthly` (|IMERG - Gauge|)
- `precip_error_anomaly` (if a long-term gauge climatology is available)
- `station_count_per_pixel` (to assess predictor confidence)
- `distance_to_nearest_station` (to account for spatial interpolation errors)
- `gauge_precip_monthly` (the observed reference)

## C. Validation strategy
- **Comparison**: Compare RF V0 (without precip-error) against RF V1 (with precip-error).
- **Validation**: Maintain the identical temporal split (Train 2016–2019, Test 2020) and spatial block cross-validation (5-Fold GroupKFold) to ensure fair comparison.
- **Ablation test**: An ablation study (with vs. without precip-error predictors).
- **Masking**: Pixels lacking a nearby station (e.g., > 20 km) should be masked or flagged to avoid spatial artifacts.

## D. Expected figures
- RF predictive skill comparison: V0 vs V1.
- Grouped permutation feature importance incorporating the new `precipitation_error` family.
- Spatial maps detailing in-situ station coverage.
- Spatial maps of the precipitation-error predictors.
- Robust predictor rankings comparing shifts from V0 to V1.

## E. Cautions
- **Gauge representativeness error**: Point-scale gauges may not perfectly represent 5 km pixel averages.
- **Station density bias**: Uneven spatial distribution of gauges could skew the RF training toward densely monitored regions.
- **Missing station periods**: Temporal gaps in gauge records require careful handling or imputation.
- **Association not causality**: The inclusion of precipitation error improves statistical association but still does not prove causality (e.g., it does not explicitly model irrigation).
