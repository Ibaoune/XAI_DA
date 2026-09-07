# LIS/Noah-MP Real Data Variable Inventory

This report was generated in read-only mode to assist with config mapping.

## A. Summary of Found Directories & Files

- **OPL**: Found in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/OPL_noirr_2016_2020`
- **DA-NoCDF**: Found in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020`
- **DA-CDF**: Found in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020`
- **SMAP**: Found in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/output`
- **IMERG**: `No .nc files` in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/data/forcing/IMERG`
- **MERRA2**: `No .nc files` in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/data/forcing/MERRA2`
- **static_fields**: Found in `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/data/lis_input`

## B & C. Dimensions and Variables by Category

### OPL
- **Dimensions**: {'ntiles': 16030, 'dim2': 4, 'dim3': 3, 'dim1': 7, 'time': 1}
- **Coordinates**: ['time']
- **Variables**:
  - `SFCRUNOFF` (m) - accumulated surface runoff
  - `UDRRUNOFF` (m) - accumulated sub-surface runoff
  - `SMC` (m3/m3) - volumtric soil moisture
  - `SH2O` (m3/m3) - volumtric liquid soil moisture
  - `TSLB` (K) - soil temperature
  - `SNEQV` (mm) - snow water equivalent
  - `SNOWH` (m) - physical snow depth
  - `CANWAT` (mm) - total canopy water + ice
  - `ACSNOM` (-) - accumulated snow melt leaving pack
  - `ACSNOW` (mm) - accumulated snow on grid
  - `ISNOW` (-) - actual no. of snow layers
  - `TV` (K) - vegetation leaf temperature
  - `TG` (K) - bulk ground surface temperature
  - `CANICE` (mm) - canopy-intercepted ice
  - `CANLIQ` (mm) - canopy-intercepted liquid water
  - `EAH` (Pa) - canopy air vapor pressure
  - `TAH` (K) - canopy air temperature
  - `CM` (-) - bulk momentum drag coefficient
  - `CH` (-) - bulk sensible heat exchange coefficient
  - `FWET` (-) - wetted or snowed fraction of canopy
  - `SNEQVO` (mm h2o) - snow mass at last time step
  - `ALBOLD` (-) - snow albedo at last time step
  - `QSNOW` (mm/s) - snowfall on the ground
  - `WSLAKE` (mm) - lake water storage
  - `ZWT` (m) - water table depth
  - `WA` (mm) - water in aquifer
  - `WT` (mm) - water in aquifer and saturated soil
  - `TSNO` (K) - snow layer temperature
  - `ZSS` (m) - snow/soil layer depth from snow surface
  - `SNOWICE` (mm) - snow layer ice
  - `SNOWLIQ` (mm) - snow layer liquid water
  - `LFMASS` (g/m2) - leaf mass
  - `RTMASS` (g/m2) - mass of fine roots
  - `STMASS` (g/m2) - stem mass
  - `WOOD` (g/m2) - mass of wood (including woody roots)
  - `STBLCP` (g/m2) - stable carbon in deep soil
  - `FASTCP` (g/m2) - short-lived carbon in shallow soil
  - `LAI` (-) - leaf area index
  - `SAI` (-) - stem area index
  - `TAUSS` (-) - snow age factor
  - `SMOISEQ` (m3/m3) - equilibrium volumetric soil moisture content
  - `SMCWTD` (-) - soil moisture content in the layer to the water table when deep
  - `DEEPRECH` (-) - recharge to the water table when deep
  - `RECH` (-) - recharge to the water table (diagnostic)
  - `GRAIN` (g/m2) - mass of grain XING
  - `GDD` (-) - growing degree days XING (based on 10C)
  - `PGS` (-) - growing degree days XING
  - `lat` (degree_north) - latitude
  - `lon` (degree_east) - longitude

