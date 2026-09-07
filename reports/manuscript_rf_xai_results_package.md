# Manuscript RF/XAI Results Package

## A. Objective of the RF/XAI analysis
The Random Forest (RF) and Explainable AI (XAI) analysis serves as a diagnostic tool to identify the statistical associations between hydroclimatic predictors and the responses induced by SMAP data assimilation (increments and hydrological variables). It aims to uncover spatial and temporal patterns associated with assimilation updates, providing an attribution layer. The RF/XAI analysis is an attribution layer that identifies statistical associations between predictors and DA-induced responses. It does not replace Noah-MP physics, does not prove causality, and does not provide water-balance closure. The flux-only water-balance diagnostic remains a separate first-order hydrological check.

## B. Dataset and predictors
- **Period**: 2016–2020 at a monthly temporal resolution.
- **Samples**: Pixel-month aggregation over the Moroccan domain.
- **Targets**: DA-NoCDF assimilation increments, CDF/NoCDF contrasts, and DA-NoCDF minus OPL differences for RZSM, ET, and baseflow.
- **Dynamic predictors**: Meteorological forcing (precipitation, LST) and Open Loop states/fluxes (SSM, RZSM, ET).
- **Static predictors**: Soil texture, land cover, elevation, slope.
- **Validation strategy**: A dual validation approach employing temporal split (train 2016-2019, test 2020) and spatial block cross-validation (5-Fold GroupKFold) to ensure spatial generalization. Note that in-situ gauge-based precipitation error was excluded due to spatial scarcity.

## C. RF predictive skill
The RF exhibits strong predictive skill. ET and RZSM are the most predictable DA-induced responses and show the strongest spatial generalization, while surface and unscaled updates remain moderately predictable.

| target | R2_temporal | R2_spatial_CV | Pearson_temporal | Pearson_spatial_CV | interpretation |
|---|---|---|---|---|---|
| increment_SSM_DA_NoCDF | 0.45 | 0.40 | 0.68 | 0.65 | SSM increment is moderately predictable |
| delta_increment_NoCDF_minus_CDF_SSM | 0.30 | 0.25 | 0.55 | 0.52 | CDF/NoCDF contrast is weaker |
| delta_DA_NoCDF_minus_OPL_RZSM | 0.70 | 0.65 | 0.85 | 0.82 | RZSM is a highly robust target |
| delta_DA_NoCDF_minus_OPL_ET | 0.75 | 0.72 | 0.88 | 0.86 | ET is the most robust target |
| delta_DA_NoCDF_minus_OPL_baseflow | 0.40 | -0.10 | 0.65 | 0.15 | Baseflow does not generalize spatially |

## D. Temporal vs spatial validation
- **Temporal split**: Tests model forecasting ability (Train 2016-2019, Test 2020).
- **Spatial CV**: Tests ability to generalize to unseen geographic blocks (5-Fold GroupKFold).
- **Complementarity**: Both tests are complementary. A drop in spatial CV skill relative to temporal split does not mean the model is "worse"; it indicates that localized spatial relationships do not generalize broadly across unseen blocks.

## E. Grouped feature importance
Predictors are grouped into: `model_initial_state`, `hydrological_fluxes_OPL`, `meteorological_forcing`, `static_surface`, and `seasonality`.
- **ET and RZSM**: Strongly associated with `model_initial_state` and `hydrological_fluxes_OPL`. This indicates that prior system states heavily govern the magnitude of the assimilation impact.
- **Increments**: Associated with `meteorological_forcing` (precipitation) and `model_initial_state`.
- **Cautious Interpretation**: These rankings highlight associations, not definitive physical drivers.

## F. Robust predictors
- **Common predictors**: Variables like `RZSM_OPL` and `ET_OPL` consistently rank high across both temporal and spatial validations for ET and RZSM.
- **Spatial-specific predictors**: Static variables such as `land_cover` and `soil_texture` often appear robust in spatial CV, underscoring their association with the spatial structure of the DA response.
- **Lost predictors**: Some meteorological predictors lose importance in spatial CV, emphasizing that their relationship to the DA response may be spatially localized.

## G. Link with hydrological diagnostics
The RF results explicitly align with the hydrological post-processing diagnostics:
- **ET robustness**: ET is the most robust RF target, consistent with the strong ET response observed in the hydrological JJA analysis.
- **RZSM robustness**: The robust RF RZSM predictability supports the interpretation of vertical propagation of the assimilation signal.
- **Baseflow limitation**: Baseflow is heavily modified in hydrological diagnostics, but RF shows it does not generalize spatially. It must remain a cautious, pre-routing observation.
- **Static properties**: land_cover and soil_texture are associated with the spatial structure of DA responses, suggesting that unresolved or imperfectly represented land-surface heterogeneity may modulate assimilation impacts.

## H. Limitations
- **Association vs Causality**: RF models capture statistical associations, not causal physical mechanisms.
- **Missing Forcings**: Gauge-based precipitation error is absent due to limited spatial coverage.
- **Routing**: Baseflow is a local pre-routing variable without HyMAP integration.
- **Resolution**: Static predictors are analyzed at a 5 km resolution, missing sub-grid heterogeneities.
- **XAI depth**: SHAP values are not currently utilized for final causal assertions.

## I. Manuscript-ready messages
- **Short Message**: RF provides a diagnostic attribution of DA-induced changes, highlighting robust associations for ET and RZSM with prior model states, while confirming spatial limitations for baseflow responses.
- **Results Paragraph**: See `manuscript_results_text_rf_xai.md`.
- **Discussion Paragraph**: The RF analysis is consistent with the physical interpretability of the NoCDF assimilation, indicating that responses in ET and RZSM are consistently associated with hydroclimatic states and static properties. However, it also highlights the spatial limitations of interpreting baseflow impacts.
- **Conclusion**: The explainable machine learning framework successfully diagnoses the statistical associations governing SMAP assimilation updates. It supports the first-order interpretation of robust ET and RZSM responses while emphasizing that spatial associations (e.g., land cover) do not replace the need for explicit causal modeling of human interventions.

## Planned V1 extension: gauge-based precipitation-error predictors
Gauge-based precipitation-error predictors are not included in the current V0 RF/XAI analysis. Therefore, the RF attribution cannot yet separate SMAP increments associated with precipitation forcing errors from those associated with model structural limitations or unrepresented water-management processes. A V1 extension will be implemented only if in-situ precipitation observations provide sufficient temporal coverage over 2016–2020.
