# SMAP DA Diagnostics Inventory

Found 22195 potential SMAP DA files.

## NetCDF Candidates
- **Sample inspected**: `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020/output/2017-09/EnKF/201709/LIS_DA_EnKF_201709030700_incr.a01.d01.nc`
- **Variables**:
  - `anlys_incr_Soil Moisture Layer 1_01`
  - `anlys_incr_Soil Moisture Layer 2_01`
  - `anlys_incr_Soil Moisture Layer 3_01`
  - `anlys_incr_Soil Moisture Layer 4_01`

## Other Candidates (Logs, Text, Bin)
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/logs/122018/DA_SMAP_nocdf_noirr_2018-12_7361172.log`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/logs/052016/DA_SMAP_nocdf_noirr_2016-05_7350616.log`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020/logs/072018/DA_SMAP_cdf_noirr_2018-07_7370802.log`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020/output/2018-07/DAPERT/201807/LIS_DAPERT_201807312345.d01.bin`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/logs/062018/DA_SMAP_nocdf_noirr_2018-06_7359472.log`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020/restarts/pert/LIS_DAPERT_201910010000.d01.bin`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/restarts/pert/LIS_DAPERT_202007010000.d01.bin`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/output/2018-06/DAPERT/201807/LIS_DAPERT_201807010000.d01.bin`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_nocdf_noirr_2016_2020/logs/082020/DA_SMAP_nocdf_noirr_2020-08_7371997.log`
- `/home/mohammad.elaabaribao/lustre/empowermed-ahl6xm8o7mg/users/mohammad.elaabaribao/NoahMP_Morocco/experiments/NorthMor/matrix_2016_2020/DA_cdf_noirr_2016_2020/restarts/pert/LIS_DAPERT_202009010000.d01.bin`

## Recommendation
To read `innovation` and `increment`, you must parse the variables like `anlys_incr_Soil Moisture...` from the `LIS_DA_EnKF_*_incr.nc` files and merge them temporally with the dataset.
