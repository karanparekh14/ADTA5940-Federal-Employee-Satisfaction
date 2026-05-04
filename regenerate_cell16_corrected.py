"""
Re-render cell 16 of Attrition_Pipeline_Cleaned.ipynb with corrected
x-axis label and color order.

FEVS Q71 coding: 1 = Very Dissatisfied  ...  5 = Very Satisfied
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / "FEVS_2024_PRDF.csv"
OUT = HERE / "figures_from_notebook" / "cell16_attrition_by_pay_CORRECTED.png"

df = pd.read_csv(DATA, low_memory=False)
df = df[df['DLEAVING'].notna()].copy()
df['DLEAVING_BIN'] = np.where(df['DLEAVING'] == 'A', 0, 1)
df['Q71'] = pd.to_numeric(df['Q71'], errors='coerce')

attr_by_pay = df.groupby('Q71')['DLEAVING_BIN'].mean()

# Red = unhappy with pay (left, x=1), Green = happy with pay (right, x=5)
colors = ['red', 'orange', 'gold', 'lightgreen', 'green']
fig, ax = plt.subplots(figsize=(8, 5))
attr_by_pay.plot(kind='bar', color=colors[:len(attr_by_pay)], ax=ax)
ax.set_title('Attrition Rate by Pay Satisfaction (Q71)')
ax.set_xlabel('Q71 (1=Very Dissatisfied ... 5=Very Satisfied)')
ax.set_ylabel('Attrition Rate')
ax.tick_params(axis='x', labelrotation=0)
fig.tight_layout()
fig.savefig(OUT, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Saved: {OUT}")
