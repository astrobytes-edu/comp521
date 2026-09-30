// Behavior assertions for the approved SWE teaching order. Build the deck first.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
import {chromium} from 'playwright';
const deck=path.resolve(process.argv[2] || '_build/html/reveal/migrations/software-engineering.html');
// Each inner array is one click. All of its content must arrive together.
const plans={
 'why-this-matters':[['This works for small scripts'],['Code that must be correct'],['Code that others must read'],['Code you must debug']],
 'id-1-think-before-you-type':[['Write one expected result'],['3','divide by two']],
 'id-2-write-down-the-contract':[['The input range','0.1']],
 'bad-repo-vs-good-repo':[['Reproducibility means','clean clone']],
 'id-4-fail-fast':[['Both return','Reject invalid mass','if not 0.1'],['A clear error']],
 'id-5-plot-first-not-last':[['Diagnose'],['Validate'],['Communicate'],['The minimum','both inputs give']],
 'id-3-assume-your-code-is-wrong':[['Not “it runs without errors.”'],['Not “the output looks reasonable.”'],['Show me the evidence.']],
 'id-6-test-requirements-not-code':[['Good test:','def test_luminosity_solar_mass','pytest.approx']],
 'id-7-debug-with-hypotheses':[['Observed','missing the square'],['f(2) == 4','before changing']],
 'id-8-delete-bad-code':[['I’ve already put so much time'],['This is the sunk cost fallacy.'],['Those 3 hours are gone.']],
 'permission-to-delete':[['Delete functions'],['Rewrite modules'],['Throw away'],['Start fresh'],['preserve the failing input','Git protects']],
 'id-9-one-source-of-truth':[['Good:','# constants.py']],
 'id-10-read-more-than-you-write':[['Before changing code:'],['Understand what it does now'],['Understand why it was written'],['Then modify']],
 'id-11-commit-before-you-experiment':[['Only model.py','staged in it'],['If it goes badly:','git restore','Uncommitted or ignored files']],
 'the-walk-away-rule':[['Stop typing'],['Go do something else'],['Come back with fresh eyes'],['This isn’t procrastination.']],
 'how-to-ask-for-help':[['Good:','Here’s my code:']],
 'the-key-insight':[['Debug your understanding, not your code.'],['Understanding the problem gives you'],['When repeated patches fail']],
 'the-anti-pattern':[['Write all the code'],['Debug until it runs'],['Make plots at the end'],['Discover something'],['Start over']],
 'the-binary-search-method':[['Check output at the end'],['Check output at the middle','Yes','No'],['Repeat until found'],['With ordered checkpoints']],
 'the-5-step-process':[['Understand'],['Plan'],['Implement'],['Test'],['Debug']],
 'transfer-the-workflow-to-your-project':[['Write the input'],['Pick one reference'],['Run the smallest'],['State a hypothesis'],['Check limits'],['Save the configuration'],['Keep the original stellar examples']],
 'before-next-class':[['Read the full guide'],['Keep the 11 principles'],['Apply these principles']],
};
const chrome=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser=await chromium.launch({headless:true,...(fs.existsSync(chrome)?{executablePath:chrome}:{})});
let checks=0;
try {
 const page=await browser.newPage();await page.goto(pathToFileURL(deck).href);await page.waitForFunction(()=>window.deckReady);
 await page.evaluate(()=>Reveal.configure({transition:'none'}));
 for(const [slug,steps] of Object.entries(plans)) {
  await page.evaluate(id=>{const s=document.getElementById(id);const {h,v}=Reveal.getIndices(s);Reveal.slide(h,v,-1);},'slide-'+slug);
  const check=async stage=>{
   await page.waitForFunction(stage=>[...Reveal.getCurrentSlide().querySelectorAll('.fragment')].every((e,i)=>(e.classList.contains('visible')&&getComputedStyle(e).visibility!=='hidden')===(i<=stage)),stage,{timeout:2000});
   const observed=await page.evaluate(()=>[...Reveal.getCurrentSlide().querySelectorAll('.fragment')].map(e=>({visible:e.classList.contains('visible')&&getComputedStyle(e).visibility!=='hidden',text:e.textContent.replace(/\s+/g,' ').trim()})));
   assert.equal(observed.length,steps.length,slug+' fragment count');
   steps.forEach((tokens,i)=>{assert.equal(observed[i].visible,i<=stage,slug+' visibility at '+stage);for(const token of tokens)assert.ok(observed[i].text.includes(token),slug+' missing grouped content: '+token);});checks++;
  };
  await check(-1);
  for(let i=0;i<steps.length;i++){await page.keyboard.press('ArrowRight');await page.waitForFunction(i=>Reveal.getIndices().f===i,i);await check(i);}
  for(let i=steps.length-2;i>=-1;i--){await page.keyboard.press('ArrowLeft');await page.waitForFunction(i=>(Reveal.getIndices().f??-1)===i,i);await check(i);}
 }
 const structure=await page.evaluate(()=>({transitions:[...document.querySelectorAll('.swe-transition .slide-eyebrow')].map(e=>e.textContent),ids:[...document.querySelectorAll('.slides section[id]')].map(e=>e.id)}));
 assert.equal(structure.ids[0],'slide-software-engineering-for-scientists');
 assert.equal(structure.ids[1],'slide-why-this-matters');
 assert.equal(structure.ids.length,50);
 assert.equal(structure.transitions.filter(t=>t.startsWith('Commandment')).length,11);
 assert.ok(structure.ids.indexOf('slide-worked-example-independent-checks')<structure.ids.indexOf('slide-before-next-class'));
 assert.equal(structure.ids.at(-1),'slide-questions');
 const result={slides:structure.ids.length,titleSlide:'passed',slidesWithExplicitSequence:Object.keys(plans).length,forwardBackwardStates:checks,commandmentTransitions:11,closingOrder:'passed'};
 fs.writeFileSync('_build/swe-sequence-review.json',JSON.stringify(result,null,2)+'\n');console.log(result);
}finally{await browser.close();}
