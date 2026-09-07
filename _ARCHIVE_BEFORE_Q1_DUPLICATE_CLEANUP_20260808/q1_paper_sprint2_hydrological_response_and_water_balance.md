# Q1 Paper Sprint 2: Hydrological Response and Water Balance

## A. Objective
Produce the indispensable hydrological diagnostics to link SMAP increments to their propagation in Noah-MP (SSM, RZSM, ET, total runoff, surface runoff, baseflow). Ensure a clean comparison between DA-NoCDF, DA-CDF, and OPL, using proper units and cautious interpretation.

## B. Variable mapping and units
- **Precipitation (P)**: Originally in mm/month, converted to **mm/day**. Sourced exclusively from IMERG.
- **Evapotranspiration (ET)**: Converted to **mm/day**.
- **Surface Runoff (Qs)**: Converted to **mm/day**.
- **Baseflow (Qsb)**: Converted to **mm/day**.
- **Total Runoff (Qtotal)**: Computed as Qs + Qsb, in **mm/day**.
- **Soil Moisture (SSM, RZSM)**: Maintained in native **m³/m³**.

*See `reports/q1_sprint2_units_and_variable_mapping.md` for full details.*

## C. CDF vs NoCDF hydrological response
- **DA-NoCDF** generally exposes a stronger hydrological response than DA-CDF. The assimilation updates significantly alter the soil moisture profile (SSM, RZSM) and propagate deeply into the hydrological fluxes (ET and Runoff).
- **DA-CDF** matching heavily attenuates the propagation of SMAP increments into the hydrological variables. CDF matching strongly attenuates the runoff/baseflow response relative to DA-NoCDF, while ET remains non-negligibly affected and season-dependent.

## D. Seasonal contrast DJF/JJA
The hydrological response exhibits a distinct seasonal signature:
- During DJF, DA-NoCDF suggests a drying effect compared to the OPL, reducing soil moisture and subsequently depressing runoff generation.
- During JJA, DA-NoCDF is associated with slight wetting, suggesting the model background is marginally too dry compared to the satellite retrievals.

## E. Runoff partitioning: surface runoff vs baseflow
- The runoff response is strongly dominated by the baseflow-like component (Qsb) in the pre-routing Noah-MP outputs. Surface runoff (Qs) response is comparatively marginal.
- This baseflow response should **not** be interpreted directly as improved streamflow, because no HyMAP routing or streamflow validation is included in this phase. It acts as a deep slow reservoir buffering the assimilation impacts.

## F. First-order water-balance diagnostic
- The flux-only water balance (P - ET - Qtotal) was calculated to assess interpretability.
- The first-order water-balance diagnostic is used to assess interpretability and diagnostic consistency, not perfect closure (which would require complex dS storage accounting).
- The flux-only balance provides a first-order interpretability check, but does not demonstrate water-balance closure because storage changes are not explicitly included.

## G. Interpretation for Q1 paper
- The contrast between DA-NoCDF and DA-CDF demonstrates that CDF matching obscures the physical diagnostic value of the assimilation. 
- NoCDF remains diagnostic rather than hydrologically conservative. It allows us to track where the model structurally deviates from satellite observations.
- IMERG precipitation forcing and seasonality provide context for interpreting the hydrological response, but precipitation-error attribution remains a future extension.

## H. Remaining limitations
- The water balance lacks the storage term (dS) for perfect closure due to temporal aggregation limits.
- The absence of a routing model limits the direct validation of the baseflow anomalies against observed streamflow.
- Irrigation is OFF; thus, any agricultural signal is absorbed as a generic structural error.

## I. Recommended figures for main paper and supplementary
**Main Paper:**
- `q1_fig_cdf_nocdf_hydrological_response_annual_2016_2020.png`
- `q1_fig_cdf_nocdf_hydrological_response_DJF_2016_2020.png`
- `q1_fig_cdf_nocdf_hydrological_response_JJA_2016_2020.png`

**Supplementary:**
- `q1_fig_precip_runoff_components_DA_NoCDF_IMERG_2016_2020.png`
- `q1_fig_precip_runoff_components_DA_CDF_IMERG_2016_2020.png`
- `q1_fig_first_order_water_balance.png`
