#!/usr/bin/env node
/**
 * Render branded 1000x1500 Pinterest pin PNGs from an SVG template (sharp).
 *
 * Usage (from site/):
 *   node scripts/make-pin.mjs --title "5 Free AI Tools, Tested" \
 *     --items "Systeme.io|MailerLite|Notion|Canva|Grammarly" \
 *     --tag "solostack.pages.dev" --out ../ops/content/pins/pin-01.png
 *
 * Long title lines wrap automatically (~16 chars/line). Items render as a
 * checklist. Output meets Pinterest's 2:3 spec.
 */
import sharp from 'sharp';
import { parseArgs } from 'node:util';
import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const { values: args } = parseArgs({
  options: {
    title: { type: 'string' },
    items: { type: 'string', default: '' },
    tag: { type: 'string', default: '25012004.xyz' },
    out: { type: 'string', default: 'pin.png' },
  },
});
if (!args.title) {
  console.error('Required: --title "..."');
  process.exit(1);
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function wrap(text, max = 16) {
  const words = text.split(/\s+/);
  const lines = [];
  let line = '';
  for (const w of words) {
    if ((line + ' ' + w).trim().length > max && line) {
      lines.push(line);
      line = w;
    } else {
      line = (line + ' ' + w).trim();
    }
  }
  if (line) lines.push(line);
  return lines.slice(0, 5);
}

const titleLines = wrap(args.title);
const items = args.items ? args.items.split('|').slice(0, 6) : [];

const titleY = 240;
const titleSvg = titleLines
  .map((l, i) => `<text x="90" y="${titleY + i * 92}" font-family="Arial, sans-serif" font-size="76" font-weight="800" fill="#141428">${esc(l)}</text>`)
  .join('\n');

const itemsStartY = titleY + titleLines.length * 92 + 90;
const itemsSvg = items
  .map((item, i) => {
    const y = itemsStartY + i * 96;
    return `
    <rect x="90" y="${y - 52}" width="820" height="72" rx="14" fill="#ffffff" stroke="#dfe3f0"/>
    <circle cx="134" cy="${y - 16}" r="16" fill="#2563eb"/>
    <path d="M126 ${y - 16} l6 6 l10 -12" stroke="#ffffff" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="170" y="${y - 4}" font-family="Arial, sans-serif" font-size="40" font-weight="600" fill="#1a1a2e">${esc(item)}</text>`;
  })
  .join('\n');

const svg = `<svg width="1000" height="1500" viewBox="0 0 1000 1500" xmlns="http://www.w3.org/2000/svg">
  <rect width="1000" height="1500" fill="#f4f6fb"/>
  <rect x="0" y="0" width="1000" height="18" fill="#2563eb"/>
  <text x="90" y="140" font-family="Arial, sans-serif" font-size="34" font-weight="700" letter-spacing="6" fill="#2563eb">TESTED, NOT HYPED</text>
  ${titleSvg}
  ${itemsSvg}
  <rect x="90" y="1310" width="820" height="90" rx="45" fill="#141428"/>
  <text x="500" y="1368" text-anchor="middle" font-family="Arial, sans-serif" font-size="38" font-weight="700" fill="#ffffff">full breakdown on ${esc(args.tag)}</text>
</svg>`;

const out = resolve(args.out);
mkdirSync(dirname(out), { recursive: true });
await sharp(Buffer.from(svg)).png().toFile(out);
console.log(`wrote ${out} (1000x1500)`);
