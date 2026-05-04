# Canva Build Kit — Intro + EDA (Slides 1–7)

Karan's portion of the deck. Use this as you build in Canva.
Chau handles modeling slides (8 onward) separately.

---

## Step 0 — Setup in Canva (do this once)

1. Open Chau's existing Canva file: https://www.canva.com/design/DAHIQdrxdb0/5kZedt9WuMFjQBu6DmNyWA/edit
2. Set page size: **1920 × 1080 px** (Resize → Custom Size). 16:9 widescreen.
3. **Brand kit colors** — add these as custom colors:
   - Primary navy: `#1E2761`
   - Light blue: `#CADCFC`
   - Accent gold: `#FFC107`
   - Text dark: `#21295C`
   - Muted gray: `#6B738D`
   - White: `#FFFFFF`
4. **Fonts** — pick from Canva's library:
   - Headers: **Montserrat Bold** (or Calibri Bold if you want to match my deck)
   - Body: **Open Sans** or **Lato** (both free in Canva)
   - Don't use Canva's "Magic Write" for any text — that flags as AI
5. **Upload your chart PNGs** (Uploads tab → Upload media):
   - From `figures_presentation/`: all 8 PNGs
   - From `figures_from_notebook/`: `cell16_attrition_by_pay_CORRECTED.png`, `cell34_importances_pd_series_rf_feature_importances_index.png`, plus any backup ones Chau wants

---

## Slide 1 — Title

**Background:** solid navy `#1E2761` covering the full slide
**Layout:** all text left-aligned, vertically centered around the middle

**Copy to type (use these exact words, or change to your voice):**

> Top of slide (small, white, bold caps): `ADTA 5940 · ANALYTICS CAPSTONE · SPRING 2026`
>
> Then a thin gold horizontal line `#FFC107` (just a Canva rectangle 1 inch wide × 6 px tall)
>
> Big title (white, bold, 60–70 pt):
> **Remote Work and Federal Employee Satisfaction**
>
> Subtitle (light blue `#CADCFC`, 24 pt):
> A view from 646,000 federal employees
>
> Bottom area (white, 18 pt):
> **Karan Parekh · Chau Le**
> University of North Texas · Dr. Denise Philpot

**What you say while it's up:** "Hi everyone, I'm Karan, this is Chau, and we looked at the 2024 Federal Employee Viewpoint Survey to figure out what actually makes federal employees satisfied at work."

---

## Slide 2 — The hook

**Background:** white with a navy bar `#1E2761` along the left edge (Canva rectangle, 0.18 inch wide, full height)

**Layout:** split slide. Left half = giant number. Right half = chart.

**Copy:**

> Top-left small caps (navy bold, 12 pt):
> `THE STARTING POINT`
>
> Center-left big number (navy, 200+ pt, bold):
> **71%**
>
> Below the number (dark blue `#21295C`, 18 pt, bold, centered):
> of federal employees say they're satisfied
>
> Smaller line below (gray `#6B738D`, 14 pt):
> Today's question: why those, and not the other 187,000?
>
> Right half: drop in `figures_presentation/01_satisfaction_distribution.png`
>
> Bottom-left footer (gray, 10 pt):
> `Source: 2024 OPM Federal Employee Viewpoint Survey · n = 646,545`
>
> Bottom-right (gray, 10 pt): `2 / 13`

**What you say:** "Out of every 10 federal workers, about 7 say they're satisfied with their job. That sounds great. But that still leaves almost 200,000 people who aren't. We wanted to know what makes the difference."

---

## Slide 3 — The research question

**Background:** light blue `#CADCFC` covering full slide
**Layout:** centered text in middle of slide. Lots of empty space.

**Copy:**

> Small bold navy text top (14 pt):
> `OUR RESEARCH QUESTION`
>
> Below it: a vertical navy bar `#1E2761` (about 0.18 inch wide × 1 inch tall) — like a quote mark
>
> Big text next to the bar (navy, bold, 36 pt):
> Does where you work — remote, hybrid, or on-site —
> actually change how satisfied you are?
>
> Bottom-right footer: `3 / 13`

