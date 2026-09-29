import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { previewServer } from './preview.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const project = path.resolve(process.argv[2] || path.join(root, 'examples/features'));
const port = Number(process.env.PORT || 4174);
const configFile = path.join(project, 'slides.json');
const config = fs.existsSync(configFile) ? JSON.parse(fs.readFileSync(configFile)) : {};
const multi = config.decks?.length;
const output = path.join(root, '_build/html/reveal', multi ? '' : `${path.basename(project)}.html`);
const previewFile = multi ? `${config.decks[0].name}.html` : path.basename(output);
const clients = new Set();
let building = false, pending = false, child, timer;
function build() {
  if (building) { pending = true; return; }
  building = true;
  child = spawn(process.execPath, [path.join(root, 'src/build.mjs'), project, output], { stdio: 'inherit' });
  child.on('error', error => { console.error(error); });
  child.on('close', status => {
    building = false;
    if (status === 0) for (const client of clients) client.write('data: reload\n\n');
    else console.error('Build failed; the preview still contains the last successful deck.');
    if (pending) { pending = false; build(); }
  });
}
const server = previewServer(path.join(root, '_build/html'), '/comp521', clients);
server.listen(port, '127.0.0.1', () => {
  console.log(`Watching ${project}\nPreview: http://127.0.0.1:${server.address().port}/comp521/reveal/${previewFile}`);
  build();
});
const watch = (dir, accept) => fs.watch(dir, { recursive: true }, (_event, filename) => {
  if (!filename || !accept(String(filename))) return;
  clearTimeout(timer); timer = setTimeout(build, 250);
});
const watchers = [
  watch(project, file => !file.split(path.sep).some(part => part.startsWith('.') || part === '_build' || part === 'node_modules')),
  watch(root, file => file.startsWith(`src${path.sep}`) || ['plugin.mjs', 'theme.css', 'handout.css', 'components.css', 'advanced.css'].includes(file)),
];
function close() { clearTimeout(timer); watchers.forEach(w => w.close()); child?.kill(); clients.forEach(c => c.end()); server.close(); }
process.once('SIGINT', close); process.once('SIGTERM', close);
