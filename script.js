(function () {
  const state = {
    lang: 'zh',
    data: [],
    selected: null,
  };

  const el = {
    title: document.getElementById('app-title'),
    desc: document.getElementById('app-description'),
    grid: document.getElementById('zodiac-grid'),
    langToggle: document.getElementById('lang-toggle'),
    modalBackdrop: document.getElementById('modal-backdrop'),
    modal: document.getElementById('modal'),
    modalTitle: document.getElementById('modal-title'),
    modalSubtitle: document.getElementById('modal-subtitle'),
    modalYear: document.getElementById('modal-year-range'),
    modalTraits: document.getElementById('modal-traits'),
    labelYear: document.getElementById('label-year'),
    labelTraits: document.getElementById('label-traits'),
    modalClose: document.getElementById('modal-close'),
  };

  function t(key) {
    const zh = {
      title: '十二生肖',
      desc: '点击任意生肖查看详情。',
      year: '年份：',
      traits: '性格：',
      subtitle: 'Zodiac',
      langButton: 'EN',
    };
    const en = {
      title: 'Chinese Zodiac',
      desc: 'Click any animal to view details.',
      year: 'Years: ',
      traits: 'Traits: ',
      subtitle: '生肖',
      langButton: '中文',
    };
    return state.lang === 'zh' ? zh[key] : en[key];
  }

  function updateTexts() {
    el.title.textContent = t('title');
    el.desc.textContent = t('desc');
    el.labelYear.textContent = t('year');
    el.labelTraits.textContent = t('traits');
    el.modalSubtitle.textContent = t('subtitle');
    el.langToggle.textContent = t('langButton');

    if (state.selected) {
      const animal = state.selected;
      el.modalTitle.textContent = state.lang === 'zh' ? animal.name : animal.name_en;
      el.modalYear.textContent = animal.year_range;
      el.modalTraits.textContent = (state.lang === 'zh' ? animal.traits : animal.traits_en).join(', ');
    }
  }

  function cardTemplate(animal) {
    const label = state.lang === 'zh' ? animal.name : animal.name_en;
    const btn = document.createElement('button');
    btn.className = 'group relative aspect-square rounded-2xl bg-white/80 backdrop-blur shadow hover:shadow-lg transition transform hover:scale-[1.03] active:scale-[0.98] flex items-center justify-center overflow-hidden';
    btn.setAttribute('data-id', animal.id);
    btn.setAttribute('aria-label', label);

    const gradient = document.createElement('div');
    gradient.className = 'absolute inset-0 bg-gradient-to-br from-amber-100 via-rose-100 to-indigo-100 opacity-70 group-hover:opacity-90 transition';

    const emoji = document.createElement('div');
    emoji.className = 'relative z-[1] text-5xl md:text-6xl select-none drop-shadow';
    emoji.textContent = animal.emoji;

    const caption = document.createElement('div');
    caption.className = 'absolute bottom-2 left-1/2 -translate-x-1/2 text-xs md:text-sm font-medium text-gray-700 bg-white/80 px-2 py-0.5 rounded-full shadow-sm';
    caption.textContent = label;

    btn.appendChild(gradient);
    btn.appendChild(emoji);
    btn.appendChild(caption);

    btn.addEventListener('click', () => openModal(animal));

    return btn;
  }

  function renderGrid() {
    el.grid.innerHTML = '';
    state.data.forEach((animal) => {
      el.grid.appendChild(cardTemplate(animal));
    });
  }

  function openModal(animal) {
    state.selected = animal;
    el.modalTitle.textContent = state.lang === 'zh' ? animal.name : animal.name_en;
    el.modalYear.textContent = animal.year_range;
    el.modalTraits.textContent = (state.lang === 'zh' ? animal.traits : animal.traits_en).join(', ');

    el.modalBackdrop.classList.remove('hidden');
    // animate in
    el.modal.classList.remove('opacity-0');
    el.modal.classList.add('animate-fadeInUp');
  }

  function closeModal() {
    // animate out
    el.modal.classList.remove('animate-fadeInUp');
    el.modal.classList.add('animate-fadeOutDown');
    setTimeout(() => {
      el.modalBackdrop.classList.add('hidden');
      el.modal.classList.remove('animate-fadeOutDown');
      el.modal.classList.add('opacity-0');
      state.selected = null;
    }, 180);
  }

  async function init() {
    try {
      const res = await fetch('./data/zodiac.json');
      const data = await res.json();
      state.data = data;
      renderGrid();
      updateTexts();
    } catch (e) {
      console.error('Failed to load zodiac data', e);
      el.desc.textContent = state.lang === 'zh' ? '加载数据失败。' : 'Failed to load data.';
    }

    el.langToggle.addEventListener('click', () => {
      state.lang = state.lang === 'zh' ? 'en' : 'zh';
      updateTexts();
      renderGrid();
    });

    el.modalClose.addEventListener('click', closeModal);
    el.modalBackdrop.addEventListener('click', (ev) => {
      if (ev.target === el.modalBackdrop) closeModal();
    });
    document.addEventListener('keydown', (ev) => {
      if (ev.key === 'Escape' && !el.modalBackdrop.classList.contains('hidden')) closeModal();
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
