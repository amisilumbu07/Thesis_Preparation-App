from content_lib import concept, card

TH = 'thesis'
N = 'nie2023patchtst'
LR = '1×10⁻⁴ for the three Transformer models and 1×10⁻³ for the four recurrent models'

concept('C-hardware', 'E', 'The hardware constraint',
 'Every experiment ran on one ASUS ROG Zephyrus G14 laptop with an NVIDIA RTX 2060 (Max-Q) and 6GB of VRAM, chosen to represent constrained, non-server-class hardware. The 6GB budget forced smaller Transformer dimensions and batch sizes. No VRAM was actually measured.',
 ['3.1', '1.5'], ('3.1', 'a single ASUS ROG Zephyrus G14 (GA401IV) laptop equipped with an NVIDIA GeForce RTX 2060 (Max-Q, 6GB VRAM)'), [TH], 0.8, decisionId='D-vram')
card('C-hardware', 'recall', 1, 'On what hardware were all experiments run?', 'A single ASUS ROG Zephyrus G14 (GA401IV) laptop with an NVIDIA GeForce RTX 2060 (Max-Q), 6GB VRAM.', ['RTX 2060 Max-Q', '6GB'],
 ('3.1', 'a single ASUS ROG Zephyrus G14 (GA401IV) laptop equipped with an NVIDIA GeForce RTX 2060 (Max-Q, 6GB VRAM)'), TH, '§3.1',
 options=['RTX 2060 Max-Q, 6GB VRAM', 'Tesla V100, 32GB', 'RTX 4090, 24GB', 'CPU only'], correct='RTX 2060 Max-Q, 6GB VRAM')
card('C-hardware', 'recall', 2, 'Why was this hardware chosen?', 'To represent constrained, non-server-class hardware, not to establish the maximum achievable performance of any architecture.', ['constrained hardware', 'not maximum performance'],
 ('1.5', 'a configuration selected to represent constrained, non-server-class hardware rather than to establish the maximum achievable performance'), TH, '§1.5')
card('C-hardware', 'transfer', 4, 'A utility offers a 4 GB edge device for 10,000 feeders. Which model do you recommend, and what can you actually claim?',
 'The thesis measured parameter counts and training time, not VRAM. On parameters PatchTST is the smallest Transformer everywhere (9,120 on Smart Meters), and GRU offers the best accuracy per parameter among the recurrent models. Say plainly that memory use was not measured, so a 4 GB recommendation needs a measurement first. Do not quote any GB figure.',
 ['uses parameters and time, not VRAM', 'admits VRAM was not measured', 'no invented GB figures'],
 ('3.5.3', "PatchTST's patch-based tokenisation made it consistently the least memory-intensive of the three Transformers"), TH, '§3.5.3', decisionId='D-vram',
 open={'decisionId': 'D-vram', 'reason': 'No VRAM was measured; the thesis claim about memory is qualitative.'})

concept('C-datasets', 'E', 'The four datasets and their roles',
 'WTH (35,064 hourly rows, 12 variables) calibrates the training budget. ETTh1 (17,420 hourly rows) is the continuous control. STEEL (35,040 rows at 15-minute resolution, 11 variables, 7 retained) is the industrial stress test. Smart Meters in London is the large-scale practical benchmark.',
 ['3.2', '3.2.1', '3.2.2', '3.2.3', '3.2.4'], ('3.2', 'This study utilises four publicly available datasets'), [TH], 0.4)
card('C-datasets', 'recall', 1, 'Which dataset is the deliberate industrial stress test?', 'STEEL (Steel Industry Energy Consumption).', ['STEEL'],
 ('3.2.3', 'This dataset therefore serves in this research as a deliberate stress test'), TH, '§3.2.3',
 options=['STEEL', 'WTH', 'ETTh1', 'Smart Meters'], correct='STEEL')
