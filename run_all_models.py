"""
FEVS 2024 Model Comparison — Run all models and save results.
This script tests 14 regression models, performs cross-validation,
tunes top models, and saves all results for the notebook.
"""
import pandas as pd
import numpy as np
import time
import warnings
import json
import joblib
import os

from sklearn.model_selection import train_test_split, KFold, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Models
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor,
                              AdaBoostRegressor, ExtraTreesRegressor, BaggingRegressor)
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
import lightgbm as lgb

from scipy import stats

warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# 1. LOAD & PREPROCESS DATA
# ============================================================
print("=" * 60)
print("LOADING DATA")
print("=" * 60)

df = pd.read_csv('C:/Users/karan/Downloads/FEVS/FEVS_2024_PRDF.csv', low_memory=False)
print(f"Raw dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")

# Define variables
# DV: Q69 (Job Satisfaction, 1-5)
# IVs: Q61 (Telework), Q64 (WLB), Engagement items, Demographics

# Engagement Index items (OPM EEI sub-items)
eei_items = ['Q3', 'Q4', 'Q6', 'Q11', 'Q12', 'Q13', 'Q14']

# All feature columns
feature_cols = ['Q61', 'Q64'] + eei_items + ['DAGEGRP', 'DSEX', 'DSUPER', 'DFEDTEN']
target_col = 'Q69'

# Keep only needed columns
cols_needed = feature_cols + [target_col]
df_model = df[cols_needed].copy()

# Convert survey items to numeric (X = not applicable -> NaN)
for col in ['Q61', 'Q64', 'Q69'] + eei_items:
    df_model[col] = pd.to_numeric(df_model[col], errors='coerce')

# Encode demographics
demo_mapping = {
    'DAGEGRP': {'A': 0, 'B': 1},       # A=Under 40, B=40+
    'DSEX': {'A': 0, 'B': 1},          # A=Male, B=Female
    'DSUPER': {'A': 0, 'B': 1},        # A=Non-supervisor, B=Supervisor
    'DFEDTEN': {'A': 0, 'B': 1, 'C': 2}  # A=<10yr, B=10-20yr, C=20+yr
}

for col, mapping in demo_mapping.items():
    df_model[col] = df_model[col].map(mapping)

# Drop rows with any NaN
df_clean = df_model.dropna()
print(f"After cleaning: {df_clean.shape[0]:,} rows (dropped {df.shape[0] - df_clean.shape[0]:,})")

# Create EEI composite
df_clean = df_clean.copy()
df_clean['EEI'] = df_clean[eei_items].mean(axis=1)

# Final features
final_features = ['Q61', 'Q64', 'EEI', 'DAGEGRP', 'DSEX', 'DSUPER', 'DFEDTEN']
X = df_clean[final_features].values
y = df_clean[target_col].values

print(f"\nFinal feature matrix: {X.shape}")
print(f"Target stats: mean={y.mean():.3f}, std={y.std():.3f}, min={y.min()}, max={y.max()}")

# ============================================================
# 2. TRAIN-TEST SPLIT & SCALING
# ============================================================
print("\n" + "=" * 60)
print("TRAIN-TEST SPLIT")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]:,} samples")
print(f"Test set:     {X_test.shape[0]:,} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Use a sample for expensive models (SVR, KNN)
SAMPLE_SIZE = 30000
np.random.seed(42)
sample_idx = np.random.choice(len(X_train_scaled), SAMPLE_SIZE, replace=False)
X_train_sample = X_train_scaled[sample_idx]
y_train_sample = y_train[sample_idx]

# ============================================================
# 3. DEFINE MODELS
# ============================================================
print("\n" + "=" * 60)
print("DEFINING CANDIDATE MODELS")
print("=" * 60)

# Models that work fine on full data
fast_models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=0.01),
    'Elastic Net': ElasticNet(alpha=0.01, l1_ratio=0.5),
    'Decision Tree': DecisionTreeRegressor(max_depth=10, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
    'AdaBoost': AdaBoostRegressor(n_estimators=100, random_state=42),
    'Extra Trees': ExtraTreesRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
    'Bagging': BaggingRegressor(n_estimators=50, random_state=42, n_jobs=-1),
    'XGBoost': xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1,
                                 random_state=42, n_jobs=-1, verbosity=0),
    'LightGBM': lgb.LGBMRegressor(n_estimators=100, max_depth=5, learning_rate=0.1,
                                   random_state=42, n_jobs=-1, verbose=-1),
}

