import fs from 'node:fs';
import {createHash} from 'node:crypto';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

export async function checkDecks(manifestFile, outputDir, options = {}) {
  const manifest=JSON.parse(fs.readFileSync(manifestFile,'utf8')),root=path.dirname(path.resolve(manifestFile));
  fs.mkdirSync(outputDir,{recursive:true});
  const chrome=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser=await chromium.launch({headless:true,...(fs.existsSync(chrome)?{executablePath:chrome}:{})});
  const report={version:1,kind:'presentation-review',scientificReview:'not-performed',visualReview:'human-review-required',findings:[],decks:[]};
  const baseline=options.baseline?JSON.parse(fs.readFileSync(options.baseline,'utf8')):null;
  const add=(deck,slide,severity,component,observed,repair,evidence)=>report.findings.push({source:deck.source,line:slide?.line||null,cellIndex:slide?.cellIndex||null,slideId:slide?.id||null,severity,component,observed,repair,evidence});
  try {
    for(const deck of manifest.decks.filter(d=>!options.deck||path.basename(d.file,'.html')===options.deck)) {
      const context=await browser.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce'}),page=await context.newPage();
      const errors=[],network=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
      const name=path.basename(deck.file,'.html'),result={file:deck.file,sha256:createHash('sha256').update(fs.readFileSync(path.join(root,deck.file))).digest('hex'),source:deck.source,slides:[],pdf:`${name}.pdf`};report.decks.push(result);
      await page.goto(pathToFileURL(path.join(root,deck.file)).href+'?review');await page.waitForFunction(()=>window.deckReady);await page.evaluate(()=>{Reveal.configure({transition:'none',autoAnimate:false});});
      for(const slide of deck.slideIndex) {
        await page.evaluate(id=>{const s=document.getElementById(id);if(!s)throw Error('Missing slide '+id);const {h,v}=Reveal.getIndices(s);Reveal.slide(h,v,-1);},slide.id);
        const fragmentCount=await page.evaluate(()=>new Set([...Reveal.getCurrentSlide().querySelectorAll('.fragment')].map(e=>e.dataset.fragmentIndex)).size);
        if(fragmentCount>40)add(deck,slide,'warning','fragments',`${fragmentCount} fragment steps; only the first 40 were inspected.`, 'Simplify staging or review remaining steps manually.');
        const states=[];
        for(let step=-1;step<Math.min(fragmentCount,40);step++) {
          await page.evaluate(step=>{const {h,v}=Reveal.getIndices();Reveal.slide(h,v,step);window.fitCurrentSlide?.();},step);await page.waitForTimeout(60);
          const observed=await page.evaluate(()=>{
            const s=Reveal.getCurrentSlide(),scale=Reveal.getScale(),bounds=s.getBoundingClientRect();
            const visible=e=>(!e.closest('details:not([open])')||!!e.closest('summary'))&&e.getClientRects().length&&!e.closest('[aria-hidden=true], [inert], .notes')&&getComputedStyle(e).visibility!=='hidden';
            const text=[...s.querySelectorAll('p,li,pre code,figcaption,h2,.source-link,.component-label,svg text')].filter(visible);
            const tiny=text.filter(e=>parseFloat(getComputedStyle(e).fontSize)<18&&!e.matches('.source-link')).map(e=>({tag:e.tagName,text:e.textContent.slice(0,90),pixels:parseFloat(getComputedStyle(e).fontSize)}));
            const badImages=[...s.querySelectorAll('img')].filter(e=>visible(e)&&(!e.complete||!e.naturalWidth||!e.alt)).map(e=>e.alt||'missing alt');
            const unnamed=[...s.querySelectorAll('button,input,iframe')].filter(visible).filter(e=>!(e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')||e.getAttribute('title')||e.textContent.trim()||e.labels?.length)).map(e=>e.tagName);
            const nested=[...s.querySelectorAll('pre code,.myst-reveal-column,.slide-panel')].filter(visible).filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.className);
            const geometry=[...s.children].filter(visible).map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,x:Math.round((r.left-bounds.left)/scale),y:Math.round((r.top-bounds.top)/scale),width:Math.round(r.width/scale),height:Math.round(r.height/scale)};});
            const focus=[...s.querySelectorAll('a[href],button,input,textarea')].filter(visible).filter(e=>!e.disabled).map(e=>{e.focus({preventScroll:true});return document.activeElement===e;});
            return {fit:window.slideFitReports?.[s.id],tiny,badImages,unnamed,nested,keyboardFocus:focus.every(Boolean),geometry};
          });
          const shot=`${name}-${slide.id}-${step+1}.png`;await page.screenshot({path:path.join(outputDir,shot)});states.push({step,screenshot:shot,...observed});
          if(observed.fit?.overflow)add(deck,slide,'error','layout',observed.fit,'Split the slide, revise columns, or reduce content. Do not lower the font floor.',shot);
          if(observed.tiny.length)add(deck,slide,'warning','text-size',observed.tiny,'Enlarge essential text; review metadata separately.',shot);
          if(observed.nested.length)add(deck,slide,'error','code-or-columns',observed.nested,'Wrap or split long code and rebalance column widths.',shot);
          if(observed.badImages.length)add(deck,slide,'error','images',observed.badImages,'Supply a loadable local image and descriptive alt text.',shot);
          if(observed.unnamed.length||!observed.keyboardFocus)add(deck,slide,'error','accessibility',{unnamed:observed.unnamed,keyboardFocus:observed.keyboardFocus},'Label controls and restore keyboard focus.',shot);
          const old=baseline?.decks.find(d=>d.file===deck.file)?.slides.find(s=>s.id===slide.id)?.states.find(s=>s.step===step);
          if(old&&JSON.stringify(old.geometry)!==JSON.stringify(observed.geometry))add(deck,slide,'warning','layout-regression',{before:old.geometry,after:observed.geometry},'Compare screenshots and approve or repair the changed layout.',shot);
        }
        result.slides.push({id:slide.id,line:slide.line,cellIndex:slide.cellIndex,states});
      }
      // Check local destinations against the output bundle, including anchor existence.
      const links=await page.locator('a[href]').evaluateAll(es=>es.map(e=>({href:e.getAttribute('href'),slide:e.closest('section[id]')?.id})));const cache=new Map();
      for(const link of links){if(/^(https?:|mailto:)/.test(link.href))continue;if(link.href.startsWith('/')){add(deck,deck.slideIndex.find(s=>s.id===link.slide),'warning','site-link',link.href,'Verify this site-root destination on the local HTTP preview or deployed site.');continue;}const url=new URL(link.href,pathToFileURL(path.join(root,deck.file)));if(url.protocol!=='file:')continue;const file=fileURLToPath(url),anchor=decodeURIComponent(url.hash.replace(/^#\/?/,''));let content=cache.get(file);if(content===undefined){content=fs.existsSync(file)?fs.readFileSync(file,'utf8'):null;cache.set(file,content);}if(!content||(anchor&&!content.includes(`id="${anchor}"`)))add(deck,deck.slideIndex.find(s=>s.id===link.slide),'error','link',link.href,'Repair the destination or include the referenced slide/source.');}
      if(errors.length)add(deck,null,'error','runtime',errors,'Repair browser errors before presenting.');
      if(network.length)add(deck,null,'warning','network',[...new Set(network)],'Bundle required assets or document intentional network dependencies.');
      const pdf=await context.newPage();await pdf.goto(pathToFileURL(path.join(root,deck.file)).href+'?print-pdf');await pdf.waitForFunction(()=>document.querySelector('.pdf-page'));await pdf.pdf({path:path.join(outputDir,result.pdf),printBackground:true,preferCSSPageSize:true});await context.close();
    }
  } finally { await browser.close(); }
  if(!report.decks.length)throw Error('No decks matched the review request.');
  report.summary={errors:report.findings.filter(f=>f.severity==='error').length,warnings:report.findings.filter(f=>f.severity==='warning').length,slides:report.decks.reduce((n,d)=>n+d.slides.length,0)};
  fs.writeFileSync(path.join(outputDir,'report.json'),JSON.stringify(report,null,2)+'\n');
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  fs.writeFileSync(path.join(outputDir,'index.html'),`<!doctype html><html lang="en"><meta charset="utf-8"><title>Slide review</title><style>body{font:16px system-ui;margin:24px;background:#eef1f5}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:20px}article{background:white;padding:12px}img{width:100%}p{overflow-wrap:anywhere}</style><h1>Slide review</h1><p>${report.summary.errors} errors; ${report.summary.warnings} warnings. Scientific review not performed. Inspect labels, contrast, composition, and PDF fallbacks manually.</p><a href="report.json">Structured report</a><main>${report.decks.flatMap(d=>d.slides.map(s=>`<article><h2>${escape(s.id)}</h2><p>${escape(d.source)}${s.cellIndex ? ' cell '+s.cellIndex : ''}:${s.line||'?'} · <a href="${escape(d.pdf)}">PDF</a></p>${s.states.map(state=>`<a href="${escape(state.screenshot)}"><img alt="${escape(s.id)} step ${state.step+1}" src="${escape(state.screenshot)}"></a>`).join('')}</article>`)).join('')}</main></html>`);
  return report;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const args=process.argv.slice(2),value=k=>args.includes(k)?args[args.indexOf(k)+1]:undefined;
  try {const report=await checkDecks(path.resolve(args[0]||'_build/html/reveal/decks.json'),path.resolve(value('--out')||'_build/review'),{deck:value('--deck'),baseline:value('--baseline')});console.log(JSON.stringify(report.summary));if(report.summary.errors)process.exitCode=1;}catch(e){console.error(e.stack);process.exitCode=1;}
}
