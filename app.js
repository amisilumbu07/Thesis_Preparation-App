(function () {
'use strict';
var D = window.LOOKBACK;
var app = document.getElementById('app');
var DAY = 864e5;

// ---------- data indexes ----------
var cmap = {}, smap = {}, kmap = {}, secmap = D.sections;
D.concepts.forEach(function (c) { cmap[c.id] = c; });
D.sources.forEach(function (s) { smap[s.id] = s; });
D.cards.forEach(function (k) { kmap[k.id] = k; });
var PILLARS = { A: 'Attention foundations', B: 'Efficient LTSF Transformers', C: 'PatchTST mechanics', D: 'Recurrent baselines and classical methods', E: 'Experimental design and metrics', F: 'The findings', R: 'Vulnerability register', M: 'Mock viva' };
var LEVELS = ['Recognize', 'Explain', 'Defend', 'Extend'];
var PLAN = D.decisions.studyPlan;
var DECISIONS = {};
D.decisions.decisions.forEach(function (d) { DECISIONS[d.id] = d; });

// ---------- tiny DOM helper (no innerHTML, so content can never inject markup) ----------
function h(tag, props) {
  var el = document.createElement(tag);
  props = props || {};
  Object.keys(props).forEach(function (k) {
    var v = props[k];
    if (v == null || v === false) return;
    if (k === 'class') el.className = v;
    else if (k === 'text') el.textContent = v;
    else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  });
  for (var i = 2; i < arguments.length; i++) add(el, arguments[i]);
  return el;
}
function add(el, kid) {
  if (kid == null || kid === false) return;
  if (Array.isArray(kid)) { kid.forEach(function (k) { add(el, k); }); return; }
  el.appendChild(typeof kid === 'object' ? kid : document.createTextNode(String(kid)));
}
function chip(text, cls) { return h('span', { class: 'chip ' + (cls || ''), text: text }); }
function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); }

// ---------- progress (localStorage, with in-memory fallback) ----------
var KEY = 'lookback-progress-v1';
var memory = null;
function load() {
  try { var s = localStorage.getItem(KEY); if (s) return JSON.parse(s); } catch (e) { if (memory) return memory; }
  return { cards: {}, register: {}, mock: [], lab: { done: 0, correct: 0 } };
}
var P = load();
P.mock = P.mock || [];
P.lab = P.lab || { done: 0, correct: 0 };
function save() { memory = P; try { localStorage.setItem(KEY, JSON.stringify(P)); } catch (e) { /* private mode */ } }

// ---------- scheduling: SM-2 style with risk weighting ----------
function daysLeft() {
  var end = new Date(PLAN.end + 'T23:59:59').getTime();
  return Math.max(0, Math.ceil((end - Date.now()) / DAY));
}
function intervalCap() { return Math.max(1, Math.floor(daysLeft() / 3)); }
function riskWeight(card) {
  var c = cmap[card.conceptId];
  return c.risk * 2 + ((card.type === 'register' || card.open) ? 1 : 0);
}
function retention(state) {
  if (!state) return 0;
  var elapsed = (Date.now() - state.reviewed) / DAY;
  return Math.pow(0.9, elapsed / Math.max(1, state.interval || 1));
}
function priority(card) {
  return (1 - retention(P.cards[card.id])) * (1 + riskWeight(card)) * (1 + 2 / Math.max(1, daysLeft()));
}
// q: 1 Again, 2 Hard, 3 Good, 4 Easy
function schedule(state, q) {
  var s = state || { ease: 2.5, interval: 0, reps: 0, lapses: 0 };
  var now = Date.now();
  if (q === 1) {
    s.reps = 0; s.interval = 0; s.lapses += 1; s.ease = Math.max(1.3, s.ease - 0.2);
  } else {
    if (q === 2) { s.interval = Math.max(1, Math.round((s.interval || 1) * 1.2)); s.ease = Math.max(1.3, s.ease - 0.15); }
    else if (s.reps === 0) s.interval = q === 4 ? 2 : 1;
    else if (s.reps === 1) s.interval = q === 4 ? 4 : 3;
    else s.interval = Math.round(s.interval * s.ease * (q === 4 ? 1.3 : 1));
    if (q === 4) s.ease += 0.15;
    s.interval = Math.min(s.interval, intervalCap());
    s.reps += 1;
  }
  s.last = q; s.reviewed = now; s.due = now + s.interval * DAY;
  return s;
}
function rate(card, q, answerText) {
  var s = schedule(P.cards[card.id], q);
  if (answerText) s.answer = answerText;
  P.cards[card.id] = s;
  save();
  return s;
}
function passed(card) { var s = P.cards[card.id]; return !!s && s.last >= 3; }
function conceptCards(cid) { return D.cards.filter(function (c) { return c.conceptId === cid; }); }
// highest level L such that every card at levels <= L that exists for this concept has been passed
function conceptLevel(cid) {
  var cards = conceptCards(cid), lvl = 0;
  for (var L = 1; L <= 4; L++) {
    var at = cards.filter(function (c) { return c.level === L; });
    if (at.length && !at.every(passed)) break;
    if (at.length) lvl = L;
  }
  return lvl;
}
function maxLevel(cid) { return conceptCards(cid).reduce(function (m, c) { return Math.max(m, c.level); }, 0); }
// defended = level 3 reached, or every card passed when the concept has no level-3 card
function defended(cid) { return conceptLevel(cid) >= Math.min(3, maxLevel(cid)); }
function readiness() {
  var total = D.concepts.length, def = D.concepts.filter(function (c) { return defended(c.id); });
  var base = total ? 100 * def.length / total : 0;
  var unresolved = D.register.filter(function (r) { return r.severity === 'high' && r.status !== 'fixed' && !(P.register[r.id] || {}).rehearsed; });
  var pillars = [];
  Object.keys(PILLARS).forEach(function (p) {
    var cs = D.concepts.filter(function (c) { return c.pillar === p; });
    if (cs.length) pillars.push({ p: p, share: cs.filter(function (c) { return defended(c.id); }).length / cs.length });
  });
  var low = pillars.filter(function (x) { return x.share < 0.6; });
  var score = Math.max(0, base - 3 * unresolved.length - 5 * low.length);
  var registerOpen = D.register.filter(function (r) { return r.status !== 'fixed' && !(P.register[r.id] || {}).rehearsed; }).length;
  var passedMocks = P.mock.filter(function (m) { return m.passed; }).length;
  var weakest = D.concepts.filter(function (c) { return !defended(c.id); }).sort(function (a, b) { return conceptLevel(a.id) - conceptLevel(b.id) || b.risk - a.risk; }).slice(0, 3);
  return { score: score, base: base, defended: def.length, total: total, unresolved: unresolved, low: low, registerOpen: registerOpen, passedMocks: passedMocks, weakest: weakest };
}
function buildQueue(mode, pillar, ahead, n) {
  var now = Date.now();
  var pool = D.cards.filter(function (c) {
    if (pillar && cmap[c.conceptId].pillar !== pillar) return false;
    var ok = mode === 'relaxed' ? (c.mode === 'both' && c.level <= 2) : c.level >= 2;
    if (!ok) return false;
    var s = P.cards[c.id];
    return ahead || !s || s.due <= now;
  });
  pool.forEach(function (c) { c._p = priority(c); });
  pool.sort(function (a, b) { return b._p - a._p; });
  var out = [], last = null;
  while (pool.length && out.length < (n || 20)) {
    var i = 0;
    for (var j = 0; j < pool.length; j++) { if (pool[j].conceptId !== last) { i = j; break; } }
    var pick = pool.splice(i, 1)[0];
    out.push(pick); last = pick.conceptId;
  }
  return out;
}
function counts() {
  var now = Date.now(), due = 0, fresh = 0, seen = 0;
  D.cards.forEach(function (c) { var s = P.cards[c.id]; if (!s) fresh++; else { seen++; if (s.due <= now) due++; } });
  return { due: due, fresh: fresh, seen: seen };
}

