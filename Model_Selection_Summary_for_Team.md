# ADTA 5940 Capstone — Model Selection Summary
### Prepared: March 19, 2026 | Team: Karan Parekh & Chau Lee

---

## 1. What We Did

We ran a **comprehensive model comparison** to find the best machine learning model for predicting **federal employee job satisfaction** (FEVS survey question Q69, scored 1–5) using the 2024 OPM Federal Employee Viewpoint Survey (FEVS) dataset.

- **Dataset:** 674,207 survey responses, 96 columns
- **After cleaning (listwise deletion):** 453,082 usable rows
- **Train/Test split:** 80% training (362,465) / 20% testing (90,617)
- **Target variable:** Q69 — "Considering everything, how satisfied are you with your job?" (1 = Very Dissatisfied → 5 = Very Satisfied, mean = 3.626)

### Features Used (7 total)

| Feature | Description | Type |
|---------|-------------|------|
| Q61 | Telework frequency (1–5 scale) | Survey item |
| Q64 | Work-life balance satisfaction (1–5 scale) | Survey item |
| EEI | Employee Engagement Index — composite mean of Q3, Q4, Q6, Q11–Q14 | Composite |
| DAGEGRP | Age group (0 = Under 40, 1 = 40+) | Demographic |
| DSEX | Gender (0 = Male, 1 = Female) | Demographic |
| DSUPER | Supervisory status (0 = Non-supervisor, 1 = Supervisor) | Demographic |
| DFEDTEN | Federal tenure (0 = <10yr, 1 = 10–20yr, 2 = 20+yr) | Demographic |

---

## 2. All 14 Models Tested — Full Results

| Rank | Model | R² (Test) | R² (Train) | MAE | RMSE | CV R² Mean | CV R² Std | Train Time |
|------|-------|-----------|------------|-----|------|------------|-----------|------------|
| **1** | **XGBoost** | **0.5322** | 0.5339 | **0.6056** | **0.8016** | 0.5241 | **0.0031** | 2.69s |
| 2 | LightGBM | 0.5322 | 0.5337 | 0.6057 | 0.8015 | 0.5243 | 0.0058 | **0.38s** |
| 3 | Gradient Boosting | 0.5321 | 0.5340 | 0.6057 | 0.8016 | 0.5239 | 0.0104 | 18.05s |
| 4 | Extra Trees | 0.5308 | 0.5369 | 0.6074 | 0.8027 | 0.5230 | 0.0127 | 2.27s |
| 5 | Random Forest | 0.5307 | 0.5374 | 0.6063 | 0.8028 | 0.5142 | 0.0042 | 3.13s |
| 6 | Decision Tree | 0.5287 | 0.5357 | 0.6072 | 0.8045 | 0.5079 | 0.0053 | 0.21s |
| 7 | MLP Neural Net | 0.5259 | 0.5343 | 0.6202 | 0.8070 | 0.5268 | 0.0090 | 2.42s |
| 8 | Linear Regression | 0.5254 | 0.5243 | 0.6172 | 0.8073 | 0.5242 | 0.0034 | 0.06s |
| 9 | Ridge Regression | 0.5254 | 0.5243 | 0.6172 | 0.8073 | 0.5230 | 0.0052 | 0.05s |
| 10 | Elastic Net | 0.5253 | 0.5242 | 0.6184 | 0.8075 | 0.5280 | 0.0061 | 0.04s |
| 11 | Lasso Regression | 0.5250 | 0.5240 | 0.6192 | 0.8077 | 0.5194 | 0.0034 | 0.06s |
| 12 | Bagging | 0.5138 | 0.5522 | 0.6136 | 0.8172 | 0.4706 | 0.0082 | 2.44s |
| 13 | AdaBoost | 0.4703 | 0.4697 | 0.6945 | 0.8530 | 0.4727 | 0.0093 | 2.45s |
| 14 | KNN | 0.4689 | 0.5512 | 0.6425 | 0.8540 | 0.4657 | 0.0064 | 0.03s |