### DA-NoCDF
- **Dimensions**: {'ntiles': 320600, 'dim2': 4, 'dim3': 3, 'dim1': 7, 'time': 1}
- **Coordinates**: ['time']
- **Variables**:
  - `SFCRUNOFF` (m) - accumulated surface runoff
  - `UDRRUNOFF` (m) - accumulated sub-surface runoff
  - `SMC` (m3/m3) - volumtric soil moisture
  - `SH2O` (m3/m3) - volumtric liquid soil moisture
  - `TSLB` (K) - soil temperature
  - `SNEQV` (mm) - snow water equivalent
  - `SNOWH` (m) - physical snow depth
  - `CANWAT` (mm) - total canopy water + ice
  - `ACSNOM` (-) - accumulated snow melt leaving pack
  - `ACSNOW` (mm) - accumulated snow on grid
  - `ISNOW` (-) - actual no. of snow layers
  - `TV` (K) - vegetation leaf temperature
  - `TG` (K) - bulk ground surface temperature
  - `CANICE` (mm) - canopy-intercepted ice
  - `CANLIQ` (mm) - canopy-intercepted liquid water
  - `EAH` (Pa) - canopy air vapor pressure
  - `TAH` (K) - canopy air temperature
  - `CM` (-) - bulk momentum drag coefficient
  - `CH` (-) - bulk sensible heat exchange coefficient
  - `FWET` (-) - wetted or snowed fraction of canopy
  - `SNEQVO` (mm h2o) - snow mass at last time step
  - `ALBOLD` (-) - snow albedo at last time step
  - `QSNOW` (mm/s) - snowfall on the ground
  - `WSLAKE` (mm) - lake water storage
  - `ZWT` (m) - water table depth
  - `WA` (mm) - water in aquifer
  - `WT` (mm) - water in aquifer and saturated soil
  - `TSNO` (K) - snow layer temperature
  - `ZSS` (m) - snow/soil layer depth from snow surface
  - `SNOWICE` (mm) - snow layer ice
  - `SNOWLIQ` (mm) - snow layer liquid water
  - `LFMASS` (g/m2) - leaf mass
  - `RTMASS` (g/m2) - mass of fine roots
  - `STMASS` (g/m2) - stem mass
  - `WOOD` (g/m2) - mass of wood (including woody roots)
  - `STBLCP` (g/m2) - stable carbon in deep soil
  - `FASTCP` (g/m2) - short-lived carbon in shallow soil
  - `LAI` (-) - leaf area index
  - `SAI` (-) - stem area index
  - `TAUSS` (-) - snow age factor
  - `SMOISEQ` (m3/m3) - equilibrium volumetric soil moisture content
  - `SMCWTD` (-) - soil moisture content in the layer to the water table when deep
  - `DEEPRECH` (-) - recharge to the water table when deep
  - `RECH` (-) - recharge to the water table (diagnostic)
  - `GRAIN` (g/m2) - mass of grain XING
  - `GDD` (-) - growing degree days XING (based on 10C)
  - `PGS` (-) - growing degree days XING
  - `lat` (degree_north) - latitude
  - `lon` (degree_east) - longitude

### DA-CDF
- **Dimensions**: {'ntiles': 320600, 'dim2': 4, 'dim3': 3, 'dim1': 7, 'time': 1}
- **Coordinates**: ['time']
- **Variables**:
  - `SFCRUNOFF` (m) - accumulated surface runoff
  - `UDRRUNOFF` (m) - accumulated sub-surface runoff
  - `SMC` (m3/m3) - volumtric soil moisture
  - `SH2O` (m3/m3) - volumtric liquid soil moisture
  - `TSLB` (K) - soil temperature
  - `SNEQV` (mm) - snow water equivalent
  - `SNOWH` (m) - physical snow depth
  - `CANWAT` (mm) - total canopy water + ice
  - `ACSNOM` (-) - accumulated snow melt leaving pack
  - `ACSNOW` (mm) - accumulated snow on grid
  - `ISNOW` (-) - actual no. of snow layers
  - `TV` (K) - vegetation leaf temperature
  - `TG` (K) - bulk ground surface temperature
  - `CANICE` (mm) - canopy-intercepted ice
  - `CANLIQ` (mm) - canopy-intercepted liquid water
  - `EAH` (Pa) - canopy air vapor pressure
  - `TAH` (K) - canopy air temperature
  - `CM` (-) - bulk momentum drag coefficient
  - `CH` (-) - bulk sensible heat exchange coefficient
  - `FWET` (-) - wetted or snowed fraction of canopy
  - `SNEQVO` (mm h2o) - snow mass at last time step
  - `ALBOLD` (-) - snow albedo at last time step
  - `QSNOW` (mm/s) - snowfall on the ground
  - `WSLAKE` (mm) - lake water storage
  - `ZWT` (m) - water table depth
  - `WA` (mm) - water in aquifer
  - `WT` (mm) - water in aquifer and saturated soil
  - `TSNO` (K) - snow layer temperature
  - `ZSS` (m) - snow/soil layer depth from snow surface
  - `SNOWICE` (mm) - snow layer ice
  - `SNOWLIQ` (mm) - snow layer liquid water
  - `LFMASS` (g/m2) - leaf mass
  - `RTMASS` (g/m2) - mass of fine roots
  - `STMASS` (g/m2) - stem mass
  - `WOOD` (g/m2) - mass of wood (including woody roots)
  - `STBLCP` (g/m2) - stable carbon in deep soil
  - `FASTCP` (g/m2) - short-lived carbon in shallow soil
  - `LAI` (-) - leaf area index
  - `SAI` (-) - stem area index
  - `TAUSS` (-) - snow age factor
  - `SMOISEQ` (m3/m3) - equilibrium volumetric soil moisture content
  - `SMCWTD` (-) - soil moisture content in the layer to the water table when deep
  - `DEEPRECH` (-) - recharge to the water table when deep
  - `RECH` (-) - recharge to the water table (diagnostic)
  - `GRAIN` (g/m2) - mass of grain XING
  - `GDD` (-) - growing degree days XING (based on 10C)
  - `PGS` (-) - growing degree days XING
  - `lat` (degree_north) - latitude
  - `lon` (degree_east) - longitude

