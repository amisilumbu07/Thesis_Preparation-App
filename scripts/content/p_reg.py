from content_lib import concept, card, reg

TH = 'thesis'
N = 'nie2023patchtst'

concept('C-register', 'R', 'Vulnerability register',
 'Places where the thesis disagrees with itself, with its own tables or with the author\'s code. A committee member who reads closely will find them. Each item is either fixed, decided by the author (the thesis text still has to change) or open (a rehearsed answer is needed). These cards stay at the top of every intensive session.',
 ['1.5'], ('1.5', 'Hyperparameters were held fixed across comparable model categories'), [TH], 1.0)

def R(id, title, sev, status, conflict, anchors, evidence, decision, resolution, level=3):
    reg(id, title, sev, status, conflict, anchors, evidence, decision, resolution)
    open_ = None
    if status == 'open':
        open_ = {'decisionId': decision, 'reason': 'Register item is open: the author has not settled this.'}
    prompt = f'{title}. What do the different passages say, which is correct, and what do you say if a committee member asks?'
    card('C-register', 'register', level, prompt, resolution, conflict, evidence, TH, '§' + anchors[0], anchors=list(anchors), decisionId=decision, open=open_,
         note=f'Register item {id} ({sev}, {status}).')

# ---- decided by the author (thesis text still to change) ----
R('R-unsupported-numbers', 'Numbers in 3.4.1 that no result supports (68,000 s, MSE 18.38)', 'high', 'decided',
  ["3.4.1: Autoformer had the longest training duration, 'exceeding 68,000 seconds'", "3.4.1: PatchTST 'producing an MSE of 18.38'", 'Tables 4.1-4.4: longest Autoformer run 10,694.7 s; PatchTST MSE 0.4871 / 0.3742 / 0.0100 / 20.1874'],
  ['3.4.1'], [('3.4.1', 'exceeding 68,000 seconds'), ('3.4.1', 'producing an MSE of 18.38')], 'D-unsupported-numbers',
  'Decided: delete both. No saved run contains either value (the author searched the repo); they date from an earlier draft. Use the tables: longest run 11,119.1 s (Informer, Smart Meters); PatchTST MSE 0.4871 / 0.3742 / 0.0100 / 20.1874.')
R('R-etth1-percentages', 'ETTh1 improvement percentages (13.6 / 25.9 / 13.8 vs 15.7 / 33.8 / 18.6)', 'high', 'decided',
  ["4.4.2: 13.6% MAE, 25.9% MSE, 13.8% RMSE 'over Informer'", '5.1: repeated as 13.6-25.9% better than Informer', 'Table 4.2: over Informer alone the gains are 15.7% / 33.8% / 18.6%'],
  ['4.4.2', '5.1'], [('4.4.2', 'a 13.6% improvement in MAE and a 25.9% improvement in MSE over Informer'), ('5.1', 'achieving the lowest MAE, MSE, and RMSE (13.6–25.9% better than Informer)')], 'D-etth1-percentages',
  'Decided: Table 4.2 stands. Over Informer: 15.7 / 33.8 / 18.6%. Over Autoformer: 11.5 / 15.9 / 8.3%. The thesis figures 13.6 / 25.9 / 13.8% are the gains over the mean of Informer and Autoformer. State the baseline or use the Informer figures; cite run three_models_comparison_ett_20260903_180948 (the run ending 165839 is the WTH run).')
R('R-patch-config', 'PatchTST patch length and stride', 'medium', 'decided',
  ['3.4.1: patch 16, stride 8', '4.2.1: patch 16, stride 4', '4.3: about 11 patches (fits stride 8)', "Author's code: ETTh1 and London 16/8 (11 patches); STEEL 12/6 (15 patches); WTH not given"],
  ['3.4.1', '4.2.1'], [('3.4.1', 'grouping 16 consecutive time steps into a single patch with a stride of 8'), ('4.2.1', 'by grouping 16 time steps into a single patch with a stride of 4')], 'D-patch-config',
  'Decided: runs used 16/8 on ETTh1 and London and 12/6 on STEEL (a deliberate override, 15 patches). 16/4 in 4.2.1 is an illustration and must be labelled so. The thesis never states the STEEL override. The WTH setting is still open.')