// ---------- shared pieces ----------
function sectionBlock(secId, evidence) {
  var sec = secmap[secId];
  if (!sec) return null;
  var body = h('pre', { class: 'sec' });
  var text = sec.text, done = false;
  if (evidence) {
    var words = evidence.split(/\s+/).filter(Boolean).map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); });
    var m = new RegExp(words.join('\\s+')).exec(text);
    if (m) { body.appendChild(document.createTextNode(text.slice(0, m.index))); body.appendChild(h('mark', { text: m[0] })); body.appendChild(document.createTextNode(text.slice(m.index + m[0].length))); done = true; }
  }
  if (!done) body.textContent = text;
  return h('details', {}, h('summary', { text: 'Thesis §' + secId + ' — ' + sec.heading }), h('div', { class: 'body' }, body));
}
function sourceLine(card) {
  var s = smap[card.sourceId];
  if (!s) return null;
  var loc = (s.locators || []).filter(function (l) { return l.label === card.sourceLocator; })[0];
  var bits = [h('strong', { text: s.cite }), ' · ', card.sourceLocator || ''];
  if (loc) bits.push(' (p.' + loc.page + ') ');
  bits.push(chip(s.status, s.status === 'verify' ? 'verify' : s.status === 'thesis-original' ? 'sig' : ''));
  if (loc) bits.push(' ', h('a', { href: s.file + '#page=' + loc.page, target: '_blank', rel: 'noopener', text: 'open PDF' }));
  return h('p', { class: 'muted' }, bits);
}
function flags(card) {
  var out = [];
  if (card.open) out.push(h('div', { class: 'note warn' }, h('p', { text: 'Open item: ' + (card.open.reason || 'not settled yet') })));
  if (card.decisionId && DECISIONS[card.decisionId]) out.push(h('p', { class: 'muted' }, 'Author decision: ', chip(card.decisionId, DECISIONS[card.decisionId].status === 'decided' ? 'ok' : 'open'), ' ', DECISIONS[card.decisionId].topic));
  if (card.note) out.push(h('p', { class: 'muted', text: card.note }));
  return out;
}
function answerBlock(card, opts) {
  opts = opts || {};
  var ev = Array.isArray(card.evidence) ? card.evidence : [card.evidence];
  return h('div', { class: 'answer' },
    h('h3', { text: 'Model answer' }), h('p', { text: card.answer }),
    !opts.noRubric && card.rubric && card.rubric.length ? h('div', {}, h('h3', { text: 'Your answer should contain' }), h('ul', { class: 'plain' }, card.rubric.map(function (r) { return h('li', { text: r }); }))) : null,
    !opts.noFollow && card.followUp ? h('div', { class: 'note' }, h('p', {}, h('strong', { text: 'Follow-up: ' }), card.followUp)) : null,
    h('h3', { text: 'Thesis evidence' }),
    ev.map(function (e) { return h('blockquote', {}, '“' + e + '”'); }),
    card.thesisAnchors.map(function (a) { return sectionBlock(a, ev[0]); }),
    sourceLine(card),
    flags(card)
  );
}
function cardHead(card) {
  var c = cmap[card.conceptId];
  return h('div', { class: 'row' },
    chip(c.pillar + ' · ' + PILLARS[c.pillar], 'sig'), chip(card.type, 'hor'), chip('L' + card.level + ' ' + LEVELS[card.level - 1]),
    card.open ? chip('open', 'open') : null, card.figure ? chip(card.figure) : null);
}
function ladder(level) {
  var kids = [];
  for (var i = 1; i <= 4; i++) kids.push(h('i', { class: i <= level ? 'on' : '' }));
  return h('span', { class: 'ladder', title: 'Mastery level ' + level + ' of 4' }, kids);
}

// ---------- screens ----------
var screens = {};

screens.home = function () {
  var n = counts(), start = new Date(PLAN.start + 'T00:00:00').getTime();
  var day = Math.floor((Date.now() - start) / DAY) + 1, inWindow = day >= 1 && day <= PLAN.days;
  var R = readiness();
  var view = h('div', {},
    h('h1', { text: 'Lookback' }),
    h('p', { class: 'lede', text: 'Study app for defending “Time Series Load Forecasting using Transformers”. Every card is anchored to a thesis section and a source paper.' }),
    h('div', { class: 'grid' },
      h('div', { class: 'card' }, h('div', { class: 'stat' }, String(daysLeft()), h('small', { text: 'days to ' + PLAN.end + (PLAN.defenseDate ? '' : ' (study window end; defense date not set)') }))),
      h('div', { class: 'card' }, h('div', { class: 'stat' }, String(n.due + n.fresh), h('small', { text: n.due + ' due, ' + n.fresh + ' new, ' + n.seen + ' seen of ' + D.cards.length + ' cards' }))),
      h('div', { class: 'card' }, h('div', { class: 'stat' }, Math.round(R.score) + '%', h('small', { text: 'readiness score' })))),
    inWindow ? h('p', { class: 'muted', text: 'Study window: day ' + day + ' of ' + PLAN.days + ', about ' + PLAN.hoursPerDay + ' hours per day.' }) : h('p', { class: 'muted', text: 'Study window ' + PLAN.start + ' to ' + PLAN.end + ' (' + PLAN.hoursPerDay + ' h per day).' }),
    h('div', { class: 'row' },
      h('a', { class: 'btn primary', href: '#/study?mode=intensive', text: 'Start viva drill (intensive)' }),
      h('a', { class: 'btn', href: '#/mock', text: 'Mock viva' }),
      h('a', { class: 'btn', href: '#/lab', text: 'Derivation lab' }),
      h('a', { class: 'btn', href: '#/study?mode=relaxed', text: 'Reading room (relaxed)' }),
      h('a', { class: 'btn', href: '#/atlas', text: 'Browse concepts' })),
    readinessBlock(R),
    h('h2', { text: 'Progress by pillar' }),
    Object.keys(PILLARS).map(function (p) {
      var cards = D.cards.filter(function (c) { return cmap[c.conceptId].pillar === p; });
      if (!cards.length) return null;
      var done = cards.filter(passed).length;
      return h('div', { class: 'pillar' }, h('div', { class: 'row' }, h('span', { text: p + ' · ' + PILLARS[p] }), h('span', { class: 'muted', text: done + '/' + cards.length })),
        h('div', { class: 'bar' }, h('i', { style: 'width:' + Math.round(100 * done / cards.length) + '%' })));
    }),
    h('h2', { text: 'Your progress data' }),
    h('p', { class: 'muted', text: 'Progress is stored in this browser only. Export it to keep a backup or move to another device.' }),
    progressButtons());
  return view;
};

