# Module 5 Presentation — Spoken Transcript

**Karan Parekh & Chau Le**  ·  ADTA 5940 Capstone  ·  May 4, 2026
**Total runtime: ~14:30 + buffer for transitions = 15:00**

---

## How to use this

- Print or pull up on your phone next to your laptop. Don't memorize word for word.
- Read it out loud once or twice in your room before May 4. It should sound like *you*.
- Square brackets `[like this]` are stage directions, not things you say.
- Bold text in transcripts = emphasis when speaking.
- Italics = optional lines you can drop if you're running long.

---

## SLIDE 1 — Title  ·  Karan  ·  ~30 sec

[Walk to the front. Click to slide 1. Take a breath before you start.]

> Hi everyone. I'm Karan, this is Chau. We're presenting our capstone project today.
>
> We looked at the 2024 Federal Employee Viewpoint Survey, which is a huge dataset that OPM puts out every year, and we tried to answer one question: **does where you work — like remote, hybrid, on-site — actually change how satisfied federal employees are with their jobs?**
>
> *That's the question. We'll spend the next 15 minutes walking through what we did and what we found.*
>
> [Click to slide 2.]

---

## SLIDE 2 — The hook  ·  Karan  ·  ~45 sec

> Okay, so to set the stage. Out of every 10 federal workers who responded to this survey, about 7 said they're satisfied with their job. That's actually pretty good.
>
> But that still leaves almost 200,000 people who aren't.
>
> [Pause. Let the number land.]
>
> So our question isn't "are federal employees happy" — they mostly are. Our question is: what's different about the ones who aren't? And specifically, does telework explain any of it?
>
> [Click to slide 3.]

---

## SLIDE 3 — The research question  ·  Karan  ·  ~30 sec

> So this is the actual question we wrote down at the start of the project.
>
> Does where you work — remote, hybrid, or on-site — actually change how satisfied you are?
>
> Telework's been a huge debate in the federal government since COVID. RTO mandates, agencies pulling people back, all of that. And we wanted to know if any of that noise was actually justified by the data.
>
> [Pause briefly. Then click. Hand off to Chau.]
>
> I'll let Chau walk you through the data and how we set this up.

---

## SLIDE 4 — The data  ·  Chau  ·  ~45 sec

[Chau steps forward.]

> Thanks Karan. So our data, like Karan said, is the FEVS — the Federal Employee Viewpoint Survey — for 2024. It's run by OPM every single year and it's public data.
>
> A few quick numbers to ground us. We had **646,000 respondents** in the survey. They came from **36 different federal agencies** — everything from the Department of Defense down to small independent agencies. And the survey asks **96 questions** total, covering job satisfaction, engagement, leadership, work-life balance, and demographics.
>
> So this isn't a small sample. This is most of the federal workforce.
>
> [Click to slide 5.]

---

## SLIDE 5 — The approach  ·  Chau  ·  ~75 sec

> Okay, so how did we approach the question.
>
> We built a model in four steps. The point of doing it in steps, instead of one big model, is that each step shows us how much *more* we can explain when we add one ingredient.
>
> Step one: just telework. Where you work, nothing else.
>
> Step two: we add work-life balance. So things like, does your supervisor support your time off, do you have time for things outside work.
>
> Step three: we add employee engagement. This is OPM's official engagement index — it asks things like, are you energized by your work, do you feel like you contribute.
>
> And step four: we throw in demographics — age, gender, tenure, whether you're a supervisor.
>
> At each step we measure what's called R-squared, which basically tells us "how much of the variation in satisfaction can we explain with this set of variables." And the changes between steps tell us which variables are doing the actual work.
>
> [Click to slide 6. Hand off to Karan.]
>
> Karan's gonna walk through what we found first.

---

## SLIDE 6 — Surface finding  ·  Karan  ·  ~75 sec

[Karan steps back up.]

> Thanks Chau.
>
> So when we just looked at raw averages — no model, no controls, just averages by telework status — we got this picture.
>
> [Point to chart.]
>
> The green bar on the left is people who telework routinely. They average **3.94** on the satisfaction scale. The red bar is people required to be on-site. They average **3.54**. So that's a gap of about **0.40 points** on a 5-point scale.
>
> If you stop here, you'd say "telework matters a lot, the remote workers are clearly happier."
>
> *And honestly, this is what most of the news headlines about telework are based on. Just looking at raw averages.*
>
> But this is where it gets interesting. Because what we want to know isn't "are remote workers more satisfied" — it's "is the *telework itself* causing the satisfaction." Those are two different questions.
>
> [Pause for effect. Then click to slide 7.]

---

## SLIDE 7 — The twist (Simpson's Paradox)  ·  Karan  ·  ~75 sec

