"""
V1 in-situ precipitation integration is currently disabled because the available station file ends in 2014 and does not overlap with the 2016-2020 SMAP assimilation period.
"""
import os
import argparse
import pandas as pd
import numpy as np
import yaml
from scipy.spatial import cKDTree

def generate_inventory(df_raw, report_path):
    print("Generating inventory report...")
    df = df_raw.copy()
    
    total_rows = len(df)
    n_stations = df['Station'].nunique()
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    missing_precip = df['Precipitation'].isna().sum()
    precip_stats = df['Precipitation'].describe()
    
    min_lon, max_lon = df['Longitude'].min(), df['Longitude'].max()
    min_lat, max_lat = df['Latitude'].min(), df['Latitude'].max()
    
    df['Year'] = df['Date'].dt.year
    stations_per_year = df.groupby('Year')['Station'].nunique()
    
    df_2016_2020 = df[(df['Date'] >= '2016-01-01') & (df['Date'] <= '2020-12-31')]
    n_stations_2016_2020 = df_2016_2020['Station'].nunique()
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# In-Situ Precipitation Inventory\n\n")
        f.write(f"- **Total rows**: {total_rows}\n")
        f.write(f"- **Total stations**: {n_stations}\n")
        f.write(f"- **Period**: {min_date.date()} to {max_date.date()}\n")
        f.write(f"- **Missing Precipitation Values**: {missing_precip}\n")
        f.write(f"- **Stations active 2016-2020**: {n_stations_2016_2020}\n\n")
        
        f.write("## Spatial Coverage\n")
        f.write(f"- **Longitude**: {min_lon:.4f} to {max_lon:.4f}\n")
        f.write(f"- **Latitude**: {min_lat:.4f} to {max_lat:.4f}\n\n")
        
        f.write("## Precipitation Statistics (Hypothesis: mm/day)\n")
        f.write("```\n")
        f.write(precip_stats.to_string())
        f.write("\n```\n\n")
        
        f.write("## Active Stations per Year\n")
        f.write("```\n")
        f.write(stations_per_year.to_string())
        f.write("\n```\n")

