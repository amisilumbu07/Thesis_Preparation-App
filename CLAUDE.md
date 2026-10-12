# Lookback: thesis-defense study app

## What to build
A single-page study app for defending the thesis "Time Series Load Forecasting using Transformers".
The full design is in `docs/lookback-design.html`. Read it completely before writing code.
Build phases 1–3 from section 13 of the design doc. Phase 4 (AI examiner, voice) is out of scope for now.

## Hard requirements
- Plain HTML, CSS and vanilla JavaScript. No framework and no build step.
- Must work offline by opening `index.html` directly or via `npx serve .`
- Study content lives in `content/*.json` (concepts, cards, sources, register), following the schema in design doc section 11.
- Progress is stored in localStorage, with JSON export and import buttons on the home screen.
- Two modes (design doc section 2): relaxed reading room and intensive viva drill.
- Mastery ladder, card types, SM-2-style scheduling with risk weighting, and readiness score (section 9).
- Screens and flows as in section 10: home, concept atlas, concept page, reading room, drill, mock viva, derivation lab, vulnerability register, source shelf.
- Keyboard: 1–4 to rate a card, space to reveal the answer. Light and dark themes. Respect prefers-reduced-motion.
- Reuse the visual tokens (colors and fonts) from the design doc's `<style>` block so the app matches it.

## Source of truth
The final thesis in `thesis/` is the only authority on thesis content. The design doc was written from an earlier draft;
where the two disagree, the final thesis wins, and you must list every disagreement you find.

Before building any content (phase 1, step 0):
1. Extract the text of the final thesis PDF: `pdftotext -layout thesis/final-thesis.pdf thesis/thesis.txt`
   (pdftotext comes with poppler-utils; if it is not installed, use Python `pdfplumber` instead). Check the output for
   broken hyphenation, merged columns and garbled formulas, and clean these up so section headings and numbers read correctly.
2. Build `thesis/sections.json`: a map from section number (e.g. "4.4.3") to its heading and full text.
3. Extract every number the app will teach (metrics, split, VRAM, training times, parameter counts, patch settings,
   dataset list, model list) into `thesis/facts.json`, each with its section number and the exact sentence it came from.
4. Compare `facts.json` against the vulnerability register in the design doc (section 4). Write `thesis/reconciliation.md`
   listing which conflicts still exist in the final version, which were fixed, and any new ones. Stop and show me this file
   before generating cards.

## Content rules
- Every card and concept must carry `thesisAnchors` (section numbers present in `sections.json`) and an `evidence` field:
  a short exact excerpt from that section supporting the model answer.
- Every source reference must point to a PDF in `sources/`, with a page or table locator.
- Write `scripts/verify.js` (run with `node scripts/verify.js`). It fails if any anchor is missing from `sections.json`,
  any `evidence` excerpt is not found verbatim in the thesis text, or any source file is missing. Run it after every
  content change and fix all failures before continuing.
- Seed content comes from the design doc: the six pillars (section 3), vulnerability register (4), STEEL case file (5), stability thread (6), source shelf (7), and the five stress-test questions (8).
- Every card must reference a thesis section and a source id.
- Sources marked "verify" must keep that status in the data and show it in the UI.
- Do not invent thesis numbers. Where the register lists conflicting values, use the value in `content/decisions.json`; if that file is missing or a value is blank, show the item as "open" rather than guessing.

## Project layout
```
index.html
app.js
styles.css
content/
  concepts.json
  cards.json
  sources.json
  register.json
  decisions.json   <- filled in by the author
docs/
  lookback-design.html
thesis/
  final-thesis.pdf    <- the FINAL version (required)
  figures/            <- exported thesis figures (Fig 4.1 ... 4.8)
sources/
  *.pdf               <- the papers the thesis cites
scripts/
  verify.js
```

## Working style
- Build phase by phase. After each phase, stop and summarize what works and how to test it.
- Write a short README with run instructions.
