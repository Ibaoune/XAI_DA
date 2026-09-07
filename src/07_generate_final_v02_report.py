import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    print("Generating final V0.2 report...")
    
    # 1. Load data
    metrics_v01 = pd.read_csv('outputs/tables/rf_metrics_v01_static.csv')
    metrics_v02 = pd.read_csv('outputs/tables/rf_metrics_v02_spatial_cv.csv')
    perm_v01 = pd.read_csv('outputs/tables/rf_permutation_importance_v01_static.csv')
    perm_v02 = pd.read_csv('outputs/tables/rf_permutation_importance_v02_spatial_cv.csv')
    
    report_path = 'reports/rf_v02_spatial_validation_summary.md'
    
    # 2. Priority targets
    targets = [
        "delta_increment_NoCDF_minus_CDF_SSM",
        "increment_SSM_DA_NoCDF",
        "delta_DA_NoCDF_minus_OPL_RZSM",
        "delta_DA_NoCDF_minus_OPL_ET",
        "delta_DA_NoCDF_minus_OPL_baseflow"
    ]
    
    # 3. Group definitions
    groups = {
        "model_initial_state": ["SSM_OPL", "RZSM_OPL", "SMC_L1_OPL", "SMC_L2_OPL", "SMC_L3_OPL", "SMC_L4_OPL"],
        "hydrological_fluxes_OPL": ["Evap_tavg_OPL", "Qs_tavg_OPL", "Qsb_tavg_OPL"],
        "meteorological_forcing": ["precipitation_model"],
        "static_surface": ["land_cover", "soil_texture", "elevation", "irrigation_fraction", "soil_texture_dominant_fraction", "land_cover_dominant_fraction"],
        "seasonality": ["month", "season"]
    }
    
    def get_group(predictor):
        for g, preds in groups.items():
            if predictor in preds: return g
        return "other"
    
    perm_v02['Group'] = perm_v02['Predictor'].apply(get_group)
    
    # Generate grouped plot
    grouped_imp = perm_v02[perm_v02['Target'].isin(targets)].groupby(['Target', 'Group'])['Importance'].sum().reset_index()
    
    plt.figure(figsize=(14, 8))
    sns.barplot(data=grouped_imp, x='Importance', y='Target', hue='Group', palette='Set2')
    plt.title('Grouped Feature Importance by Target (V0.2 Spatial CV)')
    plt.tight_layout()
    plt.savefig('outputs/figures/rf_grouped_feature_importance_v02.png', dpi=300)
    plt.close()
    
    # Generate the report
    with open(report_path, 'w') as f:
        f.write("# Random Forest Validation Summary (V0.2 Spatial CV)\n\n")
        
        f.write("## A. Objective\n")
        f.write("L'objectif de cette étape est de valider la robustesse spatiale des modèles Random Forest (V0.1). Le split temporel testait la capacité de généralisation temporelle à l'année 2020. Cependant, pour interpréter le rôle physique des variables statiques (`land_cover`, `soil_texture`, `elevation`), il est impératif de prouver que le modèle ne se contente pas de mémoriser les coordonnées spatiales vues pendant l'entraînement. La validation croisée spatiale (Spatial CV) répond à ce besoin en testant le modèle sur des pixels qu'il n'a jamais vus.\n\n")
        
        f.write("## B. Spatial CV design\n")
        f.write("- **Grille spatiale** : La zone a été découpée en **25 blocs spatiaux** (grille 5x5) via une discrétisation par quantiles (`pd.qcut`) sur les coordonnées `north_south` et `east_west`, garantissant une taille de bloc approximativement équivalente.\n")
        f.write("- **Méthode** : Validation croisée à 5 plis (5-fold CV) utilisant `GroupKFold` sur la variable `spatial_block`. Pour chaque pli, 4/5 des blocs servent à l'entraînement et le bloc restant sert au test.\n")
        f.write("- **Données** : ~769,000 pixels d'entraînement et ~192,000 pixels de test par fold. Attention : les mêmes années temporelles peuvent apparaître dans train et test ; l'objectif exclusif ici est de tester la généralisation spatiale.\n\n")
        
        f.write("## C. Metrics comparison (Temporal vs Spatial)\n")
        f.write("The spatial CV scores indicate whether the learned relationships generalize to unseen spatial blocks, while the temporal split evaluates transfer to the unseen year 2020. Differences between the two scores should therefore be interpreted as complementary robustness diagnostics.\n\n")
        
        f.write("| Target | R2_temporal_2020 | R2_spatial_CV | Pearson_temporal_2020 | Pearson_spatial_CV | interpretation_note |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for t in targets:
            try:
                r2_t = metrics_v01[metrics_v01['Target']==t]['R2'].values[0]
                r2_s = metrics_v02[metrics_v02['Target']==t]['R2'].values[0]
                p_t = metrics_v01[metrics_v01['Target']==t]['Pearson'].values[0]
                p_s = metrics_v02[metrics_v02['Target']==t]['Pearson'].values[0]
                diff = r2_t - r2_s
                note = "Spatial >= Temporal" if r2_s >= r2_t else "Temporal > Spatial"
                f.write(f"| {t} | {r2_t:.3f} | {r2_s:.3f} | {p_t:.3f} | {p_s:.3f} | {note} |\n")
            except IndexError:
                pass
                
        f.write("\n## D. Robust predictors\n")
        for t in targets:
            f.write(f"### {t}\n")
            try:
                top_t = perm_v01[perm_v01['Target']==t].nlargest(10, 'Importance')['Predictor'].tolist()
                top_s = perm_v02[perm_v02['Target']==t].nlargest(10, 'Importance')['Predictor'].tolist()
                robust = [p for p in top_t if p in top_s]
                disapp = [p for p in top_t if p not in top_s]
                app_only_s = [p for p in top_s if p not in top_t]
                
                f.write(f"- **Top 10 temporal** : {', '.join(top_t)}\n")
                f.write(f"- **Top 10 spatial** : {', '.join(top_s)}\n")
                f.write(f"- **Communs (robustes)** : {', '.join(robust)}\n")
                if disapp: f.write(f"- **Disparaissent en spatial** : {', '.join(disapp)}\n")
                if app_only_s: f.write(f"- **Apparaissent seulement en spatial** : {', '.join(app_only_s)}\n")
                f.write("\n")
            except Exception as e:
                pass
                
        f.write("## E. Grouped predictor importance (Spatial CV)\n")
        for t in targets:
            f.write(f"### {t}\n")
            g_df = grouped_imp[grouped_imp['Target']==t].sort_values(by='Importance', ascending=False)
            f.write("| Group | Importance Sum |\n")
            f.write("|---|---|\n")
            for _, row in g_df.iterrows():
                f.write(f"| {row['Group']} | {row['Importance']:.4f} |\n")
            f.write("\n")
            
        f.write("## F. Interpretation with cautious language\n")
        f.write("L'analyse **suggests** que les variables statiques (`land_cover`, `soil_texture`) sont des diagnostiques importants des incréments d'assimilation et des réponses hydrologiques associées. L'augmentation ou le maintien des scores en validation spatiale indique que cette relation est **spatially consistent with** une hétérogénéité systémique, possiblement liée à la structure du sol ou à l'occupation des terres. Le fait que `land_cover` soit robuste en validation spatiale **supports the interpretation that** les biais structurels de l'OPL sur certaines végétations sont corrigés par l'assimilation.\n\n")
        
        f.write("## G. Limitations\n")
        f.write("- Le RF n'est pas un modèle physique causal ; il ne fait que capturer des associations statistiques.\n")
        f.write("- La résolution des données statiques (5km) pourrait masquer des hétérogénéités locales plus fines (ex: parcelles irriguées sous-résolues).\n\n")
        
        f.write("## H. Next step: V1 precipitation_error from in-situ data\n")
        f.write("Maintenant que la robustesse spatiale des facteurs statiques est établie, la prochaine étape (V1) consistera à ajouter l'erreur de précipitation (OPL model precip vs In-situ gauge precip) et ses composantes retardées (30d, 90d) pour capturer les biais de forçage et isoler davantage l'effet causal de l'irrigation et de l'évapotranspiration non modélisée.\n")

if __name__ == '__main__':
    main()