function readinessBlock(R) {
  var mark = function (ok) { return ok ? '\u2611 ' : '\u2610 '; };
  return h('div', {},
    h('h2', { text: 'Readiness' }),
    h('div', { class: 'bar', role: 'img', 'aria-label': 'Readiness ' + Math.round(R.score) + ' percent' }, h('i', { style: 'width:' + Math.round(R.score) + '%' })),
    h('ul', { class: 'plain', style: 'margin-top:10px' },
      h('li', { text: R.defended + ' of ' + R.total + ' concepts defended (level 3, or all cards passed): ' + Math.round(R.base) + '%' }),
      h('li', { text: '\u2212' + 3 * R.unresolved.length + ' points for ' + R.unresolved.length + ' unresolved high-severity register items' }),
      h('li', { text: '\u2212' + 5 * R.low.length + ' points for ' + R.low.length + ' pillars below 60%' + (R.low.length ? ' (' + R.low.map(function (x) { return x.p; }).join(', ') + ')' : '') })),
    h('p', { class: 'muted', text: 'Honest by design: it cannot reach 100% while a high-severity inconsistency has no rehearsed answer. Mark register items as rehearsed on the Register screen.' }),
    h('h3', { text: 'Definition of done' }),
    h('ul', { class: 'plain' },
      h('li', { text: mark(R.defended === R.total) + 'Every concept defended (' + R.defended + '/' + R.total + ')' }),
      h('li', { text: mark(R.registerOpen === 0) + 'Every register item fixed or rehearsed (' + R.registerOpen + ' remaining)' }),
      h('li', { text: mark(R.passedMocks >= 2) + 'Two mock vivas at 80% or more (' + Math.min(2, R.passedMocks) + '/2)' })),
    R.weakest.length ? h('p', {}, h('strong', { text: 'Weakest: ' }), R.weakest.map(function (c, i) { return [i ? ', ' : '', h('a', { href: '#/concept/' + c.id, text: c.title })]; })) : null);
}

function progressButtons() {
  var msg = h('span', { class: 'muted', role: 'status' });
  var file = h('input', { type: 'file', accept: 'application/json', hidden: true, onchange: function () {
    var f = file.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var d = JSON.parse(r.result);
        if (!d || typeof d.cards !== 'object') throw new Error('not a Lookback export');
        P = { cards: d.cards, register: d.register || {}, mock: d.mock || [], lab: d.lab || { done: 0, correct: 0 }, theme: d.theme }; save(); msg.textContent = 'Imported ' + Object.keys(P.cards).length + ' card records.'; render();
      } catch (e) { msg.textContent = 'Import failed: ' + e.message; }
    };
    r.readAsText(f);
  } });
  var reset = h('button', { type: 'button', class: 'btn danger', text: 'Reset progress', onclick: function () {
    if (reset.getAttribute('data-sure') !== '1') { reset.setAttribute('data-sure', '1'); reset.textContent = 'Click again to erase all progress'; return; }
    P = { cards: {}, register: {}, mock: [], lab: { done: 0, correct: 0 } }; save(); render();
  } });
  return h('div', { class: 'row' },
    h('button', { type: 'button', class: 'btn', text: 'Export JSON', onclick: function () {
      var blob = new Blob([JSON.stringify(P, null, 1)], { type: 'application/json' });
      var a = h('a', { href: URL.createObjectURL(blob), download: 'lookback-progress.json' });
      document.body.appendChild(a); a.click(); document.body.removeChild(a); msg.textContent = 'Exported.';
    } }),
    h('button', { type: 'button', class: 'btn', text: 'Import JSON', onclick: function () { file.click(); } }), file, reset, msg);
}

screens.atlas = function (parts, params) {
  var only = params.pillar;
  return h('div', {},
    h('h1', { text: 'Concepts' }),
    h('p', { class: 'muted', text: D.concepts.length + ' concepts, ' + D.cards.length + ' cards. The bar shows mastery level (Recognize, Explain, Defend, Extend).' }),
    h('div', { class: 'row' }, h('a', { class: 'chip' + (only ? '' : ' sig'), href: '#/atlas', text: 'All' }),
      Object.keys(PILLARS).map(function (p) { return h('a', { class: 'chip' + (only === p ? ' sig' : ''), href: '#/atlas?pillar=' + p, title: PILLARS[p], text: p }); })),
    Object.keys(PILLARS).filter(function (p) { return !only || only === p; }).map(function (p) {
      var cs = D.concepts.filter(function (c) { return c.pillar === p; });
      if (!cs.length) return null;
      return h('div', {}, h('h2', { text: p + ' · ' + PILLARS[p] }),
        h('div', { class: 'grid' }, cs.map(function (c) {
          var n = conceptCards(c.id).length, lvl = conceptLevel(c.id);
          return h('a', { class: 'card link', href: '#/concept/' + c.id },
            h('strong', { text: c.title }), h('div', { class: 'row', style: 'margin-top:6px' }, ladder(lvl), h('span', { class: 'muted', text: n + ' cards' }),
              c.open ? chip('open', 'open') : null, c.decisionId ? chip('decision', 'medium') : null, c.sourceIds.some(function (s) { return smap[s] && smap[s].status === 'verify'; }) ? chip('verify', 'verify') : null));
        })));
    }));
};

screens.concept = function (parts) {
  var c = cmap[parts[1]];
  if (!c) return h('p', { text: 'Concept not found.' });
  var ev = c.evidence;
  return h('div', {},
    h('p', {}, h('a', { href: '#/atlas?pillar=' + c.pillar, text: '← ' + PILLARS[c.pillar] })),
    h('h1', { text: c.title }),
    h('div', { class: 'row' }, ladder(conceptLevel(c.id)), chip('risk ' + c.risk.toFixed(1), c.risk >= 0.7 ? 'high' : c.risk >= 0.4 ? 'medium' : 'low'), c.decisionId ? chip(c.decisionId, 'medium') : null),
    h('p', { class: 'lede', text: c.story }),
    h('h3', { text: 'In the thesis' }), h('blockquote', {}, '“' + ev + '”'),
    c.thesisAnchors.map(function (a) { return sectionBlock(a, ev); }),
    h('h3', { text: 'Sources' }),
    h('ul', { class: 'plain' }, c.sourceIds.map(function (id) {
      var s = smap[id]; return s ? h('li', {}, s.cite, ' ', chip(s.status, s.status === 'verify' ? 'verify' : s.status === 'thesis-original' ? 'sig' : ''), ' ', h('a', { href: s.file, target: '_blank', rel: 'noopener', text: 'PDF' })) : null;
    })),
    h('h2', { text: 'Cards' }),
    conceptCards(c.id).map(function (card) {
      var s = P.cards[card.id];
      return h('details', {}, h('summary', {}, chip('L' + card.level), ' ', chip(card.type, 'hor'), ' ', card.prompt, s ? ' ' : '', s ? chip(s.last >= 3 ? 'passed' : 'again', s.last >= 3 ? 'ok' : 'open') : ''),
        h('div', { class: 'body' }, answerBlock(card)));
    }),
    h('p', {}, h('a', { class: 'btn primary', href: '#/study?mode=intensive&concept=' + c.id, text: 'Drill this concept' })));
};

