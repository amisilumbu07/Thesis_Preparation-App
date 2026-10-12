from content_lib import concept, card

V, VL = 'vaswani2017', 'Scaled dot-product attention'

# ===================== Pillar A: attention foundations =====================
concept('C-attention-qkv', 'A', 'Scaled dot-product attention',
 'Every Transformer block is built on one operation. Queries are compared with keys to produce weights, and the weights are applied to the values. The dot product is divided by the square root of the key dimension before the softmax so the softmax does not saturate and the gradients do not vanish. Multi-head attention runs several of these in parallel over different learned projections.',
 ['3.4.1', '2.4.1'], ('3.4.1', 'The core computational primitive underlying every block is scaled dot-product attention over a Query-Key-Value (QKV) representation'), [V], 0.2)
card('C-attention-qkv', 'recall', 1, 'Why is the dot product QKᵀ divided by √dₖ before the softmax?',
 'It rescales the scores so the softmax does not saturate, which avoids vanishingly small gradients.', ['names the rescaling', 'names vanishing gradients'],
 ('3.4.1', 'used to rescale the dot product before the softmax', 'to avoid vanishingly small gradients'), V, VL,
 options=['To avoid vanishingly small gradients', 'To make attention cost linear in L', 'To bound every output to [-1, 1]', 'To add positional information'], correct='To avoid vanishingly small gradients')
card('C-attention-qkv', 'recall', 2, 'Write scaled dot-product attention from memory and say what Q, K and V are.',
 'Attention(Q, K, V) = softmax(QKᵀ / √dₖ) V, where Q, K and V are learned linear projections of the input and dₖ is the key dimension.',
 ['correct formula', 'Q/K/V are learned linear projections', 'd_k is the key dimension'], ('3.4.1', 'where Q, K, and V are learned linear projections of the input'), V, VL)
card('C-attention-qkv', 'recall', 2, 'What does multi-head attention add to a single attention function?',
 'Several attention functions run in parallel over different learned projections, so the model attends to different representation subspaces at once.',
 ['parallel heads', 'different learned projections', 'different subspaces'],
 ('3.4.1', 'Multi-head attention computes several such attention functions in parallel', 'simultaneously'), V, 'Multi-head attention')

concept('C-quadratic-cost', 'A', 'The O(L²) cost of self-attention',
 'Self-attention compares every position with every other, so time and memory grow with the square of the sequence length L. This single fact motivates Informer, Autoformer and PatchTST, and it is why memory, not compute, is the binding constraint on a 6GB card.',
 ['3.4.1', '1.2'], ('3.4.1', "O(L²) time and memory cost with respect to sequence length L"), [V], 0.3)
card('C-quadratic-cost', 'recall', 1, 'What is the time and memory cost of standard self-attention in the sequence length L?', 'O(L²).', ['quadratic in L'],
 ('3.4.1', "O(L²) time and memory cost with respect to sequence length L"), V, 'Table 1 (complexity per layer)',
 options=['O(L)', 'O(L log L)', 'O(L²)', 'O(N²) with N patches'], correct='O(L²)')
card('C-quadratic-cost', 'recall', 2, 'Why does the problem statement single out memory under limited hardware budgets?',
 'Quadratic complexity imposes substantial memory overhead, which becomes acute under the limited hardware budgets of many utilities and research groups.',
 ['quadratic complexity', 'memory overhead', 'limited hardware'],
 ('1.2', 'imposes substantial memory overhead due to its quadratic complexity with respect to input sequence length'), V, 'Table 1 (complexity per layer)')
card('C-quadratic-cost', 'derivation', 2, 'Vanilla self-attention over a lookback of L = 96 versus L = 192. By what factor does the number of attention pairs grow?',
 '96² = 9,216 pairs and 192² = 36,864 pairs, so doubling the lookback multiplies the cost by 4.', ['squares L', 'factor of 4'],
 ('3.4.1', "O(L²) time and memory cost with respect to sequence length L"), V, 'Table 1 (complexity per layer)')

concept('C-positional-encoding', 'A', 'Positional encoding',
 'Self-attention has no notion of order, so a Transformer needs position information added to its inputs. Absolute schemes give each position a fixed or learned vector; relative schemes model the pairwise relation between positions directly.',
 ['3.4.1', '2.4.1'], ('3.4.1', 'since the architecture itself contains no recurrence and would otherwise be blind to sequence order'), [V, 'shaw2018relpos', 'devlin2019bert', 'gehring2017convs2s'], 0.1)