### Key Metrics Explained
- **R² (Test):** How much variance in job satisfaction the model explains on unseen data (higher = better, max 1.0)
- **MAE:** Average error in predicted satisfaction score (lower = better, in points on the 1–5 scale)
- **RMSE:** Root mean squared error — penalizes large errors more (lower = better)
- **CV R² Mean ± Std:** Average R² across 5-fold cross-validation — shows how stable the model is across different data splits

---

## 3. Our Chosen Model: LightGBM

### Why LightGBM?

We tested 14 models and the top 3 (XGBoost, LightGBM, Gradient Boosting) are **statistically identical** (paired t-test p = 0.944). We selected LightGBM for these reasons:

| Criteria | LightGBM Performance | Assessment |
|----------|---------------------|------------|
| **Test R²** | 0.5322 | Tied best — explains 53.2% of variance |
| **MAE** | 0.6057 | Excellent — predictions off by ~0.6 points on average |
| **RMSE** | 0.8015 | **Best RMSE** of all 14 models |
| **CV R² Mean** | 0.5243 | **Highest CV mean** among top 5 — best generalization |
| **CV R² Std** | ± 0.0058 | Good stability across folds |
| **Train vs Test R²** | 0.5337 vs 0.5322 | Minimal gap — **no overfitting** |
| **Training Speed** | **0.38 seconds** | **Fastest** of all ensemble models (7x faster than XGBoost) |

### What does R² = 0.53 mean in plain English?
Our model explains **53% of the variation** in how satisfied federal employees are with their jobs, using just 7 features. The other 47% comes from factors we don't have data on (e.g., pay, manager quality, office culture, personal factors). For social science survey data with ordinal Likert-scale responses, this is a **strong result**.

### LightGBM Configuration (Default was optimal)
```
n_estimators = 100
max_depth = 5
learning_rate = 0.1
random_state = 42
verbose = -1
```
Hyperparameter tuning across 20 configurations showed the defaults were already near-optimal (tuned R² = 0.5296 — actually slightly lower, confirming defaults are fine).

---

## 4. Feature Importance — What Drives Job Satisfaction?

This is the **most important finding for our capstone**:

| Feature | Importance (LightGBM) | What It Means |
|---------|----------------------|---------------|
| **EEI — Employee Engagement** | **34.4%** | Engagement (feeling valued, having purpose, seeing results) is the strongest driver. |
| **Q61 — Telework Frequency** | **21.2%** | Telework frequency is the second strongest predictor — employees with more telework are more satisfied. |
| **Q64 — Work-Life Balance** | **18.9%** | WLB satisfaction is the third strongest driver. |
| DFEDTEN — Federal Tenure | 10.4% | Some contribution — longer-tenured employees show different patterns. |
| DSUPER — Supervisory Status | 5.8% | Minor contribution. |
| DSEX — Gender | 4.9% | Minor contribution. |
| DAGEGRP — Age Group | 4.5% | Minor contribution. |

### Key Takeaway for the Report
> **The three workplace experience variables (engagement, telework, work-life balance) account for 74.5% of LightGBM's predictive power, while demographics account for 25.5%.** This indicates that job satisfaction in the federal workforce is driven primarily by how employees *experience* their work — their engagement, telework flexibility, and work-life balance — rather than individual demographic characteristics. This supports the literature on intrinsic vs. extrinsic satisfaction factors.

### Average Importance Across All Top 5 Models
Even across different model types (XGBoost, LightGBM, Gradient Boosting, Extra Trees, Random Forest), the pattern is consistent:
- **EEI:** 44.1% average
- **Q64 (WLB):** 33.8% average
- **Q61 (Telework):** 16.4% average
- **All demographics combined:** < 6% average

---

## 5. Statistical Significance Tests

We ran paired t-tests to check if the top models are truly different or just noise:

| Comparison | p-value | Significant? |
|-----------|---------|--------------|
| XGBoost vs LightGBM | 0.944 | No — essentially identical |
| XGBoost vs Gradient Boosting | 0.968 | No — essentially identical |
| XGBoost vs Extra Trees | 0.874 | No |
| XGBoost vs Random Forest | **0.027** | **Yes** — XGBoost is significantly better than Random Forest in CV |
| LightGBM vs Gradient Boosting | 0.953 | No |
| LightGBM vs Extra Trees | 0.825 | No |
| LightGBM vs Random Forest | 0.080 | No (borderline) |

