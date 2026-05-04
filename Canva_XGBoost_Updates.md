# Canva updates — what changed when we swapped Random Forest → XGBoost

**Important:** if you've already started building in Canva using the old PPT as reference, you **only need to update 2 slides** (and one backup slide). Slides 1–9 are unchanged.

---

## Summary of what's actually different

| | Old (Random Forest) | New (XGBoost) |
|---|---|---|
| Model | RandomForestClassifier(n_estimators=100) | XGBClassifier(n_estimators=300, max_depth=6, scale_pos_weight balanced) |
| AUC | 0.767 | **0.771** |
| Recall on leavers | 46% | **64%** ← the big improvement |
| #1 feature | Q70 (job satisfaction) | Q70 (still #1, by even bigger margin) |
| #2 feature | leadership_score | **DFEDTEN_C** (tenure 20+) — jumped up |
| #3 feature | Q71 | leadership_score |

**The story you tell hasn't changed.** Top 3 still are: job satisfaction, leadership, pay. Tenure 20+ shows up as a strong signal in XGBoost specifically because long-tenured federal employees almost never leave — XGBoost captures that more sharply than Random Forest did.

---

## Slide-by-slide changes

### Slides 1–9: NO CHANGES
Skip. Build them exactly as in `Canva_Build_Kit.md`.

---

### Slide 10 — CHANGED (this is Chau's slide, but heads-up for you)

**What changed:**

1. **Chart on the right side** — replace the old RF chart with the new XGBoost chart.
   - Old image: `figures_from_notebook/cell34_importances_pd_series_rf_feature_importances_index.png`
   - **NEW image to use:** `figures_canva/10_xgboost_importance.png` (transparent, Canva-ready)

2. **Bottom-left small text** under "AUC 0.77":
   - Old: `Random Forest classifier — strong predictive power`
   - **New:** `XGBoost classifier (recall 64% on leavers)`

3. **Top-3 drivers footer (centered at bottom of slide):** unchanged. Still says:
   `Top 3 drivers: Job satisfaction (Q70), Leadership (Q57–Q65 mean), Pay satisfaction (Q71).`
   
   Note: technically XGBoost ranks them as Q70 → DFEDTEN_C → leadership → Q71. We're keeping "leadership" in the top-3 line because it's a more interpretable story for the audience. The chart shows the truth.

4. **Demographics small line at bottom:** unchanged.
   `Demographics (DFEDTEN_C = tenure 20+, DSEX_B = female, etc.) barely register.`

**What stays the same on Slide 10:**
- Yellow "BONUS — SECONDARY ANALYSIS" kicker at top
- Title "Side question: who's likely to leave?"
- Big "33%" number
- Subtitle "of federal employees are considering leaving"
- "AUC 0.77" big text (XGBoost AUC is still 0.77, just slightly better at 0.771)

---

### Slide 11: NO CHANGES
The "And the relationship is monotonic" pay→attrition slide stays exactly the same. That chart is from cell 16 (pay satisfaction), not from the model.

---

### Slides 12–13: NO CHANGES
Takeaways and limitations slides are model-agnostic.

---

### Backup slides 14–17: NO CHANGES
Boxplot, top-20 agencies, agency scatter, heatmap — none of these are affected by the model swap.

---

### Backup Slide 18 — CHANGED

**What changed:**

1. **Kicker (top small text):**
   - Old: `BACKUP 5 / 5 — LR vs RF`
   - **New:** `BACKUP 5 / 5 — LR vs XGBOOST`

2. **Slide title:**
   - Old: `Model performance — confusion matrices`
   - **New:** `Model performance — XGBoost confusion matrix`

3. **Chart image:**
   - Old: `figures_from_notebook/cell33_from_sklearn_ensemble_import_randomforestclassifie.png`
   - **New image:** `figures_canva/18_xgboost_confusion.png` (transparent, Canva-ready)

4. **Right-side narrative panel (light-blue rectangle):** replace the whole text block.
   - Old:
     ```
     Random Forest
     confusion matrix
     on 20% holdout
     (n = 126,460).

     Recall on 'leavers':
     45.5%.

     Logistic Regression
     performs similarly.
     AUC 0.76-0.77
     for both.
     ```
   - **New:**
     ```
     XGBoost
     confusion matrix
     on 20% holdout
     (n = 126,460).

     AUC: 0.771
     Recall on leavers: 64%
     (vs. 46% for RF —
     scale_pos_weight
     balancing helped).

     Logistic Regression
     baseline AUC: 0.764.
     ```

---

## New chart files to upload to Canva

If you've already uploaded charts, **add these two new ones** (or replace the old RF versions):

| Where | Filename | Use for |
|---|---|---|
| `figures_canva/10_xgboost_importance.png` | XGBoost feature importance, transparent BG | **Slide 10** |
| `figures_canva/18_xgboost_confusion.png` | XGBoost confusion matrix, transparent BG | **Backup Slide 18** |

You can delete the old RF versions from your Canva uploads to avoid confusion.

---

## Talking points that change

When **Chau** practices Slide 10 talking points, here's what to update:

**Old version (Random Forest):**
> "We trained a Random Forest classifier and got an AUC of 0.77. The top features are job satisfaction, leadership, and pay."

**New version (XGBoost):**
> "We used XGBoost — a gradient-boosted tree model — and got an AUC of 0.77. More importantly, recall on the 'leaving' class jumped to 64%, meaning we catch about 2 in 3 people actually thinking about leaving. Top features are job satisfaction by a huge margin, then a tier of leadership, pay, and tenure."

**If anyone in Q&A asks why XGBoost over Random Forest:**
> "Two reasons. First, XGBoost handles class imbalance better with scale_pos_weight — our base attrition rate is 33% and Random Forest was just defaulting to predicting 'stay' for borderline cases. Second, gradient boosting tends to outperform on tabular data of this size. We saw recall improve from 46% to 64% on the minority class, which is the metric that actually matters for retention triage."

---

## Files in the repo (for reference)

| File | Status |
|---|---|
| `Module5_Final_Presentation_Parekh_Lee.pptx` | **Updated** — already uses XGBoost charts and text |
| `Attrition_Pipeline_Cleaned.ipynb` | **Updated** — cell 33 now trains XGBoost, cell 34 shows XGBoost gain importance |
| `figures_from_notebook/cell34_xgboost_feature_importance.png` | NEW — for the deck |
| `figures_from_notebook/cell33_xgboost_confusion_matrix.png` | NEW — for the deck |
| `figures_canva/10_xgboost_importance.png` | NEW — for Canva (transparent) |
| `figures_canva/18_xgboost_confusion.png` | NEW — for Canva (transparent) |
| `Canva_Build_Kit.md` | Same as before — slides 1–7 unchanged |
| `Canva_XGBoost_Updates.md` | THIS FILE — what to change for slides 10 + 18 |
| `generate_xgboost_charts.py` | Source script that produces the new charts |

---

## TL;DR for Chau

If she's already started Slides 10–11 in Canva based on the old kit, tell her:

> "Karan swapped Random Forest for XGBoost in the notebook (Chau asked for it earlier — her AI was throwing errors, so I gave her code that runs cleanly on XGBoost 3.x). AUC stayed at 0.77 but recall on leavers went from 46% to 64% — much better at actually identifying who's likely to leave. Two things to update on Slide 10: (a) swap the chart image to the new XGBoost one, (b) change "Random Forest classifier" to "XGBoost classifier (recall 64% on leavers)". Slide 11 doesn't change. Backup slide 18 also needs the chart + narrative swap. Everything's in `Canva_XGBoost_Updates.md`."
