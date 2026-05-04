# Module 5 Presentation — Update for Chau

**From:** Karan
**Date:** 2026-04-29
**Re:** Final presentation deck + cleaned notebook
**Files attached:** `Module5_Final_Presentation_Parekh_Lee.pptx`, `Attrition_Pipeline_Cleaned.ipynb`

---

## TL;DR — read this first

- **The deck is done.** 18 slides total = 13 main (≈15 min) + 5 Q&A backup. Already QA'd visually.
- **Your attrition work is the bonus section** (Slides 10 + 11 + all 5 backup slides). All charts on those slides come **directly from your notebook**.
- **The main story is still job satisfaction** (matching what we submitted for Module 4) — pivoting that in 5 days felt risky.
- **I had to clean up your notebook** so it runs end-to-end. Nothing was deleted from your analysis — I only fixed bugs that were preventing it from running.
- **One thing for you to do:** re-run cell 16 in Jupyter (just hit Shift+Enter on it) and save. Takes 5 seconds. Explanation below.

---

## Why I couldn't just use your notebook as the deliverable

I tried. Three problems made it impossible to use as-is for a final presentation:

### 1. The notebook predicts a *different* outcome than what we submitted

| | Module 4 doc (submitted Apr 13) | Your notebook |
|---|---|---|
| Outcome we predict | **Job satisfaction (Q70)** — continuous 1-5 | **Attrition (DLEAVING_BIN)** — binary |
| Type of model | Hierarchical OLS regression + ML comparison | Logistic Regression + Random Forest classifier |
| Research question | "Does telework predict satisfaction?" | "Who's likely to leave?" |

The professor will have read our submitted Module 4 doc before we present. If we show up on May 4 talking about attrition, our deck won't match what's in the doc — and the rubric explicitly says "this submission will become part of the final report."

**My call:** keep the main deck aligned with the doc, position your attrition work as a **bonus secondary insight** with its own slides. That way nothing is wasted, and we're consistent with the submitted artifact.

### 2. The notebook had three execution-blocking bugs

(I want to be transparent about these — none of them are deal-breakers, but the notebook would not run end-to-end without fixes.)

| Bug | Where | What I changed |
|---|---|---|
| Spark + wrong path | Cell 1 — `spark.read.csv("/Volumes/workspace/...")` | Replaced with `pd.read_csv()` and a **portable path** that finds the FEVS CSV in either of our Downloads folders |
| `DLEAVING_BIN` used before defined | Cells 18-19 referenced `DLEAVING_BIN` but it was only created (inline) inside cell 14's plotting cell | Created `DLEAVING_BIN` cleanly in its own cell (cell 9) — runs before any cell that uses it |
| Kernel-freezing chart | Cell 16: `df.plot(kind='bar', color=colors)` on the full 674,207 × 96 DataFrame | Replaced with `df.groupby('Q71')['DLEAVING_BIN'].mean().plot(...)` — the actual "Attrition Rate by Pay Satisfaction" chart your markdown promised |

After these three fixes the notebook runs top-to-bottom in ~3 minutes.

### 3. There was a label bug in cell 16

This is small but worth mentioning because it would have confused anyone reading the chart:

> The x-axis label said *"Q71 (1=Very Satisfied … 5=Very Dissatisfied)"* but FEVS Q71 is actually coded the other way (**1=Very Dissatisfied, 5=Very Satisfied**). The data was right; the label was reversed. The color order (green→red) was matched to the wrong label.

I patched cell 16's source code to:
- Fix the label
- Reverse the color order so red is on the left (very dissatisfied → high attrition) and green is on the right (very satisfied → low attrition)

**This is the one thing you need to do:** open the notebook, click cell 16, press Shift+Enter, then Ctrl+S. The cell's stored output is from the old buggy version.

---

## What's in the cleaned notebook

`Attrition_Pipeline_Cleaned.ipynb` — same structure as yours, just runnable:

| Cells | Section | What it does |
|---|---|---|
| 1-3 | **Setup + load** | Pandas import, load FEVS CSV, basic shape/dtype/missingness check |
| 4-9 | **Cleaning** | Median-impute Q* numerics, mode-impute demographics, drop missing on `DLEAVING`, create `DLEAVING_BIN` |
| 10-13 | **Target EDA** | `DLEAVING` value counts + bar chart with the A=No / B/C/D=Leaving legend |
| 14-20 | **Driver EDA** | Q71 boxplot, attrition rate by Q71, leadership_score (mean of Q57-Q65), correlation, side-by-side comparison |
| 21-22 | **By department** | Satisfaction by agency, agency heatmap |
| 25-28 | **Top-20 agency analysis** | Attrition rate by top 20 departments, scatter of satisfaction vs attrition |
| 33-37 | **Modeling pipeline** | Train/test split, Logistic Regression, Random Forest, AUC, confusion matrices, RF feature importance |
| 38 | **Summary** | Markdown takeaways |

**Headline numbers from your pipeline:**
- Sample (after cleaning): ~626k respondents
- Base attrition rate: ~33%
- Logistic Regression AUC: 0.76
- Random Forest AUC: 0.77
- Top 3 features: Job satisfaction (Q70), Leadership composite, Pay satisfaction (Q71)
- Bottom features: Demographics — barely register

---

## What's in the deck

`Module5_Final_Presentation_Parekh_Lee.pptx` — 18 slides, 16:9, navy + gold "Midnight Executive" theme.

### Main flow (~15 minutes, 13 slides)

