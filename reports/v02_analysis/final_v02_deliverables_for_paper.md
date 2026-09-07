# Final V0.2 Deliverables for Research Paper

## 1. Dataset
- **File:** `data/processed/monthly_pixel_dataset_2016_2020_static.parquet`
- **Period:** 2016 - 2020 (Monthly scale)
- **Content:** Pixel-level integration of SMAP assimilation outcomes, hydrological variables (OPL), and static surface descriptors.

## 2. Targets Evaluated
The diagnostic analysis focuses on the following priority targets to explain assimilation impacts:
- `increment_SSM_DA_NoCDF`
- `delta_increment_NoCDF_minus_CDF_SSM`
- `delta_DA_NoCDF_minus_OPL_RZSM`
- `delta_DA_NoCDF_minus_OPL_ET`
- `delta_DA_NoCDF_minus_OPL_baseflow`

## 3. Predictors Used
- **Dynamic (OPL Model Initial State & Fluxes):** `SSM_OPL`, `RZSM_OPL`, `SMC_L1_OPL`, `SMC_L2_OPL`, `SMC_L3_OPL`, `SMC_L4_OPL`, `Evap_tavg_OPL`, `Qs_tavg_OPL`, `Qsb_tavg_OPL`
- **Meteorological Forcing:** `precipitation_model`
- **Static Surface:** `land_cover`, `soil_texture`, `elevation`, `irrigation_fraction`, `soil_texture_dominant_fraction`, `land_cover_dominant_fraction`
- **Seasonality:** `month`, `season`

## 4. Methodology (RF / XAI)
- **Model:** Scikit-Learn `RandomForestRegressor` (150 estimators).
- **Interpretability:** Permutation Importance (evaluated on unseen test data).
- **Validation 1 (Temporal):** Train on 2016-2019, Test on 2020. Evaluates generalization to an unseen year.
- **Validation 2 (Spatial CV):** 5-Fold GroupKFold on 25 geographic blocks (quantiles of coordinates). Evaluates generalization to unseen spatial domains to verify robustness of static predictors.

## 5. Available Figures
- `outputs/figures/rf_temporal_vs_spatial_cv_v02.png` *(Barplot comparing Temporal and Spatial R²)*
- `outputs/figures/rf_model_skill_v02_spatial_cv.png` *(Scatter plots of Predictions vs Observations)*
- `outputs/figures/rf_feature_importance_v02_spatial_cv.png` *(Standard Permutation Importance ranking)*
- `outputs/figures/rf_grouped_feature_importance_v02.png` *(Cumulative importance aggregated by predictor families)*

## 6. Limitations
- **No Causal Proof:** The Random Forest acts as a diagnostic tool for statistical associations; it highlights spatial consistencies rather than proving strict physical causality.
- **In-Situ Forcing Error:** `precipitation_error` from gauge stations is not included in this version due to the lack of overlap between the available station dataset (ends in 2014) and the SMAP period (2016-2020).
- **Scale Mismatch:** Static variables are provided at ~5km resolution, which may under-represent fine-scale heterogeneities like sub-pixel irrigation.

## 7. Future Analyses
- **V1 (Precipitation Error Attribution):** Once updated in-situ data (2016-2020) or alternative independent gridded precipitation products (e.g., CHIRPS, IMERG) are integrated, the pipeline will test whether precipitation forcing mismatches directly explain SMAP increments.
