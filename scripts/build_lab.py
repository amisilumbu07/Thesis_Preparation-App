"""Builds content/lab.json: numeric derivation exercises (one per derivation card) and the results tables for the practice generator."""
import json, math, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def ev(expr):
    return eval(expr.replace('Math.', 'math.'), {'math': math})

def C(label, expr, tol, unit='', alts=None):
    d = {'label': label, 'expr': expr, 'answer': round(ev(expr), 6), 'tol': tol, 'unit': unit}
    if alts: d['alts'] = alts
    return d

def gain(base, new): return f'(({base}) - ({new})) / ({base}) * 100'
MEAN2 = lambda a, b: f'({a} + {b}) / 2'

ITEMS = [
 dict(id='LAB-attention-cost', cardId='K-quadratic-cost-3', title='Attention cost when the lookback doubles',
      setup='Vanilla self-attention compares every position with every other. Compare a lookback of L = 96 with L = 192.',
      checks=[C('Attention pairs at L = 96', 'Math.pow(96, 2)', 0.5), C('Attention pairs at L = 192', 'Math.pow(192, 2)', 0.5), C('Cost factor when L doubles', 'Math.pow(192, 2) / Math.pow(96, 2)', 0.01, 'x')]),
 dict(id='LAB-patch-96-16-8', cardId='K-patch-arith-1', title='Patches for L = 96, P = 16, S = 8',
      setup='N = floor((L - P) / S) + 1 with no padding. Then compare the attention matrix over N patches with the one over L points.',
      checks=[C('Number of patches N', 'Math.floor((96 - 16) / 8) + 1', 0), C('Attention pairs over patches (N squared)', 'Math.pow(Math.floor((96 - 16) / 8) + 1, 2)', 0), C('Shrink factor (L squared / N squared)', 'Math.pow(96, 2) / Math.pow(Math.floor((96 - 16) / 8) + 1, 2)', 0.6, 'x')]),
 dict(id='LAB-patch-steel', cardId='K-patch-arith-2', title='STEEL patches: P = 12, S = 6',
      setup='The STEEL runs used patch length 12 and stride 6 with L = 96 (author\'s code).',
      checks=[C('Number of patches N', 'Math.floor((96 - 12) / 6) + 1', 0), C('Attention pairs over patches', 'Math.pow(Math.floor((96 - 12) / 6) + 1, 2)', 0), C('Shrink factor versus L = 96', 'Math.pow(96, 2) / Math.pow(Math.floor((96 - 12) / 6) + 1, 2)', 0.6, 'x')]),
 dict(id='LAB-patch-illustration', cardId='K-patch-arith-3', title='The P = 16, S = 4 illustration in 4.2.1',
      setup='Section 4.2.1 illustrates patch length 16 with stride 4 at L = 96. The thesis elsewhere says about 11 patches.',
      checks=[C('Patches with S = 4 (22 is accepted if you pad the end)', 'Math.floor((96 - 16) / 4) + 1', 0, '', [22]), C('Patches with S = 8, for comparison', 'Math.floor((96 - 16) / 8) + 1', 0)]),
 dict(id='LAB-patch-336', cardId='K-patch-arith-4', title='Longer lookback: L = 336, P = 16, S = 8',
      setup='Extend to a lookback of 336. Patching keeps attention over few tokens.',
      checks=[C('Number of tokens N', 'Math.floor((336 - 16) / 8) + 1', 0), C('Attention pairs over points (L squared)', 'Math.pow(336, 2)', 0.5), C('Attention pairs over patches (N squared)', 'Math.pow(Math.floor((336 - 16) / 8) + 1, 2)', 0), C('Shrink factor', 'Math.pow(336, 2) / Math.pow(Math.floor((336 - 16) / 8) + 1, 2)', 0.6, 'x')]),
 dict(id='LAB-split-etth1', cardId='K-split-leakage-3', title='ETTh1 is a 70/20/10 split',
      setup='ETTh1 gives 12,177 training, 3,479 validation and 1,740 test sequences.',
      checks=[C('Total usable windows', '12177 + 3479 + 1740', 0.5), C('70% of the total', '0.7 * (12177 + 3479 + 1740)', 0.5), C('20% of the total', '0.2 * (12177 + 3479 + 1740)', 0.5), C('10% of the total', '0.1 * (12177 + 3479 + 1740)', 0.5)]),
 dict(id='LAB-window-span', cardId='K-window-setup-2', title='What lookback and horizon mean on hourly ETTh1',
      setup='ETTh1 is hourly (24 data points per day). The lookback is 96 steps and the horizon 24 steps.',
      checks=[C('Lookback in days', '96 / 24', 0.01, 'days'), C('Horizon in days', '24 / 24', 0.01, 'days')]),
 dict(id='LAB-orders-of-magnitude', cardId='K-datasets-4', title='STEEL: how many orders of magnitude?',
      setup='STEEL maxima: NSM 85,500 and CO2 0.07. Means: NSM 42,750 and CO2 0.01. Orders of magnitude = log10 of the ratio.',
      checks=[C('Orders of magnitude, maxima', 'Math.log10(85500 / 0.07)', 0.05), C('Orders of magnitude, means', 'Math.log10(42750 / 0.01)', 0.05)]),
 dict(id='LAB-bilstm-double', cardId='K-bilstm-2', title='Is BiLSTM really double an LSTM?',
      setup='STEEL: LSTM 8,632 parameters, 38.3 s; BiLSTM 18,185 parameters, 48.7 s. Smart Meters: LSTM 18,816 parameters, 1,279.4 s; BiLSTM 38,097 parameters, 1,592.2 s.',
      checks=[C('Parameter ratio, STEEL', '18185 / 8632', 0.02, 'x'), C('Parameter ratio, Smart Meters', '38097 / 18816', 0.02, 'x'), C('Training-time ratio, STEEL', '48.7 / 38.3', 0.02, 'x'), C('Training-time ratio, Smart Meters', '1592.2 / 1279.4', 0.02, 'x')]),
 dict(id='LAB-wth-patchtst-vs-informer', cardId='K-wth-result-3', title='WTH: PatchTST against Informer',
      setup='Table 4.1. Informer: 2,901,542 parameters, MSE 0.4046, 1,100.9 s. PatchTST: 399,744 parameters, MSE 0.4871, 1,452.7 s.',
      checks=[C('Informer parameters divided by PatchTST parameters', '2901542 / 399744', 0.05, 'x'), C('PatchTST MSE above Informer', '(0.4871 / 0.4046 - 1) * 100', 0.3, '%'), C('PatchTST time divided by Informer time', '1452.7 / 1100.9', 0.02, 'x')]),
 dict(id='LAB-etth1-percentages', cardId='K-etth1-result-3', title='ETTh1: which baseline gives 13.6 / 25.9 / 13.8%?',
      setup='Table 4.2. Informer: MAE 0.5560, MSE 0.5652, RMSE 0.7518. Autoformer: MAE 0.5299, MSE 0.4452, RMSE 0.6673. PatchTST: MAE 0.4689, MSE 0.3742, RMSE 0.6117. Improvement = (baseline - PatchTST) / baseline.',
      checks=[C('MAE improvement over Informer', gain('0.5560', '0.4689'), 0.1, '%'), C('MSE improvement over Informer', gain('0.5652', '0.3742'), 0.1, '%'), C('RMSE improvement over Informer', gain('0.7518', '0.6117'), 0.1, '%'),
              C('MAE improvement over the mean of Informer and Autoformer', gain(MEAN2('0.5560', '0.5299'), '0.4689'), 0.1, '%'), C('MSE improvement over the mean of Informer and Autoformer', gain(MEAN2('0.5652', '0.4452'), '0.3742'), 0.1, '%'), C('RMSE improvement over the mean of Informer and Autoformer', gain(MEAN2('0.7518', '0.6673'), '0.6117'), 0.1, '%')]),
 dict(id='LAB-steel-size-ratios', cardId='K-steel-not-capacity-2', title='STEEL: how much larger are the failing Transformers?',
      setup='Table 4.3 parameters. Informer 87,623; Autoformer 88,327; LSTM 8,632; BiLSTM 18,185; LSTM-16 4,456.',
      checks=[C('Informer / BiLSTM (smallest ratio)', '87623 / 18185', 0.05, 'x'), C('Informer / LSTM', '87623 / 8632', 0.05, 'x'), C('Autoformer / LSTM-16 (largest ratio)', '88327 / 4456', 0.05, 'x')]),
 dict(id='LAB-sm-gains', cardId='K-smart-meters-result-3', title='Smart Meters: PatchTST versus the other six models',
      setup='Table 4.4 (MAE / MSE / RMSE). LSTM 5.2733 / 81.4314 / 9.0239; BiLSTM 7.1175 / 98.8821 / 9.9439; GRU 5.2432 / 75.3838 / 8.6824; LSTM-16 8.5613 / 110.1040 / 10.4930; Informer 6.0268 / 99.1785 / 9.9588; Autoformer 4.2817 / 38.6661 / 6.2182. PatchTST 2.5819 / 20.1874 / 4.4930.',
      checks=[C('Mean MAE of the other six', '(5.2733 + 7.1175 + 5.2432 + 8.5613 + 6.0268 + 4.2817) / 6', 0.001), C('Mean MSE of the other six', '(81.4314 + 98.8821 + 75.3838 + 110.1040 + 99.1785 + 38.6661) / 6', 0.01), C('Mean RMSE of the other six', '(9.0239 + 9.9439 + 8.6824 + 10.4930 + 9.9588 + 6.2182) / 6', 0.001),
              C('MAE improvement of PatchTST', gain('(5.2733 + 7.1175 + 5.2432 + 8.5613 + 6.0268 + 4.2817) / 6', '2.5819'), 0.1, '%'), C('MSE improvement of PatchTST', gain('(81.4314 + 98.8821 + 75.3838 + 110.1040 + 99.1785 + 38.6661) / 6', '20.1874'), 0.1, '%'), C('RMSE improvement of PatchTST', gain('(9.0239 + 9.9439 + 8.6824 + 10.4930 + 9.9588 + 6.2182) / 6', '4.4930'), 0.1, '%')]),
 dict(id='LAB-sm-time', cardId='K-smart-meters-result-4', title='Smart Meters: PatchTST training time',
      setup='Table 4.4 times in seconds. PatchTST 3,905.5; Informer 11,119.1; Autoformer 10,694.7; slowest recurrent BiLSTM 1,592.2; fastest recurrent LSTM-16 1,189.7.',
      checks=[C('PatchTST time as a percentage of Informer', '3905.5 / 11119.1 * 100', 0.3, '%'), C('PatchTST time as a percentage of Autoformer', '3905.5 / 10694.7 * 100', 0.3, '%'), C('PatchTST time divided by the slowest recurrent time', '3905.5 / 1592.2', 0.03, 'x'), C('PatchTST time divided by the fastest recurrent time', '3905.5 / 1189.7', 0.03, 'x')]),
]

def num(s): return float(str(s).replace(',', ''))
tables = {}
for f in json.load(open(os.path.join(ROOT, 'thesis/facts.json'), encoding='utf-8')):
    if f['category'] != 'results': continue
    m = re.match(r'Table 4\.\d (WTH|ETTh1|STEEL|Smart Meters) (\S+)$', f['label'])
    if not m or not isinstance(f['value'], dict) or 'params' not in f['value']: continue
    v = f['value']
    if 'NaN' in (v['MAE'], v['MSE'], v['RMSE']): continue
    tables.setdefault(m.group(1), {})[m.group(2)] = {'params': num(v['params']), 'MAE': num(v['MAE']), 'MSE': num(v['MSE']), 'RMSE': num(v['RMSE']), 'time': num(v['train_s'])}

json.dump({'items': ITEMS, 'tables': tables}, open(os.path.join(ROOT, 'content/lab.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ITEMS), 'exercises;', {k: len(v) for k, v in tables.items()}, 'models per table')
for it in ITEMS: print(' ', it['id'], [c['answer'] for c in it['checks']])
