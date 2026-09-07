# RF / XAI Reproduction Guide

## Overview
This document outlines how to reproduce the Random Forest Explainable AI (XAI) figures and training procedures for the SMAP DA manuscript.

## 1. Reconstructing the RF Dataset
If you need to regenerate the `monthly_pixel_dataset_2016_2020_static.parquet` from raw outputs:
```bash
cd /home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/IA_SM_assim/
# Wait for the updated pipeline (src/build_dataset/*.py)
# sbatch jobs/job_build_dataset_cpu.sh
```

## 2. Running Random Forest (Temporal Split)
To train the RF model on 2016-2019 and test on 2020:
```bash
# sbatch jobs/job_train_rf_cpu.sh --mode temporal
```

## 3. Running Spatial Cross-Validation
To perform the 5-Fold GroupKFold spatial validation:
```bash
# sbatch jobs/job_train_rf_cpu.sh --mode spatial_cv
```

## 4. Regenerating RF Figures
To regenerate the final `manuscript_rf_*` figures without re-training:
```bash
cd /home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/IA_SM_assim/
./jobs/run_rf_xai_figures.sh
```

## Output Locations
- Final Main Paper Figures: `outputs/figures/manuscript_selected/`
- RF Skill Figures (Supplementary): `outputs/figures/rf_skill/`
- RF Importance Figures (Supplementary): `outputs/figures/rf_importance/`
- Feature Grouped Importance: `outputs/figures/rf_grouped_importance/`

## Planned V1 extension: gauge-based precipitation-error predictors
Gauge-based precipitation-error predictors are not included in the current V0 RF/XAI analysis. Therefore, the RF attribution cannot yet separate SMAP increments associated with precipitation forcing errors from those associated with model structural limitations or unrepresented water-management processes. A V1 extension will be implemented only if in-situ precipitation observations provide sufficient temporal coverage over 2016–2020.