### SMAP
- **Dimensions**: {'north_south': 121, 'east_west': 181}
- **Coordinates**: []
- **Variables**:
  - `anlys_incr_Soil Moisture Layer 1_01` (N/A) - N/A
  - `anlys_incr_Soil Moisture Layer 2_01` (N/A) - N/A
  - `anlys_incr_Soil Moisture Layer 3_01` (N/A) - N/A
  - `anlys_incr_Soil Moisture Layer 4_01` (N/A) - N/A

### static_fields
- **Dimensions**: {'time': 1, 'north_south': 121, 'east_west': 181, 'sfctypes': 20, 'soiltypes': 16, 'month': 12, 'north_south_MERRA2': 361, 'east_west_MERRA2': 576, 'north_south_b': 125, 'east_west_b': 185}
- **Coordinates**: ['time']
- **Variables**:
  - `DOMAINMASK` () - N/A
  - `LANDMASK` () - N/A
  - `SURFACETYPE` (-) - N/A
  - `LANDCOVER` () - N/A
  - `TEXTURE` () - N/A
  - `ELEVFGRD` (-) - N/A
  - `ELEVATION` (m) - N/A
  - `GREENNESS` (-) - N/A
  - `SHDMIN` (-) - N/A
  - `SHDMAX` (-) - N/A
  - `ALBEDO` (-) - N/A
  - `MXSNALBEDO` (-) - N/A
  - `TBOT` (K) - N/A
  - `SLOPETYPE` (-) - N/A
  - `NOAHMP36_PBLH` (m) - N/A
  - `IRRIGFRAC` (-) - N/A
  - `ELEV_MERRA2` (m) - N/A
  - `ELEVDIFF_MERRA2` (m) - N/A
  - `lat` (degrees_north) - N/A
  - `lon` (degrees_east) - N/A
  - `lat_b` (degrees_north) - N/A
  - `lon_b` (degrees_east) - N/A
  - `CROPTYPE` (-) - N/A

## D. Recommended Mapping for config.yaml (Template)
```yaml
real_data_variable_mapping_template:
  targets:
    SSM_OPL: "SoilMoist_tavg"
    RZSM_OPL: "RootMoist_tavg"
    ET_OPL: "Evap_tavg"
  predictors:
    precip_IMERG: "Rainf_tavg"
```

## E. Missing or Ambiguous Variables
- RZSM requires verifying the layer aggregation (e.g., layers 1-3) in LIS outputs vs standard variables.
- Innovation/Increments naming convention in SMAP output files must be verified (e.g. `sm_innov`).

## F. Questions before proceeding
1. Should we calculate RZSM manually from layer 1, 2, and 3 of `SoilMoist_tavg` or is there a direct output?
2. For the static fields (soil texture, cropland), are they inside `lis_input.d01.nc` or separate files?