R('R-vram', 'VRAM: recorded, but never reported', 'high', 'decided',
  ['3.5.3 and 3.6.2: peak memory occupancy recorded for every run and a key metric', 'Chapter 4: no VRAM figure in any table', "Author: no memory logging exists in the code; repo docs quoting a V100 32 GB and per-model GB figures are unsupported"],
  ['3.5.3', '3.6.2'], [('3.5.3', 'peak memory occupancy were recorded alongside predictive accuracy for every run')], 'D-vram',
  'Decided: no VRAM was measured. Remove the claim that it was recorded (or measure peak allocated memory and report it). The only VRAM figure to teach is the 6GB budget. Statements such as "least memory-intensive" are qualitative.')
R('R-london-data', 'London Smart Meters: half-hourly and chronological, or daily and by household?', 'high', 'decided',
  ['3.2.4 and 4.1: half-hourly readings, over 3.4 million', '3.3: chronological 70/20/10 split across all datasets', "Author's code: daily per-household records; split by household (100 test households); 2.73M / 0.68M / 66k rows; lookback 96 = 96 days; windows can span two households", '5.2 speaks of aggregated versus individual household data'],
  ['3.2.4', '3.3', '4.1'], [('3.2.4', 'The dataset contains half-hourly electricity consumption readings for a sample of London households'), ('4.1', 'over 3.4 million half-hourly residential readings prior to windowing'), ('3.3', 'consistent across all four datasets')], 'D-london-data',
  'Decided: describe it as daily, per-household records, split by household and concatenated for windowing; not aggregated across households. Correct 3.2.4, 3.3 and 4.1, state lookback and horizon in days, and add the window-crossing limitation.')
R('R-single-run', 'One run per result, no seeds, no significance test', 'medium', 'decided',
  ['Chapter 4 ranks models as if results were stable', 'Author: one run per model per dataset; no seeds set (only the London household split uses seed 42)', "Repo docs claiming 54 experiments and ~380 GPU hours are unsupported"],
  ['4.4.2', '1.5'], [('4.4.2', 'PatchTST emerges as the definitive winner across every accuracy metric evaluated')], 'D-seeds-runs',
  'Decided: add a caveat that every figure is a single run, so small gaps (Informer vs Autoformer on ETTh1) may lie within seed variance. Large margins (ETTh1 MSE 0.3742 vs 0.5652; Smart Meters 20.19 vs 38.67) are unlikely to be noise.')
# ---- open ----
R('R-informer-fastest', '"Informer is fastest on every dataset"', 'high', 'open',
  ['4.4.2, 4.6.1, 4.6.3 and the abstract: fastest Transformer on every dataset', 'Tables: true on WTH (1,100.9 s) and ETTh1 (525.6 s)', 'STEEL: PatchTST 173.7 s vs Informer 502.0 s; Smart Meters: PatchTST 3,905.5 s vs Informer 11,119.1 s'],
  ['4.6.1', '4.6.3'], [('4.6.1', 'Informer is the fastest of the three Transformers to train on every dataset examined in this chapter'), ('4.6.3', 'training fastest on every dataset examined')], 'D-informer-fastest',
  'Derived from the tables (author confirmation pending): restrict the claim to WTH and ETTh1. Also note PatchTST is slower than Autoformer on WTH (1,452.7 s vs 1,252.3 s), so "PatchTST trains faster than Autoformer" (3.4.1) fails there too.')
R('R-seven-models-each', '"All seven models on each of the four datasets"', 'medium', 'open',
  ['3.5.2 and 3.7: all seven models trained on each of the four datasets', '3.7 and 5.2: WTH and ETTh1 are three-model runs; the recurrent comparison there is future work'],
  ['3.5.2', '3.7'], [('3.5.2', 'all seven models were trained on each of the four datasets under a matched protocol'), ('3.7', 'Four experimental runs are reported in this thesis')], None,
  'Say plainly: three Transformers on WTH and ETTh1; all seven only on STEEL and Smart Meters. Fix 3.2.1, 3.5.2 and the "seven architectures" wording in 4.4.')
