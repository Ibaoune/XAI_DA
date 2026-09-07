import os
import argparse
import pandas as pd
import xarray as xr
import numpy as np
import glob
import sys

def load_static_predictors(static_file):
    print(f"Loading static predictors from {static_file}...")
    ds = xr.open_dataset(static_file)
    
    static_data = {}
    
    # Check for elevation
    if 'ELEVFGRD' in ds:
        static_data['elevation'] = ds['ELEVFGRD'].values
    elif 'ELEVATION' in ds:
        static_data['elevation'] = ds['ELEVATION'].values
    elif 'elevation' in ds:
        static_data['elevation'] = ds['elevation'].values
    else:
        print("WARNING: Elevation not found in static file.")
        
    # Check for land cover
    lc_var = None
    for var in ['LANDCOVER', 'landcover', 'Landcover_inst']:
        if var in ds:
            lc_var = var
            break
            
    if lc_var:
        val = ds[lc_var]
        if len(val.dims) == 3:
            # e.g., (sfctypes, north_south, east_west)
            class_dim = val.dims[0]
            print(f"Found {lc_var} with class dimension {class_dim}. Computing argmax...")
            dominant = val.argmax(dim=class_dim).values + 1
            max_frac = val.max(dim=class_dim).values
            static_data['land_cover'] = dominant
            static_data['land_cover_dominant_fraction'] = max_frac
        elif len(val.dims) == 2:
            print(f"Found {lc_var} as 2D categorical.")
            static_data['land_cover'] = val.values
        else:
            print(f"WARNING: {lc_var} has unexpected dimensions {val.dims}. Skipping.")
    else:
        print("WARNING: Land cover not found in static file.")
        
    # Check for soil texture
    st_var = None
    for var in ['TEXTURE', 'SOILTEXTURE', 'soil_texture']:
        if var in ds:
            st_var = var
            break
            
    if st_var:
        val = ds[st_var]
        if len(val.dims) == 3:
            class_dim = val.dims[0]
            print(f"Found {st_var} with class dimension {class_dim}. Computing argmax...")
            dominant = val.argmax(dim=class_dim).values + 1
            max_frac = val.max(dim=class_dim).values
            static_data['soil_texture'] = dominant
            static_data['soil_texture_dominant_fraction'] = max_frac
        elif len(val.dims) == 2:
            print(f"Found {st_var} as 2D categorical.")
            static_data['soil_texture'] = val.values
        else:
            print(f"WARNING: {st_var} has unexpected dimensions {val.dims}. Skipping.")
    else:
        print("WARNING: Soil texture not found in static file.")
        
    # Check for irrigation fraction
    ir_var = None
    for var in ['IRRIGFRAC', 'irrigation_fraction', 'IrrigFrac']:
        if var in ds:
            ir_var = var
            break
            
    if ir_var:
        val = ds[ir_var]
        if len(val.dims) == 2:
            print(f"Found {ir_var} as 2D continuous variable.")
            static_data['irrigation_fraction'] = val.values
        else:
            print(f"WARNING: {ir_var} has unexpected dimensions {val.dims}. Skipping.")
    else:
        print("WARNING: Irrigation fraction not found in static file.")
        
    # Check for crop type
    ct_var = None
    for var in ['CROPTYPE', 'crop_type']:
        if var in ds:
            ct_var = var
            break
            
    if ct_var:
        val = ds[ct_var]
        if len(val.dims) == 3:
            class_dim = val.dims[0]
            print(f"Found {ct_var} with class dimension {class_dim}. Computing argmax...")
            dominant = val.argmax(dim=class_dim).values + 1
            max_frac = val.max(dim=class_dim).values
            static_data['crop_type'] = dominant
            static_data['crop_type_dominant_fraction'] = max_frac
        elif len(val.dims) == 2:
            print(f"Found {ct_var} as 2D categorical.")
            static_data['crop_type'] = val.values
        else:
            print(f"WARNING: {ct_var} has unexpected dimensions {val.dims}. Skipping.")
    else:
        print("WARNING: Crop type not found in static file.")
        
    # Build a DataFrame flat mapping
    ns_dim, ew_dim = ds.dims.get('north_south'), ds.dims.get('east_west')
    if not ns_dim or not ew_dim:
        print("Error: north_south and east_west dimensions not found in static file.")
        sys.exit(1)
        
    ns_idx, ew_idx = np.meshgrid(np.arange(ns_dim), np.arange(ew_dim), indexing='ij')
    flat_data = {
        'north_south': ns_idx.flatten(),
        'east_west': ew_idx.flatten()
    }
    
    for k, v in static_data.items():
        flat_data[k] = v.flatten()
        
    static_df = pd.DataFrame(flat_data)
    
    # We only keep rows where at least one static variable is not NaN and not landmask 0, 
    # but to be perfectly aligned with the merge, we keep all of them and inner join/left join
    print(f"Static predictors prepared: {static_df.shape[0]} total grid points.")
    return static_df


def process_datasets(mini_test=False):
    static_file = '/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/data/lis_input/lis_input_NorthMor_5km.nc'
    if not os.path.exists(static_file):
        print(f"Error: {static_file} not found.")
        return
        
    static_df = load_static_predictors(static_file)
    
    input_parts_dir = "data/processed/monthly_parts"
    output_parts_dir = "data/processed/monthly_parts_static"
    output_dataset = "data/processed/monthly_pixel_dataset_2016_2020_static.parquet"
    
    os.makedirs(output_parts_dir, exist_ok=True)
    
    part_files = sorted(glob.glob(f"{input_parts_dir}/monthly_pixel_dataset_*.parquet"))
    if not part_files:
        print("Error: No monthly parts found.")
        return
        
    if mini_test:
        part_files = part_files[:1] # just one file for test
        output_dataset = "data/processed/monthly_pixel_dataset_test_static.parquet"
        print("Running MINI-TEST on 1 part.")
        
    all_dfs = []
    
    for pf in part_files:
        print(f"Processing {pf}...")
        df = pd.read_parquet(pf)
        n_rows_before = len(df)
        
        # Merge static predictors
        df_merged = df.merge(static_df, on=['north_south', 'east_west'], how='left')
        
        n_rows_after = len(df_merged)
        
        if n_rows_before != n_rows_after:
            print(f"ERROR: Row count mismatch! Before: {n_rows_before}, After: {n_rows_after}")
            sys.exit(1)
            
        out_pf = os.path.join(output_parts_dir, os.path.basename(pf).replace(".parquet", "_static.parquet"))
        df_merged.to_parquet(out_pf)
        
        all_dfs.append(df_merged)
        
    print("Combining into final static dataset...")
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    if mini_test and len(final_df) > 50000:
        final_df = final_df.sample(n=50000, random_state=42)
        
    final_df.to_parquet(output_dataset)
    print(f"Successfully generated {output_dataset} with shape {final_df.shape}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mini-test", action="store_true", help="Run a quick test on a subset")
    args = parser.parse_args()
    
    process_datasets(mini_test=args.mini_test)
