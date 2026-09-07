# In-Situ Precipitation Inventory

| filename | format | columns | date_col | station_col | lat_lon_col | precip_col | frequency | period_min | period_max | has_2016_2020 |
|---|---|---|---|---|---|---|---|---|---|---|
| Agadir-massira.txt | txt | Year, Month, Day, Precip, Tmax, Tmin | Year/Month/Day | None | None | Precip | daily | 1992-01-01 | 2022-12-31 | True |
| Chefchaouen.txt | txt | Year, Month, Day, Precip, Tmax, Tmin | Year/Month/Day | None | None | Precip | daily | 1994-08-01 | 2022-12-31 | True |
| Guelmim.txt | txt | Year, Month, Day, Precip, Tmax, Tmin | Year/Month/Day | None | None | Precip | daily | 1992-02-01 | 2022-12-31 | True |
| Tiznit.txt | txt | Year, Month, Day, Precip, Tmax, Tmin | Year/Month/Day | None | None | Precip | daily | 1989-01-01 | 2022-12-31 | True |

## Conclusion
- **usable_for_2016_2020**: partial (temporally yes, spatially extremely limited)
- **station_count_2016_2020**: 4
- **temporal_frequency**: daily
- **spatial_coverage**: Very poor (only 4 stations for the entire domain).
- **main_limitations**: There are only 4 stations available without explicit latitude/longitude coordinates in the files. This spatial density is entirely insufficient to create a reliable precipitation-error predictor for a 5km pixel-based Random Forest over the Moroccan domain. A vast majority of pixels would have no data.