R('R-epochs', 'Epoch counts: ten epochs, early stopping and the NaN runs', 'medium', 'open',
  ['3.5.2: early stopping with patience 7 halted the failed STEEL runs', '4.4.3: NaN "for all ten epochs attempted"', "Author: Autoformer on ETTh1 stopped at epoch 9; London capped at 3 epochs (script comment: 'reduced epochs for faster testing')"],
  ['4.4.3', '3.5.2'], [('4.4.3', 'remaining so for all ten epochs attempted'), ('3.5.2', 'with a patience of 5 epochs for the recurrent models and 7 epochs for the Transformer models')], 'D-seeds-runs',
  'Open: how many epochs the failed STEEL runs actually executed. Disclose that Autoformer on ETTh1 stopped at epoch 9 and that the London 3-epoch cap was for run time (thesis) versus faster testing (script comment); pick one honest wording.')
R('R-citations', 'In-text citation numbers that do not match the reference list', 'medium', 'open',
  ['[36] (London data) and [37] (StandardScaler) point to session-based-recommendation papers', '[30] cited for the Temporal Fusion Transformer is iTransformer', '[58,64], [59], [61], [62], [65] do not match; the list ends at [63]'],
  ['3.2.4', '3.3', '5.2'], [('3.2.4', 'the Low Carbon London programme [36]'), ('5.2', 'such as the Temporal Fusion Transformer [30]')], 'D-thesis-citations',
  'Open: fix the reference numbers. Add the Low Carbon London source and the TFT and scikit-learn references, and re-map the future-work citations.')
R('R-derived-ratios', 'Ratio claims that do not reproduce from the tables', 'medium', 'open',
  ['3.4.2: LSTM-16 "consistently the smallest of any model tested"', '4.4.3: failing Transformers "two to ten times larger"', '4.6.3: recurrent models "three to twenty-five times faster"'],
  ['3.4.2', '4.4.3', '4.6.3'], [('3.4.2', 'consistently the smallest of any model tested'), ('4.4.3', 'only two to ten times larger than the successful recurrent models'), ('4.6.3', 'training three to twenty-five times faster than any Transformer depending on dataset scale')], None,
  'From the tables: LSTM-16 is not the smallest on Smart Meters (PatchTST 9,120 < 13,424); the size ratios are 4.8x to 19.8x; the speed ratios are about 3.6x to 19.4x. Replace each with the table-derived range.')
R('R-time-claims', 'Smart Meters "over three hours per model" and "55-70 minutes per epoch"', 'low', 'open',
  ['3.7: Transformer training on Smart Meters required over three hours per model', '4.5: each Transformer epoch took 55–70 minutes', 'Table 4.4: Informer 3.09 h, Autoformer 2.97 h, PatchTST 1.08 h (about 22 min per epoch)'],
  ['3.7', '4.5'], [('3.7', 'required over three hours per model'), ('4.5', 'each Transformer epoch took 55–70 minutes')], None,
  'Restrict to Informer and Autoformer (about 60 minutes per epoch); PatchTST took about 22 minutes per epoch.')
R('R-rq1-baselines', 'RQ1 names three recurrent baselines, the rest of the thesis four', 'low', 'open',
  ['1.3 RQ1: LSTM, BiLSTM, GRU', 'Everywhere else: four baselines including LSTM-16'],
  ['1.3'], [('1.3', 'recurrent baselines (LSTM, BiLSTM, GRU) in forecasting accuracy')], None, 'Add LSTM-16 to RQ1.')
R('R-window-count', 'ETTh1 window count arithmetic', 'low', 'open',
  ['3.3: 17,420 samples give 17,396 usable windows', 'Usual count with lookback 96 and horizon 24 would be 17,301; 17,396 = 17,420 - 24'],
  ['3.3'], [('3.3', "an exact 70/20/10 split of the dataset's 17,396 usable windows")], None, 'Have a one-line explanation ready: how the data loader counts windows (the lookback does not appear to be subtracted).')
R('R-bilstm-time', 'BiLSTM "double the training time"', 'low', 'open',
  ['3.4.2: approximately double the parameter count and training time', 'Tables 4.3 and 4.4: parameters about 2.1x and 2.0x; time only 1.27x and 1.24x'],
  ['3.4.2'], [('3.4.2', 'approximately double the parameter count and training time relative to a unidirectional LSTM')], None, 'Keep "double the parameters"; change the training-time claim to about 1.25x.')