// ---- study session ----
var session = null;
screens.study = function (parts, params) {
  var mode = params.mode === 'intensive' ? 'intensive' : 'relaxed';
  if (!session || session.key !== location.hash) {
    var queue;
    if (params.concept) queue = conceptCards(params.concept).filter(function (c) { return mode === 'intensive' || (c.mode === 'both' && c.level <= 2); });
    else queue = buildQueue(mode, params.pillar, params.ahead === '1', 20);
    session = { key: location.hash, mode: mode, queue: queue, i: 0, revealed: false, picked: null, ratings: [0, 0, 0, 0, 0], total: queue.length, again: {} };
  }
  return studyView();
};

function studyView() {
  var S = session, wrap = h('div', {});
  wrap.appendChild(h('div', { class: 'study-head' },
    h('span', { text: (S.mode === 'relaxed' ? 'Reading room (relaxed)' : 'Viva drill (intensive)') }),
    h('span', {}, S.mode === 'relaxed' ? h('a', { href: '#/study?mode=intensive', text: 'switch to intensive' }) : h('a', { href: '#/study?mode=relaxed', text: 'switch to relaxed' })),
    h('span', { text: S.i < S.queue.length ? (S.i + 1) + ' of ' + S.queue.length : 'done' })));
  if (S.i >= S.queue.length) { wrap.appendChild(summary(S)); return wrap; }
  var card = S.queue[S.i];
  var mcq = card.options && S.mode === 'relaxed';
  wrap.appendChild(cardHead(card));
  wrap.appendChild(h('p', { class: 'prompt', text: card.prompt }));
  if (S.mode === 'relaxed' || card.options == null) { /* no timer: simple version */ }

  if (mcq) {
    var opts = h('div', { class: 'opts' });
    card.options.forEach(function (o, idx) {
      var cls = 'opt';
      if (S.revealed) cls += o === card.correct ? ' right' : (o === S.picked ? ' wrong' : '');
      opts.appendChild(h('button', { type: 'button', class: cls, disabled: S.revealed, onclick: function () { pickOption(o); } }, h('kbd', { text: String(idx + 1) }), o));
    });
    wrap.appendChild(opts);
    if (S.revealed) {
      wrap.appendChild(h('p', { role: 'status', class: S.picked === card.correct ? 'chip ok' : 'chip open', text: S.picked === card.correct ? 'Correct' : 'Not quite: the answer is highlighted' }));
      wrap.appendChild(answerBlock(card));
      wrap.appendChild(h('div', { class: 'row', style: 'margin-top:14px' }, h('button', { type: 'button', class: 'btn primary', id: 'nextbtn', text: 'Next (space)', onclick: next })));
    } else wrap.appendChild(h('p', { class: 'hint', text: 'Press 1–4 to choose an option.' }));
    return wrap;
  }

  if (!S.revealed) {
    wrap.appendChild(h('textarea', { id: 'ans', placeholder: 'Answer in your own words (optional, saved with your rating)', 'aria-label': 'Your answer' }));
    wrap.appendChild(h('div', { class: 'row', style: 'margin-top:10px' },
      h('button', { type: 'button', class: 'btn primary', id: 'revealbtn', text: 'Reveal answer (space)', onclick: reveal }),
      h('button', { type: 'button', class: 'btn', text: 'Skip', onclick: next })));
    wrap.appendChild(h('p', { class: 'hint', text: 'Press space to reveal (Ctrl+Enter while typing). Then rate 1 Again, 2 Hard, 3 Good, 4 Easy.' }));
  } else {
    var mine = S.typed;
    if (mine) wrap.appendChild(h('div', { class: 'note' }, h('p', {}, h('strong', { text: 'Your answer: ' }), mine)));
    wrap.appendChild(answerBlock(card));
    var labels = ['Again', 'Hard', 'Good', 'Easy'];
    wrap.appendChild(h('div', { class: 'rate', role: 'group', 'aria-label': 'Rate your answer' }, labels.map(function (l, i) {
      return h('button', { type: 'button', class: 'btn', onclick: function () { doRate(i + 1); } }, h('kbd', { text: String(i + 1) }), l);
    })));
  }
  return wrap;
}
function summary(S) {
  var done = S.ratings.reduce(function (a, b) { return a + b; }, 0), n = counts();
  return h('div', {},
    h('h1', { text: S.total ? 'Session complete' : 'Nothing due right now' }),
    S.total ? h('p', { text: done + ' cards rated: ' + S.ratings[1] + ' again, ' + S.ratings[2] + ' hard, ' + S.ratings[3] + ' good, ' + S.ratings[4] + ' easy.' }) : h('p', { class: 'muted', text: 'Every card in this mode is scheduled for later (' + n.seen + ' seen, ' + n.fresh + ' new elsewhere).' }),
    h('div', { class: 'row' },
      h('a', { class: 'btn primary', href: '#/study?mode=' + S.mode + '&ahead=1&r=' + Date.now(), text: 'Study ahead' }),
      h('a', { class: 'btn', href: '#/', text: 'Home' }), h('a', { class: 'btn', href: '#/atlas', text: 'Concepts' })));
}
function pickOption(o) {
  var S = session, card = S.queue[S.i];
  if (S.revealed) return;
  S.picked = o; S.revealed = true;
  var q = o === card.correct ? 3 : 1;
  rate(card, q); S.ratings[q] += 1;
  if (q === 1 && !S.again[card.id]) { S.again[card.id] = 1; S.queue.push(card); }
  render(true);
}
function reveal() {
  var S = session, ta = document.getElementById('ans');
  S.typed = ta ? ta.value.trim() : ''; S.revealed = true; render(true);
}
function doRate(q) {
  var S = session, card = S.queue[S.i];
  rate(card, q, S.typed); S.ratings[q] += 1;
  if (q === 1 && !S.again[card.id]) { S.again[card.id] = 1; S.queue.push(card); }
  next();
}
function next() {
  var S = session; S.i += 1; S.revealed = false; S.picked = null; S.typed = '';
  render(true);
}

