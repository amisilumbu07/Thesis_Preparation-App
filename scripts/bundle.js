#!/usr/bin/env node
// Bundles content/*.json and thesis/sections.json into content/data.js so index.html
// works when opened directly from disk (fetch() is blocked on file://).
// Run after any content change:  node scripts/bundle.js
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const read = (p) => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));

function build() {
  const data = {
    concepts: read('content/concepts.json'),
    cards: read('content/cards.json'),
    sources: read('content/sources.json'),
    register: read('content/register.json'),
    decisions: read('content/decisions.json'),
    lab: read('content/lab.json'),
    sections: read('thesis/sections.json'),
  };
  return 'window.LOOKBACK = ' + JSON.stringify(data) + ';\n';
}

module.exports = { build };

if (require.main === module) {
  const out = build();
  fs.writeFileSync(path.join(root, 'content/data.js'), out);
  console.log(`content/data.js written (${(out.length / 1024).toFixed(0)} KB)`);
}