R('R-epoch-times', 'PatchTST "converged in 180 s (WTH) and 156 s (ETTh1)"', 'low', 'open',
  ['4.3: 180 s on WTH and 156 s on ETTh1', 'Tables 4.1 and 4.2: 1,452.7 s and 726.4 s'],
  ['4.3'], [('4.3', 'On WTH, PatchTST converged in 180 seconds during early calibration testing, and on ETTh1 in 156 seconds')], None, 'Open: identify the run behind 180 s / 156 s, or delete the sentence.')
R('R-editorial', 'Editorial defects: duplicated paragraph and stale figure numbers', 'low', 'open',
  ['4.4.2 (PDF pp. 70-71): a paragraph is duplicated in the middle of a sentence', '3.4.2 cites Figures 3.4 to 3.7 for the recurrent cells; the figures are 3.10 to 3.13'],
  ['4.4.2', '3.4.2'], [('3.4.2', 'Figure 3.4 illustrates the basic recurrent computational unit')], None, 'Remove the duplicate and renumber the figure references.')
R('R-revin-claim', 'RevIN called "critical", but PatchTST\'s own ablation shows a small effect', 'medium', 'open',
  ['4.2.2: RevIN is "a critical component"', "PatchTST paper Table 11: instance normalisation improves results only slightly; PatchTST still outperforms without it", 'The thesis runs no RevIN ablation'],
  ['4.2.2'], [('4.2.2', 'a critical component designed to address the non-stationary nature of energy data')], None, 'Soften "critical" to "helpful" or add your own ablation. Cite PatchTST Table 11.')
R('R-rnn-recursive', '"Recursive RNN" contrast versus direct-projection RNNs', 'medium', 'open',
  ['4.2.2: PatchTST avoids the cascading error of recursive RNN decoding', '3.4.2: LSTM-16 projects its final hidden state directly to the output horizon'],
  ['4.2.2', '3.4.2'], [('4.2.2', 'Unlike the recursive, step-by-step prediction methods used in traditional RNNs'), ('3.4.2', 'projected directly to the output horizon without additional intermediate layers')], None, 'Say the cascading-error argument applies to recursive decoding, not to your direct-projection baselines, and state how each RNN decodes.')
R('R-steel-two-runs', 'PatchTST error on STEEL changes between the two runs', 'medium', 'open',
  ['4.4.3 first run: PatchTST MAE 0.3407, MSE 0.2985, RMSE 0.5464', 'Table 4.3 second run: PatchTST MAE 0.0766, MSE 0.0100, RMSE 0.1000 (34,368 parameters)', 'No explanation of the configuration change'],
  ['4.4.3'], [('4.4.3', 'achieving MAE 0.3407, MSE 0.2985, and RMSE 0.5464'), ('4.4.3', 'PatchTST 34,368 0.0766 0.0100 0.1000 173.7 Success')], None, 'Open: explain what changed (capacity, patch 12/6, scaling) or drop the first-run numbers.')
R('R-mechanism-claim', 'STEEL mechanism: "isolates the property" versus "a hypothesis"', 'medium', 'open',
  ['4.6.2 and 5.1: the evidence isolates the specific property', '1.5: the mechanism is a hypothesis pending confirmatory ablations'],
  ['4.6.2', '1.5'], [('4.6.2', 'The evidence instead isolates the specific property shared by the two failing architectures'), ('1.5', 'pending confirmatory ablation experiments identified as future work')], None, 'Use "best-supported hypothesis" wherever the mechanism is stated as established.')
# ---- fixed ----
R('R-fixed-steel-outcome', 'STEEL: failed or improved? (fixed)', 'high', 'fixed',
  ['Earlier draft: NaN in 4.4.3 but "stability achieved" and "27.9% improvement" elsewhere', 'Final: one consistent account, Informer and Autoformer diverge, PatchTST and RNNs train'],
  ['4.4.3'], [('4.4.3', 'Informer and Autoformer collapsed to NaN losses from epoch 1 and never recovered')], None, 'Fixed in the final thesis. The stabilised-rerun claim and the 27.9% figure are gone. Do not claim any recovery.')
