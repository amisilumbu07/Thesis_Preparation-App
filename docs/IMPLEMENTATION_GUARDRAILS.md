# Implementation Guardrails: 3 Steps

Follow these in order. Do not start a step until the previous step's exit gate passes.

## Step 1: Ground Truth (thesis extraction and reconciliation)

Goal: establish the final thesis as the only authority before any content exists.

1. Read `docs/lookback-design.html` completely.
2. Extract text: `pdftotext -layout thesis/final-thesis.pdf thesis/thesis.txt` (fallback: Python `pdfplumber`). Fix broken hyphenation, merged columns, and garbled formulas.
3. Build `thesis/sections.json` (section number -> heading + full text).
4. Build `thesis/facts.json` (every taught number: metrics, split, VRAM, training times, parameter counts, patch settings, datasets, models), each with section number and the exact source sentence.
5. Write `thesis/reconciliation.md`: compare facts against design doc section 4 register. List conflicts still present, fixed, and new. List every design-doc vs. final-thesis disagreement.
6. Write `scripts/verify.js` (checks anchors exist in `sections.json`, `evidence` appears verbatim in the thesis text, source files exist).

Guardrails:
- The final thesis wins over the design doc. Never invent thesis numbers.
- Missing or blank value in `content/decisions.json` -> mark the item "open"; do not guess.

Exit gate: STOP and show `thesis/reconciliation.md` to the user. Do not generate cards until they respond.

## Step 2: Content (data only, no UI)

Goal: build validated study content in `content/*.json` per design doc section 11.

1. Create `concepts.json`, `cards.json`, `sources.json`, `register.json` from the seed material: six pillars (3), register (4), STEEL case file (5), stability thread (6), source shelf (7), five stress-test questions (8).
2. Every card and concept carries `thesisAnchors` (present in `sections.json`) and an `evidence` field (short verbatim excerpt).
3. Every card references a thesis section and a source id. Every source points to a PDF in `sources/` with a page or table locator.
4. Sources marked "verify" keep that status in the data.
5. Run `node scripts/verify.js` after every content change; fix all failures before continuing.

Guardrails:
- No invented numbers; unresolved conflicts stay "open".
- No UI work in this step.

Exit gate: `node scripts/verify.js` passes with zero failures. Summarize what exists and how to test it.

## Step 3: App (phases 1-3 of design doc section 13)

Goal: build the single-page app, phase by phase.

1. Stack: plain HTML, CSS, vanilla JS. No framework, no build step. Must work by opening `index.html` directly or via `npx serve .` (offline).
2. Files: `index.html`, `app.js`, `styles.css`, reusing the color and font tokens from the design doc's `<style>` block.
3. Features: home, concept atlas, concept page, reading room, drill, mock viva, derivation lab, vulnerability register, source shelf (section 10); mastery ladder, card types, SM-2-style scheduling with risk weighting, readiness score (section 9); relaxed and intensive modes (section 2).
4. Progress in localStorage, with JSON export and import buttons on home.
5. Keyboard: 1-4 rate a card, space reveals. Light and dark themes. Respect `prefers-reduced-motion`. Show "verify" and "open" statuses in the UI.
6. Write a short `README.md` with run instructions.

Guardrails:
- Phase 4 (AI examiner, voice) is out of scope.
- Build phase by phase; after each phase, stop, summarize what works and how to test it, then wait.
- Re-run `node scripts/verify.js` whenever content changes.
- Test in a browser (golden path and edge cases) before reporting a phase complete; if it can't be tested, say so.

Exit gate: all phases 1-3 demonstrated working, verify passes, README present.
