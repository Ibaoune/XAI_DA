import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute precip error predictors")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    print("Running 03_compute_precip_error_predictors.py")
    if args.dry_run:
        print("[DRY RUN] Would compute precip_bias_monthly, precip_abs_error_monthly, station_count_per_pixel")
    else:
        print("[WARNING] Missing matched stations grid. Cannot compute errors.")
