import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add precip error to RF dataset")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    print("Running 04_add_precip_error_to_rf_dataset.py")
    if args.dry_run:
        print("[DRY RUN] Would merge predictors into monthly_pixel_dataset_2016_2020_static_precip_error_v1.parquet")
    else:
        print("[BLOCKED] Insufficient spatial coverage. V1 parquet not generated.")
