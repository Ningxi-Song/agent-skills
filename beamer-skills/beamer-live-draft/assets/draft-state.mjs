export function loadState(store, key) {
  try {
    const state = JSON.parse(store.getItem(key));
    return state
      && Array.isArray(state.slides)
      && typeof state.template === 'string'
      && Number.isInteger(state.active)
      ? state
      : null;
  } catch {
    return null;
  }
}

export function saveState(store, key, state) {
  store.setItem(key, JSON.stringify(state));
}
