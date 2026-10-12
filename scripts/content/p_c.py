from content_lib import concept, card

N = 'nie2023patchtst'
PL = 'Patching and channel independence'

concept('C-patching', 'C', 'Sub-series patching',
 'PatchTST cuts each series into patches of P consecutive steps, moved by a stride S, and treats each patch as one token. Attention then runs over N patches instead of L points, and each token carries a local shape (the form of a trend) instead of one noisy reading.',
 ['3.4.1', '4.2.1', '2.4.5'], ('2.4.5', 'each of which is treated as a single token within the attention mechanism'), [N], 0.3, decisionId='D-patch-config')
card('C-patching', 'recall', 1, 'In PatchTST, what is one token given to the attention mechanism?', 'A patch: a short sub-sequence of consecutive time steps.', ['patch, not a single time step'],
 ('2.4.5', 'each of which is treated as a single token within the attention mechanism'), N, PL,
 options=['A patch of consecutive time steps', 'A single time step', 'A whole channel', 'A full lookback window'], correct='A patch of consecutive time steps')
card('C-patching', 'recall', 2, 'What does patching preserve that point-wise tokens lose?',
 'Local semantic information, the "shape" of a trend, which is otherwise lost in the point-wise noise of individual observations.', ['local semantic information', 'shape vs noise'],
 ('4.2.1', 'it retains local semantic information', 'point-wise noise of standard observations'), N, PL)
card('C-patching', 'recall', 2, 'How do Informer and Autoformer tokenise the input, compared with PatchTST?',
 'Informer and Autoformer treat individual time steps as tokens. PatchTST groups steps into patches and uses each patch as a token.', ['point-wise vs patch tokens'],
 ('3.4.1', 'While the Informer and Autoformer treat individual time steps as tokens, PatchTST introduces the concept of Sub-series Patching'), N, PL)
card('C-patching', 'transfer', 4, 'STEEL has machines that switch on and off almost instantly. Could a fixed patch length be a problem there? What does the thesis say and not say?',
 'A patch covering a switching instant would mix "on" and "off" values inside one token. That is a plausible reasoning step but the thesis does not test it: it describes the sharp vertical transitions (3.2.3) and attributes PatchTST\'s survival to within-channel attention, not to patch length. Treat it as a hypothesis.',
 ['links step changes to patch content', 'says the thesis does not test it'],
 ('3.2.3', 'industrial machinery can be switched on or off effectively', 'discontinuous vertical transitions'), N, PL, note='Extension beyond the thesis (design doc section 6); state it as a hypothesis.')

concept('C-patch-arith', 'C', 'Patch arithmetic (derivation lab)',
 'The number of patches is N = floor((L - P) / S) + 1, with no padding. With the lookback L = 96, patch length 16 and stride 8 the model sees 11 tokens, so the attention matrix shrinks from 96² = 9,216 to 11² = 121 entries, about 76 times smaller.',
 ['4.3', '3.4.1', '4.2.1'], ('4.3', 'reducing the effective sequence length from 96 raw timesteps to approximately 11 patches'), [N], 0.5, decisionId='D-patch-config')
card('C-patch-arith', 'derivation', 2, 'L = 96, P = 16, S = 8. How many patches, and by what factor does the attention matrix shrink?',
 'N = floor((96 - 16) / 8) + 1 = 11. Attention pairs go from 96² = 9,216 to 11² = 121, a factor of about 76.', ['correct formula', 'N = 11', 'about 76x', 'mentions padding variant'],
 ('4.3', 'reducing the effective sequence length from 96 raw timesteps to approximately 11 patches'), N, PL, decisionId='D-patch-config')
card('C-patch-arith', 'derivation', 3, 'The STEEL runs used patch length 12 and stride 6 (author\'s code). How many patches, and how does the attention shrink versus L = 96?',
 'N = floor((96 - 12) / 6) + 1 = 15. Attention pairs go from 9,216 to 225, a factor of about 41. The thesis text states only "approximately 11 patches" and never mentions the STEEL 12/6 override.', ['N = 15', 'about 41x', 'notes the thesis omits it'],
 ('4.3', 'reducing the effective sequence length from 96 raw timesteps to approximately 11 patches'), N, PL, decisionId='D-patch-config',
 note='Decided by the author (D-patch-config). The WTH setting is still open.')