card('C-datasets', 'recall', 2, 'Give the role of each of the four datasets in one line each.',
 'WTH: calibration of the epoch budget and early-stopping window. ETTh1: canonical benchmark and control condition. STEEL: deliberate stress test on industrial data. Smart Meters: primary practical-application benchmark at large scale.', ['four roles'],
 [('3.2.1', 'WTH served as the calibration dataset', 'early-stopping window'), ('3.2.2', 'it also serves as a control condition'), ('3.2.3', 'serves in this research as a deliberate stress test'), ('3.2.4', 'it serves as the primary practical-application benchmark')], TH, 'Table 3.1')
card('C-datasets', 'recall', 2, 'Give the size and resolution of WTH, ETTh1 and STEEL.', 'WTH: 35,064 hourly entries, 12 variables. ETTh1: 17,420 hourly samples. STEEL: 35,040 records at 15-minute resolution, 11 variables (7 retained).', ['three sizes', 'resolutions'],
 [('3.2.1', '35,064 total entries across 12 variables'), ('3.2.2', '17,420 hourly samples'), ('3.2.3', '35,040 records at 15-minute resolution across 11 variables')], TH, 'Table 3.1')
card('C-datasets', 'derivation', 3, 'STEEL\'s largest CO₂ value is 0.07 and its largest NSM value is 85,500. How many orders of magnitude apart, and what does the thesis say?',
 '85,500 / 0.07 is about 1.2 × 10⁶, so about 6.1 orders of magnitude on the maxima (about 6.6 using the means 42,750 and 0.01). The thesis says "roughly six to seven orders of magnitude", not exactly seven.', ['ratio', 'six to seven'],
 [('3.2.3', 'ranges from 0 to only 0.07 (mean 0.01)'), ('3.2.3', 'a span of roughly six to seven orders of magnitude')], TH, '§3.2.3', note='Register item R-fixed-magnitude: the thesis is now consistent.')

concept('C-split-leakage', 'E', 'Chronological split and leakage control',
 'Data are split 70/20/10 in time order, never shuffled, so the model is always evaluated on data strictly later than anything it trained on. Scaler statistics come from the training partition only and are applied unchanged to validation and test.',
 ['3.3'], ('3.3', 'This chronological, non-shuffled split is essential for time-series evaluation'), [TH], 0.7, decisionId='D-london-data')
card('C-split-leakage', 'recall', 2, 'How were the data split, and why does the order matter?', '70% / 20% / 10% chronologically, non-shuffled, so the model is always evaluated on data strictly later than any training data, preventing look-ahead bias.', ['70/20/10', 'chronological', 'look-ahead bias'],
 [('3.3', 'in a ratio of 70% / 20% / 10%'), ('3.3', 'the model is always evaluated on data strictly later than anything seen during training')], TH, '§3.3')
card('C-split-leakage', 'recall', 2, 'How does the scaler avoid information leakage?', 'Its mean and standard deviation are computed on the training partition only and then applied unmodified to validation and test.', ['train-only statistics'],
 ('3.3', 'computed on the training partition only, and then applied unmodified to the validation and test partitions to avoid information leakage'), TH, '§3.3')
card('C-split-leakage', 'derivation', 2, 'ETTh1 gives 12,177 / 3,479 / 1,740 sequences. Show that this is a 70/20/10 split.', 'The total is 17,396 usable windows; 70% is 12,177.2, 20% is 3,479.2 and 10% is 1,739.6, so the counts match after rounding.', ['sum 17,396', 'three percentages'],
 ('3.3', 'ETTh1 yields 12,177 training, 3,479 validation, and 1,740 test sequences'), TH, '§3.3')
card('C-split-leakage', 'objection', 3, 'Why not shuffle the windows to get more balanced folds?', 'Shuffling would let the model train on data later than what it is tested on (look-ahead bias) and would not mirror the real forecasting situation where future information is unavailable.', ['look-ahead bias', 'realistic scenario'],
 ('3.3', 'mirroring the realistic forecasting scenario in which future information is unavailable at training time'), TH, '§3.3')