// ---- mock viva ----
var mock = null, mockTimer = null;
var MOCK_PASS = 0.8, ESCALATE = 0.75, STRUGGLE_PENALTY = 0.15;
function mockCards() { return D.cards.filter(function (c) { return c.type === 'mock'; }); }
function stopTimer() { if (mockTimer) { clearInterval(mockTimer); mockTimer = null; } }
function limitFor(card) { return card.level >= 4 ? 120 : 90; }
function splitFollow(text) {
  var m = /^(.*?)\s+\((.*)\)\s*$/.exec(text || '');
  return m ? { q: m[1], hint: m[2] } : { q: text, hint: '' };
}
function startMock() {
  mock = { qs: mockCards(), i: 0, phase: 'answer', answers: [], ticks: [], scores: [], follow: [], typed: '', deadline: 0, saved: false };
  mock.deadline = Date.now() + limitFor(mock.qs[0]) * 1000;
}
screens.mock = function (parts, params) {
  if (params.run) { if (!mock) startMock(); return mockRun(); }
  return mockHome();
};
function mockHome() {
  var hist = P.mock.slice().reverse(), passedN = P.mock.filter(function (m) { return m.passed; }).length;
  return h('div', {},
    h('h1', { text: 'Mock viva' }),
    h('p', { class: 'lede', text: 'Five hostile committee questions on whether PatchTST generalises. Answer in writing within 90 seconds (120 for the last), then check your answer against the rubric. A strong answer draws a follow-up. You pass at 80%.' }),
    h('p', { class: 'muted', text: passedN + ' of 2 required passes so far. Each answer also updates the spaced-repetition schedule of its card.' }),
    h('div', { class: 'row' }, h('a', { class: 'btn primary', href: '#/mock?run=' + Date.now(), onclick: function () { mock = null; }, text: 'Start mock viva (5 questions)' })),
    hist.length ? h('div', {}, h('h2', { text: 'Attempts' }),
      h('div', { class: 'tw' }, h('table', {}, h('thead', {}, h('tr', {}, h('th', { text: 'When' }), h('th', { text: 'Score' }), h('th', { text: 'Result' }), h('th', { text: 'Per question' }))),
        h('tbody', {}, hist.map(function (m) {
          return h('tr', {}, h('td', { text: new Date(m.t).toLocaleString() }), h('td', { text: Math.round(m.total * 100) + '%' }), h('td', {}, chip(m.passed ? 'passed' : 'not yet', m.passed ? 'ok' : 'open')), h('td', { text: m.scores.map(function (x) { return Math.round(x * 100) + '%'; }).join(' \u00b7 ') }));
        }))))) : h('p', { class: 'muted', text: 'No attempts yet.' }));
}
function mockRun() {
  var M = mock, wrap = h('div', {});
  if (M.i >= M.qs.length) { finishMock(); return mockResult(); }
  var card = M.qs[M.i];
  wrap.appendChild(h('div', { class: 'study-head' }, h('span', { text: 'Mock viva' }), h('a', { href: '#/mock', text: 'quit' }), h('span', { text: 'Question ' + (M.i + 1) + ' of ' + M.qs.length })));
  wrap.appendChild(cardHead(card));
  wrap.appendChild(h('p', { class: 'prompt', text: card.prompt }));
  if (M.phase === 'answer') {
    wrap.appendChild(h('p', { class: 'chip sig', role: 'timer', id: 'timer', text: '' }));
    wrap.appendChild(h('textarea', { id: 'mans', placeholder: 'Type your answer as you would say it to the committee', 'aria-label': 'Your answer' }));
    wrap.appendChild(h('div', { class: 'row', style: 'margin-top:10px' }, h('button', { type: 'button', class: 'btn primary', text: 'Submit answer (Ctrl+Enter)', onclick: submitAnswer })));
  } else if (M.phase === 'grade') {
    wrap.appendChild(h('div', { class: 'note' }, h('p', {}, h('strong', { text: 'Your answer: ' }), M.answers[M.i] || '(no answer)')));
    wrap.appendChild(answerBlock(card, { noRubric: true, noFollow: true }));
    wrap.appendChild(h('h3', { text: 'Self-grade: tick each point your answer made' }));
    var ticks = M.ticks[M.i] = M.ticks[M.i] || [];
    wrap.appendChild(h('div', {}, card.rubric.map(function (r, k) {
      var id = 'rb-' + k, cb = h('input', { type: 'checkbox', id: id, checked: !!ticks[k], onchange: function () { ticks[k] = cb.checked; } });
      return h('div', { class: 'row' }, cb, h('label', { for: id, text: r }));
    })));
    wrap.appendChild(h('div', { class: 'row', style: 'margin-top:12px' }, h('button', { type: 'button', class: 'btn primary', text: 'Score this answer', onclick: scoreAnswer })));
  } else if (M.phase === 'follow') {
    var f = splitFollow(card.followUp);
    wrap.appendChild(h('div', { class: 'note' }, h('p', {}, h('strong', { text: 'The committee follows up: ' }), f.q)));
    wrap.appendChild(h('textarea', { id: 'fans', 'aria-label': 'Your reply to the follow-up', placeholder: 'Your reply (optional)' }));
    if (f.hint) wrap.appendChild(h('details', {}, h('summary', { text: 'Show suggested answer' }), h('div', { class: 'body' }, h('p', { text: f.hint }))));
    wrap.appendChild(h('div', { class: 'row', style: 'margin-top:10px' },
      h('button', { type: 'button', class: 'btn primary', text: 'I handled it', onclick: function () { endQuestion(false); } }),
      h('button', { type: 'button', class: 'btn', text: 'I struggled (\u221215%)', onclick: function () { endQuestion(true); } })));
  }
  return wrap;
}
function tickFraction(i) {
  var card = mock.qs[i], t = mock.ticks[i] || [], n = 0;
  card.rubric.forEach(function (r, k) { if (t[k]) n++; });
  return card.rubric.length ? n / card.rubric.length : 0;
}
function submitAnswer() {
  var ta = document.getElementById('mans');
  if (mock.phase !== 'answer') return;
  mock.answers[mock.i] = ta ? ta.value.trim() : (mock.answers[mock.i] || '');
  mock.phase = 'grade'; stopTimer(); render(true);
}
function scoreAnswer() {
  var card = mock.qs[mock.i], fr = tickFraction(mock.i);
  mock.scores[mock.i] = fr;
  if (fr >= ESCALATE && card.followUp) { mock.phase = 'follow'; render(true); } else endQuestion(null);
}
function endQuestion(struggled) {
  var i = mock.i, card = mock.qs[i], fr = mock.scores[i];
  var fa = document.getElementById('fans'); mock.follow[i] = { asked: struggled !== null, struggled: !!struggled, reply: fa ? fa.value.trim() : '' };
  if (struggled) fr = Math.max(0, fr - STRUGGLE_PENALTY);
  mock.scores[i] = fr;
  rate(card, fr >= 0.95 ? 4 : fr >= MOCK_PASS ? 3 : fr >= 0.5 ? 2 : 1, mock.answers[i]);
  mock.i += 1; mock.phase = 'answer';
  if (mock.i < mock.qs.length) mock.deadline = Date.now() + limitFor(mock.qs[mock.i]) * 1000;
  render(true);
}
function finishMock() {
  var M = mock; if (M.saved) return;
  var total = M.scores.reduce(function (a, b) { return a + b; }, 0) / M.qs.length;
  P.mock.push({ t: Date.now(), total: total, passed: total >= MOCK_PASS, scores: M.scores.slice(), asked: M.follow.map(function (f) { return !!(f && f.asked); }) });
  save(); M.saved = true; M.total = total;
}
function mockResult() {
  var M = mock, total = M.total, ok = total >= MOCK_PASS;
  return h('div', {},
    h('h1', { text: Math.round(total * 100) + '% \u2014 ' + (ok ? 'passed' : 'not yet') }),
    h('p', { class: 'muted', text: ok ? 'You cleared the 80% bar. Two passes complete the mock-viva part of the definition of done.' : 'The bar is 80%. Review the missed points below and try again.' }),
    h('div', { class: 'tw' }, h('table', {}, h('thead', {}, h('tr', {}, h('th', { text: 'Question' }), h('th', { text: 'Score' }), h('th', { text: 'Missed points' }))),
      h('tbody', {}, M.qs.map(function (c, i) {
        var t = M.ticks[i] || [], missed = c.rubric.filter(function (r, k) { return !t[k]; });
        return h('tr', {}, h('td', {}, h('a', { href: '#/concept/' + c.conceptId, text: c.prompt.slice(0, 90) + (c.prompt.length > 90 ? '\u2026' : '') }), M.follow[i] && M.follow[i].asked ? h('div', { class: 'muted', text: M.follow[i].struggled ? 'follow-up: struggled' : 'follow-up: handled' }) : null),
          h('td', { text: Math.round(M.scores[i] * 100) + '%' }), h('td', { text: missed.length ? missed.join('; ') : 'none' }));
      })))),
    h('div', { class: 'row', style: 'margin-top:14px' }, h('a', { class: 'btn primary', href: '#/mock?run=' + Date.now(), onclick: function () { mock = null; }, text: 'Try again' }), h('a', { class: 'btn', href: '#/', text: 'Home (see readiness)' }), h('a', { class: 'btn', href: '#/mock', text: 'All attempts' })));
}
function mockAfterRender() {
  if (!mock || mock.phase !== 'answer' || mock.i >= mock.qs.length) return;
  var el = document.getElementById('timer'); if (!el) return;
  stopTimer();
  var tick = function () {
    var left = Math.max(0, Math.ceil((mock.deadline - Date.now()) / 1000));
    el.textContent = 'Time left: ' + Math.floor(left / 60) + ':' + ('0' + (left % 60)).slice(-2);
    if (left <= 0) { stopTimer(); submitAnswer(); }
  };
  tick(); mockTimer = setInterval(tick, 500);
}

