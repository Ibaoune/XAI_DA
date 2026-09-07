# Assimilation Diagnostic Package (assim)

This directory contains the Random Forest diagnostic analysis pipeline for the Noah-MP/LIS SMAP assimilation study. It has been integrated directly into the `NoahMP_Morocco` project structure.

## Directory Structure
- `src/`: Python source code for data preprocessing, model training, and analysis.
- `notebooks/`: Jupyter notebooks for exploratory data analysis and prototyping.
- `jobs/`: Scripts for submitting jobs to the cluster.
- `data/`: Input datasets and preprocessed features.
- `outputs/`: Model outputs, predictions, and intermediate files.
- `reports/`: Generated reports, plots, and analysis summaries.
- `config.yaml`: Main configuration file for the diagnostic pipeline.
- `run_full_v0.sh`: Shell script to execute the end-to-end diagnostic workflow.
