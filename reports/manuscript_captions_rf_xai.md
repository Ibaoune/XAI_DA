# RF/XAI Manuscript Captions

**Figure X. Generalization capability of the Random Forest model (Temporal vs. Spatial CV)**
*Caption:* Generalization capability of the Random Forest model predicting SMAP DA-NoCDF responses, evaluated through both Temporal Split (Train 2016–2019, Test 2020) and Spatial Block Cross-Validation (5-Fold GroupKFold). The R² metric highlights the complementarity of both validations. ET and RZSM exhibit robust predictability across both temporal and spatial dimensions. Conversely, the baseflow response is not spatially robust, indicating that its localized associations fail to generalize across distinct spatial blocks.

**Figure Y. Grouped permutation feature importance**
*Caption:* Grouped permutation feature importance for the primary assimilation responses. Predictors are aggregated into families: initial states, hydrological fluxes (OPL), meteorological forcing, static surface properties, and seasonality. Results indicate that initial states, hydrological fluxes, and static surface properties are strongly associated with DA responses, particularly for ET and RZSM. Note that feature importance represents statistical association and does not imply causality.

**Figure S1. Random Forest Spatial Cross-Validation Skill**
*Caption:* Spatial cross-validation (5-Fold GroupKFold) predictive skill (R² and Pearson correlation) for various assimilation targets.

**Figure S2. Random Forest Permutation Feature Importance (Spatial CV)**
*Caption:* Top individual predictors identified by Random Forest permutation feature importance under spatial cross-validation for DA-induced changes in states and fluxes.

**Figure S3. Random Forest Increment Feature Importance (Spatial CV)**
*Caption:* Top individual predictors for the raw SMAP assimilation increments identified by Random Forest permutation feature importance under spatial cross-validation.
