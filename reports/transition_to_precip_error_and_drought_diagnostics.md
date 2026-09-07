# Transition Report: V1 Precip-Error and Drought Diagnostics

## 1. Git status and commits
- The `IA_SM_assim` and `NoahMP_Morocco` repositories were successfully committed prior to beginning this transition to ensure the pristine V0 cleanup state was preserved.

## 2. V0 RF/XAI package status
- The validated V0 RF/XAI package (without in-situ precipitation-error predictors) has been formally named and frozen as `manuscript_rf_xai_v0_no_precip_error_package.zip`. It remains the primary, robust package for the current manuscript.

## 3. In-situ precipitation inventory summary
- Inspection of `data/insitu_data/` revealed 4 text files (`Agadir-massira.txt`, `Chefchaouen.txt`, `Guelmim.txt`, `Tiznit.txt`).
- While these files possess daily records covering 2016–2020, they lack explicit geospatial coordinates, and 4 stations are statistically insufficient to represent the spatial heterogeneity of the entire Moroccan domain at a 5 km resolution.

## 4. V1 readiness status
- **ready_for_v1**: NO
- **Reason**: The spatial density of the in-situ precipitation data is far too low to train a robust Random Forest model. Proceeding would result in massive spatial gaps or severe representativeness bias.

## 5. New precip_error pipeline structure
- The V1 `precip_error` directories (`src`, `data`, `outputs`, `reports`) have been created in `IA_SM_assim`.
- Four scaffolded python scripts (`01` to `04`) are in place, supporting `--dry-run`, ready to process a denser gauge dataset if provided in the future.

## 6. Drought diagnostics structure added in postproc
- The `drought_diagnostics` directories have been created in `NoahMP_Morocco/scripts/postproc/` (`src`, `outputs/figures`, `outputs/tables`).
- A placeholder configuration `manuscript_drought_diagnostics.yaml` is prepared.

## 7. Planned drought methodology
- A methodology inspired by Nie et al. (2022) has been documented in `docs/planned_drought_diagnostics.md`. It outlines the computation of percentile-based drought classes for SSM and RZSM to evaluate the diagnostic sensitivity of the SMAP assimilation.

## 8. Updated inventories
- `NoahMP_Morocco/scripts/postproc/docs/manuscript_figure_inventory.md` has been updated with 7 planned drought figures.
- `IA_SM_assim/reports/rf_xai_figure_inventory.md` has been updated with 4 planned V1 precip-error figures.

## 9. Files created
- `IA_SM_assim/reports/rf_xai_versions.md`
- `IA_SM_assim/reports/precip_insitu_inventory.md`
- `IA_SM_assim/outputs/tables/precip_insitu_inventory.csv`
- `IA_SM_assim/reports/precip_error/precip_error_v1_readiness_report.md`
- `IA_SM_assim/reports/precip_error/rf_xai_v1_precip_error_design.md`
- `IA_SM_assim/src/precip_error/01_inventory_insitu_precip.py` to `04_add_precip_error_to_rf_dataset.py`
- `NoahMP_Morocco/scripts/postproc/docs/planned_drought_diagnostics.md`
- `NoahMP_Morocco/scripts/postproc/configs/figures/manuscript_drought_diagnostics.yaml`

## 10. Files not modified
- No training models, massive parquet datasets, or existing validated V0 figures were modified or deleted.

## 11. Recommended next action
- **proceed_to_precip_error_v1**: NO (Blocked by insufficient spatial data).
- **proceed_to_drought_implementation**: YES. The theoretical framework is in place, and we can proceed to implement the percentile-based drought diagnostics on the existing OPL / DA-NoCDF / DA-CDF dataset.
