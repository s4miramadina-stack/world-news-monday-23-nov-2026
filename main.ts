// Monday 23 November 2026, one page: puts the pre-rendered entry.png into the
// judge's output folder. draw.py makes the picture; this file only delivers it.
// Node 22 standard library, no network, so two runs give byte-identical output.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const target = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

let png: Buffer;
try {
  png = readFileSync(resolve(here, 'entry.png'));
} catch {
  console.error('no entry.png beside main.ts; render it with `python3 draw.py`');
  process.exit(1);
}

mkdirSync(target, { recursive: true });
const dest = resolve(target, 'entry.png');
writeFileSync(dest, png);
console.log(`entry.png -> ${dest} (${png.length} bytes)`);
