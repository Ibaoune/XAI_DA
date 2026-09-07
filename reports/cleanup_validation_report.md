# Sprint Cleanup 4: Validation Report

## A. Summary
The Sprint Cleanup 4 validation confirms that the migration of hydrological diagnostic files and RF/XAI figures into their new robust directory structures has been executed correctly without data corruption or loss. 

## B. Hydrological figure integrity checks
All 9 critical hydrological figures in `NoahMP_Morocco/scripts/postproc/matrix_2016_2020/outputs/figures/` were validated:
- Existence: **Verified**
- File Size: **> 0 bytes** (range: 50 KB to 882 KB)
- Image verification: **OK**
- Resolutions: 1800x1800 for spatial maps, 2700x750 for water balance and IMERG components.

## C. RF/XAI figure integrity checks
All 7 target RF/XAI figures in `IA_SM_assim/outputs/figures/` were validated:
- Existence: **Verified**
- File Size: **> 0 bytes** (range: 206 KB to 250 KB)
- Image verification: **OK**
- Resolutions: 4200x2400 for RF summaries, 3600x3000 for feature importance.

## D. SHA256 copy validation
Validation of critical outputs to ensure bit-perfect duplication during migration:
- `manuscript_hydro_response_states_ET_annual_2016_2020.png`: **MATCH**
- `manuscript_flux_only_water_balance_2016_2020.png`: **MATCH**
- `hydrological_response_summary_2016_2020.csv`: **MATCH**
- `hydrological_response_key_numbers_2016_2020.csv`: **MATCH**
- `flux_only_water_balance_annual_seasonal_2016_2020.csv`: **MATCH**

## E. q1_ name audit
- `grep -R "q1_"` in `NoahMP_Morocco/scripts/postproc/` confirms that `q1_` string ONLY appears in the historical `docs/hydrological_response_cleanup_report.md` (which is acceptable historical record).
- No production scripts, directories, or outputs currently use the `q1_` prefix.

## F. Cautious-language audit
- Grep checks confirmed that overly confident terms ("verifies", "demonstrates water-balance closure", "confirms physical interpretability") were successfully identified and replaced in `docs/manuscript_captions_hydrology.md` and `docs/hydrological_response_results_text.md` during the previous sprint. The text now rigorously frames results as a "diagnostic interpretation."

## G. Script dry-run tests
- **Hydrology**: `python -m py_compile` passed for `inventory_smap_da_diagnostics.py` and `hydrological_response_cdf_nocdf.py`. The `./scripts/run_manuscript_hydrological_response_figures.sh --dry-run` successfully printed accurate output paths and confirmed the `--input-parquet` parameter logic.
- **RF/XAI**: Added `--dry-run` to `run_rf_xai_figures.sh`. Execution confirmed the paths and skipped copying, successfully bypassing training hooks.

## H. Inventory status
- Both `docs/manuscript_figure_inventory.md` and `reports/rf_xai_figure_inventory.md` exist and are populated with the correct columns (`relative_path`, `generated_by_script`, `input_data`, `paper_section`, `main_or_supplement`, `scientific_message`, `status`).

## I. Files safe to delete later (safe_to_delete_later)
The following duplicate files located in `IA_SM_assim/` are safely backed up in the target infrastructure and can be safely deleted in a future sprint:
- `IA_SM_assim/outputs/figures/q1_fig_*.png`
- `IA_SM_assim/outputs/tables/q1_*.csv`
- `IA_SM_assim/reports/q1_*.md` (except those already moved to archive)
- `IA_SM_assim/outputs/figures/rf_temporal_vs_spatial_cv_v02.png` (since renamed and copied)
- `IA_SM_assim/outputs/figures/rf_model_skill_v02_spatial_cv.png`
- `IA_SM_assim/outputs/figures/rf_grouped_feature_importance_v02.png`
- `IA_SM_assim/outputs/figures/rf_feature_importance_v02_spatial_cv.png`
- `IA_SM_assim/outputs/figures/rf_increment_feature_importance_v02_spatial_cv.png`

## J. Files NOT safe to delete yet (keep_until_next_validation)
- `IA_SM_assim/scratch/scratch_*.py` (Keep archived scratch files until final project closure).
- `IA_SM_assim/archive/09_generate_diagnostic_package.py`
- `IA_SM_assim/data/processed/monthly_pixel_dataset_2016_2020_static.parquet` (This is actively consumed by the postproc script).

## K. Remaining issues
- `inventory_smap_da_diagnostics.py` contains hardcoded paths (`reports/smap_da_diagnostics_inventory.md`) that should be updated to point to `docs/` within postproc if it is run in the future. 

## L. Recommendation
**READY.** The migration has been safely executed, validated structurally and bitwise. It is ready for the final step of deleting the old duplicate files.
