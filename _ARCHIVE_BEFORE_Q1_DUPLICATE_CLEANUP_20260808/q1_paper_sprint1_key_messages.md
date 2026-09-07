# Key Messages & Structure

## 10 robust scientific messages
1. Assimilating SMAP observations without CDF matching introduces systematic modifications to the hydrological states, particularly drying during DJF and slight wetting during JJA.
2. The hydrological impact of SMAP assimilation propagates vertically, primarily modifying baseflow dynamics rather than surface runoff.
3. The random forest models show high predictive skill for predicting ET and RZSM impacts (R2 > 0.39), supporting the interpretation that assimilation increments follow physically consistent patterns.
4. Dynamic variables (precipitation, soil moisture state, seasonal timing) strongly dominate over static geographical variables (topography, soil texture) in explaining assimilation increments.
5. High soil moisture adjustments are associated with periods of precipitation, indicating structural differences between the model's precipitation forcing and satellite observations.
6. The seasonal contrast in SSM response suggests that the model is structurally too wet in winter and slightly too dry in summer compared to SMAP retrievals.
7. Baseflow serves as the primary sink for the added or removed water, acting as a slow reservoir that buffers assimilation impacts over time.
8. The implementation of CDF matching essentially eliminates the long-term hydrological impact of data assimilation, making total runoff indistinguishable from the open-loop simulation.
9. Explainable AI diagnostics provide a robust, non-parametric framework to understand spatial and temporal assimilation behavior without running computationally expensive sensitivity ensembles.
10. The lack of correlation for baseflow changes in the RF model highlights that deep groundwater processes are driven by complex routing not easily captured by pixel-based surface predictors.

## 5 messages to NOT say
1. Do not say SMAP "proves" the model is wrong; rather, it suggests inconsistencies.
2. Do not claim that assimilation "causes" ET increases; it is associated with or diagnostic of changes in ET.
3. Avoid the term "irrigation correction", as no irrigation scheme was explicitly isolated.
4. Do not say "SMAP corrected irrigation"; instead use "consistent with unmodeled agricultural practices".
5. Do not assert that DA-NoCDF is perfectly correct; just say it provides a diagnostic of the model's background hydroclimatic state.

## 5 main limitations
1. In-situ precipitation data could not be included because stations stop in 2014, requiring reliance on satellite forcings.
2. The study is limited to pre-routing diagnostics, meaning downstream river flow (HyMAP) impacts are not fully evaluated.
3. Irrigation is turned OFF, meaning the assimilation is forced to absorb agricultural signals as structural errors.
4. ET/GPP external evaluation remains a first-order validation rather than a perfect ground truth.
5. The pixel-based RF approach does not capture lateral flow dynamics between pixels.

## 5 figures for the main paper
1. Fig 1: Multi-year SMAP diagnostics (Innovation & Observation count maps).
2. Fig 2: Seasonal SSM response (DJF vs JJA DA-NoCDF impact).
3. Fig 3: Runoff partitioning and baseflow response.
4. Fig 4: RF model predictive skill (Spatial CV `rf_model_skill_v02_spatial_cv.png`).
5. Fig 5: RF grouped feature importance (`rf_grouped_feature_importance_v02.png`).

## 5 figures for supplementary
1. Fig S1: CDF vs NoCDF hydrological contrast (DA-CDF runoff).
2. Fig S2: RF temporal vs spatial cross-validation comparison (`rf_temporal_vs_spatial_cv_v02.png`).
3. Fig S3: RF individual feature importance (`rf_feature_importance_v02_spatial_cv.png`).
4. Fig S4: Initial OPL model biases (pre-assimilation maps).
5. Fig S5: Static predictor maps (Topo, Soil, Land Cover).