card('C-patch-arith', 'derivation', 3, 'Section 4.2.1 illustrates P = 16 with S = 4. How many patches is that at L = 96, and why does it disagree with "about 11 patches"?',
 'N = floor((96 - 16) / 4) + 1 = 21 (22 with end padding). "About 11" fits S = 8. Per the author, S = 4 is only an illustration; the runs used 16/8 (ETTh1, London) and 12/6 (STEEL).', ['N = 21', 'S = 8 gives 11', 'S = 4 is illustrative only'],
 [('4.2.1', 'by grouping 16 time steps into a single patch with a stride of 4'), ('4.3', 'approximately 11 patches')], N, PL, decisionId='D-patch-config')
card('C-patch-arith', 'derivation', 4, 'Extend to a lookback of L = 336 with P = 16 and S = 8. How many tokens, and what does that say about longer lookbacks on limited memory?',
 'N = floor((336 - 16) / 8) + 1 = 41 tokens, still small. Patching makes long lookbacks affordable because attention cost depends on N², not L² (336² = 112,896 versus 41² = 1,681).', ['N = 41', 'cost depends on N squared'],
 ('4.3', 'reducing the effective sequence length from 96 raw timesteps to approximately 11 patches'), N, PL, note='Extension beyond the thesis (design doc Q5).')

concept('C-channel-independence', 'C', 'Channel independence',
 'PatchTST treats every variable as its own univariate series and pushes each one through the same Transformer backbone with shared weights. One noisy or extreme variable therefore cannot corrupt the embedding of a stable one. The price is that cross-variable information is discarded.',
 ['4.2.2', '2.4.6'], ('4.2.2', 'PatchTST mitigates this by treating each multivariate feature as an independent channel'), [N, 'han2024ci'], 0.5)
card('C-channel-independence', 'recall', 1, 'In PatchTST channel independence, are the backbone weights shared across channels?', 'Yes: each channel goes through the same Transformer backbone with shared weights.', ['shared weights'],
 ('4.2.2', 'Each channel is processed through the same Transformer backbone using shared weights'), N, PL,
 options=['Yes, one backbone with shared weights', 'No, one backbone per channel', 'Only in the patching layer', 'Only in the prediction head'], correct='Yes, one backbone with shared weights')
card('C-channel-independence', 'recall', 2, 'Explain "feature interference" and how channel independence avoids it.',
 'When variables are concatenated into one embedding, an anomaly or high-variance noise in one (for example an industrial power spike) can corrupt the signal of stable variables. Channel independence processes each variable separately so this cannot happen.', ['interference definition', 'separate processing'],
 ('4.2.2', 'a significant anomaly or high-variance noise in one variable', 'corrupt the signal integrity of more stable variables'), N, PL)
card('C-channel-independence', 'contrast', 3, 'What is the capacity–robustness trade-off of channel independence?',
 'Channel-independent training sacrifices cross-variate representational capacity in exchange for improved robustness to distribution shift (Han et al.). Channel-mixing is more expressive but less robust.', ['capacity lost', 'robustness gained'],
 ('2.4.6', 'channel-independent training sacrifices cross-variate representational capacity in exchange for improved robustness to distribution shift'), 'han2024ci', 'Robustness')
card('C-channel-independence', 'objection', 3, 'Weather drives urban load, yet channel independence ignores it when forecasting load. Why is CI the right choice?',
 'It is a trade-off, not a settled choice: CI is more robust under drift and with heterogeneous channels, channel mixing is more expressive, and later work (iTransformer, Crossformer, CARD) argues discarding cross-variate information is suboptimal when inter-variable structure is strong. In this thesis PatchTST won on ETTh1 and Smart Meters, but the thesis attributes that to three design choices without its own CI ablation; you would test it by adding temperature as a covariate.',
 ['acknowledges the trade-off', 'cites the counter-designs', 'admits no CI ablation', 'proposes a test'],
 [('2.4.6', 'discarding cross-variate information entirely is suboptimal for datasets with strong inter-variable structure'), ('4.6.1', 'stems from three synergistic design choices')], 'han2024ci', 'Channel independent strategy')
card('C-channel-independence', 'recall', 2, 'Which design choices does the thesis credit for PatchTST\'s advantage, and what does the PatchTST paper\'s own ablation add?',
 'Three synergistic choices: temporal patching, channel independence and architectural efficiency (4.6.1). The PatchTST paper\'s ablation (Table 7, full version Table 10) shows patching together with channel independence carry most of the gain. The thesis runs no ablation of its own.', ['three choices named', 'points to the paper ablation', 'admits no own ablation'],
 ('4.6.1', 'stems from three synergistic design choices'), N, 'Table 7 (patching / CI ablation)', note='Ablation claim checked against the PatchTST paper, Tables 7 and 10.')

