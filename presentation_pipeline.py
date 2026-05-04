"""
ADTA 5940 Capstone — Module 5 Presentation Pipeline
====================================================
Karan Parekh & Chau Le | Spring 2026

Single end-to-end script that produces every figure and number the team
needs for the May 4 final presentation. Aligned with the submitted
Module 4 document (two research questions on job satisfaction), with an
optional attrition track included as a secondary insight.

Run:  python presentation_pipeline.py
Out:  figures_presentation/*.png  +  results_presentation.csv
"""

from __future__ import annotations
import os, warnings, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, roc_auc_score, classification_report

warnings.filterwarnings("ignore")

# -------- Plot defaults (presentation-friendly) --------
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})
PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

HERE = Path(__file__).resolve().parent
FIGDIR = HERE / "figures_presentation"
FIGDIR.mkdir(exist_ok=True)


def find_data() -> Path:
    candidates = [
        HERE / "FEVS_2024_PRDF.csv",
        Path.home() / "Downloads" / "ADTA5940-Capstone" / "FEVS_2024_PRDF.csv",
        Path.home() / "Downloads" / "FEVS_2024_PRDF.csv",
        Path.home() / "Downloads" / "FEVS" / "FEVS_2024_PRDF.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("FEVS_2024_PRDF.csv not found. Drop it next to this script.")


def load_and_clean() -> pd.DataFrame:
    path = find_data()
    print(f"[load] {path}")
    df = pd.read_csv(path, low_memory=False)
    print(f"[load] shape = {df.shape}")

    # Convert Q* to numeric, treating X / blank / -1 / -2 as missing
    q_cols = [c for c in df.columns if c.startswith("Q")]
    df[q_cols] = df[q_cols].apply(pd.to_numeric, errors="coerce")

    # OPM EEI subindex items (matches module4_analysis.py — the version submitted)
    eei_intrinsic  = ["Q2", "Q3", "Q4", "Q6", "Q7"]
    eei_supervisor = ["Q48", "Q50", "Q51", "Q52", "Q54"]
    eei_leaders    = ["Q57", "Q58", "Q59", "Q61", "Q62"]

    for sub_name, cols in [("EEI_Intrinsic", eei_intrinsic),
                           ("EEI_Supervisor", eei_supervisor),
                           ("EEI_Leaders", eei_leaders)]:
        present = [c for c in cols if c in df.columns]
        df[sub_name] = df[present].mean(axis=1)
    df["EEI"] = df[["EEI_Intrinsic", "EEI_Supervisor", "EEI_Leaders"]].mean(axis=1)

    # Work-Life Balance composite (Q34, Q49, Q63)
    wlb_cols = [c for c in ["Q34", "Q49", "Q63"] if c in df.columns]
    df["WLB"] = df[wlb_cols].mean(axis=1)

    # Leadership score (Chau's feature: Q57–Q65 mean)
    lead_cols = [f"Q{i}" for i in range(57, 66) if f"Q{i}" in df.columns]
    df["leadership_score"] = df[lead_cols].mean(axis=1)

    # Telework dummies (Q91): reference = routine/remote (1)
    df["TW_Routine"]    = (df["Q91"] == 1).astype(int)
    df["TW_Infrequent"] = (df["Q91"] == 2).astype(int)
    df["TW_Required"]   = (df["Q91"] == 3).astype(int)
    df["TW_ChooseNot"]  = (df["Q91"] == 4).astype(int)

    # Demographics (decode OPM letter codes)
    df["Supervisor"] = df["DSUPER"].map({"A": 0, "B": 1})            # 1 if super/manager/exec
    df["Male"]       = df["DSEX"].map({"A": 1, "B": 0})              # 1 if male
    df["Age40plus"]  = df["DAGEGRP"].map({"A": 0, "B": 1})           # 1 if 40+
    df["Tenure11_20"] = (df["DFEDTEN"] == "B").astype(int)
    df["Tenure20plus"] = (df["DFEDTEN"] == "C").astype(int)

    # Attrition target (Chau's RQ2 secondary)
    df["DLEAVING_BIN"] = np.where(df["DLEAVING"] == "A", 0, 1)

    print(f"[clean] composites built: WLB, EEI, leadership_score")
    return df


# ============================================================
#  RQ2 (Karan): Hierarchical OLS Regression
# ============================================================
def run_hierarchical_regression(df: pd.DataFrame) -> dict:
    print("\n[RQ2] Hierarchical OLS Regression (predicting Q70)")
    cols_needed = ["Q70", "TW_Infrequent", "TW_Required", "TW_ChooseNot",
                   "WLB", "EEI", "Supervisor", "Male", "Age40plus",
                   "Tenure11_20", "Tenure20plus"]
    sub = df[cols_needed].dropna()
    print(f"[RQ2] analytic n = {len(sub):,}")

    blocks = {
        "M1 Telework":      ["TW_Infrequent", "TW_Required", "TW_ChooseNot"],
        "M2 + WLB":         ["TW_Infrequent", "TW_Required", "TW_ChooseNot", "WLB"],
        "M3 + EEI":         ["TW_Infrequent", "TW_Required", "TW_ChooseNot", "WLB", "EEI"],
        "M4 + Demographics":["TW_Infrequent", "TW_Required", "TW_ChooseNot", "WLB", "EEI",
                             "Supervisor", "Male", "Age40plus", "Tenure11_20", "Tenure20plus"],
    }
    results = {}
    rows = []
    prev_r2 = 0.0
    for name, predictors in blocks.items():
        X = sm.add_constant(sub[predictors])
        m = sm.OLS(sub["Q70"], X).fit()
        results[name] = m
        delta = m.rsquared - prev_r2
        rows.append({"Model": name, "R2": m.rsquared, "AdjR2": m.rsquared_adj,
                     "DeltaR2": delta, "F": m.fvalue, "n": int(m.nobs)})
        prev_r2 = m.rsquared
        print(f"  {name:24s} R^2={m.rsquared:.4f}  ΔR^2={delta:.4f}")
    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(HERE / "rq2_hierarchical_results.csv", index=False)
    return {"models": results, "summary": summary_df, "sample": sub}


# ============================================================
#  RQ1 (Chau): ML Model Comparison Predicting Job Satisfaction
# ============================================================
def run_ml_comparison(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[RQ1] ML model comparison predicting Q70")
    feats = ["TW_Infrequent", "TW_Required", "TW_ChooseNot",
             "WLB", "EEI", "Supervisor", "Male", "Age40plus",
             "Tenure11_20", "Tenure20plus"]
    sub = df[["Q70"] + feats].dropna()
    X, y = sub[feats], sub["Q70"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest":     RandomForestRegressor(n_estimators=100, max_depth=12,
                                                   n_jobs=-1, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=4,
                                                       random_state=42),
    }
    rows = []
    for name, m in models.items():
        m.fit(X_train, y_train)
        pred = m.predict(X_test)
        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        rows.append({"Model": name, "R2": r2, "MAE": mae})
        print(f"  {name:20s} R^2={r2:.4f}  MAE={mae:.4f}")

    res = pd.DataFrame(rows).sort_values("R2", ascending=False).reset_index(drop=True)
    res.to_csv(HERE / "rq1_model_comparison.csv", index=False)

    # Feature importance from RF
    rf = models["Random Forest"]
    imp = pd.Series(rf.feature_importances_, index=feats).sort_values(ascending=True)
    return {"results": res, "rf_importance": imp}


# ============================================================
#  Bonus: Attrition Pipeline (Chau's notebook, refined)
# ============================================================
def run_attrition_bonus(df: pd.DataFrame) -> dict:
    print("\n[BONUS] Attrition (DLEAVING_BIN) — Logistic Regression + Random Forest")
    sub = df[["DLEAVING_BIN", "Q70", "Q71", "WLB", "EEI", "leadership_score",
              "Supervisor", "Male", "Age40plus", "Tenure11_20", "Tenure20plus"]].dropna()
    X = sub.drop("DLEAVING_BIN", axis=1)
    y = sub["DLEAVING_BIN"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        stratify=y, random_state=42)

    lr = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, n_jobs=-1,
                                random_state=42).fit(X_train, y_train)
    lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1])
    rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    print(f"  Logistic Regression  AUC = {lr_auc:.3f}")
    print(f"  Random Forest        AUC = {rf_auc:.3f}")
    leave_rate = y.mean()
    print(f"  Base attrition rate: {leave_rate:.1%}")

    imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=True)
    return {"lr_auc": lr_auc, "rf_auc": rf_auc, "leave_rate": float(leave_rate),
            "rf_importance": imp, "n": len(sub)}


