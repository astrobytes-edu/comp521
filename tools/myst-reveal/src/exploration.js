/* Author-controlled explanations and in-memory exploration replay. */
window.setupExploration=function(printing){
 const R=window.Reveal;
 const focusSlide=()=>{const heading=R.getCurrentSlide().querySelector('h1,h2,h3');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}};
 document.querySelectorAll('.linked-explanation').forEach(group=>{
  group.querySelectorAll('.hljs-ln-code').forEach(line=>line.dataset.codeLine=line.dataset.lineNumber);
  const terms=JSON.parse(group.dataset.explanation),buttons=[...group.querySelectorAll('[data-term]')];
  const select=index=>{const term=terms[index];group.dataset.selectedTerm=index;buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));group.querySelectorAll('[data-code-line]').forEach(line=>line.classList.toggle('linked-active',term.lines.includes(Number(line.dataset.codeLine))));const box=group.querySelector('.explanation-region');box.hidden=false;['left','top','width','height'].forEach((k,i)=>box.style[k]=(100*term.region[i])+'%');group.querySelector('.explanation-description').textContent=term.explain;};
  buttons.forEach((b,i)=>b.onclick=()=>select(i));select(0);
 });
 if(printing){document.querySelectorAll('.slide-evidence,.explanation-key').forEach(e=>e.open=true);return;}
 const frames=()=>[...document.querySelectorAll('iframe.python-embed')];
 let requestId=0;
 const request=(frame,action,state)=>new Promise((resolve,reject)=>{
  const id=++requestId;
  const timeout=setTimeout(()=>{window.removeEventListener('message',receive);reject(Error('Python editor did not respond; no state saved.'));},4000);
  function receive(event){if(event.source!==frame.contentWindow||event.data?.type!=='myst-state-response'||event.data.id!==id)return;clearTimeout(timeout);window.removeEventListener('message',receive);if(event.data.error)reject(Error(event.data.error));else resolve(event.data.state);}
  window.addEventListener('message',receive);frame.contentWindow.postMessage({type:'myst-state-request',id,action,state},'*');
 });
 const controls=()=>[...document.querySelectorAll('.slides input,.slides select')];
 async function capture(){
  const reveal=R.getState();
  const python=await Promise.all(frames().map(f=>request(f,'capture')));
  return {reveal,python,values:controls().map(e=>e.value),terms:[...document.querySelectorAll('.linked-explanation')].map(e=>e.dataset.selectedTerm),details:[...document.querySelectorAll('.slides details')].map(e=>e.open),media:[...document.querySelectorAll('.slides video,.slides audio')].map(e=>e.currentTime)};
 }
 async function restore(state){
  await Promise.all(frames().map(f=>request(f,'capture')));
  await Promise.all(frames().map((f,i)=>request(f,'restore',state.python[i])));
  controls().forEach((e,i)=>{e.value=state.values[i];e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));});
  document.querySelectorAll('.linked-explanation').forEach((e,i)=>e.querySelector(`[data-term="${state.terms[i]}"]`)?.click());
  document.querySelectorAll('.slides details').forEach((e,i)=>e.open=state.details[i]);
  document.querySelectorAll('.slides video,.slides audio').forEach((e,i)=>{e.pause();if(Number.isFinite(e.duration))e.currentTime=Math.min(state.media[i],e.duration);});
  R.setState(state.reveal);focusSlide();window.fitCurrentSlide?.();
 }
 const replay=[...document.querySelectorAll('.slide-replay')],paths=[...document.querySelectorAll('.explanation-paths')];
 let steps=[],cursor=-1,exploration=null,branches=[],busy=false;
 const message=text=>replay.forEach(e=>e.querySelector('output').textContent=text);
 const run=async(fn,where)=>{if(busy)return;busy=true;try{await fn();}catch(error){where(error.message);}finally{busy=false;}};
 replay.forEach(group=>group.querySelectorAll('[data-replay]').forEach(button=>button.onclick=()=>run(async()=>{
  switch(button.dataset.replay){
   case 'save':if(steps.length>=20)throw Error('Replay is limited to 20 saved states. Clear it to start again.');steps.push(await capture());message(`Saved step ${steps.length}.`);break;
   case 'start':if(!steps.length)throw Error('Save a step first.');if(!exploration)exploration=await capture();cursor=0;await restore(steps[0]);message(`Replaying step 1 of ${steps.length}.`);break;
   case 'next':if(cursor<0)throw Error('Start replay first.');if(cursor+1>=steps.length){message('Last saved step. Return to exploration when ready.');break;}await restore(steps[++cursor]);message(`Replaying step ${cursor+1} of ${steps.length}.`);break;
   case 'return':if(!exploration)throw Error('No interrupted exploration to return to.');await restore(exploration);exploration=null;cursor=-1;message('Returned to exploration.');break;
   case 'clear':steps=[];cursor=-1;exploration=null;message('Saved steps cleared.');break;
  }
 },message)));
 const branchMessage=text=>paths.forEach(e=>e.querySelector('output').textContent=text);
 const returnButtons=()=>document.querySelectorAll('[data-detour-return]').forEach(b=>b.hidden=!branches.length);
 paths.forEach(group=>{
  const select=group.querySelector('select');select.onchange=()=>group.querySelectorAll('[data-audience]').forEach(a=>a.hidden=select.value!=='all'&&a.dataset.audience!==select.value);
  group.querySelectorAll('[data-detour]').forEach(link=>link.onclick=event=>{event.preventDefault();event.stopImmediatePropagation();run(async()=>{if(branches.length>=12)throw Error('Return stack is full; return before opening another detour.');const snapshot=await capture();branches.push(snapshot);const target=document.getElementById(link.dataset.detour),{h,v}=R.getIndices(target);R.slide(h,v,-1);focusSlide();returnButtons();branchMessage(`Detour depth ${branches.length}. Return restores your previous state.`);},branchMessage);});
  group.querySelector('[data-detour-return]').onclick=()=>run(async()=>{if(!branches.length)return;await restore(branches.at(-1));branches.pop();returnButtons();branchMessage(branches.length?`Detour depth ${branches.length}.`:'Returned to the main explanation.');},branchMessage);
 });
 // Evidence opens in a focused drawer; handouts retain native expanded details.
 document.querySelectorAll('.slide-evidence').forEach(details=>{
  const summary=details.querySelector('summary');summary.onclick=event=>{
   event.preventDefault();const dialog=document.createElement('dialog');dialog.className='evidence-drawer';dialog.setAttribute('aria-label',summary.textContent);
   const close=document.createElement('button');close.textContent='Close evidence';close.onclick=()=>dialog.close();dialog.append(close);
   [...details.children].filter(e=>e!==summary).forEach(e=>dialog.append(e.cloneNode(true)));
   const keyboard=R.getConfig().keyboard;R.configure({keyboard:false});dialog.onclose=()=>{R.configure({keyboard});dialog.remove();summary.focus();};document.body.append(dialog);dialog.showModal();
  };
 });
};
