# RZSM relative dry-state diagnostics planning report

## 1. Git State & Working Tree
- **Branch:** `phase2-shap-drought-targets`
- **Git Status:** Clean. The working tree is fully prepped for drought-target implementation.
- **Base Commit:** `bf320ac Track permutation importance source table and final metrics`

## 2. Data Audit & Climatology Feasibility
Based on an audit of `config.yaml` and the `data/processed/` directory, **only the 2016–2020 period is available**. There are no references to a 2005–2015 spin-up or long-term historical simulations in the current directory paths.

**Scientific Limitations:** 
Five years (60 months) is insufficient to compute a true climatological drought reference (typically requires 30+ years). 

**Recommended Strategy:** **Strategy B**
We cannot compute a robust long-term climatology. Instead, we must strictly compute **"relative drought-state diagnostics"**. 
All metrics will represent standardizations *relative to the 2016–2020 within-period variability*. We must use cautious terminology:
- "relative dry-state transition"
- "within-period relative drought state"
- Avoid terms like "historical drought climatology".

## 3. Feasibility of Current Monthly Dataset
An inspection of the schema for `data/processed/monthly_pixel_dataset_2016_2020_static.parquet` confirms that **100% of the required columns are present**, including:
- OPL and DA states: `SSM_OPL`, `SSM_DA_NoCDF`, `RZSM_OPL`, `RZSM_DA_NoCDF`, etc.
- OPL fluxes: `Evap_tavg_OPL`, `Qs_tavg_OPL`, `Qsb_tavg_OPL`.
- Spatiotemporal coordinates: `lat`, `lon`, `north_south`, `east_west`, `month`, `season`.

No upstream processing modifications are needed.

## 4. Drought Target Definitions
We will design both continuous and categorical targets based on pixel-wise, month-wise distributions within the 2016-2020 period.

**Continuous Targets:**
- `delta_RZSM_zscore`: $Z_{RZSM\_DA} - Z_{RZSM\_OPL}$ (measures relative wetting/drying shift)
- `delta_ET_zscore`: $Z_{ET\_DA} - Z_{ET\_OPL}$ (measures evaporative stress shift)
- `delta_RZSM_percentile`: $P_{RZSM\_DA} - P_{RZSM\_OPL}$ (measures shift across relative moisture distribution)

**Categorical Targets:**
- `drought_class_transition`: Based on empirical percentiles (e.g., >30: Normal, 20-30: Moderate Dry, 10-20: Severe Dry, <10: Extreme Dry). Transition = $Class_{DA} - Class_{OPL}$.
- `binary_transition`: Aggregated to 3 classes (Attenuation [DA makes it wetter], No Change, Intensification [DA makes it drier]). 
*Treatment:* Multi-class classification (Ordinal or standard Categorical).

## 5. Script Design: `src/data/build_drought_targets.py`
**Pipeline:**
1. Read `monthly_pixel_dataset_2016_2020_static.parquet`.
2. Group by `['lat', 'lon', 'month']`.
3. Compute empirical means, std, and percentiles for `RZSM_OPL`, `ET_OPL`, `SSM_OPL`.
4. Map `DA` outputs against these reference distributions to compute DA z-scores and DA percentiles.
5. Compute the defined continuous ($\Delta$) and categorical shift targets.
6. Export enriched dataset: `data/processed/monthly_pixel_dataset_2016_2020_static_drought_targets.parquet`.

**Proposed Outputs:**
- Tables: `drought_target_definitions.csv`, `drought_class_transition_counts.csv`
- Figures: Drought transition spatial maps (`drought_transition_maps_RZSM.png`)

## 6. RF Validation Design
- **Continuous Targets:** `RandomForestRegressor` against Dummy/Ridge baselines, utilizing the exact 5-Fold Spatial CV and temporal holdout strategy established in the baseline analysis.
- **Categorical Targets:** `RandomForestClassifier` against `DummyClassifier` and `LogisticRegression`.
- **Metrics:** Given high class imbalance (most pixels will not change drought class), we will evaluate using **Macro F1-score** and **Balanced Accuracy**, alongside the Confusion Matrix. Accuracy alone will be misleading.

## 7. Scientific Guardrails
**Allowed:**
- Claiming SMAP DA shifts *relative dry-state diagnostics*.
- Identifying predictors structurally associated with attenuation or intensification.
- Discussing $\Delta$RZSM and $\Delta$ET as proxies for drought-propagation mechanisms.

**Prohibited:**
- Claiming robust, multi-decadal drought climatology.
- Claiming causal proof of irrigation correction without independent validation.
- Conflating feature importance directly with physical causality.

## 8. Next Recommended Step
The next logical step is to implement the data processing script: `src/data/build_drought_targets.py` without launching any heavy ML training yet.
