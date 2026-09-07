# Audit and Cleanup Inventory: Assimilation Post-Processing vs. RF/XAI

This report provides a comprehensive inventory and audit of the two distinct projects (`NoahMP_Morocco/scripts/postproc/` and `IA_SM_assim/`), identifying misplaced items, temporary files, and providing a migration plan to separate hydrological diagnostics from ML (Random Forest/XAI) workflows cleanly.

## A. Current organization
The workspace is currently divided into two main directories, but responsibilities overlap:

1. **Assimilation / Hydrology Project** (`NoahMP_Morocco/scripts/postproc/`):
   - Contains the core Noah-MP/LIS post-processing framework.
   - Handles independent observation validation, data extraction, and general domain analysis.
   - Contains numerous archived directories with past diagnostic scripts.

2. **IA Project** (`IA_SM_assim/`):
   - Intended for building the pixel-level dataset, training the Random Forest models, and producing XAI (permutation importance/SHAP) outputs.
   - **However**, it currently acts as a catch-all for recent hydrological diagnostic figures, summaries, and reports (often prefixed with `q1_`). 
   - It also hosts temporary `scratch_*.py` files used during Sprint 2.

## B. What belongs to assimilation/postproc
According to the project guidelines, the following elements belong **exclusively** in the assimilation/hydrology project:
- LIS/Noah-MP post-processing scripts.
- SMAP DA figures (increments, innovations).
- OPL vs. DA-NoCDF vs. DA-CDF figures.
- Hydrological state figures (SSM, RZSM, ET, runoff, baseflow).
- Any hydrological diagnostics or first-order water balance checks.
- Manuscript figures and captions linked strictly to assimilation experiments.

## C. What belongs to IA_SM_assim
This project should be strictly limited to the Machine Learning pipeline:
- Scripts for constructing the RF dataset (e.g., merging static predictors).
- Training and validation scripts for Random Forest.
- Cross-validation spatial/temporal outputs.
- Permutation importance, SHAP values, and feature importance analysis.
- Figures and tables strictly related to RF and XAI model performance.
- Associated methods/results reports for the XAI analysis.

## D. Files/scripts likely misplaced
The following items are currently inside `IA_SM_assim/` but belong in `NoahMP_Morocco/scripts/postproc/`:

**Scripts:**
- `src/00_find_smap_da_diagnostics.py`
- `src/09_generate_diagnostic_package.py`
- `src/10_hydrological_response_cdf_nocdf.py`

**Figures (in `outputs/figures/`):**
- `q1_fig_hydrological_response_runoff_JJA_2016_2020.png`
- `q1_fig_first_order_water_balance.png`
- `q1_fig_hydrological_response_runoff_DJF_2016_2020.png`
- `q1_fig_cdf_nocdf_hydrological_response_annual_2016_2020.png`
- `q1_fig_hydrological_response_states_ET_annual_2016_2020.png`
- `q1_fig_precip_runoff_components_DA_CDF_IMERG_2016_2020.png`
- `q1_fig_cdf_nocdf_hydrological_response_JJA_2016_2020.png`
- `q1_fig_hydrological_response_runoff_annual_2016_2020.png`
- `q1_fig_hydrological_response_states_ET_DJF_2016_2020.png`
- `q1_fig_precip_runoff_components_DA_NoCDF_IMERG_2016_2020.png`
- `q1_fig_hydrological_response_states_ET_JJA_2016_2020.png`
- `q1_fig_cdf_nocdf_hydrological_response_DJF_2016_2020.png`

**Tables (in `outputs/tables/`):**
- `q1_hydrological_response_key_numbers.csv`
- `q1_hydrological_response_summary.csv`
- `q1_first_order_water_balance_annual_seasonal.csv`

**Reports:**
- `reports/q1_sprint2_figures_for_review.zip`
- `reports/q1_paper_sprint2_hydrological_response_and_water_balance.md`
- `reports/q1_sprint2_2_final_hydrological_response.zip`
- `reports/q1_hydrological_response_summary.md`
- `reports/q1_sprint2_results_text_hydrological_response.md`
- `reports/q1_paper_sprint1_inventory_and_gap_analysis.md`
- `reports/q1_paper_sprint2_2_final_hydrological_response_cleanup.md`
- `reports/q1_sprint2_units_and_variable_mapping.md`
- `reports/q1_sprint1_figures_selected.zip`
- `reports/q1_paper_sprint1_key_messages.md`
- `reports/q1_sprint1_figures_selected/*` (all contained figures)
- `reports/q1_sprint2_manuscript_captions.md`
- `reports/q1_first_order_water_balance_diagnostic.md`

*(Note: There were no RF/XAI specific files found misplaced inside `NoahMP_Morocco/scripts/postproc/`)*

## E. Files/scripts temporary or scratch
The following files inside `IA_SM_assim/` are temporary, experimental, or scratchpad files that should be moved to an `archive` or `scratch` directory:
- `scratch_compute.py`
- `scratch_update_summary.py`
- `scratch_check_units.py`
- `scratch_sprint22.py`

## F. Proposed final folder structure

