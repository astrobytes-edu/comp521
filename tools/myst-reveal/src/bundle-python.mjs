import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const base='https://cdn.jsdelivr.net/pyodide/v0.29.3/full/';
export async function bundlePython(destination, requested=['numpy','matplotlib']) {
  const response=await fetch(base+'pyodide-lock.json');if(!response.ok)throw Error(`Runtime lock: HTTP ${response.status}`);const lock=await response.json();
  const selected=new Set();function visit(name){if(selected.has(name))return;const p=lock.packages[name];if(!p)throw Error('Unknown Pyodide package '+name);selected.add(name);(p.depends||[]).forEach(visit);}requested.forEach(visit);
  const files=new Map(['pyodide.js','pyodide.asm.js','pyodide.asm.wasm','python_stdlib.zip'].map(f=>[f,null]));for(const name of selected){const p=lock.packages[name];files.set(p.file_name,p.sha256);}
  fs.mkdirSync(destination,{recursive:true});const records=[];
  for(const [name,expected] of files){if(path.basename(name)!==name)throw Error('Invalid runtime filename');const target=path.join(destination,name);let bytes=fs.existsSync(target)?fs.readFileSync(target):null;const digest=b=>crypto.createHash('sha256').update(b).digest('hex');if(!bytes||!expected||digest(bytes)!==expected){const r=await fetch(base+name);if(!r.ok)throw Error(`${name}: HTTP ${r.status}`);bytes=Buffer.from(await r.arrayBuffer());}const sha256=digest(bytes);if(expected&&sha256!==expected)throw Error('Integrity mismatch: '+name);fs.writeFileSync(target,bytes);records.push({file:name,bytes:bytes.length,sha256});}
  fs.writeFileSync(path.join(destination,'pyodide-lock.json'),JSON.stringify(lock));fs.writeFileSync(path.join(destination,'bundle.json'),JSON.stringify({version:'0.29.3',source:base,packages:[...selected],files:records},null,2));return records;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){try{const result=await bundlePython(path.resolve(process.argv[2]||'_build/html/python'));console.log(JSON.stringify({files:result.length,bytes:result.reduce((n,f)=>n+f.bytes,0)}));}catch(e){console.error(e.message);process.exitCode=1;}}
