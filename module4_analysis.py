"""
ADTA 5940 - Module 4: Model with Results
Karan Parekh | Spring 2026

Research Question:
  To what extent does telework frequency predict overall job satisfaction
  among federal employees, after controlling for work-life balance
  perceptions, employee engagement, and demographic characteristics?

Model: Hierarchical OLS Regression (4 blocks)
Data:  2024 Federal Employee Viewpoint Survey (FEVS) - OPM PRDF
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy import stats
from scipy.stats import f as f_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings, os
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.dpi': 150,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'sans-serif'
})

OUT = r"C:\Users\karan\Downloads\ADTA5940-Capstone\figures"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. LOAD & CLEAN
# ============================================================
FILE = r"C:\Users\karan\Downloads\FEVS\FEVS_2024_PRDF.csv"

print("Loading data...")
df_raw = pd.read_csv(FILE, low_memory=False)
print(f"  Loaded: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns")

df = df_raw.copy()

# -- Likert items: replace invalid codes with NaN, coerce to numeric 1-5 --
INVALID = ['X', ' ', '', 'x', 'Do Not Know', 'No Basis to Judge']

LIKERT_COLS = [
    'Q2','Q3','Q4','Q6','Q7',
    'Q34','Q46','Q48','Q49','Q50','Q51','Q52','Q54',
    'Q57','Q58','Q59','Q61','Q62','Q63',
    'Q70','Q71','Q72',
    'Q86','Q87','Q88','Q89','Q90'
]

for col in LIKERT_COLS:
    if col in df.columns:
        df[col] = df[col].replace(INVALID, np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].where(df[col].between(1, 5))

# -- Q91: telework category, keep values 1-4 --
df['Q91'] = pd.to_numeric(df['Q91'].replace(INVALID, np.nan), errors='coerce')
df['Q91'] = df['Q91'].where(df['Q91'].between(1, 4))

# -- Demographics (letter-coded per OPM PRDF Codebook) --
# DAGEGRP: A=Under 40, B=40 or Older
# DSUPER:  A=Non-Supervisor/Team Leader, B=Supervisor/Manager/Executive
# DFEDTEN: A=10 yrs or fewer, B=11-20 yrs, C=More than 20 yrs
# DSEX:    A=Male, B=Female
# DLEAVING: A=No, B=Yes other, C=Yes fed job, D=Yes outside fed

df['Age_40plus']     = np.where(df['DAGEGRP'].isna(), np.nan,
                                (df['DAGEGRP'] == 'B').astype(float))
df['IsSupervisor']   = np.where(df['DSUPER'].isna(), np.nan,
                                (df['DSUPER'] == 'B').astype(float))
df['IsMale']         = np.where(df['DSEX'].isna(), np.nan,
                                (df['DSEX'] == 'A').astype(float))
# Tenure dummies (reference = 10 yrs or fewer)
df['Tenure_11_20']   = np.where(df['DFEDTEN'].isna(), np.nan,
                                (df['DFEDTEN'] == 'B').astype(float))
df['Tenure_20plus']  = np.where(df['DFEDTEN'].isna(), np.nan,
                                (df['DFEDTEN'] == 'C').astype(float))

# Drop rows missing primary outcome Q70
before = len(df)
df = df.dropna(subset=['Q70'])
print(f"  Rows after removing missing Q70: {len(df):,} / {before:,}")

# ============================================================
# 2. BUILD COMPOSITE INDICES
# ============================================================
EEI_INTRINSIC  = ['Q2','Q3','Q4','Q6','Q7']
EEI_SUPERVISOR = ['Q48','Q50','Q51','Q52','Q54']
EEI_LEADERS    = ['Q57','Q58','Q59','Q61','Q62']

df['EEI_Intrinsic']  = df[EEI_INTRINSIC].mean(axis=1)
df['EEI_Supervisor'] = df[EEI_SUPERVISOR].mean(axis=1)
df['EEI_Leaders']    = df[EEI_LEADERS].mean(axis=1)
df['EEI']            = df[['EEI_Intrinsic','EEI_Supervisor','EEI_Leaders']].mean(axis=1)
df['WLB_Composite']  = df[['Q34','Q49','Q63']].mean(axis=1)
df['EXI']            = df[['Q86','Q87','Q88','Q89','Q90']].mean(axis=1)

print("\nComposite Indices Summary:")
for idx in ['EEI','WLB_Composite','EXI']:
    m = df[idx].mean(); s = df[idx].std(); n = df[idx].notna().sum()
    print(f"  {idx:20s}  mean={m:.3f}  SD={s:.3f}  n={n:,}")

# ============================================================
# 3. CREATE TELEWORK DUMMIES
# ============================================================
# Q91: 1=Routine/Remote (reference), 2=Infrequent, 3=Required in Office, 4=Chooses Not To
tw_map = {1:'Routine/Remote', 2:'Situational/Infrequent',
          3:'Required in Office', 4:'Chooses Not To'}

df['TW_Infrequent'] = np.where(df['Q91'].isna(), np.nan, (df['Q91']==2).astype(float))
df['TW_Required']   = np.where(df['Q91'].isna(), np.nan, (df['Q91']==3).astype(float))
df['TW_ChooseNot']  = np.where(df['Q91'].isna(), np.nan, (df['Q91']==4).astype(float))

# ============================================================
# 4. DESCRIPTIVE STATISTICS
# ============================================================
print("\n" + "="*70)
print("TABLE 1: Descriptive Statistics for Model Variables")
print("="*70)

desc_vars = ['Q70', 'WLB_Composite', 'EEI', 'EEI_Intrinsic',
             'EEI_Supervisor', 'EEI_Leaders']
desc_df = df[desc_vars].describe().T[['count','mean','std','min','max']]
desc_df['count'] = desc_df['count'].astype(int)
print(desc_df.to_string(float_format='%.3f'))

print("\n\nTelework Distribution (Q91):")
tw_counts = df['Q91'].value_counts().sort_index()
total_tw = tw_counts.sum()
for k, v in tw_counts.items():
    print(f"  {tw_map.get(k, k):25s}: {v:>8,}  ({v/total_tw*100:.1f}%)")

print("\nMean Job Satisfaction by Telework Group:")
for k in sorted(df['Q91'].dropna().unique()):
    grp = df[df['Q91']==k]['Q70']
    print(f"  {tw_map.get(k,k):25s}: mean={grp.mean():.3f}, SD={grp.std():.3f}, n={len(grp):,}")

print("\nDemographic Distributions:")
print(f"  Age 40+:      {df['Age_40plus'].sum():,.0f} ({df['Age_40plus'].mean()*100:.1f}%)")
print(f"  Supervisor:   {df['IsSupervisor'].sum():,.0f} ({df['IsSupervisor'].mean()*100:.1f}%)")
print(f"  Male:         {df['IsMale'].sum():,.0f} ({df['IsMale'].mean()*100:.1f}%)")
print(f"  Tenure 11-20: {df['Tenure_11_20'].sum():,.0f}")
print(f"  Tenure 20+:   {df['Tenure_20plus'].sum():,.0f}")

# ============================================================
# 5. ONE-WAY ANOVA
# ============================================================
print("\n" + "="*70)
print("PRELIMINARY: One-Way ANOVA - Job Satisfaction by Telework Group")
print("="*70)
groups = [g['Q70'].dropna().values for _, g in df.dropna(subset=['Q91']).groupby('Q91')]
f_stat, p_val = stats.f_oneway(*groups)
n_total = sum(len(g) for g in groups)
print(f"  F({len(groups)-1}, {n_total-len(groups)}) = {f_stat:.2f}, p < .001")

ss_between = sum(len(g)*(np.mean(g) - df['Q70'].mean())**2 for g in groups)
ss_total = sum(np.sum((g - df['Q70'].mean())**2) for g in groups)
eta_sq = ss_between / ss_total
print(f"  eta-squared = {eta_sq:.4f}")

# Post-hoc pairwise comparisons
print("\n  Pairwise comparisons (Welch t-tests with Bonferroni correction):")
tw_keys = sorted(df['Q91'].dropna().unique())
comparisons = []
for i in range(len(tw_keys)):
    for j in range(i+1, len(tw_keys)):
        g1 = df[df['Q91']==tw_keys[i]]['Q70'].dropna()
        g2 = df[df['Q91']==tw_keys[j]]['Q70'].dropna()
        t, p = stats.ttest_ind(g1, g2, equal_var=False)
        d = (g1.mean() - g2.mean()) / np.sqrt((g1.var() + g2.var()) / 2)
        comparisons.append((tw_keys[i], tw_keys[j], g1.mean()-g2.mean(), t, p, d))

n_comp = len(comparisons)
for k1, k2, diff, t, p, d in comparisons:
    p_adj = min(p * n_comp, 1.0)
    sig = '***' if p_adj<.001 else '**' if p_adj<.01 else '*' if p_adj<.05 else 'ns'
    print(f"    {tw_map[k1]:25s} vs {tw_map[k2]:25s}: diff={diff:+.3f}, t={t:.2f}, p_adj={'<.001' if p_adj<.001 else f'{p_adj:.4f}'}, d={d:.3f} {sig}")

# ============================================================
# 6. HIERARCHICAL OLS REGRESSION
# ============================================================
print("\n" + "="*70)
print("HIERARCHICAL MULTIPLE REGRESSION")
print("="*70)

# Build analytic sample (listwise deletion on ALL model variables)
all_vars = ['Q70',
            'TW_Infrequent', 'TW_Required', 'TW_ChooseNot',
            'WLB_Composite', 'EEI',
            'IsSupervisor', 'IsMale', 'Age_40plus',
            'Tenure_11_20', 'Tenure_20plus']

df_model = df[all_vars].dropna()
print(f"\nAnalytic sample (listwise complete): n = {len(df_model):,}")

y = df_model['Q70']

# -- Model 1: Telework only --
tw_cols = ['TW_Infrequent','TW_Required','TW_ChooseNot']
X1 = sm.add_constant(df_model[tw_cols])
m1 = sm.OLS(y, X1).fit()

# -- Model 2: + Work-Life Balance --
X2 = sm.add_constant(df_model[tw_cols + ['WLB_Composite']])
m2 = sm.OLS(y, X2).fit()

# -- Model 3: + Employee Engagement Index --
X3 = sm.add_constant(df_model[tw_cols + ['WLB_Composite','EEI']])
m3 = sm.OLS(y, X3).fit()

# -- Model 4: Full model + Demographics --
demo_cols = ['IsSupervisor','IsMale','Age_40plus','Tenure_11_20','Tenure_20plus']
X4 = sm.add_constant(df_model[tw_cols + ['WLB_Composite','EEI'] + demo_cols])
m4 = sm.OLS(y, X4).fit()

models = [m1, m2, m3, m4]
model_labels = ['Model 1: Telework', 'Model 2: +WLB', 'Model 3: +EEI', 'Model 4: Full']

# -- Table 2: Model Comparison --
print("\n" + "-"*80)
print("TABLE 2: Model Comparison - Hierarchical Regression")
print("-"*80)
print(f"{'Metric':<20} {'Model 1':>14} {'Model 2':>14} {'Model 3':>14} {'Model 4':>14}")
print("-"*80)

metrics_list = [
    ('R-squared',     [m.rsquared for m in models],     '{:.4f}'),
    ('Adj. R-squared',[m.rsquared_adj for m in models], '{:.4f}'),
    ('F-statistic',   [m.fvalue for m in models],       '{:.2f}'),
    ('AIC',           [m.aic for m in models],          '{:,.0f}'),
    ('BIC',           [m.bic for m in models],          '{:,.0f}'),
    ('n',             [int(m.nobs) for m in models],    '{:,}'),
]

for label, vals, fmt in metrics_list:
    row = f"{label:<20}"
    for v in vals:
        row += f" {fmt.format(v):>14}"
    print(row)

# Delta R-squared
dr2 = ['--'] + [f'{models[i].rsquared - models[i-1].rsquared:.4f}' for i in range(1,4)]
print(f"{'Delta R-squared':<20} {dr2[0]:>14} {dr2[1]:>14} {dr2[2]:>14} {dr2[3]:>14}")

# F-change tests
print("\n  F-Change Tests (incremental contribution of each block):")
for i in range(1, len(models)):
    r2_r = models[i-1].rsquared
    r2_f = models[i].rsquared
    df_num = models[i].df_model - models[i-1].df_model
    df_den = models[i].df_resid
    if df_num > 0:
        f_change = ((r2_f - r2_r) / df_num) / ((1 - r2_f) / df_den)
        p_change = 1 - f_dist.cdf(f_change, df_num, df_den)
        p_str = '< .001' if p_change < .001 else f'= {p_change:.4f}'
        print(f"    Model {i} -> Model {i+1}: Delta-F({int(df_num)}, {int(df_den)}) = {f_change:.2f}, p {p_str}")

# ============================================================
# 7. FULL MODEL COEFFICIENT TABLE
# ============================================================
print("\n" + "-"*120)
print("TABLE 3: Full Model (Model 4) - OLS Regression Coefficients")
print("-"*120)

var_labels = {
    'const': 'Intercept',
    'TW_Infrequent': 'Telework: Situational/Infrequent (vs. Routine/Remote)',
    'TW_Required': 'Telework: Required in Office (vs. Routine/Remote)',
    'TW_ChooseNot': 'Telework: Chooses Not To (vs. Routine/Remote)',
    'WLB_Composite': 'Work-Life Balance Composite',
    'EEI': 'Employee Engagement Index',
    'IsSupervisor': 'Supervisor (vs. Non-Supervisor)',
    'IsMale': 'Male (vs. Female)',
    'Age_40plus': 'Age 40+ (vs. Under 40)',
    'Tenure_11_20': 'Tenure: 11-20 yrs (vs. <=10)',
    'Tenure_20plus': 'Tenure: 20+ yrs (vs. <=10)'
}

# Compute standardized coefficients: Beta_j = B_j * (SD_xj / SD_y)
sd_y = y.std()

coef_records = []
for var in m4.params.index:
    b = m4.params[var]
    se = m4.bse[var]
    t = m4.tvalues[var]
    p = m4.pvalues[var]
    ci = m4.conf_int().loc[var]
    if var == 'const':
        beta = np.nan
    else:
        sd_x = X4[var].std()
        beta = b * (sd_x / sd_y) if sd_x > 0 else 0.0
    coef_records.append({
        'var': var, 'label': var_labels.get(var, var),
        'B': b, 'SE': se, 'Beta': beta, 't': t, 'p': p,
        'CI_low': ci[0], 'CI_high': ci[1]
    })

coef_df = pd.DataFrame(coef_records)

print(f"{'Variable':<55} {'B':>8} {'SE':>8} {'Beta':>8} {'t':>8} {'p':>8} {'95% CI':>20}")
print("-"*120)
for _, r in coef_df.iterrows():
    sig = '***' if r['p']<.001 else '**' if r['p']<.01 else '*' if r['p']<.05 else ''
    p_str = '< .001' if r['p']<.001 else f'{r["p"]:.4f}'
    ci_str = f"[{r['CI_low']:.4f}, {r['CI_high']:.4f}]"
    beta_str = f"{r['Beta']:.4f}" if not np.isnan(r['Beta']) else '  --  '
    print(f"{r['label']:<55} {r['B']:>8.4f} {r['SE']:>8.4f} {beta_str:>8} {r['t']:>8.2f} {p_str:>8} {ci_str:>20} {sig}")

print(f"\n  Note: *p < .05, **p < .01, ***p < .001")
print(f"  R-squared = {m4.rsquared:.4f}, Adjusted R-squared = {m4.rsquared_adj:.4f}")
print(f"  F({int(m4.df_model)}, {int(m4.df_resid)}) = {m4.fvalue:.2f}, p < .001")

# ============================================================
# 8. TABLE: Telework Coefficients Across All Models
# ============================================================
print("\n" + "-"*80)
print("TABLE 4: Telework Coefficients Across Models")
print("-"*80)
print(f"{'Variable':<55} {'M1':>8} {'M2':>8} {'M3':>8} {'M4':>8}")
print("-"*80)
for var in tw_cols:
    row_vals = []
    for m in models:
        b = m.params[var]
        p = m.pvalues[var]
        sig = '***' if p<.001 else '**' if p<.01 else '*' if p<.05 else ''
        row_vals.append(f"{b:.3f}{sig}")
    label = var_labels.get(var, var)
    print(f"{label:<55} {row_vals[0]:>8} {row_vals[1]:>8} {row_vals[2]:>8} {row_vals[3]:>8}")

# ============================================================
# 9. VIF
# ============================================================
print("\n" + "-"*80)
print("TABLE 5: Variance Inflation Factors (VIF) - Full Model")
print("-"*80)
X4_no_const = X4.drop('const', axis=1)
for i, col in enumerate(X4_no_const.columns):
    vif = variance_inflation_factor(X4_no_const.values, i)
    flag = ' WARNING' if vif > 5 else ''
    print(f"  {var_labels.get(col, col):<55} VIF = {vif:.2f}{flag}")
print("  (VIF > 5 indicates potential multicollinearity concern)")

# ============================================================
# 10. REGRESSION DIAGNOSTICS
# ============================================================
print("\n" + "="*70)
print("REGRESSION DIAGNOSTICS - Model 4")
print("="*70)

residuals = m4.resid
fitted = m4.fittedvalues

skew_val = stats.skew(residuals)
kurt_val = stats.kurtosis(residuals)
dw = durbin_watson(residuals)
bp_stat, bp_p, _, _ = het_breuschpagan(residuals, X4)

print(f"  Residual Skewness:  {skew_val:.4f}")
print(f"  Residual Kurtosis:  {kurt_val:.4f}")
print(f"  Durbin-Watson:      {dw:.4f}  (approx 2 = no autocorrelation)")
print(f"  Breusch-Pagan:      chi2 = {bp_stat:.2f}, p {'< .001' if bp_p < .001 else f'= {bp_p:.4f}'}")

if bp_p < .05:
    print("  -> Heteroscedasticity detected; reporting HC3 robust standard errors.")
    m4_robust = sm.OLS(y, X4).fit(cov_type='HC3')
    
    print(f"\n{'Variable':<55} {'B':>8} {'Robust SE':>10} {'t':>8} {'p':>8}")
    print("-"*90)
    for var in m4_robust.params.index:
        label = var_labels.get(var, var)
        b = m4_robust.params[var]
        se = m4_robust.bse[var]
        t = m4_robust.tvalues[var]
        p = m4_robust.pvalues[var]
        sig = '***' if p<.001 else '**' if p<.01 else '*' if p<.05 else ''
        p_str = '< .001' if p<.001 else f'{p:.4f}'
        print(f"  {label:<53} {b:>8.4f} {se:>10.4f} {t:>8.2f} {p_str:>8} {sig}")

# ============================================================
# 11. EFFECT SIZES
# ============================================================
print("\n" + "="*70)
print("EFFECT SIZE SUMMARY")
print("="*70)
for i, (m, name) in enumerate(zip(models, model_labels)):
    f2 = m.rsquared / (1 - m.rsquared)
    effect = 'large' if f2 >= 0.35 else 'medium' if f2 >= 0.15 else 'small' if f2 >= 0.02 else 'negligible'
    print(f"  {name:<25}: R2 = {m.rsquared:.4f}, f2 = {f2:.4f} ({effect} effect)")

print("\n  Incremental f2 (unique contribution of each block):")
for i in range(1, len(models)):
    dr2_val = models[i].rsquared - models[i-1].rsquared
    f2_inc = dr2_val / (1 - models[i].rsquared)
    effect = 'large' if f2_inc >= 0.35 else 'medium' if f2_inc >= 0.15 else 'small' if f2_inc >= 0.02 else 'negligible'
    print(f"    Block {i+1}: Delta-f2 = {f2_inc:.4f} ({effect})")

# ============================================================
# 12. FIGURES
# ============================================================
print("\n" + "="*70)
print("GENERATING FIGURES...")
print("="*70)

# --- Figure 1: Job Satisfaction by Telework Group ---
fig, ax = plt.subplots(figsize=(8, 5))
tw_means = df.groupby('Q91')['Q70'].agg(['mean','std','count']).reset_index()
tw_means['label'] = tw_means['Q91'].map(tw_map)
tw_means['se'] = tw_means['std'] / np.sqrt(tw_means['count'])
colors = ['#2196F3','#FF9800','#F44336','#9E9E9E']
bars = ax.bar(tw_means['label'], tw_means['mean'], yerr=tw_means['se']*1.96,
              capsize=5, color=colors, edgecolor='white', linewidth=0.5)
ax.bar_label(bars, fmt='%.3f', padding=6, fontsize=9, fontweight='bold')
ax.set_ylabel("Mean Job Satisfaction (Q70, 1-5 Scale)")
ax.set_xlabel("Telework Category")
ax.set_title("Figure 1. Mean Job Satisfaction by Telework Category\n(Error bars = 95% CI)")
ax.set_ylim(1, 4.6)
ax.axhline(y=df['Q70'].mean(), color='gray', linestyle='--', alpha=0.7,
           label=f'Overall Mean ({df["Q70"].mean():.2f})')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig1_satisfaction_by_telework.png'), bbox_inches='tight')
plt.close()
print("  Saved fig1_satisfaction_by_telework.png")

# --- Figure 2: R-squared Progression ---
fig, ax = plt.subplots(figsize=(7, 5))
r2_vals = [m.rsquared for m in models]
adj_r2_vals = [m.rsquared_adj for m in models]
x = np.arange(len(models))
w = 0.35
bars1 = ax.bar(x - w/2, r2_vals, w, color='steelblue', alpha=0.85, label='R-squared')
bars2 = ax.bar(x + w/2, adj_r2_vals, w, color='coral', alpha=0.85, label='Adj. R-squared')
for b in bars1:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.005,
            f'{b.get_height():.4f}', ha='center', fontsize=8, fontweight='bold')
for b in bars2:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.005,
            f'{b.get_height():.4f}', ha='center', fontsize=8)
short_names = ['Model 1\n(Telework)', 'Model 2\n(+WLB)', 'Model 3\n(+EEI)', 'Model 4\n(+Demo)']
ax.set_xticks(x)
ax.set_xticklabels(short_names)
ax.set_ylabel('Variance Explained')
ax.set_title('Figure 2. Hierarchical Regression: Cumulative R-squared by Model Block')
ax.legend()
ax.set_ylim(0, max(r2_vals)*1.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig2_r2_progression.png'), bbox_inches='tight')
plt.close()
print("  Saved fig2_r2_progression.png")

# --- Figure 3: Standardized Coefficient Forest Plot ---
fig, ax = plt.subplots(figsize=(9, 6))
plot_coefs = coef_df[coef_df['var'] != 'const'].copy()
plot_coefs = plot_coefs.sort_values('Beta')
clrs = ['#F44336' if b < 0 else '#4CAF50' for b in plot_coefs['Beta']]
bars = ax.barh(plot_coefs['label'], plot_coefs['Beta'], color=clrs, edgecolor='white', height=0.7)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel('Standardized Coefficient (Beta)')
ax.set_title('Figure 3. Standardized Regression Coefficients - Full Model (Model 4)')
for i, (_, row) in enumerate(plot_coefs.iterrows()):
    p = m4.pvalues[row['var']]
    sig = '***' if p<.001 else '**' if p<.01 else '*' if p<.05 else ''
    offset = 0.005 if row['Beta'] >= 0 else -0.005
    ha = 'left' if row['Beta'] >= 0 else 'right'
    ax.text(row['Beta'] + offset, i, f"{row['Beta']:.3f}{sig}", va='center', ha=ha, fontsize=7.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig3_coefficients_forest.png'), bbox_inches='tight')
plt.close()
print("  Saved fig3_coefficients_forest.png")

# --- Figure 4: WLB vs Satisfaction ---
fig, ax = plt.subplots(figsize=(7, 5))
sample = df[['WLB_Composite','Q70']].dropna()
if len(sample) > 10000:
    sample = sample.sample(n=10000, random_state=42)
ax.scatter(sample['WLB_Composite'], sample['Q70'] + np.random.normal(0, 0.05, len(sample)),
           alpha=0.06, s=6, color='steelblue', rasterized=True)
z = np.polyfit(sample['WLB_Composite'], sample['Q70'], 1)
p_fn = np.poly1d(z)
x_line = np.linspace(1, 5, 100)
ax.plot(x_line, p_fn(x_line), color='#F44336', linewidth=2.5, label=f'OLS fit (slope={z[0]:.3f})')
r_val, _ = stats.pearsonr(sample['WLB_Composite'], sample['Q70'])
ax.set_xlabel('Work-Life Balance Composite (1-5)')
ax.set_ylabel('Job Satisfaction (Q70, 1-5)')
ax.set_title(f'Figure 4. Work-Life Balance vs. Job Satisfaction\nr = {r_val:.3f}, p < .001')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig4_wlb_vs_satisfaction.png'), bbox_inches='tight')
plt.close()
print("  Saved fig4_wlb_vs_satisfaction.png")

# --- Figure 5: Correlation Heatmap ---
fig, ax = plt.subplots(figsize=(8, 6))
corr_vars = ['Q70','WLB_Composite','EEI','EEI_Intrinsic','EEI_Supervisor','EEI_Leaders']
corr_labels_fig = ['Job Satisfaction','WLB Composite','EEI Overall','EEI Intrinsic',
               'EEI Supervisor','EEI Leaders']
corr_matrix = df[corr_vars].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.3f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True,
            xticklabels=corr_labels_fig, yticklabels=corr_labels_fig, ax=ax, linewidths=0.5)
ax.set_title('Figure 5. Correlation Matrix of Key Model Variables')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig5_correlation_heatmap.png'), bbox_inches='tight')
plt.close()
print("  Saved fig5_correlation_heatmap.png")

# --- Figure 6: Residual Diagnostics ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(fitted, residuals, alpha=0.02, s=3, color='steelblue', rasterized=True)
axes[0].axhline(y=0, color='red', linewidth=1)
axes[0].set_xlabel('Fitted Values')
axes[0].set_ylabel('Residuals')
axes[0].set_title('Figure 6a. Residuals vs. Fitted Values')

axes[1].hist(residuals, bins=80, color='steelblue', edgecolor='white', density=True)
x_norm = np.linspace(residuals.min(), residuals.max(), 200)
axes[1].plot(x_norm, stats.norm.pdf(x_norm, residuals.mean(), residuals.std()),
             color='red', linewidth=2, label='Normal curve')
axes[1].set_xlabel('Residuals')
axes[1].set_ylabel('Density')
axes[1].set_title('Figure 6b. Distribution of Residuals')
axes[1].legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'fig6_diagnostics.png'), bbox_inches='tight')
plt.close()
print("  Saved fig6_diagnostics.png")

# ============================================================
# DONE
# ============================================================
print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("All figures saved to:", OUT)
print("="*70)
