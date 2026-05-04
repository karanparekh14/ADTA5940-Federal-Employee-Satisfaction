# Module 5 — Final Presentation Outline

**Karan Parekh & Chau Le · ADTA 5940 Spring 2026**
**Due: Mon May 4, 2026 9:00 PM · 15-minute limit · 200 points**

---

## Strategic decisions baked into this deck

1. **Aligned with the submitted Module 4 doc** — same two RQs (predict job satisfaction, hierarchical regression on telework). Don't pivot to a new story in the final week.
2. **Attrition is positioned as a bonus secondary insight** — one slide, late in the deck. Chau's notebook work shows up here.
3. **General-audience framing** (per the HBR article Dr. Philpot pointed at):
   - Use plain-English metaphors. No β, R², F-stat on slides — translate them.
   - Minimize text per slide. One number, one sentence, one chart.
   - Cut aggressively. ~12 slides for 15 min = ~75 sec/slide with breathing room.
4. **Graphics carry 75/200 points** — figures are pre-built in `figures_presentation/`. Drop them straight into the deck.

---

## Speaking split (suggested)

| Section | Speaker | Slides | Time |
|---|---|---:|---:|
| Open + question | Karan | 1–3 | 2:00 |
| Data + approach | Chau | 4–5 | 2:00 |
| Finding 1: Simpson's paradox | Karan | 6–7 | 2:30 |
| Finding 2: What actually drives satisfaction | Chau | 8–9 | 2:30 |
| Finding 3: Bonus — who's likely to leave | Chau | 10 | 1:30 |
| Recommendations | Karan | 11 | 2:00 |
| Limitations + close | Chau | 12 | 1:30 |
| Buffer for transitions | — | — | 1:00 |
| **Total** | | **12** | **~15:00** |

Q&A is separate (15 pts on rubric, but not part of the 15-minute limit).

---

## Slide-by-slide content

### Slide 1 — Title
- **Remote Work and Federal Employee Satisfaction**
- *A view from 646,000 federal employees*
- Karan Parekh & Chau Le · ADTA 5940 · Spring 2026
- Single full-bleed photo (federal building or "remote work" stock image), title overlaid bottom-left.
- **No** university logo clutter, no email addresses on title slide.

### Slide 2 — The hook (one number)
- Big text: **"60%"**
- Subtext: *of federal employees say they're satisfied with their job.*
- Small caption: *That leaves ~258,000 who aren't.*
- Read this slowly. Pause. Then transition.
- Chart: `figures_presentation/01_satisfaction_distribution.png`

### Slide 3 — The question
- One sentence on the slide:
  *"Does where you work — remote, hybrid, on-site — actually change how satisfied you are?"*
- That's it. No bullets. The question lands.

### Slide 4 — The data (1 slide, no more)
- 646,000 federal employees · 36 agencies · 2024 OPM Federal Employee Viewpoint Survey
- Three icons or callouts: **646K respondents** · **36 agencies** · **96 questions**
- **Skip:** sample size after listwise deletion, missingness rates, weighting decisions. (Save those for Q&A.)

### Slide 5 — How we approached it
- Plain-English version:
  *"We built a model in four steps. Each step adds one ingredient and shows how much more it explains."*
- Diagram: 4 stacked boxes — **Telework → + Work-life balance → + Engagement → + Demographics**
- Don't call it "hierarchical OLS regression" on the slide. Say it once verbally for the academics.

### Slide 6 — Surface finding (set up the surprise)
- Title: *"At first glance, remote workers look more satisfied"*
- Chart: `figures_presentation/02_telework_raw_gap.png`
- Verbal: "Routine remote workers average 3.94. Required-on-site averages 3.54. That's a 0.40-point gap. Looks like a clear win for telework."
- **Pause. Then turn to slide 7.**

### Slide 7 — The twist (Simpson's Paradox)
- Title: *"…but that's not the whole story"*
- Chart: `figures_presentation/04_simpsons_paradox.png`
- Verbal: "Once we control for engagement and work-life balance, the on-site effect actually flips positive. The original gap wasn't really *about* telework — it was about who happens to telework."
- **Metaphor for Q&A:** *"It's like saying ice-cream sales cause sunburns. They're both caused by the sun. Telework looked like the cause, but engagement was the real driver."*

### Slide 8 — What actually drives satisfaction (the headline chart)
- Title: *"Engagement explains 60% of the variation in satisfaction"*
- Chart: `figures_presentation/03_r2_progression.png`
- Verbal: "Telework alone explains 2%. Add work-life balance, you get to 41%. Add engagement, you're at 60%. Demographics — gender, age, tenure — add almost nothing on top."

### Slide 9 — Ranked drivers (in case anyone doubts it)
- Title: *"Engagement isn't just one factor. It's by far the biggest one."*
- Chart: `figures_presentation/05_standardized_coefs.png`
- Verbal: "Same picture from a totally different angle — standardized effect sizes. Engagement is ~7× larger than the next thing. Where you work barely shows up."
- **Optional swap:** `figures_presentation/07_rf_importance_satisfaction.png` to show the same finding from a Random Forest (different model class, same answer = robust).

