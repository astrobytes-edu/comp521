/** Authoring extensions. Content stays as ordinary MyST nodes until export. */
function container(name, className, options = {}) {
  return {
    name,
    body: { type: String, required: true },
    options,
    run(data, _file, context) {
      return [{ type: 'div', class: className, reveal: data.options || {}, children: context.parseMyst(data.body).children }];
    },
  };
}

export default {
  name: 'MyST Reveal authoring',
  directives: [
    container('slide-evidence', 'slide-evidence', { title: { type: String }, claim: { type: String, required: true }, status: { type: String, required: true } }),
    { name: 'slide-explanation', body: {type: String, required: true}, run(data) { return [{type:'div',class:'slide-explanation',reveal:JSON.parse(data.body),children:[]}]; } },
    { name: 'slide-paths', body: {type: String, required: true}, run(data) { return [{type:'div',class:'slide-paths',reveal:JSON.parse(data.body),children:[]}]; } },
    { name: 'slide-replay', run() { return [{type:'div',class:'slide-replay',children:[]}]; } },
    container('fragment', 'fragment', { effect: { type: String }, index: { type: Number } }),
    container('speaker-note', 'myst-reveal-notes'),
    container('slide-columns', 'myst-reveal-columns', { ratio: { type: String }, gap: { type: Number }, align: { type: String } }),
    container('slide-column', 'myst-reveal-column'),
    container('slide-element', 'myst-reveal-element', { id: { type: String }, style: { type: String }, class: { type: String } }),
    container('slide-incremental', 'myst-reveal-incremental'),
    container('slide-stack', 'r-stack'),
    {
      name: 'slide-options',
      body: { type: String, required: true },
      run(data) {
        // JSON uses Reveal's existing attribute vocabulary, rather than a second schema.
        const options = JSON.parse(data.body);
        return [{ type: 'div', class: 'myst-reveal-options', reveal: options, children: [] }];
      },
    },
    {
      name: 'slide-code', arg: { type: String }, body: { type: String, required: true },
      options: { lines: { type: String }, id: { type: String }, start: { type: Number }, title: { type: String }, steps: { type: String } },
      run(data) { return [{ type: 'code', lang: data.arg || 'text', value: data.body, reveal: data.options || {} }]; },
    },
    {
      name: 'slide-media', arg: { type: String, required: true },
      options: { kind: { type: String }, title: { type: String, required: true },
        poster: { type: String }, captions: { type: String }, muted: { type: Boolean },
        loop: { type: Boolean }, autoplay: { type: Boolean } },
      run(data) { return [{ type: 'div', class: 'myst-reveal-media', reveal: { ...data.options, src: data.arg }, children: [] }]; },
    },
    {
      name: 'slide-embed', arg: { type: String, required: true },
      options: { title: { type: String, required: true }, fallback: { type: String }, alt: { type: String } },
      run(data) { return [{ type: 'div', class: 'myst-reveal-embed', reveal: { src: data.arg, ...data.options }, children: [] }]; },
    },
    {
      name: 'slide-python', body: { type: String, required: true },
      options: { packages: { type: String }, alt: { type: String }, fallback: { type: String }, parameters: { type: String }, trace: { type: Boolean } },
      run(data) { return [{ type: 'div', class: 'myst-reveal-python', reveal: { source: data.body, ...data.options }, children: [] }]; },
    },
    container('slide-question', 'slide-question', { title: { type: String } }),
    container('slide-answer', 'slide-answer', { title: { type: String }, index: { type: Number } }),
    container('slide-worked', 'slide-worked', { title: { type: String } }),
    container('slide-step', 'slide-step', { title: { type: String }, index: { type: Number } }),
    container('slide-panel', 'slide-panel', { title: { type: String }, index: { type: Number } }),
    {
      name: 'slide-timer', arg: { type: Number, required: true },
      options: { title: { type: String } },
      run(data) { return [{ type: 'div', class: 'slide-timer', reveal: { seconds: data.arg, ...data.options }, children: [] }]; },
    },
    {
      name: 'slide-code-example', arg: { type: String, required: true },
      options: { title: { type: String }, lines: { type: String }, steps: { type: String }, view: { type: String }, alt: { type: String } },
      run(data) { return [{ type: 'div', class: 'slide-code-example', reveal: { source: data.arg, ...data.options }, children: [] }]; },
    },
    {
      name: 'slide-figure', arg: { type: String, required: true }, body: { type: String },
      options: { alt: { type: String, required: true }, caption: { type: String }, focus: { type: String }, title: { type: String } },
      run(data) { return [{ type: 'div', class: 'slide-scientific-figure', reveal: { source: data.arg, ...data.options, annotations: data.body ? JSON.parse(data.body) : [] }, children: [] }]; },
    },
    {
      name: 'slide-linked-plot', arg: { type: String, required: true },
      options: { title: { type: String, required: true } },
      run(data) { return [{ type: 'div', class: 'slide-linked-plot', reveal: { source: data.arg, ...data.options }, children: [] }]; },
    },
    {
      name: 'slide-image-compare', body: { type: String, required: true },
      run(data) { return [{ type: 'div', class: 'slide-image-compare', reveal: JSON.parse(data.body), children: [] }]; },
    },
    {
      name: 'slide-movies', body: { type: String, required: true },
      run(data) { return [{ type: 'div', class: 'slide-movies', reveal: JSON.parse(data.body), children: [] }]; },
    },
    {
      name: 'slide-bibliography',
      run() { return [{ type: 'div', class: 'myst-reveal-bibliography', children: [] }]; },
    },
  ],
};
