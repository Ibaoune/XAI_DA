import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# Create directories
os.makedirs('outputs/figures', exist_ok=True)
os.makedirs('outputs/tables', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# 1. Load Data
df = pd.read_parquet('data/processed/monthly_pixel_dataset_2016_2020_static.parquet')

# Variables mapping
var_map = {
    'SSM': ('SSM_OPL', 'SSM_DA_NoCDF', 'SSM_DA_CDF'),
    'RZSM': ('RZSM_OPL', 'RZSM_DA_NoCDF', 'RZSM_DA_CDF'),
    'ET': ('Evap_tavg_OPL', 'Evap_tavg_DA_NoCDF', 'Evap_tavg_DA_CDF'),
    'Qs': ('Qs_tavg_OPL', 'Qs_tavg_DA_NoCDF', 'Qs_tavg_DA_CDF'),
    'Qsb': ('Qsb_tavg_OPL', 'Qsb_tavg_DA_NoCDF', 'Qsb_tavg_DA_CDF'),
    'P': ('Rainf_tavg_OPL', 'Rainf_tavg_DA_NoCDF', 'Rainf_tavg_DA_CDF')
}

# 2. Conversion mm/month -> mm/day
days_in_month = {1:31, 2:28.25, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
if 'month' not in df.columns:
    df['month'] = pd.to_datetime(df['time']).dt.month
df['days'] = df['month'].map(days_in_month)

for v in ['ET', 'Qs', 'Qsb', 'P']:
    for c in var_map[v]:
        if c in df.columns:
            # Assume original is mm/month based on data exploration
            df[c + '_mm_day'] = df[c] / df['days']

# Compute total runoff
for exp in ['OPL', 'DA_NoCDF', 'DA_CDF']:
    df[f'Qtotal_{exp}_mm_day'] = df[f'Qs_tavg_{exp}_mm_day'] + df[f'Qsb_tavg_{exp}_mm_day']

# Subsets
df_djf = df[df['month'].isin([12, 1, 2])]
df_jja = df[df['month'].isin([6, 7, 8])]
df_ann = df

# 3. Plotting function
def plot_hydrological_response(subset_df, period_name, filename):
    fig, axes = plt.subplots(3, 6, figsize=(24, 12))
    
    # Calculate means
    mean_df = subset_df.groupby(['lat', 'lon']).mean().reset_index()
    
    variables = [
        ('SSM', 'SSM', 'SSM', 'm3/m3', 0.05),
        ('RZSM', 'RZSM', 'RZSM', 'm3/m3', 0.05),
        ('ET', 'Evap_tavg', '_mm_day', 'mm/day', 0.5),
        ('Qtotal', 'Qtotal', '_mm_day', 'mm/day', 0.2),
        ('Qs', 'Qs_tavg', '_mm_day', 'mm/day', 0.1),
        ('Qsb', 'Qsb_tavg', '_mm_day', 'mm/day', 0.2)
    ]
    
    experiments = [
        ('DA_NoCDF - OPL', 'DA_NoCDF', 'OPL'),
        ('DA_CDF - OPL', 'DA_CDF', 'OPL'),
        ('DA_NoCDF - DA_CDF', 'DA_NoCDF', 'DA_CDF')
    ]
    
    for c, (title, base_var, suffix, unit, vmax) in enumerate(variables):
        for r, (row_title, exp1, exp2) in enumerate(experiments):
            ax = axes[r, c]
            ax.set_aspect('equal')
            ax.set_facecolor('white')
            
            if base_var == 'Qtotal':
                col1 = f'Qtotal_{exp1}{suffix}'
                col2 = f'Qtotal_{exp2}{suffix}'
            else:
                col1 = f'{base_var}_{exp1}'
                if suffix == '_mm_day': col1 += suffix
                col2 = f'{base_var}_{exp2}'
                if suffix == '_mm_day': col2 += suffix
            
            diff = mean_df[col1] - mean_df[col2]
            
            sc = ax.scatter(mean_df['lon'], mean_df['lat'], c=diff, cmap='RdBu', 
                            vmin=-vmax, vmax=vmax, s=15, marker='s', edgecolors='none')
            
            d_min, d_mean, d_max = diff.min(), diff.mean(), diff.max()
            pos_pct = (diff > 0).mean() * 100
            neg_pct = (diff < 0).mean() * 100
            
            ax.set_title(f"{row_title}\nΔ{title}")
            ax.text(0.05, 0.05, f"Min: {d_min:.3f}\nMean: {d_mean:.3f}\nMax: {d_max:.3f}", 
                    transform=ax.transAxes, fontsize=9, bbox=dict(facecolor='white', alpha=0.7))
            ax.axis('off')
            
            if r == 2:
                cbar = plt.colorbar(sc, ax=axes[:, c], orientation='horizontal', fraction=0.05, pad=0.1)
                cbar.set_label(f"Δ{title} ({unit})")

    plt.tight_layout()
    plt.savefig(f'outputs/figures/{filename}', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

# Avoid recreating figures if they already exist to save time
if not os.path.exists("outputs/figures/q1_fig_cdf_nocdf_hydrological_response_annual_2016_2020.png"):
    print("Generating response figures...")
    plot_hydrological_response(df_ann, "Annual", "q1_fig_cdf_nocdf_hydrological_response_annual_2016_2020.png")
    plot_hydrological_response(df_djf, "DJF", "q1_fig_cdf_nocdf_hydrological_response_DJF_2016_2020.png")
    plot_hydrological_response(df_jja, "JJA", "q1_fig_cdf_nocdf_hydrological_response_JJA_2016_2020.png")

# 4. Generate Summary Table
print("Generating summary table...")
summary_data = []
periods = [('annual', df_ann), ('DJF', df_djf), ('JJA', df_jja)]
variables = [
    ('SSM', 'SSM', 'SSM', 'm3/m3'),
    ('RZSM', 'RZSM', 'RZSM', 'm3/m3'),
    ('ET', 'Evap_tavg', '_mm_day', 'mm/day'),
    ('total_runoff', 'Qtotal', '_mm_day', 'mm/day'),
    ('surface_runoff', 'Qs_tavg', '_mm_day', 'mm/day'),
    ('baseflow', 'Qsb_tavg', '_mm_day', 'mm/day')
]
experiments = [
    ('DA-NoCDF_minus_OPL', 'DA_NoCDF', 'OPL'),
    ('DA-CDF_minus_OPL', 'DA_CDF', 'OPL'),
    ('DA-NoCDF_minus_DA-CDF', 'DA_NoCDF', 'DA_CDF')
]

for p_name, p_df in periods:
    mean_df = p_df.groupby(['lat', 'lon']).mean().reset_index()
    for exp_name, exp1, exp2 in experiments:
        for v_name, base_var, suffix, unit in variables:
            if base_var == 'Qtotal':
                col1 = f'Qtotal_{exp1}{suffix}'
                col2 = f'Qtotal_{exp2}{suffix}'
            else:
                col1 = f'{base_var}_{exp1}'
                if suffix == '_mm_day': col1 += suffix
                col2 = f'{base_var}_{exp2}'
                if suffix == '_mm_day': col2 += suffix
                
            diff = mean_df[col1] - mean_df[col2]
            summary_data.append({
                'experiment_difference': exp_name,
                'period': p_name,
                'variable': v_name,
                'unit': unit,
                'min': diff.min(),
                'mean': diff.mean(),
                'median': diff.median(),
                'max': diff.max(),
                'std': diff.std(),
                'percent_positive': (diff > 0).mean() * 100,
                'percent_negative': (diff < 0).mean() * 100,
                'n_pixels': len(diff)
            })

sum_df = pd.DataFrame(summary_data)
sum_df.to_csv('outputs/tables/q1_hydrological_response_summary.csv', index=False)

with open('reports/q1_hydrological_response_summary.md', 'w') as f:
    f.write("| " + " | ".join(sum_df.columns) + " |\n")
    f.write("| " + " | ".join(["---"] * len(sum_df.columns)) + " |\n")
    for _, row in sum_df.iterrows():
        f.write("| " + " | ".join([str(x) for x in row.values]) + " |\n")

# 5. First-order water balance (mm/day)
print("Generating water balance...")
wb_data = []
for p_name, p_df in periods:
    mean_df = p_df.groupby(['lat', 'lon']).mean().reset_index()
    for exp in ['OPL', 'DA_NoCDF', 'DA_CDF']:
        p = mean_df[f'Rainf_tavg_{exp}_mm_day'].mean()
        et = mean_df[f'Evap_tavg_{exp}_mm_day'].mean()
        qs = mean_df[f'Qs_tavg_{exp}_mm_day'].mean()
        qsb = mean_df[f'Qsb_tavg_{exp}_mm_day'].mean()
        qtot = qs + qsb
        
        # dS soil (very rough estimate by looking at SMC layers if we want, but for now flux-only)
        # Using flux-only residual as instructed since dS requires time-differences which are complex for grouped seasonal means
        residual = p - et - qtot
        
        wb_data.append({
            'period': p_name,
            'experiment': exp,
            'P': p,
            'ET': et,
            'Qs': qs,
            'Qsb': qsb,
            'Qtotal': qtot,
            'flux_only_residual': residual
        })

wb_df = pd.DataFrame(wb_data)
wb_df.to_csv('outputs/tables/q1_first_order_water_balance_annual_seasonal.csv', index=False)

# Plot water balance
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, p_name in enumerate(['annual', 'DJF', 'JJA']):
    ax = axes[i]
    sub = wb_df[wb_df['period'] == p_name]
    x = np.arange(3)
    width = 0.2
    
    ax.bar(x - width*1.5, sub['P'], width, label='P')
    ax.bar(x - width*0.5, sub['ET'], width, label='ET')
    ax.bar(x + width*0.5, sub['Qtotal'], width, label='Qtotal')
    ax.bar(x + width*1.5, sub['flux_only_residual'], width, label='Residual')
    
    ax.set_xticks(x)
    ax.set_xticklabels(sub['experiment'])
    ax.set_title(f"Water Balance ({p_name})")
    ax.set_ylabel("mm/day")
    if i == 0:
        ax.legend()

plt.tight_layout()
plt.savefig('outputs/figures/q1_fig_first_order_water_balance.png', dpi=150, facecolor='white')
plt.close()

# 6. Correct existing Precip/Runoff figures
def plot_precip_runoff(exp, filename):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    mean_df = df_ann.groupby(['lat', 'lon']).mean().reset_index()
    
    vars_to_plot = [
        (f'Rainf_tavg_{exp}_mm_day', 'Precipitation (IMERG)', 0, 5),
        (f'Qtotal_{exp}_mm_day', 'Total Runoff', 0, 1),
        (f'Qsb_tavg_{exp}_mm_day', 'Baseflow', 0, 1)
    ]
    
    for ax, (var, title, vmin, vmax) in zip(axes, vars_to_plot):
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        sc = ax.scatter(mean_df['lon'], mean_df['lat'], c=mean_df[var], cmap='viridis', 
                        vmin=vmin, vmax=vmax, s=15, marker='s', edgecolors='none')
        ax.set_title(title)
        d_min, d_mean, d_max = mean_df[var].min(), mean_df[var].mean(), mean_df[var].max()
        ax.text(0.05, 0.05, f"Mean: {d_mean:.3f}", transform=ax.transAxes, 
                fontsize=9, bbox=dict(facecolor='white', alpha=0.7))
        plt.colorbar(sc, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, label='mm/day')
        ax.axis('off')
        
    plt.suptitle(f"{exp} Components (Note: Weak color contrast in DA-CDF indicates small response relative to NoCDF)")
    plt.tight_layout()
    plt.savefig(f'outputs/figures/{filename}', dpi=150, facecolor='white')
    plt.close()

plot_precip_runoff('DA_NoCDF', 'q1_fig_precip_runoff_components_DA_NoCDF_IMERG_2016_2020.png')
plot_precip_runoff('DA_CDF', 'q1_fig_precip_runoff_components_DA_CDF_IMERG_2016_2020.png')

print("All tasks completed.")
