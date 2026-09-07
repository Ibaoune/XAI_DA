# Precipitation Error V1 Readiness Report

## Status
- **ready_for_v1**: no

## Why
The available in-situ precipitation data in `data/insitu_data/` consists of only 4 stations (Agadir-massira, Chefchaouen, Guelmim, Tiznit) for the entire Moroccan domain. Furthermore, the raw files do not contain explicit latitude and longitude coordinates. This spatial density is statistically insufficient to train a pixel-based Random Forest model over a 5 km grid without introducing severe representativeness bias and overfitting. The vast majority of the pixels would lack a valid precipitation-error predictor.

## Required Additional Data
- A denser network of in-situ stations covering the Moroccan domain.
- Explicit geospatial metadata (latitude, longitude, elevation) for every station.
- Continuous records over the 2016–2020 period to match the SMAP DA temporal window.

## Recommended Next Step
- **Block the V1 production**: Do not execute `04_add_precip_error_to_rf_dataset.py` until a comprehensive, dense gauge dataset is provided.
- Focus on the V0 package (without precipitation error) for the main manuscript, explicitly mentioning this limitation.
- Proceed with the drought diagnostics pipeline using the existing robust states and fluxes.
