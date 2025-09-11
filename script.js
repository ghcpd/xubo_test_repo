class TripPlanner {
    constructor() {
        this.cities = [];
        this.itinerary = {};
        this.filteredCities = [];
        
        // Initialize 7 days
        for (let i = 1; i <= 7; i++) {
            this.itinerary[`day${i}`] = [];
        }
        
        this.init();
    }
    
    async init() {
        await this.loadCities();
        this.setupEventListeners();
        this.renderCities();
        this.renderItinerary();
        this.updateSummary();
        this.updateJsonPreview();
    }
    
    async loadCities() {
        try {
            const response = await fetch('cities.json');
            this.cities = await response.json();
            this.filteredCities = [...this.cities];
        } catch (error) {
            console.error('Error loading cities:', error);
            // Fallback data in case JSON file can't be loaded
            this.cities = [
                { "city": "Tokyo", "country": "Japan" },
                { "city": "Kyoto", "country": "Japan" },
                { "city": "Paris", "country": "France" },
                { "city": "Nice", "country": "France" },
                { "city": "New York", "country": "USA" },
                { "city": "Los Angeles", "country": "USA" },
                { "city": "Beijing", "country": "China" },
                { "city": "Shanghai", "country": "China" },
                { "city": "Sydney", "country": "Australia" },
                { "city": "Melbourne", "country": "Australia" }
            ];
            this.filteredCities = [...this.cities];
        }
    }
    
    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', (e) => {
            this.filterCities(e.target.value);
        });
    }
    
    filterCities(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        this.filteredCities = this.cities.filter(city => 
            city.city.toLowerCase().includes(term) || 
            city.country.toLowerCase().includes(term)
        );
        this.renderCities();
    }
    
    renderCities() {
        const citiesList = document.getElementById('cities-list');
        citiesList.innerHTML = '';
        
        this.filteredCities.forEach(city => {
            const cityCard = this.createCityCard(city);
            citiesList.appendChild(cityCard);
        });
    }
    
    createCityCard(city) {
        const card = document.createElement('div');
        card.className = 'city-card';
        card.draggable = true;
        card.dataset.city = city.city;
        card.dataset.country = city.country;
        
        card.innerHTML = `
            <div class="city-name">${city.city}</div>
            <div class="country-name">${city.country}</div>
        `;
        
        // Drag events for city cards
        card.addEventListener('dragstart', (e) => {
            card.classList.add('dragging');
            e.dataTransfer.setData('text/plain', JSON.stringify(city));
            e.dataTransfer.effectAllowed = 'copy';
        });
        
        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
        });
        
        return card;
    }
    
    renderItinerary() {
        const itinerary = document.getElementById('itinerary');
        itinerary.innerHTML = '';
        
        for (let i = 1; i <= 7; i++) {
            const dayCard = this.createDayCard(i);
            itinerary.appendChild(dayCard);
        }
        
        // Render destinations after all day cards are created
        for (let i = 1; i <= 7; i++) {
            this.renderDayDestinations(`day${i}`);
        }
    }
    
    createDayCard(dayNumber) {
        const dayKey = `day${dayNumber}`;
        const dayData = this.itinerary[dayKey] || [];
        
        const dayCard = document.createElement('div');
        dayCard.className = 'day-card';
        dayCard.dataset.day = dayKey;
        
        dayCard.innerHTML = `
            <div class="day-header" onclick="toggleDay('${dayKey}')">
                <h3>Day ${dayNumber}</h3>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="day-content" id="${dayKey}-content">
                <div class="day-destinations" id="${dayKey}-destinations">
                    ${dayData.length === 0 ? '<div class="empty">Drop cities here</div>' : ''}
                </div>
            </div>
        `;
        
        const destinations = dayCard.querySelector('.day-destinations');
        
        // Add drop functionality to day destinations
        destinations.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            destinations.classList.add('drag-over');
        });
        
        destinations.addEventListener('dragleave', (e) => {
            if (!destinations.contains(e.relatedTarget)) {
                destinations.classList.remove('drag-over');
            }
        });
        
        destinations.addEventListener('drop', (e) => {
            e.preventDefault();
            destinations.classList.remove('drag-over');
            
            const cityData = JSON.parse(e.dataTransfer.getData('text/plain'));
            
            // Check if it's a city from the left panel or a reorder
            if (e.dataTransfer.getData('source') === 'itinerary') {
                // Handle reordering within itinerary
                const sourceDay = e.dataTransfer.getData('sourceDay');
                const sourceIndex = parseInt(e.dataTransfer.getData('sourceIndex'));
                this.moveDestination(sourceDay, sourceIndex, dayKey);
            } else {
                // Add new city to itinerary
                this.addCityToDay(dayKey, cityData);
            }
        });
        
        return dayCard;
    }
    
    renderDayDestinations(dayKey) {
        const destinations = document.getElementById(`${dayKey}-destinations`);
        const dayData = this.itinerary[dayKey] || [];
        
        if (dayData.length === 0) {
            destinations.innerHTML = '<div class="empty">Drop cities here</div>';
            destinations.classList.add('empty');
        } else {
            destinations.classList.remove('empty');
            destinations.innerHTML = '';
            
            dayData.forEach((destination, index) => {
                const destCard = this.createDestinationCard(destination, dayKey, index);
                destinations.appendChild(destCard);
            });
        }
    }
    
    createDestinationCard(destination, dayKey, index) {
        const card = document.createElement('div');
        card.className = 'destination-card';
        card.draggable = true;
        card.dataset.day = dayKey;
        card.dataset.index = index;
        
        card.innerHTML = `
            <div class="destination-info">
                <div class="destination-details">
                    <div class="city-name">${destination.city}</div>
                    <div class="country-name">${destination.country}</div>
                </div>
                <button class="remove-btn" onclick="tripPlanner.removeDestination('${dayKey}', ${index})" title="Remove destination">×</button>
            </div>
            <textarea class="note-field" placeholder="Add notes for ${destination.city}..." onchange="tripPlanner.updateNote('${dayKey}', ${index}, this.value)">${destination.note || ''}</textarea>
        `;
        
        // Drag events for destination cards (for reordering)
        card.addEventListener('dragstart', (e) => {
            card.classList.add('dragging');
            e.dataTransfer.setData('text/plain', JSON.stringify(destination));
            e.dataTransfer.setData('source', 'itinerary');
            e.dataTransfer.setData('sourceDay', dayKey);
            e.dataTransfer.setData('sourceIndex', index.toString());
            e.dataTransfer.effectAllowed = 'move';
        });
        
        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
        });
        
        return card;
    }
    
    addCityToDay(dayKey, cityData) {
        if (!this.itinerary[dayKey]) {
            this.itinerary[dayKey] = [];
        }
        
        const destination = {
            city: cityData.city,
            country: cityData.country,
            note: ''
        };
        
        this.itinerary[dayKey].push(destination);
        this.renderDayDestinations(dayKey);
        this.updateSummary();
        this.updateJsonPreview();
    }
    
    removeDestination(dayKey, index) {
        this.itinerary[dayKey].splice(index, 1);
        this.renderDayDestinations(dayKey);
        this.updateSummary();
        this.updateJsonPreview();
    }
    
    moveDestination(sourceDayKey, sourceIndex, targetDayKey) {
        const destination = this.itinerary[sourceDayKey][sourceIndex];
        this.itinerary[sourceDayKey].splice(sourceIndex, 1);
        this.itinerary[targetDayKey].push(destination);
        
        this.renderDayDestinations(sourceDayKey);
        this.renderDayDestinations(targetDayKey);
        this.updateSummary();
        this.updateJsonPreview();
    }
    
    updateNote(dayKey, index, note) {
        if (this.itinerary[dayKey] && this.itinerary[dayKey][index]) {
            this.itinerary[dayKey][index].note = note;
            this.updateJsonPreview();
        }
    }
    
    updateSummary() {
        const totalCities = Object.values(this.itinerary).reduce((total, day) => total + day.length, 0);
        
        const uniqueCountries = new Set();
        Object.values(this.itinerary).forEach(day => {
            day.forEach(destination => {
                uniqueCountries.add(destination.country);
            });
        });
        
        document.getElementById('total-cities').textContent = `Cities: ${totalCities}`;
        document.getElementById('unique-countries').textContent = `Countries: ${uniqueCountries.size}`;
    }
    
    updateJsonPreview() {
        const jsonState = document.getElementById('json-state');
        jsonState.textContent = JSON.stringify(this.itinerary, null, 2);
    }
}

// Global functions for event handlers
function toggleDay(dayKey) {
    const content = document.getElementById(`${dayKey}-content`);
    const icon = content.parentElement.querySelector('.toggle-icon');
    
    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
        icon.classList.remove('expanded');
    } else {
        content.classList.add('expanded');
        icon.classList.add('expanded');
    }
}

// Initialize the app when DOM is loaded
let tripPlanner;
document.addEventListener('DOMContentLoaded', () => {
    tripPlanner = new TripPlanner();
});

// Prevent default drag behavior on document
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});