concept('C-revin', 'C', 'RevIN and layered normalisation',
 'Reversible Instance Normalisation normalises each input window before the model and reverses the transformation on the output, which addresses distribution shift between windows. In this thesis StandardScaler (fitted on training data only) is applied to all models and RevIN sits inside the PatchTST pipeline.',
 ['4.2.2', '2.4.6', '3.3'], ('4.2.2', 'a critical component designed to address the non-stationary nature of energy data by handling distribution shifts between training and testing sets'), [N, 'liu2022nonstationary'], 0.5)
card('C-revin', 'recall', 2, 'What does RevIN do, step by step?', 'It normalises each input window before processing and reverses the transformation on the output, which improves robustness to non-stationary input statistics.', ['normalise window', 'reverse on output'],
 ('2.4.6', 'by normalizing each input window prior to processing and reversing the transformation on the output'), N, PL)
card('C-revin', 'contrast', 3, 'Which normalisation applies to which model in your pipeline?',
 'All models: Z-score standardisation with scikit-learn\'s StandardScaler, fitted on the training partition only. In addition, RevIN is part of the PatchTST pipeline (4.2.2). The thesis does not describe RevIN for the other models. Describe the pipeline as layered.', ['StandardScaler for all', 'RevIN inside PatchTST'],
 [('3.3', "all continuous features were normalised using Z-score standardisation via scikit-learn's StandardScaler"), ('4.2.2', 'The end-to-end architectural journey begins with Reversible Instance Normalization')], N, PL)
card('C-revin', 'objection', 3, 'You call RevIN "critical". What does the PatchTST paper\'s own ablation say?',
 'In the PatchTST paper, instance normalisation improves performance only slightly (Table 11) and PatchTST still outperforms other Transformers without it. The thesis runs no RevIN ablation of its own, so "critical" is stronger than the evidence you have. Soften it or say why energy data differs.', ['cites Table 11', 'admits no own ablation', 'suggests softening'],
 ('4.2.2', 'a critical component designed to address the non-stationary nature of energy data'), N, 'Table 11 (instance normalization)', note='PatchTST paper Table 11 (p.18) says instance normalisation helps slightly. Register item R-revin-claim.')
card('C-revin', 'objection', 3, 'What is the known cost of normalising each window (over-stationarisation), and does the horizon share the lookback\'s statistics?',
 'Instance normalisation assumes the horizon shares the lookback\'s level and scale. Liu et al. call the side effect over-stationarisation: normalising away information the model needs. RevIN corrects level and scale shift between windows but not a change of shape or a structural break inside the horizon.', ['assumption about the horizon', 'names over-stationarisation'],
 ('2.4.6', 'by normalizing each input window prior to processing and reversing the transformation on the output'), 'liu2022nonstationary', 'Over-stationarization', note='Beyond the thesis (Liu et al. 2022 is on the design doc\'s verify list and is not in the thesis references).')

concept('C-flatten-head', 'C', 'Backbone-to-head and single-pass forecasts',
 'After the TSTiEncoder processes each channel, a flatten head projects the latent representation linearly into the full 24-step forecast in one forward pass. Predicting the whole horizon at once avoids the cascading error of step-by-step rollouts.',
 ['4.2.2'], ('4.2.2', 'this "Backbone-to-Head" flow generates the entire horizon in a single forward pass'), [N], 0.3)
card('C-flatten-head', 'recall', 1, 'How many forward passes does PatchTST need to produce the 24-step horizon?', 'One: the flatten head projects to all 24 steps at once.', ['single pass'],
 ('4.2.2', 'this "Backbone-to-Head" flow generates the entire horizon in a single forward pass'), N, PL,
 options=['One', '24', '11 (one per patch)', 'One per channel per step'], correct='One')
card('C-flatten-head', 'recall', 2, 'What is the "cascading error" effect and why does single-pass forecasting prevent it?',
 'A small mistake in the first predicted hour grows into a significant deviation by the end of the window when predictions are fed back step by step. Generating the whole horizon in one pass avoids feeding predictions back.', ['error growth definition', 'single pass avoids feedback'],
 ('4.2.2', 'This prevents the "cascading error" effect', 'by the end of the window'), N, PL)
