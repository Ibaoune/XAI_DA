# Sprint Cleanup 2: Final Architecture Plan

## 1. Executive Summary
This document outlines the final, clean architectural plan for the twin projects (`NoahMP_Morocco/scripts/postproc/` and `IA_SM_assim/`). The primary objective is to separate hydrological diagnostics (which belong to the post-processing framework) from Machine Learning experiments (which belong to the IA project). No files have been deleted or moved yet; this is a strictly read-only audit to prepare for the migration phase. The plan eliminates temporary `scratch_*.py` files by archiving them, deprecates the `q1_` naming convention in favor of manuscript-ready names, and defines clear Git and migration strategies.

## 2. Final Target Architecture

### A. Architecture finale côté NoahMP_Morocco/scripts/postproc/
```text
NoahMP_Morocco/scripts/postproc/
├── configs/
│   ├── global.yaml
│   ├── experiments.yaml
│   └── figures/
│       ├── manuscript_assimilation.yaml
│       ├── manuscript_hydrological_response.yaml
│       └── manuscript_water_balance.yaml
│
├── src/
│   ├── assimilation_diagnostics/
│   │   └── inventory_smap_da_diagnostics.py
│   ├── hydrological_response/
│   │   └── hydrological_response_cdf_nocdf.py
│   ├── water_balance/
│   │   └── flux_only_water_balance.py
│   └── plotting/
│       └── manuscript_plot_utils.py
│
├── matrix_2016_2020/
│   └── outputs/
│       ├── figures/
│       │   ├── assimilation_diagnostics/
│       │   ├── hydrological_response/
│       │   ├── runoff_partitioning/
│       │   ├── water_balance/
│       │   └── manuscript_selected/
│       └── tables/
│           ├── hydrological_response_summary_2016_2020.csv
│           ├── hydrological_response_key_numbers_2016_2020.csv
│           └── flux_only_water_balance_annual_seasonal_2016_2020.csv
│
├── scripts/
│   ├── run_manuscript_assimilation_figures.sh
│   ├── run_manuscript_hydrological_response_figures.sh
│   └── run_manuscript_water_balance.sh
│
└── docs/
    ├── manuscript_figure_inventory.md
    ├── manuscript_figure_reproduction.md
    ├── hydrological_response_results_text.md
    └── manuscript_captions_hydrology.md
```

### B. Architecture finale côté IA_SM_assim/
```text
IA_SM_assim/
├── config.yaml
├── src/
│   ├── build_dataset/
│   ├── train_rf/
│   ├── plot_rf_xai/
│   └── reports/
│
├── outputs/
│   ├── tables/
│   │   ├── rf_metrics_temporal.csv
│   │   ├── rf_metrics_spatial_cv.csv
│   │   ├── rf_permutation_importance_temporal.csv
│   │   └── rf_permutation_importance_spatial_cv.csv
│   ├── figures/
│   │   ├── rf_skill/
│   │   ├── rf_importance/
│   │   ├── rf_grouped_importance/
│   │   └── manuscript_selected/
│   └── models/
│
├── reports/
│   ├── rf_xai_method_summary.md
│   ├── rf_xai_results_summary.md
│   ├── rf_xai_figure_inventory.md
│   └── rf_xai_reproduction_guide.md
│
├── jobs/
│   ├── job_build_dataset_cpu.sh
│   ├── job_train_rf_cpu.sh
│   └── run_rf_xai_figures.sh
│
└── scratch/
    └── scratch_*.py
```

## 3. File Classification Table