**What you say:** "So the question we asked is simple. Telework has been a huge debate in the federal workforce since 2020. We wanted to know: does it actually matter for how satisfied people are at work?"

---

## Slide 4 — The data

**Background:** white with navy left bar
**Layout:** title at top, three equal cards across the middle

**Header:**

> Top small caps (navy, 12 pt): `WHAT WE WORKED WITH`
> Then big title (navy, 32 pt, bold): **The data**

**Three cards (equal size, centered, with a navy strip across the top of each):**

| Card 1 | Card 2 | Card 3 |
|---|---|---|
| **646K** (huge navy) | **36** (huge navy) | **96** (huge navy) |
| respondents (bold) | agencies (bold) | questions (bold) |
| Every federal employee who responded to the 2024 survey. (small gray text) | From cabinet departments to small independent agencies. | Job satisfaction, engagement, work-life balance, demographics. |

**Footer (gray, 11 pt):**
> Source: U.S. Office of Personnel Management — Public Release Data File

**Bottom-right:** `4 / 13`

**What you say:** "Our data is the FEVS — the Federal Employee Viewpoint Survey. It's run by OPM every year. The 2024 version covers about 646,000 employees across 36 agencies, and asks 96 questions covering everything from satisfaction to engagement to work-life balance."

---

## Slide 5 — The approach

**Background:** white with navy left bar
**Layout:** title at top, four boxes across the middle connected by arrows

**Header:**

> Top small caps: `APPROACH`
> Big title (navy, 32 pt, bold): **We built the model in four steps**
> Subtitle (gray, 15 pt): Each step adds one ingredient and shows how much more it explains.

**Four boxes (equal size, navy strip on top with white "1", "2", "3", "4"):**

| Step 1 | → | Step 2 | → | Step 3 | → | Step 4 |
|---|---|---|---|---|---|---|
| **Telework only** | | **+ Work-life balance** | | **+ Engagement** | | **+ Demographics** |
| Where you work. | | Do you have time for life? | | Are you energized by your work? | | Age, gender, tenure, supervisor. |

(In Canva: use the "Right Arrow" shape between each box, navy color)

**Bottom-right:** `5 / 13`

**What you say:** "Our approach was step by step. We started with just telework. Then added work-life balance. Then engagement. Then demographics. At each step we measured how much more of the variation we could explain. That tells us which factor is actually doing the work."

---

## Slide 6 — Surface finding

**Background:** white with navy left bar
**Layout:** chart on left, callout panel on right

**Header:**

> Top small caps: `FINDING 1 — SURFACE`
> Big title (navy, 32 pt, bold): **At first glance, remote workers look more satisfied**

**Left side:** drop in `figures_presentation/02_telework_raw_gap.png`

**Right side:** light blue `#CADCFC` filled rectangle, with these inside:

> Small bold navy at top: `THE GAP`
>
> Huge number (navy, 72 pt, bold): **0.40**
>
> Below it (dark text, 13 pt):
> points on the 5-point satisfaction scale
>
> Smaller (gray, 11 pt):
> Routine remote (3.94)
> vs. required on-site (3.54)

**Footer (gray, 10 pt):** `FEVS 2024  ·  Q70 mean by Q91 telework status`
**Bottom-right:** `6 / 13`

**What you say:** "When we just looked at the raw averages, there was a clear gap. People who telework routinely averaged 3.94 on satisfaction. People who are required on-site averaged 3.54. That's almost half a point. Looks like a big win for telework."

**Pause here — set up the next slide carefully.**

---

## Slide 7 — The twist

**Background:** white with navy left bar
**Layout:** chart on left, dark navy callout on right (this one is darker than slide 6)

**Header:**

> Top small caps: `FINDING 1 — THE TWIST`
> Big title (navy, 32 pt, bold): **…but that's not the whole story**

**Left side:** drop in `figures_presentation/04_simpsons_paradox.png`

**Right side:** SOLID navy `#1E2761` rectangle (filling about 30% of slide width, full height of the chart):

