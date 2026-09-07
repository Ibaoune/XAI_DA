# Sprint Cleanup 5: Duplicate Deletion Report

## A. Archive Créée
Une archive de sauvegarde a été créée avant toute suppression à la racine du projet IA :
`_ARCHIVE_BEFORE_Q1_DUPLICATE_CLEANUP_20260808/`

## B. Nombre de Fichiers Archivés
**32 fichiers** ont été sécurisés dans cette archive. Un fichier `manifest.txt` y répertorie les chemins originaux, les tailles, et les empreintes cryptographiques SHA256 pour prévenir toute perte de données accidentelle.

## C. Fichiers Supprimés
**32 fichiers** ont été supprimés des dossiers actifs (`outputs/` et `reports/`), incluant :
- Tous les anciens fichiers hydrologiques (figures et tableaux) ayant le préfixe `q1_`.
- Les rapports historiques (textes et zips) commençant par `q1_`.
- Les anciennes figures RF à la racine de `outputs/figures/` (telles que `rf_temporal_vs_spatial_cv_v02.png`), **uniquement** parce que leur copie `manuscript_*` avait été validée dans les sous-dossiers propres lors du Sprint 4.

## D. Fichiers Conservés
Ont été strictement préservés de la suppression :
- Le jeu de données clé de l'IA : `data/processed/monthly_pixel_dataset_2016_2020_static.parquet`.
- Tous les scripts du dossier `scratch/`.
- Le dossier `archive/`.
- Les scripts source `.py`.
- Toutes les nouvelles figures `manuscript_*` et les tableaux validés du côté hydrologie (dans le projet NoahMP_Morocco) et IA.

## E. Fichiers q1_* Restants et Justification
- La commande `find . -name "q1_*"` démontre qu'aucun fichier `q1_*` n'existe en dehors du dossier d'archive sécurisé `_ARCHIVE_BEFORE_Q1_DUPLICATE_CLEANUP_20260808/`.
- Tous les outputs et reports de production sont désormais propres.

## F. Tests dry-run après suppression
Les deux scripts de génération de figures ont été testés via un `--dry-run`.
- **Hydrologie :** Le script `run_manuscript_hydrological_response_figures.sh` simule parfaitement la génération des 9 figures et des tableaux sans pointer vers le moindre fichier supprimé ou corrompu.
- **RF / XAI :** Le script `run_rf_xai_figures.sh` s'exécute avec succès en simulant la copie des fichiers.

## G. Statut Git
- Toutes les suppressions ont été ajoutées (stagées) et validées dans un commit avec le message `"chore: remove validated duplicate q1 artifacts after cleanup migration"`. Le dépôt IA est maintenant synchronisé et propre.

## H. Risques Restants
- Le dépôt d'archive `_ARCHIVE_BEFORE_Q1_DUPLICATE_CLEANUP_20260808/` occupe de l'espace disque. Il pourra être supprimé de façon permanente une fois que l'article sera officiellement soumis ou publié.

## I. Conclusion
**REPOSITORY CLEAN.** L'architecture des projets IA et Hydrologie a été rationalisée. Les données et les scripts sont isolés proprement sans compromettre la reproductibilité des résultats ni supprimer involontairement des données utiles à de prochaines analyses.
