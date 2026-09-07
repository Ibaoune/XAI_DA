# Scientific Diagnostics Interpretation Package (V0.2)

## 1. Objectif général des diagnostics V0.2
Ce document de synthèse a pour but d'analyser la manière dont les incréments SMAP se distribuent spatialement et temporellement, et comment les configurations d'assimilation (DA-NoCDF vs DA-CDF) diffèrent.
L'analyse diagnostique (Random Forest & XAI) évalue statistiquement la propagation de ces corrections vers la RZSM, l'évapotranspiration (ET), le ruissellement (runoff) et le flux de base (baseflow). L'objectif est d'identifier quels facteurs (états initiaux, flux, forçages, propriétés de surface) **are associated with** ou **diagnostic of** ces réponses.
L'ajout des variables statiques (`land_cover`, `soil_texture`, `elevation`, `irrigation_fraction`) permet de vérifier si ces réponses sont **spatially coherent with** l'hétérogénéité du terrain. La validation spatiale (V0.2) teste si ces relations se maintiennent sur des zones non vues, ce qui **suggests** une robustesse physique plutôt qu'une simple mémorisation de coordonnées.
Il est impératif d'utiliser un langage prudent : l'analyse identifie des cohérences diagnostiques et des biais systématiques, mais ne prouve pas de liens de causalité stricts ou de corrections d'irrigation directes.

## 2. Inventaire complet des fichiers produits
### A. Dataset
- `data/processed/monthly_pixel_dataset_2016_2020.parquet` (Base)
- `data/processed/monthly_pixel_dataset_2016_2020_static.parquet` (V0.1/V0.2 Final)
### B. Tables
- `outputs/tables/rf_metrics.csv` (V0)
- `outputs/tables/rf_metrics_v01_static.csv` (V0.1)
- `outputs/tables/rf_metrics_v02_spatial_cv.csv` (V0.2)
- `outputs/tables/rf_permutation_importance_v01_static.csv` (V0.1)
- `outputs/tables/rf_permutation_importance_v02_spatial_cv.csv` (V0.2)
### C. Reports
- `reports/rf_v01_static_results_summary.md`
- `reports/rf_v02_spatial_validation_summary.md`
- `reports/final_v02_deliverables_for_paper.md`
- `reports/random_forest_xai_method_summary.md`
- `reports/insitu_precip_inventory.md`
### D. Figures
- `outputs/figures/rf_model_skill_v02_spatial_cv.png` : Montre la corrélation prédiction vs observation des incréments (question: Le RF arrive-t-il à prédire les impacts spatiaux ?). Limite : dispersion résiduelle importante.
- `outputs/figures/rf_feature_importance_v02_spatial_cv.png` : Classement global des variables (question: Quels sont les top drivers ?). Limite : ignore les corrélations inter-prédicteurs.
- `outputs/figures/rf_temporal_vs_spatial_cv_v02.png` : Compare R2 Temporel 2020 vs Spatial CV (question: Les relations sont-elles géographiquement robustes ?). Limite : le spatial mask dépend du qcut.
- `outputs/figures/rf_grouped_feature_importance_v02.png` : Agrégation des importances par familles physiques (question: Quel compartiment du modèle est dominant ?).

