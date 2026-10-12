import json, os, re, subprocess
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
S = json.load(open(os.path.join(ROOT, 'thesis/sections.json'), encoding='utf-8'))
norm = lambda t: re.sub(r'\s+', ' ', re.sub('[​­]', '', t)).strip()
T = {k: norm(v['text']) for k, v in S.items()}

def ev(sec, start, end=None):
    """Exact excerpt of section `sec` from `start` through `end` (inclusive)."""
    t = T[sec]
    i = t.find(start)
    assert i >= 0, f'[{sec}] start not found: {start!r}'
    j = i + len(start)
    if end is not None:
        j = t.find(end, i)
        assert j >= 0, f'[{sec}] end not found: {end!r}'
        j += len(end)
    out = t[i:j]
    assert len(out) <= 460, f'[{sec}] evidence too long ({len(out)}): {start!r}'
    return out

def _pages(path):
    out = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    n = int(re.search(r'Pages:\s+(\d+)', out).group(1))
    return [subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', path, '-'], capture_output=True, text=True).stdout.lower() for i in range(1, n + 1)]

# ---------- sources ----------
# id: (cite, thesisRef, status, why, [(label, needle)])
SRC = {
 'vaswani2017': ('Vaswani et al., Attention Is All You Need, NeurIPS 2017', '[1]', 'in-project', 'Scaled dot-product attention, sqrt(d_k) scaling, positional encoding, O(L^2) cost', [('Scaled dot-product attention', 'scaled dot-product attention'), ('Multi-head attention', 'multi-head attention'), ('Positional encoding', 'positional encoding'), ('Table 1 (complexity per layer)', 'complexity per layer')]),
 'zhou2021informer': ('Zhou et al., Informer, AAAI 2021', '[7]', 'in-project', 'ProbSparse attention, self-attention distilling, generative decoder', [('ProbSparse self-attention', 'probsparse self-attention'), ('Self-attention distilling', 'self-attention distilling'), ('Generative style decoder', 'generative style decoder')]),
 'wu2021autoformer': ('Wu et al., Autoformer, NeurIPS 2021', '[8]', 'in-project', 'Series decomposition, auto-correlation', [('Series decomposition block', 'series decomposition block'), ('Auto-correlation mechanism', 'auto-correlation mechanism')]),
 'zhou2022fedformer': ('Zhou et al., FEDformer, ICML 2022', '[28]', 'in-project', 'Frequency-domain attention (reviewed, not run)', [('Frequency enhanced block', 'frequency enhanced')]),
 'nie2023patchtst': ('Nie et al., A Time Series is Worth 64 Words (PatchTST), ICLR 2023', '[9]', 'in-project', 'Patching, channel independence, ablations (Tables 7, 10, 11), seed variance (Table 14)', [('Patching and channel independence', 'channel-independence'), ('Table 7 (patching / CI ablation)', 'table 7:'), ('Table 10 (full ablation)', 'table 10:'), ('Table 11 (instance normalization)', 'table 11:'), ('Table 14 (seed variance)', 'table 14:')]),
 'zeng2023dlinear': ('Zeng et al., Are Transformers Effective for Time Series Forecasting?, AAAI 2023', '[10]', 'in-project', 'DLinear: the strongest skeptical counterpoint', [('DLinear / LTSF-Linear', 'dlinear')]),
 'han2024ci': ('Han, Ye, Zhan, The Capacity and Robustness Trade-off: Revisiting the Channel Independent Strategy, IEEE TKDE 2024', '[11]', 'verify', 'Theory for why channel independence helps and what it costs', [('Channel independent strategy', 'channel independent'), ('Robustness', 'robustness')]),
 'liu2024itransformer': ('Liu et al., iTransformer, ICLR 2024', '[30]', 'verify', 'Inverts tokens to variables; counter-design to channel independence', [('Inverted Transformer', 'inverted')]),
 'micikevicius2018mixed': ('Micikevicius et al., Mixed Precision Training, ICLR 2018', '[44]', 'verify', 'float16 range and loss scaling; cited in 4.4.3 for floating-point overflow', [('Loss scaling', 'loss scaling'), ('FP16 range', 'fp16')]),
 'liu2022nonstationary': ('Liu et al., Non-stationary Transformers, NeurIPS 2022', None, 'verify', 'Over-stationarization critique of instance normalization (not in thesis references)', [('Over-stationarization', 'over-stationarization')]),
 'dehghani2023vit22b': ('Dehghani et al., Scaling Vision Transformers to 22B Parameters, ICML 2023', None, 'verify', 'Attention-logit growth and query/key normalization (not in thesis references)', [('Attention logit growth / QK normalization', 'logit')]),
 'wortsman2023instabilities': ('Wortsman et al., Small-scale Proxies for Large-scale Transformer Training Instabilities, 2023', None, 'verify', 'Attention-logit growth as a cause of divergence (not in thesis references)', [('Attention logit growth', 'logit growth')]),
 'cho2014gru': ('Cho et al., Learning Phrase Representations using RNN Encoder-Decoder (GRU), EMNLP 2014', '[22]', 'in-thesis', 'GRU reset and update gates', [('Reset and update gates', 'reset gate'), ('Update gate', 'update gate')]),
 'pascanu2013difficulty': ('Pascanu, Mikolov, Bengio, On the difficulty of training recurrent neural networks, ICML 2013', '[41]', 'in-thesis', 'Vanishing and exploding gradients; gradient clipping', [('Vanishing / exploding gradients', 'vanishing gradient'), ('Gradient clipping', 'clipping')]),
 'bai2018tcn': ('Bai, Kolter, Koltun, An Empirical Evaluation of Generic Convolutional and Recurrent Networks (TCN), 2018', '[23]', 'in-thesis', 'Temporal convolutional networks', [('Dilated causal convolutions', 'dilated')]),
 'lai2018lstnet': ('Lai et al., LSTNet, SIGIR 2018', '[24]', 'in-thesis', 'Hybrid convolution + recurrence', [('LSTNet architecture', 'convolutional')]),
 'devlin2019bert': ('Devlin et al., BERT, NAACL 2019', '[25]', 'in-thesis', 'Learned absolute position embeddings', [('Position embeddings', 'position embeddings')]),
 'gehring2017convs2s': ('Gehring et al., Convolutional Sequence to Sequence Learning, ICML 2017', '[26]', 'in-thesis', 'Implicit position via convolution', [('Position embeddings', 'position embeddings')]),
 'shaw2018relpos': ('Shaw, Uszkoreit, Vaswani, Self-Attention with Relative Position Representations, NAACL 2018', '[27]', 'in-thesis', 'Relative positional embeddings', [('Relative position representations', 'relative position')]),
 'wang2024card': ('Wang et al., CARD, ICLR 2024', '[31]', 'in-thesis', 'Channel-aligned attention', [('Channel aligned attention', 'channel aligned')]),
 'ilbert2024samformer': ('Ilbert et al., SAMformer, ICML 2024', '[32]', 'in-thesis', 'Sharpness-aware minimization for Transformers', [('Sharpness-aware minimization', 'sharpness')]),
 'chen2024pathformer': ('Chen et al., Pathformer, ICLR 2024', '[33]', 'in-thesis', 'Multi-scale adaptive patching', [('Multi-scale patching', 'multi-scale')]),
 'wen2023survey': ('Wen et al., Transformers in Time Series: A Survey, IJCAI 2023', '[34]', 'in-thesis', 'Taxonomy and context for Chapter 2', [('Taxonomy', 'taxonomy')]),
 'lheureux2022energies': ("L'Heureux, Grolinger, Capretz, Transformer-based model for electrical load forecasting, Energies 2022", '[3]', 'in-project', 'Load-forecasting application context', [('Transformer for load forecasting', 'transformer')]),
 'kingma2015adam': ('Kingma and Ba, Adam, ICLR 2015', '[38]', 'in-thesis', 'Optimiser used throughout', [('Algorithm 1 (Adam)', 'algorithm 1')]),
 'hinton2015distill': ('Hinton, Vinyals, Dean, Distilling the Knowledge in a Neural Network, 2015', '[45]', 'in-thesis', 'Future work: knowledge distillation', [('Distillation', 'distillation')]),
 'han2016compression': ('Han, Mao, Dally, Deep Compression, ICLR 2016', '[46]', 'in-thesis', 'Future work: pruning', [('Pruning', 'pruning')]),
 'jacob2018quant': ('Jacob et al., Quantization and Training of Neural Networks, CVPR 2018', '[56]', 'in-thesis', 'Future work: quantization', [('Integer-arithmetic-only inference', 'integer-arithmetic')]),
 'mcmahan2017fedavg': ('McMahan et al., Communication-Efficient Learning of Deep Networks from Decentralized Data, AISTATS 2017', '[55]', 'in-thesis', 'Future work: federated learning', [('FederatedAveraging', 'federatedaveraging')]),
 'xu2022anomaly': ('Xu et al., Anomaly Transformer, ICLR 2022', '[54]', 'in-thesis', 'Future work: anomaly detection', [('Association discrepancy', 'association discrepancy')]),
 'li2018dcrnn': ('Li et al., DCRNN, ICLR 2018', '[52]', 'in-thesis', 'Future work: traffic forecasting', [('Traffic forecasting', 'traffic')]),
 'zhang2019deeplob': ('Zhang, Zohren, Roberts, DeepLOB, IEEE TSP 2019', '[53]', 'in-thesis', 'Future work: financial forecasting', [('Limit order books', 'limit order')]),
 'serrano2019attention': ('Serrano and Smith, Is Attention Interpretable?, ACL 2019', '[57]', 'in-thesis', 'Future work: attention interpretability', [('Attention interpretability', 'interpretab')]),
 'lopezpaz2017gem': ('Lopez-Paz and Ranzato, Gradient Episodic Memory, NeurIPS 2017', '[60]', 'in-thesis', 'Future work: continual learning', [('Continual learning', 'continual')]),
 'ribeiro2016lime': ('Ribeiro, Singh, Guestrin, Why Should I Trust You? (LIME), KDD 2016', '[62]', 'in-thesis', 'Explanation methods', [('LIME', 'lime')]),
 'ba2016layernorm': ('Ba, Kiros, Hinton, Layer Normalization, 2016', '[47]', 'in-thesis', 'Layer normalization in Transformer blocks', [('Layer normalization', 'layer normalization')]),
 'ioffe2015batchnorm': ('Ioffe and Szegedy, Batch Normalization, ICML 2015', '[48]', 'in-thesis', 'Batch normalization', [('Batch normalization', 'batch normalization')]),
 'hendrycks2016gelu': ('Hendrycks and Gimpel, GELUs, 2016', '[49]', 'in-thesis', 'GELU activation', [('GELU', 'gelu')]),
}
THESIS_SRC = ('Final thesis (Amisi Lumbu Espoir, Hohai University, Sept 2026): original experiments', None, 'thesis-original', 'The thesis is the authority for every experiment, table and figure', None)

def build_sources():
    out = []
    for sid, (cite, ref, status, why, locs) in SRC.items():
        f = f'sources/{sid}.pdf'
        pg = _pages(os.path.join(ROOT, f))
        L = []
        for label, needle in locs:
            hit = [i + 1 for i, t in enumerate(pg) if needle.lower() in t]
            assert hit, f'{sid}: locator needle not found: {needle!r}'
            L.append({'label': label, 'page': hit[0]})
        out.append({'id': sid, 'cite': cite, 'file': f, 'status': status, 'thesisRef': ref, 'why': why, 'locators': L})
    # thesis itself: one locator per section heading, plus tables
    pg = _pages(os.path.join(ROOT, 'sources/final-thesis.pdf'))
    L = []
    for n, s in S.items():
        head = norm(s['heading']).lower()[:40]
        hit = [i + 1 for i, t in enumerate(pg) if i > 8 and re.search(r'^\s*' + re.escape(n) + r'\.?\s*' + re.escape(head[:25]), re.sub('[​]', ' ', t), re.M)]
        assert hit, f'thesis heading not found for {n} {head}'
        L.append({'label': f'§{n}', 'page': hit[0]})
    for tb in ['Table 3.1', 'Table 4.1', 'Table 4.2', 'Table 4.3', 'Table 4.4']:
        needle = tb.lower() if tb == 'Table 3.1' else tb.lower() + '.'
        hit = [i + 1 for i, t in enumerate(pg) if i > 8 and needle in t]
        assert hit, tb
        L.append({'label': tb, 'page': hit[0]})
    out.append({'id': 'thesis', 'cite': THESIS_SRC[0], 'file': 'sources/final-thesis.pdf', 'status': 'thesis-original', 'thesisRef': None, 'why': THESIS_SRC[3], 'locators': L})
    return out

# ---------- concepts / cards / register ----------
CONCEPTS, CARDS, REGISTER = [], [], []
_cnt = {}

def concept(id, pillar, title, story, anchors, evidence, sources, risk=0.3, open=None, decisionId=None):
    e = ev(*evidence)
    assert all(a in S for a in anchors), (id, anchors)
    c = dict(id=id, pillar=pillar, title=title, story=story, thesisAnchors=anchors, evidence=e, sourceIds=sources, risk=risk)
    if open: c['open'] = open
    if decisionId: c['decisionId'] = decisionId
    CONCEPTS.append(c)

def card(cid, type, level, prompt, answer, rubric, evd, src, loc, anchors=None, options=None, correct=None, mode=None, open=None, decisionId=None, note=None, figure=None, followUp=None):
    evs = [evd] if isinstance(evd, tuple) else evd
    excerpts = [ev(*e) for e in evs]
    anc = anchors or []
    for e in evs:
        if e[0] not in anc: anc.append(e[0])
    _cnt[cid] = _cnt.get(cid, 0) + 1
    k = dict(id=f'K-{cid[2:]}-{_cnt[cid]}', conceptId=cid, type=type, level=level,
             mode=mode or ('intensive' if type in ('derivation', 'objection', 'register', 'transfer', 'mock') else 'both'),
             prompt=prompt, answer=answer, rubric=rubric, thesisAnchors=anc,
             evidence=excerpts[0] if len(excerpts) == 1 else excerpts, sourceId=src, sourceLocator=loc)
    if options: k['options'], k['correct'] = options, correct
    if open: k['open'] = open
    if decisionId: k['decisionId'] = decisionId
    if note: k['note'] = note
    if figure: k['figure'] = figure
    if followUp: k['followUp'] = followUp
    CARDS.append(k)

def reg(id, title, severity, status, conflict, anchors, evidence, decision, resolution, rehearsed=''):
    assert all(a in S for a in anchors), (id, anchors)
    REGISTER.append(dict(id=id, title=title, severity=severity, status=status, conflict=conflict, thesisAnchors=anchors,
                         evidence=[ev(*e) for e in evidence], decisionId=decision, resolution=resolution, rehearsedAnswer=rehearsed))
