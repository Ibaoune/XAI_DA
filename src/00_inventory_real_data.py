import os
import glob
import xarray as xr
import pandas as pd
from pathlib import Path

def inventory_real_data():
    print("--- Starting Advanced Real Data Inventory (00_inventory_real_data.py) ---")
    
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, "lis_and_team_data_inventory.md")
    
    # 1. Inspect LIS Outputs (focusing on LIS_HIST*.nc)
    base_lis_dir = "/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020"
    
    experiments = {
        "OPL": os.path.join(base_lis_dir, "OPL_noirr_2016_2020"),
        "DA-NoCDF": os.path.join(base_lis_dir, "DA_nocdf_noirr_2016_2020"),
        "DA-CDF": os.path.join(base_lis_dir, "DA_cdf_noirr_2016_2020")
    }
    
    lis_inventory = []
    
    print("Scanning LIS directories for HIST NetCDF files...")
    for exp, exp_dir in experiments.items():
        if not os.path.exists(exp_dir):
            print(f"Directory not found for {exp}: {exp_dir}")
            continue
            
        hist_files = glob.glob(os.path.join(exp_dir, "**", "LIS_HIST*.nc"), recursive=True)
        if not hist_files:
            # Fallback to RST if HIST missing, just to report
            rst_files = glob.glob(os.path.join(exp_dir, "**", "LIS_RST*.nc"), recursive=True)
            if rst_files:
                lis_inventory.append((exp, len(rst_files), "Only RST files found", None, []))
            else:
                lis_inventory.append((exp, 0, "No NC files found", None, []))
            continue
            
        # Inspect first HIST file
        sample_file = hist_files[0]
        try:
            ds = xr.open_dataset(sample_file, decode_times=False)
            dims = dict(ds.sizes)
            coords = list(ds.coords)
            
            vars_info = []
            for var_name in ds.data_vars:
                var = ds[var_name]
                long_name = var.attrs.get("long_name", "N/A")
                units = var.attrs.get("units", "N/A")
                vars_info.append(f"`{var_name}` ({units}) - {long_name}")
                
            lis_inventory.append((exp, len(hist_files), sample_file, dims, coords, vars_info))
            ds.close()
        except Exception as e:
            print(f"Failed to read {sample_file}: {e}")
            
    # 2. Inspect TEAM/data
    team_data_dir = "/home/mohammad.elaabaribao/lustre/climat-um6p-st-iwri-7ksifkvwkuy/shared/TEAM/data"
    team_inventory = []
    
    print(f"Scanning TEAM/data directory: {team_data_dir}...")
    if os.path.exists(team_data_dir):
        # We will walk through the directory and find files of interest
        extensions = ['.nc', '.nc4', '.csv', '.txt', '.xlsx', '.tif', '.grib', '.bin']
        
        for ext in extensions:
            files = list(Path(team_data_dir).rglob(f"*{ext}"))
            # Just take up to 5 samples per extension to keep the report concise
            for f in files[:5]:
                try:
                    size_mb = os.path.getsize(f) / (1024*1024)
                    info = {"path": str(f), "ext": ext, "size_mb": round(size_mb, 2), "details": ""}
                    
                    if ext in ['.csv', '.txt']:
                        df = pd.read_csv(f, nrows=2)
                        info["details"] = f"Columns: {list(df.columns)}"
                    elif ext in ['.nc', '.nc4']:
                        ds = xr.open_dataset(f, decode_times=False)
                        info["details"] = f"Vars: {list(ds.data_vars.keys())[:5]}"
                        ds.close()
                    else:
                        info["details"] = "Binary/Spatial file (header not parsed)"
                        
                    team_inventory.append(info)
                except Exception as e:
                    team_inventory.append({"path": str(f), "ext": ext, "size_mb": 0, "details": f"Error: {e}"})
    else:
        print("TEAM/data directory not found or not accessible.")
        
    # Generate Markdown Report
    print("Generating report...")
    with open(report_file, "w") as f:
        f.write("# LIS and TEAM Data Variable Inventory\n\n")
        
        f.write("## A. LIS Outputs Found\n\n")
        for res in lis_inventory:
            exp = res[0]
            count = res[1]
            if len(res) == 5: # Error or missing case
                f.write(f"### {exp}\n")
                f.write(f"- Files found: {count} ({res[2]})\n\n")
            else:
                sample = res[2]
                dims = res[3]
                coords = res[4]
                vars_info = res[5]
                f.write(f"### {exp}\n")
                f.write(f"- **HIST files found**: {count}\n")
                f.write(f"- **Sample inspected**: `{sample}`\n")
                f.write(f"- **Dimensions**: {dims}\n")
                f.write(f"- **Coordinates**: {coords}\n")
                f.write("- **Variables**:\n")
                for v in vars_info:
                    f.write(f"  - {v}\n")
                f.write("\n")
                
        f.write("## B. Candidate LIS Variables Identified\n")
        f.write("- **SMC** (SoilMoist_tavg): Multilayer soil moisture (often 4 layers).\n")
        f.write("- **SH2O** (SoilMoist_tavg equivalent for liquid): Liquid soil moisture.\n")
        f.write("- **ET / Qle**: Look for `Evap_tavg` or `Qle_tavg`. If `Qle_tavg` (latent heat) is present but not ET, ET can be derived via latent heat of vaporization.\n")
        f.write("- **Runoff**: `Qs_tavg` (surface) and `Qsb_tavg` (baseflow).\n")
        f.write("- **Precipitation**: `Rainf_tavg` (if present in LIS_HIST, serves as the effective forcing).\n")
        f.write("- **Water Table**: `ZWT_tavg` or `WaterTableD_tavg`.\n\n")
        
        f.write("## C. RZSM Calculation Rule\n")
        f.write("RZSM will be computed as a weighted average of SMC layers 1–3:\n")
        f.write("```text\nRZSM = (SMC1*0.1 + SMC2*0.3 + SMC3*0.6) / 1.0\n```\n")
        f.write("This represents the 0–1 m root-zone soil moisture. Individual soil layers will be kept as optional predictors.\n\n")
        
        f.write("## D. TEAM/data Inventory\n")
        if team_inventory:
            for item in team_inventory:
                f.write(f"- **File**: `{item['path']}`\n")
                f.write(f"  - Format: {item['ext']} | Size: {item['size_mb']} MB\n")
                f.write(f"  - Details: {item['details']}\n\n")
        else:
            f.write("No files found or directory inaccessible.\n\n")
            
        f.write("## E. Recommended config.yaml mapping\n")
        f.write("```yaml\n")
        f.write("# real_data_variable_mapping_template:\n")
        f.write("#   targets:\n")
        f.write("#     SSM_OPL: \"SoilMoist_tavg_1\" # Layer 1\n")
        f.write("#     RZSM_OPL: \"computed\" # RZSM calculated via rule\n")
        f.write("#     ET_OPL: \"Qle_tavg\" # Requires conversion to ET if Evap_tavg is missing\n")
        f.write("#   predictors:\n")
        f.write("#     precipitation: \"Rainf_tavg\" # From LIS_HIST\n")
        f.write("```\n")
        
    print(f"Inventory complete. Report saved to {report_file}")

if __name__ == "__main__":
    inventory_real_data()
