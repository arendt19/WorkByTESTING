// Function to toggle theme
function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.classList.contains('dark-theme') ? 'light' : 'dark';
    
    // Toggle theme class
    if (currentTheme === 'dark') {
        root.classList.add('dark-theme');
    } else {
        root.classList.remove('dark-theme');
    }
    
    // Save theme preference to localStorage
    localStorage.setItem('workby-theme', currentTheme);
    
    // Update icon
    updateThemeIcon(currentTheme);
}

// Function to update theme icon
function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.classList.remove('bi-sun');
            themeIcon.classList.add('bi-moon');
        } else {
            themeIcon.classList.remove('bi-moon');
            themeIcon.classList.add('bi-sun');
        }
    }
}

// Initialize theme
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;
    
    // Получаем сохраненную тему из localStorage или используем системную настройку
    let darkMode = localStorage.getItem('darkMode');
    if (darkMode === null) {
        // Используем системные настройки, если пользователь еще не указал предпочтения
        darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    } else {
        // Преобразуем строку в boolean
        darkMode = darkMode === 'true';
    }
    
    // Устанавливаем начальное состояние
    applyTheme(darkMode);
    
    // Обработчик клика на кнопку переключения темы
    themeToggle.addEventListener('click', function() {
        // Переключаем тему
        darkMode = !darkMode;
        
        // Применяем изменения
        applyTheme(darkMode);
        
        // Сохраняем настройку
        localStorage.setItem('darkMode', darkMode.toString());
        
        // Если пользователь авторизован, сохраняем настройку на сервере
        const saveThemeUrl = document.querySelector('meta[name="save-theme-url"]');
        if (saveThemeUrl) {
            const url = saveThemeUrl.getAttribute('content');
            fetch(url + '?next=' + encodeURIComponent(window.location.pathname), {
                method: 'GET',
                credentials: 'same-origin',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).catch(error => console.error('Error saving theme preference:', error));
        }
    });
    
    // Функция применения темы
    function applyTheme(isDark) {
        if (isDark) {
            html.classList.add('dark-theme');
            if (themeIcon) {
                themeIcon.classList.remove('bi-sun');
                themeIcon.classList.add('bi-moon-fill');
            }
            
            // Принудительно применяем CSS переменные для темной темы
            document.documentElement.style.setProperty('--body-bg', '#111111');
            document.documentElement.style.setProperty('--text-color', '#FFFFFF');
            document.documentElement.style.setProperty('--primary-color', '#8B0000');
            document.documentElement.style.setProperty('--secondary-color', '#B0B0B0');
            document.documentElement.style.setProperty('--card-bg', '#222222');
            document.documentElement.style.setProperty('--card-border', '#333333');
            
            // Исправляем проблемы с конкретными элементами
            fixElementsInDarkTheme();
        } else {
            html.classList.remove('dark-theme');
            if (themeIcon) {
                themeIcon.classList.remove('bi-moon-fill');
                themeIcon.classList.add('bi-sun');
            }
            
            // Принудительно применяем CSS переменные для светлой темы
            document.documentElement.style.setProperty('--background-color', '#FFFFFF');
            document.documentElement.style.setProperty('--text-color', '#1A1A1A');
            document.documentElement.style.setProperty('--primary-color', '#8B0000');
            document.documentElement.style.setProperty('--secondary-color', '#B0B0B0');
            
            // Исправляем проблемы с конкретными элементами
            fixElementsInLightTheme();
        }
    }
    
    // Специальный обработчик элементов в темной теме
    function fixElementsInDarkTheme() {
        // Исправляем counter-wrapper
        const counterWrappers = document.querySelectorAll('.counter-wrapper');
        counterWrappers.forEach(el => {
            el.style.backgroundColor = '#222222';
            el.style.borderColor = '#333333';
        });
        
        // Исправляем text-muted
        const mutedTexts = document.querySelectorAll('.text-muted');
        mutedTexts.forEach(el => {
            el.style.color = '#B0B0B0';
        });
        
        // Исправляем иконки и текст-primary
        const primaryTexts = document.querySelectorAll('.text-primary');
        primaryTexts.forEach(el => {
            el.style.color = '#8B0000';
        });
        
        // Исправляем фоны светлых секций
        const lightBgSections = document.querySelectorAll('.bg-light');
        lightBgSections.forEach(el => {
            el.style.backgroundColor = '#222222';
            el.style.color = '#FFFFFF';
        });
        
        // Исправляем карточки
        const cards = document.querySelectorAll('.card');
        cards.forEach(el => {
            el.style.backgroundColor = '#222222';
            el.style.borderColor = '#333333';
            el.style.color = '#FFFFFF';
        });
    }
    
    // Специальный обработчик элементов в светлой теме
    function fixElementsInLightTheme() {
        // Возвращаем стандартные стили для counter-wrapper
        const counterWrappers = document.querySelectorAll('.counter-wrapper');
        counterWrappers.forEach(el => {
            el.style.backgroundColor = '#FFFFFF';
            el.style.borderColor = '#B0B0B0';
        });
        
        // Возвращаем стандартные стили для text-muted
        const mutedTexts = document.querySelectorAll('.text-muted');
        mutedTexts.forEach(el => {
            el.style.color = '';  // Возвращаем исходный цвет
        });
        
        // Исправляем фоны светлых секций
        const lightBgSections = document.querySelectorAll('.bg-light');
        lightBgSections.forEach(el => {
            el.style.backgroundColor = '#f8f9fa';
            el.style.color = '#1A1A1A';
        });
    }
}); 