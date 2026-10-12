#!/usr/bin/env node
// Verifies content against the final thesis. Usage: node scripts/verify.js
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const root = path.join(__dirname, '..');
const norm = (t) => String(t).replace(/[​­]/g, '').replace(/\s+/g, ' ').trim();
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const exists = (p) => fs.existsSync(path.join(root, p));
const errors = [];
const fail = (msg) => errors.push(msg);

if (!exists('thesis/sections.json')) {
  console.error('FAIL: thesis/sections.json is missing (run scripts/build_sections.py)');
  process.exit(1);
}
const sections = readJSON('thesis/sections.json');
const sectionText = {};
for (const [n, s] of Object.entries(sections)) sectionText[n] = norm(s.text);

// facts.json: every sentence must appear in its section
let factCount = 0;
if (exists('thesis/facts.json')) {
  for (const f of readJSON('thesis/facts.json')) {
    factCount++;
    if (!sectionText[f.section]) fail(`facts ${f.id}: section ${f.section} not in sections.json`);
    else if (!sectionText[f.section].includes(norm(f.sentence))) fail(`facts ${f.id}: sentence not found in section ${f.section}`);
  }
}

const asList = (d) => (Array.isArray(d) ? d : d.items || d.cards || d.concepts || d.sources || d.entries || []);

// sources
const sources = {};
let sourceCount = 0;
function pageCount(file) {
  try {
    const out = execFileSync('pdfinfo', [path.join(root, file)], { encoding: 'utf8' });
    return Number(/Pages:\s+(\d+)/.exec(out)[1]);
  } catch (e) { return null; }
}
if (exists('content/sources.json')) {
  for (const s of asList(readJSON('content/sources.json'))) {
    sourceCount++;
    sources[s.id] = s;
    if (!s.file) { fail(`source ${s.id}: no file`); continue; }
    if (!exists(s.file)) { fail(`source ${s.id}: file missing (${s.file})`); continue; }
    if (!Array.isArray(s.locators) || s.locators.length === 0) { fail(`source ${s.id}: no page/table locator`); continue; }
    const pages = pageCount(s.file);
    for (const l of s.locators) {
      if (!l.label || !Number.isInteger(l.page)) fail(`source ${s.id}: bad locator ${JSON.stringify(l)}`);
      else if (pages && (l.page < 1 || l.page > pages)) fail(`source ${s.id}: locator "${l.label}" page ${l.page} outside 1-${pages}`);
    }
    if (s.status === 'verify' && !s.why) fail(`source ${s.id}: verify status without reason`);
  }
}

// concepts, cards, register
const conceptIds = new Set();
function checkEvidence(id, anchors, evidence) {
  const list = Array.isArray(evidence) ? evidence : [evidence];
  if (list.length === 0 || !list[0]) { fail(`${id}: missing evidence`); return; }
  for (const e of list) {
    const ev = norm(e);
    if (!anchors.some((a) => sectionText[a] && sectionText[a].includes(ev))) fail(`${id}: evidence not found verbatim in anchored sections: "${ev.slice(0, 60)}..."`);
  }
}
function checkAnchors(id, anchors) {
  if (!Array.isArray(anchors) || anchors.length === 0) { fail(`${id}: missing thesisAnchors`); return false; }
  let ok = true;
  for (const a of anchors) if (!sections[a]) { fail(`${id}: anchor ${a} not in sections.json`); ok = false; }
  return ok;
}
function checkSourceRef(id, sourceId, locator) {
  const s = sources[sourceId];
  if (!sourceId) { fail(`${id}: no source id`); return; }
  if (!s) { fail(`${id}: unknown source id ${sourceId}`); return; }
  if (!locator) fail(`${id}: no source locator`);
  else if (!s.locators.some((l) => l.label === locator)) fail(`${id}: locator "${locator}" not defined for source ${sourceId}`);
}