> Small gold caps `#FFC107` at top: `WHAT HAPPENED`
>
> Big white bold text (22 pt):
> The telework
> effect flipped
> sign.
>
> Light blue text below (`#CADCFC`, 11 pt, line spacing 1.4):
> Once we account for engagement
> and work-life balance, being
> required on-site goes from
> −0.40 to slightly positive.
>
> The original gap wasn't really
> about where people work.

**Footer (gray, 10 pt):** `Hierarchical OLS regression  ·  M1 vs. M4 telework coefficients`
**Bottom-right:** `7 / 13`

**What you say:** "Now here's where it gets interesting. When we add the other variables to the model — work-life balance and engagement — the telework effect doesn't just shrink. It flips sign. Being required on-site actually has a tiny positive effect once we account for the rest. So that 0.40-point gap from the previous slide wasn't really about where people work. It was about something else. And that something else is what we'll show you next."

(That's the handoff to Chau for slide 8 onward.)

---

## Layout cheat sheet (for every content slide)

```
┌────────────────────────────────────────────┐
│┃ KICKER (small navy caps)                  │ ← navy left bar
│┃                                           │
│┃ Big slide title (navy 32 pt bold)         │
│┃                                           │
│┃                                           │
│┃    [Chart]              [Callout panel]   │
│┃                                           │
│┃                                           │
│┃ Footer source line (gray 10 pt)           │  X / 13
└────────────────────────────────────────────┘
```

- **Margins:** at least 0.5 inch from every edge
- **Vertical rhythm:** kicker (0.5"), title (0.5"–1.0"), then breathing room, then content, then footer
- **Don't center body text.** Left-align always. Center is OK only for big stat callouts.
- **Don't use Canva's gradient backgrounds.** They scream "AI-generated."
- **Don't add decorative lines under titles.** AI presentation generators do that. Keep it clean.

---

## Things to absolutely AVOID (these get flagged as AI)

| ❌ Avoid | ✅ Do this instead |
|---|---|
| Em-dashes (—) | Periods or colons |
| "delve into," "leverage," "robust framework," "comprehensive analysis" | Plain words |
| Perfectly-balanced bullet lists (all the same length) | Varied lengths, some longer some shorter |
| Stock business templates with banners and stripes | Plain background + your charts |
| Generic Canva AI illustrations | Your real charts only |
| Animated transitions on every slide | Maybe 1-2 simple fade transitions |
| Rainbow color palettes | Stick to navy + light blue + gold |

---

## Checklist before you hand off to Chau

- [ ] All 7 slides have your real charts (not Canva stock images)
- [ ] No em-dashes anywhere — replace with periods or colons
- [ ] No "AI-tell" phrases (delve, leverage, robust, comprehensive, intricate, multifaceted, in conclusion, in summary)
- [ ] Page numbers `X / 13` on slides 2–7 (not on slide 1)
- [ ] Spell-check pass
- [ ] Talk through it once out loud, time it. Slides 1–7 should run about 7 minutes.
- [ ] Save as a copy named `Module5_Final_Parekh_Lee.pptx` when ready to submit (Canva: File → Download → PPTX)

---

## What Chau builds (slides 8–13)

Just so you both stay aligned:

| Slide | What it shows | Chart to use |
|---|---|---|
| 8 | Engagement explains 60% (R² progression) | `figures_presentation/03_r2_progression.png` |
| 9 | Engagement is 7× the next thing | `figures_presentation/05_standardized_coefs.png` |
| 10 | Bonus: who's likely to leave (XGBoost) | `figures_from_notebook/cell34_importances_pd_series_rf_feature_importances_index.png` *(she'll re-render this with XGBoost outputs after running the updated notebook)* |
| 11 | And the relationship is monotonic | `figures_from_notebook/cell16_attrition_by_pay_CORRECTED.png` |
| 12 | Three takeaways for federal agencies | (text only, three numbered circles) |
| 13 | Limitations + close | (text only, dark navy background) |

She has the same color palette and font conventions to match your slides.

---

## Files you need open while building

- This guide: `Canva_Build_Kit.md`
- Charts folder: `figures_presentation/`
- Charts folder: `figures_from_notebook/`
- Reference deck (don't copy directly, just to remind yourself): `Module5_Final_Presentation_Parekh_Lee.pptx`
