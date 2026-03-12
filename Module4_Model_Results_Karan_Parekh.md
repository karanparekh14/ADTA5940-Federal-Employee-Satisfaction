# Module 4: Model with Results

## Remote Work, Work-Life Balance, and Federal Employee Job Satisfaction: A Hierarchical Regression Analysis

**Karan Parekh**
**ADTA 5940 — Analytics Capstone Experience**
**University of North Texas | Spring 2026**

---

## 1. Research Question

This analysis investigates the following research question:

> **To what extent does telework frequency predict overall job satisfaction among federal employees, after accounting for work-life balance perceptions, employee engagement, and demographic characteristics?**

Building on the exploratory data analysis presented previously, this study moves from descriptive patterns to a formal inferential model. The research question is motivated by two observations from the EDA: (1) federal employees who telework routinely report higher raw satisfaction than those required to work on-site, and (2) work-life balance perceptions and employee engagement are strongly correlated with satisfaction. The analytic challenge is to disentangle the *independent* contribution of telework arrangement from these correlated attitudinal factors.

Three hypotheses guide the analysis:

- **H1:** Telework frequency is a statistically significant predictor of job satisfaction. Specifically, employees who telework routinely or remotely will report higher satisfaction than those required to work in the office.
- **H2:** Work-life balance perceptions and employee engagement each explain substantial additional variance in job satisfaction beyond telework arrangement alone.
- **H3:** After controlling for work-life balance and engagement, the magnitude of the telework effect on job satisfaction will be substantially reduced, suggesting that these attitudinal variables partially mediate the telework–satisfaction relationship.

---

## 2. Formal Model

### 2.1 Model Specification

A **hierarchical (blockwise) ordinary least squares (OLS) multiple regression** is employed to assess the incremental explanatory power of each set of predictors. The dependent variable is overall job satisfaction (Q70), measured on a 1–5 Likert scale (1 = Very Dissatisfied, 5 = Very Satisfied). Four nested models are estimated:

**Model 1 (Telework Only):**

$$\text{Satisfaction}_i = \beta_0 + \beta_1 \text{TW\_Infrequent}_i + \beta_2 \text{TW\_Required}_i + \beta_3 \text{TW\_ChooseNot}_i + \varepsilon_i$$

**Model 2 (+ Work-Life Balance):**

$$\text{Satisfaction}_i = \beta_0 + \beta_1 \text{TW\_Infrequent}_i + \beta_2 \text{TW\_Required}_i + \beta_3 \text{TW\_ChooseNot}_i + \beta_4 \text{WLB\_Composite}_i + \varepsilon_i$$

**Model 3 (+ Employee Engagement):**

$$\text{Satisfaction}_i = \beta_0 + \cdots + \beta_4 \text{WLB\_Composite}_i + \beta_5 \text{EEI}_i + \varepsilon_i$$

**Model 4 (Full Model with Demographics):**

$$\text{Satisfaction}_i = \beta_0 + \cdots + \beta_5 \text{EEI}_i + \beta_6 \text{Supervisor}_i + \beta_7 \text{Male}_i + \beta_8 \text{Age40+}_i + \beta_9 \text{Tenure11\text{-}20}_i + \beta_{10} \text{Tenure20+}_i + \varepsilon_i$$

### 2.2 Variable Definitions

| Variable | Measurement | Source |
|----------|------------|--------|
| **Job Satisfaction** (DV) | Q70: "Considering everything, how satisfied are you with your job?" (1–5 Likert) | FEVS 2024 |
| **TW_Infrequent** | = 1 if respondent teleworks situationally/infrequently; 0 otherwise | Q91 = 2 |
| **TW_Required** | = 1 if respondent is required to work in the office (does not telework); 0 otherwise | Q91 = 3 |
| **TW_ChooseNot** | = 1 if respondent chooses not to telework; 0 otherwise | Q91 = 4 |
| *Reference group* | Routine telework / full-time remote work | Q91 = 1 |
| **WLB_Composite** | Mean of Q34 (peer support for work-life balance), Q49 (supervisor supports work-life balance), Q63 (senior leaders support work-life programs); range 1–5 | Computed |
| **EEI** | Employee Engagement Index: mean of three OPM subindices (Intrinsic Work Experience, Supervisor, Leaders Lead), each a 5-item mean; range 1–5 | OPM formula |
| **Supervisor** | = 1 if Supervisor/Manager/Executive; 0 if Non-Supervisor/Team Leader | DSUPER |
| **Male** | = 1 if Male; 0 if Female | DSEX |
| **Age 40+** | = 1 if age 40 or older; 0 if under 40 | DAGEGRP |
| **Tenure 11–20** | = 1 if federal tenure 11–20 years; 0 otherwise (reference: ≤10 yrs) | DFEDTEN |
| **Tenure 20+** | = 1 if federal tenure more than 20 years; 0 otherwise | DFEDTEN |

