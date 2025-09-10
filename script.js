const grid = document.getElementById('grid');
const overlay = document.getElementById('overlay');
const modal = document.getElementById('modal');
const closeBtn = document.getElementById('closeBtn');
const modalTitle = document.getElementById('modalTitle');
const modalYear = document.getElementById('modalYear');
const modalTraits = document.getElementById('modalTraits');
const langToggle = document.getElementById('langToggle');
const title = document.getElementById('title');

let lang = 'zh';
let data = [];

async function loadData() {
  const res = await fetch('./zodiac.json');
  data = await res.json();
  renderGrid();
}

function renderGrid() {
  grid.innerHTML = '';
  data.forEach((item, idx) => {
    const btn = document.createElement('button');
    btn.className = 'bg-white rounded shadow hover:shadow-lg transition transform hover:scale-105 p-2 flex flex-col items-center';
    btn.innerHTML = `
      <img src="${item.image}" alt="${item.name_en}" class="w-full h-32 object-cover rounded" />
      <span class="mt-2">${lang === 'zh' ? item.name : item.name_en}</span>
    `;
    btn.addEventListener('click', () => openModal(item));
    grid.appendChild(btn);
  });
}

function openModal(item) {
  modalTitle.textContent = lang === 'zh' ? `${item.name} / ${item.name_en}` : `${item.name_en} / ${item.name}`;
  modalYear.textContent = (lang === 'zh' ? '年份：' : 'Years: ') + item.year_range;
  modalTraits.textContent = (lang === 'zh' ? '特点：' : 'Traits: ') + item.traits;

  overlay.classList.remove('hidden');
  modal.classList.add('modal-enter');
  requestAnimationFrame(() => {
    modal.classList.add('modal-enter-active');
  });
}

function closeModal() {
  modal.classList.remove('modal-enter-active');
  modal.classList.add('modal-exit');
  modal.classList.add('modal-exit-active');
  setTimeout(() => {
    overlay.classList.add('hidden');
    modal.classList.remove('modal-exit', 'modal-exit-active');
    modal.classList.remove('modal-enter');
  }, 160);
}

closeBtn.addEventListener('click', closeModal);
overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });

langToggle.addEventListener('click', () => {
  lang = lang === 'zh' ? 'en' : 'zh';
  title.textContent = lang === 'zh' ? '十二生肖' : 'Chinese Zodiac';
  langToggle.textContent = lang === 'zh' ? 'English' : '中文';
  renderGrid();
});

loadData();
