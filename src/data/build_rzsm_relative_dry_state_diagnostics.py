"""
build_rzsm_relative_dry_state_diagnostics.py
============================================
Computes RZSM percentile-based relative dry-state diagnostics using OPL as the
common reference distribution. Quantifies how DA-NoCDF and DA-CDF shift
root-zone soil-moisture dry-state categories relative to the OPL reference.

NOTE: The reference period is limited to the available simulation period
(2016-2020, 60 months). This is NOT a long-term drought climatology.
All diagnostics represent within-period relative dry-state rankings.

Usage:
  python src/data/build_rzsm_relative_dry_state_diagnostics.py \
    --input data/processed/monthly_pixel_dataset_2016_2020_static.parquet \
    --output data/processed/monthly_pixel_dataset_2016_2020_static_rzsm_dry_state.parquet \
    --reference opl_available_period \
    --sample 50000 \
    --dry-run

  Add --write to persist the full output parquet.
"""

import argparse
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# Exclusive dry-state class thresholds (percentile-based, OPL-referenced)
# Class 0 = normal (wettest), class 5 = exceptional dry
DRY_CLASS_THRESHOLDS = [
    (5, 100, 0, "normal"),
    (4,  30, 1, "abnormally_dry"),
    (3,  20, 2, "moderate_dry"),
    (2,  10, 3, "severe_dry"),
    (1,   5, 4, "extreme_dry"),
    (0,   2, 5, "exceptional_dry"),
]

# Nested dry-state indicator thresholds (each includes all drier categories)
# INTERPRETABILITY NOTE (5-year OPL reference, Hazen n=5):
#   With n_ref=5, OPL Hazen percentiles can only take values: 10, 30, 50, 70, 90.
#   D0 (<=30th): ~40% of OPL pixels by construction → robust
#   D1 (<=20th): ~20% of OPL pixels by construction → robust
#   D2 (<=10th): ~20% of OPL pixels by construction → usable with caution (same as D1 for n=5)
#   D3 (<=5th) : 0% of OPL pixels by construction  → NOT interpretable as extreme drought
#   D4 (<=2nd) : 0% of OPL pixels by construction  → NOT interpretable as exceptional drought
#   D3/D4 for DA experiments indicate values BELOW THE OPL REFERENCE MINIMUM,
#   not a robust identification of extreme/exceptional dry states.
NESTED_THRESHOLDS = {"D0": 30, "D1": 20, "D2": 10, "D3": 5, "D4": 2}

NESTED_ROBUSTNESS = {
    "D0": "main",
    "D1": "main",
    "D2": "cautious_supplementary",
    "D3": "qc_only_not_robust_with_5yr_reference",
    "D4": "qc_only_not_robust_with_5yr_reference",
}

PIXEL_COLS = ["lat", "lon"]
ALT_PIXEL_COLS = ["north_south", "east_west"]
REQUIRED_RZSM = ["RZSM_OPL", "RZSM_DA_NoCDF", "RZSM_DA_CDF"]


# ---------------------------------------------------------------------------
# Percentile engine
# ---------------------------------------------------------------------------
def compute_percentile_against_reference(values: np.ndarray,
                                         reference_values: np.ndarray,
                                         method: str = "minmax_plotting_position") -> np.ndarray:
    """
    Rank each element of `values` against `reference_values` using a
    plotting-position approach scaled to [0, 100].

    Low RZSM → low percentile. Returns NaN when reference has < 3 valid values.
    """
    ref_clean = reference_values[~np.isnan(reference_values)]
    if len(ref_clean) < 3:
        return np.full(len(values), np.nan)

    ref_sorted = np.sort(ref_clean)
    n = len(ref_sorted)
    # Hazen plotting positions for the reference
    ref_pcts = (np.arange(1, n + 1) - 0.5) / n * 100.0

    # For each value, interpolate its percentile against the reference CDF
    out = np.interp(values, ref_sorted, ref_pcts, left=0.0, right=100.0)
    out = np.clip(out, 0.0, 100.0)
    # Propagate NaN from input
    out[np.isnan(values)] = np.nan
    return out


# ---------------------------------------------------------------------------
# Dry-state class assignment
# ---------------------------------------------------------------------------
def assign_dry_class(pct: pd.Series) -> pd.Series:
    """Map percentile series → exclusive dry-state class 0-5."""
    cls = pd.Series(np.nan, index=pct.index, dtype="float32")
    cls[pct > 30] = 0
    cls[(pct > 20) & (pct <= 30)] = 1
    cls[(pct > 10) & (pct <= 20)] = 2
    cls[(pct >  5) & (pct <= 10)] = 3
    cls[(pct >  2) & (pct <=  5)] = 4
    cls[pct <= 2] = 5
    return cls