def process_insitu():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mini-test", action="store_true")
    args = parser.parse_args()
    
    print("--- 1. Reading in-situ dataset ---")
    insitu_file = "/home/mohammad.elaabaribao/lustre/climat-um6p-st-iwri-7ksifkvwkuy/shared/TEAM/data/Observed_data/ABH_stations_plusziz_and_abhbc1.csv"
    df_insitu = pd.read_csv(insitu_file)
    df_insitu['Date'] = pd.to_datetime(df_insitu['Date'])
    
    inventory_report = "reports/insitu_precip_inventory.md"
    generate_inventory(df_insitu, inventory_report)
    
    print("--- 2. Temporal Aggregation ---")
    df_p = df_insitu[(df_insitu['Date'] >= '2016-01-01') & (df_insitu['Date'] <= '2020-12-31')].copy()
    df_p['year'] = df_p['Date'].dt.year
    df_p['month'] = df_p['Date'].dt.month
    
    monthly_agg = df_p.groupby(['Station', 'year', 'month']).agg(
        gauge_precip_monthly=('Precipitation', 'sum'),
        n_days_available=('Precipitation', 'count'),
        Longitude=('Longitude', 'first'),
        Latitude=('Latitude', 'first')
    ).reset_index()
    
    monthly_agg['expected_days'] = pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01').dt.days_in_month
    monthly_agg['completeness_ratio'] = monthly_agg['n_days_available'] / monthly_agg['expected_days']
    
    monthly_valid = monthly_agg[monthly_agg['completeness_ratio'] >= 0.8].copy()
    
    out_csv = "data/processed/station_monthly_precip.csv"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    monthly_valid.to_csv(out_csv, index=False)
    
    print("--- 3. Dataset Update (Interpolation) ---")
    input_ds_path = "data/processed/monthly_pixel_dataset_2016_2020_static.parquet"
    if args.mini_test:
        input_ds_path = "data/processed/monthly_pixel_dataset_test_static.parquet"
        print("MINI-TEST mode: loading smaller dataset")
        
    ds = pd.read_parquet(input_ds_path)
    if args.mini_test:
        ds = ds.sample(n=min(5000, len(ds)), random_state=42)
        # Limit to 2 months
        sample_months = ds[['year', 'month']].drop_duplicates().head(2)
        ds = ds.merge(sample_months, on=['year', 'month'])
        print(f"Mini-test dataset shape: {ds.shape}")
        
    orig_shape = ds.shape
    
    ds_result = pd.DataFrame()
    
    for (y, m), group in ds.groupby(['year', 'month']):
        print(f"Interpolating {y}-{m:02d}...")
        
        stat_m = monthly_valid[(monthly_valid['year'] == y) & (monthly_valid['month'] == m)]
        if len(stat_m) < 3:
            print(f"  WARNING: Only {len(stat_m)} stations valid for {y}-{m:02d}. Proceeding anyway.")
            
        points = stat_m[['Longitude', 'Latitude']].values
        values = stat_m['gauge_precip_monthly'].values
        
        if len(points) == 0:
            group['gauge_precip'] = np.nan
            group['gauge_station_count_used'] = 0
            group['gauge_distance_nearest'] = np.nan
        else:
            tree = cKDTree(points)
            grid_points = group[['lon', 'lat']].values
            
            k = min(5, len(points))
            distances, indices = tree.query(grid_points, k=k)
            
            if k == 1:
                distances = distances.reshape(-1, 1)
                indices = indices.reshape(-1, 1)
                
            # Convert degrees to roughly km for filtering
            # 1 deg roughly 111km
            distances_km = distances * 111.0
            
            interpolated = np.zeros(len(grid_points))
            counts = np.zeros(len(grid_points))
            nearest_dist = distances_km[:, 0]
            
            power = 2
            max_dist_km = 150.0
            
            for i in range(len(grid_points)):
                dist = distances_km[i]
                idx = indices[i]
                
                valid = dist <= max_dist_km
                if not np.any(valid):
                    valid = [True] * k # Fallback to nearest k if none within 150km
                    
                v_dist = dist[valid]
                v_idx = idx[valid]
                v_val = values[v_idx]
                
                if np.any(v_dist == 0):
                    interpolated[i] = v_val[v_dist == 0][0]
                else:
                    weights = 1.0 / (v_dist ** power)
                    interpolated[i] = np.sum(weights * v_val) / np.sum(weights)
                    
                counts[i] = np.sum(valid)
                
            group['gauge_precip'] = interpolated
            group['gauge_station_count_used'] = counts
            group['gauge_distance_nearest'] = nearest_dist
            
        ds_result = pd.concat([ds_result, group])
        
    ds_result = ds_result.sort_values(['north_south', 'east_west', 'year', 'month']).reset_index(drop=True)
    
    # 4. Compute Metrics
    print("Computing error metrics and lags...")
    ds_result['precipitation_error'] = ds_result['precipitation_model'] - ds_result['gauge_precip']
    ds_result['abs_precipitation_error'] = ds_result['precipitation_error'].abs()
    ds_result['precipitation_ratio'] = ds_result['precipitation_model'] / ds_result['gauge_precip'].replace(0, np.nan)
    
    ds_result = ds_result.sort_values(['north_south', 'east_west', 'year', 'month'])
    
    # 3-month rolling
    def rolling_sum_3(x): return x.rolling(window=3, min_periods=1).sum()
    
    g = ds_result.groupby(['north_south', 'east_west'])
    ds_result['gauge_precip_3month'] = g['gauge_precip'].apply(rolling_sum_3).reset_index(level=[0,1], drop=True)
    ds_result['precipitation_model_3month'] = g['precipitation_model'].apply(rolling_sum_3).reset_index(level=[0,1], drop=True)
    ds_result['precipitation_error_3month'] = ds_result['precipitation_model_3month'] - ds_result['gauge_precip_3month']
    
    ds_result['gauge_precip_lag1'] = g['gauge_precip'].shift(1)
    ds_result['precipitation_error_lag1'] = g['precipitation_error'].shift(1)
    
    new_shape = ds_result.shape
    print(f"Original shape: {orig_shape}, New shape: {new_shape}")
    
    # Save
    out_ds = "data/processed/monthly_pixel_dataset_2016_2020_static_precip.parquet"
    if args.mini_test:
        out_ds = out_ds.replace(".parquet", "_test.parquet")
    ds_result.to_parquet(out_ds)
    print(f"Saved dataset to {out_ds}")
    
    # 5. Merge Report
    merge_report = "reports/insitu_precip_merge_report.md"
    if args.mini_test:
        merge_report = merge_report.replace(".md", "_test.md")
        
    with open(merge_report, "w") as f:
        f.write("# In-Situ Precipitation Merge Report (V1)\n\n")
        f.write(f"- **Shape before**: {orig_shape}\n")
        f.write(f"- **Shape after**: {new_shape}\n")
        f.write(f"- **Target Columns Intact**: {all(c in ds_result.columns for c in ['increment_SSM_DA_NoCDF', 'delta_DA_NoCDF_minus_OPL_ET'])}\n\n")
        
        f.write("## Station Coverage per Month\n")
        f.write("```\n")
        f.write(ds_result.groupby(['year', 'month'])['gauge_station_count_used'].mean().to_string())
        f.write("\n```\n\n")
        
        f.write("## Precipitation Statistics\n")
        f.write("### gauge_precip\n")
        f.write("```\n")
        f.write(ds_result['gauge_precip'].describe().to_string())
        f.write("\n```\n")
        
        f.write("### precipitation_model\n")
        f.write("```\n")
        f.write(ds_result['precipitation_model'].describe().to_string())
        f.write("\n```\n")
        
        f.write("### precipitation_error (model - gauge)\n")
        f.write("```\n")
        f.write(ds_result['precipitation_error'].describe().to_string())
        f.write("\n```\n")
        
if __name__ == "__main__":
    process_insitu()
