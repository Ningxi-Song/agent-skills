export const SCHEMA_VERSION = 2;
export const COMPONENT_TYPES = new Set([
  'diagram', 'formula', 'table', 'figure', 'flow', 'rich-text',
]);

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function legacyComponents(slide, slideIndex) {
  const id = `slide-${slideIndex + 1}-component-1`;
  if (slide.type === 'title') {
    return [{ id, type: 'rich-text', role: 'title', title: slide.title ?? '', subtitle: slide.subtitle ?? '', author: slide.author ?? '', institute: slide.institute ?? '', date: slide.date ?? '' }];
  }
  if (slide.type === 'itemize') return [{ id, type: 'rich-text', items: clone(slide.items ?? []) }];
  if (slide.type === 'columns') return [{ id, type: 'rich-text', columns: [clone(slide.left ?? []), clone(slide.right ?? [])] }];
  if (slide.type === 'block') return [{ id, type: 'rich-text', blocktitle: slide.blocktitle ?? '', body: slide.body ?? '' }];
  throw new Error(`unsupported legacy slide type ${slide.type}`);
}

export function validateState(state) {
  if (!state || state.schemaVersion !== SCHEMA_VERSION || !Array.isArray(state.slides) || !state.slides.length) throw new Error('invalid draft state');
  if (typeof state.template !== 'string' || !Number.isInteger(state.active)) throw new Error('invalid draft metadata');
  for (const slide of state.slides) {
    if (!slide.id || !Array.isArray(slide.components)) throw new Error(`invalid slide ${slide.id ?? '<missing>'}`);
    for (const component of slide.components) {
      if (!component.id || !COMPONENT_TYPES.has(component.type)) throw new Error(`unsupported component ${component.type ?? '<missing>'}`);
      if (component.type === 'figure' && component.fullPageRaster) throw new Error('Full-page raster slides are prohibited');
    }
  }
  return state;
}

export function migrateState(input, deckId = 'default') {
  if (input?.schemaVersion === SCHEMA_VERSION) return validateState(clone(input));
  const known = new Set(['id', 'type', 'frametitle', 'title', 'subtitle', 'author', 'institute', 'date', 'items', 'left', 'right', 'blocktitle', 'body']);
  const slides = (input?.slides ?? []).map((slide, index) => ({
    id: slide.id ?? `slide-${index + 1}`,
    role: slide.type === 'title' ? 'title' : 'content',
    frametitle: slide.frametitle ?? '',
    components: legacyComponents(slide, index),
    legacy: Object.fromEntries(Object.entries(slide).filter(([key]) => !known.has(key))),
  }));
  return validateState({ schemaVersion: SCHEMA_VERSION, deckId, template: input?.template ?? 'clean', active: input?.active ?? 0, slides });
}

export function loadState(store, key, deckId = 'default') {
  try {
    const raw = store.getItem(key);
    if (raw === null) return null;
    return migrateState(JSON.parse(raw), deckId);
  } catch {
    const backup = store.getItem(`${key}:last-good`);
    if (backup === null) return null;
    try { return migrateState(JSON.parse(backup), deckId); } catch { return null; }
  }
}

export function saveStateAtomic(store, key, state) {
  const validated = validateState(clone(state));
  const previous = store.getItem(key);
  if (previous !== null) store.setItem(`${key}:last-good`, previous);
  const encoded = JSON.stringify(validated);
  store.setItem(`${key}:pending`, encoded);
  validateState(JSON.parse(store.getItem(`${key}:pending`)));
  store.setItem(key, encoded);
  if (typeof store.removeItem === 'function') store.removeItem(`${key}:pending`);
}

export const saveState = saveStateAtomic;
