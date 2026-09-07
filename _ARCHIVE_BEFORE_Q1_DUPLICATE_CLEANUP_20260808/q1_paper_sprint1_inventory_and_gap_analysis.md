# Q1 Paper Sprint 1: Inventory and Gap Analysis

## A. Scope actuel du papier
- **Période** : 2016–2020
- **Domaine** : Nord du Maroc
- **Expériences** : OPL (Open-Loop), DA-NoCDF (Assimilation sans CDF matching), DA-CDF (Assimilation avec CDF matching)
- **Irrigation** : OFF (désactivée)
- **HyMAP** : Non inclus dans cette version
- **Pluie in situ** : Non incluse (les stations s’arrêtent en 2014)
- **RF/XAI** : Disponible jusqu’à la version V0.2
- **Objectif principal** : Diagnostic de propagation hydrologique pré-routing (analyse des impacts d'assimilation SMAP sur les variables hydrologiques avant routage).

## B. Liste complète des datasets et outputs

| Fichier / Dossier | Rôle scientifique | Statut | Remarque |
| --- | --- | --- | --- |
| `IA_SM_assim/data/processed/monthly_pixel_dataset_2016_2020.parquet` (Dataset V0) | Dataset de base pour RF | Archive | |
| `IA_SM_assim/data/processed/monthly_pixel_dataset_2016_2020_static.parquet` (Dataset V0.1/V0.2) | Dataset avec variables statiques (topo, soil, veg) | Main paper | Utilisé pour V0.2 spatial CV |
| `IA_SM_assim/outputs/tables/rf_metrics_v02_spatial_cv.csv` | Performances du modèle RF (R2, Pearson) | Main paper | Validation croisée spatiale robuste |
| `IA_SM_assim/outputs/tables/rf_feature_importance_v02_spatial_cv.csv` | Importance des facteurs explicatifs | Main paper | Base de l'interprétation XAI |
| `IA_SM_assim/outputs/figures/*v02*.png` | Figures principales d'explicabilité | Main paper / Supplementary | Prêtes pour l'article |
| `NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/` (Output netCDF) | Résultats bruts Noah-MP LIS | Archive | Base des post-traitements |
| `NoahMP_Morocco/scripts/postproc/_ARCHIVE_TO_REVIEW_AFTER_CLEANUP_20260712/` | Anciennes figures (draft précédent) | À refaire | Nécessite une mise à jour via la nouvelle pipeline propre |

## C. Vérification des figures déjà disponibles

| figure_file | suggested_paper_figure_number | section | main_or_supplement | message | issue_to_fix |
| --- | --- | --- | --- | --- | --- |
| `multi-year SMAP diagnostics (draft archive)` | Fig 1 | 3.1 | Main | Nombre d'obs et innovations | À refaire avec la pipeline standardisée |
| `seasonal SSM DA-NoCDF vs OL (draft archive)` | Fig 2 | 3.2 | Main | Impact direct de l'assimilation selon la saison | À refaire / standardiser |
| `runoff seasonal OL vs DA-NoCDF (draft archive)` | Fig 3 | 3.4 | Main | Partitionnement de l'écoulement | À refaire / vérifier les cartes |
| `precipitation/runoff components DA-NoCDF (draft archive)` | Fig 4 | 3.4 | Main | Réponse de l'écoulement de base vs surface | À refaire / standardiser |
| `precipitation/runoff DA-CDF (draft archive)` | Fig 5 | 3.5 | Supplementary | La correction de biais CDF masque l'impact hydrologique | Vérifier le contraste presque nul |
| `rf_temporal_vs_spatial_cv_v02.png` | Fig 6 | 3.6 | Supplementary | Le modèle RF est robuste spatialement | Aucune, prête |
| `rf_model_skill_v02_spatial_cv.png` | Fig 7 | 3.6 | Main | Forte capacité prédictive pour l'ET et RZSM | Aucune, prête |
| `rf_grouped_feature_importance_v02.png` | Fig 8 | 3.7 | Main | Le forçage hydroclimatique domine sur le statique | Aucune, prête |
| `rf_feature_importance_v02_spatial_cv.png` | Fig 9 | 3.7 | Supplementary | Détail par variable spécifique | Aucune, prête |

## D. Problèmes critiques à corriger

1. **Incohérence possible du forçage pluie :**
   - **Vérification** : Dans le fichier `lis_opl.config.template`, la configuration indique : `Met forcing sources: "MERRA2" "GPM IMERG"` avec la méthode `overlay`. IMERG écrase MERRA2 pour la précipitation. 
   - **Conclusion** : La source réelle du modèle de précipitation (`Rainf_tavg`) est **IMERG** (version finale V07B). MERRA-2 fournit les autres forçages.
   - **Label correct à utiliser** : "IMERG" pour la précipitation.
   - **Correction dans le manuscrit** : S'assurer que le manuscrit précise clairement l'hybridation des forçages (MERRA-2 + IMERG overlay).

2. **Figure DA-CDF runoff :**
   - **Diagnostic** : Le runoff DA-CDF semble visuellement identique à l'OPL, ce n'est pas un bug de plotting, les différences sont mathématiquement très faibles mais non nulles.
   - **DA-CDF − OPL total runoff** :
     - DJF : min=-27.67, mean=0.049, max=107.95
     - JJA : min=-17.09, mean=-0.013, max=99.09
   - **DA-CDF − OPL surface runoff (Qs)** :
     - DJF : min=-6.02, mean=0.002, max=12.45
     - JJA : min=-0.62, mean=0.001, max=2.02
   - **DA-CDF − OPL baseflow (Qsb)** :
     - DJF : min=-25.69, mean=0.047, max=104.91
     - JJA : min=-16.72, mean=-0.014, max=98.91
   - **Conclusion** : Les moyennes de différence sont pratiquement nulles, justifiant visuellement l'absence d'impact significatif comparé à DA-NoCDF.

3. **Drought-class transitions :**
   - **Statut** : Non présentes de manière consolidée dans la version propre actuelle (des scripts exploratoires anciens existent).
   - **Recommandation** : À ajouter comme *future work* ou *supplementary* pour ne pas retarder Q1.

4. **Water-balance diagnostic :**
   - **Disponibilité** : Oui. Les variables `Rainf_tavg` (P), `Evap_tavg` (ET), `Qs_tavg` (Qs), `Qsb_tavg` (Qsb), et `SMC_L1_L4` (dS soil) sont disponibles dans le dataset pour un bilan de premier ordre. Le bilan de la nappe (`WaterTableD` / `WT`) est également accessible.
   - **Action** : Calculable facilement, mais pas prioritaire pour bloquer la soumission.

## E. Résultats numériques déjà disponibles

### 1. Seasonal SSM response
- **OL DJF mean** : 0.1902
- **DA-NoCDF DJF mean** : 0.1571
- **Δ DJF mean** : -0.0331
- **% pixels negative/positive DJF** : 81.64% negative / 18.36% positive
- **OL JJA mean** : 0.0914
- **DA-NoCDF JJA mean** : 0.0978
- **Δ JJA mean** : +0.0063
- **% pixels negative/positive JJA** : 27.74% negative / 72.26% positive

### 2. Runoff partitioning DA-NoCDF
- **Precipitation DJF mean** : 20.96 mm/mois
- **Precipitation JJA mean** : 6.25 mm/mois
- **Δ total runoff DJF mean** : +1.750
- **Δ total runoff JJA mean** : +0.348
- **Δ surface runoff (Qs) DJF mean** : +0.118
- **Δ surface runoff (Qs) JJA mean** : +0.008
- **Δ baseflow (Qsb) DJF mean** : +1.631
- **Δ baseflow (Qsb) JJA mean** : +0.339
*(Le drainage profond domine largement la réponse du runoff).*

### 3. ET/GPP evaluation
- **Disponibilité** : Les tables quantitatives de validation (GLEAM, FLUXSAT) doivent être mises à jour / vérifiées via les scripts de post-processing récents. L'inventaire de données existe (`NoahMP_Morocco/reports/inventory_gleam.csv`).
- **Statut** : À vérifier.

### 4. RF V0.1/V0.2
- **R2 (Spatial CV, V0.2)** : RZSM=0.39, ET=0.51, Baseflow=-0.07, SSM=0.26
- **Top predictors robustes** : `Rainf_tavg_OPL`, `SMC_L*`, `month/season`.
- **Grouped importance** : Les facteurs dynamiques hydrologiques/météorologiques expliquent l'essentiel de la variance, tandis que les facteurs géographiques statiques (topo, sol) sont mineurs.

## F. Structure Q1 recommandée

1. **Introduction**
2. **Data and Methods**
3. **Results**
   - **3.1 Multi-year assimilation behavior and CDF sensitivity** : (Fig. Main: Séries temporelles d'innovations. Suppl: Cartes du biais initial). *À discuter : Le biais systématique du modèle justifie l'impact.*
   - **3.2 Seasonal SSM response** : (Fig. Main: Cartes DJF vs JJA). *À discuter : Le modèle s'assèche en hiver et s'humidifie en été, consistent avec les corrections.*
   - **3.3 ET/GPP response** : (Fig. Main: Anomalies ET). *Manquant: Les tables de validation.*
   - **3.4 Runoff partitioning and baseflow response** : (Fig. Main: Scatter ou bar plots DA-NoCDF - OL). *À discuter : La propagation est largement capturée par le baseflow.*
   - **3.5 CDF vs NoCDF hydrological contrast** : (Fig. Suppl: DA-CDF Runoff vs OPL). *À discuter : Le CDF matching écrase le signal hydrologique.*
   - **3.6 RF predictive skill and spatial robustness** : (Fig. Main: `rf_model_skill_v02_spatial_cv.png`). *À discuter : La fiabilité de l'explicabilité basée sur de bonnes prédictions RF.*
   - **3.7 RF attribution of assimilation responses** : (Fig. Main: `rf_grouped_feature_importance_v02.png`, Suppl: individuelles). *À discuter : Les incréments sont conditionnés par l'état hydrique (SMC) et le forçage (Precip).*
   - **3.8 Integrated interpretation**
4. **Discussion**
5. **Conclusions**

## G. Liste priorisée des prochaines actions

**Priority 1 (Indispensable pour Q1)**
- Refaire / corriger la figure DA-CDF hydrologique propre.
- Produire la figure "CDF vs NoCDF hydrological response" de manière lisible.
- Corriger le texte concernant la precipitation-error / in-situ pour bien spécifier IMERG.
- Créer un workflow propre et standardisé pour générer les figures hydrologiques.

**Priority 2 (Utile, supplementary)**
- Mettre à jour les tables de validation ET / GPP.
- Produire des cartes des prédicteurs statiques (static predictor maps).
- Produire un *water-balance first-order diagnostic* léger (tableau).

**Priority 3 (Future work)**
- Drought-class transitions.
- Évaluation via routage (HyMAP).