### 2.3 Analytic Approach

The hierarchical regression strategy allows assessment of each variable block's *incremental* contribution to explained variance. Block 1 establishes the baseline telework effect. Block 2 adds an attitudinal mediator (work-life balance). Block 3 adds the Employee Engagement Index. Block 4 introduces demographic controls. The incremental *R²* change and *F*-change at each step are tested for statistical significance.

The analytic sample consists of *n* = 517,697 respondents with complete data across all model variables (listwise deletion). Models are first estimated with conventional OLS standard errors; given the large sample size, heteroscedasticity-consistent (HC3) robust standard errors are also reported to confirm the robustness of inferences.

---

## 3. Results

### 3.1 Descriptive Overview

Table 1 presents descriptive statistics for the continuous model variables. Mean job satisfaction is 3.82 on the 5-point scale (*SD* = 1.09), indicating that the average federal employee falls between "Neither" and "Satisfied." Both the Work-Life Balance composite (*M* = 4.02) and the Employee Engagement Index (*M* = 3.95) are well above the scale midpoint, reflecting generally positive perceptions among respondents.

**Table 1. Descriptive Statistics for Continuous Model Variables (*N* = 646,545)**

| Variable | Mean | SD | Min | Max |
|----------|-----:|---:|----:|----:|
| Job Satisfaction (Q70) | 3.815 | 1.088 | 1.0 | 5.0 |
| Work-Life Balance Composite | 4.018 | 0.898 | 1.0 | 5.0 |
| Employee Engagement Index | 3.951 | 0.817 | 1.0 | 5.0 |
| EEI — Intrinsic Work Experience | 3.941 | 0.861 | 1.0 | 5.0 |
| EEI — Supervisor | 4.244 | 0.931 | 1.0 | 5.0 |
| EEI — Leaders Lead | 3.669 | 1.041 | 1.0 | 5.0 |

The telework distribution shows that 42.8% of respondents telework routinely or work remotely, 33.6% telework situationally, 19.7% are required to work on-site, and 3.8% choose not to telework. Raw group means confirm a substantial satisfaction gap: routine teleworkers average 3.94 versus 3.54 for those required to be on-site — a difference of 0.40 points on the 5-point scale (see Figure 1). A one-way ANOVA confirmed this difference is statistically significant, *F*(3, 639,584) = 4,046.84, *p* < .001, though the effect size is small (η² = 0.019).

### 3.2 Hierarchical Regression Results

Table 2 summarizes the model-fit statistics across the four regression steps. The progression of *R²* reveals a clear story about what matters most for federal employee job satisfaction.

**Table 2. Model Comparison — Hierarchical Regression (*n* = 517,697)**

| Metric | Model 1 | Model 2 | Model 3 | Model 4 |
|--------|--------:|--------:|--------:|--------:|
| Block added | Telework | + WLB | + EEI | + Demographics |
| *R²* | .0200 | .4091 | .5945 | .5966 |
| Adj. *R²* | .0200 | .4091 | .5945 | .5966 |
| Δ*R²* | — | .3891 | .1854 | .0021 |
| *F* | 3,516.10 | 89,600.50 | 151,801.68 | 76,564.48 |
| Δ*F* | — | 340,907.51*** | 236,722.43*** | 538.79*** |
| Cohen's *f²* | 0.020 (small) | 0.692 (large) | 1.466 (large) | 1.479 (large) |

*Note.* All Δ*F* tests significant at *p* < .001.

**Key observations from the model progression:**

1. **Telework alone explains only 2.0% of variance** in job satisfaction (Model 1). While statistically significant, the practical effect is small (*f²* = 0.020).

2. **Adding Work-Life Balance increases *R²* by 38.9 percentage points** (Model 2, *R²* = .409). This is the single largest increment, confirming that employees' perceptions of organizational support for balancing work and personal life are far more predictive of satisfaction than telework arrangement alone. The incremental *f²* = 0.659 indicates a large effect.

3. **Adding Employee Engagement increases *R²* by another 18.5 percentage points** (Model 3, *R²* = .595). Together, WLB and EEI account for nearly 60% of variance in satisfaction — a substantial explanatory model. The incremental *f²* = 0.457 is also a large effect.

4. **Demographics add only 0.2 percentage points** (Model 4, *R²* = .597). While statistically significant due to the large sample, the practical contribution of age, sex, supervisory status, and tenure is negligible (*f²* = 0.005).

### 3.3 Full Model Coefficients

Table 3 presents the estimated coefficients for the full model (Model 4). Standardized coefficients (β) are included to enable comparison of relative predictor importance.