| current_path | current_file | category | final_project | final_path | final_name | action | reason | risk |
|---|---|---|---|---|---|---|---|---|
| `IA_SM_assim/src/` | `00_find_smap_da_diagnostics.py` | hydrological_script | `NoahMP_Morocco` | `src/assimilation_diagnostics/` | `inventory_smap_da_diagnostics.py` | `copy_and_refactor` | DA diagnostic logic | Hardcoded paths |
| `IA_SM_assim/src/` | `09_generate_diagnostic_package.py` | sprint_working_report | `IA_SM_assim` | `archive/` (or `src/reports/`) | `09_generate_diagnostic_package.py` | `archive_only` | Mixes RF and hydro reporting | None |
| `IA_SM_assim/src/` | `10_hydrological_response_cdf_nocdf.py` | hydrological_script | `NoahMP_Morocco` | `src/hydrological_response/` | `hydrological_response_cdf_nocdf.py` | `copy_and_refactor` | Core hydro plotting | Hardcoded paths |
| `IA_SM_assim/outputs/figures/` | `q1_fig_first_order_water_balance.png` | hydrological_figure | `NoahMP_Morocco` | `matrix_2016_2020/outputs/figures/water_balance/` | `manuscript_flux_only_water_balance_2016_2020.png` | `copy_to_postproc` | Water balance | Breaks MD links |
| `IA_SM_assim/outputs/figures/` | `q1_fig_hydrological_response_*.png` | hydrological_figure | `NoahMP_Morocco` | `matrix_2016_2020/outputs/figures/hydrological_response/` | `manuscript_hydro_response_*.png` | `copy_to_postproc` | Hydro analysis | Breaks MD links |
| `IA_SM_assim/outputs/tables/` | `q1_hydrological_response_summary.csv` | hydrological_table | `NoahMP_Morocco` | `matrix_2016_2020/outputs/tables/` | `hydrological_response_summary_2016_2020.csv` | `copy_to_postproc` | Hydro tables | None |
| `IA_SM_assim/reports/` | `q1_sprint2_results_text_hydrological_response.md` | manuscript_caption_or_text | `NoahMP_Morocco` | `docs/` | `hydrological_response_results_text.md` | `copy_to_postproc` | Paper text | None |
| `IA_SM_assim/reports/` | `q1_sprint2_manuscript_captions.md` | manuscript_caption_or_text | `NoahMP_Morocco` | `docs/` | `manuscript_captions_hydrology.md` | `copy_to_postproc` | Paper text | None |
| `IA_SM_assim/reports/` | `q1_sprint1_figures_selected.zip` | sprint_working_report | `IA_SM_assim` | `archive/` | `sprint1_figures_selected.zip` | `archive_only` | Outdated | None |
| `IA_SM_assim/` | `scratch_compute.py` | scratch | `IA_SM_assim` | `scratch/` | `scratch_compute.py` | `archive_only` | Temporary code | None |

## 4. Script Dependency Audit

### `IA_SM_assim/src/00_find_smap_da_diagnostics.py`
- **Imports:** `os`, `glob`, `Path`, `xarray as xr`.
- **Hardcoded paths:** `base_dir = ".../NoahMP_Morocco"`, `reports/smap_da_diagnostics_inventory.md`.
- **Files read:** Scans NoahMP output directories for `.nc` files.
- **Files written:** `reports/smap_da_diagnostics_inventory.md`.
- **Dependencies:** None to `config.yaml` or local utils.
- **Conclusion:** `copy_and_refactor` to `postproc/src/assimilation_diagnostics/`. Need to adjust output path to `docs/` or `reports/`.

### `IA_SM_assim/src/09_generate_diagnostic_package.py`
- **Imports:** `pandas`, `numpy`, `os`, `shutil`.
- **Hardcoded paths:** `data/processed/monthly_pixel_dataset_2016_2020_static.parquet`, `outputs/tables/`, `outputs/figures/`, `reports/`.
- **Files read:** RF metrics, permutation importance CSVs, parquet dataset.
- **Files written:** Markdown package summary, zip archive of figures.
- **Dependencies:** None to `config.yaml` or local utils.
- **Conclusion:** `archive_only` or `keep_in_IA`. It mixes RF results and hydrological interpretations in a one-shot sprint summary script.

