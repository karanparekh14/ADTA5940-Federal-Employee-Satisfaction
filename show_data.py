import pandas as pd
df = pd.read_csv('C:/Users/karan/Downloads/FEVS/FEVS_2024_PRDF.csv', low_memory=False)

# Show sample rows
print('=== SAMPLE DATA (key columns) ===')
key_cols = ['RandomID', 'agency', 'Q61', 'Q64', 'Q69', 'DAGEGRP', 'DSEX', 'DSUPER', 'DFEDTEN']
print(df[key_cols].head(10).to_string())

# Unique agencies
print(f'\nUnique agencies: {df["agency"].nunique()}')
print(df['agency'].value_counts().head(10))

# Quick stats
print('\n=== JOB SATISFACTION (Q69) STATS ===')
q69 = pd.to_numeric(df['Q69'], errors='coerce')
print(f'  Mean: {q69.mean():.2f}')
print(f'  Median: {q69.median():.1f}')
print(f'  Std Dev: {q69.std():.2f}')
print(f'  Valid: {q69.notna().sum():,} / Missing: {q69.isna().sum():,}')

print('\n=== TELEWORK (Q61) STATS ===')
q61 = pd.to_numeric(df['Q61'], errors='coerce')
print(f'  Mean: {q61.mean():.2f}')
print(f'  Median: {q61.median():.1f}')
print(f'  Valid: {q61.notna().sum():,} / X (not applicable): {(df["Q61"]=="X").sum():,}')

print('\n=== WLB (Q64) STATS ===')
q64 = pd.to_numeric(df['Q64'], errors='coerce')
print(f'  Mean: {q64.mean():.2f}')
print(f'  Median: {q64.median():.1f}')
print(f'  Valid: {q64.notna().sum():,}')

# EEI composite (Q3, Q4, Q5, Q6, Q11, Q12, Q13, Q14)
print('\n=== ENGAGEMENT INDEX (EEI) ===')
eei_items = ['Q3','Q4','Q6','Q11','Q12','Q13','Q14']
for q in eei_items:
    val = pd.to_numeric(df[q], errors='coerce')
    print(f'  {q}: mean={val.mean():.2f}, valid={val.notna().sum():,}')