# Models that need sampled data (too slow on 400K+ rows)
slow_models = {
    'KNN': KNeighborsRegressor(n_neighbors=7, n_jobs=-1),
    'MLP Neural Net': MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=200,
                                    random_state=42, early_stopping=True),
}

print(f"Fast models (full data): {len(fast_models)}")
print(f"Slow models (sampled):   {len(slow_models)}")
print(f"Total models to test:    {len(fast_models) + len(slow_models)}")

# ============================================================
# 4. TRAIN & EVALUATE ALL MODELS
# ============================================================
print("\n" + "=" * 60)
print("TRAINING & EVALUATING ALL MODELS")
print("=" * 60)

results = []
cv_scores_dict = {}  # Store CV fold scores for box plots

kf = KFold(n_splits=5, shuffle=True, random_state=42)

def evaluate_model(name, model, X_tr, y_tr, X_te, y_te):
    print(f"\n  Training {name}...", end=" ", flush=True)

    # Time the training
    start = time.time()
    model.fit(X_tr, y_tr)
    train_time = time.time() - start

    # Predictions
    y_pred_train = model.predict(X_tr)
    y_pred_test = model.predict(X_te)

    # Metrics on TEST set
    mae = mean_absolute_error(y_te, y_pred_test)
    mse = mean_squared_error(y_te, y_pred_test)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_te, y_pred_test)

    # Train R² for overfitting check
    r2_train = r2_score(y_tr, y_pred_train)

    # Cross-validation (5-fold) on training data
    # Use a sample for CV if data is large
    if len(X_tr) > 100000:
        cv_idx = np.random.choice(len(X_tr), 50000, replace=False)
        X_cv, y_cv = X_tr[cv_idx], y_tr[cv_idx]
    else:
        X_cv, y_cv = X_tr, y_tr

    cv_r2 = cross_val_score(model, X_cv, y_cv, cv=kf, scoring='r2', n_jobs=-1)
    cv_neg_mae = cross_val_score(model, X_cv, y_cv, cv=kf, scoring='neg_mean_absolute_error', n_jobs=-1)

    cv_scores_dict[name] = cv_r2

    result = {
        'Model': name,
        'R² (Test)': round(r2, 4),
        'R² (Train)': round(r2_train, 4),
        'MAE': round(mae, 4),
        'RMSE': round(rmse, 4),
        'CV R² Mean': round(cv_r2.mean(), 4),
        'CV R² Std': round(cv_r2.std(), 4),
        'CV MAE Mean': round(-cv_neg_mae.mean(), 4),
        'Train Time (s)': round(train_time, 2),
    }

    print(f"R²={r2:.4f}, MAE={mae:.4f}, RMSE={rmse:.4f}, Time={train_time:.1f}s")
    return result, model

# Train fast models on full scaled data
trained_models = {}
for name, model in fast_models.items():
    result, fitted = evaluate_model(name, model, X_train_scaled, y_train, X_test_scaled, y_test)
    results.append(result)
    trained_models[name] = fitted

# Train slow models on sampled data, evaluate on full test
for name, model in slow_models.items():
    result, fitted = evaluate_model(name, model, X_train_sample, y_train_sample, X_test_scaled, y_test)
    result['Model'] = name + ' *'  # Mark as trained on sample
    results.append(result)
    trained_models[name] = fitted

# ============================================================
# 5. RESULTS TABLE
# ============================================================
print("\n" + "=" * 60)
print("MODEL COMPARISON RESULTS")
print("=" * 60)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('R² (Test)', ascending=False).reset_index(drop=True)
results_df.index = results_df.index + 1  # 1-indexed rank

print("\n")
print(results_df.to_string())

# Save results
results_df.to_csv('model_comparison_results.csv', index_label='Rank')
print("\nResults saved to model_comparison_results.csv")

# ============================================================
# 6. IDENTIFY TOP 5 MODELS
# ============================================================
print("\n" + "=" * 60)
print("TOP 5 MODELS")
print("=" * 60)

top5 = results_df.head(5)
for i, row in top5.iterrows():
    print(f"\n  #{i}. {row['Model']}")
    print(f"      R²={row['R² (Test)']:.4f}  MAE={row['MAE']:.4f}  RMSE={row['RMSE']:.4f}  CV R²={row['CV R² Mean']:.4f}±{row['CV R² Std']:.4f}")

top5_names = [n.replace(' *', '') for n in top5['Model'].values]

