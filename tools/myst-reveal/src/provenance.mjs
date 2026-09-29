import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
export function buildProvenance(projectDir, documents) {
  const root=new URL('../',import.meta.url),pkg=JSON.parse(fs.readFileSync(new URL('package.json',root)));
  const sourceFiles=documents.map(d=>d.location.replace(/^\//,''));
  const sources=sourceFiles.map(source=>({source,sha256:fs.existsSync(path.join(projectDir,source))?hash(path.join(projectDir,source)):null}));
  const kernels=new Set(sourceFiles.filter(f=>f.endsWith('.ipynb')).map(f=>JSON.parse(fs.readFileSync(path.join(projectDir,f))).metadata?.kernelspec?.name||'python3'));
  const observed=[];
  if(kernels.size){
    const result=spawnSync('jupyter',['kernelspec','list','--json'],{encoding:'utf8',timeout:10000});
    let specs;try{specs=JSON.parse(result.stdout||'{}').kernelspecs;}catch{specs=null;}
    for(const name of kernels){const spec=specs?.[name]?.spec,python=spec?.argv?.[0];let environment;
      if(python){const r=spawnSync(python,['-c','import json,sys,importlib.metadata as m; print(json.dumps({"python":sys.version,"executable":sys.executable,"packages":{n:m.version(n) for n in ("numpy","matplotlib","ipykernel") if m.packages_distributions().get(n)}}))'],{encoding:'utf8',timeout:15000});try{environment=JSON.parse(r.stdout);}catch{environment={unavailable:true};}}
      observed.push({name,argv:spec?.argv||null,environment:environment||{unavailable:true}});
    }
  }
  return {version:1,node:process.version,dependencies:pkg.dependencies,lockfileSha256:hash(new URL('../package-lock.json',import.meta.url)),sources,kernels:observed,kernelEvidence:'Environment observed at export using notebook kernelspec names. Cached MyST outputs may have been executed previously; this is not historical execution provenance.'};
}
