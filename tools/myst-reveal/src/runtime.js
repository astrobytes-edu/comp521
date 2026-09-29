/* Browser behavior shared by every deck. Reveal owns presentation state. */
(() => {
  const settings = window.mystRevealSettings;
  const printing = new URLSearchParams(location.search).has('print-pdf');
  if (printing) {
    document.querySelectorAll('video:not(.synced-movies video), audio').forEach(media => {
      const replacement = document.createElement('p'); replacement.className = 'print-embed';
      replacement.textContent = `${media.getAttribute('aria-label') || 'Media'}. Playback is available in the HTML deck.`;
      media.pause(); media.removeAttribute('src'); media.load(); media.replaceWith(replacement);
    });
    document.querySelectorAll('[data-background-video]').forEach(slide => {
      slide.removeAttribute('data-background-video');
      slide.removeAttribute('data-background-video-loop');
      slide.removeAttribute('data-background-video-muted');
    });
    document.querySelectorAll('iframe').forEach(frame => {
      if (frame.dataset.hasFallback) { frame.remove(); return; }
      const replacement = document.createElement('div'); replacement.className = 'print-embed';
      const parsed = new DOMParser().parseFromString(frame.srcdoc, 'text/html');
      if (frame.classList.contains('output-embed') && !parsed.querySelector('script, iframe, object, embed')) {
        replacement.append(...parsed.body.childNodes);
      } else replacement.textContent = `${frame.title}. Interactive controls are available in the HTML deck.`;
      frame.replaceWith(replacement);
    });
    document.querySelectorAll('[data-background-iframe]').forEach(slide => {
      slide.removeAttribute('data-background-iframe');
      slide.removeAttribute('data-background-interactive');
      const fallback = document.createElement('p'); fallback.className = 'print-embed';
      fallback.textContent = 'The interactive background is available in the HTML deck.';
      slide.append(fallback);
    });
  }
  // Reveal splits background-video on commas; a data URI contains a comma.
  // Object URLs preserve a single offline source without changing Reveal itself.
  if (!printing) {
    const urls = [];
    document.querySelectorAll('[data-background-video]').forEach(slide => {
      const source = slide.getAttribute('data-background-video');
      const match = /^data:([^;]+);base64,(.*)$/.exec(source);
      if (!match) return;
      const bytes = Uint8Array.from(atob(match[2]), character => character.charCodeAt(0));
      const url = URL.createObjectURL(new Blob([bytes], { type: match[1] }));
      urls.push(url); slide.setAttribute('data-background-video', url);
    });
    window.addEventListener('pagehide', event => { if (!event.persisted) urls.forEach(url => URL.revokeObjectURL(url)); });
  }
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealOptions = { ...settings.reveal };
  if (reducedMotion) Object.assign(revealOptions, { transition: 'none', backgroundTransition: 'none', autoAnimate: false });
  document.querySelectorAll('.myst-reveal-incremental > ul > li, .myst-reveal-incremental > ol > li').forEach(li => li.classList.add('fragment'));

  // Generate real tab semantics from MyST tab-set nodes.
  document.querySelectorAll('.slide-tabs').forEach((set, setIndex) => {
    const items = [...set.querySelectorAll(':scope > .slide-tab')];
    const list = document.createElement('div');
    list.setAttribute('role', 'tablist');
    list.setAttribute('aria-label', 'Slide examples');
    const tabs = [], panels = [];
    items.forEach((item, i) => {
      const tab = item.querySelector('.slide-tab-label');
      const panel = item.querySelector('.slide-tab-content');
      if (!tab || !panel) return;
      tab.id = `tab-${setIndex}-${i}`;
      panel.id = `panel-${setIndex}-${i}`;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      tabs.push(tab); panels.push(panel); list.append(tab);
    });
    const select = i => {
      tabs.forEach((tab, j) => { tab.setAttribute('aria-selected', String(i === j)); tab.tabIndex = i === j ? 0 : -1; panels[j].hidden = i !== j; });
      if (Reveal.isReady()) Reveal.layout();
    };
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(i));
      tab.addEventListener('keydown', event => {
        const next = { ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1 }[event.key];
        if (next !== undefined) { event.preventDefault(); event.stopPropagation(); select(next); tabs[next].focus(); }
      });
    });
    set.prepend(list);
    select(0);
  });

  function setupComponents() {
    const updateCode = () => document.querySelectorAll('.code-card[data-code-steps]').forEach(card => {
      const codes = [...card.querySelectorAll('pre code')];
      const current = codes.findIndex(code => code.classList.contains('current-fragment'));
      card.querySelectorAll('[data-code-step]').forEach((item, i) => { item.hidden = !printing && i !== Math.max(0, current); });
    });
    updateCode(); Reveal.on('fragmentshown', updateCode); Reveal.on('fragmenthidden', updateCode); Reveal.on('slidechanged', updateCode);
    document.querySelectorAll('.code-copy').forEach(button => button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(button.closest('.code-card').dataset.codeSource);
        button.dataset.copied = 'true'; button.setAttribute('aria-label', 'Copied'); button.title = 'Copied';
        setTimeout(() => { delete button.dataset.copied; button.setAttribute('aria-label', 'Copy'); button.title = 'Copy code'; }, 2000);
      } catch { button.setAttribute('aria-label', 'Select code to copy'); button.title = 'Select code to copy'; }
    }));
    document.querySelectorAll('[data-footnote]').forEach(link => link.addEventListener('click', event => {
      event.preventDefault(); document.getElementById(link.dataset.footnote)?.focus();
    }));
    document.querySelectorAll('.exercise-timer').forEach(timer => {
      if (printing) return;
      const total = Number(timer.dataset.seconds), output = timer.querySelector('output'), start = timer.querySelector('[data-timer-action=start]');
      let remaining = total, until, interval;
      const draw = () => { output.textContent = `${Math.floor(remaining / 60)}:${String(remaining % 60).padStart(2, '0')}`; };
      const pause = () => { clearInterval(interval); interval = null; start.textContent = 'Start'; };
      start.addEventListener('click', () => {
        if (interval) { pause(); return; }
        if (remaining === 0) remaining = total;
        until = performance.now() + remaining * 1000; start.textContent = 'Pause';
        interval = setInterval(() => { remaining = Math.max(0, Math.ceil((until - performance.now()) / 1000)); draw(); if (!remaining) pause(); }, 100);
      });
      timer.querySelector('[data-timer-action=reset]').addEventListener('click', () => { pause(); remaining = total; draw(); });
      Reveal.on('slidechanged', () => { if (!Reveal.getCurrentSlide().contains(timer)) pause(); });
    });
    document.querySelectorAll('.linked-plot').forEach(plot => {
      const spec = JSON.parse(plot.dataset.plot), slider = plot.querySelector('input');
      const update = () => {
        const i = Number(slider.value), x = JSON.parse(plot.dataset.x)[i];
        plot.querySelectorAll('svg').forEach(svg => {
          const line = svg.querySelector('.plot-cursor'), dot = svg.querySelector('.plot-dot');
          line.setAttribute('x1', x); line.setAttribute('x2', x); dot.setAttribute('cx', x); dot.setAttribute('cy', JSON.parse(dot.dataset.y)[i]);
        });
        plot.querySelector('output').textContent = `${spec.xLabel || 'x'}: ${spec.x[i]}; ${spec.panels.map(p => `${p.label}: ${p.values[i].toPrecision(4)}`).join('; ')}`;
      };
      slider.addEventListener('input', update);
      slider.addEventListener('keydown', event => event.stopPropagation());
      plot.querySelector('.plot-reset').addEventListener('click', () => { slider.value = 0; update(); });
    });
    document.querySelectorAll('.figure-enlarge').forEach(button => button.addEventListener('click', () => {
      const dialog = document.createElement('dialog'); dialog.className = 'figure-dialog'; dialog.setAttribute('aria-label', 'Enlarged figure');
      const close = document.createElement('button'); close.textContent = 'Close'; close.addEventListener('click', () => dialog.close());
      const content = button.closest('figure').cloneNode(true); content.querySelector('.figure-enlarge')?.remove();
      content.querySelectorAll('[inert]').forEach(el => { el.inert = false; el.removeAttribute('aria-hidden'); });
      dialog.append(close, content); document.body.append(dialog);
      const keyboard = Reveal.getConfig().keyboard; Reveal.configure({ keyboard: false });
      dialog.addEventListener('close', () => { Reveal.configure({ keyboard }); dialog.remove(); button.focus(); });
      dialog.showModal();
    }));
  }

  Reveal.initialize({ ...revealOptions,
    plugins: [RevealHighlight, RevealNotes, RevealSearch, RevealZoom,
      ...settings.plugins.map(name => { if (!window[name]) throw new Error(`Missing Reveal plugin global: ${name}`); return window[name]; })],
  }).then(() => {
    const syncFragments = () => document.querySelectorAll('.fragment').forEach(el => {
      // Match Reveal's effect semantics immediately; computed opacity is still
      // interpolating when fragment events fire.
      const classes = el.classList;
      const visible = classes.contains('visible');
      const beginsVisible = [...classes].some(c => ['grow', 'shrink', 'strike', 'semi-fade-out'].includes(c) || c.startsWith('highlight-'));
      const currentOnly = classes.contains('current-visible') || classes.contains('fade-in-then-out');
      const hidden = classes.contains('fade-out') ? visible : currentOnly ? !classes.contains('current-fragment') : beginsVisible ? false : !visible;
      el.setAttribute('aria-hidden', String(hidden));
      el.inert = hidden;
    });
    Reveal.on('fragmentshown', syncFragments);
    Reveal.on('fragmenthidden', syncFragments);
    Reveal.on('slidechanged', syncFragments);
    syncFragments();
    setupComponents();
    const baseMaxScale = Reveal.getConfig().maxScale;
    const sizeInteractiveSlide = () => {
      // Chromium sandboxed iframes misroute pointer events when enlarged above
      // native size. Keep interactive slides at <=1 while retaining downscaling.
      const maxScale = Reveal.getCurrentSlide()?.querySelector('iframe') ? Math.min(1, baseMaxScale) : baseMaxScale;
      if (Reveal.getConfig().maxScale !== maxScale) Reveal.configure({ maxScale });
    };
    if (!printing) { sizeInteractiveSlide(); Reveal.on('slidechanged', sizeInteractiveSlide); }
    window.setupAdvanced?.(settings, printing);
    window.deckReady = true;
    if (printing || window.self !== window.top) return;

    const bar = document.createElement('nav');
    bar.className = 'deck-tools'; bar.setAttribute('aria-label', 'Presentation tools');
    document.body.append(bar);
    const button = (name, action) => {
      const el = document.createElement('button'); el.type = 'button'; el.textContent = name;
      el.addEventListener('click', action); bar.append(el); return el;
    };
    const dialog = document.createElement('dialog');
    dialog.className = 'slide-menu'; dialog.setAttribute('aria-label', 'Slide navigator');
    const close = document.createElement('button'); close.textContent = 'Close'; close.type = 'button';
    close.addEventListener('click', () => dialog.close()); dialog.append(close);
    const list = document.createElement('ol'); dialog.append(list);
    Reveal.getSlides().forEach((slide, i) => {
      const item = document.createElement('li'), jump = document.createElement('button');
      jump.type = 'button'; jump.textContent = `${i + 1}. ${slide.querySelector('h2')?.textContent || slide.id}`;
      jump.addEventListener('click', () => { const { h, v } = Reveal.getIndices(slide); dialog.close(); Reveal.slide(h, v); });
      item.append(jump); list.append(item);
    });
    document.body.append(dialog);
    let keyboard;
    dialog.addEventListener('close', () => Reveal.configure({ keyboard }));
    button('Slides', () => { keyboard = Reveal.getConfig().keyboard; Reveal.configure({ keyboard: false }); dialog.showModal(); });
    button('Notes', () => Reveal.getPlugin('notes').open());
    button('Search', () => Reveal.getPlugin('search').open());
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && event.target.matches('.searchinput')) {
        event.preventDefault(); event.stopImmediatePropagation();
        event.target.closest('.searchbox').style.display = 'none';
        event.target.blur();
      }
    }, true);
    button('Overview', () => Reveal.toggleOverview());
    const pointer = document.createElement('div'); pointer.className = 'laser-pointer'; pointer.hidden = true;
    pointer.setAttribute('aria-hidden', 'true'); document.body.append(pointer);
    const toggle = button('Pointer', () => { pointer.hidden = !pointer.hidden; toggle.setAttribute('aria-pressed', String(!pointer.hidden)); });
    toggle.setAttribute('aria-pressed', 'false');
    document.addEventListener('pointermove', e => { pointer.style.left = `${e.clientX}px`; pointer.style.top = `${e.clientY}px`; });
    if (settings.handout) {
      const link = document.createElement('a'); link.href = settings.handout; link.textContent = 'Handout'; bar.append(link);
    }
  });
})();
