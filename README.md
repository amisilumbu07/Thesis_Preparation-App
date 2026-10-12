# Lookback

Study app for defending the thesis *Time Series Load Forecasting using Transformers*.
Plain HTML, CSS and JavaScript. No framework, no build step, works offline.

## Run
- Open `index.html` in a browser (double-click), or run `npx serve .` and open the URL.
- Progress is saved in your browser (localStorage). Use **Export JSON** / **Import JSON** on the home screen to back it up.

## Use
- **Home**: due and new cards, days left, progress per pillar.
- **Concepts**: every concept with its mastery level. Open one to read the story, the thesis quote (with the full section, quote highlighted), the sources, and all its cards.
- **Study**: *Reading room* (relaxed: recognition questions, no pressure) or *Viva drill* (intensive: blank prompts, self-graded). Space reveals the answer, keys 1-4 rate it (Again, Hard, Good, Easy). Multiple-choice cards use keys 1-4 to pick an option. Scheduling is SM-2 style, weighted towards risky concepts and capped so cards return before the end of the study window.
- **Mock viva**: five hostile committee questions. Answer in writing (90 s, 120 s for the last), then tick the rubric points you made. A score of 75% or more draws the follow-up; struggling with it costs 15 points. 80% passes. Attempts are saved, and each answer updates that card's schedule.
- **Lab**: the derivation lab. *Thesis derivations* are 14 exercises, one per derivation card (patch counts, attention cost, split arithmetic, percentage gains, size and time ratios). Type the numbers (commas, %, x are fine); each check has a stated tolerance and shows its working. First-try correct counts as Good, retries as Hard, showing the answers as Again, and the card's schedule updates. *Practice generator* makes unlimited fresh problems (patches, ratios, improvement %, splits) from the thesis results tables and keeps a tally.
- **Readiness** (Home): share of concepts defended (level 3, or all cards passed when a concept has no level-3 card), minus 3 points per unresolved high-severity register item and 5 per pillar below 60%. Also shows the definition of done and your weakest concepts.
- **Register**: places where the thesis disagrees with itself, with your decisions and a box to record a rehearsed answer.
- **Sources**: the cited papers in `sources/`, with page locators. Items marked *verify* keep that status.
- Light and dark themes (Theme button); reduced motion is respected.

## Content
Content lives in `content/*.json` and is checked against the final thesis.

    node scripts/verify.js     # anchors, verbatim evidence, source files and pages, data.js freshness
    python3 scripts/build_lab.py regenerate content/lab.json if lab exercises change
    node scripts/bundle.js     # regenerate content/data.js after any content change

`content/data.js` is generated (browsers block `fetch` on `file://`). Author decisions are in `content/decisions.json`; open and unresolved items show as *open* in the app.

## Not built yet
The 45-minute session structure with warm-up and review, and the AI examiner (phase 4).
# Thesis_Preparation-App
# Thesis_Preparation-App