concept('C-window-setup', 'E', 'Lookback, label length and horizon',
 'Every model and dataset uses a lookback of 96 timesteps, a label length of 48 and a horizon of 24. On hourly data that is 4 days of history predicting the next day. The label length feeds the Transformer decoders; recurrent models and PatchTST use only the lookback. For London the unit is days (see the London concept).',
 ['3.3', '3.2.2'], ('3.3', 'using a Lookback of 96 timesteps, a Label length of 48 timesteps, and a prediction Horizon of 24 timesteps'), [TH], 0.5, decisionId='D-london-data')
card('C-window-setup', 'recall', 1, 'What are the lookback, label length and horizon?', 'Lookback 96, label length 48, horizon 24 timesteps.', ['96 / 48 / 24'],
 ('3.3', 'using a Lookback of 96 timesteps, a Label length of 48 timesteps, and a prediction Horizon of 24 timesteps'), TH, '§3.3',
 options=['96 / 48 / 24', '48 / 96 / 24', '24 / 48 / 96', '96 / 24 / 48'], correct='96 / 48 / 24')
card('C-window-setup', 'derivation', 2, 'On hourly ETTh1, what real time span do the lookback and horizon cover?', 'A 96-step lookback is 4 days of history and the 24-step horizon is the next day.', ['96 h = 4 days', '24 h = 1 day'],
 ('3.2.2', 'still providing 24 data points per day of context for the Lookback-96 window'), TH, '§3.2.2')
card('C-window-setup', 'recall', 3, 'Which models use the label length, and how?', 'The Transformer decoders (Informer, Autoformer): it overlaps the final 48 steps of the lookback and serves as a start token. Recurrent models and PatchTST consume only the lookback window.', ['who uses it', 'start token'],
 ('3.3', 'while the recurrent models and PatchTST consume only the Lookback window directly'), TH, '§3.3')

concept('C-features', 'E', 'Preprocessing and feature engineering',
 'Missing values (under 0.5%) are linearly interpolated, features are Z-score standardised, calendar features become sine–cosine pairs, and for ETTh1, STEEL and Smart Meters lagged values and rolling statistics are added. This expands ETTh1 from 7 columns to 33 input features.',
 ['3.3', '4.2', '3.2.2'], ('3.2.2', 'expands the native seven-column structure to 33 input features per timestep'), [TH], 0.4)
card('C-features', 'recall', 1, 'Why are calendar features encoded with sine and cosine?', 'So the 23rd hour is numerically adjacent to the 0th hour instead of a discontinuous jump.', ['cyclical adjacency'],
 ('3.3', 'ensuring that the 23rd hour is represented as numerically adjacent to the 0th hour'), TH, '§3.3',
 options=['So hour 23 is adjacent to hour 0', 'To remove seasonality', 'To normalise variance', 'To reduce the number of features'], correct='So hour 23 is adjacent to hour 0')
card('C-features', 'recall', 2, 'List the lag and rolling-window features and where they are used.', 'Lags at 1, 6, 12 and 24 hours; rolling mean and standard deviation over 3-, 12- and 24-hour windows; used for the richest datasets (ETTh1, STEEL, Smart Meters).', ['lags', 'rolling windows', 'which datasets'],
 ('3.3', 'lagged values (at 1, 6, 12, and 24-hour intervals)', '24-hour windows)'), TH, '§3.3')
card('C-features', 'recall', 2, 'How many input features does ETTh1 have after engineering, and why does the thesis disclose it?', '33, up from 7 native columns. It departs from the seven-feature setting of the original Informer, Autoformer and PatchTST papers, which matters when comparing with their published numbers.', ['33 features', 'methodological departure'],
 ('3.2.2', 'because it constitutes a methodological departure from the seven-feature configuration used in the original'), TH, '§3.2.2')
card('C-features', 'recall', 3, 'Was Z-score standardisation enough on every dataset?', 'No. It sufficed for WTH, ETTh1 and Smart Meters but on its own was insufficient to prevent numerical instability in two of the three Transformers on STEEL.', ['works on three datasets', 'insufficient on STEEL'],
 ('3.3', 'was, on its own, insufficient to prevent numerical instability in two of the three Transformer architectures on the STEEL dataset'), TH, '§3.3')