card('C-positional-encoding', 'recall', 1, 'Why does the Transformer need positional encoding?', 'It has no recurrence, so without it the model is blind to sequence order.', ['no recurrence', 'blind to order'],
 ('3.4.1', 'since the architecture itself contains no recurrence and would otherwise be blind to sequence order'), V, 'Positional encoding')
card('C-positional-encoding', 'contrast', 2, 'Contrast absolute and relative positional encoding.',
 'Absolute schemes assign each position a fixed or learned vector added to the input. Relative schemes model the pairwise relationship between positions directly (Shaw et al. add a learnable relative embedding to the attention keys).',
 ['absolute = per position vector', 'relative = pairwise relation'],
 ('2.4.1', 'Relative positional encoding schemes instead model the pairwise relationship between input positions directly'), 'shaw2018relpos', 'Relative position representations')

concept('C-transformer-block', 'A', 'Encoder–decoder structure and blocks',
 'Both encoder and decoder are stacks of identical blocks. An encoder block is multi-head self-attention plus a position-wise feed-forward network, each wrapped in a residual connection and layer normalisation. The decoder adds masked self-attention and cross-attention over the encoder output. In the thesis the final projection gives continuous forecasts directly, not a softmax over words.',
 ['3.4.1', '2.4.1'], ('3.4.1', 'Each encoder block consists of a multi-head self-attention module followed by a position-wise feed-forward network'), [V, 'ba2016layernorm'], 0.1)
card('C-transformer-block', 'recall', 2, 'What are the sub-layers of an encoder block, and what wraps each one?',
 'Multi-head self-attention, then a position-wise feed-forward network; residual (Add) connections and layer normalisation are applied around each sub-layer.', ['both sub-layers', 'residual + layer norm'],
 ('3.4.1', 'Each encoder block consists of a multi-head self-attention module followed by a position-wise feed-forward network'), V, 'Multi-head attention')
card('C-transformer-block', 'recall', 2, 'What does each decoder block add compared with an encoder block?',
 'A masked multi-head self-attention module and a cross-attention module that attends over the encoder output.', ['masked self-attention', 'cross-attention'],
 ('3.4.1', 'each decoder block additionally inserts a masked multi-head self-attention module and a cross-attention module that attends over the encoder'), V, 'Multi-head attention')
card('C-transformer-block', 'recall', 1, 'How does the final projection differ in the thesis\'s forecasting adaptations from the original language model?',
 'It produces continuous-valued forecasts directly instead of a softmax over output probabilities.', ['continuous values', 'no softmax over words'],
 ('3.4.1', 'in the time-series forecasting adaptations used in this thesis, this final projection instead produces continuous-valued forecasts directly'), V, 'Multi-head attention',
 options=['Continuous-valued forecasts directly', 'A softmax over output probabilities', 'A sigmoid gate', 'A convolution'], correct='Continuous-valued forecasts directly')

concept('C-parallel-vs-sequential', 'A', 'Parallel attention versus sequential recurrence',
 'Transformers process the whole input at once and relate any two timesteps directly. RNNs step through the sequence, carrying a hidden state forward. That is why Transformers parallelise well but cost O(L²), and why RNNs are cheap in memory (linear in length) but slow to train and hard to parallelise.',
 ['3.4', '2.3.1'], ('3.4', 'Transformers process the entire input sequence in parallel via self-attention'), [V, 'pascanu2013difficulty'], 0.2)
card('C-parallel-vs-sequential', 'contrast', 2, 'How do Transformers and RNNs differ in the way they process a sequence?',
 'Transformers process the whole sequence in parallel and compute relationships between arbitrary pairs of timesteps directly; RNNs go step by step, propagating information through an evolving hidden state.', ['parallel vs sequential', 'direct pairwise vs hidden state'],
 ('3.4', 'Transformers process the entire input sequence in parallel via self-attention', 'evolving hidden state'), V, 'Multi-head attention')
card('C-parallel-vs-sequential', 'recall', 2, 'Name the inherent limitation of RNN-family models that motivates attention-based architectures.',
 'Sequential processing impedes parallelisation, training is comparatively slow, and very long-range dependencies stay hard to capture.', ['not parallelisable', 'slow training', 'long-range dependencies'],
 ('2.3.1', 'their sequential processing impedes parallelization, training is comparatively slow'), 'pascanu2013difficulty', 'Vanishing / exploding gradients')

