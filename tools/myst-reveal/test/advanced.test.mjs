import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { chromium } from 'playwright';
import { exportDeck } from '../src/build.mjs';
import { loadDocuments, selectDocument } from '../src/project.mjs';
import { renderSlides, splitSlides } from '../src/render.mjs';
import { linkedPlotHtml } from '../src/figures.mjs';
import { previewServer } from '../src/preview.mjs';
import { checkDecks } from '../src/check.mjs';
const root=new URL('../',import.meta.url).pathname,project=root+'examples/courses',out=root+'_build/html/reveal';
const chrome=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const launch=()=>chromium.launch({headless:true,...(fs.existsSync(chrome)?{executablePath:chrome}:{})});
const go=async(page,id)=>{await page.evaluate(id=>{const s=document.getElementById(id),{h,v}=Reveal.getIndices(s);Reveal.slide(h,v,-1);},id);await page.waitForTimeout(250);};

test('notebook prose cells split into slides and retain cell addresses',()=>{
 const heading=id=>({type:'heading',depth:2,identifier:id,children:[{type:'text',value:id}]});
 const slides=splitSlides({children:[{type:'block',children:[heading('first')]},{type:'block',kind:'notebook-code',children:[{type:'code',value:'x=1'}]},{type:'block',kind:'notebook-content',children:[heading('second')]}]});
 assert.deepEqual(slides.map(s=>[s.id,s.cellIndex]),[['slide-first',1],['slide-second',3]]);
 assert.equal(slides[0].children[1].kind,'notebook-code');
});
test('variants retain stable IDs; invalid columns and logarithmic plots fail explicitly',()=>{
 const m=JSON.parse(fs.readFileSync(out+'/decks.json'));assert.equal(m.decks.find(d=>d.file==='advanced-short.html').slides,4);
 const docs=loadDocuments(project),doc=structuredClone(selectDocument(docs,'advanced.md'));
 const visit=n=>{if(n.class==='myst-reveal-columns')n.reveal.ratio='2 1';(n.children||[]).forEach(visit);};visit(doc.mdast);
 assert.throws(()=>renderSlides(doc,project+'/_build/site/public',{documents:docs,projectDir:project,siteUrl:'/comp521'}),/Column ratio/);
 const spec={x:[1,10,100],xScale:'log',xLabel:'Synthetic input',panels:[{label:'Square',scale:'log',values:[1,100,10000]}]};
 const data={location:'/data.ipynb',mdast:{children:[{type:'block',identifier:'plot',children:[{type:'output',jupyter_data:{data:{'application/json':{content:spec}}}}]}]}};
 const opts={source:'data.ipynb#plot',title:'Log plot'},settings={documents:[data],siteUrl:'/comp521'};
 const html=linkedPlotHtml(opts,settings,'',s=>String(s));assert.match(html,/data-x="\[65,345,625\]"/);
 spec.panels[0].values[0]=0;assert.throws(()=>linkedPlotHtml(opts,settings,'',s=>String(s)),/positive/);
 spec.panels[0].values[0]=1;spec.panels[0].lower=[.9,99,9999];spec.panels[0].upper=[1.1,101,10001];assert.throws(()=>linkedPlotHtml(opts,settings,'',s=>String(s)),/bandLabel/);
});
test('advanced UI: columns, sizing floor, image blend, synchronized movies, backups and rehearsal', {timeout:90000},async()=>{
 const b=await launch();try{
  const p=await b.newPage({viewport:{width:1440,height:900}});const errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto('file://'+out+'/advanced.html');await p.waitForFunction(()=>window.deckReady);
  assert.equal(await p.locator('body.theme-dark').count(),1);
  await go(p,'slide-flexible-columns');const widths=await p.locator('.present .myst-reveal-column').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().width));assert.ok(Math.abs(widths[0]/widths[1]-2)<.05);assert.ok(await p.evaluate(()=>slideFitReports['slide-flexible-columns'].fontSize>=28));
  await p.evaluate(()=>{const s=Reveal.getCurrentSlide();const div=document.createElement('div');div.style.height='1000px';div.dataset.testOversize='true';s.append(div);fitCurrentSlide();});assert.equal(await p.evaluate(()=>slideFitReports['slide-flexible-columns'].overflow),true);assert.equal(await p.evaluate(()=>slideFitReports['slide-flexible-columns'].fontSize),28);await p.locator('[data-test-oversize]').evaluate(e=>e.remove());
  await go(p,'slide-give-the-figure-room');assert.equal(await p.locator('.present .figure-region').count(),1);
  await go(p,'slide-compare-images-deliberately');await p.getByRole('slider',{name:'Image blend'}).fill('70');assert.equal(await p.locator('.present .comparison-images').evaluate(e=>e.style.getPropertyValue('--blend')),'0.7');
  await go(p,'slide-synchronize-playback');await p.getByRole('button',{name:'Play together'}).click();await p.waitForTimeout(500);const times=await p.locator('.present video').evaluateAll(es=>es.map(e=>e.currentTime));assert.ok(times[0]>0);assert.ok(Math.abs(times[0]-times[1])<.2);await p.getByRole('button',{name:'Reset',exact:true}).click();assert.equal(await p.locator('.present video').first().evaluate(e=>e.currentTime),0);
  await go(p,'slide-follow-the-evidence-into-questions');await p.getByRole('button',{name:'Tools',exact:true}).click();await p.getByRole('button',{name:'Backups',exact:true}).click();await p.getByRole('dialog').getByRole('button',{name:'Backup: what the trace records',exact:true}).click();assert.equal(await p.evaluate(()=>Reveal.getCurrentSlide().dataset.backup),'true');await p.getByRole('button',{name:'Tools',exact:true}).click();await p.getByRole('button',{name:'Return to talk'}).click();assert.equal(await p.evaluate(()=>Reveal.getCurrentSlide().id),'slide-follow-the-evidence-into-questions');
  await p.getByRole('button',{name:'Tools',exact:true}).click();await p.getByRole('button',{name:'Rehearse',exact:true}).click();const panel=p.getByRole('complementary',{name:'Rehearsal'});await panel.getByRole('button',{name:'Start',exact:true}).click();await p.waitForTimeout(1100);await panel.getByRole('button',{name:'Pause',exact:true}).click();const download=p.waitForEvent('download');await panel.getByRole('button',{name:'Download timings'}).click();const file=await (await download).path();const recording=JSON.parse(fs.readFileSync(file));assert.ok(recording.totalSeconds>=1);assert.ok(recording.records.some(r=>r.slideId==='slide-follow-the-evidence-into-questions'));
  assert.deepEqual(errors,[]);
 }finally{await b.close();}
});
test('offline local Python: parameters, actual trace, keyboard editing and plot generation', {timeout:150000,skip:!fs.existsSync(root+'_build/html/python/bundle.json')},async()=>{
 const server=previewServer(root+'_build/html');await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/comp521`;
 const docs=loadDocuments(project),doc=selectDocument(docs,'advanced.md');exportDeck(project,out+'/offline-check.html',{document:doc,documents:docs,siteUrl:base,pythonRuntime:base+'/python/',theme:'dark'});
 const b=await launch();try{const p=await b.newPage({viewport:{width:1440,height:900}}),remote=[];await p.route('**/*',r=>{if(/^https?:/.test(r.request().url())&&!r.request().url().startsWith(base)){remote.push(r.request().url());return r.abort();}return r.continue();});await p.goto(base+'/reveal/offline-check.html');await p.waitForFunction(()=>window.deckReady);
  await go(p,'slide-trace-actual-python-state');let frame=p.frameLocator('.present iframe');await frame.getByRole('button',{name:'Run Python',exact:true}).click();await frame.locator('#status').filter({hasText:/^Done$/}).waitFor({timeout:60000});assert.match(await frame.locator('#output').textContent(),/\[1, 4, 9\]/);await frame.getByRole('button',{name:'Next step'}).click();await frame.locator('#variables').filter({hasText:'values'}).waitFor();assert.match(await frame.locator('#variables').textContent(),/values/);assert.ok(await frame.locator('.trace-active').count());
  const code=frame.getByRole('textbox',{name:'Python code'});await code.fill('for i in range(2):');await code.press('End');await code.press('Enter');assert.match(await code.inputValue(),/\n    $/);await code.type('print(i)');await code.press('Control+Enter');await frame.locator('#status').filter({hasText:/^Done$/}).waitFor({timeout:60000});assert.match(await frame.locator('#output').textContent(),/0\n1/);
  await go(p,'slide-change-a-parameter-and-compute');frame=p.frameLocator('.present iframe');await frame.getByRole('slider',{name:'Amplitude',exact:true}).fill('2');await frame.getByRole('button',{name:'Run Python',exact:true}).click();await frame.locator('#status').filter({hasText:/^Done$/}).waitFor({timeout:60000});assert.equal(await frame.locator('#figures img').count(),1);await frame.locator('#divider').focus();await frame.locator('#divider').press('ArrowRight');assert.equal(await frame.locator('#divider').getAttribute('aria-valuenow'),'55');await frame.getByRole('button',{name:'Reset',exact:true}).click();assert.equal(await frame.getByRole('slider',{name:'Amplitude',exact:true}).inputValue(),'1');await frame.getByRole('button',{name:'Precomputed result',exact:true}).click();assert.ok(await frame.locator('#fallback img').isVisible());assert.deepEqual(remote,[]);
 }finally{await b.close();await new Promise(r=>server.close(r));}
});
test('review report detects an intentionally oversized slide and retains source location', {timeout:90000},async()=>{
 const folder=root+'_build/checker-negative';fs.mkdirSync(folder,{recursive:true});const html=fs.readFileSync(out+'/advanced-short.html','utf8').replace('<h2 id="flexible-columns">','<div style="height:1200px">Overflow fixture</div><h2 id="flexible-columns">');fs.writeFileSync(folder+'/deck.html',html);
 const manifest=JSON.parse(fs.readFileSync(out+'/decks.json'));const deck=manifest.decks.find(d=>d.file==='advanced-short.html');fs.writeFileSync(folder+'/decks.json',JSON.stringify({decks:[{...deck,file:'deck.html',slideIndex:deck.slideIndex.filter(s=>s.id==='slide-flexible-columns')}]}));
 const report=await checkDecks(folder+'/decks.json',folder+'/report');assert.ok(report.findings.some(f=>f.component==='layout'&&f.source==='/advanced.md'&&f.line===13));assert.ok(fs.existsSync(folder+'/report/index.html'));assert.ok(fs.existsSync(folder+'/report/deck.pdf'));
});

test('icon tools start collapsed, dismiss, preserve theme icons and support keyboard focus',async()=>{
 const browser=await launch();
 try {
  const page=await browser.newPage({viewport:{width:1280,height:720}});
  await page.goto('file://'+out+'/advanced.html');await page.waitForFunction(()=>window.deckReady);
  const tools=page.getByRole('button',{name:'Tools',exact:true});
  assert.equal(await tools.getAttribute('aria-expanded'),'false');
  assert.equal(await tools.locator('svg').count(),1);assert.equal(await tools.textContent(),'');
  await tools.click();const dark=page.getByRole('button',{name:'Dark mode',exact:true});
  assert.equal(await dark.isVisible(),true);await dark.click();
  assert.equal(await tools.getAttribute('aria-expanded'),'false');
  await tools.press('Enter');assert.equal(await dark.locator('svg').count(),1);assert.equal(await dark.getAttribute('aria-pressed'),'false');
  await page.keyboard.press('Escape');assert.equal(await tools.getAttribute('aria-expanded'),'false');
  assert.equal(await tools.evaluate(e=>e===document.activeElement),true);
  await tools.click();await page.locator('h2').first().click();assert.equal(await tools.getAttribute('aria-expanded'),'false');
  await tools.press('Enter');await tools.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.getAttribute('aria-label')),'Slides');
  await page.keyboard.press('Escape');
  fs.mkdirSync(root+'output/playwright',{recursive:true});await page.screenshot({path:root+'output/playwright/tools-collapsed.png'});
  await tools.click();await page.screenshot({path:root+'output/playwright/tools-expanded.png'});
 }finally{await browser.close();}
});
