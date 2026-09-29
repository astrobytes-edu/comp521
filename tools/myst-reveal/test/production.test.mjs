import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { exportProject } from '../src/build.mjs';

const root = new URL('../', import.meta.url).pathname;
const project = path.join(root, 'migrations/comp536');

test('selected SWE export excludes the other decks and source pages; stale outputs fail closed', () => {
  const output = fs.mkdtempSync(path.join(root, '_build/production-test-'));
  try {
    const manifest = exportProject(project, output, 'software-engineering');
    assert.deepEqual(manifest.decks.map(deck => deck.file), ['software-engineering.html']);
    assert.deepEqual(manifest.sources, []);
    assert.deepEqual(fs.readdirSync(output).sort(), [
      'decks.json', 'provenance.json', 'software-engineering.handout.html', 'software-engineering.html',
    ]);
    const provenance = JSON.parse(fs.readFileSync(path.join(output, 'provenance.json')));
    assert.deepEqual(provenance.sources.map(source => source.source), ['software-engineering.md']);
    assert.deepEqual(provenance.kernels, []);
    const previous = fs.readFileSync(path.join(output, 'software-engineering.html'));
    fs.writeFileSync(path.join(output, 'ode-methods.html'), 'unrelated draft');
    assert.throws(() => exportProject(project, output, 'software-engineering'), /unrelated files/);
    assert.deepEqual(fs.readFileSync(path.join(output, 'software-engineering.html')), previous);
  } finally {
    fs.rmSync(output, { recursive: true, force: true });
  }
});