# ============================================================
# 7. HYPERPARAMETER TUNING FOR TOP 5
# ============================================================
print("\n" + "=" * 60)
print("HYPERPARAMETER TUNING (Top 5 Models)")
print("=" * 60)

param_grids = {
    'Ridge Regression': {
        'alpha': [0.01, 0.1, 1.0, 10.0, 100.0],
    },
    'Lasso Regression': {
        'alpha': [0.001, 0.005, 0.01, 0.05, 0.1],
    },
    'Elastic Net': {
        'alpha': [0.001, 0.01, 0.05, 0.1],
        'l1_ratio': [0.2, 0.5, 0.7, 0.9],
    },
    'Linear Regression': {},  # No hyperparameters
    'Decision Tree': {
        'max_depth': [5, 8, 10, 15, 20],
        'min_samples_split': [10, 50, 100],
        'min_samples_leaf': [5, 20, 50],
    },
    'Random Forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [8, 10, 15, 20],
        'min_samples_split': [10, 50],
        'min_samples_leaf': [5, 20],
    },
    'Gradient Boosting': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'subsample': [0.8, 1.0],
    },
    'AdaBoost': {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.05, 0.1, 0.5, 1.0],
    },
    'Extra Trees': {
        'n_estimators': [100, 200, 300],
        'max_depth': [8, 10, 15, 20],
        'min_samples_split': [10, 50],
    },
    'Bagging': {
        'n_estimators': [50, 100, 200],
        'max_samples': [0.5, 0.7, 1.0],
    },
    'XGBoost': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.7, 0.8, 1.0],
    },
    'LightGBM': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7, -1],
        'learning_rate': [0.01, 0.05, 0.1],
        'num_leaves': [15, 31, 63],
    },
    'KNN': {
        'n_neighbors': [3, 5, 7, 11, 15],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan'],
    },
    'MLP Neural Net': {
        'hidden_layer_sizes': [(64, 32), (128, 64), (64, 32, 16)],
        'alpha': [0.0001, 0.001, 0.01],
        'learning_rate_init': [0.001, 0.01],
    },
}

# Use 50K sample for tuning to keep runtime reasonable
tuning_results = []

for name in top5_names:
    print(f"\n  Tuning {name}...", end=" ", flush=True)

    if name not in param_grids or not param_grids[name]:
        print("No hyperparameters to tune.")
        tuning_results.append({
            'Model': name,
            'Best Params': 'N/A (no hyperparameters)',
            'Best CV R²': results_df[results_df['Model'].str.contains(name.split(' ')[0])]['CV R² Mean'].values[0],
            'Tuned R² (Test)': results_df[results_df['Model'].str.contains(name.split(' ')[0])]['R² (Test)'].values[0],
        })
        continue

    # Recreate model for tuning
    model_templates = {
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Elastic Net': ElasticNet(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'AdaBoost': AdaBoostRegressor(random_state=42),
        'Extra Trees': ExtraTreesRegressor(random_state=42, n_jobs=-1),
        'Bagging': BaggingRegressor(random_state=42, n_jobs=-1),
        'XGBoost': xgb.XGBRegressor(random_state=42, n_jobs=-1, verbosity=0),
        'LightGBM': lgb.LGBMRegressor(random_state=42, n_jobs=-1, verbose=-1),
        'KNN': KNeighborsRegressor(),
        'MLP Neural Net': MLPRegressor(random_state=42, early_stopping=True, max_iter=200),
    }

    base_model = model_templates[name]
    grid = param_grids[name]

    # Use sample for tuning
    search = RandomizedSearchCV(
        base_model, grid, n_iter=min(20, np.prod([len(v) for v in grid.values()])),
        cv=3, scoring='r2', random_state=42, n_jobs=-1
    )

    start = time.time()
    search.fit(X_train_sample, y_train_sample)
    tune_time = time.time() - start

    # Evaluate tuned model on full test set
    y_pred_tuned = search.predict(X_test_scaled)
    tuned_r2 = r2_score(y_test, y_pred_tuned)
    tuned_mae = mean_absolute_error(y_test, y_pred_tuned)

    print(f"Best R²={tuned_r2:.4f}, MAE={tuned_mae:.4f}, Time={tune_time:.1f}s")
    print(f"      Best params: {search.best_params_}")

    tuning_results.append({
        'Model': name,
        'Best Params': str(search.best_params_),
        'Best CV R²': round(search.best_score_, 4),
        'Tuned R² (Test)': round(tuned_r2, 4),
        'Tuned MAE': round(tuned_mae, 4),
    })

    # Save the best model
    trained_models[name + '_tuned'] = search.best_estimator_

