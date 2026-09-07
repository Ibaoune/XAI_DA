# Random Forest Validation Summary (V0.2 Spatial CV)

## A. Objective
L'objectif de cette étape est de valider la robustesse spatiale des modèles Random Forest (V0.1). Le split temporel testait la capacité de généralisation temporelle à l'année 2020. Cependant, pour interpréter le rôle physique des variables statiques (`land_cover`, `soil_texture`, `elevation`), il est impératif de prouver que le modèle ne se contente pas de mémoriser les coordonnées spatiales vues pendant l'entraînement. La validation croisée spatiale (Spatial CV) répond à ce besoin en testant le modèle sur des pixels qu'il n'a jamais vus.

## B. Spatial CV design
- **Grille spatiale** : La zone a été découpée en **25 blocs spatiaux** (grille 5x5) via une discrétisation par quantiles (`pd.qcut`) sur les coordonnées `north_south` et `east_west`, garantissant une taille de bloc approximativement équivalente.
- **Méthode** : Validation croisée à 5 plis (5-fold CV) utilisant `GroupKFold` sur la variable `spatial_block`. Pour chaque pli, 4/5 des blocs servent à l'entraînement et le bloc restant sert au test.
- **Données** : ~769,000 pixels d'entraînement et ~192,000 pixels de test par fold. Attention : les mêmes années temporelles peuvent apparaître dans train et test ; l'objectif exclusif ici est de tester la généralisation spatiale.

## C. Metrics comparison (Temporal vs Spatial)
The spatial CV scores indicate whether the learned relationships generalize to unseen spatial blocks, while the temporal split evaluates transfer to the unseen year 2020. Differences between the two scores should therefore be interpreted as complementary robustness diagnostics.

| Target | R2_temporal_2020 | R2_spatial_CV | Pearson_temporal_2020 | Pearson_spatial_CV | interpretation_note |
|---|---|---|---|---|---|
| delta_increment_NoCDF_minus_CDF_SSM | 0.040 | 0.121 | 0.225 | 0.350 | Spatial >= Temporal |
| increment_SSM_DA_NoCDF | 0.197 | 0.269 | 0.447 | 0.520 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_RZSM | 0.363 | 0.398 | 0.609 | 0.637 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_ET | 0.447 | 0.519 | 0.681 | 0.725 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_baseflow | 0.129 | -0.072 | 0.400 | 0.248 | Temporal > Spatial |

## D. Robust predictors
### delta_increment_NoCDF_minus_CDF_SSM
- **Top 10 temporal** : land_cover, Qsb_tavg_OPL, season, soil_texture, month, SSM_OPL, land_cover_dominant_fraction, SMC_L4_OPL, elevation, irrigation_fraction
- **Top 10 spatial** : season, land_cover, Evap_tavg_OPL, month, SMC_L1_OPL, SSM_OPL, Qsb_tavg_OPL, precipitation_model, RZSM_OPL, Qs_tavg_OPL
- **Communs (robustes)** : land_cover, Qsb_tavg_OPL, season, month, SSM_OPL
- **Disparaissent en spatial** : soil_texture, land_cover_dominant_fraction, SMC_L4_OPL, elevation, irrigation_fraction
- **Apparaissent seulement en spatial** : Evap_tavg_OPL, SMC_L1_OPL, precipitation_model, RZSM_OPL, Qs_tavg_OPL

### increment_SSM_DA_NoCDF
- **Top 10 temporal** : land_cover, Evap_tavg_OPL, SMC_L1_OPL, SSM_OPL, Qsb_tavg_OPL, season, SMC_L4_OPL, precipitation_model, soil_texture, month
- **Top 10 spatial** : Evap_tavg_OPL, land_cover, SMC_L1_OPL, SSM_OPL, precipitation_model, season, Qsb_tavg_OPL, month, Qs_tavg_OPL, SMC_L4_OPL
- **Communs (robustes)** : land_cover, Evap_tavg_OPL, SMC_L1_OPL, SSM_OPL, Qsb_tavg_OPL, season, SMC_L4_OPL, precipitation_model, month
- **Disparaissent en spatial** : soil_texture
- **Apparaissent seulement en spatial** : Qs_tavg_OPL

### delta_DA_NoCDF_minus_OPL_RZSM
- **Top 10 temporal** : RZSM_OPL, land_cover, SMC_L3_OPL, Qsb_tavg_OPL, soil_texture, SMC_L2_OPL, SMC_L4_OPL, season, Qs_tavg_OPL, SSM_OPL
- **Top 10 spatial** : RZSM_OPL, land_cover, SMC_L3_OPL, Qsb_tavg_OPL, soil_texture, SMC_L2_OPL, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL, SMC_L4_OPL
- **Communs (robustes)** : RZSM_OPL, land_cover, SMC_L3_OPL, Qsb_tavg_OPL, soil_texture, SMC_L2_OPL, SMC_L4_OPL, SSM_OPL
- **Disparaissent en spatial** : season, Qs_tavg_OPL
- **Apparaissent seulement en spatial** : SMC_L1_OPL, Evap_tavg_OPL

