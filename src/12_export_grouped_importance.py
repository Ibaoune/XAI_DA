import pandas as pd
import numpy as np

def generate_summary():
    # 1. Load data
    perm_df = pd.read_csv('outputs/tables/rf_permutation_importance_all.csv')
    perf_df = pd.read_csv('outputs/tables/rf_spatial_cv_summary_with_uncertainty.csv')
    
    # 2. Filter for spatial folds only
    perm_spat = perm_df[perm_df['Importance_Type'].str.contains('Permutation_Spatial_Fold')].copy()
    perm_spat['Fold'] = perm_spat['Importance_Type'].str.extract(r'Fold(\d+)').astype(int)
    
    # 3. Define groups
    groups = {
        "initial soil-water state": ["SSM_OPL", "RZSM_OPL", "SMC_L1_OPL", "SMC_L2_OPL", "SMC_L3_OPL", "SMC_L4_OPL"],
        "OPL hydrological fluxes": ["Evap_tavg_OPL", "Qs_tavg_OPL", "Qsb_tavg_OPL"],
        "meteorological forcing": ["precipitation_model"],
        "static surface properties": ["land_cover", "soil_texture", "elevation", "irrigation_fraction", "soil_texture_dominant_fraction", "land_cover_dominant_fraction", "crop_type", "basin_id"],
        "seasonality": ["month", "season"]
    }
    
    def get_group(p):
        for g, preds in groups.items():
            if p in preds: return g
        return "other"
        
    perm_spat['predictor_family'] = perm_spat['Predictor'].apply(get_group)
    
    # 4. Aggregate by target, fold, and predictor_family
    # Raw importance sum per group per fold
    fold_grouped = perm_spat.groupby(['Target', 'Fold', 'predictor_family'])['Importance'].sum().reset_index()
    
    # Calculate normalization within each target-fold
    fold_grouped['Total_Imp'] = fold_grouped.groupby(['Target', 'Fold'])['Importance'].transform('sum')
    fold_grouped['Norm_Imp'] = fold_grouped['Importance'] / fold_grouped['Total_Imp']
    
    # 5. Calculate means and stds across folds
    summary = fold_grouped.groupby(['Target', 'predictor_family']).agg(
        mean_importance=('Importance', 'mean'),
        std_importance_across_spatial_folds=('Importance', 'std'),
        normalized_mean_importance=('Norm_Imp', 'mean'),
        normalized_std_importance=('Norm_Imp', 'std')
    ).reset_index()
    
    # 6. Merge with performance metrics
    # Perf df has 'Target', 'R2_mean', 'R2_std' for Model == 'RF'
    perf_rf = perf_df[perf_df['Model'] == 'RF'][['Target', 'R2_mean', 'R2_std']]
    summary = summary.merge(perf_rf, on='Target', how='left')
    summary.rename(columns={'R2_mean': 'model_spatial_cv_R2_mean', 'R2_std': 'model_spatial_cv_R2_std'}, inplace=True)
    
    # 7. Add interpretation flag
    def interpret(r2):
        if pd.isna(r2): return 'unknown'
        if r2 > 0.3: return 'robust'
        if r2 > 0.1: return 'moderate'
        if r2 > 0: return 'weak'
        return 'not spatially robust'
        
    summary['interpretation_flag'] = summary['model_spatial_cv_R2_mean'].apply(interpret)
    
    # 8. Sort and save
    summary = summary.sort_values(by=['Target', 'normalized_mean_importance'], ascending=[True, False])
    output_path = 'outputs/tables/manuscript_grouped_permutation_importance_summary.csv'
    summary.to_csv(output_path, index=False)
    
    # 9. Print for specific targets
    targets_to_print = ['delta_DA_NoCDF_minus_OPL_RZSM', 'delta_DA_NoCDF_minus_OPL_ET']
    for t in targets_to_print:
        print(f"\\n--- Target: {t} ---")
        df_t = summary[summary['Target'] == t].copy()
        
        # format output
        for _, row in df_t.iterrows():
            print(f"Family: {row['predictor_family']:<28} | "
                  f"Norm Imp: {row['normalized_mean_importance']:.3f} ± {row['normalized_std_importance']:.3f} | "
                  f"R2: {row['model_spatial_cv_R2_mean']:.3f} ({row['interpretation_flag']})")

if __name__ == '__main__':
    generate_summary()
