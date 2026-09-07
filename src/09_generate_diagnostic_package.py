import pandas as pd
import numpy as np
import os
import shutil

def main():
    print("Gathering data for scientific diagnostic package...")
    
    # 1. Load data
    df = pd.read_parquet("data/processed/monthly_pixel_dataset_2016_2020_static.parquet")
    metrics_v01 = pd.read_csv("outputs/tables/rf_metrics_v01_static.csv")
    metrics_v02 = pd.read_csv("outputs/tables/rf_metrics_v02_spatial_cv.csv")
    perm_v01 = pd.read_csv("outputs/tables/rf_permutation_importance_v01_static.csv")
    perm_v02 = pd.read_csv("outputs/tables/rf_permutation_importance_v02_spatial_cv.csv")
    
    # Dataset stats
    n_rows = len(df)
    n_cols = len(df.columns)
    months = df[['year', 'month']].drop_duplicates()
    n_months = len(months)
    pixels_per_month = df.groupby(['year', 'month']).size().mean()
    
    # Stats functions
    def get_stats(col):
        try:
            s = df[col]
            return {"min": s.min(), "max": s.max(), "mean": s.mean(), "std": s.std()}
        except KeyError:
            return {"min": np.nan, "max": np.nan, "mean": np.nan, "std": np.nan}
        
    inc_stats = {
        'increment_SSM_DA_NoCDF': get_stats('increment_SSM_DA_NoCDF'),
        'increment_SSM_DA_CDF': get_stats('increment_SSM_DA_CDF'),
        'delta_increment_NoCDF_minus_CDF_SSM': get_stats('delta_increment_NoCDF_minus_CDF_SSM'),
        'increment_RZSM_DA_NoCDF': get_stats('increment_RZSM_DA_NoCDF'),
        'increment_RZSM_DA_CDF': get_stats('increment_RZSM_DA_CDF'),
        'delta_increment_NoCDF_minus_CDF_RZSM': get_stats('delta_increment_NoCDF_minus_CDF_RZSM')
    }
    
    hydro_stats = {
        'delta_DA_NoCDF_minus_OPL_RZSM': get_stats('delta_DA_NoCDF_minus_OPL_RZSM'),
        'delta_DA_CDF_minus_OPL_RZSM': get_stats('delta_DA_CDF_minus_OPL_RZSM'),
        'delta_DA_NoCDF_minus_OPL_ET': get_stats('delta_DA_NoCDF_minus_OPL_ET'),
        'delta_DA_CDF_minus_OPL_ET': get_stats('delta_DA_CDF_minus_OPL_ET'),
        'delta_DA_NoCDF_minus_OPL_runoff': get_stats('delta_DA_NoCDF_minus_OPL_runoff'),
        'delta_DA_CDF_minus_OPL_runoff': get_stats('delta_DA_CDF_minus_OPL_runoff'),
        'delta_DA_NoCDF_minus_OPL_baseflow': get_stats('delta_DA_NoCDF_minus_OPL_baseflow'),
        'delta_DA_CDF_minus_OPL_baseflow': get_stats('delta_DA_CDF_minus_OPL_baseflow')
    }
    
    # Generate Markdown
    md = []
    md.append("# Scientific Diagnostics Interpretation Package (V0.2)")
    md.append("\n## 1. Objectif général des diagnostics V0.2")
    md.append("Ce document de synthèse a pour but d'analyser la manière dont les incréments SMAP se distribuent spatialement et temporellement, et comment les configurations d'assimilation (DA-NoCDF vs DA-CDF) diffèrent.")
    md.append("L'analyse diagnostique (Random Forest & XAI) évalue statistiquement la propagation de ces corrections vers la RZSM, l'évapotranspiration (ET), le ruissellement (runoff) et le flux de base (baseflow). L'objectif est d'identifier quels facteurs (états initiaux, flux, forçages, propriétés de surface) **are associated with** ou **diagnostic of** ces réponses.")
    md.append("L'ajout des variables statiques (`land_cover`, `soil_texture`, `elevation`, `irrigation_fraction`) permet de vérifier si ces réponses sont **spatially coherent with** l'hétérogénéité du terrain. La validation spatiale (V0.2) teste si ces relations se maintiennent sur des zones non vues, ce qui **suggests** une robustesse physique plutôt qu'une simple mémorisation de coordonnées.")
    md.append("Il est impératif d'utiliser un langage prudent : l'analyse identifie des cohérences diagnostiques et des biais systématiques, mais ne prouve pas de liens de causalité stricts ou de corrections d'irrigation directes.")
    
    md.append("\n## 2. Inventaire complet des fichiers produits")
    md.append("### A. Dataset")
    md.append("- `data/processed/monthly_pixel_dataset_2016_2020.parquet` (Base)")
    md.append("- `data/processed/monthly_pixel_dataset_2016_2020_static.parquet` (V0.1/V0.2 Final)")
    md.append("### B. Tables")
    md.append("- `outputs/tables/rf_metrics.csv` (V0)")
    md.append("- `outputs/tables/rf_metrics_v01_static.csv` (V0.1)")
    md.append("- `outputs/tables/rf_metrics_v02_spatial_cv.csv` (V0.2)")
    md.append("- `outputs/tables/rf_permutation_importance_v01_static.csv` (V0.1)")
    md.append("- `outputs/tables/rf_permutation_importance_v02_spatial_cv.csv` (V0.2)")
    md.append("### C. Reports")
    md.append("- `reports/rf_v01_static_results_summary.md`")
    md.append("- `reports/rf_v02_spatial_validation_summary.md`")
    md.append("- `reports/final_v02_deliverables_for_paper.md`")
    md.append("- `reports/random_forest_xai_method_summary.md`")
    md.append("- `reports/insitu_precip_inventory.md`")
    md.append("### D. Figures")
    md.append("- `outputs/figures/rf_model_skill_v02_spatial_cv.png` : Montre la corrélation prédiction vs observation des incréments (question: Le RF arrive-t-il à prédire les impacts spatiaux ?). Limite : dispersion résiduelle importante.")
    md.append("- `outputs/figures/rf_feature_importance_v02_spatial_cv.png` : Classement global des variables (question: Quels sont les top drivers ?). Limite : ignore les corrélations inter-prédicteurs.")
    md.append("- `outputs/figures/rf_temporal_vs_spatial_cv_v02.png` : Compare R2 Temporel 2020 vs Spatial CV (question: Les relations sont-elles géographiquement robustes ?). Limite : le spatial mask dépend du qcut.")
    md.append("- `outputs/figures/rf_grouped_feature_importance_v02.png` : Agrégation des importances par familles physiques (question: Quel compartiment du modèle est dominant ?).")
    
    md.append("\n## 3. Résumé du dataset utilisé")
    md.append(f"- **Période** : 2016–2020")
    md.append(f"- **Nombre de mois** : {n_months}")
    md.append(f"- **Pixels valides/mois** : ~{pixels_per_month:.0f}")
    md.append(f"- **Total lignes** : {n_rows}")
    md.append(f"- **Total colonnes** : {n_cols}")
    md.append("- **Statut de la pluie in situ (V1)** : Bloqué (stations s'arrêtent en 2014, pas de recouvrement avec SMAP).")
    
    md.append("\n## 4. Résumé des targets")
    md.append("- `increment_SSM_DA_NoCDF` : Incrément absolu de surface. Positif = SMAP ajoute de l'eau. Négatif = SMAP retire de l'eau. Prudence: inclut les biais saisonniers.")
    md.append("- `delta_increment_NoCDF_minus_CDF_SSM` : Différence de correction avec/sans correction de biais (CDF). Isole l'effet de la climatologie locale vs la dynamique absolue.")
    md.append("- `delta_DA_NoCDF_minus_OPL_RZSM/ET/runoff/baseflow` : Impact net de l'assimilation sur la réponse hydrologique (modèle DA - modèle Open-Loop). Positif = la DA a augmenté le flux/état. Négatif = réduction.")
    
    md.append("\n## 5. Résultats descriptifs des incréments SMAP")
    md.append("| Target | Min | Max | Mean | Std |")
    md.append("|---|---|---|---|---|")
    for k, v in inc_stats.items():
        md.append(f"| {k} | {v['min']:.4f} | {v['max']:.4f} | {v['mean']:.4f} | {v['std']:.4f} |")
    md.append("\n**Discussion** : La différence NoCDF/CDF nous apprend que la correction de biais (CDF) écrase une partie des signaux de basse fréquence (biais structurels du forçage/modèle). L'analyse diagnostique sur NoCDF permet d'identifier ces biais systématiques (souvent liés à la végétation ou l'irrigation ignorée par l'OPL).")
    
    md.append("\n## 6. Résultats hydrologiques")
    md.append("| Target | Min | Max | Mean | Std |")
    md.append("|---|---|---|---|---|")
    for k, v in hydro_stats.items():
        md.append(f"| {k} | {v['min']:.4f} | {v['max']:.4f} | {v['mean']:.4f} | {v['std']:.4f} |")
    md.append("\n**Discussion** : L'ET et la RZSM réagissent fortement, avec une grande variance. Les flux lents (baseflow) réagissent avec des amplitudes minimes, montrant l'inertie du système. La propagation surface → root zone → ET est directe.")
    
    md.append("\n## 7. Résumé RF V0 (Sans statiques)")
    md.append("Le RF V0 utilisait uniquement l'état initial (SSM_OPL, RZSM_OPL...) et les flux pour prédire les incréments. **Message principal** : L'état initial du modèle limite mathématiquement les incréments (ex: un sol déjà saturé limite les incréments positifs). Ce signal 'interne' domine.")
    
    md.append("\n## 8. Résumé RF V0.1 avec variables statiques")
    md.append("L'ajout de `land_cover`, `soil_texture`, `elevation` a significativement augmenté les scores, notamment pour l'ET et le baseflow. Cela indique que les incréments SMAP compensent des déficits du modèle liés à des hétérogénéités de surface sous-résolues.")
    
    md.append("\n## 9. Résumé V0.2 validation spatiale")
    md.append("Méthode : 25 blocs spatiaux, 5-Fold GroupKFold.")
    md.append("Le Spatial CV évalue le transfert vers des zones non vues (généralisation physique), tandis que le Temporal Split évalue le transfert vers une année non vue (2020). Les deux diagnostics sont complémentaires.")
    
    targets_prio = [
        "delta_increment_NoCDF_minus_CDF_SSM",
        "increment_SSM_DA_NoCDF",
        "delta_DA_NoCDF_minus_OPL_RZSM",
        "delta_DA_NoCDF_minus_OPL_ET",
        "delta_DA_NoCDF_minus_OPL_baseflow"
    ]
    md.append("| target | R2_temporal | R2_spatial_CV | Pearson_temporal | Pearson_spatial_CV | interpretation |")
    md.append("|---|---|---|---|---|---|")
    for t in targets_prio:
        try:
            r2_t = metrics_v01[metrics_v01['Target']==t]['R2'].values[0]
            r2_s = metrics_v02[metrics_v02['Target']==t]['R2'].values[0]
            p_t = metrics_v01[metrics_v01['Target']==t]['Pearson'].values[0]
            p_s = metrics_v02[metrics_v02['Target']==t]['Pearson'].values[0]
            note = "Spatial >= Temporal" if r2_s >= r2_t else "Temporal > Spatial"
            md.append(f"| {t} | {r2_t:.3f} | {r2_s:.3f} | {p_t:.3f} | {p_s:.3f} | {note} |")
        except: pass
    
    md.append("\n## 10. Top predictors robustes")
    for t in targets_prio:
        try:
            top_t = set(perm_v01[perm_v01['Target']==t].nlargest(10, 'Importance')['Predictor'])
            top_s = set(perm_v02[perm_v02['Target']==t].nlargest(10, 'Importance')['Predictor'])
            robust = top_t.intersection(top_s)
            disapp = top_t - top_s
            app = top_s - top_t
            md.append(f"### {t}")
            md.append(f"- **Top 10 temporal** : {', '.join(top_t)}")
            md.append(f"- **Top 10 spatial** : {', '.join(top_s)}")
            md.append(f"- **Communs (robustes)** : {', '.join(robust)}")
            md.append(f"- **Disparaissent en spatial** : {', '.join(disapp) if disapp else 'Aucun'}")
            md.append(f"- **Apparaissent seulement en spatial** : {', '.join(app) if app else 'Aucun'}")
        except: pass
    
    md.append("\n## 11. Importance groupée par famille")
    groups = {
        "model_initial_state": ["SSM_OPL", "RZSM_OPL", "SMC_L1_OPL", "SMC_L2_OPL", "SMC_L3_OPL", "SMC_L4_OPL"],
        "hydrological_fluxes_OPL": ["Evap_tavg_OPL", "Qs_tavg_OPL", "Qsb_tavg_OPL"],
        "meteorological_forcing": ["precipitation_model"],
        "static_surface": ["land_cover", "soil_texture", "elevation", "irrigation_fraction", "soil_texture_dominant_fraction", "land_cover_dominant_fraction"],
        "seasonality": ["month", "season"]
    }
    def get_group(p):
        for g, preds in groups.items():
            if p in preds: return g
        return "other"
    
    perm_v02['Group'] = perm_v02['Predictor'].apply(get_group)
    grouped_imp = perm_v02.groupby(['Target', 'Group'])['Importance'].sum().reset_index()
    
    for t in targets_prio:
        md.append(f"### {t}")
        g_df = grouped_imp[grouped_imp['Target']==t].sort_values(by='Importance', ascending=False)
        for _, row in g_df.iterrows():
            md.append(f"- {row['Group']} : {row['Importance']:.4f}")
            
    md.append("\n**Discussion** : L'assimilation est principalement contrainte par l'état initial du modèle (mémoire intrinsèque de l'humidité du sol). Cependant, la réponse des flux (ET, baseflow) est lourdement associée aux propriétés statiques (static_surface) et aux flux OPL. Cela souligne le rôle de modérateur du land cover et du sol.")

    md.append("\n## 12. Message scientifique principal du diagnostic")
    md.append("### A. Message court (2-3 phrases)")
    md.append("Les diagnostics RF/XAI révèlent que les incréments SMAP et leurs réponses hydrologiques ne sont pas aléatoires. Ils sont associés de manière robuste à l'état initial du sol, aux flux préexistants et aux propriétés statiques de surface (land cover, soil texture), ce qui démontre une généralisation cohérente à l'échelle régionale (Spatial CV).")
    md.append("### B. Pour l'Introduction / Discussion")
    md.append("L'utilisation conjointe de validations temporelles et spatiales suggère que les ajustements d'assimilation compensent des limites structurelles du modèle liées à la représentation du land cover. Le maintien des scores prédictifs sur des domaines non vus renforce l'utilité des approches XAI comme outils de diagnostic physique.")
    md.append("### C. Pour la Conclusion")
    md.append("L'assimilation SMAP interagit fortement avec la mémoire du sol et les propriétés de surface locales. Bien que la correction directe de l'irrigation ne soit pas causalement prouvée, la cohérence spatiale des relations diagnostiquées souligne la nécessité d'intégrer de meilleures paramétrisations de surface dans les modèles hydrologiques régionaux.")
    
    md.append("\n## 13. Limites à discuter")
    md.append("- L'absence d'erreurs de précipitation basées sur des jauges (gauge-based precipitation_error) pour 2016–2020 empêche d'évaluer l'impact des biais de forçage.")
    md.append("- L'absence de routage avancé (HyMAP) dans la configuration OPL.")
    md.append("- Les modèles RF identifient des corrélations (associations), non une stricte causalité physique.")
    md.append("- L'échelle des variables statiques (~5km) peut masquer la fine hétérogénéité des parcelles irriguées.")
    md.append("- Les flux lents profonds (baseflow) s'avèrent difficiles à généraliser géographiquement (scores négatifs en Spatial CV).")
    
    md.append("\n## 14. Figures recommandées pour le papier")
    md.append("- **Main Paper** : `rf_grouped_feature_importance_v02.png` (Titre: *Cumulative Feature Importance by Hydrological Group*). Message: Met en évidence le rôle central des propriétés de surface dans la modulation des incréments (Section Discussion).")
    md.append("- **Main Paper** : `rf_temporal_vs_spatial_cv_v02.png` (Titre: *Model Generalization: Temporal vs. Spatial Cross-Validation*). Message: Démontre la robustesse géographique des relations diagnostiquées (Section Validation).")
    md.append("- **Supplement** : `rf_model_skill_v02_spatial_cv.png` (Titre: *Scatter Plots of RF Predictions*).")
    md.append("- **Supplement** : `rf_feature_importance_v02_spatial_cv.png` (Titre: *Top Individual Predictors*).")
    
    md.append("\n## 15. Discussion-ready bullets")
    md.append("- **CDF vs NoCDF** : L'assimilation NoCDF permet au SMAP d'introduire sa propre climatologie, exposant les biais structurels de l'OPL, tandis que le CDF les masque.")
    md.append("- **Propagation verticale** : La forte association avec `RZSM_OPL` montre que l'incrément de surface dépend de la saturation sous-jacente.")
    md.append("- **Réponse ET** : Fortement associée à l'évapotranspiration OPL et au `land_cover`, l'ET est très sensible à la correction de la couche superficielle.")
    md.append("- **Réponse runoff/baseflow** : La réponse est amortie; le baseflow peine à se généraliser spatialement, soulignant des limites de routage.")
    md.append("- **Rôle land_cover/soil_texture** : Leur résilience en Spatial CV suggère que le modèle OPL sous-estime systématiquement la capacité de rétention de certains sols et végétations.")
    md.append("- **Rôle limité de precipitation_model** : Sans l'erreur par rapport aux jauges, la précipitation modèle seule n'explique qu'une fraction de l'incrément.")
    md.append("- **Limites in-situ** : L'évaluation fine du forçage requerra des campagnes de terrain sur la période 2016-2020.")
    md.append("- **Future work** : Implémenter le routage HyMAP et des simulations explicites d'irrigation pour confirmer l'origine des biais.")

    with open("reports/v02_scientific_diagnostics_interpretation_package.md", "w") as f:
        f.write("\n".join(md))
        
    print("Markdown generated.")
    
    # Copy figures
    print("Copying figures to reports/v02_figures_to_review/")
    out_dir = "reports/v02_figures_to_review"
    os.makedirs(out_dir, exist_ok=True)
    
    src_dir = "outputs/figures"
    fig_files = [f for f in os.listdir(src_dir) if f.endswith('.png')]
    for f in fig_files:
        shutil.copy(os.path.join(src_dir, f), os.path.join(out_dir, f))
        
    # Zip the folder
    print("Creating archive...")
    shutil.make_archive(out_dir, 'zip', out_dir)
    print("Process complete.")

if __name__ == '__main__':
    main()
