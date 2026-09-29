import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
export function rehearsalPacket(manifestFile,reviewFile,output){
 const manifest=JSON.parse(fs.readFileSync(manifestFile)),review=JSON.parse(fs.readFileSync(reviewFile)),root=path.dirname(manifestFile);
 const decks=review.decks.map(checked=>{
  const deck=manifest.decks.find(d=>d.file===checked.file);if(!deck)throw Error('Review deck is absent from manifest.');
  const hash=createHash('sha256').update(fs.readFileSync(path.join(root,deck.file))).digest('hex');if(hash!==checked.sha256)throw Error('Review is stale. Run the checker on the current export first.');
  return {file:deck.file,slides:deck.slideIndex.map(slide=>({id:slide.id,title:slide.title,source:deck.source,line:slide.line,cellIndex:slide.cellIndex,cue:slide.cue,evidence:slide.evidence||[],paths:slide.paths||[],screenshots:checked.slides.find(s=>s.id===slide.id)?.states.map(s=>path.resolve(path.dirname(reviewFile),s.screenshot))||[],findings:review.findings.filter(f=>f.slideId===slide.id&&f.source===deck.source),questions:[`What should this audience understand after “${slide.title}”?`,'Which assumptions and units are needed to interpret this slide?','What source supports the claim, and what would falsify it?',...(slide.paths?.length?['Take each explanation branch, explore its controls, then verify that Return restores the starting state.']:[]),'Explain how this slide connects to the next main-story slide without relying on speaker notes.']}))};
 });
 const packet={version:1,kind:'agent-rehearsal-packet',scientificReview:'not-performed',instructions:'For each slide, inspect its screenshots and source. Exercise relevant controls. Answer the audience questions using provided evidence only. Report missing support as a question, not a fabricated defect. Separate reproduced UI defects, visual judgments, scientific questions, and suggested edits. Cite slide IDs and evidence. Do not treat this generated packet as a completed review.',decks};
 fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(packet,null,2)+'\n');return packet;
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 try{const [manifest,review,output]=process.argv.slice(2);if(!manifest||!review||!output)throw Error('Usage: npm run rehearse -- decks.json report.json rehearsal.json');const packet=rehearsalPacket(path.resolve(manifest),path.resolve(review),path.resolve(output));console.log(`Prepared ${packet.decks.reduce((n,d)=>n+d.slides.length,0)} slide briefs. Agent review still required.`);}catch(error){console.error(error.message);process.exitCode=1;}
}
