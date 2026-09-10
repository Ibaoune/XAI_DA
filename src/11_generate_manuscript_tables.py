import pandas as pd
import numpy as np
import os

def generate_tables():
    print("Generating manuscript-ready tables...")
    os.makedirs("outputs/tables", exist_ok=True)
    
    # --- Table 1: RF Target Definitions ---
    targets_def = [
        {
            "Readable Target Name": "SSM Increment",
            "Raw Column Name": "increment_SSM_DA_NoCDF",
            "Physical Meaning": "Absolute surface water added/removed by EnKF per month",
            "Formula": "DA_NoCDF_incr",
            "Units": "m³/m³",
            "Interpretation of Positive Values": "Assimilation adds moisture",
            "Drought-Propagation Relevance": "Initial surface correction"
        },
        {
            "Readable Target Name": "NoCDF-CDF Incr Contrast",
            "Raw Column Name": "delta_increment_NoCDF_minus_CDF_SSM",
            "Physical Meaning": "Contrast between biased and unbiased assimilation",
            "Formula": "increment_SSM_DA_NoCDF - increment_SSM_DA_CDF",
            "Units": "m³/m³",
            "Interpretation of Positive Values": "CDF suppresses positive increments",
            "Drought-Propagation Relevance": "Isolates bias correction effect"
        },
        {
            "Readable Target Name": "Δ RZSM",
            "Raw Column Name": "delta_DA_NoCDF_minus_OPL_RZSM",
            "Physical Meaning": "Impact of assimilation on deep root-zone moisture",
            "Formula": "RZSM_DA_NoCDF - RZSM_OPL",
            "Units": "m³/m³",
            "Interpretation of Positive Values": "Assimilation wets deep soil",
            "Drought-Propagation Relevance": "Memory propagation"
        },
        {
            "Readable Target Name": "Δ ET",
            "Raw Column Name": "delta_DA_NoCDF_minus_OPL_ET",
            "Physical Meaning": "Impact of assimilation on evapotranspiration",
            "Formula": "ET_DA_NoCDF - ET_OPL",
            "Units": "mm/day",
            "Interpretation of Positive Values": "Assimilation increases water flux",
            "Drought-Propagation Relevance": "Atmospheric feedback"
        },
        {
            "Readable Target Name": "Δ Baseflow",
            "Raw Column Name": "delta_DA_NoCDF_minus_OPL_baseflow",
            "Physical Meaning": "Impact of assimilation on subsurface drainage",
            "Formula": "Qsb_DA_NoCDF - Qsb_OPL",
            "Units": "mm/day",
            "Interpretation of Positive Values": "Assimilation increases baseflow",
            "Drought-Propagation Relevance": "Hydrological extreme modulation"
        }
    ]
    
    pd.DataFrame(targets_def).to_csv("outputs/tables/manuscript_rf_target_definitions.csv", index=False)
    
    # --- Table 2: RF Performance Summary ---
    temp_path = "outputs/tables/model_comparison_temporal.csv"
    spat_path = "outputs/tables/model_comparison_spatial_cv.csv"
    
    if os.path.exists(temp_path) and os.path.exists(spat_path):
        temp_df = pd.read_csv(temp_path)
        spat_df = pd.read_csv(spat_path)
        
        summary_rows = []
        for t in [d["Raw Column Name"] for d in targets_def]:
            # RF Temporal
            rf_temp = temp_df[(temp_df['Model'] == 'RF') & (temp_df['Target'] == t)]
            if rf_temp.empty: continue
            rf_t_r2 = rf_temp['R2'].values[0]
            rf_t_p = rf_temp['Pearson'].values[0]
            
            # RF Spatial
            rf_spat = spat_df[(spat_df['Model'] == 'RF') & (spat_df['Target'] == t)]
            rf_s_r2_m = rf_spat['R2_mean'].values[0]
            rf_s_r2_s = rf_spat['R2_std'].values[0]
            rf_s_p_m = rf_spat['Pearson_mean'].values[0]
            rf_s_p_s = rf_spat['Pearson_std'].values[0]
            
            # Baselines Spatial
            base_spat = spat_df[(spat_df['Model'] != 'RF') & (spat_df['Target'] == t)]
            best_base_r2 = base_spat['R2_mean'].max()
            
            if rf_s_r2_m > 0.3: interpretation = "Robustly predictable"
            elif rf_s_r2_m > 0.1: interpretation = "Moderately predictable"
            elif rf_s_r2_m > 0: interpretation = "Weakly predictable"
            else: interpretation = "Not spatially generalizable"
            
            summary_rows.append({
                "Target": t,
                "RF Temporal R2": f"{rf_t_r2:.3f}",
                "RF Temporal Pearson r": f"{rf_t_p:.3f}",
                "RF Spatial-CV R2": f"{rf_s_r2_m:.3f} ± {rf_s_r2_s:.3f}",
                "RF Spatial-CV Pearson r": f"{rf_s_p_m:.3f} ± {rf_s_p_s:.3f}",
                "Best Baseline Spatial-CV R2": f"{best_base_r2:.3f}",
                "Interpretation": interpretation
            })
            
        pd.DataFrame(summary_rows).to_csv("outputs/tables/manuscript_rf_performance_summary.csv", index=False)
    
    print("Tables generated successfully.")

if __name__ == "__main__":
    generate_tables()