card('C-flatten-head', 'objection', 3, 'Section 4.2.2 contrasts PatchTST with "recursive, step-by-step" RNNs. Is that fair to your own RNN baselines?',
 'Only partly. The LSTM-16 baseline projects its final hidden state directly to the output horizon, so it is not a recursive rollout, and the thesis does not say how the other RNNs decode. The cascading-error argument applies to recursive decoding, not to these direct-projection RNNs. Register item R-rnn-recursive.', ['notes LSTM-16 is direct', 'limits the claim to recursive decoding'],
 [('4.2.2', 'Unlike the recursive, step-by-step prediction methods used in traditional RNNs'), ('3.4.2', 'projected directly to the output horizon without additional intermediate layers')], N, PL)

concept('C-counter-designs', 'C', 'Counter-designs to channel independence',
 'The literature after PatchTST argues over how much cross-variable information to keep. iTransformer makes each variate a token; CARD adds channel-aligned attention; SAMformer blames sharp loss landscapes and adds sharpness-aware minimisation; Pathformer generalises patching to multiple adaptive scales; Crossformer models cross-dimension dependency explicitly.',
 ['2.4.6'], ('2.4.6', 'iTransformer inverts the conventional Transformer input representation, treating each variate as a token and each time step as a feature'), ['liu2024itransformer', 'wang2024card', 'ilbert2024samformer', 'chen2024pathformer'], 0.3)
card('C-counter-designs', 'recall', 1, 'Which model treats each variate as a token and each time step as a feature?', 'iTransformer.', ['iTransformer'],
 ('2.4.6', 'iTransformer inverts the conventional Transformer input representation, treating each variate as a token and each time step as a feature'), 'liu2024itransformer', 'Inverted Transformer',
 options=['iTransformer', 'PatchTST', 'Informer', 'Autoformer'], correct='iTransformer')
card('C-counter-designs', 'recall', 2, 'What does Pathformer add to the patching idea?', 'A multi-scale, adaptive patching scheme that selects patch granularity dynamically from the input series.', ['multi-scale', 'adaptive granularity'],
 ('2.4.6', 'Pathformer further generalizes the patching concept introduced by PatchTST into a multi-scale, adaptive patching scheme'), 'chen2024pathformer', 'Multi-scale patching')
card('C-counter-designs', 'contrast', 3, 'CARD and SAMformer both respond to channel-independent training. How do their diagnoses differ?',
 'CARD proposes channel-aligned attention to recover inter-variable structure that channel independence discards. SAMformer attributes part of the accuracy gap between linear models and Transformers to the sharper loss landscapes of channel-independent training and proposes sharpness-aware minimisation.', ['CARD = recover structure', 'SAMformer = sharp loss landscape'],
 [('2.4.6', 'CARD architecture proposes channel-aligned attention'), ('2.4.6', 'sharper loss landscapes induced by channel-independent training')], 'ilbert2024samformer', 'Sharpness-aware minimization')

concept('C-dlinear', 'C', 'The DLinear counterpoint',
 'Zeng et al. showed that a considerably simpler linear model can match or exceed several Transformer variants on standard benchmarks. The thesis uses this as the motive for reporting accuracy together with computational cost. No linear model was run as a baseline.',
 ['2.4.6', '1.1'], ('2.4.6', 'a considerably simpler linear model could match or exceed several Transformer variants'), ['zeng2023dlinear'], 0.5)
card('C-dlinear', 'recall', 2, 'What did Zeng et al. show, and how does the thesis use it?',
 'A considerably simpler linear model could match or exceed several Transformer variants on standard LTSF benchmarks. It motivates the thesis\'s emphasis on reporting accuracy jointly with computational cost.', ['claim', 'thesis motive'],
 ('2.4.6', 'directly motivates this thesis\'s emphasis on jointly reporting accuracy and computational cost'), 'zeng2023dlinear', 'DLinear / LTSF-Linear')
card('C-dlinear', 'objection', 3, 'Why was no linear baseline such as DLinear included, given that paper is in your bibliography?',
 'The scope (1.5) fixes the comparison to three Transformers and four recurrent baselines and treats other baselines as beyond scope. The thesis cites the linear result as motivation but did not run it, which is a genuine gap you should acknowledge and offer as future work.', ['scope statement', 'admits the gap'],
 [('1.5', 'the selection of specific models and baselines defines the boundary of the comparison'), ('1.1', 'a considerably simpler linear model could')], 'zeng2023dlinear', 'DLinear / LTSF-Linear')
