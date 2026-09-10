# Phase 1: HPC Execution Status

## 1. Background Run Status
- **Status**: The previous background run (PID 2681753) was **stopped** cleanly via a terminal termination signal (`SIGINT`) because it was running as an unauthorized heavy process on the login/interactive node.
- **Partial Outputs**: A few partial outputs (like the spatial blocks diagnostic table and temporal model joblib backups) had been generated. These were successfully moved to a backup folder at `outputs/phase1_partial_background_run_20260908_1909/` to prevent silent overwriting.
- **Missing Outputs**: Because the run was terminated early, the final summary CSVs and all `outputs/figures/` for Phase 1 are still **missing**.

## 2. SLURM Submission Details
To enforce HPC best practices, all heavy Random Forest and XAI pipelines must now be executed via SLURM. 

I have created the SLURM submission script at `jobs/run_rf_xai_phase1.sbatch`.

### How to Submit
To queue the complete Phase 1 pipeline, simply execute the submission helper from your terminal:
```bash
./jobs/submit_rf_xai_phase1.sh
```
Or directly via sbatch:
```bash
sbatch jobs/run_rf_xai_phase1.sbatch
```

### How to Monitor
You can monitor the status of the job in the SLURM queue using:
```bash
squeue -u $USER
```

### How to Inspect Logs
The standard output and error streams will be piped into `logs/slurm/`. You can view them in real-time or after completion:
```bash
cat logs/slurm/rf_xai_phase1_<JOBID>.out
cat logs/slurm/rf_xai_phase1_<JOBID>.err
```

## 3. Re-running Figures Only
If the training completes successfully but you need to adjust aesthetics in the figures, there is no need to run the entire pipeline again. You can re-generate just the figures and tables directly using:
```bash
python src/03_plot_results.py
python src/11_generate_manuscript_tables.py
```
*(These plotting scripts take only seconds to execute and are safe to run interactively.)*
