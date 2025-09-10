// Global variables
let zodiacData = [];
let currentLanguage = 'en'; // Default to English

// DOM elements
const loading = document.getElementById('loading');
const zodiacGrid = document.getElementById('zodiacGrid');
const modal = document.getElementById('modal');
const languageToggle = document.getElementById('languageToggle');
const languageText = document.getElementById('languageText');
const closeModal = document.getElementById('closeModal');
const modalCloseBtn = document.getElementById('modalCloseBtn');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadZodiacData();
    setupEventListeners();
});

// Load zodiac data from JSON file
async function loadZodiacData() {
    try {
        const response = await fetch('zodiac-data.json');
        const data = await response.json();
        zodiacData = data.zodiacs;
        renderZodiacGrid();
        hideLoading();
    } catch (error) {
        console.error('Error loading zodiac data:', error);
        showError();
    }
}

// Hide loading spinner and show content
function hideLoading() {
    loading.classList.add('hidden');
    zodiacGrid.classList.remove('hidden');
    zodiacGrid.classList.add('animate-fade-in');
}

// Show error message if data fails to load
function showError() {
    loading.innerHTML = `
        <div class="text-center">
            <div class="text-red-500 text-xl mb-2">⚠️</div>
            <p class="text-red-600" data-zh="加载失败，请刷新页面重试" data-en="Failed to load data, please refresh and try again">
                Failed to load data, please refresh and try again
            </p>
        </div>
    `;
}

// Render the zodiac animal grid
function renderZodiacGrid() {
    zodiacGrid.innerHTML = '';
    
    zodiacData.forEach((zodiac, index) => {
        const button = createZodiacButton(zodiac, index);
        zodiacGrid.appendChild(button);
    });
}

// Create individual zodiac button
function createZodiacButton(zodiac, index) {
    const button = document.createElement('button');
    button.className = 'zodiac-button';
    button.style.animationDelay = `${index * 0.1}s`;
    
    button.innerHTML = `
        <div class="zodiac-emoji">${zodiac.image}</div>
        <div>
            <div class="zodiac-name" data-zh="${zodiac.name}" data-en="${zodiac.name_en}">
                ${currentLanguage === 'zh' ? zodiac.name : zodiac.name_en}
            </div>
            <div class="zodiac-alt-name" data-zh="${zodiac.name_en}" data-en="${zodiac.name}">
                ${currentLanguage === 'zh' ? zodiac.name_en : zodiac.name}
            </div>
        </div>
    `;
    
    button.addEventListener('click', () => openModal(zodiac));
    
    return button;
}

// Open modal with zodiac details
function openModal(zodiac) {
    // Update modal content
    document.getElementById('modalImage').textContent = zodiac.image;
    document.getElementById('modalTitle').textContent = currentLanguage === 'zh' ? zodiac.name : zodiac.name_en;
    document.getElementById('modalSubtitle').textContent = currentLanguage === 'zh' ? zodiac.name_en : zodiac.name;
    document.getElementById('modalYears').textContent = zodiac.year_range;
    document.getElementById('modalTraits').textContent = currentLanguage === 'zh' ? zodiac.traits : zodiac.traits_en;
    document.getElementById('modalDescription').textContent = currentLanguage === 'zh' ? zodiac.description : zodiac.description_en;
    
    // Show modal
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModalHandler() {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

// Toggle language
function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'zh' : 'en';
    languageText.textContent = currentLanguage === 'en' ? '中文' : 'English';
    
    // Update all text elements
    updateLanguageText();
    
    // Re-render zodiac grid to update button text
    renderZodiacGrid();
}

// Update text based on current language
function updateLanguageText() {
    const elements = document.querySelectorAll('[data-zh][data-en]');
    elements.forEach(element => {
        const zhText = element.getAttribute('data-zh');
        const enText = element.getAttribute('data-en');
        element.textContent = currentLanguage === 'zh' ? zhText : enText;
    });
}

// Setup event listeners
function setupEventListeners() {
    // Language toggle
    languageToggle.addEventListener('click', toggleLanguage);
    
    // Modal close events
    closeModal.addEventListener('click', closeModalHandler);
    modalCloseBtn.addEventListener('click', closeModalHandler);
    
    // Close modal when clicking backdrop
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.classList.contains('modal-overlay')) {
            closeModalHandler();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModalHandler();
        }
    });
    
    // Prevent modal content click from closing modal
    modal.querySelector('.modal-content').addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

// Add some interactive flourishes
document.addEventListener('DOMContentLoaded', function() {
    // Add a subtle parallax effect to the header on scroll
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const header = document.querySelector('header');
        if (header) {
            header.style.transform = `translateY(${scrolled * 0.1}px)`;
        }
    });
    
    // Add animation to zodiac buttons on hover
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.zodiac-button')) {
            const emoji = e.target.closest('.zodiac-button').querySelector('.zodiac-emoji');
            if (emoji) {
                emoji.style.animation = 'bounceLight 0.6s ease-out';
                setTimeout(() => {
                    emoji.style.animation = '';
                }, 600);
            }
        }
    });
});