# ===================== Pillar B: efficient LTSF Transformers =====================
concept('C-informer-probsparse', 'B', 'Informer: ProbSparse attention',
 'Informer observes that self-attention is sparse: only a few query-key pairs matter. A query-sparsity measure picks the dominant queries and attention is computed only for those, cutting the cost from O(L²) to O(L log L).',
 ['3.4.1', '2.4.2'], ('3.4.1', 'only a few dot-product pairs contribute significantly to the overall attention mechanism'), ['zhou2021informer'], 0.2)
card('C-informer-probsparse', 'recall', 1, 'What complexity does ProbSparse attention reach?', 'O(L log L).', ['O(L log L)'],
 ('3.4.1', 'This mathematical refinement successfully reduces the computational burden to O(L log L)'), 'zhou2021informer', 'ProbSparse self-attention',
 options=['O(L log L)', 'O(L)', 'O(L²)', 'O(N²)'], correct='O(L log L)')
card('C-informer-probsparse', 'recall', 2, 'What observation about attention does ProbSparse exploit, and how?',
 'The attention distribution is sparse: only a few dot-product pairs contribute significantly. A query-sparsity measurement finds the dominant queries, and attention is computed only for them.', ['sparse attention observation', 'query-sparsity picks dominant queries'],
 [('3.4.1', 'only a few dot-product pairs contribute significantly to the overall attention mechanism'), ('3.4.1', 'to identify the most dominant queries')], 'zhou2021informer', 'ProbSparse self-attention')

concept('C-informer-distilling', 'B', 'Informer: self-attention distilling',
 'Between encoder layers, 1-D convolution and max-pooling halve the temporal dimension. This keeps memory manageable across stacked layers. It shrinks the hidden state; it does not change what the attention saw in each layer.',
 ['3.4.1', '2.4.2'], ('3.4.1', 'The encoder implements Self-Attention Distilling, a process that applies 1D convolutions and max-pooling between attention layers'), ['zhou2021informer'], 0.2)
card('C-informer-distilling', 'recall', 1, 'Which Informer component halves the sequence length between encoder layers?', 'Self-attention distilling (1-D convolution plus max-pooling).', ['distilling'],
 ('3.4.1', 'The encoder implements Self-Attention Distilling, a process that applies 1D convolutions and max-pooling between attention layers'), 'zhou2021informer', 'Self-attention distilling',
 options=['Self-attention distilling', 'ProbSparse attention', 'Series decomposition', 'Sub-series patching'], correct='Self-attention distilling')
card('C-informer-distilling', 'contrast', 3, 'Distilling and patching both shorten sequences. What does each do to the information attention sees?',
 'Distilling halves the hidden state between layers (convolution and max-pooling), so it saves memory across the stack. Patching groups steps into tokens before attention, so the attention matrix itself is over N patches instead of L points and each token carries a local shape.',
 ['distilling acts between layers on hidden states', 'patching acts on the input tokens', 'patching keeps local shape in each token'],
 [('3.4.1', 'This "distills" the hidden state by halving its temporal dimension at each step'), ('3.4.1', 'the input sequence is segmented into overlapping or non-overlapping patches')], 'zhou2021informer', 'Self-attention distilling')

concept('C-informer-decoder', 'B', 'Informer: generative decoder and label length',
 'The Informer decoder predicts the whole horizon in one forward pass instead of decoding step by step. In this thesis the Transformer decoders receive the last 48 steps of the lookback as a start token (label length 48).',
 ['3.4.1', '2.4.2', '3.3'], ('2.4.2', 'a generative-style decoder capable of predicting the entire output sequence in a single forward pass rather than through iterative, step-by-step decoding'), ['zhou2021informer'], 0.2)
card('C-informer-decoder', 'recall', 2, 'How does Informer\'s decoder produce the forecast, and how does that differ from RNNs?',
 'Generative inference: the whole output sequence in a single forward pass, rather than iterative step-by-step decoding.', ['single forward pass', 'not step by step'],
 ('2.4.2', 'a generative-style decoder capable of predicting the entire output sequence in a single forward pass rather than through iterative, step-by-step decoding'), 'zhou2021informer', 'Generative style decoder')
card('C-informer-decoder', 'recall', 2, 'What is the label length in this thesis and who uses it?',
 '48 timesteps: it overlaps the final 48 steps of the lookback and is given to the Transformer decoders as a start token. The recurrent models and PatchTST consume only the lookback.', ['48', 'start token for decoders', 'RNNs and PatchTST do not use it'],
 ('3.3', 'The Label length overlaps with the final 48 steps of the Lookback window and is provided to the Transformer decoders as a'), 'zhou2021informer', 'Generative style decoder')