# ---------------------------------------------------------------------------
# Core computation (vectorised, group-by pixel × month)
# ---------------------------------------------------------------------------
def compute_dry_state_diagnostics(df: pd.DataFrame,
                                  pixel_cols: list,
                                  verbose: bool = True) -> pd.DataFrame:
    """
    For every (pixel, month) group, build the OPL reference distribution and
    rank all three experiments against it. Returns the input df enriched with
    new columns.
    """
    group_keys = pixel_cols + ["month"]
    total_groups = df.groupby(group_keys).ngroups

    # ---- Quality report storage
    qc_rows = []

    # Use a reset-index copy so positional indices are contiguous
    df_reset = df.reset_index(drop=True)

    pct_opl      = np.full(len(df_reset), np.nan)
    pct_nocdf    = np.full(len(df_reset), np.nan)
    pct_cdf      = np.full(len(df_reset), np.nan)
    z_opl        = np.full(len(df_reset), np.nan)
    z_nocdf      = np.full(len(df_reset), np.nan)
    z_cdf        = np.full(len(df_reset), np.nan)

    for name, grp in df_reset.groupby(group_keys):
        idx = grp.index  # positional after reset
        ref = grp["RZSM_OPL"].values
        ref_clean = ref[~np.isnan(ref)]
        n_ref = len(ref_clean)

        # OPL reference statistics
        ref_mean = np.nanmean(ref) if n_ref > 0 else np.nan
        ref_std  = np.nanstd(ref)  if n_ref > 0 else np.nan

        qc_rows.append({"group": str(name), "n_ref": n_ref,
                        "ref_mean": ref_mean, "ref_std": ref_std})

        if n_ref < 3:
            continue

        # Percentile ranking
        pct_opl[idx]   = compute_percentile_against_reference(ref,                          ref)
        pct_nocdf[idx] = compute_percentile_against_reference(grp["RZSM_DA_NoCDF"].values,  ref)
        pct_cdf[idx]   = compute_percentile_against_reference(grp["RZSM_DA_CDF"].values,    ref)

        # Z-scores against OPL reference
        if ref_std and ref_std > 1e-9:
            z_opl[idx]   = (ref                            - ref_mean) / ref_std
            z_nocdf[idx] = (grp["RZSM_DA_NoCDF"].values   - ref_mean) / ref_std
            z_cdf[idx]   = (grp["RZSM_DA_CDF"].values     - ref_mean) / ref_std

    if verbose:
        qc_df = pd.DataFrame(qc_rows)
        n_low = (qc_df["n_ref"] < 3).sum()
        print(f"  [QC] Total pixel-month groups : {total_groups}")
        print(f"  [QC] Groups with <3 ref values: {n_low}")
        print(f"  [QC] Median ref count         : {qc_df['n_ref'].median():.0f}")
        print(f"  [QC] Min ref count            : {qc_df['n_ref'].min()}")

    # Attach percentile columns to the reset-index copy
    df = df_reset.copy()
    df["rzsm_pct_opl_ref_opl"]       = pct_opl.astype("float32")
    df["rzsm_pct_da_nocdf_ref_opl"]  = pct_nocdf.astype("float32")
    df["rzsm_pct_da_cdf_ref_opl"]    = pct_cdf.astype("float32")

    df["delta_rzsm_pct_nocdf_minus_opl"] = (df["rzsm_pct_da_nocdf_ref_opl"]
                                             - df["rzsm_pct_opl_ref_opl"]).astype("float32")
    df["delta_rzsm_pct_cdf_minus_opl"]   = (df["rzsm_pct_da_cdf_ref_opl"]
                                             - df["rzsm_pct_opl_ref_opl"]).astype("float32")

    # Z-score columns
    df["rzsm_z_opl_ref_opl"]        = z_opl.astype("float32")
    df["rzsm_z_da_nocdf_ref_opl"]   = z_nocdf.astype("float32")
    df["rzsm_z_da_cdf_ref_opl"]     = z_cdf.astype("float32")
    df["delta_rzsm_z_nocdf_minus_opl"] = (df["rzsm_z_da_nocdf_ref_opl"]
                                           - df["rzsm_z_opl_ref_opl"]).astype("float32")
    df["delta_rzsm_z_cdf_minus_opl"]   = (df["rzsm_z_da_cdf_ref_opl"]
                                           - df["rzsm_z_opl_ref_opl"]).astype("float32")

    # Nested indicators — float32 for matplotlib compatibility (NaN-safe)
    for tag, thr in NESTED_THRESHOLDS.items():
        df[f"rzsm_{tag.lower()}_opl"]      = (df["rzsm_pct_opl_ref_opl"]      <= thr).astype("float32")
        df[f"rzsm_{tag.lower()}_da_nocdf"] = (df["rzsm_pct_da_nocdf_ref_opl"] <= thr).astype("float32")
        df[f"rzsm_{tag.lower()}_da_cdf"]   = (df["rzsm_pct_da_cdf_ref_opl"]   <= thr).astype("float32")
        # Propagate NaN where percentile was NaN
        for sfx, pct_col in [("opl", "rzsm_pct_opl_ref_opl"),
                              ("da_nocdf", "rzsm_pct_da_nocdf_ref_opl"),
                              ("da_cdf",   "rzsm_pct_da_cdf_ref_opl")]:
            mask = df[pct_col].isna()
            df.loc[mask, f"rzsm_{tag.lower()}_{sfx}"] = np.nan

    # Exclusive dry-state classes
    df["rzsm_dry_class_opl"]     = assign_dry_class(df["rzsm_pct_opl_ref_opl"])
    df["rzsm_dry_class_da_nocdf"]= assign_dry_class(df["rzsm_pct_da_nocdf_ref_opl"])
    df["rzsm_dry_class_da_cdf"]  = assign_dry_class(df["rzsm_pct_da_cdf_ref_opl"])

    df["rzsm_dry_class_transition_nocdf_minus_opl"] = (
        df["rzsm_dry_class_da_nocdf"] - df["rzsm_dry_class_opl"]).astype("float32")
    df["rzsm_dry_class_transition_cdf_minus_opl"] = (
        df["rzsm_dry_class_da_cdf"] - df["rzsm_dry_class_opl"]).astype("float32")

    def label_transition(s):
        return s.map(lambda x: ("attenuation" if x < 0
                                else ("intensification" if x > 0 else "no_change"))
                     if pd.notna(x) else np.nan)

    df["rzsm_transition_label_nocdf"] = label_transition(
        df["rzsm_dry_class_transition_nocdf_minus_opl"])
    df["rzsm_transition_label_cdf"]   = label_transition(
        df["rzsm_dry_class_transition_cdf_minus_opl"])

    # -------------------------------------------------------------------
    # below_opl_ref_min: honest replacement for D3/D4
    # 1 when DA value < min(OPL reference) for this pixel-month group
    # This is what D3/D4 actually measure with n_ref=5.
    # -------------------------------------------------------------------
    below_min_nocdf = np.full(len(df_reset), np.nan)
    below_min_cdf   = np.full(len(df_reset), np.nan)
    below_min_opl   = np.full(len(df_reset), np.nan)

    for name, grp in df_reset.groupby(group_keys):
        idx = grp.index
        ref_clean = grp["RZSM_OPL"].values
        ref_clean = ref_clean[~np.isnan(ref_clean)]
        if len(ref_clean) < 1:
            continue
        ref_min = ref_clean.min()
        below_min_opl[idx]   = (grp["RZSM_OPL"].values   < ref_min).astype(float)
        below_min_nocdf[idx] = (grp["RZSM_DA_NoCDF"].values < ref_min).astype(float)
        below_min_cdf[idx]   = (grp["RZSM_DA_CDF"].values   < ref_min).astype(float)
        # OPL can never be below its own min (always 0)
        below_min_opl[idx] = 0.0
        # Propagate NaN from missing DA
        below_min_nocdf[idx[np.isnan(grp["RZSM_DA_NoCDF"].values)]] = np.nan
        below_min_cdf[idx[np.isnan(grp["RZSM_DA_CDF"].values)]]     = np.nan

    df["rzsm_below_opl_ref_min_opl"]     = below_min_opl.astype("float32")
    df["rzsm_below_opl_ref_min_da_nocdf"]= below_min_nocdf.astype("float32")
    df["rzsm_below_opl_ref_min_da_cdf"]  = below_min_cdf.astype("float32")

    return df, pd.DataFrame(qc_rows)


