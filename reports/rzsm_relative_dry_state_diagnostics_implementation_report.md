# RZSM relative dry-state diagnostics implementation report

## 1. Input Dataset
- **Source:** `data/processed/monthly_pixel_dataset_2016_2020_static.parquet`
- **Period:** 2016–2020 (60 months)
- **Reference:** OPL-reference percentile ranking over 2016–2020.
- **Method:** Hazen plotting-position.

## 2. Methodology and Limitations
- The reference distribution is strictly limited to the 2016–2020 period. This is a relative dry-state diagnostic, not a long-term reference.
- Due to the 5-year period, there are only 5 OPL values per pixel × calendar-month group.
- **D0 (≤30th) and D1 (≤20th):** Robust and usable for main analysis.
- **D2 (≤10th):** Usable with caution, as it is structurally similar to D1 with n_ref=5.
- **D3 (≤5th) and D4 (≤2nd):** QC only. These are not robust with a 5-year reference. They indicate values below the lower bound of the OPL reference distribution, rather than a robust identification of extreme dry states.
- **Main diagnostic replacing D3/D4:** `below OPL reference minimum`. This metric quantifies the fraction of DA values falling strictly below the lowest OPL value observed in the 2016–2020 reference period for a given pixel-month.

## 3. Key Results (Full Run)
- **Intensification (DA-NoCDF):** 53.5 % of pixel-months show a relative downward shift in dry-state class compared to OPL.
- **Intensification (DA-CDF):** 42.2 % (more conservative than DA-NoCDF).
- **Below OPL reference minimum (DA-NoCDF):** 47.9 % of the domain falls below the lower bound of the OPL reference distribution.
- **Below OPL reference minimum (DA-CDF):** 36.5 %.
- **Seasonal Signal:** The maximal relative downward shift (intensification) occurs in MAM (spring), consistent with the model–observation mismatch signal during the recharge period.

## 4. Generated Outputs
**Tables:**
- `outputs/tables/rzsm_dry_state_area_domain.csv`
- `outputs/tables/rzsm_dry_state_area_delta_da_minus_opl.csv`
- `outputs/tables/rzsm_dry_state_area_by_season.csv`
- `outputs/tables/rzsm_dry_state_area_by_landcover.csv`
- `outputs/tables/rzsm_dry_state_area_by_irrigation_class.csv`
- `outputs/tables/rzsm_dry_state_transition_percentages.csv`
- `outputs/tables/rzsm_dry_state_transition_counts_nocdf.csv`
- `outputs/tables/rzsm_dry_state_transition_counts_cdf.csv`
- `outputs/tables/rzsm_dry_state_transition_by_landcover.csv`
- `outputs/tables/rzsm_dry_state_target_definitions.csv`
- `outputs/tables/rzsm_dry_state_reference_quality.csv`
- `outputs/tables/rzsm_dry_state_dataset_summary.csv`
- `outputs/tables/rzsm_below_opl_ref_min_summary.csv`

**Figures (QC only):**
- `outputs/figures/rzsm_dry_state/rzsm_dry_state_area_domain.png`
- `outputs/figures/rzsm_dry_state/rzsm_dry_state_transition_summary.png`

## 5. Recommended Next Steps
- Proceed with RF/XAI training using `delta_rzsm_pct_nocdf_minus_opl` (continuous target) and `rzsm_dry_class_transition_nocdf_minus_opl` (categorical transition labels).
