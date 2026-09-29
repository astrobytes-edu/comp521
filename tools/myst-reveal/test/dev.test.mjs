import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const root = new URL('../', import.meta.url).pathname;
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

test('watch preview rebuilds after a source edit and injects live reload', { timeout: 60000 }, async () => {
  const project = path.join(root, '_build/watch-fixture');
  fs.mkdirSync(project, { recursive: true });
  fs.writeFileSync(path.join(project, 'myst.yml'), 'version: 1\nproject:\n  toc:\n    - file: index.md\nsite:\n  template: book-theme\n');
  fs.writeFileSync(path.join(project, 'index.md'), '---\ntitle: Watch fixture\n---\n\n## Initial title\n\nInitial content.\n');
  // Reuse the already downloaded template to keep this check local.
  fs.cpSync(path.join(root, 'examples/features/_build/templates'), path.join(project, '_build/templates'), { recursive: true });
  let log = '';
  const child = spawn(process.execPath, [path.join(root, 'src/dev.mjs'), project], { env: { ...process.env, PORT: '0' } });
  child.stdout.on('data', data => { log += data; }); child.stderr.on('data', data => { log += data; });
  let url;
  async function waitForContent(needle) {
    for (let i = 0; i < 150; i++) {
      url ||= log.match(/Preview: (http:\/\/\S+)/)?.[1];
      if (url) {
        const html = await fetch(url).then(r => r.text());
        if (html.includes(needle)) return html;
      }
      await pause(150);
    }
    throw new Error(`Preview did not show ${needle}: ${log}`);
  }
  try {
    const html = await waitForContent('Initial title');
    assert.ok(html.includes("new EventSource('/comp521/__events')"));
    fs.writeFileSync(path.join(project, 'index.md'), '---\ntitle: Watch fixture\n---\n\n## Revised title\n\nChanged content.\n');
    const changed = await waitForContent('Revised title');
    assert.ok(changed.includes('Changed content.'));
  } finally {
    child.kill('SIGTERM');
    await new Promise(resolve => child.once('close', resolve));
  }
});