**Table 3. OLS Regression Coefficients — Full Model (Model 4)**

| Predictor | *B* | *SE* | β | *t* | *p* | 95% CI |
|-----------|----:|-----:|--:|----:|----:|--------|
| Intercept | −0.469 | 0.006 | — | −82.60 | < .001 | [−0.480, −0.458] |
| TW: Infrequent (vs. Routine/Remote) | −0.002 | 0.002 | −0.001 | −0.98 | .326 | [−0.007, 0.002] |
| TW: Required in Office (vs. Routine/Remote) | 0.114 | 0.003 | 0.043 | 42.19 | < .001 | [0.109, 0.119] |
| TW: Chooses Not To (vs. Routine/Remote) | 0.090 | 0.005 | 0.016 | 17.72 | < .001 | [0.080, 0.099] |
| Work-Life Balance Composite | 0.111 | 0.002 | 0.091 | 62.39 | < .001 | [0.107, 0.114] |
| **Employee Engagement Index** | **0.945** | **0.002** | **0.705** | **487.21** | **< .001** | **[0.941, 0.949]** |
| Supervisor (vs. Non-Supervisor) | −0.019 | 0.003 | −0.007 | −7.77 | < .001 | [−0.024, −0.015] |
| Male (vs. Female) | 0.018 | 0.002 | 0.009 | 9.44 | < .001 | [0.015, 0.022] |
| Age 40+ (vs. Under 40) | 0.088 | 0.003 | 0.036 | 35.24 | < .001 | [0.083, 0.093] |
| Tenure 11–20 yrs (vs. ≤10) | −0.002 | 0.002 | −0.001 | −0.62 | .536 | [−0.006, 0.003] |
| Tenure 20+ yrs (vs. ≤10) | 0.049 | 0.003 | 0.020 | 18.09 | < .001 | [0.044, 0.055] |

*Note.* *n* = 517,697. *R²* = .5966, Adjusted *R²* = .5966, *F*(10, 517686) = 76,564.48, *p* < .001. Robust (HC3) standard errors were also computed; all significance conclusions remained unchanged.

**Interpretation of key coefficients:**

- **Employee Engagement Index (β = 0.705):** By far the dominant predictor. A one-unit increase in EEI is associated with a 0.945-point increase in satisfaction, holding all else constant. This single variable contributes the bulk of the model's explanatory power.

- **Work-Life Balance Composite (β = 0.091):** A one-unit increase in perceived work-life balance support corresponds to a 0.111-point increase in satisfaction. While much smaller than EEI, this is the second-largest standardized effect and confirms the importance of organizational WLB policies.

- **Telework — Critical reversal:** In Model 1 (unadjusted), employees required to work in the office scored 0.407 points *lower* than routine teleworkers. However, in the full model, the coefficient *reverses* to +0.114 (*p* < .001). This indicates that the raw satisfaction gap is not attributable to the office arrangement itself, but rather to differences in engagement and perceived work-life balance support between groups. After equalizing these attitudinal factors, required-in-office employees are slightly *more* satisfied — possibly reflecting self-selection or alignment between certain roles and in-person preferences.

- **Infrequent telework** shows no significant difference from routine telework once WLB and EEI are controlled (*B* = −0.002, *p* = .326).

- **Demographics** have statistically significant but practically negligible effects. Older employees (β = 0.036) and those with 20+ years of tenure (β = 0.020) report marginally higher satisfaction. Supervisors report slightly lower satisfaction (β = −0.007), possibly reflecting added workload responsibilities.

### 3.4 Telework Coefficient Progression Across Models

Table 4 illustrates how the telework coefficients change as additional controls are introduced — providing direct evidence of confounding and partial mediation.

**Table 4. Telework Coefficients Across Models**

| Predictor | Model 1 | Model 2 | Model 3 | Model 4 |
|-----------|--------:|--------:|--------:|--------:|
| TW: Infrequent | −0.121*** | 0.013*** | −0.002 | −0.002 |
| TW: Required in Office | −0.407*** | 0.094*** | 0.109*** | 0.114*** |
| TW: Chooses Not To | −0.029*** | 0.127*** | 0.096*** | 0.089*** |

The dramatic sign reversal for the "Required in Office" coefficient — from −0.407 in Model 1 to +0.094 in Model 2 and +0.114 in Model 4 — constitutes a classic case of **Simpson's Paradox** (or confounding). In-office employees systematically report lower WLB support and engagement, which drives their lower raw satisfaction, not the physical work arrangement per se.

### 3.5 Model Diagnostics

The following diagnostics were assessed for the full model:

- **Multicollinearity:** Variance Inflation Factors were below 5 for all demographic and telework indicators (range 1.09–4.91). However, WLB Composite (VIF = 56.74) and EEI (VIF = 58.65) show high multicollinearity, reflecting the strong conceptual overlap between engagement and work-life balance constructs. While this inflates individual standard errors for these two predictors, it does not affect overall model *R²* or the significance pattern of other variables. The substantive conclusion about their combined importance holds.

- **Independence of errors:** Durbin-Watson = 1.989, indicating no autocorrelation in residuals (expected with cross-sectional survey data).

- **Heteroscedasticity:** The Breusch-Pagan test was significant (χ² = 29,938.87, *p* < .001), indicating non-constant variance. HC3 robust standard errors were computed; all significance conclusions were identical to conventional OLS estimates.

- **Normality:** Residuals show mild negative skew (−0.531) and slight leptokurtosis (kurtosis = 1.757). Given the sample size (*n* > 500,000), the Central Limit Theorem ensures that parameter estimates and t-tests remain reliable (see Figure 6).

---

## 4. Discussion and Conclusions

### 4.1 Summary of Findings

The hierarchical regression analysis yields three primary findings:

**First, telework arrangement alone is a weak predictor of job satisfaction.** While raw group differences in satisfaction by telework category are statistically significant, telework explains only 2% of the total variance. The practical significance of work location pales in comparison to attitudinal and engagement factors.

**Second, employee engagement is the dominant driver of satisfaction.** The Employee Engagement Index alone accounts for the majority of explained variance and carries the largest standardized coefficient (β = 0.705). Work-life balance perceptions add meaningful but secondary explanatory power (β = 0.091). Together, these attitudinal variables explain nearly 60% of the variance in job satisfaction.

**Third, the apparent telework advantage is largely spurious.** The raw satisfaction gap between routine teleworkers and in-office employees (0.40 points) virtually disappears — and actually reverses — once engagement and work-life balance are held constant. This finding challenges the popular narrative that remote work inherently increases satisfaction. Instead, it suggests that organizations offering remote work also tend to offer better engagement and work-life balance ecosystems.

### 4.2 Implications for Federal Workforce Policy

These results carry practical implications for federal agency leaders:

1. **Engagement and WLB support matter more than physical location.** Rather than focusing narrowly on expanding telework eligibility, agencies should invest in the factors that directly drive satisfaction: intrinsic work motivation, effective supervision, visible leadership commitment to work-life balance, and peer support cultures.

2. **Telework is not a substitute for good management.** The coefficient reversal demonstrates that the telework–satisfaction link is mediated by organizational culture. Simply allowing remote work without addressing engagement levers will not produce the expected satisfaction gains.

3. **In-office employees can be equally satisfied** — if their engagement and WLB needs are met. Policy-makers should ensure equitable access to flexible scheduling, supervisor support, and leadership attention regardless of telework status.

### 4.3 Limitations

- **Cross-sectional design:** The data are from a single time point (2024 FEVS), precluding causal claims. The observed mediation pattern is consistent with a causal pathway (telework → engagement → satisfaction) but could also reflect reverse causation or common unmeasured causes.
- **Multicollinearity between EEI and WLB:** The high VIF for these composites means that their individual coefficients should be interpreted cautiously; their combined effect is stable, but parsing the relative importance of engagement versus work-life balance requires further study (e.g., structural equation modeling).
- **Self-selection bias:** Employees who telework may differ systematically from those who do not in ways not captured by the available demographic controls.
- **Likert scale treatment:** Treating ordinal 1–5 Likert items as continuous in OLS is a common but imperfect practice. An ordinal logistic regression could provide a robustness check.

### 4.4 Future Research

Future research should consider longitudinal FEVS panels (e.g., linking 2020–2024 waves) to assess whether changes in telework policy predict changes in satisfaction within agencies. Structural equation modeling could formally test the mediation pathway from telework through engagement and WLB to satisfaction. Agency-level models (multilevel regression) could account for organizational culture differences that cluster employees within agencies.

---

## References

- Office of Personnel Management. (2024). *Federal Employee Viewpoint Survey: Public Release Data File and Codebook.* Washington, DC: OPM.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Erlbaum.
- Caillier, J. G. (2012). The impact of teleworking on work motivation in a U.S. federal government agency. *American Review of Public Administration*, 42(4), 461–480.
- De Vries, H., Tummers, L., & Bekkers, V. (2019). The benefits of teleworking in the public sector: Reality or rhetoric? *Review of Public Personnel Administration*, 39(4), 570–593.
- Mahler, J. (2012). The telework divide: Managerial and personnel challenges of telework. *Review of Public Personnel Administration*, 32(4), 407–418.

---

*Figures 1–6 are saved in the `figures/` directory and should be inserted into the final submission document as referenced above.*
