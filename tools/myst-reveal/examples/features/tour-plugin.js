/* Minimal self-contained Reveal extension fixture. */
window.RevealTourPlugin = {
  id: 'tour-example',
  init(deck) { deck.getRevealElement().dataset.extension = 'loaded'; },
};
