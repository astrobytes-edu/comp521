function button(label, title) {
  const el = document.createElement("button");
  el.type = "button";
  el.title = title;
  el.setAttribute("aria-label", title);
  el.textContent = label;
  return el;
}

function activeAct(slides, currentIndex) {
  for (let index = currentIndex; index >= 0; index -= 1) {
    const title = slides[index].querySelector("h2")?.textContent.trim().replace("¶", "") || "";
    if (/^[IVX]+ · /.test(title)) return title;
  }
  return "Introduction";
}

export default {
  render({ el }) {
    const root = el.getRootNode();
    if (root.querySelector("#comp521-projector-controls-style")) return;
    const style = document.createElement("style");
    style.id = "comp521-projector-controls-style";
    style.textContent = `
      .projector-controls{position:fixed;z-index:50;right:1rem;bottom:1rem;display:flex;align-items:center;gap:.35rem;padding:.45rem;border:1px solid #79a8b0;border-radius:.65rem;background:color-mix(in srgb,#f7ffff 94%,transparent);box-shadow:0 .25rem 1.2rem #07344728;color:#073447;font:600 14px system-ui,sans-serif}
      .projector-controls button{min-width:2rem;padding:.35rem;border:1px solid #75a2aa;border-radius:.35rem;background:#fff;color:#073447;cursor:pointer;font:inherit}.projector-controls button:hover,.projector-controls button:focus{background:#e8f5f4;outline:2px solid transparent}.projector-controls__label{max-width:18rem;padding:0 .25rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
      html.lecture-high-contrast .projector-lecture{color:#000;background:#fff}html.lecture-high-contrast .projector-lecture h2{color:#000}html.lecture-high-contrast .projector-lecture pre{border:2px solid #000}
      @media print{.projector-controls{display:none}}
      @media (max-width:45rem){.projector-controls{left:.5rem;right:.5rem;bottom:.5rem;justify-content:center}.projector-controls__label{display:none}}
    `;
    root.append(style);
    const slides = [...document.querySelectorAll(".projector-lecture.projector-slide")];
    if (!slides.length) return;
    const sectionMode = slides.some((slide) => slide.classList.contains("lecture-scroll"));
    const unit = sectionMode ? "section" : "slide";
    const shell = document.createElement("nav");
    shell.className = "projector-controls";
    shell.setAttribute(
      "aria-label",
      sectionMode ? "Lecture section controls" : "Projector lecture controls",
    );
    const previous = button("←", `Previous ${unit} (Left Arrow or Page Up)`);
    const next = button("→", `Next ${unit} (Right Arrow, Space, or Page Down)`);
    const smaller = button("A−", "Decrease lecture font size");
    const larger = button("A+", "Increase lecture font size");
    const contrast = button("◐", "Toggle high contrast");
    const fullscreen = button("⛶", "Toggle full screen");
    const label = document.createElement("span");
    label.className = "projector-controls__label";
    shell.append(previous, next, label, smaller, larger, contrast, fullscreen);
    el.replaceChildren(shell);
    let currentIndex = 0;
    let scale = 1;
    function update(index) {
      currentIndex = Math.max(0, Math.min(slides.length - 1, index));
      label.textContent = `${currentIndex + 1}/${slides.length} · ${activeAct(slides, currentIndex)}`;
    }
    function go(index) {
      update(index);
      slides[currentIndex].scrollIntoView({ behavior: "smooth", block: "start" });
    }
    previous.addEventListener("click", () => go(currentIndex - 1));
    next.addEventListener("click", () => go(currentIndex + 1));
    smaller.addEventListener("click", () => {
      scale = Math.max(0.82, Number((scale - 0.06).toFixed(2)));
      document.documentElement.style.setProperty("--lecture-font-scale", scale);
    });
    larger.addEventListener("click", () => {
      scale = Math.min(1.24, Number((scale + 0.06).toFixed(2)));
      document.documentElement.style.setProperty("--lecture-font-scale", scale);
    });
    contrast.addEventListener("click", () => document.documentElement.classList.toggle("lecture-high-contrast"));
    fullscreen.addEventListener("click", async () => {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    });
    document.addEventListener("keydown", (event) => {
      if (event.defaultPrevented || /^(INPUT|TEXTAREA|SELECT)$/.test(event.target?.tagName || "")) return;
      if (["ArrowRight", "PageDown", " "].includes(event.key)) { event.preventDefault(); go(currentIndex + 1); }
      if (["ArrowLeft", "PageUp"].includes(event.key)) { event.preventDefault(); go(currentIndex - 1); }
    });
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) update(slides.indexOf(visible.target));
    }, { threshold: [0.45, 0.7] });
    slides.forEach((slide) => observer.observe(slide));
    update(0);
  },
};
