# Chinese Zodiac Animals Web App

A responsive single-page web application that displays the 12 Chinese zodiac animals as interactive animated image buttons. Users can click on any zodiac animal to learn more about its characteristics, years, and traits in both Chinese and English.

## Features

✨ **Interactive Zodiac Grid**: All 12 Chinese zodiac animals displayed as clickable image buttons
🌐 **Bilingual Support**: Toggle between Chinese (中文) and English languages
📱 **Responsive Design**: Optimized for desktop, tablet, and mobile devices
🎯 **Modal Popups**: Detailed information about each zodiac animal
🎨 **Smooth Animations**: Hover effects, modal transitions, and loading animations
📊 **Dynamic Data Loading**: JSON-based data structure for easy maintenance

## Demo Screenshots

### Desktop View (English)
![Desktop View](https://github.com/user-attachments/assets/f3063d9c-22be-4bf2-9d90-23e3ae0a658d)

### Modal Popup (English)
![Modal Popup English](https://github.com/user-attachments/assets/c0a62dcf-fd62-43a2-9f14-204fcf0a51f0)

### Mobile View (Chinese)
![Mobile View Chinese](https://github.com/user-attachments/assets/28c05d0f-a447-44c6-b2a4-b3aad349ed02)

### Mobile Modal (Chinese)
![Mobile Modal Chinese](https://github.com/user-attachments/assets/7e6c8a5d-e72a-4a35-ad22-8a4090c5b2a3)

## Tech Stack

- **HTML5**: Semantic markup structure
- **CSS3**: Custom responsive styling with animations
- **Vanilla JavaScript**: Dynamic functionality and interactivity
- **JSON**: Data storage for zodiac information

## File Structure

```
├── index.html          # Main HTML file with embedded CSS
├── script.js          # JavaScript functionality
├── zodiac-data.json   # Zodiac animals data (Chinese/English)
└── README.md          # Project documentation
```

## Features Implemented

### ✅ Core Requirements
- [x] Load JSON data dynamically
- [x] Clickable image buttons for each zodiac animal
- [x] Modal popup with detailed information
- [x] Language toggle (Chinese/English)
- [x] Hover effects on images
- [x] Responsive design for all screen sizes
- [x] Animated modal appearances

### 🎯 Information Displayed
- **Chinese Name** (e.g., 龙)
- **English Name** (e.g., Dragon)
- **Year Range** (e.g., 2024, 2012, 2000...)
- **Personality Traits** (bilingual)
- **Detailed Description** (bilingual)

### 🎨 Interactive Features
- **Hover Effects**: Scale and shadow animations on zodiac buttons
- **Modal Animations**: Slide-up and fade-in effects
- **Language Toggle**: Instant translation of all UI text
- **Responsive Grid**: Adaptive layout (2-6 columns based on screen size)
- **Loading States**: Spinner animation while data loads
- **Keyboard Support**: ESC key to close modals

## Usage

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/ghcpd/xubo_test_repo.git
cd xubo_test_repo
```

2. Start a local server (any of these methods):
```bash
# Python 3
python -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080

# Node.js (if you have http-server installed)
npx http-server -p 8080

# PHP
php -S localhost:8080
```

3. Open your browser and navigate to `http://localhost:8080`

### Direct File Access
You can also open `index.html` directly in your browser, though some features may not work due to CORS restrictions.

## Browser Compatibility

- ✅ Chrome/Chromium (88+)
- ✅ Firefox (85+)
- ✅ Safari (14+)
- ✅ Edge (88+)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Responsive Breakpoints

- **Mobile**: < 768px (2 columns)
- **Tablet**: 768px - 1023px (3 columns)
- **Desktop**: 1024px - 1279px (4 columns)
- **Large Desktop**: ≥ 1280px (6 columns)

## Data Structure

The zodiac data is stored in `zodiac-data.json` with the following structure:

```json
{
  "zodiacs": [
    {
      "id": "dragon",
      "name": "龙",
      "name_en": "Dragon",
      "year_range": "2024, 2012, 2000...",
      "traits": "雄心勃勃、热情、创新",
      "traits_en": "Ambitious, passionate, innovative",
      "image": "🐲",
      "description": "属龙的人雄心勃勃...",
      "description_en": "People born in the Year of the Dragon..."
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across different devices/browsers
5. Submit a pull request

## Future Enhancements

- 🎯 Add zodiac compatibility checker
- 🎨 Include more detailed animations
- 📅 Add current year zodiac highlighting
- 🔊 Sound effects for interactions
- 🌙 Dark/light mode toggle
- 📱 Progressive Web App (PWA) features

## License

This project is open source and available under the MIT License.