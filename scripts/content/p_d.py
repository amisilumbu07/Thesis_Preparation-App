from content_lib import concept, card

TH = 'thesis'

concept('C-rnn-gradient', 'D', 'Vanishing and exploding gradients in plain RNNs',
 'A plain RNN multiplies the same weight matrix again and again through the unrolled sequence, so gradients shrink or blow up over long windows. Gated units (LSTM, GRU) were built to fix this.',
 ['3.4.2', '1.1'], ('3.4.2', 'A plain RNN of this form is prone to the vanishing and exploding gradient problem when trained via backpropagation through time over long sequences'), ['pascanu2013difficulty'], 0.2)
card('C-rnn-gradient', 'recall', 2, 'Why is a plain RNN prone to vanishing and exploding gradients?', 'Training by backpropagation through time repeatedly multiplies the same weight matrix through the unrolled graph over long sequences.', ['same matrix repeated', 'long sequences'],
 ('3.4.2', 'because the same weight matrix is repeatedly multiplied through the unrolled computational graph'), 'pascanu2013difficulty', 'Vanishing / exploding gradients')
card('C-rnn-gradient', 'recall', 1, 'Which architectural idea was introduced to overcome vanishing gradients in RNNs?', 'A gated memory cell (LSTM).', ['gated memory cell'],
 ('2.3.1', 'Long Short-Term Memory (LSTM) networks were introduced specifically to overcome this limitation through a gated memory-cell design'), 'pascanu2013difficulty', 'Vanishing / exploding gradients',
 options=['A gated memory cell', 'Self-attention', 'Patching', 'Series decomposition'], correct='A gated memory cell')

concept('C-lstm-gates', 'D', 'LSTM gates and bounded activations',
 'An LSTM has a forget gate, an input gate and an output gate, each a sigmoid layer over the current input and previous hidden state, plus a tanh candidate update. Every gate is bounded to [0, 1] and every content update to [-1, 1], so the contribution of any one input value is mathematically bounded. This property carries the STEEL argument.',
 ['3.4.2'], ('3.4.2', 'every gate is sigmoid-activated (bounding its output to the range [0, 1])'), ['pascanu2013difficulty', TH], 0.7)
card('C-lstm-gates', 'recall', 2, 'Name the three LSTM gates and what each decides.',
 'Forget gate: how much of the existing cell state to retain. Input gate: how much of a tanh candidate update to add. Output gate: how much of the tanh-activated cell state to expose as the new hidden state.', ['three gates', 'role of each'],
 ('3.4.2', 'a Forget Gate, which determines what proportion of the existing cell state to retain; an Input Gate'), TH, '§3.4.2', note='Primary reference [5] (Hochreiter and Schmidhuber 1997) is not in sources/; the thesis section is the source.')
card('C-lstm-gates', 'recall', 1, 'Which activation bounds every LSTM gate to the range [0, 1]?', 'Sigmoid.', ['sigmoid'],
 ('3.4.2', 'every gate is sigmoid-activated (bounding its output to the range [0, 1])'), TH, '§3.4.2',
 options=['Sigmoid', 'Tanh', 'ReLU', 'Softmax'], correct='Sigmoid')
card('C-lstm-gates', 'contrast', 3, 'Why can a single huge input value not blow up an LSTM the way it can in unbounded attention?',
 'Because gates are sigmoid-bounded and updates are tanh-bounded, the contribution of any single input value to the cell and hidden state at each timestep is mathematically bounded, however large the value. Raw dot-product attention scores have no such bound.', ['bounded gates and updates', 'contrast with unbounded scores'],
 [('3.4.2', 'regardless of the magnitude of any single input value, its contribution to the cell state and hidden state at each timestep is mathematically bounded'), ('4.4.3', 'compute raw dot-product or correlation scores with no such bound')], TH, '§3.4.2')

concept('C-bilstm', 'D', 'BiLSTM',
 'A BiLSTM runs a forward and a backward LSTM over the window and concatenates their hidden states, giving both past and future context inside the input window. The thesis says this costs about double the parameters and training time; the tables confirm the parameters but not the time.',
 ['3.4.2', '4.4.3', '4.5'], ('3.4.2', 'a Forward Layer processing the sequence from start to end, and a Backward Layer processing it from end to start'), [TH], 0.4)
card('C-bilstm', 'recall', 1, 'What are the two layers of a BiLSTM?', 'A forward layer (start to end) and a backward layer (end to start), whose hidden states are concatenated at each timestep.', ['forward + backward', 'concatenated'],
 ('3.4.2', 'a Forward Layer processing the sequence from start to end, and a Backward Layer processing it from end to start'), TH, '§3.4.2',
 options=['A forward and a backward layer', 'An encoder and a decoder', 'A sigmoid and a tanh layer', 'A trend and a seasonal layer'], correct='A forward and a backward layer')