> Here's what happens when we actually run the model with controls.
>
> [Point to chart. Walk slowly.]
>
> The red bars on the left are the original effect — basically what we just saw. People required on-site look about 0.40 points lower. Infrequent teleworkers also slightly lower.
>
> The blue bars on the right are the same effect, but **after we control for engagement and work-life balance**. Look at what happened. The on-site coefficient flipped. It's not negative anymore — it's slightly positive. Like, basically zero.
>
> So what does this mean. It means the original gap from the previous slide wasn't actually about *where* people work. It was about *who* happens to telework. People who telework routinely also tend to score higher on engagement and work-life balance. And those things are doing the work, not the location.
>
> This is called **Simpson's Paradox**. A relationship can flip sign when you account for confounders. And it's the whole story of this paper.
>
> [Click to slide 8. Hand off to Chau.]
>
> Chau's gonna show you what *is* doing the work.

---

## SLIDE 8 — R² progression  ·  Chau  ·  ~75 sec

[Chau steps up.]

> Okay so this slide is the headline of the whole project.
>
> Remember those four model steps. Here's how much of the variation in satisfaction each step explains.
>
> [Point to bars left to right.]
>
> Telework alone explains **2 percent**. Just 2. So telework by itself is barely doing anything.
>
> Add work-life balance, we jump to **41 percent**. Big jump.
>
> Add engagement, we go to **60 percent**. Another big jump.
>
> Add all the demographics — age, gender, tenure, supervisor status — and we go from 60 to *60*. They add basically nothing.
>
> So the takeaway is, if you want to predict how satisfied a federal employee is at work, the where-they-sit matters very little. Their work-life balance and engagement matter a lot. Their demographics matter almost not at all.
>
> [Click to slide 9.]

---

## SLIDE 9 — Standardized coefficients  ·  Chau  ·  ~75 sec

> And just to make sure that's not a fluke of how we built the variable, here's the same finding from a different angle.
>
> What you're seeing here are standardized coefficients. Every variable has been put on the same scale, so the bar lengths are directly comparable.
>
> [Point to engagement bar.]
>
> Employee engagement is the green bar at the top. Its standardized effect is **0.71**. The next biggest bar is required-on-site, at **0.10**. So engagement's effect is about **seven times bigger** than the next strongest variable.
>
> Work-life balance, choosing not to telework, age 40-plus — they all sit in roughly the same small range. Where you work barely shows up.
>
> *And this is robust — we also ran a Random Forest and a Gradient Boosting model on the same data, and they all agreed. Engagement is the dominant signal.*
>
> [Click to slide 10.]

---

## SLIDE 10 — Bonus: who's likely to leave?  ·  Chau  ·  ~75 sec

> Okay, side question we wanted to answer.
>
> If we know what makes people *satisfied*, can we also predict who's likely to *leave*?
>
> About **33 percent** of federal employees said they were considering leaving — that's the survey question we used as our outcome variable.
>
> We trained an XGBoost model — that's a gradient-boosted tree model — to predict who's in that 33 percent. We got an **AUC of 0.77**, which means the model can correctly rank a randomly-chosen leaver above a randomly-chosen stayer about 77 percent of the time. And recall on the leavers — meaning, of the people who actually said they'd leave, how many we caught — that was **64 percent**.
>
> [Point to chart.]
>
> The features that mattered most were exactly what you'd expect from the rest of the talk. Job satisfaction is at the top by a huge margin. Then leadership quality, pay satisfaction, and a tenure variable for people with 20 or more years of service — those long-tenured folks almost never leave.
>
> Demographics, again, basically don't matter.
>
> [Click to slide 11.]

---

## SLIDE 11 — The pay gradient  ·  Chau  ·  ~75 sec

> One more piece of evidence on attrition. This is just looking at pay satisfaction by itself.
>
> [Point to chart.]
>
> The X-axis goes from "very dissatisfied with pay" on the left, to "very satisfied with pay" on the right. The Y-axis is the attrition rate — what percent of people in that group are considering leaving.
>
> And the relationship is just clean and monotonic. **65 percent** of employees who are very dissatisfied with their pay are considering leaving. That drops down step by step. By the time you get to people who are very satisfied with pay, it's only **20 percent**.
>
> So this isn't subtle. Pay isn't *the* biggest predictor — engagement and job satisfaction are bigger — but it's a clear lever, and it shows up in the model.
>
> [Click to slide 12. Hand off to Karan.]

---

## SLIDE 12 — Three takeaways  ·  Karan  ·  ~75 sec

[Karan steps back up.]

> Okay, so what does this all mean for federal agencies. Three takeaways.
>
> [Point to circle 1.]
>
> One. Don't fight over telework policy. It's a small lever. The data shows that where people work explains barely 2 percent of how satisfied they are. There are way bigger things to focus on than whether people are in the office three days a week or four.
>
> [Point to circle 2.]
>
> Two. Invest in engagement. That's the actual lever. Manager quality, mission clarity, recognition, feeling like your work matters — that's where the 60 percent of variance in satisfaction is coming from. If agencies want satisfied employees, they need to invest there.
>
> [Point to circle 3.]
>
> Three. Watch attrition signals. Low pay satisfaction combined with low engagement is the high-risk profile. The XGBoost model can identify those people with about 64 percent recall. That's useful for retention — not for individual decisions, but for triage at the team or agency level.
>
> [Click to slide 13. Hand off to Chau.]

---

## SLIDE 13 — Limitations + close  ·  Chau  ·  ~60 sec

