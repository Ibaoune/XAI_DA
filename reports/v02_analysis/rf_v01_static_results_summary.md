# Random Forest V0.1 (Static Predictors) Results Summary

## A. Dataset
- **Source**: `monthly_pixel_dataset_2016_2020_static.parquet`
- **Split**: Train (2016-2019), Test (2020)
- **Targets trained**: 13

## B. Configuration
- **Model**: `RandomForestRegressor(n_estimators=150, max_features='sqrt', min_samples_leaf=5)`
- **Preprocessing**: `SimpleImputer` + `OneHotEncoder(handle_unknown='ignore')`
- **Mode**: `environmental_explanatory` (Strictly independent variables, no leakage)

## C. Metrics Summary