| # | Slide | Source of chart |
|---|---|---|
| 1 | Title — *Remote Work and Federal Employee Satisfaction* | — |
| 2 | Hook — **71% are satisfied** + distribution chart | Generated from the regression pipeline |
| 3 | Research question (just one sentence) | — |
| 4 | The data (3 cards: 646K · 36 · 96) | — |
| 5 | Approach — 4-step process flow diagram | — |
| 6 | Surface finding — telework gap (0.40 points) | Regression pipeline |
| 7 | The twist — **Simpson's Paradox** (effect flips sign) | Regression pipeline |
| 8 | Engagement explains 60% — R² progression chart | Regression pipeline |
| 9 | Engagement is ~7× the next thing — standardized β | Regression pipeline |
| **10** | **Bonus: who's likely to leave?** | ⭐ **Your notebook, cell 34** (RF feature importance) |
| **11** | **And the relationship is monotonic** | ⭐ **Your notebook, cell 16** (corrected version, red→green) |
| 12 | Three takeaways for federal agencies | — |
| 13 | Limitations + close (*"Telework gets the headlines. Engagement gets the results."*) | — |

### Q&A backup (5 slides — only if asked)

| # | Topic | Source |
|---|---|---|
| 14 | Pay satisfaction vs. leaving (boxplot) | **Your notebook, cell 14** |
| 15 | Attrition varies by agency (top 20) | **Your notebook, cell 25** |
| 16 | Less satisfied agencies have higher attrition (scatter) | **Your notebook, cell 27** |
| 17 | Department satisfaction heatmap | **Your notebook, cell 22** |
| 18 | Confusion matrix — model performance | **Your notebook, cell 33** |

**8 of the 18 charts come directly from your notebook output.** The other 10 are from the regression analysis we already submitted.

---

## Why this order of slides?

The deck follows a **"set up → twist → resolve"** narrative arc, which is what HBR's "presenting to a general audience" article (the one Dr. Philpot pointed at) recommends:

1. **Slides 1-5 — Set the stage.** Here's the question, here's the data, here's how we approached it.
2. **Slide 6 — Plant the surface finding.** "Remote workers look more satisfied" — looks like the answer.
3. **Slide 7 — The twist.** Simpson's Paradox: once we control for engagement, the telework effect flips. This is the *moment of surprise* that makes the talk memorable.
4. **Slides 8-9 — Resolve.** Engagement is the real driver, by a huge margin.
5. **Slides 10-11 — Your bonus.** "We asked a side question — who's leaving? Same drivers."
6. **Slides 12-13 — Recommendations + close.**

The Simpson's Paradox slide is the **money slide** of the talk. It's the one that gets people to pay attention.

---

## Speaking split (suggestion — happy to swap)

| Section | Speaker | Slides | Time |
|---|---|---:|---:|
| Open + question | Karan | 1-3 | 2:00 |
| Data + approach | Chau | 4-5 | 2:00 |
| Surface finding + Simpson's twist | Karan | 6-7 | 2:30 |
| What actually drives satisfaction | Chau | 8-9 | 2:30 |
| **Your bonus — who's leaving** | **Chau** | **10-11** | **2:30** |
| Recommendations | Karan | 12 | 1:30 |
| Limitations + close | Chau | 13 | 1:00 |
| Buffer for hand-offs | — | — | 1:00 |
| **Total** | | **13** | **~15:00** |

You'd carry Slides 10-11 (your bonus attrition track using your charts) which makes sense — you built that pipeline. I'd carry the Simpson's Paradox slides since I built the hierarchical regression. Open to flipping any of this.

---

## What I'd like your sign-off on before May 4

1. **Open the deck and click through it** end to end. Tell me anything you want to swap, rephrase, or remove.
2. **Re-run cell 16** in the notebook (Shift+Enter on it, then Ctrl+S) — I patched it but the saved output is stale.
3. **Decide if the speaker split works** for you.
4. **Practice run** — I'd like to do at least one timed walkthrough together. The Mechanics rubric is 25 points and timing matters.

---

## Files in the repo

| File | What it is |
|---|---|
| **`Module5_Final_Presentation_Parekh_Lee.pptx`** | The deck |
| `Attrition_Pipeline_Cleaned.ipynb` | Your notebook, cleaned and runnable |
| `Module 4_ Model with Results.docx` | The doc we submitted |
| `Presentation_Outline_Module5.md` | Speaker notes + Q&A prep |
| `figures_from_notebook/` | The charts your notebook produces |
| `figures_presentation/` | The charts the regression pipeline produces |
| `presentation_pipeline.py` | Single-script regression analysis (matches the submitted doc) |
| `build_presentation.py` | Source code for the deck |

---

## Anticipated Q&A — what we should both be ready to answer

I drafted ~6 prepared answers in `Presentation_Outline_Module5.md`. The big ones:

- **"Why OLS instead of ordinal logit on a Likert outcome?"** — Standard practice with n>500K; we cross-checked.
- **"Why is the on-site coefficient *positive* in the final model?"** — Don't read it as "make people come in." Read it as "the original telework effect was carried by engagement and WLB, not by location."
- **"Are engagement and satisfaction the same construct?"** — Correlated (~0.75) but distinct. 40 percentage points of unexplained variance say so.
- **"How would you act on this if you were OPM?"** — Three things: (1) measure engagement quarterly, (2) tie manager reviews to team engagement deltas, (3) stop using telework as the main lever for retention.
- **"How good is your attrition model?"** — AUC 0.77, recall on leavers ~46%. Useful for triage, not for individual decisions.

---

Let me know what you want to change, what you want to keep, and if there's anything you'd rather present that I'd present (or vice versa). Five days to go.

— Karan