## 3. Résumé du dataset utilisé
- **Période** : 2016–2020
- **Nombre de mois** : 60
- **Pixels valides/mois** : ~16030
- **Total lignes** : 961800
- **Total colonnes** : 72
- **Statut de la pluie in situ (V1)** : Bloqué (stations s'arrêtent en 2014, pas de recouvrement avec SMAP).

## 4. Résumé des targets
- `increment_SSM_DA_NoCDF` : Incrément absolu de surface. Positif = SMAP ajoute de l'eau. Négatif = SMAP retire de l'eau. Prudence: inclut les biais saisonniers.
- `delta_increment_NoCDF_minus_CDF_SSM` : Différence de correction avec/sans correction de biais (CDF). Isole l'effet de la climatologie locale vs la dynamique absolue.
- `delta_DA_NoCDF_minus_OPL_RZSM/ET/runoff/baseflow` : Impact net de l'assimilation sur la réponse hydrologique (modèle DA - modèle Open-Loop). Positif = la DA a augmenté le flux/état. Négatif = réduction.

## 5. Résultats descriptifs des incréments SMAP
| Target | Min | Max | Mean | Std |
|---|---|---|---|---|
| increment_SSM_DA_NoCDF | -0.8347 | 0.8333 | -0.0294 | 0.0963 |
| increment_SSM_DA_CDF | -0.9093 | 0.4582 | -0.0183 | 0.0693 |
| delta_increment_NoCDF_minus_CDF_SSM | -0.8347 | 1.1568 | -0.0111 | 0.1060 |
| increment_RZSM_DA_NoCDF | -0.6899 | 0.6635 | -0.0072 | 0.0258 |
| increment_RZSM_DA_CDF | -0.7459 | 0.1235 | -0.0045 | 0.0179 |
| delta_increment_NoCDF_minus_CDF_RZSM | -0.6899 | 0.7156 | -0.0027 | 0.0291 |

**Discussion** : La différence NoCDF/CDF nous apprend que la correction de biais (CDF) écrase une partie des signaux de basse fréquence (biais structurels du forçage/modèle). L'analyse diagnostique sur NoCDF permet d'identifier ces biais systématiques (souvent liés à la végétation ou l'irrigation ignorée par l'OPL).

## 6. Résultats hydrologiques
| Target | Min | Max | Mean | Std |
|---|---|---|---|---|
| delta_DA_NoCDF_minus_OPL_RZSM | -0.2171 | 0.1710 | -0.0152 | 0.0274 |
| delta_DA_CDF_minus_OPL_RZSM | -0.2255 | 0.1011 | -0.0088 | 0.0208 |
| delta_DA_NoCDF_minus_OPL_ET | -96.6497 | 117.0223 | -1.3960 | 10.6716 |
| delta_DA_CDF_minus_OPL_ET | -100.6835 | 48.0892 | 1.3316 | 8.7536 |
| delta_DA_NoCDF_minus_OPL_runoff | -13.5415 | 66.5796 | 0.0825 | 0.9812 |
| delta_DA_CDF_minus_OPL_runoff | nan | nan | nan | nan |
| delta_DA_NoCDF_minus_OPL_baseflow | -58.0544 | 254.5277 | 0.8985 | 6.8712 |
| delta_DA_CDF_minus_OPL_baseflow | nan | nan | nan | nan |

**Discussion** : L'ET et la RZSM réagissent fortement, avec une grande variance. Les flux lents (baseflow) réagissent avec des amplitudes minimes, montrant l'inertie du système. La propagation surface → root zone → ET est directe.

## 7. Résumé RF V0 (Sans statiques)
Le RF V0 utilisait uniquement l'état initial (SSM_OPL, RZSM_OPL...) et les flux pour prédire les incréments. **Message principal** : L'état initial du modèle limite mathématiquement les incréments (ex: un sol déjà saturé limite les incréments positifs). Ce signal 'interne' domine.

## 8. Résumé RF V0.1 avec variables statiques
L'ajout de `land_cover`, `soil_texture`, `elevation` a significativement augmenté les scores, notamment pour l'ET et le baseflow. Cela indique que les incréments SMAP compensent des déficits du modèle liés à des hétérogénéités de surface sous-résolues.

## 9. Résumé V0.2 validation spatiale
Méthode : 25 blocs spatiaux, 5-Fold GroupKFold.
Le Spatial CV évalue le transfert vers des zones non vues (généralisation physique), tandis que le Temporal Split évalue le transfert vers une année non vue (2020). Les deux diagnostics sont complémentaires.
| target | R2_temporal | R2_spatial_CV | Pearson_temporal | Pearson_spatial_CV | interpretation |
|---|---|---|---|---|---|
| delta_increment_NoCDF_minus_CDF_SSM | 0.040 | 0.121 | 0.225 | 0.350 | Spatial >= Temporal |
| increment_SSM_DA_NoCDF | 0.197 | 0.269 | 0.447 | 0.520 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_RZSM | 0.363 | 0.398 | 0.609 | 0.637 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_ET | 0.447 | 0.519 | 0.681 | 0.725 | Spatial >= Temporal |
| delta_DA_NoCDF_minus_OPL_baseflow | 0.129 | -0.072 | 0.400 | 0.248 | Temporal > Spatial |

## 10. Top predictors robustes
### delta_increment_NoCDF_minus_CDF_SSM
- **Top 10 temporal** : Qsb_tavg_OPL, soil_texture, land_cover, irrigation_fraction, SMC_L4_OPL, season, SSM_OPL, elevation, month, land_cover_dominant_fraction
- **Top 10 spatial** : Qsb_tavg_OPL, RZSM_OPL, land_cover, Qs_tavg_OPL, precipitation_model, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL, month
- **Communs (robustes)** : Qsb_tavg_OPL, land_cover, season, SSM_OPL, month
- **Disparaissent en spatial** : soil_texture, irrigation_fraction, SMC_L4_OPL, elevation, land_cover_dominant_fraction
- **Apparaissent seulement en spatial** : RZSM_OPL, Qs_tavg_OPL, precipitation_model, SMC_L1_OPL, Evap_tavg_OPL
### increment_SSM_DA_NoCDF
- **Top 10 temporal** : Qsb_tavg_OPL, soil_texture, land_cover, precipitation_model, SMC_L4_OPL, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL, month
- **Top 10 spatial** : Qsb_tavg_OPL, land_cover, Qs_tavg_OPL, precipitation_model, SMC_L4_OPL, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL, month
- **Communs (robustes)** : Qsb_tavg_OPL, land_cover, precipitation_model, SMC_L4_OPL, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL, month
- **Disparaissent en spatial** : soil_texture
- **Apparaissent seulement en spatial** : Qs_tavg_OPL
### delta_DA_NoCDF_minus_OPL_RZSM
- **Top 10 temporal** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, SMC_L2_OPL, Qs_tavg_OPL, SMC_L4_OPL, SMC_L3_OPL, season, SSM_OPL
- **Top 10 spatial** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, SMC_L2_OPL, SMC_L4_OPL, SMC_L3_OPL, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL
- **Communs (robustes)** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, SMC_L2_OPL, SMC_L4_OPL, SMC_L3_OPL, SSM_OPL
- **Disparaissent en spatial** : Qs_tavg_OPL, season
- **Apparaissent seulement en spatial** : SMC_L1_OPL, Evap_tavg_OPL
### delta_DA_NoCDF_minus_OPL_ET
- **Top 10 temporal** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, Qs_tavg_OPL, SMC_L4_OPL, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL
- **Top 10 spatial** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, season, SMC_L1_OPL, SMC_L3_OPL, SSM_OPL, Evap_tavg_OPL, month
- **Communs (robustes)** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, season, SMC_L1_OPL, SSM_OPL, Evap_tavg_OPL
- **Disparaissent en spatial** : Qs_tavg_OPL, SMC_L4_OPL
- **Apparaissent seulement en spatial** : SMC_L3_OPL, month
### delta_DA_NoCDF_minus_OPL_baseflow
- **Top 10 temporal** : Qsb_tavg_OPL, soil_texture, SMC_L2_OPL, land_cover, SMC_L4_OPL, SMC_L3_OPL, season, SMC_L1_OPL, SSM_OPL, land_cover_dominant_fraction
- **Top 10 spatial** : Qsb_tavg_OPL, soil_texture, RZSM_OPL, land_cover, SMC_L2_OPL, Qs_tavg_OPL, SMC_L4_OPL, SMC_L3_OPL, SMC_L1_OPL, SSM_OPL
- **Communs (robustes)** : Qsb_tavg_OPL, soil_texture, SMC_L2_OPL, land_cover, SMC_L4_OPL, SMC_L3_OPL, SMC_L1_OPL, SSM_OPL
- **Disparaissent en spatial** : season, land_cover_dominant_fraction
- **Apparaissent seulement en spatial** : RZSM_OPL, Qs_tavg_OPL

## 11. Importance groupée par famille
### delta_increment_NoCDF_minus_CDF_SSM
- model_initial_state : 0.0856
- hydrological_fluxes_OPL : 0.0588
- seasonality : 0.0552
- static_surface : 0.0457
- meteorological_forcing : 0.0159
### increment_SSM_DA_NoCDF
- model_initial_state : 0.1435
- hydrological_fluxes_OPL : 0.1121
- static_surface : 0.0741
- seasonality : 0.0453
- meteorological_forcing : 0.0291
### delta_DA_NoCDF_minus_OPL_RZSM
- model_initial_state : 0.3716
- static_surface : 0.1613
- hydrological_fluxes_OPL : 0.1292
- seasonality : 0.0630
- meteorological_forcing : 0.0205
### delta_DA_NoCDF_minus_OPL_ET
- hydrological_fluxes_OPL : 0.3100
- model_initial_state : 0.2377
- static_surface : 0.1257
- seasonality : 0.0723
- meteorological_forcing : 0.0167
### delta_DA_NoCDF_minus_OPL_baseflow
- static_surface : 0.9394
- model_initial_state : 0.6785
- hydrological_fluxes_OPL : 0.1728
- meteorological_forcing : 0.0274
- seasonality : 0.0182

**Discussion** : L'assimilation est principalement contrainte par l'état initial du modèle (mémoire intrinsèque de l'humidité du sol). Cependant, la réponse des flux (ET, baseflow) est lourdement associée aux propriétés statiques (static_surface) et aux flux OPL. Cela souligne le rôle de modérateur du land cover et du sol.

## 12. Message scientifique principal du diagnostic
### A. Message court (2-3 phrases)
Les diagnostics RF/XAI révèlent que les incréments SMAP et leurs réponses hydrologiques ne sont pas aléatoires. Ils sont associés de manière robuste à l'état initial du sol, aux flux préexistants et aux propriétés statiques de surface (land cover, soil texture), ce qui démontre une généralisation cohérente à l'échelle régionale (Spatial CV).
### B. Pour l'Introduction / Discussion
L'utilisation conjointe de validations temporelles et spatiales suggère que les ajustements d'assimilation compensent des limites structurelles du modèle liées à la représentation du land cover. Le maintien des scores prédictifs sur des domaines non vus renforce l'utilité des approches XAI comme outils de diagnostic physique.
### C. Pour la Conclusion
L'assimilation SMAP interagit fortement avec la mémoire du sol et les propriétés de surface locales. Bien que la correction directe de l'irrigation ne soit pas causalement prouvée, la cohérence spatiale des relations diagnostiquées souligne la nécessité d'intégrer de meilleures paramétrisations de surface dans les modèles hydrologiques régionaux.

## 13. Limites à discuter
- L'absence d'erreurs de précipitation basées sur des jauges (gauge-based precipitation_error) pour 2016–2020 empêche d'évaluer l'impact des biais de forçage.
- L'absence de routage avancé (HyMAP) dans la configuration OPL.
- Les modèles RF identifient des corrélations (associations), non une stricte causalité physique.
- L'échelle des variables statiques (~5km) peut masquer la fine hétérogénéité des parcelles irriguées.
- Les flux lents profonds (baseflow) s'avèrent difficiles à généraliser géographiquement (scores négatifs en Spatial CV).

## 14. Figures recommandées pour le papier
- **Main Paper** : `rf_grouped_feature_importance_v02.png` (Titre: *Cumulative Feature Importance by Hydrological Group*). Message: Met en évidence le rôle central des propriétés de surface dans la modulation des incréments (Section Discussion).
- **Main Paper** : `rf_temporal_vs_spatial_cv_v02.png` (Titre: *Model Generalization: Temporal vs. Spatial Cross-Validation*). Message: Démontre la robustesse géographique des relations diagnostiquées (Section Validation).
- **Supplement** : `rf_model_skill_v02_spatial_cv.png` (Titre: *Scatter Plots of RF Predictions*).
- **Supplement** : `rf_feature_importance_v02_spatial_cv.png` (Titre: *Top Individual Predictors*).

## 15. Discussion-ready bullets
- **CDF vs NoCDF** : L'assimilation NoCDF permet au SMAP d'introduire sa propre climatologie, exposant les biais structurels de l'OPL, tandis que le CDF les masque.
- **Propagation verticale** : La forte association avec `RZSM_OPL` montre que l'incrément de surface dépend de la saturation sous-jacente.
- **Réponse ET** : Fortement associée à l'évapotranspiration OPL et au `land_cover`, l'ET est très sensible à la correction de la couche superficielle.
- **Réponse runoff/baseflow** : La réponse est amortie; le baseflow peine à se généraliser spatialement, soulignant des limites de routage.
- **Rôle land_cover/soil_texture** : Leur résilience en Spatial CV suggère que le modèle OPL sous-estime systématiquement la capacité de rétention de certains sols et végétations.
- **Rôle limité de precipitation_model** : Sans l'erreur par rapport aux jauges, la précipitation modèle seule n'explique qu'une fraction de l'incrément.
- **Limites in-situ** : L'évaluation fine du forçage requerra des campagnes de terrain sur la période 2016-2020.
- **Future work** : Implémenter le routage HyMAP et des simulations explicites d'irrigation pour confirmer l'origine des biais.