tuning_df = pd.DataFrame(tuning_results)
print("\n\nTuning Results:")
print(tuning_df.to_string(index=False))
tuning_df.to_csv('tuning_results.csv', index=False)

# ============================================================
# 8. STATISTICAL SIGNIFICANCE TESTS
# ============================================================
print("\n" + "=" * 60)
print("STATISTICAL SIGNIFICANCE TESTS (Paired t-tests on CV scores)")
print("=" * 60)

top5_cv = {n: cv_scores_dict.get(n, cv_scores_dict.get(n.replace(' *', '')))
           for n in top5_names if n in cv_scores_dict or n.replace(' *', '') in cv_scores_dict}

sig_results = []
names_list = list(top5_cv.keys())
for i in range(len(names_list)):
    for j in range(i + 1, len(names_list)):
        n1, n2 = names_list[i], names_list[j]
        s1, s2 = top5_cv[n1], top5_cv[n2]
        if len(s1) == len(s2):
            t_stat, p_val = stats.ttest_rel(s1, s2)
            sig_results.append({
                'Model A': n1,
                'Model B': n2,
                'Mean Diff': round(s1.mean() - s2.mean(), 4),
                't-statistic': round(t_stat, 3),
                'p-value': round(p_val, 5),
                'Significant (p<0.05)': 'Yes' if p_val < 0.05 else 'No'
            })

sig_df = pd.DataFrame(sig_results)
print(sig_df.to_string(index=False))
sig_df.to_csv('significance_tests.csv', index=False)

# ============================================================
# 9. SAVE CV SCORES FOR PLOTTING
# ============================================================
cv_data = []
for name, scores in cv_scores_dict.items():
    for fold, score in enumerate(scores):
        cv_data.append({'Model': name, 'Fold': fold + 1, 'R²': score})
cv_plot_df = pd.DataFrame(cv_data)
cv_plot_df.to_csv('cv_fold_scores.csv', index=False)

# ============================================================
# 10. FEATURE IMPORTANCES
# ============================================================
print("\n" + "=" * 60)
print("FEATURE IMPORTANCES (Top Models)")
print("=" * 60)

fi_data = []
for name in top5_names:
    model = trained_models.get(name)
    if model is None:
        continue
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        for feat, imp in zip(final_features, importances):
            fi_data.append({'Model': name, 'Feature': feat, 'Importance': round(imp, 4)})
        print(f"\n  {name}:")
        for feat, imp in sorted(zip(final_features, importances), key=lambda x: -x[1]):
            print(f"    {feat:12s}: {imp:.4f}")
    elif hasattr(model, 'coef_'):
        coefs = model.coef_
        for feat, c in zip(final_features, coefs):
            fi_data.append({'Model': name, 'Feature': feat, 'Importance': round(abs(c), 4)})
        print(f"\n  {name} (coefficients):")
        for feat, c in sorted(zip(final_features, coefs), key=lambda x: -abs(x[1])):
            print(f"    {feat:12s}: {c:.4f}")

fi_df = pd.DataFrame(fi_data)
fi_df.to_csv('feature_importances.csv', index=False)

# ============================================================
# 11. SAVE TRAINED MODELS
# ============================================================
print("\n" + "=" * 60)
print("SAVING TOP MODELS")
print("=" * 60)

os.makedirs('saved_models', exist_ok=True)
for name in top5_names:
    safe_name = name.replace(' ', '_').replace('(', '').replace(')', '')
    path = f'saved_models/{safe_name}.joblib'
    model = trained_models.get(name + '_tuned', trained_models.get(name))
    if model:
        joblib.dump(model, path)
        print(f"  Saved {name} -> {path}")

# Save scaler too
joblib.dump(scaler, 'saved_models/scaler.joblib')
print("  Saved scaler -> saved_models/scaler.joblib")

# Save predictions for top models
pred_data = {'Actual': y_test}
for name in top5_names:
    model = trained_models.get(name + '_tuned', trained_models.get(name))
    if model:
        pred_data[name] = model.predict(X_test_scaled)
pred_df = pd.DataFrame(pred_data)
pred_df.to_csv('test_predictions.csv', index=False)

print("\n" + "=" * 60)
print("ALL DONE!")
print("=" * 60)