// ---- derivation lab ----
var labState = {}, prac = null;
var DSET = { WTH: 'Table 4.1', ETTh1: 'Table 4.2', STEEL: 'Table 4.3', 'Smart Meters': 'Table 4.4' };
function parseNum(str) {
  var t = String(str == null ? '' : str).replace(/[\u2212\u2013]/g, '-').replace(/[,\s]/g, '').replace(/(%|x|\u00d7|days?|s)$/i, '');
  return t === '' ? NaN : Number(t);
}
function fieldOK(chk, val) {
  var n = parseNum(val);
  if (isNaN(n)) return false;
  return [chk.answer].concat(chk.alts || []).some(function (a) { return Math.abs(n - a) <= chk.tol + 1e-9; });
}
function fmt(x) { return (Math.round(x * 1000) / 1000).toLocaleString('en-US', { maximumFractionDigits: 3 }); }
function showExpr(e) { return e.replace(/Math\./g, ''); }
function fieldsBlock(checks, prefix) {
  var inputs = [], marks = [], node = h('div', {});
  checks.forEach(function (c, k) {
    var inp = h('input', { type: 'text', inputmode: 'decimal', autocomplete: 'off', id: prefix + '-' + k, 'aria-label': c.label });
    var mk = h('span', { class: 'mk' });
    inputs.push(inp); marks.push(mk);
    node.appendChild(h('div', { class: 'field' }, h('label', { for: prefix + '-' + k, text: c.label + (c.unit ? ' (' + c.unit + ')' : '') }), h('span', { class: 'row' }, inp, mk)));
  });
  return {
    node: node,
    read: function () { return inputs.map(function (i) { return i.value; }); },
    mark: function (oks) { oks.forEach(function (ok, k) { marks[k].textContent = ok ? '\u2713' : '\u2717'; marks[k].className = 'mk ' + (ok ? 'okmk' : 'badmk'); inputs[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); }); },
    reveal: function () { checks.forEach(function (c, k) { marks[k].textContent = '= ' + fmt(c.answer) + (c.unit ? ' ' + c.unit : ''); marks[k].className = 'mk revmk'; }); }
  };
}
function workingList(checks) {
  return h('ul', { class: 'plain' }, checks.map(function (c) { return h('li', { text: c.label + ': ' + (c.expr ? showExpr(c.expr) + ' = ' : '') + fmt(c.answer) + (c.unit ? ' ' + c.unit : '') }); }));
}
function exerciseBody(item) {
  var card = kmap[item.cardId], st = labState[item.id] || (labState[item.id] = { checks: 0, revealed: false, rated: false });
  var fb = fieldsBlock(item.checks, 'lab-' + item.id), msg = h('p', { role: 'status', class: 'muted' }), after = h('div', {});
  function finish() {
    clear(after);
    after.appendChild(h('h3', { text: 'Working' })); after.appendChild(workingList(item.checks));
    after.appendChild(answerBlock(card, { noRubric: true, noFollow: true }));
    var chipEl = document.getElementById('chip-' + item.id);
    if (chipEl) { var sc = statusChip(P.cards[card.id]); chipEl.textContent = sc[0]; chipEl.className = 'chip ' + sc[1]; }
  }
  function check() {
    var vals = fb.read(), oks = item.checks.map(function (c, k) { return fieldOK(c, vals[k]); });
    fb.mark(oks); st.checks += 1;
    var n = oks.filter(Boolean).length;
    if (n === oks.length) {
      msg.textContent = 'All correct.';
      if (!st.rated) { rate(card, st.checks === 1 && !st.revealed ? 3 : 2); st.rated = true; }
      finish();
    } else msg.textContent = n + ' of ' + oks.length + ' correct. Fix the marked fields, or show the answers.';
  }
  function reveal() {
    st.revealed = true; fb.reveal();
    if (!st.rated) { rate(card, 1); st.rated = true; }
    msg.textContent = 'Answers shown, so this counts as Again in your schedule. Come back and solve it from scratch.';
    finish();
  }
  return h('div', { class: 'body' }, h('p', { text: item.setup }),
    h('form', { onsubmit: function (e) { e.preventDefault(); check(); } }, fb.node,
      h('div', { class: 'row', style: 'margin-top:10px' }, h('button', { type: 'submit', class: 'btn primary', text: 'Check' }), h('button', { type: 'button', class: 'btn', text: 'Show answers', onclick: reveal })), msg),
    after);
}
function statusChip(s) { return !s ? ['', ''] : s.last >= 3 ? ['passed', 'ok'] : s.last === 2 ? ['hard', 'medium'] : ['again', 'open']; }
function tolFor(x) { return Math.max(0.02, Math.abs(x) * 0.01); }
function rnd(a) { return a[Math.floor(Math.random() * a.length)]; }
function newProblem(kind) {
  var kinds = ['patch', 'ratio', 'gain', 'split'], k = kind && kind !== 'all' ? kind : rnd(kinds), T = D.lab.tables, names = Object.keys(T);
  if (k === 'patch') {
    var L = rnd([96, 168, 192, 336, 512, 720]), Pp = rnd([8, 12, 16, 24]), S = rnd([Pp, Pp / 2, Pp / 4]), N = Math.floor((L - Pp) / S) + 1, f = (L * L) / (N * N);
    return { kind: k, text: 'A PatchTST model has lookback L = ' + L + ', patch length P = ' + Pp + ' and stride S = ' + S + ' (no padding).', checks: [
      { label: 'Number of patches N', answer: N, tol: 0, unit: '', expr: 'floor((' + L + ' - ' + Pp + ') / ' + S + ') + 1' },
      { label: 'Attention pairs over patches (N squared)', answer: N * N, tol: 0, unit: '', expr: N + '^2' },
      { label: 'Shrink factor versus attention over L points', answer: f, tol: Math.max(0.6, f * 0.01), unit: 'x', expr: L + '^2 / ' + N + '^2' }] };
  }
  if (k === 'split') {
    var Tt = rnd([17396, 35064, 35040, 17420]);
    return { kind: k, text: 'A dataset has ' + Tt.toLocaleString('en-US') + ' windows, split chronologically 70 / 20 / 10.', checks: [
      { label: 'Training windows', answer: 0.7 * Tt, tol: 0.5, unit: '', expr: '0.7 * ' + Tt }, { label: 'Validation windows', answer: 0.2 * Tt, tol: 0.5, unit: '', expr: '0.2 * ' + Tt }, { label: 'Test windows', answer: 0.1 * Tt, tol: 0.5, unit: '', expr: '0.1 * ' + Tt }] };
  }
  var ds = rnd(names.filter(function (n) { return Object.keys(T[n]).length >= 2; })), ms = Object.keys(T[ds]);
  if (k === 'ratio') {
    var a = rnd(ms), b = rnd(ms.filter(function (m) { return m !== a; })), met = rnd(['params', 'time']), q = T[ds][a][met] / T[ds][b][met];
    return { kind: k, text: 'On ' + ds + ' (' + DSET[ds] + '), ' + a + ' has ' + fmt(T[ds][a][met]) + (met === 'time' ? ' s of training time' : ' parameters') + ' and ' + b + ' has ' + fmt(T[ds][b][met]) + '.', checks: [
      { label: 'How many times larger is ' + a + ' than ' + b + '?', answer: q, tol: tolFor(q), unit: 'x', expr: fmt(T[ds][a][met]) + ' / ' + fmt(T[ds][b][met]) }] };
  }
  var others = ms.filter(function (m) { return m !== 'PatchTST'; }), dsg = names.filter(function (n) { return T[n].PatchTST && Object.keys(T[n]).length >= 2; });
  ds = rnd(dsg); others = Object.keys(T[ds]).filter(function (m) { return m !== 'PatchTST'; });
  var o = rnd(others), m2 = rnd(['MAE', 'MSE', 'RMSE']), base = T[ds][o][m2], pt = T[ds].PatchTST[m2], g = (base - pt) / base * 100;
  return { kind: 'gain', text: 'On ' + ds + ' (' + DSET[ds] + '), ' + o + ' has ' + m2 + ' ' + base + ' and PatchTST has ' + pt + '.', checks: [
    { label: 'PatchTST improvement over ' + o + ' on ' + m2 + ' (negative if worse)', answer: g, tol: 0.15, unit: '%', expr: '(' + base + ' - ' + pt + ') / ' + base + ' * 100' }] };
}
function practiceView(kind) {
  if (!prac || prac.kind0 !== kind) { prac = newProblem(kind); prac.kind0 = kind; prac.attempts = 0; }
  var box = h('div', {});
  (function build() {
    clear(box);
    var pr = prac, fb = fieldsBlock(pr.checks, 'prac'), msg = h('p', { role: 'status', class: 'muted' }), after = h('div', {});
    function done(first) { if (!pr.counted) { pr.counted = true; P.lab.done += 1; if (first) P.lab.correct += 1; save(); stats.textContent = statsText(); } }
    function check() {
      var vals = fb.read(), oks = pr.checks.map(function (c, k) { return fieldOK(c, vals[k]); });
      fb.mark(oks); pr.attempts += 1;
      if (oks.every(Boolean)) { msg.textContent = 'Correct.'; done(pr.attempts === 1 && !pr.revealed); clear(after); after.appendChild(workingList(pr.checks)); }
      else msg.textContent = oks.filter(Boolean).length + ' of ' + oks.length + ' correct. Try again or show the working.';
    }
    function reveal() { pr.revealed = true; fb.reveal(); done(false); msg.textContent = 'Working shown.'; clear(after); after.appendChild(workingList(pr.checks)); }
    var stats = h('p', { class: 'muted', text: statsText() });
    box.appendChild(stats);
    box.appendChild(h('div', { class: 'card' }, h('p', { text: pr.text }),
      h('form', { onsubmit: function (e) { e.preventDefault(); check(); } }, fb.node,
        h('div', { class: 'row', style: 'margin-top:10px' }, h('button', { type: 'submit', class: 'btn primary', text: 'Check' }), h('button', { type: 'button', class: 'btn', text: 'Show working', onclick: reveal }),
          h('button', { type: 'button', class: 'btn', text: 'New problem', onclick: function () { prac = newProblem(kind); prac.kind0 = kind; prac.attempts = 0; build(); } })), msg), after));
  })();
  return box;
}
function statsText() { return 'Practice: ' + P.lab.correct + ' correct first try out of ' + P.lab.done + ' problems finished.'; }
screens.lab = function (parts, params) {
  var tab = params.tab === 'practice' ? 'practice' : 'thesis';
  var solved = D.lab.items.filter(function (it) { return passed(kmap[it.cardId]); }).length;
  var view = h('div', {},
    h('h1', { text: 'Derivation lab' }),
    h('p', { class: 'lede', text: 'Type the numbers. The thesis derivations check your arithmetic against the thesis tables; the practice generator makes fresh problems from the same tables. Round as you like: each answer has a stated tolerance.' }),
    h('div', { class: 'row' }, h('a', { class: 'chip' + (tab === 'thesis' ? ' sig' : ''), href: '#/lab', text: 'Thesis derivations' }), h('a', { class: 'chip' + (tab === 'practice' ? ' sig' : ''), href: '#/lab?tab=practice', text: 'Practice generator' })));
  if (tab === 'thesis') {
    view.appendChild(h('p', { class: 'muted', text: solved + ' of ' + D.lab.items.length + ' derivations passed. Solving one first try counts as Good; needing retries counts as Hard; showing the answers counts as Again.' }));
    D.lab.items.forEach(function (it) {
      var s = P.cards[it.cardId], sc = statusChip(s);
      view.appendChild(h('details', {}, h('summary', {}, it.title, ' ', s ? h('span', { id: 'chip-' + it.id, class: 'chip ' + sc[1], text: sc[0] }) : h('span', { id: 'chip-' + it.id })), exerciseBody(it)));
    });
  } else {
    var kind = ['patch', 'ratio', 'gain', 'split'].indexOf(params.kind) >= 0 ? params.kind : 'all';
    view.appendChild(h('div', { class: 'row', style: 'margin-top:10px' }, [['all', 'Mixed'], ['patch', 'Patches'], ['ratio', 'Ratios'], ['gain', 'Improvement %'], ['split', 'Splits']].map(function (x) {
      return h('a', { class: 'chip' + (kind === x[0] ? ' sig' : ''), href: '#/lab?tab=practice&kind=' + x[0], text: x[1] });
    })));
    view.appendChild(practiceView(kind));
  }
  return view;
};