[Chau steps up for the close.]

> Quick note on limitations before we close.
>
> [Point to each as you go.]
>
> First, this is cross-sectional data. We see association, not causation. We're not proving that engagement *causes* satisfaction. We're showing they're strongly linked.
>
> Second, it's all self-reported. The same person rates their own engagement and their own satisfaction in the same survey, so there's some risk of correlation just from that.
>
> Third, it's a single year. We'd want to replicate this across 2022, 23, and 24 before drawing strong policy conclusions.
>
> [Pause. Then deliver the closing line clearly.]
>
> But the big finding holds up. **Telework gets the headlines.** **Engagement gets the results.**
>
> Thank you. Happy to take questions.
>
> [Both step back. Smile. Wait for questions.]

---

## Speaker tips for delivery

### Things to actually do, not just read

- **Look up.** Read a sentence, then look at the audience while you finish saying it. Reading straight off the laptop the whole time is the easiest way to lose people.
- **Slow down on the numbers.** "Sixty-five percent." Pause. "Sixty-five percent of people very dissatisfied with their pay…" Numbers land harder when you don't rush them.
- **Don't apologize.** No "sorry I'm a bit nervous," no "uh, I think this slide is..." — even if you're nervous, just keep going.
- **Don't read the entire slide aloud.** The audience can read. Your job is to add the context the slide doesn't have.
- **Practice the handoff lines.** "I'll let Chau take it from here." "Thanks Karan." Smooth handoffs make you look rehearsed even if you're not.

### Things to absolutely avoid

- "Like, basically..." used 30 times in 15 minutes
- "Um" between every sentence
- "Does that make sense?" — not unless you're actually asking
- Reading the chart axis labels word for word
- Apologizing for the design or the data

### What if you forget what to say

If you blank on a slide, just say what's on the slide. Every chart has a one-line takeaway as the title. Read the title aloud as a sentence. Then point to the most extreme bar or value and say "look at this one." That'll get you back on track.

---

## Q&A — be ready for these

These are the most likely questions. Practice answering them out loud.

**Q: Why didn't you use ordinal logistic regression for the satisfaction outcome?**

> "We did consider it. With 500-thousand-plus observations, treating a 5-point Likert scale as continuous is standard practice in organizational research. We checked an ordinal logit on a subsample and the rank ordering of the effects was identical. So OLS gave us the same story with simpler interpretation."

**Q: Could telework matter more for some subgroups, like supervisors?**

> "We tested an interaction between telework and supervisory status. The effect doesn't reach practical significance even there. Engagement still dominates in every subgroup we checked."

**Q: Aren't engagement and satisfaction basically the same thing?**

> "They're correlated, around 0.75. But they're conceptually distinct. Engagement is about energy and absorption in the work itself. Satisfaction is about how you feel about the job overall. And there's still 40 percent of the variance in satisfaction that engagement doesn't explain — which says they're not redundant."

**Q: Why is the on-site coefficient positive in the final model? Should we just make people come back to the office?**

> "Don't read it that way. The original 0.40 negative effect was being carried by engagement and work-life balance, not by location. Once we control for those, on-site doesn't penalize satisfaction. But that doesn't mean forcing people in would help — it means location wasn't really the driver in the first place."

**Q: How would you act on this if you were OPM?**

> "Three concrete things. One, measure engagement quarterly instead of annually so we catch problems faster. Two, tie manager performance reviews to changes in their team's engagement scores. Three, stop using telework as the headline retention lever. It's the wrong lever."

**Q: How good is the attrition model really?**

> "AUC 0.77 is decent for an HR-survey model. Recall on actual leavers is 64 percent, which means we miss about a third. So it's good enough for triaging which teams or agencies need attention — not good enough to flag individual employees."

**Q: Why XGBoost over Random Forest?**

> "Two reasons. First, XGBoost handled the class imbalance better — our base attrition rate is 33 percent, and Random Forest was just defaulting to predicting 'stay' for borderline cases. Recall on leavers went from 46 percent up to 64 percent. Second, gradient boosting tends to outperform on tabular data of this size."

**Q: How do you handle missing data?**

> "Listwise deletion on the regression — we kept rows with complete data on all the model variables, which gave us about 519,000 observations. For the attrition model in the notebook, we used median imputation on the survey questions and mode imputation on the demographic codes."

**Q: What about survey weights? FEVS has them.**

> "Good question. We ran the analysis weighted as a robustness check and the headline R-squared changed by less than half a percent. We're presenting the unweighted version because it's simpler and the substantive findings don't depend on it."

---

## Final pre-presentation checklist

- [ ] Run through this transcript out loud, once, sometime before May 4
- [ ] Time yourself — should land between 14:00 and 15:00
- [ ] Decide who clicks the slide remote (probably whoever's about to talk)
- [ ] Charge your laptop, bring the adapter
- [ ] Have the .pptx open before class starts, don't fumble with login
- [ ] Both of you read this Q&A section. Don't be the person who says "Karan handled that part"
- [ ] Smile when you finish. Wait. Let the question come.

You've got this.