### delta_DA_NoCDF_minus_OPL_ET
- **Top 10 temporal** : Evap_tavg_OPL, soil_texture, Qsb_tavg_OPL, land_cover, SSM_OPL, SMC_L1_OPL, season, Qs_tavg_OPL, RZSM_OPL, SMC_L4_OPL
- **Top 10 spatial** : Evap_tavg_OPL, SSM_OPL, soil_texture, land_cover, SMC_L1_OPL, Qsb_tavg_OPL, season, SMC_L3_OPL, RZSM_OPL, month
- **Communs (robustes)** : Evap_tavg_OPL, soil_texture, Qsb_tavg_OPL, land_cover, SSM_OPL, SMC_L1_OPL, season, RZSM_OPL
- **Disparaissent en spatial** : Qs_tavg_OPL, SMC_L4_OPL
- **Apparaissent seulement en spatial** : SMC_L3_OPL, month

### delta_DA_NoCDF_minus_OPL_baseflow
- **Top 10 temporal** : land_cover, soil_texture, Qsb_tavg_OPL, SMC_L3_OPL, SMC_L1_OPL, land_cover_dominant_fraction, season, SMC_L4_OPL, SMC_L2_OPL, SSM_OPL
- **Top 10 spatial** : land_cover, soil_texture, SMC_L3_OPL, RZSM_OPL, SMC_L2_OPL, Qsb_tavg_OPL, Qs_tavg_OPL, SMC_L1_OPL, SSM_OPL, SMC_L4_OPL
- **Communs (robustes)** : land_cover, soil_texture, Qsb_tavg_OPL, SMC_L3_OPL, SMC_L1_OPL, SMC_L4_OPL, SMC_L2_OPL, SSM_OPL
- **Disparaissent en spatial** : land_cover_dominant_fraction, season
- **Apparaissent seulement en spatial** : RZSM_OPL, Qs_tavg_OPL

## E. Grouped predictor importance (Spatial CV)
### delta_increment_NoCDF_minus_CDF_SSM
| Group | Importance Sum |
|---|---|
| model_initial_state | 0.0856 |
| hydrological_fluxes_OPL | 0.0588 |
| seasonality | 0.0552 |
| static_surface | 0.0457 |
| meteorological_forcing | 0.0159 |

### increment_SSM_DA_NoCDF
| Group | Importance Sum |
|---|---|
| model_initial_state | 0.1435 |
| hydrological_fluxes_OPL | 0.1121 |
| static_surface | 0.0741 |
| seasonality | 0.0453 |
| meteorological_forcing | 0.0291 |

### delta_DA_NoCDF_minus_OPL_RZSM
| Group | Importance Sum |
|---|---|
| model_initial_state | 0.3716 |
| static_surface | 0.1613 |
| hydrological_fluxes_OPL | 0.1292 |
| seasonality | 0.0630 |
| meteorological_forcing | 0.0205 |

### delta_DA_NoCDF_minus_OPL_ET
| Group | Importance Sum |
|---|---|
| hydrological_fluxes_OPL | 0.3100 |
| model_initial_state | 0.2377 |
| static_surface | 0.1257 |
| seasonality | 0.0723 |
| meteorological_forcing | 0.0167 |

### delta_DA_NoCDF_minus_OPL_baseflow
| Group | Importance Sum |
|---|---|
| static_surface | 0.9394 |
| model_initial_state | 0.6785 |
| hydrological_fluxes_OPL | 0.1728 |
| meteorological_forcing | 0.0274 |
| seasonality | 0.0182 |

## F. Interpretation with cautious language
L'analyse **suggests** que les variables statiques (`land_cover`, `soil_texture`) sont des diagnostiques importants des incréments d'assimilation et des réponses hydrologiques associées. L'augmentation ou le maintien des scores en validation spatiale indique que cette relation est **spatially consistent with** une hétérogénéité systémique, possiblement liée à la structure du sol ou à l'occupation des terres. Le fait que `land_cover` soit robuste en validation spatiale **supports the interpretation that** les biais structurels de l'OPL sur certaines végétations sont corrigés par l'assimilation.

## G. Limitations
- Le RF n'est pas un modèle physique causal ; il ne fait que capturer des associations statistiques.
- La résolution des données statiques (5km) pourrait masquer des hétérogénéités locales plus fines (ex: parcelles irriguées sous-résolues).

## H. Limitations and future extension
- Precipitation error (`precipitation_error`) from in-situ gauges is not included in V0.2 because the currently available station dataset ends before the SMAP assimilation period (2016-2020).
- The current RF/XAI analysis therefore explains SMAP increments and hydrological responses using model initial states, hydrological fluxes, static surface properties, seasonality, and model precipitation forcing.
- Future work will include precipitation-error attribution once updated in-situ precipitation data covering 2016–2020 are available.
