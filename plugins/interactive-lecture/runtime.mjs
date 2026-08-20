import { mountTransitDepthFigure } from "./transit-depth-figure.mjs";

const STYLE_ID = "comp521-lecture-runtime";
const STYLE = `
.comp521-lecture-static{margin:1.25rem 0;padding:1rem 1.1rem;border:1px solid #c8d7df;border-radius:.75rem;background:#fff;color:#172b3a}
.comp521-lecture-runtime{margin:1.25rem 0;border-radius:1rem;border:1px solid #b7d5d3;background:#f7fffe;color:#102a2c;overflow:hidden}
.comp521-lecture-runtime__head{padding:1rem 1.25rem;background:#073447;color:white;display:flex;justify-content:space-between;gap:1rem;align-items:center}.comp521-lecture-runtime__body{padding:1.25rem}
.comp521-lecture-runtime button{font:inherit;font-weight:650;border:1px solid #0c6f72;border-radius:.5rem;background:#fff;color:#075f63;padding:.5rem .75rem;cursor:pointer}.comp521-lecture-runtime button:hover{background:#e9f8f6}.comp521-lecture-runtime textarea{box-sizing:border-box;width:100%;min-height:7rem;font:inherit;padding:.65rem;border:1px solid #92bbb9;border-radius:.5rem}.comp521-lecture-runtime__status{font-size:.88rem;color:#426165;margin-top:.5rem}
@media (prefers-reduced-motion:reduce){.comp521-lecture-runtime *{transition:none!important;scroll-behavior:auto!important}}`;

function addStyle(root) { if (!root.querySelector?.(`#${STYLE_ID}`)) { const s=document.createElement("style");s.id=STYLE_ID;s.textContent=STYLE;root.append(s); } }
function key(model) { return `comp521:lecture:${model.get("pageSlug")}:${model.get("id")}`; }
function download(text, name) { const url=URL.createObjectURL(new Blob([text],{type:"text/plain;charset=utf-8"})); const a=document.createElement("a");a.href=url;a.download=name;a.click();URL.revokeObjectURL(url); }
export function presentationEnabled() { return new URLSearchParams(location.search).get("lecture") === "presentation"; }
export function mountLecture(model, el) {
  addStyle(el.getRootNode()); const options=model.get("options")||{}; const id=model.get("id")||"lecture"; const staticBlock=document.querySelector(`.lecture-id-${CSS.escape(id)}`); if (staticBlock && model.get("kind")!=="lecture-reveal") staticBlock.hidden=true;
  const wrap=document.createElement("section");wrap.className="comp521-lecture-runtime";wrap.dataset.kind=model.get("kind"); const head=document.createElement("div");head.className="comp521-lecture-runtime__head";head.innerHTML=`<strong>${options.label||options.title||model.get("kind")}</strong><span>${presentationEnabled()?"Presenter mode":"Student mode"}</span>`;const body=document.createElement("div");body.className="comp521-lecture-runtime__body";wrap.append(head,body);
  const kind=model.get("kind");
  if (["lecture-write","lecture-checkpoint","lecture-predict"].includes(kind)) { const prompt=document.createElement("p");prompt.textContent=options.prompt||"Write your reasoning.";const area=document.createElement("textarea");area.setAttribute("aria-label",prompt.textContent);try{area.value=localStorage.getItem(key(model))||"";}catch{}area.addEventListener("input",()=>{try{localStorage.setItem(key(model),area.value);}catch{}});const controls=document.createElement("p");for(const [label,fn] of [["Copy",async()=>navigator.clipboard?.writeText(area.value)],["Download",()=>download(`${prompt.textContent}\n\n${area.value}\n`,`${id}.txt`)],["Clear",()=>{area.value="";try{localStorage.removeItem(key(model));}catch{}}]]){const b=document.createElement("button");b.type="button";b.textContent=label;b.onclick=fn;controls.append(b);}body.append(prompt,area,controls); }
  else if(kind==="lecture-reveal"){const b=document.createElement("button");b.type="button";b.textContent="Reveal reasoning";b.setAttribute("aria-expanded","false");if(staticBlock){staticBlock.hidden=true;b.onclick=()=>{staticBlock.hidden=!staticBlock.hidden;b.textContent=staticBlock.hidden?"Reveal reasoning":"Hide reasoning";b.setAttribute("aria-expanded",String(!staticBlock.hidden));};}body.append(b);}
  else if(kind==="lecture-figure" && options.model==="transit-depth"){mountTransitDepthFigure(body);}
  else { body.textContent=model.get("body")||options.fallback||"Continue to the next activity."; }
  el.replaceChildren(wrap);
}
