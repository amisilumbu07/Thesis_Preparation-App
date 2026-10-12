# Reconciliation report (Step 1)

Source of truth: `thesis/final-thesis.pdf` (90 pages), extracted to `thesis/thesis.txt`, split into 58 sections in `thesis/sections.json`, with 77 quoted facts in `thesis/facts.json` (every quote checked programmatically). Compared against `docs/lookback-design.html` (v0.1, written from an earlier draft). Author decisions are now in `content/decisions.json` (answers of 2026-09-25). Items still without an answer show as **open**.

## Summary

- Of the 10 register items in design doc section 4, **6 are fixed**, **2 are partly fixed** and **2 still exist**.
- The final thesis corrects its own STEEL mechanism. This **invalidates several design-doc statements**: the STEEL case file (section 5), the section 1 claims, and stress-test Q1 (section B).
- There are **27 conflicts inside the final thesis** (section C). Author answers resolved C1, C2, C3, C11 and C13 (what the thesis text must change) and exposed C20-C27, mostly about the London data and the citation numbers.

## A. Design-doc vulnerability register (section 4) vs final thesis

| # | Register item | Status in final | Evidence in final thesis |
|---|---------------|-----------------|--------------------------|
| A1 | STEEL: failed or improved? | **Fixed** | 4.4.3 and 5.1 consistently report NaN from epoch 1 for Informer and Autoformer only. No clipping/pruning/stabilisation claim (no "clip" in the text) and no 27.9% figure. The design doc's suggested "stabilised rerun" does not exist in the thesis. |
| A2 | Data split 60/20/20 vs 70/20/10 | **Fixed** | 70/20/10 in 3.3, 3.7, 4.1. No 60/20/20 anywhere. Window counts sum exactly (12,177 + 3,479 + 1,740 = 17,396). |
| A3 | GPU memory 3.8-8.5 GB on a 6 GB card | **Fixed by removal, but a gap remains** | The 3.8-8.5 GB figures are gone. But the thesis says peak VRAM was recorded (3.5.3, 3.6.2) and reports no VRAM number besides the 6GB budget (C13). |
| A4 | Speed ratio (3-5x, 4-6x, 22-42x; 48,000-68,000 s) | **Partly fixed** | Results tables now give real times. But "exceeding 68,000 seconds" is still in 3.4.1 (C1), and 4.6.3 now says "three to twenty-five times" (C9). |
| A5 | Parameter ratio (155-1,600x; GRU 15K vs PatchTST 6.2M) | **Fixed** | No such figures remain. The parameter tables now show PatchTST at 9,120-399,744 parameters, which reverses the design doc's premise (B3). |
| A6 | Patch configuration (S = 4 vs 11 patches) | **Still exists** | 4.2.1 says P16/S4; 3.4.1 says P16/S8; 4.3 says about 11 patches (matches S8). See C11. |
| A7 | Normalization (instance vs global vs RevIN) | **Fixed** | 3.3 and 4.2 describe StandardScaler fitted on the training partition; 4.2.2 describes RevIN inside PatchTST. The "instance normalization per sequence" in the methodology is gone. The layered description is implicit; it would help to state it in one sentence. |
| A8 | Scope: hybrids, FEDformer, 3 vs 4 datasets, LCL-ECD | **Partly fixed** | Fixed: FEDformer explicitly "not among the models empirically evaluated" (2.4.4); four datasets everywhere; LCL-ECD gone; 2.5 no longer promises hybrids (they are future work, 5.2). Still open: "all seven models on each of the four datasets" (3.2.1, 3.5.2, 3.7) vs three-model runs on WTH and ETTh1 (C10). |
| A9 | Orders of magnitude (10^7 vs 7 orders) | **Fixed** | 3.2.3 and 4.4.3 both say "roughly six to seven orders of magnitude". The design doc's "seven" is not what the thesis says. |
| A10 | Accuracy headline (~26.6%, 25-28%, 27.9%) | **Fixed, replaced by new numbers** | Headline figures are now 57.6 / 76.0 / 50.4% (Smart Meters, reproduce from Table 4.4) and 13.6-25.9% (ETTh1, which do **not** reproduce, C3). |

