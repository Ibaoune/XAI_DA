import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match stations to grid")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    print("Running 02_match_stations_to_grid.py")
    if args.dry_run:
        print("[DRY RUN] Would associate stations to nearest LIS pixel based on lat/lon.")
        print("[DRY RUN] If lat/lon absent, would stop with a warning.")
    else:
        print("[WARNING] Coordinates missing in raw data. Cannot match stations to grid. Exiting.")