concept('C-training-protocol', 'E', 'Training protocol',
 'Adam throughout. Learning rate 1e-4 for the Transformers and 1e-3 for the recurrent models. Early stopping on validation loss with patience 7 (Transformers) and 5 (recurrent). Batch size 32 for recurrent models; 8 for Transformers on WTH, ETTh1 and STEEL and 16 on Smart Meters. A 10-epoch budget chosen from the WTH calibration. Capacity was reduced per dataset to fit 6GB.',
 ['3.5.2', '4.3', '3.5.1'], ('3.5.2', 'The Adam optimiser [38] was used throughout'), ['kingma2015adam', TH], 0.5, decisionId='D-seeds-runs')
card('C-training-protocol', 'recall', 1, 'What learning rates were used?', '1e-4 for the three Transformers, 1e-3 for the four recurrent models.', ['both values'],
 ('3.5.2', 'learning rate of ' + LR), 'kingma2015adam', 'Algorithm 1 (Adam)',
 options=['1e-4 Transformers, 1e-3 recurrent', '1e-3 Transformers, 1e-4 recurrent', '1e-3 for all', '1e-5 for all'], correct='1e-4 Transformers, 1e-3 recurrent')
card('C-training-protocol', 'recall', 2, 'State the early-stopping patience for each model family.', '5 epochs for the recurrent models and 7 for the Transformer models, monitoring validation loss.', ['5 and 7'],
 ('3.5.2', 'with a patience of 5 epochs for the recurrent models and 7 epochs for the Transformer models'), 'kingma2015adam', 'Algorithm 1 (Adam)')
card('C-training-protocol', 'recall', 2, 'What batch sizes were used and why do they differ?', '32 for all recurrent models. For Transformers 8 on WTH, ETTh1 and STEEL and 16 on the smaller-capacity Smart Meters configurations, because batch size was constrained by the 6GB VRAM budget.', ['32', '8 and 16', 'VRAM reason'],
 ('3.5.2', 'a batch size of 8 was used for the Transformer models on WTH, ETTh1, and STEEL, while a batch size of 16 was used'), TH, '§3.5.2')
card('C-training-protocol', 'objection', 3, 'You did not tune hyperparameters per model. Doesn\'t that bias the comparison?', 'Hyperparameters were held fixed across comparable model categories to preserve comparability rather than tuned to optimality; the thesis states this may understate the best-case performance of any single architecture. Differences are therefore under a matched protocol, not best-case results.', ['matched protocol', 'admits understatement'],
 ('1.5', 'Hyperparameters were held fixed across comparable model categories', 'best-case performance achievable by any single architecture'), TH, '§1.5')
card('C-training-protocol', 'recall', 2, 'Why are the two learning rates different?', 'They were chosen to reflect the differing training-stability characteristics of the Transformer and recurrent families.', ['stability reason'],
 ('3.5.2', 'values chosen to reflect the differing training stability characteristics of each family'), TH, '§3.5.2')

concept('C-metrics', 'E', 'Metrics and what they hide',
 'MAE is the average error in original units; MSE squares errors so large misses dominate; RMSE returns to original units. MAPE was computed but is infinite on Smart Meters because of exact zeros in the target, so it is excluded. Operational metrics are training time, parameter count and VRAM (VRAM was not measured).',
 ['3.6.1', '3.6.2'], ('3.6.1', 'the average magnitude of prediction error in the original units of the target variable'), [TH], 0.5, decisionId='D-vram')
card('C-metrics', 'recall', 2, 'Define MAE, MSE and RMSE and say what each emphasises.', 'MAE: average absolute error in original units. MSE: average squared error, penalises large deviations disproportionately. RMSE: square root of MSE, back in original units but still sensitive to large errors.', ['three definitions', 'sensitivity'],
 [('3.6.1', 'the average magnitude of prediction error in the original units of the target variable'), ('3.6.1', 'which penalises large deviations disproportionately')], TH, '§3.6.1')