### `IA_SM_assim/src/10_hydrological_response_cdf_nocdf.py`
- **Imports:** `pandas`, `numpy`, `matplotlib.pyplot`, `matplotlib.colors`, `os`.
- **Hardcoded paths:** `data/processed/monthly_pixel_dataset_2016_2020_static.parquet`, `outputs/figures/q1_*`, `outputs/tables/q1_*`.
- **Files read:** Parquet dataset.
- **Files written:** Hydrological response maps, water balance bar plots, CSV summaries, markdown tables.
- **Dependencies:** None to `config.yaml` or local utils.
- **Conclusion:** `copy_and_refactor` to `postproc/src/hydrological_response/`. The data loading logic must point to the correct postproc dataset path, and the output paths must point to the new `matrix_2016_2020/outputs/` structure.

## 5. Proposed Rename Table

| Original Name | Proposed Clean Name | Project Destination |
|---|---|---|
| `q1_fig_hydrological_response_states_ET_annual_2016_2020.png` | `manuscript_hydro_response_states_ET_annual_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_hydrological_response_states_ET_DJF_2016_2020.png` | `manuscript_hydro_response_states_ET_DJF_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_hydrological_response_states_ET_JJA_2016_2020.png` | `manuscript_hydro_response_states_ET_JJA_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_hydrological_response_runoff_annual_2016_2020.png` | `manuscript_runoff_partitioning_annual_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_hydrological_response_runoff_DJF_2016_2020.png` | `manuscript_runoff_partitioning_DJF_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_hydrological_response_runoff_JJA_2016_2020.png` | `manuscript_runoff_partitioning_JJA_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_first_order_water_balance.png` | `manuscript_flux_only_water_balance_2016_2020.png` | NoahMP_Morocco |
| `q1_fig_precip_runoff_components_DA_CDF_IMERG_2016_2020.png` | `manuscript_assim_diagnostics_precip_runoff_components_DA_CDF.png` | NoahMP_Morocco |
| `q1_fig_precip_runoff_components_DA_NoCDF_IMERG_2016_2020.png`| `manuscript_assim_diagnostics_precip_runoff_components_DA_NoCDF.png`| NoahMP_Morocco |
| `q1_hydrological_response_summary.csv` | `hydrological_response_summary_2016_2020.csv` | NoahMP_Morocco |
| `q1_hydrological_response_key_numbers.csv` | `hydrological_response_key_numbers_2016_2020.csv` | NoahMP_Morocco |
| `q1_first_order_water_balance_annual_seasonal.csv` | `flux_only_water_balance_annual_seasonal_2016_2020.csv` | NoahMP_Morocco |
| `rf_temporal_vs_spatial_cv_v02.png` | `manuscript_rf_temporal_vs_spatial_cv.png` | IA_SM_assim |
| `rf_grouped_feature_importance_v02.png` | `manuscript_rf_grouped_feature_importance.png` | IA_SM_assim |

## 6. Proposed Documentation Files

### `NoahMP_Morocco/scripts/postproc/docs/manuscript_figure_reproduction.md`
**Contenu attendu :**
- **Assimilation Figures :** Comment reproduire les incréments SMAP, l'exécution du script `inventory_smap_da_diagnostics.py`.
- **Hydrological Response :** Exécution du script `hydrological_response_cdf_nocdf.py`, données d'entrée (parquet ou nc).
- **Water Balance :** Comment regénérer le diagnostic *flux-only water balance*.
- **Classification :** Liste explicite des figures pour le papier principal (`main paper`) vs les documents supplémentaires (`supplementary`).
- **Scripts & Data :** Mapping direct entre la figure générée, le script qui l'a produite et la source de données d'entrée.

### `IA_SM_assim/reports/rf_xai_reproduction_guide.md`
**Contenu attendu :**
- **Dataset Generation :** Commande pour relancer le build du dataset (pixel-month).
- **Temporal Split :** Comment lancer le script de train sur la validation temporelle (2016-2019 train, 2020 test).
- **Spatial CV :** Comment lancer la validation croisée spatiale (GroupKFold).
- **Figure Regeneration :** Scripts à utiliser pour tracer les barplots d'importance et les métriques de compétence.
- **Classification :** Indiquer quelles métriques RF/XAI finissent dans le papier principal.