## B. Other places where the design doc disagrees with the final thesis

The design doc was written from an earlier draft. Where they disagree, the final thesis wins. These design-doc items need rewriting before they become cards.

| # | Design doc location | Design doc says | Final thesis says |
|---|---------------------|-----------------|-------------------|
| B1 | Section 1, section 5, Q1 | "Every Transformer collapsed to NaN on STEEL"; Q1 asks why PatchTST "collapse[d] on STEEL" | Only **Informer and Autoformer** collapsed. PatchTST trained successfully in both runs (Table 4.3: MAE 0.0766, MSE 0.0100, RMSE 0.1000; the lowest MSE and RMSE of all seven models). Q1's premise is wrong. Rewrite it as: why did Informer/Autoformer fail while PatchTST and every RNN survived? |
| B2 | Section 5 (whole case file) | Mechanism = StandardScaler overwhelmed, softmax exponent > float32 limit, step transitions | 4.4.3 explicitly **supersedes** this: it calls softmax overflow "an unlikely primary cause on its own" and gives a **bounded-activation** account instead (sigmoid/tanh gates bound RNNs; PatchTST's attention is within-channel; Informer/Autoformer compute unbounded cross-channel attention/auto-correlation). 1.5 says the mechanism is a hypothesis pending ablations. The design doc's diagnostics (fp16, clipping, RobustScaler, anomaly detection) are not in the thesis. The thesis lists only "instrument attention-logit magnitudes" and "robust scaling" as future work (5.2). |
| B3 | Section 1 | PatchTST "most accurate and most VRAM-efficient on WTH, ETTh1 and London"; Transformers buy "25-28% lower error at the price of far more parameters, memory and training time than RNNs" | PatchTST is **not** best on WTH (Informer wins MAE/MSE/RMSE). No VRAM numbers exist. RNN vs Transformer comparison exists only on STEEL and Smart Meters; on Smart Meters PatchTST has the fewest parameters of all seven (9,120). Informer is worse than most RNNs on MAE there. |
| B4 | Section 3 pillar D | EfficientLSTM "~8-10K params"; "Thesis Figs 3.11-3.14" | 3.4.2 and Ch. 4: called **LSTM-16** (EfficientLSTM only in logs), 4,456 (STEEL) to 13,424 (Smart Meters) parameters. Recurrent figures are 3.10-3.13. |
| B5 | Section 3 pillar F | "Figs 4.7-4.8" for the findings | 4.7-4.8 are WTH. STEEL is 4.11-4.13; Smart Meters is 4.14-4.15. |
| B6 | Section 3 pillar E | batch 8 vs 32 | Also **16** for Transformers on Smart Meters (3.5.2). |
| B7 | Section 6 (RevIN row) | Cites PatchTST's Table 11: RevIN helps only slightly | The thesis (4.2.2) calls RevIN "a critical component" for non-stationary energy data. This is a tension between the source and the thesis's wording that a committee may probe. The thesis does not report its own RevIN ablation. |
| B8 | Section 8 Q4 | "apparently one seed" | The thesis never states the number of seeds or runs, and reports no significance test. Open: you need to say what was actually run. |
| B9 | Section 7 (source shelf) | 8 "verify" external works | Cited in the final thesis reference list: Kim RevIN [13], Han et al. [11], iTransformer [30], Crossformer [29], Micikevicius [44]. **Not** in the thesis references: Liu et al. 2022 (Non-stationary Transformers), Dehghani et al. 2023, Wortsman et al. 2023. All keep "verify" status until the PDFs are in `sources/`. |

Confirmed consistent with the final thesis: hero figure (L96, 11 patches, P16, S8, H24), derivation card (11 patches; 96^2/11^2 about 76x), 10-epoch training budget, 1 layer / 16 hidden LSTM-16, FEDformer reviewed but not run, DLinear (Zeng et al.) discussed in 2.4.6 but not a baseline (Q5 follow-up holds), four datasets.

## C. Conflicts inside the final thesis

Severity: **H** = a stated number or claim is contradicted by the thesis's own tables; **M** = inconsistent statements; **L** = editorial.

| # | Sev | Where | Claim | What the thesis's own data shows |
|---|-----|-------|-------|----------------------------------|
| C1 | H | 3.4.1 | Autoformer had "the longest training duration among all tested models, exceeding 68,000 seconds" | Largest Autoformer time in any table is 10,694.7 s (Table 4.4). Informer is longer (11,119.1 s). 68,000 s appears nowhere else. (Leftover from the earlier draft's 48,000-68,000 s.) |
| C2 | H | 3.4.1 | PatchTST "achieved the best performance ... producing an MSE of 18.38" | PatchTST MSE is 0.4871 (WTH), 0.3742 (ETTh1), 0.0100 (STEEL), 20.1874 (Smart Meters). 18.38 matches none. PatchTST is also not best on WTH. |
| C3 | H | 4.4.2, 5.1 | PatchTST beats Informer on ETTh1 by 13.6% (MAE), 25.9% (MSE), 13.8% (RMSE); 5.1: "13.6-25.9% better" | From Table 4.2: 15.7% (MAE), 33.8% (MSE), 18.6% (RMSE). The stated percentages don't reproduce. (The Smart Meters figures 57.6 / 76.0 / 50.4% do reproduce.) |
| C4 | H | Abstract, 4.4.2, 4.6.1, 4.6.3 | Informer is "consistently the fastest ... on every dataset" / "fastest of the three Transformers on every dataset examined" | True on WTH (1,100.9 s) and ETTh1 (525.6 s) only. STEEL: PatchTST 173.7 s vs Informer 502.0 s. Smart Meters: PatchTST 3,905.5 s vs Informer 11,119.1 s. |
| C5 | M | 3.4.1 vs Table 4.1 | PatchTST "trains significantly faster than the Autoformer" | Not on WTH: PatchTST 1,452.7 s vs Autoformer 1,252.3 s. True on the other three datasets. |
| C6 | M | 3.4.2 | LSTM-16 is "consistently the smallest of any model tested" | On Smart Meters PatchTST has 9,120 parameters, fewer than LSTM-16's 13,424 (4.5 itself says PatchTST is "the fewest of any model"). |
| C7 | M | 3.7, 3.2.4, 4.5 | Smart Meters Transformer training "required over three hours per model"; "each Transformer epoch took 55-70 minutes" | Informer 11,119 s = 3.09 h; Autoformer 10,694.7 s = 2.97 h (under three hours); PatchTST 3,905.5 s = 1.08 h (about 22 min/epoch). |
| C8 | M | 4.4.3 | Failing Transformers are "only two to ten times larger than the successful recurrent models" | From Table 4.3 the ratios are 4.8x to 19.8x. |
| C9 | M | 4.6.3 | Recurrent models train "three to twenty-five times faster than any Transformer" | Table-derived range is 3.6x (BiLSTM vs PatchTST, STEEL) to 19.4x (Autoformer vs LSTM-16, STEEL). No 25x anywhere. |
| C10 | M | 3.2.1, 3.5.2, 3.7 vs 3.7, 4.1, 5.2 | "all seven models" trained on "each of the four datasets"; no failure on WTH "for any of the seven models" | 3.7 itself says WTH and ETTh1 were three-model runs; 5.2 lists the recurrent comparison on WTH and ETTh1 as outstanding. Only STEEL and Smart Meters have all seven. |
| C11 | M | 3.4.1 vs 4.2.1 | Patch settings: P16/S8 (3.4.1); P16/S4 (4.2.1) | 4.3 says 96 steps become about 11 patches, which fits S8 ((96-16)/8+1 = 11). S4 gives 21. The patch length and stride actually run are never stated. |
| C12 | M | 3.5.2 vs 4.4.3 | Early stopping (patience 7 for Transformers) halted the failed STEEL runs | 4.4.3 says NaN losses persisted "for all ten epochs attempted". With patience 7, early stopping would end the run before epoch 10. Epochs actually run are not reported. |
| C13 | M | 3.5.3, 3.6.2 vs Ch. 4 | Peak VRAM "was recorded ... for every run" and is a key metric | No VRAM figure appears in any results table. |
| C14 | M | 1.3 (RQ1) | Baselines are "LSTM, BiLSTM, GRU" (three) | Everywhere else there are four recurrent baselines (adds LSTM-16). |
| C15 | L | 3.3, 4.1 | ETTh1: 17,420 samples, "17,396 usable windows" | Split arithmetic is exact. But 17,420 - 96 - 24 + 1 = 17,301 would be the usual window count; 17,396 = 17,420 - 24, so the lookback does not appear to be subtracted. Worth a one-line explanation. |
| C16 | L | 4.4.2 (PDF pp. 70-71) | Duplicated paragraph ("The qualitative evidence reinforces this ranking...") spliced into the middle of the "dataset-conditional" sentence | Present in the PDF itself, not an extraction artefact. |
| C17 | L | 3.4.1, 3.4.2 | Figure cross-references "Figure 3.4/3.5/3.6/3.7" for the recurrent cells; "Figure 3.1" for the vanilla Transformer | Actual numbers are 3.10 / 3.11 / 3.12 / 3.13 and 3.2. Left over from earlier numbering. |
| C18 | M | 5.2 vs 3.2.4, 4.5 | 5.2 proposes federated learning "for genuinely individual (rather than aggregated) household-level smart-meter data" | 3.2.4 and 4.5 describe the Smart Meters data as household-level readings ("household-level noise", "household energy consumption"). Whether the data used was aggregated or per-household is unclear. This is exactly the question design-doc Q1 asks. |
| C19 | M | 3.4.2 | BiLSTM has "approximately double the parameter count **and training time**" of LSTM | Parameters: 2.0-2.1x (18,185 vs 8,632; 38,097 vs 18,816), fine. Training time: only 1.24-1.27x (48.7 s vs 38.3 s; 1,592.2 s vs 1,279.4 s). |

| C20 | H | 3.2.4, 3.3, 5.2 vs reference list | In-text citations: London dataset [36]; StandardScaler [37]; TFT [30]; robust scaling [59]; TinyML [61]; interpretability [58, 64]; continual learning [62]; deployment [65] | [36] and [37] are session-based-recommendation papers (GNN, STAMP), unrelated to London data or StandardScaler. [30] is iTransformer (no TFT entry). [59] is the TinyML book (robust scaling is Huber, [58]); [61] is Gneiting (TinyML is [59]); [62] is LIME (continual learning is [60]); [64] and [65] do not exist (63 references). No entry cites the Low Carbon London source. |
| C21 | H | 3.3, 4.1 vs author's code (D-london-data) | Chronological, non-shuffled 70/20/10 split "consistent across all four datasets" | London was split **by household** (100 test households, then 20% of the rest for validation). Row counts 2.73M / 0.68M / 66k are about 78.5 / 19.6 / 1.9%. Not 70/20/10, not chronological. (Author-reported from code, not verifiable in this repo.) |
| C22 | H | 3.2.4, 4.1, 3.3 vs author's code | London: "half-hourly" readings, "over 3.4 million readings"; Lookback 96, Horizon 24 "consistent across every dataset" | The model input is **daily** per-household records: lookback 96 = 96 **days**, horizon 24 = 24 **days**. 4.1's "daily and sub-daily cycles" does not apply to London. The ">3.4 million" figure matches the daily row total (2.73M + 0.68M + 0.066M = 3.48M), not half-hourly readings. |
| C23 | M | Limitations vs author's code | (not disclosed) | Households are concatenated into one table and windows are slid across it, so some 96-day windows span two households. Needs a line in 1.5 or 4.5. |
| C24 | M | 3.5, 3.7, 1.5 | Results presented as comparisons of models | Each result is a **single run with no seeds** (author). No significance test. Differences such as Informer vs Autoformer on ETTh1 may be within seed variance. (Design-doc Q4.) |
| C25 | L | 3.5.1, 4.4.1 vs author's runs | "10-epoch training budget"; London capped at 3 epochs because Transformer epochs took 55-70 minutes (4.5) | Autoformer on ETTh1 stopped at epoch 9 by early stopping (not disclosed). The London script comment says the cap was "for faster testing", not a time necessity. |
| C26 | L | 4.3 vs Tables 4.1, 4.2 | "On WTH, PatchTST converged in 180 seconds ... and on ETTh1 in 156 seconds" | Table 4.1 gives 1,452.7 s (WTH) and Table 4.2 726.4 s (ETTh1) for PatchTST. The 180 s / 156 s figures presumably come from different (calibration) runs that are not reported. Author to confirm. |
| C27 | M | 4.3 / 4.2.1 vs author's code | "approximately 11 patches" and P16 as the PatchTST setting for all datasets | STEEL used patch 12 / stride 6 = 15 patches (author). Not stated in the thesis. WTH setting unknown (open). |

Checked and consistent (no action): 70/20/10 split arithmetic; Smart Meters gains 57.6 / 76.0 / 50.4% (recomputed 57.56 / 75.95 / 50.37); STEEL "MAE 0.071-0.083" and PatchTST RMSE "roughly half" of best recurrent (0.1000 vs 0.1893); LSTM-16 fastest and least accurate on Smart Meters; the "roughly two orders of magnitude larger than ETTh1" claim (about 195x).

## Impact on card generation

- Cards teach **table values**, never the erroneous prose values (C1, C2, C3, C4, C8, C9, C19).
- Register deck: A6 and C1-C4, C10-C13, C18 become register items. Fixed items A1, A2, A5, A7, A9, A10 can be recorded as "fixed" with the final-thesis evidence.
- STEEL case file, pillar F and Q1 are rewritten around the bounded-activation account (B1, B2).
- No VRAM number beyond the 6GB budget can be taught (C13); the patch length and stride are "open" (C11).
- Sources marked "verify" keep that status and show it in the UI.

## Decisions received (2026-09-25) and what is still open

| Ref | Decision | Status |
|-----|----------|--------|
| C11 / C27 | ETTh1 16/8 (11 patches), London 16/8, STEEL 12/6 (15 patches); WTH not given | Decided; **WTH open** |
| C1 / C2 | Delete 68,000 s and MSE 18.38 (not in any saved run) | Decided |
| C3 | Table 4.2 values stand: vs Informer 15.7 / 33.8 / 18.6%; the thesis's 13.6 / 25.9 / 13.8% are vs the mean of Informer and Autoformer (I recomputed and confirmed). Run 180948 is the ETTh1 run; run 165839 is the WTH run | Decided |
| C4 | Informer fastest only on WTH and ETTh1 (from the tables) | Derived; author confirmation pending |
| C13 | No VRAM measured; repo doc figures (V100 32 GB, per-model GB) are unsupported | Decided |
| C18 / C21-C23 | London: daily per-household records, split by household, concatenated, windows can cross households | Decided; thesis text must change |
| C24 / C25 | Single run, no seeds; London 3 epochs; Autoformer ETTh1 stopped at epoch 9 | Decided |
| C20 | Fix the in-text citation numbers | **Open** |
| C26 | Which run gave PatchTST 180 s / 156 s | **Open** |
| C12 | How many epochs the STEEL Informer/Autoformer runs actually ran (NaN "for all ten epochs" vs early stopping) | **Open** |
| Defense date | Author gave a study window 27 Sep-10 Oct 2026, 3 h/day, not a defense date | **Open** (scheduler uses 10 Oct as the end date) |

Files: the newer thesis is `Final Thesis For Submission_Espoir (1).pdf` (90 pages, 9 Sep). `Final Thesis For Submission.pdf` in Downloads is an older 63-page version from 28 Aug and was not used.

Sources: see `content/decisions.json` D-sources. 37 cited papers downloaded to `sources/`; Kim et al. (RevIN) and Crossformer could not be downloaded (OpenReview returned 403) and still need to be added by hand.
