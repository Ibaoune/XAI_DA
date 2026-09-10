#!/bin/bash
set -e

echo "Starting Phase 1 Execution..."

echo "1. Training Models and Exporting Baseline & Fold Metrics..."
python src/02_train_rf.py --dataset static

echo "2. Generating Figures A and B..."
python src/03_plot_results.py

echo "3. Generating Manuscript Tables..."
python src/11_generate_manuscript_tables.py

echo "Phase 1 Execution Complete. Check outputs/tables/ and outputs/figures/."