# ---------------------------------------------------------------------------
# Summary tables
# ---------------------------------------------------------------------------
def compute_area_summaries(df: pd.DataFrame, out_dir: Path):
    """Compute monthly % area under nested dry-state categories (domain, seasonal, land-cover)."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Domain monthly
    rows = []
    for exp, col_suffix in [("OPL", "opl"), ("DA_NoCDF", "da_nocdf"), ("DA_CDF", "da_cdf")]:
        for tag in NESTED_THRESHOLDS:
            col = f"rzsm_{tag.lower()}_{col_suffix}"
            if col not in df.columns:
                continue
            monthly = (df.groupby(["year", "month"])[col]
                       .mean().reset_index().rename(columns={col: "pct_area"}))
            monthly["pct_area"] *= 100
            monthly["experiment"] = exp
            monthly["dry_category"] = tag
            monthly["robustness"] = NESTED_ROBUSTNESS[tag]
            rows.append(monthly)
    if rows:
        out = pd.concat(rows, ignore_index=True)
        out.to_csv(out_dir / "rzsm_dry_state_area_domain.csv", index=False)
        print(f"  Saved: rzsm_dry_state_area_domain.csv ({len(out)} rows)")

        # Delta table
        pivot = out.pivot_table(index=["year","month","dry_category"],
                                columns="experiment", values="pct_area").reset_index()
        if "OPL" in pivot.columns:
            if "DA_NoCDF" in pivot.columns:
                pivot["delta_nocdf_minus_opl"] = pivot["DA_NoCDF"] - pivot["OPL"]
            if "DA_CDF" in pivot.columns:
                pivot["delta_cdf_minus_opl"]   = pivot["DA_CDF"]   - pivot["OPL"]
        pivot.to_csv(out_dir / "rzsm_dry_state_area_delta_da_minus_opl.csv", index=False)
        print(f"  Saved: rzsm_dry_state_area_delta_da_minus_opl.csv")

        # Seasonal breakdown
        def to_season(m):
            return {12:"DJF",1:"DJF",2:"DJF",3:"MAM",4:"MAM",5:"MAM",
                    6:"JJA",7:"JJA",8:"JJA",9:"SON",10:"SON",11:"SON"}.get(m, "?")
        out["season"] = out["month"].map(to_season)
        seas = (out.groupby(["experiment","season","dry_category","robustness"])
                ["pct_area"].mean().reset_index())
        seas.to_csv(out_dir / "rzsm_dry_state_area_by_season.csv", index=False)
        print(f"  Saved: rzsm_dry_state_area_by_season.csv")

    # --- Land-cover breakdown (if column present)
    if "land_cover" in df.columns:
        lc_rows = []
        for exp, col_suffix in [("OPL", "opl"), ("DA_NoCDF", "da_nocdf"), ("DA_CDF", "da_cdf")]:
            for tag in ["D0", "D1", "D2"]:  # only robust categories
                col = f"rzsm_{tag.lower()}_{col_suffix}"
                if col not in df.columns: continue
                lc = (df.groupby(["land_cover", "year", "month"])[col]
                      .mean().reset_index().rename(columns={col: "pct_area"}))
                lc["pct_area"] *= 100
                lc["experiment"] = exp
                lc["dry_category"] = tag
                lc_rows.append(lc)
        if lc_rows:
            lc_out = pd.concat(lc_rows, ignore_index=True)
            lc_out.to_csv(out_dir / "rzsm_dry_state_area_by_landcover.csv", index=False)
            print(f"  Saved: rzsm_dry_state_area_by_landcover.csv")

    # --- Irrigation-class breakdown (if column present)
    if "irrigation_fraction" in df.columns:
        irr = df["irrigation_fraction"].fillna(0)
        df["irrigation_class"] = pd.cut(
            irr,
            bins=[-0.001, 0.01, 0.15, 0.40, 1.01],
            labels=["non_irrigated", "low", "medium", "high"])
        irr_rows = []
        for exp, col_suffix in [("OPL", "opl"), ("DA_NoCDF", "da_nocdf"), ("DA_CDF", "da_cdf")]:
            for tag in ["D0", "D1", "D2"]:
                col = f"rzsm_{tag.lower()}_{col_suffix}"
                if col not in df.columns: continue
                ir = (df.groupby(["irrigation_class", "year", "month"])[col]
                      .mean().reset_index().rename(columns={col: "pct_area"}))
                ir["pct_area"] *= 100
                ir["experiment"] = exp
                ir["dry_category"] = tag
                irr_rows.append(ir)
        if irr_rows:
            irr_out = pd.concat(irr_rows, ignore_index=True)
            irr_out.to_csv(out_dir / "rzsm_dry_state_area_by_irrigation_class.csv", index=False)
            print(f"  Saved: rzsm_dry_state_area_by_irrigation_class.csv")


def compute_transition_summaries(df: pd.DataFrame, out_dir: Path):
    """Count and percentage of attenuation / no_change / intensification,
    with land-cover and irrigation-class breakdowns."""
    out_dir.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for exp, col in [("NoCDF", "rzsm_transition_label_nocdf"),
                     ("CDF",   "rzsm_transition_label_cdf")]:
        if col not in df.columns:
            continue
        counts = df[col].value_counts(dropna=True).rename("count").reset_index()
        counts.columns = ["transition", "count"]
        counts["pct"] = counts["count"] / counts["count"].sum() * 100
        counts["experiment"] = f"DA_{exp}_minus_OPL"
        counts.to_csv(out_dir / f"rzsm_dry_state_transition_counts_{exp.lower()}.csv", index=False)
        print(f"  Saved: rzsm_dry_state_transition_counts_{exp.lower()}.csv")
        all_rows.append(counts)

    if all_rows:
        pct_table = pd.concat(all_rows, ignore_index=True)
        pct_table.to_csv(out_dir / "rzsm_dry_state_transition_percentages.csv", index=False)
        print(f"  Saved: rzsm_dry_state_transition_percentages.csv")

    # Land-cover breakdown
    if "land_cover" in df.columns:
        lc_rows = []
        for exp, col in [("NoCDF", "rzsm_transition_label_nocdf"),
                         ("CDF",   "rzsm_transition_label_cdf")]:
            if col not in df.columns: continue
            lc = (df.groupby(["land_cover", col])
                  .size().reset_index(name="count"))
            lc.rename(columns={col: "transition"}, inplace=True)
            total = df.groupby("land_cover")[col].count().rename("total")
            lc = lc.join(total, on="land_cover")
            lc["pct"] = lc["count"] / lc["total"] * 100
            lc["experiment"] = f"DA_{exp}_minus_OPL"
            lc_rows.append(lc)
        if lc_rows:
            pd.concat(lc_rows, ignore_index=True).to_csv(
                out_dir / "rzsm_dry_state_transition_by_landcover.csv", index=False)
            print(f"  Saved: rzsm_dry_state_transition_by_landcover.csv")


def save_target_definitions(out_dir: Path):
    """Write a human-readable target definition table with recommended_use flags."""
    rows = [
        {"target": "rzsm_pct_opl_ref_opl",
         "type": "continuous", "unit": "percentile [0-100]",
         "description": "OPL RZSM ranked against OPL reference distribution (2016-2020)",
         "recommended_use": "main"},
        {"target": "rzsm_pct_da_nocdf_ref_opl",
         "type": "continuous", "unit": "percentile [0-100]",
         "description": "DA-NoCDF RZSM ranked against OPL reference distribution",
         "recommended_use": "main"},
        {"target": "rzsm_pct_da_cdf_ref_opl",
         "type": "continuous", "unit": "percentile [0-100]",
         "description": "DA-CDF RZSM ranked against OPL reference distribution",
         "recommended_use": "main"},
        {"target": "delta_rzsm_pct_nocdf_minus_opl",
         "type": "continuous", "unit": "percentile points",
         "description": "DA-NoCDF minus OPL percentile shift (positive=wetter, negative=drier)",
         "recommended_use": "main"},
        {"target": "delta_rzsm_pct_cdf_minus_opl",
         "type": "continuous", "unit": "percentile points",
         "description": "DA-CDF minus OPL percentile shift",
         "recommended_use": "main"},
        {"target": "rzsm_dry_class_opl",
         "type": "ordinal [0-5]", "unit": "class",
         "description": "OPL exclusive dry-state class: 0=normal, 5=exceptional",
         "recommended_use": "main"},
        {"target": "rzsm_dry_class_da_nocdf",
         "type": "ordinal [0-5]", "unit": "class",
         "description": "DA-NoCDF exclusive dry-state class",
         "recommended_use": "main"},
        {"target": "rzsm_dry_class_transition_nocdf_minus_opl",
         "type": "ordinal [-5 to +5]", "unit": "class units",
         "description": "Transition: negative=attenuation, 0=no change, positive=intensification",
         "recommended_use": "main"},
        {"target": "rzsm_transition_label_nocdf",
         "type": "categorical", "unit": "label",
         "description": "attenuation / no_change / intensification (DA-NoCDF vs OPL)",
         "recommended_use": "main"},
        {"target": "rzsm_transition_label_cdf",
         "type": "categorical", "unit": "label",
         "description": "attenuation / no_change / intensification (DA-CDF vs OPL)",
         "recommended_use": "main"},
        {"target": "rzsm_below_opl_ref_min_da_nocdf",
         "type": "binary", "unit": "0/1",
         "description": "1 if DA-NoCDF RZSM is below the minimum of the OPL reference distribution",
         "recommended_use": "main (replaces D3/D4 interpretation)"},
        {"target": "rzsm_below_opl_ref_min_da_cdf",
         "type": "binary", "unit": "0/1",
         "description": "1 if DA-CDF RZSM is below the minimum of the OPL reference distribution",
         "recommended_use": "main (replaces D3/D4 interpretation)"},
    ]
    for tag, thr in NESTED_THRESHOLDS.items():
        use = NESTED_ROBUSTNESS[tag]
        desc_note = (
            " NOTE: OPL always 0% by construction with n_ref=5 (Hazen); "
            "DA values here indicate sub-reference-minimum, not robust extreme drought."
            if tag in ("D3", "D4") else ""
        )
        rows.append({"target": f"rzsm_{tag.lower()}_opl",
                     "type": "binary", "unit": "0/1",
                     "description": f"1 if OPL RZSM percentile <= {thr} ({tag}).{desc_note}",
                     "recommended_use": use})
        rows.append({"target": f"rzsm_{tag.lower()}_da_nocdf",
                     "type": "binary", "unit": "0/1",
                     "description": f"1 if DA-NoCDF RZSM percentile <= {thr} ({tag}).{desc_note}",
                     "recommended_use": use})
    pd.DataFrame(rows).to_csv(out_dir / "rzsm_dry_state_target_definitions.csv", index=False)
    print(f"  Saved: rzsm_dry_state_target_definitions.csv")


def save_below_ref_min_summary(df: pd.DataFrame, out_dir: Path):
    """Compute % area below OPL reference minimum — robust replacement for D3/D4."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for exp, col in [("DA_NoCDF", "rzsm_below_opl_ref_min_da_nocdf"),
                     ("DA_CDF",   "rzsm_below_opl_ref_min_da_cdf")]:
        if col not in df.columns: continue
        monthly = (df.groupby(["year", "month"])[col]
                   .mean().reset_index().rename(columns={col: "pct_below_ref_min"}))
        monthly["pct_below_ref_min"] *= 100
        monthly["experiment"] = exp
        rows.append(monthly)
    if rows:
        out = pd.concat(rows, ignore_index=True)
        out.to_csv(out_dir / "rzsm_below_opl_ref_min_summary.csv", index=False)
        print(f"  Saved: rzsm_below_opl_ref_min_summary.csv")
        mean_by_exp = out.groupby("experiment")["pct_below_ref_min"].mean()
        print(f"  Mean % below OPL ref min: {mean_by_exp.to_dict()}")


