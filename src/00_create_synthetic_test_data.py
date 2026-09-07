import os
import numpy as np
import xarray as xr
import pandas as pd

def create_synthetic_data():
    out_dir = "data/synthetic"
    os.makedirs(out_dir, exist_ok=True)
    
    # Dimensions
    n_time = 24
    n_lat = 10
    n_lon = 12
    
    # Coordinates
    # 2019 and 2020 to cover some training and testing years
    times = pd.date_range(start="2019-01-01", periods=n_time, freq="M")
    lats = np.linspace(30, 31, n_lat)
    lons = np.linspace(-9, -8, n_lon)
    
    print(f"Creating synthetic NetCDF data in {out_dir}...")
    
    # Function to create dynamic data
    def make_dynamic_nc(var_name, data, filename):
        ds = xr.Dataset(
            {var_name: (["time", "lat", "lon"], data)},
            coords={"time": times, "lat": lats, "lon": lons}
        )
        ds.to_netcdf(os.path.join(out_dir, filename))
        
    # Function to create static data
    def make_static_nc(var_name, data, filename):
        ds = xr.Dataset(
            {var_name: (["lat", "lon"], data)},
            coords={"lat": lats, "lon": lons}
        )
        ds.to_netcdf(os.path.join(out_dir, filename))

    # Dynamic variables
    # SSM/RZSM between 0 and 0.5
    make_dynamic_nc("OPL_SSM", np.random.uniform(0.05, 0.45, (n_time, n_lat, n_lon)), "opl_ssm.nc")
    make_dynamic_nc("DA_NoCDF_SSM", np.random.uniform(0.05, 0.45, (n_time, n_lat, n_lon)), "da_nocdf_ssm.nc")
    make_dynamic_nc("DA_CDF_SSM", np.random.uniform(0.05, 0.45, (n_time, n_lat, n_lon)), "da_cdf_ssm.nc")
    
    make_dynamic_nc("OPL_RZSM", np.random.uniform(0.1, 0.5, (n_time, n_lat, n_lon)), "opl_rzsm.nc")
    make_dynamic_nc("DA_NoCDF_RZSM", np.random.uniform(0.1, 0.5, (n_time, n_lat, n_lon)), "da_nocdf_rzsm.nc")
    make_dynamic_nc("DA_CDF_RZSM", np.random.uniform(0.1, 0.5, (n_time, n_lat, n_lon)), "da_cdf_rzsm.nc")
    
    # ET positive
    make_dynamic_nc("OPL_ET", np.random.uniform(0, 10, (n_time, n_lat, n_lon)), "opl_et.nc")
    make_dynamic_nc("DA_NoCDF_ET", np.random.uniform(0, 10, (n_time, n_lat, n_lon)), "da_nocdf_et.nc")
    make_dynamic_nc("DA_CDF_ET", np.random.uniform(0, 10, (n_time, n_lat, n_lon)), "da_cdf_et.nc")
    
    # runoff / baseflow positive
    make_dynamic_nc("OPL_runoff", np.random.uniform(0, 5, (n_time, n_lat, n_lon)), "opl_runoff.nc")
    make_dynamic_nc("DA_NoCDF_runoff", np.random.uniform(0, 5, (n_time, n_lat, n_lon)), "da_nocdf_runoff.nc")
    make_dynamic_nc("DA_CDF_runoff", np.random.uniform(0, 5, (n_time, n_lat, n_lon)), "da_cdf_runoff.nc")

    make_dynamic_nc("OPL_baseflow", np.random.uniform(0, 2, (n_time, n_lat, n_lon)), "opl_baseflow.nc")
    make_dynamic_nc("DA_NoCDF_baseflow", np.random.uniform(0, 2, (n_time, n_lat, n_lon)), "da_nocdf_baseflow.nc")
    make_dynamic_nc("DA_CDF_baseflow", np.random.uniform(0, 2, (n_time, n_lat, n_lon)), "da_cdf_baseflow.nc")
    
    # Precipitation positive
    make_dynamic_nc("IMERG_precip", np.random.uniform(0, 100, (n_time, n_lat, n_lon)), "imerg_precip.nc")
    make_dynamic_nc("gauge_precip", np.random.uniform(0, 100, (n_time, n_lat, n_lon)), "gauge_precip.nc")
    
    make_dynamic_nc("SMAP_obs_count", np.random.randint(0, 15, (n_time, n_lat, n_lon)), "smap_obs_count.nc")
    
    # Static variables
    # Elevation positive
    make_static_nc("elevation", np.random.uniform(100, 3000, (n_lat, n_lon)), "elevation.nc")
    make_static_nc("slope", np.random.uniform(0, 45, (n_lat, n_lon)), "slope.nc")
    make_static_nc("cropland_fraction", np.random.uniform(0, 1, (n_lat, n_lon)), "cropland_fraction.nc")
    
    # Soil texture categories (e.g. 1 to 12)
    make_static_nc("soil_texture", np.random.randint(1, 13, (n_lat, n_lon)), "soil_texture.nc")
    make_static_nc("basin_id", np.random.randint(1, 5, (n_lat, n_lon)), "basin_id.nc")
    
    print("Synthetic datasets generated successfully.")

if __name__ == "__main__":
    create_synthetic_data()
