import fs from 'node:fs';
import path from 'node:path';

export function localFile(root, relative) {
  const base = fs.realpathSync(root);
  const file = fs.realpathSync(path.resolve(base, relative));
  if (!file.startsWith(base + path.sep)) throw new Error(`Asset escapes project: ${relative}`);
  return file;
}

export function assetData(root, relative) {
  const file = localFile(root, relative);
  const mime = { '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.mp4': 'video/mp4',
    '.webm': 'video/webm', '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg',
    '.vtt': 'text/vtt' }[path.extname(file).toLowerCase()];
  if (!mime) throw new Error(`Unsupported asset format: ${relative}`);
  return `data:${mime};base64,${fs.readFileSync(file).toString('base64')}`;
}

export function embeddedHtml(root, relative) {
  const html = fs.readFileSync(localFile(root, relative), 'utf8');
  // Embedded documents own their runtime. Relative external assets would break in srcdoc.
  if (/(?:src|href)\s*=\s*["'](?!data:|#)(?!["'])/i.test(html) || /@import\s|url\(\s*["']?(?!data:)/i.test(html)) {
    throw new Error(`Embed ${relative} must inline its static assets.`);
  }
  return html;
}
