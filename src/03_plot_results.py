import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_results():
    print("--- Starting Plotting Results (03_plot_results.py) ---")
    
    out_dir = "outputs/figures"
    os.makedirs(out_dir, exist_ok=True)
    
    # Target ordering and mapping
    target_order = [
        "increment_SSM_DA_NoCDF",
        "delta_increment_NoCDF_minus_CDF_SSM",
        "delta_DA_NoCDF_minus_OPL_RZSM",
        "delta_DA_NoCDF_minus_OPL_ET",
        "delta_DA_NoCDF_minus_OPL_baseflow"
    ]
    
    readable_names = {
        "increment_SSM_DA_NoCDF": "SSM Increment",
        "delta_increment_NoCDF_minus_CDF_SSM": "NoCDF-CDF Incr Contrast",
        "delta_DA_NoCDF_minus_OPL_RZSM": "Δ RZSM",
        "delta_DA_NoCDF_minus_OPL_ET": "Δ ET",
        "delta_DA_NoCDF_minus_OPL_baseflow": "Δ Baseflow"
    }

    # 1. Figure A: RF predictive skill with baselines
    print("Generating Figure A: Predictive skill with baselines...")
    temp_df_path = "outputs/tables/model_comparison_temporal.csv"
    spat_df_path = "outputs/tables/model_comparison_spatial_cv.csv"
    
    if os.path.exists(temp_df_path) and os.path.exists(spat_df_path):
        temp_df = pd.read_csv(temp_df_path)
        spat_df = pd.read_csv(spat_df_path)
        
        # Filter to priority targets and order them
        temp_df = temp_df[temp_df['Target'].isin(target_order)].copy()
        spat_df = spat_df[spat_df['Target'].isin(target_order)].copy()
        
        temp_df['Target_Name'] = temp_df['Target'].map(readable_names)
        spat_df['Target_Name'] = spat_df['Target'].map(readable_names)
        
        # Sort categorical
        temp_df['Target_Name'] = pd.Categorical(temp_df['Target_Name'], categories=[readable_names[t] for t in target_order], ordered=True)
        spat_df['Target_Name'] = pd.Categorical(spat_df['Target_Name'], categories=[readable_names[t] for t in target_order], ordered=True)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=True)
        
        # Panel 1: Temporal
        sns.barplot(data=temp_df, x='Target_Name', y='R2', hue='Model', ax=axes[0], palette='Set2')
        axes[0].set_title("(a) Temporal Holdout Validation (Test 2020)", fontsize=14)
        axes[0].set_ylabel("R² Score", fontsize=12)
        axes[0].set_xlabel("")
        axes[0].axhline(0, color='black', linewidth=0.8)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Panel 2: Spatial
        # Seaborn barplot doesn't easily take pre-computed std for error bars with hue. 
        # We will use matplotlib manually or errorbar format.
        ax2 = axes[1]
        width = 0.25
        models = ['Dummy', 'Ridge', 'RF']
        colors = sns.color_palette('Set2', n_colors=3)
        
        for i, t in enumerate(target_order):
            for j, m in enumerate(models):
                row = spat_df[(spat_df['Target'] == t) & (spat_df['Model'] == m)]
                if not row.empty:
                    mean_val = row['R2_mean'].values[0]
                    std_val = row['R2_std'].values[0]
                    ax2.bar(i + (j - 1)*width, mean_val, width, color=colors[j], yerr=std_val, capsize=4, label=m if i==0 else "")
                    
        ax2.set_xticks(range(len(target_order)))
        ax2.set_xticklabels([readable_names[t] for t in target_order], rotation=45)
        ax2.set_title("(b) Spatial Block Cross-Validation (5-Fold)", fontsize=14)
        ax2.axhline(0, color='black', linewidth=0.8)
        ax2.legend()
        
        plt.suptitle("Predictive Skill: Random Forest vs Baselines", fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "q1_rf_model_skill_with_baselines.png"), dpi=300)
        plt.savefig(os.path.join(out_dir, "q1_rf_model_skill_with_baselines.pdf"))
        plt.close()
        
    # 2. Figure B: Grouped permutation importance
    print("Generating Figure B: Grouped permutation importance...")
    perm_df_path = "outputs/tables/rf_permutation_importance_all.csv"
    if os.path.exists(perm_df_path):
        perm_df = pd.read_csv(perm_df_path)
        
        # Filter only spatial fold importances
        perm_spat = perm_df[perm_df['Importance_Type'].str.contains("Permutation_Spatial_Fold")].copy()
        perm_spat = perm_spat[perm_spat['Target'].isin(target_order)]
        perm_spat['Fold'] = perm_spat['Importance_Type'].str.extract(r'Fold(\d+)').astype(int)
        
        # Group definitions
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
            
        perm_spat['Group'] = perm_spat['Predictor'].apply(get_group)
        
        # Sum importance by group per target per fold
        grouped = perm_spat.groupby(['Target', 'Fold', 'Group'])['Importance'].sum().reset_index()
        
        # Normalize within each target-fold so they sum to 1
        grouped['Total_Imp'] = grouped.groupby(['Target', 'Fold'])['Importance'].transform('sum')
        grouped['Norm_Imp'] = grouped['Importance'] / grouped['Total_Imp']
        
        # Calculate mean and std across folds
        final_imp = grouped.groupby(['Target', 'Group'])['Norm_Imp'].agg(['mean', 'std']).reset_index()
        
        final_imp['Target_Name'] = final_imp['Target'].map(readable_names)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # We will plot a stacked bar chart using the means.
        # Adding error bars to stacked charts is tricky, so we'll plot them grouped or use a nice format.
        # Let's use a grouped bar chart for clearer uncertainty visualization.
        
        sns.barplot(data=final_imp, x='Target_Name', y='mean', hue='Group', 
                    order=[readable_names[t] for t in target_order], palette='Set1', ax=ax)
        
        # Add error bars manually
        # Seaborn places bars at specific x offsets
        num_groups = len(final_imp['Group'].unique())
        width = 0.8 / num_groups
        offsets = np.linspace(-0.4 + width/2, 0.4 - width/2, num_groups)
        
        group_order = final_imp['Group'].unique()
        for i, t in enumerate(target_order):
            for j, g in enumerate(group_order):
                row = final_imp[(final_imp['Target'] == t) & (final_imp['Group'] == g)]
                if not row.empty:
                    ax.errorbar(i + offsets[j], row['mean'].values[0], yerr=row['std'].values[0], 
                                color='black', capsize=3, fmt='none')
                                
        ax.set_title("Grouped Permutation Importance (Normalized, Spatial CV)", fontsize=16)
        ax.set_ylabel("Normalized Importance Fraction", fontsize=12)
        ax.set_xlabel("")
        ax.set_xticklabels([readable_names[t] for t in target_order], rotation=45, fontsize=11)
        
        # Annotate Baseflow limitation
        ax.annotate("⚠️ Not Spatially Robust", 
                    xy=(4, 0.8), xytext=(4, 0.9),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                    ha='center', fontsize=11, color='red', weight='bold')

        plt.legend(title="Predictor Family", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "q1_grouped_permutation_importance.png"), dpi=300)
        plt.savefig(os.path.join(out_dir, "q1_grouped_permutation_importance.pdf"))
        plt.close()

    print("Plotting complete.")

if __name__ == "__main__":
    plot_results()
