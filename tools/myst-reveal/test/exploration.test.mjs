import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chromium} from 'playwright';
import {exportDeck} from '../src/build.mjs';
import {loadDocuments,selectDocument} from '../src/project.mjs';
import {previewServer} from '../src/preview.mjs';
import {explanationHtml} from '../src/explanations.mjs';
import {rehearsalPacket} from '../src/rehearse.mjs';
const root=new URL('../',import.meta.url).pathname;
const launch=()=>chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const go=async(page,id)=>{await page.evaluate(id=>{const s=document.getElementById(id),p=Reveal.getIndices(s);Reveal.slide(p.h,p.v,-1);},id);await page.waitForTimeout(150);};
test('linked explanation rejects untraceable code lines and figure regions',()=>{
 const base={title:'Example',alt:'Curve',source:'unused',code:'x=1',terms:[{label:'x',math:'x',explain:'Input',lines:[2],region:[0,0,1,1]}]};
 assert.throws(()=>explanationHtml(base,{},'',String),/one-based/);
 base.terms[0].lines=[1];base.terms[0].region=[.8,0,.4,1];assert.throws(()=>explanationHtml(base,{},'',String),/normalized/);
});
test('nested explanation paths restore linked selection and exact Reveal fragment state',{timeout:60000},async()=>{
 const browser=await launch();try{
 const page=await browser.newPage({viewport:{width:1280,height:720}});await page.goto('file://'+root+'_build/html/reveal/exploration.html');await page.waitForFunction(()=>window.deckReady);
 assert.equal(await page.evaluate(()=>Reveal.getSlides().length),5);assert.equal(await page.evaluate(()=>Reveal.getHorizontalSlides().length),3);
 await page.evaluate(()=>{const e=document.createElement('span');e.className='fragment';e.textContent='Test fragment';Reveal.getCurrentSlide().append(e);Reveal.syncFragments();Reveal.navigateFragment(0);});
 await page.getByRole('button',{name:'Squared coordinate',exact:true}).click();
 assert.equal(await page.locator('.linked-explanation [data-code-line]').count(),7);
 assert.doesNotMatch(await page.locator('.linked-explanation pre').textContent(),/<span/);
 assert.ok(await page.locator('.linked-explanation .hljs-number').count()>0);
 assert.deepEqual(await page.locator('.linked-explanation .linked-active').evaluateAll(lines=>lines.map(e=>Number(e.dataset.codeLine))),[4,5]);
 await page.getByRole('combobox',{name:'Explanation level',exact:true}).filter({visible:true}).selectOption('Conceptual');
 assert.equal(await page.getByRole('link',{name:'Try the calculation',exact:true}).isVisible(),false);
 await page.getByRole('link',{name:'Why this shape?',exact:true}).click();await page.waitForFunction(()=>Reveal.getCurrentSlide().id==='slide-why-this-shape');
 await page.getByRole('link',{name:'Inspect numerical values',exact:true}).click();await page.waitForFunction(()=>Reveal.getCurrentSlide().id==='slide-try-the-calculation');
 const frame=page.frameLocator('.present iframe');await frame.getByRole('textbox',{name:'Python code'}).fill('print("detour edit")');
 await page.getByRole('button',{name:'Return to previous explanation',exact:true}).filter({visible:true}).click();await page.waitForFunction(()=>Reveal.getCurrentSlide().id==='slide-why-this-shape');
 await page.getByRole('button',{name:'Return to previous explanation',exact:true}).filter({visible:true}).click();await page.waitForFunction(()=>Reveal.getCurrentSlide().id==='slide-one-expression-three-views');
 assert.equal(await page.getByRole('button',{name:'Squared coordinate',exact:true}).getAttribute('aria-pressed'),'true');
 assert.equal(await page.evaluate(()=>Reveal.getIndices().f),0);
 assert.equal(await page.evaluate(()=>document.activeElement.closest('section').id),'slide-one-expression-three-views');
 await go(page,'slide-why-this-shape');await page.getByText('Assumptions behind the derivation',{exact:true}).click();assert.match(await page.getByRole('dialog').textContent(),/positive scalar/);await page.getByRole('button',{name:'Close evidence'}).click();
 await page.goto('file://'+root+'_build/html/reveal/exploration.handout.html');assert.match(await page.locator('body').textContent(),/No measurement or physical calibration/);
 }finally{await browser.close();}
});
test('replay restores offline Python figures, edited code and parameters without recomputing', {timeout:60000,skip:!fs.existsSync(root+'_build/html/python/bundle.json')},async()=>{
 const server=previewServer(root+'_build/html');await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port+'/comp521';
 const docs=loadDocuments(root+'examples/courses');
 let browser;
 try{
 exportDeck(root+'examples/courses',root+'_build/html/replay-test/exploration.html',{document:selectDocument(docs,'exploration.md'),documents:docs,siteUrl:base,pythonRuntime:base+'/python/'});
 browser=await launch();const context=await browser.newContext({viewport:{width:1280,height:720}});await context.route(/^https?:/,route=>route.request().url().startsWith(base)?route.continue():route.abort());const page=await context.newPage();await page.goto(base+'/replay-test/exploration.html');await page.waitForFunction(()=>window.deckReady);await go(page,'slide-try-the-calculation');
 const frame=page.frameLocator('.present iframe'),slider=frame.getByRole('slider',{name:'Amplitude'});
 const run=async()=>{await frame.getByRole('button',{name:'Run Python',exact:true}).click();await frame.locator('#status').filter({hasText:/^Done$/}).waitFor({timeout:40000});return frame.locator('#figures img').getAttribute('src');};
 const save=async()=>{await page.getByRole('button',{name:'Save step',exact:true}).filter({visible:true}).click();await page.locator('.present .slide-replay output').filter({hasText:/Saved step/}).waitFor();};
 const first=await run();await save();await slider.fill('2');const second=await run();assert.notEqual(first,second);await save();
 await slider.fill('0.5');const third=await run();const initial=await frame.getByRole('textbox',{name:'Python code'}).inputValue();await frame.getByRole('textbox',{name:'Python code'}).fill(initial+'\n# Exploration note');
 await page.getByRole('button',{name:'Replay from start'}).filter({visible:true}).click();await frame.locator('#status').filter({hasText:/restored/}).waitFor();assert.equal(await slider.inputValue(),'1');assert.equal(await frame.locator('#figures img').getAttribute('src'),first);
 await page.getByRole('button',{name:'Next saved step'}).filter({visible:true}).click();await page.locator('.present .slide-replay output').filter({hasText:/step 2 of 2/}).waitFor();assert.equal(await slider.inputValue(),'2');assert.equal(await frame.locator('#figures img').getAttribute('src'),second);
 await page.getByRole('button',{name:'Return to exploration'}).filter({visible:true}).click();await page.locator('.present .slide-replay output').filter({hasText:/Returned/}).waitFor();assert.equal(await slider.inputValue(),'0.5');assert.equal(await frame.locator('#figures img').getAttribute('src'),third);assert.match(await frame.getByRole('textbox',{name:'Python code'}).inputValue(),/Exploration note/);
 }finally{await browser?.close();await new Promise(r=>server.close(r));}
});

test('agent rehearsal rejects stale rendered evidence',()=>{
 const dir=fs.mkdtempSync('/private/tmp/myst-rehearsal-test-');
 try{
  fs.writeFileSync(dir+'/deck.html','new rendered content');
  fs.writeFileSync(dir+'/decks.json',JSON.stringify({decks:[{file:'deck.html',slideIndex:[]}]}));
  fs.writeFileSync(dir+'/report.json',JSON.stringify({decks:[{file:'deck.html',sha256:'stale'}]}));
  assert.throws(()=>rehearsalPacket(dir+'/decks.json',dir+'/report.json',dir+'/packet.json'),/stale/);
  assert.equal(fs.existsSync(dir+'/packet.json'),false);
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
