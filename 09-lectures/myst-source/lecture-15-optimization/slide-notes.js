window.OptimizationSlideNotes = {
  id: 'optimization-slide-notes',

  init(deck) {
    const dialog = document.createElement('dialog');
    dialog.className = 'optimization-slide-notes';
    dialog.setAttribute('aria-labelledby', 'optimization-notes-heading');
    dialog.innerHTML = `
      <form method="dialog">
        <h2 id="optimization-notes-heading">Speaker notes</h2>
        <button type="submit" autofocus>Close</button>
      </form>
      <div class="optimization-notes-content"></div>`;
    document.body.append(dialog);

    const revealNotes = deck.getPlugin('notes');
    const openNative = revealNotes.open;
    let keyboard;
    let opener;
    const open = () => {
      if (dialog.open) return;
      const slide = deck.getCurrentSlide();
      const notes = slide?.querySelector('aside.notes');
      if (!notes) return;
      const title = slide.querySelector('h2')?.textContent;
      dialog.querySelector('h2').textContent = title ? `Speaker notes · ${title}` : 'Speaker notes';
      dialog.querySelector('.optimization-notes-content').replaceChildren(
        ...Array.from(notes.childNodes, node => node.cloneNode(true)),
      );
      opener = document.activeElement;
      keyboard = deck.getConfig().keyboard;
      deck.configure({ keyboard: false });
      dialog.showModal();
    };
    dialog.addEventListener('close', () => {
      deck.configure({ keyboard });
      // The presentation toolbar collapses its popover after a menu action.
      opener?.closest('.tools-popover')?.closest('.deck-tools')?.querySelector('.tools-toggle')?.focus();
    });
    revealNotes.open = open;
    deck.addKeyBinding({ keyCode: 83, key: 'S', description: 'Open speaker notes' }, open);
    this.cleanup = () => {
      if (dialog.open) dialog.close();
      dialog.remove();
      revealNotes.open = openNative;
      deck.removeKeyBinding(83);
    };
  },

  destroy() {
    this.cleanup?.();
  },
};
