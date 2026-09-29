import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function previewServer(root, base = '/comp521', liveClients = null) {
  const directory = path.resolve(root);
  return http.createServer((request, response) => {
    let pathname;
    try { pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname); }
    catch { response.writeHead(400).end(); return; }
    if (liveClients && pathname === `${base}/__events`) {
      response.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
      response.write(': connected\n\n'); liveClients.add(response);
      request.on('close', () => liveClients.delete(response)); return;
    }
    if (pathname === `${base}/` || pathname === `${base}/lecture-prototype`) {
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      response.end(`<!doctype html><html lang="en"><meta charset="utf-8"><title>Lecture prototype</title>
        <main><h1>MyST Reveal prototype</h1><p>This local preview checks the course base path.</p>
        <a href="${base}/reveal/prototype.html">Open the six-slide prototype</a>
        <p><a href="${base}/reveal/features.html">Open the feature tour</a></p>
        <p><a href="${base}/reveal/computation.html">Computational science example</a></p>
        <p><a href="${base}/reveal/astronomy.html">Astronomy example</a></p><p><a href="${base}/reveal/advanced.html">Advanced presentation tools</a></p><p><a href="${base}/reveal/advanced-short.html">Short talk variant</a></p></main></html>`);
      return;
    }
    if (!pathname.startsWith(`${base}/`)) { response.writeHead(404).end(); return; }
    const file = path.resolve(directory, pathname.slice(base.length + 1));
    if (!file.startsWith(directory + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      response.writeHead(404).end(); return;
    }
    const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.json':'application/json', '.wasm':'application/wasm', '.zip':'application/zip', '.whl':'application/zip', '.png':'image/png', '.pdf':'application/pdf' }[path.extname(file)] || 'application/octet-stream';
    response.writeHead(200, { 'Content-Type': mime, 'Access-Control-Allow-Origin': '*' });
    if (liveClients && path.extname(file) === '.html') {
      const html = fs.readFileSync(file, 'utf8');
      response.end(html.replace('</body>', `<script>new EventSource('${base}/__events').onmessage=()=>location.reload();</script></body>`));
    } else fs.createReadStream(file).pipe(response);
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const server = previewServer(fileURLToPath(new URL('../_build/html', import.meta.url)));
  server.listen(4173, '127.0.0.1', () => console.log('Preview: http://127.0.0.1:4173/comp521/'));
}
