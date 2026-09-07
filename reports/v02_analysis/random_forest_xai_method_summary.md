# Random Forest and XAI Method Summary

## 1. Objective of the RF/XAI Analysis (V0.2 Final Version)
The objective of this analysis is to employ Explainable Artificial Intelligence (XAI), specifically Random Forest coupled with permutation importance, to diagnose and understand the drivers of assimilation increments and their impacts. This diagnostic framework helps in identifying hydroclimatic and static factors that are **associated with** or **diagnostic of** differences between CDF and No-CDF assimilation experiments.

**Note on Versioning:** The definitive version used for the research paper is **V0.2**, which includes static predictors, temporal splitting, and spatial block cross-validation. The V1 integration (`precipitation_error` from in-situ data) is planned for future work but is not included in the current analysis due to data availability constraints.

## 2. Targets
The primary variables we seek to explain are:
- `delta_NoCDF_minus_CDF_SSM`: Differences in surface soil moisture due to CDF matching.
- `increment_NoCDF`: The soil moisture increment added/removed during assimilation.
- `delta_DA_NoCDF_minus_OPL_ET`: Changes in evapotranspiration post-assimilation.
- `delta_DA_NoCDF_minus_OPL_baseflow`: Changes in baseflow post-assimilation.

## 3. Predictors
The models are trained using two categories of predictors:
- **Dynamic Predictors:** IMERG precipitation, gauge precipitation, precipitation_error (IMERG - gauge), antecedent precipitation (7/30/90 days), OPL variables (SSM, RZSM, ET, runoff, baseflow), and SMAP observation counts.
- **Static Predictors:** Elevation, slope, land cover, cropland/irrigation proxy, soil texture, basin ID, month, and season.

*Note:* In `environmental_explanatory` mode, innovation is strictly excluded to prevent data leakage.

## 4. Train/Test Split (Temporal and Spatial)
To ensure the robustness of the Random Forest relationships and prevent spatial/temporal memorization, the model is evaluated using two complementary validation strategies (V0.2):
- **Temporal Split:** Training on 2016–2019, testing on an unseen year (2020) to evaluate inter-annual generalization.
- **Spatial Block CV:** 5-fold cross-validation on 25 geographic blocks (qcut on coordinates) to evaluate generalization to entirely unseen spatial domains.

## 5. Metrics
Model performance is evaluated using:
- R² (Coefficient of Determination)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Pearson Correlation Coefficient

## 6. Limitations and Cautious Interpretation
Machine learning models identify patterns and correlations, not definitive causation. Therefore, the interpretation of feature importance and SHAP values must remain prudent. 

**Required Language:**
Results should be discussed using terms such as:
- *"associated with"*
- *"consistent with"*
- *"diagnostic of"*
- *"suggests"*

**Strictly Avoid:**
Do NOT use definitive causal claims such as:
- *"proves irrigation"*
- *"proves precipitation error"*
- *"proves SMAP bias"*

These results are diagnostic tools designed to guide physical understanding rather than provide absolute proof of underlying errors or physical phenomena.