card('C-bilstm', 'derivation', 3, 'Section 3.4.2 says BiLSTM costs about double the parameters and training time of an LSTM. Check that against Tables 4.3 and 4.4.',
 'Parameters: 18,185 / 8,632 = 2.1x (STEEL) and 38,097 / 18,816 = 2.0x (Smart Meters), so "double" holds. Training time: 48.7 s / 38.3 s = 1.27x and 1,592.2 s / 1,279.4 s = 1.24x, so time is not doubled. Register item R-bilstm-time.', ['parameter ratio 2x', 'time ratio about 1.25x', 'concludes the claim is half right'],
 [('3.4.2', 'approximately double the parameter count and training time relative to a unidirectional LSTM'), ('4.4.3', 'LSTM 8,632 0.0827 0.0419 0.2047 38.3 Success'), ('4.4.3', 'BiLSTM 18,185 0.0746 0.0358 0.1893 48.7 Success'), ('4.5', 'LSTM 18,816 5.2733 81.4314 9.0239 1,279.4'), ('4.5', 'BiLSTM 38,097 7.1175 98.8821 9.9439 1,592.2')], TH, 'Table 4.3')
card('C-bilstm', 'recall', 2, 'Does BiLSTM beat plain LSTM on accuracy?', 'It varies by dataset: better on STEEL (MAE 0.0746 vs 0.0827) but worse on Smart Meters (MAE 7.1175 vs 5.2733).', ['dataset-dependent', 'one number each way'],
 [('3.4.2', "BiLSTM's accuracy relative to plain LSTM varies by dataset"), ('4.5', 'BiLSTM 38,097 7.1175 98.8821 9.9439 1,592.2')], TH, 'Table 4.4')

concept('C-gru', 'D', 'GRU',
 'A GRU merges the LSTM\'s three gates into two (reset and update) and joins the cell and hidden state into one vector. It has fewer parameters, is lighter and often converges faster. In the results it gives the best accuracy-per-parameter among the recurrent models.',
 ['3.4.2', '4.5'], ('3.4.2', 'The GRU simplifies the LSTM', 'Update Gate'), ['cho2014gru', TH], 0.3)
card('C-gru', 'recall', 1, 'How many gates does a GRU have and what are they?', 'Two: a reset gate and an update gate.', ['reset', 'update'],
 ('3.4.2', 'The GRU simplifies the LSTM', 'Update Gate'), 'cho2014gru', 'Reset and update gates',
 options=['Two: reset and update', 'Three: forget, input, output', 'One: update', 'Four'], correct='Two: reset and update')
card('C-gru', 'recall', 2, 'What does the GRU update gate do?', 'It sets the interpolation between the previous hidden state and the tanh candidate to produce the new hidden state, through the (1 - z) and z weighting.', ['interpolation', 'previous state vs candidate'],
 ('3.4.2', 'while the Update Gate determines the interpolation between the previous hidden state and this candidate to produce the new hidden state'), 'cho2014gru', 'Update gate')
card('C-gru', 'recall', 2, 'What did the Smart Meters comparison conclude about GRU?', 'GRU offers the best accuracy-per-parameter trade-off among the recurrent models (MAE 5.2432, MSE 75.3838, RMSE 8.6824 with 16,896 parameters).', ['best accuracy per parameter among RNNs'],
 ('4.5', 'GRU offers the best accuracy-per-parameter trade-off among the recurrent models'), TH, 'Table 4.4')

concept('C-lstm16', 'D', 'LSTM-16 (the minimal configuration)',
 'LSTM-16 is a deliberately minimal single-layer LSTM with 16 hidden units whose final hidden state is projected straight to the horizon. It sets a lower bound on recurrent capacity: competitive on the seven-feature STEEL data, worst of all seven on the 26-feature Smart Meters data. It appears as "EfficientLSTM" in the code logs.',
 ['3.4.2', '4.5'], ('3.4.2', 'with a hidden dimension of 16 units'), [TH], 0.5)
card('C-lstm16', 'recall', 2, 'What is LSTM-16 and what is its role in the study?', 'A single-layer LSTM with 16 hidden units, final hidden state projected directly to the horizon, used to quantify the accuracy sacrificed at the smallest practical parameter footprint.', ['16 units', 'single layer', 'lower-bound role'],
 ('3.4.2', 'its role is specifically to quantify the accuracy sacrificed at the smallest practical parameter footprint'), TH, '§3.4.2')
