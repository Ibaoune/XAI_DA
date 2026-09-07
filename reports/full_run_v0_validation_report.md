# Full Run V0 Technical Validation Report

## A. Dataset Overview
- **Path**: `data/processed/monthly_pixel_dataset_2016_2020.parquet`
- **Total Rows**: 961800
- **Total Columns**: 66
- **Total Months**: 60
- **Period**: 201601 to 202012
- **Missing Months**: None. All 60 months present.
- **Pixels per Month**: ~16030
- **Duplicates (year, month, lat, lon)**: 0
- **File Size**: 258.3 MB

### Available Targets
- increment_SSM_DA_NoCDF (Missing: 0)
- increment_SSM_DA_CDF (Missing: 0)
- delta_increment_NoCDF_minus_CDF_SSM (Missing: 0)
- increment_RZSM_DA_NoCDF (Missing: 0)
- increment_RZSM_DA_CDF (Missing: 0)
- delta_increment_NoCDF_minus_CDF_RZSM (Missing: 0)
- delta_NoCDF_minus_CDF_SSM (Missing: 0)
- delta_DA_NoCDF_minus_OPL_RZSM (Missing: 0)
- delta_DA_CDF_minus_OPL_RZSM (Missing: 0)
- delta_DA_NoCDF_minus_OPL_ET (Missing: 0)
- delta_DA_CDF_minus_OPL_ET (Missing: 0)
- delta_DA_NoCDF_minus_OPL_runoff (Missing: 0)
- delta_DA_NoCDF_minus_OPL_baseflow (Missing: 0)

## B. Target Statistics
| Target | Min | Max | Mean | Std |
|---|---|---|---|---|
| increment_SSM_DA_NoCDF | -0.8347 | 0.8333 | -0.0294 | 0.0963 |
| increment_SSM_DA_CDF | -0.9093 | 0.4582 | -0.0183 | 0.0693 |
| delta_increment_NoCDF_minus_CDF_SSM | -0.8347 | 1.1568 | -0.0111 | 0.1060 |
| increment_RZSM_DA_NoCDF | -0.6899 | 0.6635 | -0.0072 | 0.0258 |
| increment_RZSM_DA_CDF | -0.7459 | 0.1235 | -0.0045 | 0.0179 |
| delta_increment_NoCDF_minus_CDF_RZSM | -0.6899 | 0.7156 | -0.0027 | 0.0291 |
| delta_NoCDF_minus_CDF_SSM | -0.1911 | 0.2146 | -0.0073 | 0.0286 |
| delta_DA_NoCDF_minus_OPL_RZSM | -0.2171 | 0.1710 | -0.0152 | 0.0274 |
| delta_DA_CDF_minus_OPL_RZSM | -0.2255 | 0.1011 | -0.0088 | 0.0208 |
| delta_DA_NoCDF_minus_OPL_ET | -96.6497 | 117.0223 | -1.3960 | 10.6716 |
| delta_DA_CDF_minus_OPL_ET | -100.6835 | 48.0892 | 1.3316 | 8.7536 |
| delta_DA_NoCDF_minus_OPL_runoff | -13.5415 | 66.5796 | 0.0825 | 0.9812 |
| delta_DA_NoCDF_minus_OPL_baseflow | -58.0544 | 254.5277 | 0.8985 | 6.8712 |

## C. Orders of Magnitude Check
- **Soil Moisture Realistic (0-0.6)**: 100.0% of values
- **ET Positive**: 100.0% of values
- **Rainf Positive**: 100.0% of values
- **Runoff Non-Negative**: 100.0% of values

## D. Increments Check
- **Mean Abs Amplitude (NoCDF)**: 0.06343
- **Mean Abs Amplitude (CDF)**: 0.02524
- **Ratio NoCDF/CDF**: 2.5

## E. RF Outputs Check
- **rf_metrics.csv**: Exists
- **rf_feature_importance.csv**: Exists
- **.joblib models saved**: 14
- **.png figures saved**: 4

## Recommendations
- Validation technique réussie. Le dataset est prêt pour l'interprétation scientifique, ou pour générer la version V1 avec les stations in situ.