card('C-metrics', 'recall', 2, 'Why is MAPE not reported for Smart Meters?', 'It returned infinite or undefined values for every model, because exact zeros in the target series cause division by zero.', ['zeros in target'],
 ('3.6.1', 'MAPE returned an infinite or undefined value for every model tested'), TH, '§3.6.1')
card('C-metrics', 'objection', 3, 'Informer had the best MAE at 5 epochs on WTH but the predictions were flat. How can low error be misleading?', 'A mean-reverting prediction achieves low error by predicting close to the average instead of learning temporal structure, so summary error alone cannot distinguish learning from a flat guess. Check the predictions visually.', ['mean reversion', 'need qualitative check'],
 ('4.4.1', 'a mean-reverting pattern that achieves low error by predicting close to the average value rather than learning genuine temporal structure'), TH, '§4.4.1')
card('C-metrics', 'recall', 3, 'Which operational metrics does the thesis define, and which of them was never actually measured?', 'Training time, parameter count and peak GPU memory (VRAM). The author confirms no VRAM measurement exists, although 3.5.3 says peak memory was recorded for every run.', ['three metrics', 'VRAM missing'],
 ('3.6.2', 'Training Time: total wall-clock time in seconds to reach the early-stopping criterion or the epoch budget'), TH, '§3.6.2', decisionId='D-vram',
 open={'decisionId': 'D-vram', 'reason': 'The thesis says VRAM was recorded; no VRAM figure exists in the code or results.'})

concept('C-calibration', 'E', 'WTH calibration: 5 versus 10 epochs',
 'At 5 epochs Informer looked better than Autoformer on summary metrics (MAE 0.51 vs 0.56) but produced flat, mean-reverting predictions. Extending to 10 epochs let the slower Autoformer catch up. This fixed the 10-epoch budget used everywhere else.',
 ['4.4.1', '3.5.1'], ('4.4.1', 'Informer achieved an MAE of 0.51 and RMSE of 0.69', 'RMSE of 0.74'), [TH], 0.5)
card('C-calibration', 'recall', 2, 'Tell the WTH calibration story in three sentences.', 'At 5 epochs Informer had better MAE/RMSE (0.51/0.69) than Autoformer (0.56/0.74) but its predictions were flat and mean-reverting. At 10 epochs Autoformer, a slower learner, improved markedly and both reached nearly identical validation losses. That fixed the 10-epoch budget.', ['5-epoch numbers', 'flat predictions', '10-epoch outcome'],
 ('4.4.1', 'Informer achieved an MAE of 0.51 and RMSE of 0.69', 'RMSE of 0.74'), TH, '§4.4.1')
card('C-calibration', 'figure', 3, 'Figure 4.5 shows the WTH 5-epoch predictions. Why is the Informer curve misleading?', 'Its predictions are overly smooth and flat and fail to capture the dynamic downward trends of the ground truth, so the low error comes from predicting near the average.', ['flat vs trend', 'links to low MAE'],
 ('4.4.1', 'its actual predictions were overly smooth and flat, failing to capture the dynamic downward trends present in the ground truth'), TH, '§4.4.1', figure='Figure 4.5')
card('C-calibration', 'objection', 3, 'Informer won on MAE at 5 epochs. Why should I believe the 10-epoch ranking is the stable one?', 'Both models reached nearly identical validation losses at 10 epochs, and Table 4.1 then shows Informer best on WTH (test MAE 0.4802 vs 0.5988). But each figure is a single run with no seeds and no significance test, so the ranking is supported, not proven. Say what you would add: several seeds and a significance test.', ['5 vs 10 epoch story', 'single-run caveat', 'proposes seeds and a test'],
 [('4.4.1', 'both models eventually reached nearly identical validation losses'), ('4.4.1', 'Informer 2,901,542 0.4802 0.4046 0.6361 1,100.9')], N, 'Table 14 (seed variance)', decisionId='D-seeds-runs')

concept('C-single-run', 'E', 'One run per result: how stable is the ranking?',
 'Each reported figure comes from one run with no random seeds and no significance test (the only seed is the London household split). Small gaps, such as Informer versus Autoformer on ETTh1, may lie within seed variance. The PatchTST paper itself ran 5 seeds and found variance small on large datasets.',
 ['1.5', '4.4.2'], ('4.4.2', 'PatchTST emerges as the definitive winner across every accuracy metric evaluated'), [N], 0.9, decisionId='D-seeds-runs')