R('R-fixed-split-text', 'Data split wording (fixed for the text)', 'high', 'fixed',
  ['Earlier draft: 60/20/20 in some sections, 70/20/10 in others', 'Final: 70/20/10 throughout the text (but see R-london-data)'],
  ['3.3'], [('3.3', 'in a ratio of 70% / 20% / 10%')], None, 'Fixed in the text. The London split is a separate open contradiction (R-london-data).')
R('R-fixed-normalization', 'Normalisation description (fixed)', 'medium', 'fixed',
  ['Earlier draft: instance normalisation, global StandardScaler and RevIN described inconsistently', 'Final: StandardScaler on training data for all models; RevIN inside PatchTST'],
  ['3.3', '4.2.2'], [('3.3', "all continuous features were normalised using Z-score standardisation via scikit-learn's StandardScaler")], None, 'Fixed. Describe it as layered: StandardScaler (train-only) for all models plus RevIN inside PatchTST.')
R('R-fixed-magnitude', 'Orders of magnitude (fixed)', 'low', 'fixed',
  ['Earlier draft: 10^7 versus seven orders', 'Final: "roughly six to seven orders of magnitude" in 3.2.3 and 4.4.3'],
  ['3.2.3'], [('3.2.3', 'a span of roughly six to seven orders of magnitude')], None, 'Fixed. Use "roughly six to seven orders of magnitude".')
R('R-fixed-scope', 'Scope statements (fixed)', 'medium', 'fixed',
  ['Earlier draft: hybrid CNN-Transformers, FEDformer as compared, three versus four datasets, LCL-ECD', 'Final: FEDformer reviewed only; four datasets; hybrids are future work'],
  ['2.4.4', '3.2'], [('2.4.4', 'it was not among the models empirically evaluated in this thesis'), ('3.2', 'This study utilises four publicly available datasets')], None, 'Fixed in the text (but see R-seven-models-each).')
R('R-fixed-headline', 'Accuracy headline and parameter ratio (fixed)', 'low', 'fixed',
  ['Earlier draft: about 26.6% / 25-28% / 27.9% accuracy figures and a 155-1,600x parameter ratio', 'Final: Smart Meters gains 57.6 / 76.0 / 50.4%, which reproduce from Table 4.4'],
  ['4.5'], [('4.5', 'improving on the average of the other six models by 57.6%, 76.0%, and 50.4%')], None, 'Fixed. The current headline figures reproduce; the ETTh1 percentages are covered by R-etth1-percentages.')

# ---------------- mock viva ----------------
concept('C-mock-viva', 'M', 'Committee stress tests (mock viva)',
 'Five hostile questions on whether PatchTST generalises to non-stationary urban data, rewritten against the final thesis. Answer aloud in 90 seconds, then check the model answer and the follow-up.',
 ['4.6.1'], ('4.6.1', 'PatchTST is the strongest choice on rich, higher-dimensional data where accuracy is the priority'), [TH, N, 'han2024ci', 'zeng2023dlinear'], 1.0)
card('C-mock-viva', 'mock', 3, 'Household smart-meter load is spiky and full of near-zero periods, like STEEL. Informer and Autoformer failed on STEEL but trained on London, and PatchTST trained on both. What separates the cases?',
 'The thesis attributes the STEEL failure to unbounded cross-channel attention or correlation meeting a heavy-tailed value that survives standardisation, in data spanning six to seven orders of magnitude and with abrupt on/off transitions; recurrent gates are bounded and PatchTST attends within each channel. Standardisation was sufficient on Smart Meters, and the thesis reports extreme scale heterogeneity only for STEEL. Be candid that this is a hypothesis (1.5), that London is daily per-household data split by household, and that logging attention logits would confirm it.',
 ['states the bounded-activation account', 'names the scale-heterogeneity difference', 'calls it a hypothesis', 'gives the correct London description'],
 [('4.4.3', 'A heavy-tailed value that survives Z-score standardisation in one channel'), ('3.2.4', 'genuine household-level noise such as localised consumption spikes from individual appliances')], TH, '§4.4.3', decisionId='D-london-data',
 followUp='If I gave you one household that was empty for two weeks, what happens to RevIN? (The thesis does not test this; a near-constant window makes the instance standard deviation approach zero, so check how it is handled.)')
