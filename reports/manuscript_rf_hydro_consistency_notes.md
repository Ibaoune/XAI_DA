# Consistency Notes: Hydrology Diagnostics vs RF/XAI

This document explicitly links the physical hydrological results (from `NoahMP_Morocco/scripts/postproc/`) to the statistical diagnostic results (from `IA_SM_assim/`).

| hydrological_result | RF_result | consistency_message | caution |
|---|---|---|---|
| ET response strong (especially in JJA) | RF ET target high R2 (Temporal & Spatial) | Coherent. ET and RZSM are the most predictable DA-induced responses and show the strongest spatial generalization. | Association is not causal. |
| RZSM response interpretable | RF RZSM robust (R2 > 0.65) | Supports the interpretation of vertical propagation of assimilation signals. | ET and RZSM are strongly associated with OPL states. |
| Baseflow changes visible (strong in DJF) | RF baseflow negative spatial R2 | Baseflow structural changes are heavily localized and do not generalize. | Baseflow should remain a cautious, pre-routing diagnostic interpretation. |
| Surface states directly updated | RF SSM increment moderately predictable | Expected direct impact, though non-linearities obscure full predictability. | Rescaling (CDF) weakens pure statistical links. |
| Spatial patterns follow topography/texture | Static-surface variables (land_cover, soil_texture) important in RF | Consistent. Static heterogeneity correlates with the spatial structure of increments. | land_cover and soil_texture are associated with the spatial structure of DA responses, suggesting that unresolved or imperfectly represented land-surface heterogeneity may modulate assimilation impacts. |