card('C-lstm16', 'contrast', 3, 'LSTM-16 was competitive on STEEL and the least accurate model on Smart Meters. What does that show?',
 'A fixed minimal capacity is adequate for some forecasting tasks and inadequate for others: 4,456 parameters were enough for 7-feature STEEL (MAE 0.0718) but not for the 26-feature Smart Meters data (MAE 8.5613, worst on every metric).', ['dataset-dependent cost of the efficiency floor'],
 [('4.5', 'LSTM-16 was the fastest model overall but was simultaneously the least accurate of all seven on every metric'), ('4.4.3', 'LSTM-16 4,456 0.0718 0.0420 0.2049 34.2 Success')], TH, 'Table 4.4')
card('C-lstm16', 'recall', 2, 'Is LSTM-16 "consistently the smallest model of any tested"?', 'Not on Smart Meters: PatchTST has 9,120 parameters against LSTM-16\'s 13,424 there. It is the smallest on STEEL (4,456). Register item R-derived-ratios.', ['catches the counter-example'],
 [('3.4.2', 'consistently the smallest of any model tested'), ('4.5', 'PatchTST 9,120 2.5819 20.1874 4.4930 3,905.5')], TH, 'Table 4.4')

concept('C-cnn-hybrids', 'D', 'CNN and hybrid forecasters (literature)',
 'Temporal convolutional networks use dilated causal convolutions to widen the receptive field with stable gradients and full parallelism. LSTNet combines convolution for local patterns with recurrence for longer memory. Convolutions can decline on irregularly sampled data or very long sequences without hybridisation.',
 ['2.3.2'], ('2.3.2', 'which use dilated causal convolutions to expand the receptive field'), ['bai2018tcn', 'lai2018lstnet'], 0.1)
card('C-cnn-hybrids', 'recall', 1, 'What do temporal convolutional networks use to expand the receptive field?', 'Dilated causal convolutions.', ['dilated causal convolutions'],
 ('2.3.2', 'which use dilated causal convolutions to expand the receptive field'), 'bai2018tcn', 'Dilated causal convolutions',
 options=['Dilated causal convolutions', 'Self-attention', 'Gated recurrence', 'Patching'], correct='Dilated causal convolutions')
card('C-cnn-hybrids', 'recall', 2, 'How does LSTNet combine convolution and recurrence?', 'Convolutional layers extract local, short-term patterns and recurrent layers model longer-term dependencies.', ['conv for local', 'recurrence for long-term'],
 ('2.3.2', 'combine convolutional layers for extracting local, short-term patterns with recurrent layers for modelling longer-term dependencies'), 'lai2018lstnet', 'LSTNet architecture')

concept('C-classical', 'D', 'Classical forecasting methods',
 'ARIMA combines autoregression, differencing and moving averages; SARIMA adds seasonal terms; VAR extends autoregression to several variables; ETS uses weighted averages with trend and seasonal components. They are interpretable baselines but assume linearity and stationarity, and struggle with volatile, high-dimensional, long-horizon data.',
 ['2.2', '2.2.1', '2.2.2', '2.2.3', '2.2.4'], ('2.2.1', 'autoregression (AR), which models the relationship between an observation and its own past values'), [TH], 0.1)
card('C-classical', 'recall', 2, 'Name the three components of ARIMA.', 'Autoregression (AR), differencing (I) to achieve stationarity, and moving averages (MA) over past forecast errors.', ['AR', 'I', 'MA'],
 ('2.2.1', 'autoregression (AR), which models the relationship between an observation and its own past values', 'moving averages (MA)'), TH, '§2.2.1', note='Primary reference [14] (Box and Jenkins) is a book, not in sources/.')
card('C-classical', 'recall', 2, 'Why do classical methods restrict applicability in smart grids?', 'Their linear assumptions, limited capacity for multivariate dependencies and difficulty with long-horizon prediction.', ['linear', 'multivariate', 'long horizon'],
 ('2.2', 'their linear assumptions, limited capacity to represent multivariate dependencies, and difficulty with long-horizon prediction'), TH, '§2.2')
card('C-classical', 'recall', 1, 'What limits VAR as the number of variables grows?', 'The "curse of dimensionality": scalability falls as variables are added, and it assumes linear interactions.', ['curse of dimensionality'],
 ('2.2.3', 'reduces scalability as the number of variables grows'), TH, '§2.2.3',
 options=['Curse of dimensionality', 'Vanishing gradients', 'Quadratic attention', 'Label leakage'], correct='Curse of dimensionality')