### Slide 10 — Bonus: who's likely to leave?
- Title: *"Side question — can we predict who's thinking about leaving?"*
- One stat: **33% of federal employees are considering leaving.**
- Chart: `figures_presentation/08_attrition_bonus.png`
- Verbal: "We built a second model on a different question — leaving — and the answer rhymes. The same factors — engagement, pay satisfaction, leadership — dominate. Random forest predicts attrition with AUC = 0.77."
- This is Chau's track. **One slide. Don't dwell.**

### Slide 11 — What this means for federal agencies
- Title: *"Three takeaways"*
- Three short bullets (one line each):
  1. **Don't fight over telework policy.** It's a small lever. Engagement is the big one.
  2. **Invest in engagement.** Manager quality, mission clarity, recognition — that's the 60%.
  3. **Watch for attrition signals.** Low pay satisfaction + low engagement = high flight risk.
- Photo of federal employees / office, far less prominent than text.

### Slide 12 — Limitations & close
- Three brief bullets, then thank-you:
  - **Cross-sectional** — we can't prove causation, only association.
  - **Self-reported** — same person rates engagement and satisfaction.
  - **One year** — 2024 only. Replication across 2022–2024 in scope for follow-up.
- Closing line: *"Telework gets the headlines. Engagement gets the results."*
- Thank you · Q&A.

---

## Backup slides (for Q&A — keep ready, don't show in main flow)

| # | Topic | Asset |
|---|---|---|
| B1 | Hierarchical regression numbers (R², ΔR², F) | Table from `rq2_hierarchical_results.csv` |
| B2 | Three-model ML comparison | `figures_presentation/06_rq1_models.png` |
| B3 | Random forest feature importance (satisfaction) | `figures_presentation/07_rf_importance_satisfaction.png` |
| B4 | Sample size & missingness | One-liner: 519,284 analytic n after listwise deletion |
| B5 | Why OLS, not ordinal logit? | "Treating 5-point Likert as continuous is standard with n>500K" |
| B6 | Effect of survey weights (POSTWT) | "Re-ran weighted, headline R² within ±0.005" |
| B7 | Variance inflation factors / multicollinearity | "All VIFs <3, EEI items pre-averaged into composite" |
| B8 | EEI definition | "OPM 15-item index: Intrinsic + Supervisor + Leaders sub-indices" |

---

## Anticipated Q&A — short answers

**Q: Why did you treat satisfaction as continuous instead of ordinal?**
A: Standard practice in organizational research with samples this large. We checked an ordinal logit on a subsample — the rank-ordering of effects was identical.

**Q: Could telework matter more in some subgroups?**
A: We tested an interaction between telework and supervisory status — the effect doesn't reach practical significance even there. Engagement still dominates.

**Q: Aren't engagement and satisfaction essentially the same construct?**
A: They're correlated (~.75) but distinct. Engagement is about energy, identification, and absorption *in the work itself*; satisfaction is the affective evaluation of the job. The 40 percentage points of variance unexplained by engagement support that they're not redundant.

**Q: Why is "required on-site" positive in the final model?**
A: Once you net out engagement and WLB, the people forced into the office aren't penalized — and the comparison group (routine remote) loses its engagement advantage. Don't read this as "make people come in" — read it as "telework wasn't doing the work we thought it was."

**Q: How would you act on this if you were OPM?**
A: Three things. (1) Run the engagement battery quarterly, not annually. (2) Tie manager performance reviews to their team's engagement deltas. (3) Stop using telework as the main lever for retention — it's the wrong lever.

**Q: What about employees who *chose* not to telework?**
A: Small group (3.8%), and once we control for engagement, their satisfaction is similar to routine remote. Their choice signals something about engagement — not the other way around.

---

## Pre-presentation checklist

### Slides
- [ ] Font consistency throughout (one sans-serif: Inter, Calibri, or similar)
- [ ] All chart titles match the deck — no leftover matplotlib defaults
- [ ] No tracked changes, no comment bubbles, no red "TODO" text
- [ ] Page numbers on every slide except title and thank-you
- [ ] Spell-check entire deck (rubric: 10 pts)

### Visuals
- [ ] All 8 figures from `figures_presentation/` placed on slides 2, 6, 7, 8, 9, 10
- [ ] Each chart has a one-line takeaway *as the slide title*, not a generic "Figure 3"
- [ ] Image quality good at projector resolution (200+ DPI — already set in pipeline)

### Mechanics (rubric: 25 pts)
- [ ] Practiced run-through ≤15:00
- [ ] Speaking split rehearsed, hand-offs smooth
- [ ] Both team members can answer Q&A on either RQ (don't be the person who says "Karan handled that part")
- [ ] Looked up the room — laptop adapter, clicker, water

### Q&A (rubric: 15 pts)
- [ ] Both members read backup slides before going up
- [ ] Practiced the Simpson's Paradox metaphor out loud at least 3 times
- [ ] Has a "we'll follow up after class" answer ready for any question that needs the data file

---

## Files referenced

- `presentation_pipeline.py` — single-script reproduction of every figure and number
- `figures_presentation/` — 8 PNGs ready to drop into slides
- `rq1_model_comparison.csv`, `rq2_hierarchical_results.csv`, `presentation_headline_numbers.csv` — backing tables
- `Attrition_Pipeline_Cleaned.ipynb` — Chau's notebook, cleaned and committed to repo
- `Module 4_ Model with Results.docx` — submitted document this deck builds on
