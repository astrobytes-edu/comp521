/* Optional teaching and talk tools, using Reveal's navigation and clock state. */
window.setupAdvanced = function(settings, printing) {
  const R = window.Reveal;
  window.setupExploration?.(printing);
  window.slideFitReports = {};
  const fit = () => {
    const slide = R.getCurrentSlide(); if (!slide || printing) return;
    slide.style.fontSize = ''; slide.style.removeProperty('--figure-height');
    const base = parseFloat(getComputedStyle(slide).fontSize), min = Math.min(base,Number(slide.dataset.minFont || 26));
    const measure = () => {
      const rect = slide.getBoundingClientRect(), scale = R.getScale();
      let bottom=0,right=0;
      for (const el of slide.querySelectorAll('*')) {
        if(el.closest('details:not([open])') && !el.closest('summary'))continue;
        if((el instanceof SVGElement && el.tagName.toLowerCase() !== 'svg') || el.closest('aside.notes') || !el.getClientRects().length || getComputedStyle(el).position === 'absolute')continue;
        const r=el.getBoundingClientRect();bottom=Math.max(bottom,(r.bottom-rect.top)/scale);right=Math.max(right,(r.right-rect.left)/scale);
      }
      return {height:Math.max(slide.scrollHeight,bottom),width:Math.max(slide.scrollWidth,right)};
    };
    const height=R.getConfig().height,width=R.getConfig().width;
    let size=base,bounds=measure();
    const media=slide.querySelector('.scientific-figure');
    if(media && bounds.height>height+2){const current=parseFloat(getComputedStyle(slide).getPropertyValue('--figure-height'))||360;slide.style.setProperty('--figure-height',Math.max(220,current-(bounds.height-height)-8)+'px');bounds=measure();}
    if(slide.dataset.fit==='bounded') {
      while ((bounds.height>height+2 || bounds.width>width+2) && size>min) { size=Math.max(min,size-1);slide.style.fontSize=size+'px';bounds=measure(); }
    }
    window.slideFitReports[slide.id]={...bounds,fontSize:size,baseFontSize:base,minimum:min,overflow:bounds.height>height+2 || bounds.width>width+2};
    document.querySelector('.fit-warning')?.remove();
    if(window.slideFitReports[slide.id].overflow && new URLSearchParams(location.search).has('review')) {
      const warning=document.createElement('div');warning.className='fit-warning';warning.setAttribute('role','status');warning.textContent='Slide exceeds available space. Split content or revise the layout.';document.body.append(warning);
    }
  };
  window.fitCurrentSlide=fit;R.on('slidechanged',()=>requestAnimationFrame(fit));R.on('fragmentshown',()=>requestAnimationFrame(fit));R.on('fragmenthidden',()=>requestAnimationFrame(fit));window.addEventListener('resize',()=>requestAnimationFrame(fit));document.fonts.ready.then(fit);
  document.querySelectorAll('.reveal img').forEach(img=>img.addEventListener('load',fit));
  document.querySelectorAll('.image-comparison').forEach(group=>{
    const slider=group.querySelector('input'),images=group.querySelector('.comparison-images');
    if(!printing)slider.oninput=()=>{images.classList.add('blending');images.style.setProperty('--blend',slider.value/100);};
  });
  document.querySelectorAll('.synced-movies').forEach(group=>{
    const videos=[...group.querySelectorAll('video')],slider=group.querySelector('input'),output=group.querySelector('output');
    if(printing){videos.forEach(v=>{v.removeAttribute('src');v.load();});return;}
    let playing=false;
    const pause=()=>{playing=false;videos.forEach(v=>v.pause());};
    const duration=()=>Math.min(...videos.map(v=>Number.isFinite(v.duration)?v.duration:0));
    const seek=value=>{pause();videos.forEach(v=>v.currentTime=value);slider.value=value;output.textContent=value.toFixed(2)+' s';};
    videos.forEach(v=>{v.addEventListener('loadedmetadata',()=>{slider.max=duration()||1;});v.addEventListener('error',()=>{pause();output.textContent='Video unavailable; use the poster or check its format.';});});
    group.querySelector('[data-movie=play]').onclick=async()=>{try{await Promise.all(videos.map(v=>v.play()));playing=true;output.textContent='Playing';}catch{pause();output.textContent='Playback unavailable; use the poster.';}};
    group.querySelector('[data-movie=pause]').onclick=()=>{pause();output.textContent='Paused';};group.querySelector('[data-movie=reset]').onclick=()=>seek(0);slider.oninput=()=>seek(Number(slider.value));slider.onkeydown=e=>e.stopPropagation();
    videos[0].addEventListener('timeupdate',()=>{if(!playing)return;const t=videos[0].currentTime;if(t>=duration()){seek(0);return;}videos.slice(1).forEach(v=>{if(Math.abs(v.currentTime-t)>.08)v.currentTime=t;});slider.value=t;output.textContent=t.toFixed(2)+' s';});
    R.on('slidechanged',()=>{if(!R.getCurrentSlide().contains(group))pause();});
  });
  if(printing || window.self!==window.top)return;
  // Toolbar is created by the main runtime immediately after this callback.
  queueMicrotask(()=>{
    const bar=document.querySelector('.deck-tools');if(!bar)return;
    const add=(label,action)=>{const button=document.createElement('button');button.type='button';button.textContent=label;button.onclick=action;bar.append(button);return button;};
    const toggle=add('Tools',()=>{const closed=bar.classList.toggle('tools-collapsed');toggle.setAttribute('aria-expanded',String(!closed));});toggle.className='tools-toggle';toggle.setAttribute('aria-expanded','false');bar.prepend(toggle);bar.classList.add('tools-collapsed');
    const themeKey='myst-reveal-theme:'+location.pathname;
    let theme=document.body.classList.contains('theme-dark')?'dark':'light';
    try { const saved=localStorage.getItem(themeKey);if(saved==='dark'||saved==='light')theme=saved; } catch { /* Storage may be unavailable for standalone files. */ }
    const sendTheme=frame=>frame.contentWindow?.postMessage({type:'myst-reveal-theme',theme},'*');
    const themeButton=add('Dark mode',()=>{theme=theme==='dark'?'light':'dark';applyTheme();try{localStorage.setItem(themeKey,theme);}catch{/* Keep the toggle usable without storage. */}});
    themeButton.setAttribute('aria-label','Dark mode');
    function applyTheme(){document.body.classList.toggle('theme-dark',theme==='dark');document.body.classList.toggle('theme-light',theme==='light');document.documentElement.style.colorScheme=theme;themeButton.setAttribute('aria-pressed',String(theme==='dark'));themeButton.dataset.tooltip=theme==='dark'?'Dark mode: on':'Dark mode: off';document.querySelectorAll('iframe.python-embed').forEach(sendTheme);}
    document.querySelectorAll('iframe.python-embed').forEach(frame=>frame.addEventListener('load',()=>sendTheme(frame)));
    window.addEventListener('message',event=>{if(event.data?.type!=='myst-reveal-theme-ready')return;const frame=[...document.querySelectorAll('iframe.python-embed')].find(f=>f.contentWindow===event.source);if(frame)sendTheme(frame);});
    applyTheme();
    const backups=R.getSlides().filter(s=>s.dataset.backup==='true');let returnState;
    const back=add('Return to talk',()=>{if(returnState){R.setState(returnState);returnState=null;back.hidden=true;}});back.hidden=true;
    if(backups.length)add('Backups',()=>{
      const dialog=document.createElement('dialog');dialog.className='slide-menu';dialog.setAttribute('aria-label','Backup slides');const close=document.createElement('button');close.textContent='Close';close.onclick=()=>dialog.close();dialog.append(close);
      const keyboard=R.getConfig().keyboard;R.configure({keyboard:false});dialog.onclose=()=>{R.configure({keyboard});dialog.remove();};
      backups.forEach(slide=>{const b=document.createElement('button');b.textContent=slide.querySelector('h2')?.textContent||slide.id;b.onclick=()=>{if(!returnState)returnState=R.getState();const {h,v}=R.getIndices(slide);dialog.close();R.slide(h,v);back.hidden=false;};const p=document.createElement('p');p.append(b);dialog.append(p);});document.body.append(dialog);dialog.showModal();
    });
    const panel=document.createElement('aside');panel.className='rehearsal-panel';panel.hidden=true;panel.setAttribute('aria-label','Rehearsal');
    const clock=document.createElement('output');clock.setAttribute('aria-live','off');panel.append(clock);
    let running=false,started=0,total=0,current=R.getCurrentSlide().id,rows=[],slideStarted=0,slideElapsed=0;
    const record=()=>{if(!running)return;const now=performance.now(),seconds=(now-slideStarted)/1000;rows.push({slideId:current,seconds});slideElapsed+=seconds;total+=now-started;started=now;slideStarted=now;};
    const action=(label,fn)=>{const b=document.createElement('button');b.textContent=label;b.onclick=fn;panel.append(b);return b;};
    const start=action('Start',()=>{if(running){record();running=false;start.textContent='Resume';}else{running=true;started=slideStarted=performance.now();start.textContent='Pause';}});
    action('Reset',()=>{running=false;total=0;rows=[];slideElapsed=0;start.textContent='Start';});
    action('Download timings',()=>{record();const blob=new Blob([JSON.stringify({version:1,deck:document.title,variant:settings.variant||null,records:rows,totalSeconds:total/1000},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='rehearsal.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
    action('Close',()=>panel.hidden=true);document.body.append(panel);add('Rehearse',()=>panel.hidden=!panel.hidden);
    R.on('slidechanged',()=>{record();current=R.getCurrentSlide().id;slideElapsed=0;slideStarted=performance.now();});
    // Original stroke icons: inline SVG keeps the exported deck self-contained.
    const icons={
      'Tools':'<path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="3"/><circle cx="15" cy="17" r="3"/>',
      'Slides':'<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
      'Notes':'<path d="M5 3h10l4 4v14H5zM14 3v5h5M8 12h8M8 16h6"/>',
      'Search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
      'Overview':'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
      'Pointer':'<circle cx="12" cy="12" r="5"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',
      'Handout':'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
      'Dark mode':'<path d="M20 15A9 9 0 0 1 9 4a9 9 0 1 0 11 11Z"/>',
      'Return to talk':'<path d="m9 5-6 6 6 6M3 11h12a5 5 0 0 1 0 10"/>',
      'Backups':'<path d="m3 8 9-5 9 5-9 5zM3 12l9 5 9-5M3 16l9 5 9-5"/>',
      'Rehearse':'<circle cx="12" cy="13" r="8"/><path d="M9 2h6M12 5V2M12 9v5l3 2"/>'
    };
    const popover=document.createElement('div');popover.className='tools-popover';popover.id='presentation-tools-popover';popover.setAttribute('role','group');popover.setAttribute('aria-label','Slide actions');
    for(const control of [...bar.children]){
      const label=control.getAttribute('aria-label')||control.textContent;
      control.setAttribute('aria-label',label);control.dataset.tooltip ||= label;
      control.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+icons[label]+'</svg>';
      if(control!==toggle)popover.append(control);
    }
    bar.append(popover);toggle.setAttribute('aria-controls',popover.id);
    const closeTools=(restore=false)=>{bar.classList.add('tools-collapsed');toggle.setAttribute('aria-expanded','false');if(restore)toggle.focus();};
    popover.addEventListener('click',event=>{if(event.target.closest('button,a')){const focusInside=popover.contains(document.activeElement);closeTools(focusInside);}});
    document.addEventListener('pointerdown',event=>{if(!bar.contains(event.target))closeTools();},true);
    document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!bar.classList.contains('tools-collapsed')){event.preventDefault();event.stopImmediatePropagation();closeTools(true);}},true);
    bar.addEventListener('focusout',()=>setTimeout(()=>{if(!bar.contains(document.activeElement))closeTools();},0));
    const tick=setInterval(()=>{if(!panel.isConnected){clearInterval(tick);return;}const elapsed=(total+(running?performance.now()-started:0))/1000,target=Number(R.getCurrentSlide().dataset.timing||settings.reveal.defaultTiming||90),onSlide=slideElapsed+(running?(performance.now()-slideStarted)/1000:0);clock.textContent=`Total ${Math.floor(elapsed/60)}:${String(Math.floor(elapsed%60)).padStart(2,'0')} · Slide ${Math.floor(onSlide)} / ${target} s`;clock.dataset.late=String(onSlide>target);},250);
  });
};