// ---- register ----
screens.register = function () {
  var order = { open: 0, decided: 1, fixed: 2 }, sev = { high: 0, medium: 1, low: 2 };
  var items = D.register.slice().sort(function (a, b) { return order[a.status] - order[b.status] || sev[a.severity] - sev[b.severity]; });
  var openCount = items.filter(function (r) { return r.status === 'open' && !(P.register[r.id] || {}).rehearsed; }).length;
  return h('div', {},
    h('h1', { text: 'Vulnerability register' }),
    h('p', { class: 'lede', text: 'Places where the thesis disagrees with itself, with its own tables or with your code. Open items need a rehearsed answer; “decided” items need a text fix; “fixed” items are recorded for reference.' }),
    h('p', { class: 'muted', text: openCount + ' open items without a rehearsed answer.' }),
    items.map(function (r) {
      var st = P.register[r.id] || {};
      var box = h('input', { type: 'checkbox', id: 'rh-' + r.id, checked: !!st.rehearsed, onchange: function () { P.register[r.id] = Object.assign({}, P.register[r.id], { rehearsed: box.checked }); save(); } });
      var ta = h('textarea', { 'aria-label': 'Rehearsed answer for ' + r.title, placeholder: 'Your rehearsed answer', onchange: function () { P.register[r.id] = Object.assign({}, P.register[r.id], { answer: ta.value }); save(); } });
      ta.value = st.answer || '';
      var dec = r.decisionId && DECISIONS[r.decisionId];
      return h('details', { open: r.status === 'open' && r.severity === 'high' },
        h('summary', {}, chip(r.severity, r.severity), ' ', chip(r.status, r.status), ' ', r.title),
        h('div', { class: 'body' },
          h('h3', { text: 'What the sources say' }), h('ul', { class: 'plain' }, r.conflict.map(function (x) { return h('li', { text: x }); })),
          r.evidence.map(function (e) { return h('blockquote', {}, '“' + e + '”'); }),
          r.thesisAnchors.map(function (a) { return sectionBlock(a, r.evidence[0]); }),
          h('h3', { text: 'Resolution' }), h('p', { text: r.resolution }),
          dec ? h('p', { class: 'muted' }, 'Author decision ', chip(dec.id, dec.status === 'decided' ? 'ok' : 'open'), ' — ', dec.topic, dec.thesisFix ? '. Thesis fix: ' + dec.thesisFix : '') : null,
          h('div', { class: 'row' }, box, h('label', { for: 'rh-' + r.id, text: 'I have rehearsed an answer' })), ta));
    }));
};

