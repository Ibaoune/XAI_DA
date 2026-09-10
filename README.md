# SMAP Assimilation Diagnostic Package (RF/XAI)

This repository contains the Machine Learning (Random Forest) diagnostic analysis pipeline to interpret the physical impacts of SMAP data assimilation into Noah-MP/LIS over Morocco.

## Scientific Objective
The objective is not simply to predict, but to use Random Forest as a post-hoc diagnostic tool to understand *how* and *why* the assimilation system updates the land surface state, and how those corrections propagate through the hydrological cycle (drought memory and fluxes).

## Directory Structure
- `src/`: Python source code for data preprocessing, model training, and analysis.
- `notebooks/`: Jupyter notebooks for exploratory data analysis.
- `jobs/`: SLURM scripts for submitting jobs to the cluster.
- `data/`: Input datasets and preprocessed features (ignored in git).
- `outputs/`: Model metrics, diagnostic figures, and models (`models/` ignored).
- `reports/`: Generated markdown reports and execution logs.
- `config.yaml`: Central configuration for paths and variables.

## RF/XAI Phase 1 checkpoint

**Modeling Framework:**
- **Objective:** RF used as a post-hoc diagnostic to explain DA behavior (not causal proof).
- **Targets:** SSM increment, NoCDF-CDF increment contrast, ΔRZSM, ΔET, Δbaseflow.
- **Validation:** Temporal holdout (2016-2019 train → 2020 test) and strict 5-Fold Spatial block Cross-Validation.
- **Baselines:** DummyRegressor (mean climatology) and Ridge Regression.

**Final Figures:**
- `outputs/figures/q1_rf_model_skill_with_baselines.png`
- `outputs/figures/q1_grouped_permutation_importance.png`

**Final Tables:**
- `outputs/tables/manuscript_rf_performance_summary.csv`
- `outputs/tables/manuscript_grouped_permutation_importance_summary.csv`

**Execution & SLURM:**
All heavy Phase 1 tasks must be executed on the HPC via SLURM:
```bash
# Submit Phase 1 pipeline
./jobs/submit_rf_xai_phase1.sh

# Re-run plotting only (safe interactively)
python src/03_plot_results.py
python src/11_generate_manuscript_tables.py
```

**Not Versioned in Git:**
- Large NetCDF/Parquet datasets (`data/`).
- Heavy ML model checkpoints (`outputs/models/*.joblib`).
- HPC execution logs (`logs/`).
- Intermediate/legacy plots (`outputs/archive_phase1_*/`).