## 7. Git Strategy

1. **Commit État Actuel :** `git add . && git commit -m "chore: save state before repo split and file migration"` dans les deux repos.
2. **Migration Copiée :** Copier les fichiers (pas de `mv` destructif) vers leurs nouvelles destinations avec les nouveaux noms.
3. **Tests :** Tester les imports et les chemins d'exécution pour les scripts refactorisés (`10_hydrological_response_cdf_nocdf.py`).
4. **Commit Postproc :** `git add configs/ src/ matrix_2016_2020/ docs/ scripts/ && git commit -m "feat: integrate hydrological diagnostics and rename figures to manuscript standards"` dans `NoahMP_Morocco`.
5. **Commit IA :** `git commit -m "chore: archive sprint reports and setup final clean RF architecture"` dans `IA_SM_assim`.
6. **Suppression Différée :** Après validation que tout fonctionne dans `NoahMP_Morocco`, supprimer les fichiers doublons restés dans `IA_SM_assim`.

## 8. Migration Commands Proposed (Not Executed)

```bash
# 1. Archive Scratch and Old Reports in IA_SM_assim
mkdir -p archive/ scratch/
cp scratch_*.py scratch/
cp reports/q1_sprint* archive/

# 2. Copy scripts to Postproc (with renaming)
cp src/10_hydrological_response_cdf_nocdf.py ../NoahMP_Morocco/scripts/postproc/src/hydrological_response/hydrological_response_cdf_nocdf.py
cp src/00_find_smap_da_diagnostics.py ../NoahMP_Morocco/scripts/postproc/src/assimilation_diagnostics/inventory_smap_da_diagnostics.py

# 3. Copy and Rename Figures to Postproc
mkdir -p ../NoahMP_Morocco/scripts/postproc/matrix_2016_2020/outputs/figures/hydrological_response/
cp outputs/figures/q1_fig_hydrological_response_states_ET_annual_2016_2020.png ../NoahMP_Morocco/scripts/postproc/matrix_2016_2020/outputs/figures/hydrological_response/manuscript_hydro_response_states_ET_annual_2016_2020.png
# (And so on for other figures and tables based on the Rename Table)

# 4. Rename RF figures internally in IA_SM_assim
cp outputs/figures/rf_temporal_vs_spatial_cv_v02.png outputs/figures/manuscript_rf_temporal_vs_spatial_cv.png
```

## 9. Risks and Safeguards
- **Chemins d'accès brisés :** Le script `10_hydrological_response_cdf_nocdf.py` lit le dataset via `'data/processed/monthly_pixel_dataset_2016_2020_static.parquet'`. Une fois déplacé dans `postproc/`, ce chemin relatif échouera s'il ne pointe pas vers une source valide de données.
- **Rapports Markdown corrompus :** Déplacer ou renommer des figures brisera les balises d'images (`![alt](path)`) dans `q1_sprint2_results_text_hydrological_response.md`. Il faudra un search & replace dans les textes.
- **Sauvegarde :** En utilisant `cp` plutôt que `mv` pour la migration initiale, nous garantissons un fallback immédiat en cas d'échec d'un script refactorisé.

## 10. Priority Actions for Sprint Cleanup 3
1. **Créer l'arborescence cible** avec un script `mkdir -p` (sans copier les fichiers).
2. **Exécuter les copies et renommages** pour les outputs (tables, figures, docs).
3. **Refactorer `10_hydrological_response_cdf_nocdf.py`** : modifier le code pour que le chemin des `data` lise le parquet depuis sa source correcte.
4. **Générer les templates de documentation** (`manuscript_figure_reproduction.md` et `rf_xai_reproduction_guide.md`).
5. **Suppression finale** dans `IA_SM_assim` après commit fonctionnel sur le repo `NoahMP_Morocco`.
