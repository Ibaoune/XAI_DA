import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inventory in-situ precip data")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    print("Running 01_inventory_insitu_precip.py")
    if args.dry_run:
        print("[DRY RUN] Would read data/insitu_data/ and produce precip_insitu_inventory.csv")
    else:
        print("[INVENTORY MODE] Checking data/insitu_data/")
