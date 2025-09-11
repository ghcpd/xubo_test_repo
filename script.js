const itinerary = {
  day1: [],
  day2: [],
  day3: [],
  day4: [],
  day5: [],
  day6: [],
  day7: []
};

let citiesData = [];
let draggedData = null; // { city, country, from: 'cities' | { day, index } }

function $(sel) {
  return document.querySelector(sel);
}
function $all(sel) {
  return Array.from(document.querySelectorAll(sel));
}

function createCityItem(city, country) {
  const el = document.createElement('div');
  el.className = 'city-item';
  el.draggable = true;
  el.innerHTML = `<strong>${city}</strong><div class="meta">${country}</div>`;
  el.addEventListener('dragstart', (e) => {
    draggedData = { city, country, from: 'cities' };
    e.dataTransfer.setData('text/plain', JSON.stringify(draggedData));
  });
  // Fallback for environments where dataTransfer isn't populated
  el.addEventListener('mousedown', () => {
    draggedData = { city, country, from: 'cities' };
  });
  return el;
}

function createDestItem(entry, day, index) {
  const el = document.createElement('div');
  el.className = 'dest-item';
  el.draggable = true;
  el.innerHTML = `
    <div><strong>${entry.city}</strong> <span class="meta">${entry.country}</span></div>
    <div class="note" contenteditable="true" aria-label="Note for ${entry.city}">${entry.note || ''}</div>
  `;
  el.addEventListener('dragstart', (e) => {
    draggedData = { city: entry.city, country: entry.country, from: { day, index } };
    e.dataTransfer.setData('text/plain', JSON.stringify(draggedData));
  });

  // Fallback for environments where dataTransfer isn't populated
  el.addEventListener('mousedown', () => {
    draggedData = { city: entry.city, country: entry.country, from: { day, index } };
  });

  // Update note inline
  const noteEl = el.querySelector('.note');
  noteEl.addEventListener('input', () => {
    itinerary[day][index].note = noteEl.textContent;
    updateState();
  });

  return el;
}

function renderCities(list) {
  const container = $('#cities-list');
  container.innerHTML = '';
  list.forEach(({ city, country }) => container.appendChild(createCityItem(city, country)));
}

function renderItinerary() {
  const container = $('#itinerary');
  container.innerHTML = '';
  Object.keys(itinerary).forEach((dayKey, dayIdx) => {
    const card = document.createElement('div');
    card.className = 'day-card open';
    card.dataset.day = dayKey;

    const header = document.createElement('div');
    header.className = 'day-header';
    header.innerHTML = `<div><strong>Day ${dayIdx + 1}</strong></div><div class="chevron">▶</div>`;

    const body = document.createElement('div');
    body.className = 'destinations';

    // Toggle collapse
    header.addEventListener('click', () => {
      card.classList.toggle('open');
    });

    // Allow dropping on header (append to day)
    addDropHandlers(header, dayKey);

    // Drop handling on the day body
    addDropHandlers(body, dayKey);

    // Populate existing destinations
    itinerary[dayKey].forEach((entry, index) => {
      const item = createDestItem(entry, dayKey, index);
      addDropHandlers(item, dayKey, index);
      body.appendChild(item);
    });

    card.appendChild(header);
    card.appendChild(body);
    container.appendChild(card);

    // Ensure body starts expanded for smooth transition then can be toggled
    requestAnimationFrame(() => card.classList.add('open'));
  });
}

function addDropHandlers(target, dayKey, targetIndex = null) {
  target.addEventListener('dragover', (e) => {
    e.preventDefault();
    target.classList.add('drop-target');
  });
  target.addEventListener('dragleave', () => {
    target.classList.remove('drop-target');
  });
  target.addEventListener('drop', (e) => {
    e.preventDefault();
    target.classList.remove('drop-target');
    const data = draggedData || JSON.parse(e.dataTransfer.getData('text/plain') || '{}');

    if (!data || !data.city) return;

    // If dragging from itinerary, remove from original location first
    if (data.from !== 'cities') {
      const { day, index } = data.from;
      const [moved] = itinerary[day].splice(index, 1);
      // Adjust targetIndex if same day and removing before insertion
      if (day === dayKey && targetIndex !== null && index < targetIndex) {
        targetIndex -= 1;
      }
      insertIntoDay(dayKey, moved.city, moved.country, moved.note || '', targetIndex);
    } else {
      insertIntoDay(dayKey, data.city, data.country, '', targetIndex);
    }

    renderItinerary();
    updateState();
  });
}

function insertIntoDay(dayKey, city, country, note = '', index = null) {
  const entry = { city, country, note };
  if (index === null || index < 0 || index > itinerary[dayKey].length) {
    itinerary[dayKey].push(entry);
  } else {
    itinerary[dayKey].splice(index, 0, entry);
  }
}

function updateState() {
  // Update summary
  const all = Object.values(itinerary).flat();
  const total = all.length;
  const uniqueCountries = new Set(all.map((e) => e.country)).size;
  $('#summary').innerHTML = `<strong>Summary:</strong> Total cities: ${total} | Unique countries: ${uniqueCountries}`;

  // Update JSON preview
  $('#state-json').textContent = JSON.stringify(itinerary, null, 2);
}

function setupSearch() {
  const input = $('#search');
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    const filtered = citiesData.filter(({ city, country }) =>
      city.toLowerCase().includes(q) || country.toLowerCase().includes(q)
    );
    renderCities(filtered);
  });
}

async function init() {
  try {
    const res = await fetch('cities.json');
    citiesData = await res.json();
    renderCities(citiesData);
    renderItinerary();
    setupSearch();
    updateState();
  } catch (e) {
    console.error('Failed to load cities:', e);
  }
}

window.addEventListener('DOMContentLoaded', init);
