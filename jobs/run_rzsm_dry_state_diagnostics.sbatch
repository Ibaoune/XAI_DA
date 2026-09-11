#!/bin/bash
#SBATCH --job-name=rzsm_dry_state
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/slurm/rzsm_dry_state_%j.out
#SBATCH --error=logs/slurm/rzsm_dry_state_%j.err

set -eo pipefail

echo "Job started at: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: $(hostname)"
echo "Working directory: $(pwd)"

cd /home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/IA_SM_assim

mkdir -p logs/slurm outputs/tables outputs/figures/rzsm_dry_state data/processed

# Activate python environment
export PATH="/srv/software/easybuild/software/Anaconda3/2020.11/bin:$PATH"

# Limit thread usage to avoid CPU contention on shared nodes
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export PYTHONUNBUFFERED=1

echo "Python executable:"
which python
python --version

echo "Git branch:"
git branch --show-current || true

echo "Running RZSM relative dry-state diagnostics (full dataset, --write)..."
python src/data/build_rzsm_relative_dry_state_diagnostics.py \
  --input  data/processed/monthly_pixel_dataset_2016_2020_static.parquet \
  --output data/processed/monthly_pixel_dataset_2016_2020_static_rzsm_dry_state.parquet \
  --reference opl_available_period \
  --write

echo "Checking expected outputs..."
test -f data/processed/monthly_pixel_dataset_2016_2020_static_rzsm_dry_state.parquet
test -f outputs/tables/rzsm_dry_state_area_domain.csv
test -f outputs/tables/rzsm_dry_state_transition_counts_nocdf.csv
test -f outputs/tables/rzsm_dry_state_transition_counts_cdf.csv
test -f outputs/tables/rzsm_dry_state_target_definitions.csv
test -f outputs/tables/rzsm_dry_state_dataset_summary.csv
test -f outputs/tables/rzsm_dry_state_reference_quality.csv
test -f outputs/figures/rzsm_dry_state/rzsm_dry_state_area_domain.png
test -f outputs/figures/rzsm_dry_state/rzsm_dry_state_transition_summary.png

echo "Output parquet size:"
ls -lh data/processed/monthly_pixel_dataset_2016_2020_static_rzsm_dry_state.parquet

echo "Job completed successfully at: $(date)"