concept('C-autoformer-decomposition', 'B', 'Autoformer: series decomposition',
 'Autoformer builds a decomposition block into the model. It continuously splits hidden states into a trend-cyclical component (long-term progression) and a seasonal component (repeating patterns), instead of treating the series as a flat set of tokens.',
 ['3.4.1', '2.4.3'], ('3.4.1', 'the Trend-Cyclical component, which captures the long-term progression of the data'), ['wu2021autoformer'], 0.2)
card('C-autoformer-decomposition', 'recall', 1, 'Into which two components does Autoformer\'s decomposition block split the hidden state?', 'A trend-cyclical component and a seasonal component.', ['trend-cyclical', 'seasonal'],
 ('3.4.1', 'the Trend-Cyclical component, which captures the long-term progression of the data'), 'wu2021autoformer', 'Series decomposition block',
 options=['Trend-cyclical and seasonal', 'Signal and noise', 'Low and high frequency only', 'Past and future'], correct='Trend-cyclical and seasonal')
card('C-autoformer-decomposition', 'recall', 2, 'Why did Autoformer look worse than Informer at 5 epochs on WTH?',
 'It is a slower learner because of its internal series-decomposition blocks; at 10 epochs it improved markedly and both models reached comparable validation losses.', ['slower learner', 'decomposition blocks', '10 epochs fixed it'],
 ('4.4.1', 'a slower learner owing to its internal series-decomposition blocks'), 'wu2021autoformer', 'Series decomposition block')

concept('C-autoformer-autocorrelation', 'B', 'Autoformer: auto-correlation',
 'Autoformer replaces point-wise dot-product attention with an auto-correlation mechanism. It uses the FFT to compute autocorrelation in the frequency domain, finds period-based dependencies, and aggregates similar sub-series across periods, for O(L log L) cost.',
 ['3.4.1', '2.4.3'], ('3.4.1', 'It utilizes the Fast Fourier Transform (FFT) to calculate autocorrelation in the frequency domain'), ['wu2021autoformer'], 0.3)
card('C-autoformer-autocorrelation', 'contrast', 2, 'How does auto-correlation differ from standard attention?',
 'Standard attention compares points (point-to-point similarity), which is expensive and noise-prone. Auto-correlation finds similarity between sub-series, using the FFT to discover period-based dependencies, at O(L log L).', ['point vs sub-series', 'FFT / period-based'],
 ('3.4.1', 'While standard attention calculates point-to-point similarities', 'Auto-Correlation identifies sub-series level similarities'), 'wu2021autoformer', 'Auto-correlation mechanism')
card('C-autoformer-autocorrelation', 'recall', 1, 'What transform does Autoformer use to compute auto-correlation efficiently?', 'The Fast Fourier Transform (FFT).', ['FFT'],
 ('3.4.1', 'It utilizes the Fast Fourier Transform (FFT) to calculate autocorrelation in the frequency domain'), 'wu2021autoformer', 'Auto-correlation mechanism',
 options=['Fast Fourier Transform', 'Wavelet transform', 'Principal component analysis', 'Discrete cosine only'], correct='Fast Fourier Transform')

concept('C-fedformer', 'B', 'FEDformer (reviewed, not run)',
 'FEDformer works in the frequency domain: it keeps a compact set of dominant spectral components and uses a mixture-of-experts decomposition. It appears in the literature review for completeness. It was not one of the models empirically evaluated in the thesis.',
 ['2.4.4', '1.5'], ('2.4.4', 'FEDformer is included in this literature review for architectural completeness, though it was not among the models empirically evaluated in this thesis'), ['zhou2022fedformer'], 0.4)
card('C-fedformer', 'recall', 1, 'Which of these models was NOT empirically evaluated in the thesis?', 'FEDformer (reviewed only).', ['FEDformer'],
 ('2.4.4', 'it was not among the models empirically evaluated in this thesis'), 'zhou2022fedformer', 'Frequency enhanced block',
 options=['Informer', 'Autoformer', 'PatchTST', 'FEDformer'], correct='FEDformer')
card('C-fedformer', 'objection', 3, 'Why does FEDformer appear in Chapter 2 but not in your experiments?',
 'It is included for architectural completeness. The scope (1.5) fixes the comparison to Informer, Autoformer and PatchTST against four recurrent baselines and treats generalisation to other Transformer variants as beyond scope.', ['completeness in the review', 'scope statement'],
 [('2.4.4', 'included in this literature review for architectural completeness'), ('1.5', 'generalization to other Transformer variants or baseline models is beyond its immediate scope')], 'zhou2022fedformer', 'Frequency enhanced block')
