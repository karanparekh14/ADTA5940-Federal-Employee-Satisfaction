"""
Re-export the deck charts with transparent backgrounds, larger fonts,
and Canva-friendly sizing. Drops into figures_canva/.

These are the same charts but optimized for placing on a colored slide
background without a white box around them.
"""
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures_canva"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 200,
    "savefig.dpi": 250,
    "savefig.transparent": True,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "font.family": "DejaVu Sans",
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.2,
    "grid.color": "#888888",
})

NAVY = "#1E2761"
GREEN = "#2ca02c"
RED = "#d62728"
ORANGE = "#ff7f0e"
BLUE = "#1f77b4"

# --------- Load + clean (same as presentation_pipeline.py) ----------
df = pd.read_csv(HERE / "FEVS_2024_PRDF.csv", low_memory=False)
q_cols = [c for c in df.columns if c.startswith("Q")]
df[q_cols] = df[q_cols].apply(pd.to_numeric, errors="coerce")
df["EEI_Intrinsic"]  = df[["Q2","Q3","Q4","Q6","Q7"]].mean(axis=1)
df["EEI_Supervisor"] = df[["Q48","Q50","Q51","Q52","Q54"]].mean(axis=1)
df["EEI_Leaders"]    = df[["Q57","Q58","Q59","Q61","Q62"]].mean(axis=1)
df["EEI"]            = df[["EEI_Intrinsic","EEI_Supervisor","EEI_Leaders"]].mean(axis=1)
df["WLB"]            = df[["Q34","Q49","Q63"]].mean(axis=1)
df["TW_Infrequent"]  = (df["Q91"] == 2).astype(int)
df["TW_Required"]    = (df["Q91"] == 3).astype(int)
df["TW_ChooseNot"]   = (df["Q91"] == 4).astype(int)
df["Supervisor"]     = df["DSUPER"].map({"A": 0, "B": 1})
df["Male"]           = df["DSEX"].map({"A": 1, "B": 0})
df["Age40plus"]      = df["DAGEGRP"].map({"A": 0, "B": 1})
df["Tenure11_20"]    = (df["DFEDTEN"] == "B").astype(int)
df["Tenure20plus"]   = (df["DFEDTEN"] == "C").astype(int)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight",
                transparent=True, pad_inches=0.05)
    plt.close(fig)
    print(f"  {name}.png")


# --------- 1. Satisfaction distribution ----------
sat = df["Q70"].dropna()
counts = sat.value_counts().sort_index()
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(counts.index, counts.values, color=NAVY, alpha=0.9)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["Very\nDissat.", "Dissat.", "Neutral", "Satisfied",
                    "Very\nSatisfied"])
ax.set_ylabel("Federal employees")
ax.set_title(f"71% say satisfied or very satisfied", color=NAVY, pad=12)
save(fig, "01_satisfaction_distribution")

# --------- 2. Telework raw gap ----------
tw_means = df.groupby("Q91")["Q70"].mean().reindex([1, 2, 3, 4])
labels = ["Routine\nremote", "Infrequent\ntelework", "Required\non-site",
          "Chooses\nnot to"]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(labels, tw_means.values, color=[GREEN, BLUE, RED, ORANGE], alpha=0.9)
ax.axhline(df["Q70"].mean(), ls="--", color="gray", lw=1,
           label=f"Overall mean {df['Q70'].mean():.2f}")
ax.set_ylim(3.0, 4.2)
ax.set_ylabel("Mean job satisfaction (1–5)")
ax.legend(frameon=False)
save(fig, "02_telework_raw_gap")

# --------- 3. R² progression ----------
sub = df[["Q70","TW_Infrequent","TW_Required","TW_ChooseNot",
          "WLB","EEI","Supervisor","Male","Age40plus","Tenure11_20",
          "Tenure20plus"]].dropna()
blocks = {
    "M1\nTelework": ["TW_Infrequent","TW_Required","TW_ChooseNot"],
    "M2\n+WLB":     ["TW_Infrequent","TW_Required","TW_ChooseNot","WLB"],
    "M3\n+EEI":     ["TW_Infrequent","TW_Required","TW_ChooseNot","WLB","EEI"],
    "M4\n+Demo":    ["TW_Infrequent","TW_Required","TW_ChooseNot","WLB","EEI",
                     "Supervisor","Male","Age40plus","Tenure11_20","Tenure20plus"],
}
r2s = []
for name, preds in blocks.items():
    X = sm.add_constant(sub[preds])
    m = sm.OLS(sub["Q70"], X).fit()
    r2s.append(m.rsquared)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(list(blocks.keys()), r2s, color=[RED, ORANGE, GREEN, NAVY], alpha=0.9)
for bar, v in zip(bars, r2s):
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.012,
            f"{v:.0%}", ha="center", fontweight="bold", fontsize=15)
ax.set_ylim(0, 0.75)
ax.set_ylabel("Variance explained (R²)")
save(fig, "03_r2_progression")

# --------- 4. Simpson's paradox ----------
X1 = sm.add_constant(sub[["TW_Infrequent","TW_Required","TW_ChooseNot"]])
m1 = sm.OLS(sub["Q70"], X1).fit()
X4 = sm.add_constant(sub[blocks["M4\n+Demo"]])
m4 = sm.OLS(sub["Q70"], X4).fit()

coefs = pd.DataFrame({
    "Before controls (M1)": [m1.params["TW_Required"], m1.params["TW_Infrequent"]],
    "After controls (M4)":  [m4.params["TW_Required"], m4.params["TW_Infrequent"]],
}, index=["Required on-site", "Infrequent telework"])
fig, ax = plt.subplots(figsize=(9, 5))
coefs.plot(kind="bar", ax=ax, color=[RED, BLUE], width=0.7, alpha=0.9)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("Effect on satisfaction\n(vs. routine remote)")
ax.legend(frameon=False)
ax.tick_params(axis="x", labelrotation=0)
save(fig, "04_simpsons_paradox")

# --------- 5. Standardized coefficients ----------
Xz = sub.drop(columns=["Q70"]).apply(
    lambda c: (c - c.mean()) / c.std() if c.nunique() > 2 else c)
Xz = sm.add_constant(Xz)
yz = (sub["Q70"] - sub["Q70"].mean()) / sub["Q70"].std()
mz = sm.OLS(yz, Xz).fit()
betas = mz.params.drop("const").sort_values()
pretty = {
    "EEI": "Employee engagement",
    "WLB": "Work-life balance",
    "TW_Required": "Required on-site",
    "TW_Infrequent": "Infrequent telework",
    "TW_ChooseNot": "Chooses not to telework",
    "Supervisor": "Is a supervisor",
    "Male": "Male",
    "Age40plus": "Age 40+",
    "Tenure11_20": "Tenure 11–20 yrs",
    "Tenure20plus": "Tenure 20+ yrs",
}
betas.index = [pretty.get(i, i) for i in betas.index]
fig, ax = plt.subplots(figsize=(9, 6))
colors = [GREEN if v > 0 else RED for v in betas.values]
ax.barh(betas.index, betas.values, color=colors, alpha=0.9)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Standardized coefficient (β)")
save(fig, "05_standardized_coefs")

print("\nAll Canva-ready transparent charts saved to figures_canva/")
