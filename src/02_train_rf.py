import os
import sys
import yaml
import argparse
import pandas as pd
import numpy as np
import traceback

if not hasattr(np, 'float'): np.float = float
if not hasattr(np, 'bool'): np.bool = bool
if not hasattr(np, 'int'): np.int = int
if not hasattr(np, 'object'): np.object = object

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupKFold
from scipy.stats import pearsonr

def train_models():
    """
    Trains Random Forest, Ridge Regression, and Dummy Regressors.
    Evaluates them using temporal holdout and spatial block cross-validation.
    """
    print("--- Starting Model Training (02_train_rf.py) ---")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default=None, help="Override run_mode from config")
    parser.add_argument("--dataset", default="v0", help="Dataset version to use (e.g., static)")
    parser.add_argument("--cv", default="spatial", help="Validation mode: temporal or spatial")
    parser.add_argument("--mini-test", action="store_true", help="Run a quick test on a 50k sample")
    args = parser.parse_args()
    
    config_path = "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    paths = config.get("paths", {})
    options = config.get("options", {})
    random_state = options.get("random_state", 42)
    
    input_dataset = paths.get("output_dataset", "data/processed/monthly_pixel_dataset_2016_2020.parquet")
    output_models_dir = paths.get("output_models_dir", "outputs/models")
    
    if args.dataset == "static":
        input_dataset = "data/processed/monthly_pixel_dataset_2016_2020_static.parquet"
        
    run_mode = args.mode if args.mode else options.get("run_mode", "real_data")
    
    if args.mini_test and args.dataset == "static":
        test_static = "data/processed/monthly_pixel_dataset_test_static.parquet"
        if os.path.exists(test_static):
            input_dataset = test_static
            
    if not os.path.exists(input_dataset):
        fallback = "data/processed/monthly_pixel_dataset.parquet"
        if args.dataset == "static":
            fallback = "data/processed/monthly_pixel_dataset_2016_2020_static.parquet"
        if os.path.exists(fallback):
            input_dataset = fallback
        else:
            print(f"Error: Dataset {input_dataset} not found.")
            return
            
    print(f"Loading dataset from {input_dataset}...")
    df = pd.read_parquet(input_dataset)
    
    if args.mini_test and len(df) > 50000:
        df = df.sample(n=50000, random_state=random_state)
        
    os.makedirs(output_models_dir, exist_ok=True)
    os.makedirs("outputs/tables", exist_ok=True)
    
    # 1. Setup Spatial Blocks
    # north_south and east_west are each cut into 5 quantiles.
    # This creates 5 * 5 = 25 distinct spatial blocks.
    if 'north_south' in df.columns and 'east_west' in df.columns:
        df['block_ns'] = pd.qcut(df['north_south'], 5, labels=False, duplicates='drop')
        df['block_ew'] = pd.qcut(df['east_west'], 5, labels=False, duplicates='drop')
        df['spatial_block'] = df['block_ns'].astype(str) + "_" + df['block_ew'].astype(str)
    else:
        print("Error: Spatial coords north_south and east_west not found.")
        return
        
    # Export spatial blocks diagnostic
    blocks_diag = df.groupby('spatial_block').agg(
        n_pixels=('lat', 'nunique'),
        n_samples=('lat', 'count'),
        ns_min=('north_south', 'min'),
        ns_max=('north_south', 'max'),
        ew_min=('east_west', 'min'),
        ew_max=('east_west', 'max')
    ).reset_index()
    
    # Assign folds identically to how GroupKFold does it to document it
    gkf = GroupKFold(n_splits=5)
    fold_assignments = {}
    for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(df, groups=df['spatial_block'])):
        test_blocks = df.iloc[test_idx]['spatial_block'].unique()
        for b in test_blocks:
            fold_assignments[b] = fold_idx + 1
            
    blocks_diag['fold_assignment'] = blocks_diag['spatial_block'].map(fold_assignments)
    blocks_diag.to_csv("outputs/tables/rf_spatial_cv_diagnostic_blocks.csv", index=False)
    print("Saved spatial blocks diagnostic table.")

    # 2. Setup Targets and Predictors
    priority_targets = [
        "increment_SSM_DA_NoCDF",
        "delta_increment_NoCDF_minus_CDF_SSM",
        "delta_DA_NoCDF_minus_OPL_RZSM",
        "delta_DA_NoCDF_minus_OPL_ET",
        "delta_DA_NoCDF_minus_OPL_baseflow",
        "delta_DA_NoCDF_minus_OPL_runoff",
        "delta_increment_NoCDF_minus_CDF_RZSM",
        "delta_DA_CDF_minus_OPL_ET",
        "delta_DA_CDF_minus_OPL_RZSM"
    ]
    
    potential_predictors = [
        "precipitation_model", "SSM_OPL", "RZSM_OPL", "Evap_tavg_OPL", "Qs_tavg_OPL", "Qsb_tavg_OPL",
        "SMC_L1_OPL", "SMC_L2_OPL", "SMC_L3_OPL", "SMC_L4_OPL",
        "month", "season", "elevation", "soil_texture", "land_cover", 
        "irrigation_fraction", "crop_type", "soil_texture_dominant_fraction", "land_cover_dominant_fraction",
        "basin_id"
    ]
    
    targets = [t for t in priority_targets if t in df.columns]
    predictors = [p for p in potential_predictors if p in df.columns]
    
    categorical_features = [f for f in ["land_cover", "soil_texture", "crop_type", "basin_id", "season"] if f in predictors]
    numerical_features = [f for f in predictors if f not in categorical_features]
    
    # 3. Pipelines
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()) # important for Ridge
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'
    )
    
    models = {
        'Dummy': DummyRegressor(strategy='mean'),
        'Ridge': Ridge(random_state=random_state),
        'RF': RandomForestRegressor(n_estimators=150 if not args.mini_test else 10, 
                                    max_features="sqrt", min_samples_leaf=5, 
                                    random_state=random_state, n_jobs=-1)
    }

    # Data structures for results
    spatial_fold_metrics = []
    spatial_summary = []
    temporal_summary = []
    perm_imp_list = []
    
    # Train/Test Split for Temporal
    train_years = options.get("train_years", [2016, 2017, 2018, 2019])
    test_years = options.get("test_years", [2020])
    
    if "year" in df.columns and not args.mini_test:
        train_df = df[df["year"].isin(train_years)]
        test_df = df[df["year"].isin(test_years)]
    else:
        train_df = df.sample(frac=0.8, random_state=random_state)
        test_df = df.drop(train_df.index)

    X_train_temp = train_df[predictors]
    X_test_temp = test_df[predictors]
    
    # Precompute processed features
    print("Preprocessing full dataset features...")
    X_full = df[predictors]
    
    for t in targets:
        print(f"\n========== Target: {t} ==========")
        y_full = df[t].fillna(0)
        y_train_temp = train_df[t].fillna(0)
        y_test_temp = test_df[t].fillna(0)
        
        # We need to process data inside the loop for each model pipeline
        for model_name, model in models.items():
            print(f"--- Model: {model_name} ---")
            pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
            
            # --- Temporal Holdout Validation ---
            pipeline.fit(X_train_temp, y_train_temp)
            preds_temp = pipeline.predict(X_test_temp)
            
            r2_t = r2_score(y_test_temp, preds_temp)
            rmse_t = np.sqrt(mean_squared_error(y_test_temp, preds_temp))
            mae_t = mean_absolute_error(y_test_temp, preds_temp)
            pearson_t, _ = pearsonr(y_test_temp, preds_temp) if len(y_test_temp) > 1 and np.std(preds_temp)>0 else (np.nan, np.nan)
            
            temporal_summary.append({
                "Model": model_name, "Target": t,
                "R2": r2_t, "Pearson": pearson_t, "RMSE": rmse_t, "MAE": mae_t
            })
            print(f"Temporal R2: {r2_t:.4f}, Pearson: {pearson_t:.4f}")

            # --- Permutation Importance (Only for RF) ---
            if model_name == 'RF':
                print(f"Calculating Permutation Importance (Temporal)...")
                perm_sample_size = min(len(X_test_temp), 10000)
                X_test_perm = X_test_temp.sample(n=perm_sample_size, random_state=random_state)
                y_test_perm = y_test_temp.loc[X_test_perm.index]
                
                perm_results = permutation_importance(pipeline, X_test_perm, y_test_perm, n_repeats=5, random_state=random_state, n_jobs=-1)
                for p, imp in zip(predictors, perm_results.importances_mean):
                    perm_imp_list.append({"Target": t, "Predictor": p, "Importance": imp, "Importance_Type": "Permutation_Temporal"})
                
                joblib.dump(pipeline, os.path.join(output_models_dir, f"rf_{t}_temporal.joblib"))

            # --- Spatial CV ---
            # 5 GroupKFold blocks. Full spatial blocks are excluded from training when used for testing.
            fold_r2, fold_pearson, fold_rmse, fold_mae = [], [], [], []
            groups = df['spatial_block']
            
            for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(X_full, y_full, groups=groups)):
                X_train_cv, X_test_cv = X_full.iloc[train_idx], X_full.iloc[test_idx]
                y_train_cv, y_test_cv = y_full.iloc[train_idx], y_full.iloc[test_idx]
                
                pipeline.fit(X_train_cv, y_train_cv)
                preds_cv = pipeline.predict(X_test_cv)
                
                r2 = r2_score(y_test_cv, preds_cv)
                rmse = np.sqrt(mean_squared_error(y_test_cv, preds_cv))
                mae = mean_absolute_error(y_test_cv, preds_cv)
                pearson, _ = pearsonr(y_test_cv, preds_cv) if len(y_test_cv) > 1 and np.std(preds_cv)>0 else (np.nan, np.nan)
                bias = np.mean(preds_cv - y_test_cv)
                
                fold_r2.append(r2)
                fold_pearson.append(pearson)
                fold_rmse.append(rmse)
                fold_mae.append(mae)
                
                if model_name == 'RF':
                    spatial_fold_metrics.append({
                        "Target": t, "Fold": fold_idx + 1, "R2": r2, "Pearson": pearson,
                        "RMSE": rmse, "MAE": mae, "Bias": bias, "N_Test": len(y_test_cv)
                    })

                    # Calculate permutation importance on spatial fold
                    perm_sample_size = min(len(X_test_cv), 5000)
                    X_test_perm = X_test_cv.sample(n=perm_sample_size, random_state=random_state)
                    y_test_perm = y_test_cv.loc[X_test_perm.index]
                    perm_results = permutation_importance(pipeline, X_test_perm, y_test_perm, n_repeats=3, random_state=random_state, n_jobs=-1)
                    
                    for p, imp in zip(predictors, perm_results.importances_mean):
                        perm_imp_list.append({"Target": t, "Predictor": p, "Importance": imp, "Importance_Type": f"Permutation_Spatial_Fold{fold_idx+1}"})
            
            spatial_summary.append({
                "Model": model_name, "Target": t,
                "R2_mean": np.mean(fold_r2), "R2_std": np.std(fold_r2),
                "Pearson_mean": np.mean(fold_pearson), "Pearson_std": np.std(fold_pearson),
                "RMSE_mean": np.mean(fold_rmse), "MAE_mean": np.mean(fold_mae)
            })
            print(f"Spatial R2: {np.mean(fold_r2):.4f} +/- {np.std(fold_r2):.4f}")

    # 4. Save Outputs
    pd.DataFrame(temporal_summary).to_csv("outputs/tables/model_comparison_temporal.csv", index=False)
    pd.DataFrame(spatial_summary).to_csv("outputs/tables/model_comparison_spatial_cv.csv", index=False)
    
    df_fold = pd.DataFrame(spatial_fold_metrics)
    df_fold.to_csv("outputs/tables/rf_spatial_cv_fold_metrics.csv", index=False)
    
    # Create the aggregated uncertainty table for RF only
    rf_spatial_summary = [s for s in spatial_summary if s["Model"] == "RF"]
    df_spatial_unc = pd.DataFrame(rf_spatial_summary)
    
    # Calculate mean bias across folds for RF
    bias_summary = df_fold.groupby("Target")["Bias"].mean().reset_index().rename(columns={"Bias": "Bias_mean"})
    df_spatial_unc = pd.merge(df_spatial_unc, bias_summary, on="Target", how="left")
    df_spatial_unc.to_csv("outputs/tables/rf_spatial_cv_summary_with_uncertainty.csv", index=False)
    
    # Save Feature Importance
    perm_df = pd.DataFrame(perm_imp_list)
    perm_df.to_csv("outputs/tables/rf_permutation_importance_all.csv", index=False)
    
    print("Training and evaluation completed successfully.")

if __name__ == "__main__":
    train_models()