### 1. IA_SM_assim/
```
IA_SM_assim/
├── src/                  # ONLY RF/XAI scripts (01_build_dataset.py ... 08_add_insitu_precipitation.py)
├── data/                 # RF pixel-month inputs
├── models/               # *.joblib RF models
├── outputs/
│   ├── figures/          # ONLY RF/XAI figures (rf_model_skill, rf_feature_importance, etc.)
│   └── tables/           # ONLY RF/XAI tables (rf_metrics, rf_permutation_importance, etc.)
├── reports/              # RF/XAI diagnostic summaries, method writeups
└── scratch/              # (New) for scratch_*.py files
```

### 2. NoahMP_Morocco/scripts/postproc/
```
NoahMP_Morocco/scripts/postproc/
├── src/
│   └── hydrology_diagnostics/  # (New or existing) For 00_find, 09_generate, 10_hydro scripts
├── figures/
│   └── manuscript/             # (New) Cleanly named hydro_response, assim_diagnostics figures
└── reports/
    └── manuscript/             # (New) Cleanly named paper summaries and captions
```

## G. Proposed renaming table
Removing the `q1_` logic in favor of publishing-standard, neutral filenames:

| Original Filename (in IA_SM_assim) | Proposed New Filename (in NoahMP_Morocco) |
|------------------------------------|-------------------------------------------|
| `q1_fig_hydrological_response_runoff_JJA_2016_2020.png` | `hydro_response_runoff_JJA_2016_2020.png` |
| `q1_fig_first_order_water_balance.png` | `water_balance_diagnostic.png` |
| `q1_fig_cdf_nocdf_hydrological_response_annual_2016_2020.png` | `cdf_nocdf_hydrological_response_annual_2016_2020.png` |
| `q1_fig_hydrological_response_states_ET_annual_2016_2020.png` | `hydro_response_states_ET_annual_2016_2020.png` |
| `q1_fig_precip_runoff_components_DA_CDF_IMERG_2016_2020.png` | `assim_diagnostics_precip_runoff_components_DA_CDF_IMERG.png` |
| `q1_fig_cdf_nocdf_hydrological_response_JJA_2016_2020.png` | `cdf_nocdf_hydrological_response_JJA_2016_2020.png` |
| `q1_fig_hydrological_response_runoff_annual_2016_2020.png` | `hydro_response_runoff_annual_2016_2020.png` |
| `q1_fig_hydrological_response_states_ET_DJF_2016_2020.png` | `hydro_response_states_ET_DJF_2016_2020.png` |
| `q1_fig_precip_runoff_components_DA_NoCDF_IMERG_2016_2020.png` | `assim_diagnostics_precip_runoff_components_DA_NoCDF_IMERG.png` |
| `q1_fig_hydrological_response_states_ET_JJA_2016_2020.png` | `hydro_response_states_ET_JJA_2016_2020.png` |
| `q1_fig_cdf_nocdf_hydrological_response_DJF_2016_2020.png` | `cdf_nocdf_hydrological_response_DJF_2016_2020.png` |
| `q1_paper_sprint2_hydrological_response_and_water_balance.md` | `paper_hydrological_response_and_water_balance.md` |
| `q1_hydrological_response_summary.md` | `hydro_response_summary.md` |
| `q1_sprint2_results_text_hydrological_response.md` | `manuscript_results_text_hydrological_response.md` |
| `q1_paper_sprint1_inventory_and_gap_analysis.md` | `paper_inventory_and_gap_analysis.md` |
| `q1_sprint2_manuscript_captions.md` | `manuscript_captions.md` |
| `q1_first_order_water_balance_diagnostic.md` | `water_balance_diagnostic.md` |
| `q1_hydrological_response_key_numbers.csv` | `hydro_response_key_numbers.csv` |
| `q1_hydrological_response_summary.csv` | `hydro_response_summary.csv` |
| `q1_first_order_water_balance_annual_seasonal.csv` | `water_balance_annual_seasonal.csv` |

## H. Risks before moving
- **Hardcoded Paths in Code:** Scripts `09_generate_diagnostic_package.py` and `10_hydrological_response_cdf_nocdf.py` likely contain hardcoded relative paths pointing to `../outputs/figures/...`. Moving these scripts to another repository will break paths unless updated.
- **Import Conflicts:** Moved scripts may rely on `IA_SM_assim/src/utils/` functions (like `plotting_utils.py` or `io_utils.py`). A standalone extraction might break dependencies if these utilities aren't ported over or adapted to the existing NoahMP postproc utilities.
- **Broken Markdown Links:** Renaming and moving figures will break all `![alt](...)` image references in the markdown reports.

## I. Recommended migration plan
1. **Archive Scratch Files:** Create `IA_SM_assim/scratch/` and safely move all `scratch_*.py` files there to immediately clean the root directory.
2. **Review Code Dependencies:** Before moving scripts 00, 09, and 10 to `NoahMP_Morocco`, scan them for custom dependencies (`IA_SM_assim/src/utils`). If they heavily depend on IA utilities, extract those utility functions or rewrite them to use `NoahMP_Morocco`'s existing utils.
3. **Move and Rename Artifacts:** Execute a scripted move operation that transfers all `q1_*` figures, tables, and reports to their designated locations in `NoahMP_Morocco` while simultaneously applying the neutral renaming mappings.
4. **Update File References:** Perform a project-wide search-and-replace in the moved markdown files to update image links to their new names.
5. **Update Output Paths in Scripts:** Modify the output logic in scripts 09 and 10 to save directly to their new home in `NoahMP_Morocco/scripts/postproc/figures/`.
