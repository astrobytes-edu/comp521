/** Selection is shared by rendering and the source manifest. */
export function selectSlides(slides, settings = {}) {
  const include = settings.includeTags;
  if (include !== undefined && (!Array.isArray(include) || include.some(t => typeof t !== 'string'))) throw new Error('includeTags must be a list of strings.');
  return slides.filter(slide => {
    const tags = slide.options?.tags || [];
    if (!Array.isArray(tags) || tags.some(t => typeof t !== 'string')) throw new Error('Slide tags must be a list of strings.');
    return !include || !tags.length || tags.some(t => include.includes(t));
  });
}