**Bottom line:** The top 3 models (XGBoost, LightGBM, Gradient Boosting) perform statistically the same. XGBoost is chosen for its superior stability (lowest CV variance) and strong interpretability via feature importances.

---

## 6. Correlation Matrix Findings

Bivariate correlations between features and job satisfaction (Q69):

| Feature | Correlation with Q69 |
|---------|---------------------|
| EEI (Engagement) | **0.647** — strong positive |
| Q64 (Work-Life Balance) | **0.634** — strong positive |
| Q61 (Telework) | **0.603** — strong positive |
| DSUPER (Supervisor) | 0.058 — negligible |
| DAGEGRP (Age) | 0.047 — negligible |
| DFEDTEN (Tenure) | 0.016 — negligible |
| DSEX (Gender) | -0.011 — negligible |

Note: Q61, Q64, and EEI are also correlated with each other (r = 0.59–0.68), which is expected since engaged employees with telework also tend to report better WLB.

---

## 7. How to Proceed — Next Steps

### For Module 5 (Final Model & Report)
1. **Primary model: LightGBM** — Use this for all final predictions and analysis
2. **Baseline model: Linear Regression** — Include this for comparison and interpretability (OLS coefficients are easier to explain)
3. **Report the model comparison** — We tested 14 models and can show why LightGBM was selected
4. **Focus the discussion on feature importances** — This is where the research value is. The finding that engagement, telework, and WLB dominate is a strong capstone conclusion

### For the Written Report
- We have the **hierarchical OLS regression** from Module 4 (for the traditional statistical approach)
- We now have the **ML model comparison** showing tree-based ensemble models perform best
- Together, these two approaches provide a **comprehensive analysis**: statistical inference (OLS) + predictive modeling (XGBoost)

### What's Saved and Where
All files are in `C:\Users\karan\Downloads\ADTA5940-Capstone\`:

| File | Description |
|------|-------------|
| `Model_Comparison_Analysis.ipynb` | Complete Jupyter notebook with all code, charts, and analysis |
| `model_comparison_results.csv` | Full 14-model comparison table |
| `significance_tests.csv` | Paired t-test results |
| `tuning_results.csv` | Hyperparameter tuning attempts |
| `feature_importances.csv` | Feature importances for all top 5 models |
| `test_predictions.csv` | Actual vs. predicted values on test set |
| `cv_fold_scores.csv` | Individual cross-validation fold scores |
| `saved_models/lightgbm.joblib` | Trained LightGBM model (ready to use) |
| `saved_models/scaler.joblib` | StandardScaler used for feature normalization |
| `figures/` folder | All visualization PNGs (correlation matrix, R² comparison, CV boxplots, scatter plots, residuals, training time, feature importances, final ranking) |

---

## 8. One-Paragraph Summary (for the report)

> We evaluated 14 regression models on the 2024 Federal Employee Viewpoint Survey (N = 453,082) to predict overall job satisfaction (Q69). After training and testing via 80/20 split with 5-fold cross-validation, the top 5 models were all ensemble tree-based methods: XGBoost (R² = 0.532), LightGBM (R² = 0.532), Gradient Boosting (R² = 0.532), Extra Trees (R² = 0.531), and Random Forest (R² = 0.531). Paired t-tests confirmed the top 3 models are statistically indistinguishable (p = 0.944). We selected LightGBM as the primary model due to its identical accuracy, highest cross-validation mean R² (0.5243), best RMSE (0.8015), and fastest training time (0.38s — 7x faster than XGBoost). Feature importance analysis revealed that employee engagement (34.4%), telework frequency (21.2%), and work-life balance satisfaction (18.9%) account for 74.5% of the model's predictive power. While demographic variables show some contribution in LightGBM's split-based importance, the three core workplace experience factors clearly dominate, indicating that job satisfaction in the federal workforce is driven primarily by how employees experience their work rather than individual demographic characteristics.

---

*Generated from Model_Comparison_Analysis.ipynb — all code, data, and visualizations are reproducible.*
