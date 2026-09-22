import fs from 'node:fs';
const load = n => JSON.parse(fs.readFileSync(`src/data/${n}.json`, 'utf8'));
const errors = [];
function check(ok, msg) { if (!ok) errors.push(msg); }
function text(v) { return typeof v === 'string' && v.trim().length > 0; }
function bilingual(v) { return v && (text(v.en) || text(v.ko)); }
function urls(value, path = '') {
  if (!value || typeof value !== 'object') return;
  for (const [k, v] of Object.entries(value)) {
    const name = `${path}.${k}`;
    if (['link','pdf','photo','image','scholar','orcid','github','linkedin'].includes(k) && v) {
      const local = ['photo','image','pdf'].includes(k) && /^\/(?!\/)/.test(v) && !v.includes('..') && !v.includes('\\');
      check(typeof v === 'string' && (/^https?:\/\//i.test(v) || local), `Invalid URL: ${name}`);
      if (local) check(fs.existsSync(`public${v}`), `Missing uploaded file: ${v}`);
    }
    if (k === 'images' && Array.isArray(v)) {
      v.forEach((item, i) => {
        if (typeof item !== 'string' || !item) return;
        const local = /^\/(?!\/)/.test(item) && !item.includes('..') && !item.includes('\\');
        check(/^https?:\/\//i.test(item) || local, `Invalid URL: ${name}[${i}]`);
        if (local) check(fs.existsSync(`public${item}`), `Missing uploaded file: ${item}`);
      });
    }
    urls(v, name);
  }
}
for (const name of ['news','members','research','publications','collaborators','carousel']) {
  const rows = load(name); check(Array.isArray(rows), `${name}: expected list`);
  if (!Array.isArray(rows)) continue;
  const ids = new Set();
  for (const [i, row] of rows.entries()) {
    const at = `${name}[${i + 1}]`;
    if (row.id) { check(/^[a-z0-9][a-z0-9-]*$/.test(row.id), `${at}: invalid ID`); check(!ids.has(row.id), `${at}: duplicate ID`); ids.add(row.id); }
    if (name === 'news') { check(/^\d{4}-\d{2}-\d{2}$/.test(row.date) && !Number.isNaN(Date.parse(row.date)) && new Date(row.date).toISOString().slice(0,10) === row.date, `${at}: invalid date`); check(bilingual(row.text), `${at}: missing text`); check(['grant','honor','talk','paper','news'].includes(row.type), `${at}: invalid type`); }
    if (name === 'members') { check(bilingual(row.name), `${at}: missing name`); check(['pi','postdoc','phd','ms','undergrad','intern','alumni'].includes(row.role), `${at}: invalid role`); }
    if (name === 'research') { check(bilingual(row.title) && bilingual(row.summary), `${at}: missing title/summary`); check(['platform','method'].includes(row.track), `${at}: invalid track`); }
    if (name === 'collaborators') { check(bilingual(row.institution), `${at}: missing institution`); }
    if (name === 'carousel') { check(text(row.image), `${at}: missing image`); }
    if (name === 'publications') { check(text(row.title) && text(row.authors), `${at}: missing title/authors`); check(Number.isInteger(row.year) && row.year > 1900 && row.year < 2200, `${at}: invalid year`); if (row.authorRole) check(['first','corresponding'].includes(row.authorRole), `${at}: invalid authorRole`); }
  }
  urls(rows, name);
}
const lab = load('lab'); check(bilingual(lab.name) && bilingual(lab.hero?.headline), 'Lab: missing name/headline'); urls(lab, 'lab');
const join = load('join'); check(Array.isArray(join.positions), 'Join: positions must be a list'); urls(join, 'join');
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log('Content validation passed.');
