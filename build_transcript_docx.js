/**
 * Build the presentation transcript as a properly formatted .docx.
 * 9 slides (Karan's portion). Slides 10-13 are Chau's modeling section.
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  TabStopType, TabStopPosition,
  HeadingLevel, BorderStyle, WidthType, ShadingType, PageNumber,
} = require("docx");

// ---------- Color palette (Midnight Executive theme) ----------
const NAVY  = "1E2761";
const INK   = "21295C";
const GOLD  = "FFC107";
const MUTED = "6B738D";
const ICE   = "CADCFC";
const BG    = "F4F6FB";

// ---------- Helpers ----------
const para = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: 120, line: 320 },
    ...opts,
    children: [new TextRun({ text, font: "Calibri", size: 22, ...(opts.run || {}) })],
  });

const heading = (text, level) =>
  new Paragraph({
    heading: level,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, font: "Calibri", bold: true,
                             color: level === HeadingLevel.HEADING_1 ? NAVY : INK })],
  });

const direction = (text) =>
  new Paragraph({
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: `[ ${text} ]`, font: "Calibri",
                             italics: true, size: 20, color: MUTED })],
  });

const speakerLine = (text) =>
  new Paragraph({
    spacing: { after: 140, line: 320 },
    indent: { left: 360 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 18, color: NAVY, space: 12 },
    },
    children: [new TextRun({ text, font: "Calibri", size: 23 })],
  });

const emphasized = (children) =>
  new Paragraph({
    spacing: { after: 140, line: 320 },
    indent: { left: 360 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 18, color: NAVY, space: 12 },
    },
    children,
  });

const bullet = (text) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, font: "Calibri", size: 22 })],
  });

const slideHeader = (num, title, time) => [
  new Paragraph({
    spacing: { before: 480, after: 100 },
    children: [
      new TextRun({ text: `SLIDE ${num}`, font: "Calibri", bold: true,
                    color: NAVY, size: 18 }),
      new TextRun({ text: "    ·    ", color: MUTED, size: 18 }),
      new TextRun({ text: time.toUpperCase(), color: MUTED, size: 18,
                    font: "Calibri" }),
    ],
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { after: 200 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 4 },
    },
    children: [new TextRun({ text: title, font: "Calibri", bold: true,
                             color: INK, size: 32 })],
  }),
];

// ---------- Cover ----------
const cover = [
  new Paragraph({ spacing: { before: 1800 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({
      text: "ADTA 5940  ·  ANALYTICS CAPSTONE  ·  SPRING 2026",
      bold: true, color: NAVY, size: 22, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({ text: "————", color: GOLD, size: 28, font: "Calibri" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({
      text: "Presentation Transcript",
      bold: true, color: INK, size: 56, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 800 },
    children: [new TextRun({
      text: "Remote Work and Federal Employee Satisfaction",
      italics: true, color: INK, size: 32, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({
      text: "Presenter: Karan Parekh",
      bold: true, color: NAVY, size: 26, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({
      text: "Co-presenter for modeling section: Chau Le",
      color: MUTED, size: 22, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({
      text: "University of North Texas  ·  Dr. Denise Philpot",
      color: MUTED, size: 22, font: "Calibri",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 600, after: 60 },
    children: [new TextRun({
      text: "9 slides  ·  Estimated runtime ~9 minutes",
      color: MUTED, size: 22, font: "Calibri",
    })],
  }),
  new Paragraph({ pageBreakBefore: true, children: [] }),
];

// ---------- How to use ----------
const howto = [
  heading("How to use this transcript", HeadingLevel.HEADING_1),
  bullet("Print this or open it on your phone next to your laptop on May 4."),
  bullet("Read it out loud once at home before the day of. It should sound like you, not a script."),
  bullet("Stage directions in italics inside [brackets] are not things you say out loud."),
  bullet("The bordered grey blocks are the actual lines you say. Look at the audience between sentences."),
  bullet("If you blank on a slide, read the slide title aloud and point at the biggest number on the chart. You'll be back on track."),
  bullet("Slides 1 through 9 are yours. Chau takes over for slides 10 through 13 (modeling)."),
];

// ---------- Slide content ----------
const slides = [
  {
    num: 1, title: "Title — Remote Work and Federal Employee Satisfaction",
    time: "≈30 sec",
    pre: "Walk to the front. Click to slide 1. Take a breath before you start.",
    lines: [
      "Hi everyone. I'm Karan, this is Chau. We're presenting our capstone project today.",
      "We looked at the 2024 Federal Employee Viewpoint Survey, which is a huge dataset that OPM puts out every year. We tried to answer two questions. First, does where you work — remote, hybrid, or on-site — actually change how satisfied federal employees are with their jobs. And second, can we predict who's likely to leave.",
      "I'll cover the first question. Chau will cover the second. We'll spend about 15 minutes total.",
    ],
    post: "Click to slide 2.",
  },
  {
    num: 2, title: "The hook — 71%",
    time: "≈45 sec",
    pre: "Slide 2 is up. The big 71% on the left, distribution chart on the right.",
    lines: [
      "Okay so to set the stage. Out of every 10 federal workers who responded to this survey, about 7 said they're satisfied with their job. That's actually pretty good.",
      "But that still leaves almost 200,000 people who aren't.",
    ],
    direction: "Pause. Let the number land.",
    lines2: [
      "So our question isn't really 'are federal employees happy.' Most of them are. The question is what's different about the ones who aren't. And does telework explain any of it.",
    ],
    post: "Click to slide 3.",
  },
  {
    num: 3, title: "Our research questions",
    time: "≈40 sec",
    pre: "Two questions on screen, numbered.",
    lines: [
      "These are the two questions we wrote down at the start of the project.",
      "Number one. Does where you work — remote, hybrid, or on-site — actually change how satisfied you are.",
      "Number two. Which employees are at risk of leaving.",
      "Telework has been a huge debate in the federal government since COVID. RTO mandates, agencies pulling people back, all of that. We wanted to see if any of that noise was actually justified by the data. And we also wanted a model that could flag who might be on the way out.",
    ],
    post: "Click to slide 4.",
  },
  {
    num: 4, title: "The data — 646K · 36 · 96",
    time: "≈45 sec",
    pre: "Three big number cards on screen.",
    lines: [
      "Quick rundown of the data. The FEVS is run by OPM every year and it's all public.",
      "We had 646,000 respondents in the 2024 wave. They came from 36 different federal agencies — everything from cabinet departments like Defense and Treasury, down to small independent ones. And the survey asks 96 questions covering job satisfaction, engagement, leadership, work-life balance, and demographics.",
      "So this isn't a small sample. This is most of the federal workforce.",
    ],
    post: "Click to slide 5.",
  },
  {
    num: 5, title: "The approach — 4 steps",
    time: "≈75 sec",
    pre: "Four numbered boxes connected by arrows.",
    lines: [
      "Okay, so how did we approach the first question.",
      "We built the model in four steps. The reason we did it in steps instead of one big model is that each step shows us how much more we can explain when we add one new ingredient. That tells us which variable is actually doing the work.",
      "Step one. Just telework. Where you work, nothing else.",
      "Step two. We add work-life balance. So things like, does your supervisor support your time off, do you have time for things outside of work.",
      "Step three. We add employee engagement. This is OPM's official engagement index. It asks things like, are you energized by your work, do you feel like you contribute.",
      "And step four. We throw in demographics. Age, gender, tenure, whether you're a supervisor.",
      "At each step we measure R-squared, which basically tells us how much of the variation in satisfaction this set of variables can explain.",
    ],
    post: "Click to slide 6.",
  },
  {
    num: 6, title: "Surface finding — the 0.40 telework gap",
    time: "≈75 sec",
    pre: "Bar chart with 4 telework groups, callout box on the right.",
    lines: [
      "When we just looked at the raw averages — no model, no controls, just averages by telework status — we got this picture.",
    ],
    direction: "Point to the chart.",
    lines2: [
      "The green bar on the left is people who telework routinely. They average 3.94 on the satisfaction scale. The red bar is people required to be on-site. They average 3.54. So that's a gap of about 0.40 points on a 5-point scale.",
      "If you stop here, you'd say telework matters a lot. The remote workers are clearly happier.",
      "And honestly, this is what most of the news headlines about telework are based on. Just looking at raw averages.",
      "But this is where it gets interesting. Because what we want to know isn't 'are remote workers more satisfied.' It's 'is the telework itself causing the satisfaction.' Those are two different questions.",
    ],
    post: "Pause for effect. Then click to slide 7.",
  },
  {
    num: 7, title: "The twist — Simpson's Paradox",
    time: "≈75 sec",
    pre: "Coefficient flip chart, dark navy callout box on the right.",
    lines: [
      "Here's what happens when we actually run the model with controls.",
    ],
    direction: "Point to the chart. Walk through it slowly.",
    lines2: [
      "The red bars on the left are the original effect. Basically what we just saw. People required on-site look about 0.40 points lower. Infrequent teleworkers also slightly lower.",
      "The blue bars on the right are the same effect, but after we control for engagement and work-life balance. Look at what happened. The on-site coefficient flipped. It's not negative anymore. It's actually slightly positive.",
      "So what does this mean. It means the original gap from the previous slide wasn't really about where people work. It was about who happens to telework. People who telework routinely also tend to score higher on engagement and work-life balance. And those things are doing the work, not the location.",
      "This is called Simpson's Paradox. A relationship can flip sign when you account for confounders.",
    ],
    post: "Click to slide 8.",
  },
  {
    num: 8, title: "What actually matters — engagement explains 60%",
    time: "≈75 sec",
    pre: "R-squared progression bar chart, three big stat callouts on the right.",
    lines: [
      "Okay, so this slide is the headline of the whole project.",
      "Remember those four model steps. Here's how much of the variation in satisfaction each step explains.",
    ],
    direction: "Point to bars left to right.",
    lines2: [
      "Telework alone explains 2 percent. Just 2. Telework by itself is barely doing anything.",
      "Add work-life balance, we jump to 41 percent. Big jump.",
      "Add engagement, we go to 60 percent. Another big jump.",
      "And add all the demographics — age, gender, tenure, supervisor status — and we go from 60 to 60. They add basically nothing.",
      "So the takeaway is: where people sit barely matters. Their work-life balance and engagement matter a lot. Their demographics matter almost not at all.",
    ],
    post: "Click to slide 9.",
  },
  {
    num: 9, title: "Ranked drivers — engagement is 7× the next thing",
    time: "≈75 sec",
    pre: "Standardized coefficient chart, reading-guide panel on the right.",
    lines: [
      "Just to make sure that's not a fluke of how we built the variables, here's the same finding from a different angle.",
      "What you're seeing here are standardized coefficients. Every variable has been put on the same scale, so the bar lengths are directly comparable.",
    ],
    direction: "Point to the engagement bar.",
    lines2: [
      "Employee engagement is the green bar at the top. Its standardized effect is 0.71. The next biggest bar is required on-site, at 0.10. So engagement's effect is about seven times bigger than the next strongest variable.",
      "Work-life balance, choosing not to telework, age 40-plus — they all sit in roughly the same small range. Where you work barely shows up.",
      "And this is robust. We also ran a Random Forest and a Gradient Boosting model on the same data, and they all agreed. Engagement is the dominant signal.",
      "That's the answer to the first research question. Where you work isn't the lever. Engagement is.",
      "I'll let Chau take it from here for the second research question.",
    ],
    post: "Click to slide 10. Step back. Chau steps up.",
  },
];

const slideContent = slides.flatMap((s) => {
  const out = [...slideHeader(s.num, s.title, s.time)];
  if (s.pre) out.push(direction(s.pre));
  out.push(...(s.lines || []).map((l) => speakerLine(l)));
  if (s.direction) out.push(direction(s.direction));
  out.push(...(s.lines2 || []).map((l) => speakerLine(l)));
  if (s.post) out.push(direction(s.post));
  return out;
});

// ---------- Q&A and tips section ----------
const qaItems = [
  {
    q: "Why didn't you use ordinal logistic regression for the satisfaction outcome?",
    a: "We did consider it. With 500-thousand-plus observations, treating a 5-point Likert scale as continuous is standard practice in organizational research. We checked an ordinal logit on a subsample and the rank ordering of the effects was identical. So OLS gave us the same story with simpler interpretation.",
  },
  {
    q: "Could telework matter more for some subgroups, like supervisors?",
    a: "We tested an interaction between telework and supervisory status. The effect doesn't reach practical significance even there. Engagement still dominates in every subgroup we checked.",
  },
  {
    q: "Aren't engagement and satisfaction basically the same thing?",
    a: "They're correlated, around 0.75. But they're conceptually distinct. Engagement is about energy and absorption in the work itself. Satisfaction is about how you feel about the job overall. There's still 40 percent of the variance in satisfaction that engagement doesn't explain. So they're related but not redundant.",
  },
  {
    q: "Why is the on-site coefficient positive in the final model? Should we just make people come back to the office?",
    a: "Don't read it that way. The original 0.40 negative effect was being carried by engagement and work-life balance, not by location. Once we control for those, on-site doesn't penalize satisfaction. But that doesn't mean forcing people in would help. It means location wasn't really the driver in the first place.",
  },
  {
    q: "How do you handle missing data?",
    a: "Listwise deletion on the regression. We kept rows with complete data on all the model variables, which gave us about 519,000 observations. Plenty of statistical power.",
  },
  {
    q: "What about the survey weights, FEVS has them?",
    a: "Good question. We ran the analysis weighted as a robustness check and the headline R-squared changed by less than half a percent. We're presenting the unweighted version because it's simpler and the substantive findings don't depend on it.",
  },
];

const qaSection = [
  new Paragraph({ pageBreakBefore: true, children: [] }),
  heading("Q&A — be ready for these", HeadingLevel.HEADING_1),
  para("These are the most likely questions on your part of the talk. Practice answering them out loud at least once."),
  ...qaItems.flatMap((item, i) => [
    new Paragraph({
      spacing: { before: 240, after: 80 },
      children: [
        new TextRun({ text: `Q${i + 1}.  `, bold: true, color: GOLD,
                      font: "Calibri", size: 22 }),
        new TextRun({ text: item.q, bold: true, color: INK,
                      font: "Calibri", size: 22 }),
      ],
    }),
    speakerLine(item.a),
  ]),
];

// ---------- Delivery tips ----------
const tipsSection = [
  new Paragraph({ pageBreakBefore: true, children: [] }),
  heading("Delivery tips", HeadingLevel.HEADING_1),
  heading("Things to actually do", HeadingLevel.HEADING_2),
  bullet("Look up. Read a sentence, then look at the audience while you finish saying it. Reading off the laptop the whole time is the easiest way to lose them."),
  bullet("Slow down on the numbers. “Sixty-five percent.” Pause. Let the number land before you keep going."),
  bullet("Don't apologize. No “sorry I'm a bit nervous,” no “uh, I think this slide is...” Even if you're nervous, just keep going."),
  bullet("Don't read the entire slide aloud. The audience can read. Your job is the context the slide doesn't have."),
  bullet("Practice the handoff line at slide 9. “I'll let Chau take it from here.” Smooth handoffs make you look rehearsed even if you're not."),
  heading("Things to absolutely avoid", HeadingLevel.HEADING_2),
  bullet("“Like, basically...” used 30 times in 9 minutes."),
  bullet("“Um” between every sentence."),
  bullet("“Does that make sense?” unless you're actually asking."),
  bullet("Reading the chart axis labels word for word."),
  bullet("Apologizing for the design or the data."),
];

// ---------- Pre-flight checklist ----------
const checklistSection = [
  new Paragraph({ pageBreakBefore: true, children: [] }),
  heading("Pre-flight checklist", HeadingLevel.HEADING_1),
  para("Run through this the day before. The Mechanics rubric is 25 points and timing matters."),
  bullet("Read this transcript out loud once. Time yourself. Should land between 8:30 and 9:30."),
  bullet("Decide who clicks the slide remote. Probably whoever's about to talk."),
  bullet("Charge your laptop. Bring the adapter."),
  bullet("Have the .pptx open before class starts. Don't fumble with login on stage."),
  bullet("Both you and Chau read the Q&A section. Don't be the person who says “Karan handled that part.”"),
  bullet("Smile when you finish your last slide. Wait. Let the question come."),
  new Paragraph({
    spacing: { before: 480 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({
      text: "You've got this.",
      italics: true, bold: true, color: NAVY, size: 28, font: "Calibri",
    })],
  }),
];

// ---------- Build the document ----------
const doc = new Document({
  creator: "Karan Parekh",
  title: "Presentation Transcript - Remote Work and Federal Employee Satisfaction",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 36, bold: true, font: "Calibri", color: NAVY },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, font: "Calibri", color: INK },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({ text: "ADTA 5940 · Capstone · Spring 2026",
                          font: "Calibri", size: 18, color: MUTED }),
            new TextRun({ text: "\tKaran Parekh · Chau Le",
                          font: "Calibri", size: 18, color: MUTED }),
          ],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: "Calibri", size: 18, color: MUTED }),
            new TextRun({ children: [PageNumber.CURRENT],
                          font: "Calibri", size: 18, color: MUTED }),
            new TextRun({ text: " of ", font: "Calibri", size: 18, color: MUTED }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES],
                          font: "Calibri", size: 18, color: MUTED }),
          ],
        })],
      }),
    },
    children: [...cover, ...howto, ...slideContent, ...qaSection,
               ...tipsSection, ...checklistSection],
  }],
});

const out = path.join(__dirname,
                     "Presentation_Transcript_Karan.docx");
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(out, buf);
  console.log(`Saved: ${out} (${buf.length} bytes)`);
});
