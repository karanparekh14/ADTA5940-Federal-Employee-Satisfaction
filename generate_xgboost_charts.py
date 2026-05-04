"""
Generate the XGBoost charts that the deck needs (and Canva-ready transparents).

Outputs:
  figures_from_notebook/cell34_xgboost_feature_importance.png   (deck)
  figures_from_notebook/cell33_xgboost_confusion_matrix.png     (deck, backup)
  figures_canva/10_xgboost_importance.png                        (transparent)
  figures_canva/18_xgboost_confusion.png                         (transparent)
"""
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, confusion_matrix
)

HERE = Path(__file__).resolve().parent
NB_DIR = HERE / "figures_from_notebook"
CANVA_DIR = HERE / "figures_canva"
NB_DIR.mkdir(exist_ok=True)
CANVA_DIR.mkdir(exist_ok=True)

# ---------- Replicate notebook data prep ----------
df = pd.read_csv(HERE / "FEVS_2024_PRDF.csv", low_memory=False)
df = df[df["DLEAVING"].notna()].copy()
df["DLEAVING_BIN"] = np.where(df["DLEAVING"] == "A", 0, 1)

q_cols = [c for c in df.columns if c.startswith("Q")]
df[q_cols] = df[q_cols].apply(pd.to_numeric, errors="coerce")
for c in q_cols:
    df[c] = df[c].fillna(df[c].median())
for c in ["DSEX", "DSUPER", "DFEDTEN", "DAGEGRP"]:
    df[c] = df[c].fillna(df[c].mode()[0])
df["leadership_score"] = df[[f"Q{i}" for i in range(57, 66)]].mean(axis=1)

features = ["Q70", "Q71", "leadership_score",
            "DSEX", "DSUPER", "DFEDTEN", "DAGEGRP"]
X = pd.get_dummies(df[features].copy(), drop_first=True)
y = df["DLEAVING_BIN"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ---------- Train XGBoost ----------
scale_pos_weight = (y_train == 0).sum() / max((y_train == 1).sum(), 1)
clf = xgb.XGBClassifier(
    n_estimators=300, max_depth=6, learning_rate=0.1,
    subsample=0.9, colsample_bytree=0.9,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss", random_state=42,
    n_jobs=-1, tree_method="hist",
)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_prob)
print(f"XGBoost AUC: {auc:.3f}")
print(classification_report(y_test, y_pred))

# ---------- Feature importance (gain-based) ----------
imp = pd.Series(
    clf.get_booster().get_score(importance_type="gain"),
).reindex(X.columns).fillna(0).sort_values(ascending=True)

# Deck version (white background, matches notebook style)
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(imp.index, imp.values, color="#bdb2ff")
ax.set_title("Feature Importance (XGBoost — gain)")
ax.set_xlabel("Average gain per split")
fig.tight_layout()
fig.savefig(NB_DIR / "cell34_xgboost_feature_importance.png", dpi=150,
            bbox_inches="tight")
plt.close(fig)

# Canva version (transparent, larger fonts, navy color)
plt.rcParams.update({
    "savefig.transparent": True, "figure.facecolor": "none",
    "axes.facecolor": "none", "font.size": 14, "axes.titlesize": 18,
    "axes.spines.top": False, "axes.spines.right": False,
})
pretty = {
    "Q70": "Job satisfaction",
    "leadership_score": "Leadership",
    "Q71": "Pay satisfaction",
    "DFEDTEN_C": "Tenure 20+ yrs",
    "DSEX_B": "Female",
    "DSUPER_B": "Supervisor",
    "DFEDTEN_B": "Tenure 11–20 yrs",
    "DAGEGRP_B": "Age 40+",
}
imp_pretty = imp.copy()
imp_pretty.index = [pretty.get(i, i) for i in imp_pretty.index]
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(imp_pretty.index, imp_pretty.values, color="#1E2761", alpha=0.9)
ax.set_xlabel("Gain (XGBoost feature importance)")
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig(CANVA_DIR / "10_xgboost_importance.png", dpi=200,
            bbox_inches="tight", transparent=True)
plt.close(fig)
plt.rcdefaults()

# ---------- Confusion matrix ----------
cm = confusion_matrix(y_test, y_pred)

# Deck version
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", ax=ax,
            xticklabels=[0, 1], yticklabels=[0, 1])
ax.set_title("XGBoost Confusion Matrix")
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
fig.tight_layout()
fig.savefig(NB_DIR / "cell33_xgboost_confusion_matrix.png", dpi=150,
            bbox_inches="tight")
plt.close(fig)

# Canva version
plt.rcParams.update({
    "savefig.transparent": True, "figure.facecolor": "none",
    "axes.facecolor": "none", "font.size": 14, "axes.titlesize": 18,
})
fig, ax = plt.subplots(figsize=(8, 5.5))
sns.heatmap(cm, annot=True, fmt=",d", cmap="Greens", ax=ax,
            xticklabels=["Stay (0)", "Leave (1)"],
            yticklabels=["Stay (0)", "Leave (1)"],
            cbar=False, annot_kws={"fontsize": 18})
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
fig.tight_layout()
fig.savefig(CANVA_DIR / "18_xgboost_confusion.png", dpi=200,
            bbox_inches="tight", transparent=True)
plt.close(fig)
plt.rcdefaults()

print("\nSaved:")
print(f"  Deck:  {NB_DIR/'cell34_xgboost_feature_importance.png'}")
print(f"  Deck:  {NB_DIR/'cell33_xgboost_confusion_matrix.png'}")
print(f"  Canva: {CANVA_DIR/'10_xgboost_importance.png'}  (transparent)")
print(f"  Canva: {CANVA_DIR/'18_xgboost_confusion.png'}  (transparent)")
print(f"\nAUC: {auc:.3f}  ·  recall on leavers: {(cm[1,1]/cm[1].sum()):.0%}")