// ---- sources ----
screens.sources = function () {
  var missing = (DECISIONS['D-sources'] || {}).missingPdfs || [];
  return h('div', {},
    h('h1', { text: 'Source shelf' }),
    h('p', { class: 'lede', text: D.sources.length + ' PDFs from the thesis reference list are in sources/. Entries marked verify are external works whose citation you should confirm against the original.' }),
    missing.length ? h('div', { class: 'note warn' }, h('p', {}, h('strong', { text: 'PDF still missing: ' }), missing.map(function (m) { return m.cite; }).join('; '), '. Add the file to sources/.')) : null,
    h('div', { class: 'tw' }, h('table', {},
      h('thead', {}, h('tr', {}, h('th', { text: 'Source' }), h('th', { text: 'Why it is here' }), h('th', { text: 'Status' }), h('th', { text: 'Locators' }))),
      h('tbody', {}, D.sources.map(function (s) {
        return h('tr', {},
          h('td', {}, s.cite, s.thesisRef ? h('div', { class: 'muted', text: 'thesis ref ' + s.thesisRef }) : null),
          h('td', { text: s.why }), h('td', {}, chip(s.status, s.status === 'verify' ? 'verify' : s.status === 'thesis-original' ? 'sig' : '')),
          h('td', {}, s.locators.filter(function (l) { return s.id !== 'thesis' || !/^§/.test(l.label); }).map(function (l) { return h('div', {}, h('a', { href: s.file + '#page=' + l.page, target: '_blank', rel: 'noopener', text: l.label + ' (p.' + l.page + ')' })); })));
      })))));
};

// ---------- router ----------
function parseHash() {
  var raw = location.hash.replace(/^#\/?/, ''), q = raw.split('?'), parts = q[0].split('/'), params = {};
  (q[1] || '').split('&').forEach(function (kv) { if (kv) { var p = kv.split('='); params[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); } });
  return { parts: parts, params: params };
}
function render(keepScroll) {
  var r = parseHash(), name = r.parts[0] || 'home';
  var fn = screens[name] || screens.home;
  if (name !== 'study') session = null;
  if (name !== 'mock' || !r.params.run) { stopTimer(); if (name !== 'mock') mock = null; }
  clear(app);
  app.appendChild(fn(r.parts, r.params));
  document.querySelectorAll('.top nav a').forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-nav') === (name === 'concept' ? 'atlas' : name)); });
  document.title = 'Lookback' + (name === 'home' ? '' : ' · ' + name);
  if (!keepScroll) window.scrollTo(0, 0);
  if (name === 'mock') mockAfterRender();
  var f = document.getElementById(session && session.revealed ? 'nextbtn' : 'ans');
  if (f && name === 'study' && !session.revealed) { /* keep focus off the textarea so space reveals; user can click in */ }
}
window.addEventListener('hashchange', function () { render(); });

// ---------- keyboard ----------
document.addEventListener('keydown', function (e) {
  if (e.altKey || e.metaKey) return;
  var tag = (e.target.tagName || '').toLowerCase(), typing = tag === 'textarea' || tag === 'input';
  if (mock && parseHash().parts[0] === 'mock') {
    if (typing && e.key === 'Enter' && (e.ctrlKey || e.metaKey) && mock.phase === 'answer') { e.preventDefault(); submitAnswer(); }
    return;
  }
  if (!session || parseHash().parts[0] !== 'study' || session.i >= session.queue.length) return;
  var S = session, card = S.queue[S.i], mcq = card.options && S.mode === 'relaxed';
  if (typing) { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && !S.revealed && !mcq) { e.preventDefault(); reveal(); } return; }
  if (tag === 'button' && e.key === ' ') return;
  if (mcq) {
    if (!S.revealed && /^[1-4]$/.test(e.key) && card.options[+e.key - 1]) { e.preventDefault(); pickOption(card.options[+e.key - 1]); }
    else if (S.revealed && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); next(); }
    return;
  }
  if (!S.revealed && e.key === ' ') { e.preventDefault(); reveal(); }
  else if (S.revealed && /^[1-4]$/.test(e.key)) { e.preventDefault(); doRate(+e.key); }
});

// ---------- theme ----------
var root = document.documentElement;
try { var t = localStorage.getItem('lookback-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) { /* ignore */ }
document.getElementById('themebtn').addEventListener('click', function () {
  var cur = root.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  var nx = cur === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', nx);
  try { localStorage.setItem('lookback-theme', nx); } catch (e) { /* ignore */ }
});

window.Lookback = { practice: function () { return prac; }, parseNum: parseNum, fieldOK: fieldOK, labState: function () { return labState; }, readiness: readiness, mockState: function () { return mock; }, rate: rate, schedule: schedule, buildQueue: buildQueue, conceptLevel: conceptLevel, progress: function () { return P; }, render: render };
render();
})();
