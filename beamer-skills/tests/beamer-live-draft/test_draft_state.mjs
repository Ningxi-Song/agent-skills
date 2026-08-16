import assert from 'node:assert/strict';
import {
  SCHEMA_VERSION,
  loadState,
  migrateState,
  saveStateAtomic,
} from '../../beamer-live-draft/assets/draft-state.mjs';

function memoryStore(initial = {}) {
  const values = new Map(Object.entries(initial));
  return {
    getItem: key => values.has(key) ? values.get(key) : null,
    setItem: (key, value) => values.set(key, value),
    removeItem: key => values.delete(key),
    values,
  };
}

const legacy = {
  template: 'clean',
  active: 0,
  slides: [{
    type: 'itemize',
    frametitle: 'Edited',
    items: ['manual text'],
    unknown: 7,
  }],
};

const migrated = migrateState(legacy, 'deck-a');
assert.equal(migrated.schemaVersion, SCHEMA_VERSION);
assert.equal(migrated.deckId, 'deck-a');
assert.equal(migrated.slides[0].components[0].items[0], 'manual text');
assert.equal(migrated.slides[0].legacy.unknown, 7);

const store = memoryStore({ deck: JSON.stringify(legacy) });
saveStateAtomic(store, 'deck', migrated);
assert.ok(store.values.has('deck:last-good'));
assert.deepEqual(JSON.parse(store.values.get('deck')), migrated);
assert.deepEqual(loadState(store, 'deck'), migrated);

const queryIndependent = new URL('http://localhost/editor/beamer-draft.html?rev=2');
assert.equal(queryIndependent.pathname, '/editor/beamer-draft.html');

console.log('draft-state preservation tests passed');