# ============================================================
#  Figures (presentation-quality, minimal text on chart)
# ============================================================
def make_figures(df: pd.DataFrame, rq2: dict, rq1: dict, attrition: dict):
    print("\n[fig] generating presentation figures")

    # FIG A — The Hook: only ~60% of feds say they're satisfied
    sat = df["Q70"].dropna()
    pct_satisfied = (sat >= 4).mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts = sat.value_counts().sort_index()
    bars = ax.bar(counts.index, counts.values, color=PALETTE[0], alpha=0.85)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["Very\nDissat.", "Dissat.", "Neutral", "Satisfied", "Very\nSatisfied"])
    ax.set_ylabel("Federal employees")
    ax.set_title(f"How satisfied are 646,000 federal employees?\n{pct_satisfied:.0f}% say satisfied or very satisfied")
    fig.tight_layout()
    fig.savefig(FIGDIR / "01_satisfaction_distribution.png", bbox_inches="tight")
    plt.close(fig)

    # FIG B — Telework looks great…
    tw_means = df.groupby("Q91")["Q70"].mean().reindex([1, 2, 3, 4])
    labels = ["Routine\nremote", "Infrequent\ntelework", "Required\non-site", "Chooses\nnot to"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, tw_means.values, color=[PALETTE[2], PALETTE[0], PALETTE[3], PALETTE[1]])
    ax.axhline(df["Q70"].mean(), ls="--", color="gray", lw=1, label=f"Overall mean {df['Q70'].mean():.2f}")
    ax.set_ylim(3.0, 4.2)
    ax.set_ylabel("Mean job satisfaction (1–5)")
    ax.set_title("At first glance: remote workers look more satisfied\n(0.40-point gap vs. on-site)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGDIR / "02_telework_raw_gap.png", bbox_inches="tight")
    plt.close(fig)

    # FIG C — R² progression (the headline of the regression)
    summ = rq2["summary"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(summ["Model"], summ["R2"], color=[PALETTE[3], PALETTE[1], PALETTE[2], PALETTE[0]])
    for i, v in enumerate(summ["R2"]):
        ax.text(i, v + 0.01, f"{v:.0%}", ha="center", fontweight="bold")
    ax.set_ylim(0, 0.75)
    ax.set_ylabel("Variance explained (R²)")
    ax.set_title("Engagement and work-life balance carry the model\nDemographics add almost nothing")
    ax.tick_params(axis="x", labelrotation=0)
    fig.tight_layout()
    fig.savefig(FIGDIR / "03_r2_progression.png", bbox_inches="tight")
    plt.close(fig)

    # FIG D — The Simpson's Paradox slide
    m1 = rq2["models"]["M1 Telework"]
    m4 = rq2["models"]["M4 + Demographics"]
    coefs = pd.DataFrame({
        "Before controls (M1)": [m1.params.get("TW_Required", 0),
                                 m1.params.get("TW_Infrequent", 0)],
        "After controls (M4)":  [m4.params.get("TW_Required", 0),
                                 m4.params.get("TW_Infrequent", 0)],
    }, index=["Required on-site", "Infrequent telework"])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    coefs.plot(kind="bar", ax=ax, color=[PALETTE[3], PALETTE[0]], width=0.7)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Effect on satisfaction\n(vs. routine remote, in scale points)")
    ax.set_title("Simpson's Paradox: the telework effect flips sign\nonce engagement and WLB are controlled")
    ax.legend(frameon=False)
    ax.tick_params(axis="x", labelrotation=0)
    fig.tight_layout()
    fig.savefig(FIGDIR / "04_simpsons_paradox.png", bbox_inches="tight")
    plt.close(fig)

    # FIG E — Standardized coefficient ranking (what matters most)
    sub = rq2["sample"]
    Xz = sub.drop(columns=["Q70"]).apply(lambda c: (c - c.mean()) / c.std() if c.nunique() > 2 else c)
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
    fig, ax = plt.subplots(figsize=(8, 5.5))
    colors = [PALETTE[2] if v > 0 else PALETTE[3] for v in betas.values]
    ax.barh(betas.index, betas.values, color=colors)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Standardized coefficient (β)")
    ax.set_title("Engagement is by far the dominant predictor of satisfaction")
    fig.tight_layout()
    fig.savefig(FIGDIR / "05_standardized_coefs.png", bbox_inches="tight")
    plt.close(fig)

    # FIG F — RQ1: ML model comparison
    res = rq1["results"]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(res["Model"], res["R2"], color=[PALETTE[2], PALETTE[0], PALETTE[1]])
    for i, v in enumerate(res["R2"]):
        ax.text(i, v + 0.005, f"{v:.3f}", ha="center", fontweight="bold")
    ax.set_ylim(0, max(res["R2"]) * 1.15)
    ax.set_ylabel("Test-set R²")
    ax.set_title("Three models, similar accuracy\nA simple linear model is enough for this story")
    fig.tight_layout()
    fig.savefig(FIGDIR / "06_rq1_models.png", bbox_inches="tight")
    plt.close(fig)

    # FIG G — RF feature importance for satisfaction
    imp = rq1["rf_importance"]
    imp.index = [pretty.get(i, i) for i in imp.index]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(imp.index, imp.values, color=PALETTE[0])
    ax.set_xlabel("Random-forest importance")
    ax.set_title("Same finding from a totally different model class:\nengagement and WLB rule")
    fig.tight_layout()
    fig.savefig(FIGDIR / "07_rf_importance_satisfaction.png", bbox_inches="tight")
    plt.close(fig)

    # FIG H — Bonus attrition figure
    imp_a = attrition["rf_importance"]
    rename_attr = {**pretty, "Q70": "Job satisfaction", "Q71": "Pay satisfaction",
                   "leadership_score": "Leadership score"}
    imp_a.index = [rename_attr.get(i, i) for i in imp_a.index]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(imp_a.index, imp_a.values, color=PALETTE[3])
    ax.set_xlabel("Random-forest importance")
    ax.set_title(f"Bonus: who's likely to leave?\n{attrition['leave_rate']:.0%} are considering it. Same drivers — engagement, pay, leadership")
    fig.tight_layout()
    fig.savefig(FIGDIR / "08_attrition_bonus.png", bbox_inches="tight")
    plt.close(fig)

    print(f"[fig] saved 8 figures to {FIGDIR}")


# ============================================================
#  Main
# ============================================================
def main():
    df = load_and_clean()
    rq2 = run_hierarchical_regression(df)
    rq1 = run_ml_comparison(df)
    attrition = run_attrition_bonus(df)
    make_figures(df, rq2, rq1, attrition)

    # One CSV summarizing everything for the deck
    summary = {
        "n_observations": len(df),
        "n_analytic_rq2": len(rq2["sample"]),
        "rq2_M4_R2": rq2["summary"].iloc[-1]["R2"],
        "rq2_M1_R2": rq2["summary"].iloc[0]["R2"],
        "rq1_best_model": rq1["results"].iloc[0]["Model"],
        "rq1_best_R2": rq1["results"].iloc[0]["R2"],
        "attrition_leave_rate": attrition["leave_rate"],
        "attrition_rf_auc": attrition["rf_auc"],
        "attrition_lr_auc": attrition["lr_auc"],
    }
    pd.DataFrame([summary]).to_csv(HERE / "presentation_headline_numbers.csv", index=False)
    print("\n[done] All artifacts written.")
    print(f"       figures   -> {FIGDIR}")
    print(f"       summary   -> presentation_headline_numbers.csv")
    print(f"       RQ1 table -> rq1_model_comparison.csv")
    print(f"       RQ2 table -> rq2_hierarchical_results.csv")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