# ---------------------------------------------------------------------------
# Lightweight QC figures
# ---------------------------------------------------------------------------
def make_qc_figures(df: pd.DataFrame, out_dir: Path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        out_dir.mkdir(parents=True, exist_ok=True)

        # --- Figure 1: domain monthly % area under D0/D1/D2
        if "year" in df.columns and "rzsm_d0_opl" in df.columns:
            fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
            for ax, (exp, sfx) in zip(axes, [("OPL", "opl"),
                                              ("DA-NoCDF", "da_nocdf"),
                                              ("DA-CDF", "da_cdf")]):
                monthly = df.groupby(["year", "month"])[[
                    f"rzsm_d0_{sfx}", f"rzsm_d1_{sfx}", f"rzsm_d2_{sfx}"]].mean() * 100
                monthly = monthly.reset_index()
                monthly["date_idx"] = monthly["year"] * 12 + monthly["month"]
                monthly = monthly.sort_values("date_idx")
                ax.fill_between(monthly["date_idx"], monthly[f"rzsm_d0_{sfx}"],
                                alpha=0.4, label="D0 (≤30th)", color="#f4a460")
                ax.fill_between(monthly["date_idx"], monthly[f"rzsm_d1_{sfx}"],
                                alpha=0.5, label="D1 (≤20th)", color="#cd853f")
                ax.fill_between(monthly["date_idx"], monthly[f"rzsm_d2_{sfx}"],
                                alpha=0.6, label="D2 (≤10th)", color="#8b4513")
                ax.set_title(f"% area under dry-state categories – {exp}", fontsize=10)
                ax.set_ylabel("% domain area")
                ax.legend(fontsize=8)
                ax.set_ylim(0, 105)
            axes[-1].set_xlabel("Year × 12 + Month index")
            plt.tight_layout()
            plt.savefig(out_dir / "rzsm_dry_state_area_domain.png", dpi=150)
            plt.close()
            print("  Saved: rzsm_dry_state_area_domain.png")

        # --- Figure 2: transition bar chart
        if "rzsm_transition_label_nocdf" in df.columns:
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            for ax, (exp, col) in zip(axes, [("DA-NoCDF", "rzsm_transition_label_nocdf"),
                                              ("DA-CDF",   "rzsm_transition_label_cdf")]):
                if col not in df.columns:
                    continue
                cts = df[col].value_counts(dropna=True)
                pct = cts / cts.sum() * 100
                colors = {"attenuation": "#2196F3",
                          "no_change":   "#9E9E9E",
                          "intensification": "#F44336"}
                labels = [l for l in ["attenuation", "no_change", "intensification"] if l in pct]
                vals   = [pct.get(l, 0) for l in labels]
                ax.bar(labels, vals,
                       color=[colors[l] for l in labels])
                ax.set_title(f"RZSM transition distribution\n{exp} vs OPL")
                ax.set_ylabel("% pixel-months")
                ax.set_ylim(0, 100)
                for i, v in enumerate(vals):
                    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
            plt.tight_layout()
            plt.savefig(out_dir / "rzsm_dry_state_transition_summary.png", dpi=150)
            plt.close()
            print("  Saved: rzsm_dry_state_transition_summary.png")

    except Exception as e:
        print(f"  [WARN] Figure generation failed: {e}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="Compute RZSM OPL-reference relative dry-state diagnostics.")
    p.add_argument("--input",  required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--reference", default="opl_available_period",
                   choices=["opl_available_period"])
    p.add_argument("--sample", type=int, default=None,
                   help=("Row-level random sample (DEBUGGING ONLY). "
                         "WARNING: breaks pixel-month reference distributions."))
    p.add_argument("--sample-pixels", type=int, default=None,
                   help=("Randomly select N unique pixels and keep ALL rows for those "
                         "pixels. This preserves the full 2016-2020 OPL reference "
                         "per pixel × calendar-month group."))
    p.add_argument("--dry-run", action="store_true",
                   help=("Run diagnostics without writing final outputs. "
                         "Saves summaries to outputs/*/dryrun/ only."))
    p.add_argument("--write", action="store_true",
                   help="Write the enriched output parquet to --output path.")
    p.add_argument("--exclude-jja", action="store_true",
                   help="Exclude June-July-August months.")
    p.add_argument("--spatial-strata", nargs="+",
                   default=["all"],
                   choices=["all", "land_cover", "basin_id", "irrigation_class"])
    return p.parse_args()


def main():
    args = parse_args()

    print("=" * 70)
    print("RZSM OPL-reference relative dry-state diagnostics")
    print("=" * 70)
    print()

    # ---- 1. Load data
    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"ERROR: input file not found: {input_path}")

    print(f"Reading: {input_path}")
    df = pd.read_parquet(input_path)
    print(f"  Full dataset : {len(df):,} rows × {df.shape[1]} columns")

    # ---- 2. Inspect coverage
    years = sorted(df["year"].unique()) if "year" in df.columns else []
    months = sorted(df["month"].unique()) if "month" in df.columns else []
    print(f"  Available years  : {years}")
    print(f"  Available months : {months}")
    print(f"  2015 present     : {2015 in years}")
    print(f"  2020 present     : {2020 in years}")

    # ---- 3. Column detection
    pixel_cols = PIXEL_COLS if all(c in df.columns for c in PIXEL_COLS) else ALT_PIXEL_COLS
    print(f"  Pixel identifiers: {pixel_cols}")

    missing = [c for c in REQUIRED_RZSM if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: missing required columns: {missing}")
    print(f"  RZSM columns     : OK ({REQUIRED_RZSM})")

    opt_cols = {"land_cover": "land_cover" in df.columns,
                "irrigation_fraction": "irrigation_fraction" in df.columns,
                "basin_id": "basin_id" in df.columns}
    for col, present in opt_cols.items():
        print(f"  {col:25s}: {'present' if present else 'MISSING (strata skipped)'}")

    n_pixels = df.groupby(pixel_cols).ngroups
    print(f"  Unique pixels    : {n_pixels:,}")

    # ---- 4. Optional filters
    if args.exclude_jja:
        df = df[~df["month"].isin([6, 7, 8])].copy()
        print(f"  After JJA exclusion: {len(df):,} rows")

    # ---- 5. Sampling strategy
    if args.sample_pixels:
        all_pixels = df[pixel_cols].drop_duplicates()
        n_sample = min(args.sample_pixels, len(all_pixels))
        sampled_pixels = all_pixels.sample(n=n_sample, random_state=42)
        df_work = df.merge(sampled_pixels, on=pixel_cols, how="inner")
        print(f"  Pixel-preserving sample: {n_sample:,} pixels → {len(df_work):,} rows")
        print(f"  (All years/months retained per pixel — OPL reference intact)")
    elif args.sample:
        print(f"  [WARNING] Row-level sampling breaks pixel-month reference distributions")
        print(f"  [WARNING] and should NOT be used to interpret percentile/class diagnostics.")
        df_work = df.sample(n=min(args.sample, len(df)), random_state=42)
        print(f"  Row-sampled {len(df_work):,} rows (debugging only)")
    else:
        df_work = df

    # ---- 6. Compute diagnostics
    print()
    print("Computing OPL-reference percentile rankings and dry-state diagnostics...")
    df_enriched, qc_df = compute_dry_state_diagnostics(df_work, pixel_cols, verbose=True)

    # ---- 7. Print target preview
    new_cols = [c for c in df_enriched.columns if c not in df.columns]
    print()
    print(f"  New columns created : {len(new_cols)}")
    print("  Sample of new targets:")
    preview_cols = [c for c in [
        "rzsm_pct_opl_ref_opl", "rzsm_pct_da_nocdf_ref_opl",
        "delta_rzsm_pct_nocdf_minus_opl",
        "rzsm_dry_class_opl", "rzsm_dry_class_da_nocdf",
        "rzsm_dry_class_transition_nocdf_minus_opl",
        "rzsm_transition_label_nocdf",
    ] if c in df_enriched.columns]
    print(df_enriched[preview_cols].describe(include="all").T.to_string())

    # ---- 8. Transition distribution summary
    print()
    if "rzsm_transition_label_nocdf" in df_enriched.columns:
        cts = df_enriched["rzsm_transition_label_nocdf"].value_counts(dropna=True)
        pct = cts / cts.sum() * 100
        print("  Transition distribution (DA-NoCDF vs OPL):")
        for lbl in ["attenuation", "no_change", "intensification"]:
            print(f"    {lbl:18s}: {pct.get(lbl, 0):.1f}%")

    # ---- 9. Route outputs: dry-run goes to dryrun/ subdirs, final run to main dirs
    if args.dry_run:
        table_dir = Path("outputs/tables/dryrun")
        fig_dir   = Path("outputs/figures/rzsm_dry_state/dryrun")
        print("  [dry-run] Outputs routed to outputs/*/dryrun/ (not final dirs)")
    else:
        table_dir = Path("outputs/tables")
        fig_dir   = Path("outputs/figures/rzsm_dry_state")
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    compute_area_summaries(df_enriched, table_dir)
    compute_transition_summaries(df_enriched, table_dir)
    save_target_definitions(table_dir)
    save_below_ref_min_summary(df_enriched, table_dir)

    # QC reference quality
    qc_df.to_csv(table_dir / "rzsm_dry_state_reference_quality.csv", index=False)
    print(f"  Saved: rzsm_dry_state_reference_quality.csv")

    # Dataset summary
    sample_desc = (f"{args.sample_pixels} pixels" if args.sample_pixels
                   else (f"{args.sample} rows (row-sample)" if args.sample else "full dataset"))
    summary = {
        "n_rows_full_dataset": len(df),
        "n_rows_processed": len(df_enriched),
        "n_pixels_in_sample": (args.sample_pixels if args.sample_pixels else n_pixels),
        "sample_description": sample_desc,
        "years_available": str(years),
        "months_available": str(months),
        "reference_period": "OPL 2016-2020 (5 years, 60 months)",
        "reference_method": "OPL-reference percentile ranking (Hazen plotting positions)",
        "period_caveat": (
            f"Reference period: {len(years)} years only (2016-2020). "
            f"Each pixel × calendar-month group has at most {len(years)} OPL values. "
            f"D3/D4 thresholds (<5th, <2nd pct) are coarse. "
            f"This is NOT a long-term drought climatology."
        ),
        "n_new_columns": len(new_cols),
    }
    pd.DataFrame([summary]).T.rename(columns={0: "value"}).to_csv(
        table_dir / "rzsm_dry_state_dataset_summary.csv")
    print(f"  Saved: rzsm_dry_state_dataset_summary.csv")

    # ---- 10. QC figures
    print()
    print("Generating QC figures...")
    make_qc_figures(df_enriched, fig_dir)

    # ---- 11. Write output parquet (only with --write)
    print()
    if args.write:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Writing enriched parquet: {output_path}")
        df_enriched.to_parquet(output_path, index=False)
        print(f"  Done: {output_path.stat().st_size / 1e6:.1f} MB")
    else:
        mem_est_mb = df.memory_usage(deep=True).sum() * (1 + len(new_cols) / df.shape[1]) / 1e6
        print("  --write not set. Skipping output parquet.")
        print(f"  Estimated full-run memory : ~{mem_est_mb:.0f} MB")
        print(f"  Estimated full-run rows   : {len(df):,}")
        print()
        print("  *** WARNINGS ***")
        print("  - Reference period: 5 years (60 months) only.")
        print("  - This is NOT a long-term drought climatology.")
        print("  - D3/D4 thresholds are coarse and should be interpreted cautiously.")
        print("  - Use 'within-period relative dry-state ranking' terminology only.")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