card('C-mock-viva', 'mock', 3, 'Urban demand shifts in regime: lockdowns, heatwaves, heat pumps. RevIN assumes the horizon looks like the lookback. How does PatchTST cope when it does not?',
 'RevIN corrects level and scale shift between windows (it normalises each window and reverses the transformation on the output). It cannot correct a change of shape or a structural break inside the horizon, and instance normalisation can remove information (over-stationarisation, Liu et al.). Remedies: rolling retraining, exogenous regime indicators, and evaluating on a deliberately shifted period.',
 ['states what RevIN corrects', 'states what it cannot', 'proposes remedies'],
 ('2.4.6', 'by normalizing each input window prior to processing and reversing the transformation on the output'), N, 'Table 11 (instance normalization)',
 followUp='Your chronological split puts the test data at the end. Was there any regime change in that period? (For WTH, ETTh1 and STEEL the split is chronological and no regime analysis was done; for London the test set is 100 different households, not a later period.)')
card('C-mock-viva', 'mock', 3, 'Channel independence ignores temperature when forecasting load, yet weather drives urban demand. Why is CI the right choice here?',
 'It is a trade-off: CI is more robust under distribution shift and with heterogeneous channels, channel mixing is more expressive (Han et al.), and iTransformer, Crossformer and CARD argue cross-variate information matters when inter-variable structure is strong. In your runs PatchTST won on ETTh1 and Smart Meters, but you ran no CI ablation, so test it by adding temperature as a covariate and comparing.',
 ['trade-off named', 'counter-designs named', 'admits no CI ablation', 'proposes a test'],
 ('2.4.6', 'channel-independent training sacrifices cross-variate representational capacity in exchange for improved robustness to distribution shift'), 'han2024ci', 'Robustness',
 followUp='If CI discards cross-channel information, what did Informer gain by mixing channels, and why did it underfit anyway? (Informer mean-collapsed on ETTh1 despite the lowest training loss; the thesis does not isolate why.)')
card('C-mock-viva', 'mock', 3, 'You trained on one chronological split, one run per model. How confident are you that the ranking is stable?',
 'Acknowledge it plainly: each result is a single run with no seeds and no significance test. The large margins (PatchTST ETTh1 MSE 0.3742 vs 0.5652; Smart Meters 20.19 vs 38.67) are unlikely to be seed noise, and the PatchTST paper reports small variance across 5 seeds, but small gaps may be. The stronger protocol is rolling-origin evaluation, several seeds and a Diebold–Mariano test.',
 ['admits single run', 'separates large from small gaps', 'names a stronger protocol'],
 ('4.4.2', 'PatchTST emerges as the definitive winner across every accuracy metric evaluated'), N, 'Table 14 (seed variance)', decisionId='D-seeds-runs',
 followUp='Informer won on MAE at 5 epochs on WTH. Why should I believe the 10-epoch result is the stable one?')
card('C-mock-viva', 'mock', 4, 'Your horizon is 24 steps with a 96-step lookback; the PatchTST paper uses horizons up to 720. Is this long-term forecasting, and would your conclusions hold on 6 GB at longer horizons?',
 'Define long-term as the thesis does: mapping extended historical windows onto extended future horizons, with 24 steps as the horizon used here. Patching makes longer lookbacks affordable: L = 336, P = 16, S = 8 gives 41 tokens. Informer and Autoformer would be the first to run out of memory on 6 GB. Be ready for the DLinear result that a simple linear model is competitive at long horizons, which was not among your baselines.',
 ['position on "long-term"', 'patch arithmetic', 'memory reasoning without invented GB figures', 'DLinear acknowledged'],
 ('1.1', 'Long-Term Time Series Forecasting (LTSF) requires models to map extended historical windows onto extended future horizons'), 'zeng2023dlinear', 'DLinear / LTSF-Linear', decisionId='D-vram',
 followUp='Why was no linear baseline such as DLinear included, given that paper is in your bibliography?')
