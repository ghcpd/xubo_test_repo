const state = (() => {
  const s = {};
  for (let i = 1; i <= 7; i++) s[`day${i}`] = [];
  return s;
})();

const els = {};

async function loadCities() {
  const res = await fetch('cities.json');
  const data = await res.json();
  els.allCities = data;
  renderCityList(data);
}

function renderCityList(list) {
  els.cities.innerHTML = '';
  list.forEach((c, idx) => {
    const li = document.createElement('li');
    li.className = 'city-item';
    li.textContent = `${c.city} (${c.country})`;
    li.draggable = true;
    li.dataset.city = c.city;
    li.dataset.country = c.country;
    li.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', JSON.stringify({ city: c.city, country: c.country, type: 'new' }));
    });
    els.cities.appendChild(li);
  });
}

function initDayCards() {
  Object.keys(state).forEach((dKey) => {
    const card = document.createElement('div');
    card.className = 'card day-drop';

    const header = document.createElement('div');
    header.className = 'card-header';
    header.textContent = dKey.toUpperCase();
    header.addEventListener('click', () => card.classList.toggle('open'));

    const body = document.createElement('div');
    body.className = 'card-body';
    body.dataset.day = dKey;
    body.setAttribute('role', 'region');
    body.setAttribute('aria-label', `Drop area ${dKey}`);

    card.appendChild(header);
    card.appendChild(body);

    // DnD highlight and handling
    ;['dragenter','dragover'].forEach(ev => body.addEventListener(ev, (e) => { e.preventDefault(); card.classList.add('drag-over'); }));
    ;['dragleave','drop'].forEach(ev => body.addEventListener(ev, () => card.classList.remove('drag-over')));
    body.addEventListener('drop', onDropToDay);

    els.itinerary.appendChild(card);
  });
}

function onDropToDay(e) {
  e.preventDefault();
  e.stopPropagation();
  const payload = JSON.parse(e.dataTransfer.getData('text/plain'));
  const dayKey = e.currentTarget.dataset.day;

  if (payload.type === 'new') {
    state[dayKey].push({ city: payload.city, country: payload.country, note: '' });
  } else if (payload.type === 'move') {
    const { fromDay, index } = payload;
    const item = state[fromDay].splice(index, 1)[0];
    state[dayKey].push(item);
  }
  renderItinerary();
}

function renderItinerary() {
  // Clear each day's body and rebuild
  Array.from(els.itinerary.querySelectorAll('.card-body')).forEach((body) => {
    const day = body.dataset.day;
    body.innerHTML = '';
    state[day].forEach((item, idx) => {
      const row = document.createElement('div');
      row.className = 'destination';
      row.draggable = true;
      row.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', JSON.stringify({ type: 'move', fromDay: day, index: idx }));
      });
      const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const payload = JSON.parse(e.dataTransfer.getData('text/plain'));
        if (payload.type === 'move') {
          const moving = state[payload.fromDay].splice(payload.index, 1)[0];
          const insertIndex = idx; // insert before this row
          state[day].splice(insertIndex, 0, moving);
          renderItinerary();
        } else if (payload.type === 'new') {
          state[day].splice(idx, 0, { city: payload.city, country: payload.country, note: '' });
          renderItinerary();
        }
      };
      row.addEventListener('dragover', (e) => e.preventDefault());
      row.addEventListener('drop', handleDrop);

      const label = document.createElement('div');
      label.textContent = `${item.city} - ${item.country}`;
      label.addEventListener('dragover', (e) => e.preventDefault());
      label.addEventListener('drop', handleDrop);

      const note = document.createElement('input');
      note.type = 'text';
      note.className = 'note';
      note.placeholder = 'Add note...';
      note.value = item.note || '';
      note.addEventListener('dragover', (e) => e.preventDefault());
      note.addEventListener('drop', handleDrop);
      note.addEventListener('input', () => { item.note = note.value; updateSummary(); updateJSON(); });

      row.appendChild(label);
      row.appendChild(note);
      body.appendChild(row);
    });
  });
  updateSummary();
  updateJSON();
}

function updateSummary() {
  const total = Object.values(state).reduce((sum, arr) => sum + arr.length, 0);
  const countries = new Set();
  Object.values(state).forEach(arr => arr.forEach(i => countries.add(i.country)));
  els.totalCities.textContent = String(total);
  els.uniqueCountries.textContent = String(countries.size);
}

function updateJSON() {
  els.jsonPreview.textContent = JSON.stringify(state, null, 2);
}

function bindSearch() {
  els.search.addEventListener('input', () => {
    const q = els.search.value.trim().toLowerCase();
    const filtered = els.allCities.filter(c => c.city.toLowerCase().includes(q) || c.country.toLowerCase().includes(q));
    renderCityList(filtered);
  });
}

window.addEventListener('DOMContentLoaded', () => {
  els.search = document.getElementById('search');
  els.cities = document.getElementById('cities');
  els.itinerary = document.getElementById('itinerary');
  els.totalCities = document.getElementById('totalCities');
  els.uniqueCountries = document.getElementById('uniqueCountries');
  els.jsonPreview = document.getElementById('jsonPreview');

  initDayCards();
  bindSearch();
  renderItinerary();
  loadCities();
});