card('C-single-run', 'objection', 3, 'You trained once on one chronological split. How confident are you in the model ranking?', 'Acknowledge the limitation: each result is one run, no seeds, no significance test. The large PatchTST margins (ETTh1 MSE 0.3742 vs 0.5652, Smart Meters 20.19 vs the next best 38.67) are unlikely to be seed noise, especially since the PatchTST paper reports small variance across 5 seeds, but small gaps (Informer vs Autoformer on ETTh1) may be. Stronger protocol: several seeds, rolling-origin evaluation and a Diebold–Mariano test.', ['admits single run', 'separates large from small gaps', 'names a stronger protocol'],
 ('4.4.2', 'PatchTST emerges as the definitive winner across every accuracy metric evaluated'), N, 'Table 14 (seed variance)', decisionId='D-seeds-runs', note='Design doc Q4. Table 14 of the PatchTST paper (p.20): 5 seeds, variance considerably small.')
card('C-single-run', 'recall', 2, 'What does the PatchTST paper report about seed sensitivity, and how does that help you?', 'It trained the supervised model with 5 random seeds and found the variance considerably small (its Table 14). That supports, but does not replace, replication of your own results.', ['5 seeds', 'small variance', 'limits of the inference'],
 ('4.4.2', 'PatchTST emerges as the definitive winner across every accuracy metric evaluated'), N, 'Table 14 (seed variance)', decisionId='D-seeds-runs')

concept('C-london-data', 'E', 'What the London data really is (decided)',
 'The thesis describes Smart Meters as half-hourly readings, over 3.4 million, with a chronological 70/20/10 split. The author\'s code shows something different: daily per-household records (one row per household per day, with energy statistics pre-aggregated), split by household, then concatenated. The lookback of 96 is 96 days and the horizon is 24 days. Some windows span two households.',
 ['3.2.4', '3.3', '4.1'], ('3.2.4', 'The dataset contains half-hourly electricity consumption readings for a sample of London households'), [TH], 0.95, decisionId='D-london-data')
card('C-london-data', 'register', 3, 'What does the thesis say the London data is, and what does the code actually use?', 'Thesis: half-hourly readings, over 3.4 million before windowing. Code: daily per-household records (one row per household per day, energy_sum as target), so lookback 96 = 96 days and horizon 24 = 24 days. The ">3.4 million" matches the daily row total (2.73M + 0.68M + 66k), not half-hourly readings. The thesis text needs correcting.', ['half-hourly vs daily', 'lookback in days', 'text needs fixing'],
 ('4.1', 'over 3.4 million half-hourly residential readings prior to windowing'), TH, '§4.1', decisionId='D-london-data', note='Author-reported from code (not verifiable in this repo).')
card('C-london-data', 'register', 3, 'How was the London data split, and is it the chronological 70/20/10 the thesis describes?', 'No. It was split by household (seed 42): 100 test households, then 20% of the rest for validation. Households with fewer than 365 days were dropped. Row counts are 2.73M / 0.68M / 66k, about 78.5 / 19.6 / 1.9%. The thesis says a chronological 70/20/10 split across all four datasets.', ['by household', 'row counts', 'contradicts 3.3'],
 ('3.3', 'The data was then divided chronologically into training, validation, and test partitions in a ratio of 70% / 20% / 10%'), TH, '§3.3', decisionId='D-london-data')
card('C-london-data', 'register', 3, 'Is the London data "aggregated across households"? What limitation follows from how windows were built?', 'No: it is per-household daily data. But households are stacked into one long table and windows slide over it without a household boundary, so some 96-day windows span two different households. This belongs in the limitations.', ['per-household', 'window crossing', 'limitation'],
 ('5.2', 'for genuinely individual (rather than aggregated) household-level smart-meter data'), TH, '§5.2', decisionId='D-london-data')