const counts = { concepts: 0, cards: 0, register: 0 };
if (exists('content/concepts.json')) {
  for (const c of asList(readJSON('content/concepts.json'))) {
    counts.concepts++;
    conceptIds.add(c.id);
    const id = `concepts:${c.id}`;
    if (checkAnchors(id, c.thesisAnchors)) checkEvidence(id, c.thesisAnchors, c.evidence);
    if (!Array.isArray(c.sourceIds) || !c.sourceIds.length) fail(`${id}: no sourceIds`);
    else for (const sid of c.sourceIds) if (!sources[sid]) fail(`${id}: unknown source id ${sid}`);
  }
}
const seen = new Set();
if (exists('content/cards.json')) {
  for (const k of asList(readJSON('content/cards.json'))) {
    counts.cards++;
    const id = `cards:${k.id}`;
    if (seen.has(k.id)) fail(`${id}: duplicate id`);
    seen.add(k.id);
    if (conceptIds.size && !conceptIds.has(k.conceptId)) fail(`${id}: unknown conceptId ${k.conceptId}`);
    if (!k.prompt || !k.answer) fail(`${id}: missing prompt or answer`);
    if (checkAnchors(id, k.thesisAnchors)) checkEvidence(id, k.thesisAnchors, k.evidence);
    checkSourceRef(id, k.sourceId, k.sourceLocator);
    if (k.options && (!Array.isArray(k.options) || !k.options.includes(k.correct))) fail(`${id}: correct answer not among options`);
  }
}
if (exists('content/register.json')) {
  for (const r of asList(readJSON('content/register.json'))) {
    counts.register++;
    const id = `register:${r.id}`;
    if (checkAnchors(id, r.thesisAnchors)) checkEvidence(id, r.thesisAnchors, r.evidence);
    if (!['open', 'fixed', 'decided'].includes(r.status)) fail(`${id}: bad status ${r.status}`);
  }
}

// decisions.json: every decision referenced by the register must exist
if (exists('content/decisions.json') && exists('content/register.json')) {
  const dec = new Set(readJSON('content/decisions.json').decisions.map((d) => d.id));
  for (const r of asList(readJSON('content/register.json'))) if (r.decisionId && !dec.has(r.decisionId)) fail(`register:${r.id}: unknown decisionId ${r.decisionId}`);
}

// lab.json: every derivation card has an exercise; every expected value recomputes from its stored expression
let labCount = 0;
if (exists('content/lab.json') && exists('content/cards.json')) {
  const lab = readJSON('content/lab.json');
  const byId = {};
  for (const k of asList(readJSON('content/cards.json'))) byId[k.id] = k;
  const covered = new Set();
  for (const it of lab.items) {
    labCount++;
    const id = `lab:${it.id}`;
    const card = byId[it.cardId];
    if (!card) { fail(`${id}: unknown cardId ${it.cardId}`); continue; }
    if (card.type !== 'derivation') fail(`${id}: card ${it.cardId} is not a derivation card`);
    covered.add(it.cardId);
    if (!it.checks || !it.checks.length) fail(`${id}: no checks`);
    for (const c of it.checks || []) {
      if (!c.label || typeof c.tol !== 'number' || c.tol < 0) { fail(`${id}: bad check ${JSON.stringify(c.label)}`); continue; }
      if (!/^[0-9+\-*/().,\s]*(?:Math\.(?:floor|pow|log10)[0-9+\-*/().,\s]*)*$/.test(c.expr)) { fail(`${id}: expression not allowed: ${c.expr}`); continue; }
      let v; try { v = Function('Math', `return (${c.expr});`)(Math); } catch (e) { fail(`${id}: expression fails: ${c.expr}`); continue; }
      if (!(Math.abs(v - c.answer) <= 1e-4 * Math.max(1, Math.abs(v)))) fail(`${id}: "${c.label}" stored ${c.answer} but expression gives ${v}`);
    }
  }
  for (const k of Object.values(byId)) if (k.type === 'derivation' && !covered.has(k.id)) fail(`lab: derivation card ${k.id} has no exercise`);
  if (!lab.tables || !Object.keys(lab.tables).length) fail('lab: no tables for the practice generator');
}

// content/data.js must match the JSON files (run node scripts/bundle.js)
if (exists('content/data.js')) {
  const fresh = require('./bundle.js').build();
  if (fs.readFileSync(path.join(root, 'content/data.js'), 'utf8') !== fresh) fail('content/data.js is stale: run node scripts/bundle.js');
} else fail('content/data.js is missing: run node scripts/bundle.js');

console.log(`sections: ${Object.keys(sections).length}, facts: ${factCount}, sources: ${sourceCount}, concepts: ${counts.concepts}, cards: ${counts.cards}, register: ${counts.register}, lab exercises: ${labCount}`);
if (errors.length) {
  console.error(`FAILED (${errors.length}):`);
  for (const e of errors.slice(0, 80)) console.error(' - ' + e);
  if (errors.length > 80) console.error(` ... and ${errors.length - 80} more`);
  process.exit(1);
}
console.log('OK');
