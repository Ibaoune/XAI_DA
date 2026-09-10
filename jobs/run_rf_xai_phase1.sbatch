#!/bin/bash
#SBATCH --job-name=rf_xai_phase1
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=logs/slurm/rf_xai_phase1_%j.out
#SBATCH --error=logs/slurm/rf_xai_phase1_%j.err

set -eo pipefail

echo "Job started at: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: $(hostname)"
echo "Working directory: $(pwd)"

cd /home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/IA_SM_assim

mkdir -p logs/slurm outputs/tables outputs/figures outputs/models reports

# Activate python environment by prepending Anaconda to PATH
export PATH="/srv/software/easybuild/software/Anaconda3/2020.11/bin:$PATH"

echo "Python executable:"
which python
python --version

echo "Git status:"
git status --short || true

echo "Running RF/XAI Phase 1 training..."
python src/02_train_rf.py --dataset static

echo "Generating Phase 1 figures..."
python src/03_plot_results.py

echo "Generating manuscript tables..."
python src/11_generate_manuscript_tables.py

echo "Checking expected outputs..."
test -f outputs/tables/rf_spatial_cv_fold_metrics.csv
test -f outputs/tables/rf_spatial_cv_summary_with_uncertainty.csv
test -f outputs/tables/model_comparison_temporal.csv
test -f outputs/tables/model_comparison_spatial_cv.csv
test -f outputs/tables/manuscript_rf_target_definitions.csv
test -f outputs/tables/manuscript_rf_performance_summary.csv
test -f outputs/figures/q1_rf_model_skill_with_baselines.png
test -f outputs/figures/q1_grouped_permutation_importance.png

echo "Job completed successfully at: $(date)"
