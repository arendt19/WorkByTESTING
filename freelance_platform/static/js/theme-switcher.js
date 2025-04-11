// Function to toggle theme
function toggleTheme() {
    const root = document.documentElement;
    const isDarkTheme = root.classList.contains('dark-theme');
    
    // Получаем сохраненную тему из localStorage
    let darkMode = !isDarkTheme; // Инвертируем текущее состояние
    
    // Применяем изменения
    applyTheme(darkMode);
    
    // Сохраняем настройку в localStorage
    localStorage.setItem('darkMode', darkMode.toString());
    
    // Вызываем событие изменения темы, чтобы другие скрипты могли на него реагировать
    const themeChangeEvent = new CustomEvent('themeChange', { detail: { darkMode: darkMode } });
    document.dispatchEvent(themeChangeEvent);
    
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
}

// Функция применения темы
function applyTheme(isDark) {
    const html = document.documentElement;
    const themeIcon = document.getElementById('theme-icon');
    
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
    
    // Вызываем функцию updatePageTheme для обновления стилей в зависимости от текущей страницы
    updatePageTheme();
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
    
    // Исправляем заголовки карточек
    const cardHeaders = document.querySelectorAll('.card-header');
    cardHeaders.forEach(el => {
        if (el.classList.contains('bg-primary') || el.classList.contains('wallet-card-header')) {
            el.style.backgroundColor = '#333 !important';
            el.style.borderBottom = '2px solid var(--primary-color)';
        }
    });
    
    // Исправляем карточки
    const cards = document.querySelectorAll('.card');
    cards.forEach(el => {
        el.style.backgroundColor = '#222222';
        el.style.borderColor = '#333333';
        el.style.color = '#FFFFFF';
    });
    
    // Исправляем таблицы
    const tableLightHeaders = document.querySelectorAll('.table-light');
    tableLightHeaders.forEach(el => {
        el.style.backgroundColor = '#333';
        el.style.color = '#f0f0f0';
    });
    
    // Исправляем строки таблиц при наведении 
    const tables = document.querySelectorAll('.table-hover');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.style.backgroundColor = 'rgba(255, 255, 255, 0.075)';
            });
            row.addEventListener('mouseleave', () => {
                row.style.backgroundColor = '';
            });
        });
    });
    
    // Исправляем элементы чата
    const chatContainers = document.querySelectorAll('.chat-container');
    chatContainers.forEach(el => {
        el.style.backgroundColor = '#2a2a2a';
        el.style.borderColor = '#444';
    });
    
    const chatMessages = document.querySelectorAll('.chat-message:not(.outgoing)');
    chatMessages.forEach(el => {
        el.style.backgroundColor = '#333';
        el.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.3)';
        el.style.color = '#FFFFFF';
    });
    
    const outgoingMessages = document.querySelectorAll('.chat-message.outgoing');
    outgoingMessages.forEach(el => {
        el.style.backgroundColor = '#700000';
    });
    
    const contactInfo = document.querySelectorAll('.contact-info');
    contactInfo.forEach(el => {
        el.style.backgroundColor = '#2a2a2a';
        el.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';
        el.style.borderColor = '#444';
        el.style.color = '#FFFFFF';
    });
    
    const contactAvatars = document.querySelectorAll('.contact-avatar');
    contactAvatars.forEach(el => {
        el.style.backgroundColor = '#444';
        el.style.color = '#f0f0f0';
    });
    
    const conversationHeaders = document.querySelectorAll('.conversation-header');
    conversationHeaders.forEach(el => {
        el.style.backgroundColor = '#333';
        el.style.borderBottom = '2px solid var(--primary-color)';
    });
    
    const messagesList = document.querySelectorAll('.messages-list li, .notifications-list li');
    messagesList.forEach(el => {
        el.style.borderBottomColor = '#444';
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
    
    // Возвращаем стандартные стили для карточек
    const cards = document.querySelectorAll('.card');
    cards.forEach(el => {
        el.style.backgroundColor = '';
        el.style.borderColor = '';
        el.style.color = '';
    });
    
    // Возвращаем стандартные стили для заголовков карточек
    const cardHeaders = document.querySelectorAll('.card-header');
    cardHeaders.forEach(el => {
        if (el.classList.contains('bg-primary') || el.classList.contains('wallet-card-header')) {
            el.style.backgroundColor = 'var(--primary-color) !important';
            el.style.borderBottom = '';
        }
    });
    
    // Возвращаем стандартные стили для таблиц
    const tableLightHeaders = document.querySelectorAll('.table-light');
    tableLightHeaders.forEach(el => {
        el.style.backgroundColor = '';
        el.style.color = '';
    });
    
    // Возвращаем стандартные стили для элементов чата
    const chatContainers = document.querySelectorAll('.chat-container');
    chatContainers.forEach(el => {
        el.style.backgroundColor = '#f0f0f0';
        el.style.borderColor = '#ddd';
    });
    
    const chatMessages = document.querySelectorAll('.chat-message:not(.outgoing)');
    chatMessages.forEach(el => {
        el.style.backgroundColor = '#fff';
        el.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        el.style.color = '';
    });
    
    const outgoingMessages = document.querySelectorAll('.chat-message.outgoing');
    outgoingMessages.forEach(el => {
        el.style.backgroundColor = 'var(--primary-color)';
        el.style.color = 'white';
    });
    
    const contactInfo = document.querySelectorAll('.contact-info');
    contactInfo.forEach(el => {
        el.style.backgroundColor = '#f9f9f9';
        el.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
        el.style.borderColor = '';
        el.style.color = '';
    });
    
    const contactAvatars = document.querySelectorAll('.contact-avatar');
    contactAvatars.forEach(el => {
        el.style.backgroundColor = '#e0e0e0';
        el.style.color = '#333';
    });
    
    const conversationHeaders = document.querySelectorAll('.conversation-header');
    conversationHeaders.forEach(el => {
        el.style.backgroundColor = 'var(--primary-color)';
        el.style.borderBottom = '';
    });
    
    const messagesList = document.querySelectorAll('.messages-list li, .notifications-list li');
    messagesList.forEach(el => {
        el.style.borderBottomColor = '#eee';
    });
}

// Initialize theme
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
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
    
    // Принудительно вызываем updatePageTheme после загрузки страницы
    document.addEventListener('load', function() {
        updatePageTheme();
    });
    
    // Также добавляем обработчик события для DOMContentLoaded для элементов, загруженных динамически
    document.addEventListener('DOMNodeInserted', function(event) {
        // Если вставлены новые элементы, которые могут быть частью чата, обновляем тему
        const affectedNodes = event.target.querySelectorAll ? event.target.querySelectorAll('.chat-container, .chat-message, .contact-info') : null;
        if (affectedNodes && affectedNodes.length > 0) {
            updatePageTheme();
        }
    });
    
    // Проверяем наличие кнопки переключения темы и добавляем обработчик
    if (themeToggle) {
        // Добавляем обработчик для кнопки переключения темы
        themeToggle.addEventListener('click', toggleTheme);
        console.log('Theme toggle button found and event listener attached.');
    } else {
        console.warn('Theme toggle button not found. Make sure the element with id "theme-toggle" exists.');
    }
});

// Функция для обновления темы на конкретной странице
function updatePageTheme() {
    const isDarkTheme = document.documentElement.classList.contains('dark-theme');
    
    // Отправляем событие изменения темы
    const themeChangeEvent = new CustomEvent('themeChange', { detail: { darkMode: isDarkTheme } });
    document.dispatchEvent(themeChangeEvent);
    
    // Проверяем текущий путь страницы и вызываем соответствующие обработчики
    const currentPath = window.location.pathname;
    
    // Вызываем функцию обновления темы для кошелька, если мы на странице кошелька
    if (currentPath.includes('/payments/wallet/') || currentPath.includes('/wallet/')) {
        if (typeof applyThemeToWallet === 'function') {
            applyThemeToWallet();
        }
    }
    
    // Вызываем соответствующую функцию в зависимости от темы
    if (isDarkTheme) {
        fixElementsInDarkTheme();
    } else {
        fixElementsInLightTheme();
    }
    
    // Для страниц чата требуется дополнительная обработка
    if (currentPath.includes('/chat/') || currentPath.includes('/messages/') || currentPath.includes('/conversation/')) {
        // Применяем дополнительные стили для чата
        applyChatTheme(isDarkTheme);
    }
}

// Функция для обновления стилей чата
function applyChatTheme(isDarkTheme) {
    // Выбираем все основные элементы чата
    const chatElements = {
        container: document.querySelectorAll('.chat-container'),
        messages: document.querySelectorAll('.chat-message:not(.outgoing)'),
        outgoingMessages: document.querySelectorAll('.chat-message.outgoing'),
        contactInfo: document.querySelectorAll('.contact-info'),
        contactAvatars: document.querySelectorAll('.contact-avatar'),
        headers: document.querySelectorAll('.conversation-header, .chat-header, .notifications-header'),
        messageItems: document.querySelectorAll('.messages-list li, .notifications-list li')
    };
    
    if (isDarkTheme) {
        // Применяем темные стили
        chatElements.container.forEach(el => {
            el.style.backgroundColor = '#2a2a2a';
            el.style.borderColor = '#444';
        });
        
        chatElements.messages.forEach(el => {
            el.style.backgroundColor = '#333';
            el.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.3)';
            el.style.color = '#FFFFFF';
        });
        
        chatElements.outgoingMessages.forEach(el => {
            el.style.backgroundColor = '#700000';
        });
        
        chatElements.contactInfo.forEach(el => {
            el.style.backgroundColor = '#2a2a2a';
            el.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';
            el.style.borderColor = '#444';
            el.style.color = '#FFFFFF';
        });
        
        chatElements.contactAvatars.forEach(el => {
            el.style.backgroundColor = '#444';
            el.style.color = '#f0f0f0';
        });
        
        chatElements.headers.forEach(el => {
            el.style.backgroundColor = '#333';
            el.style.borderBottom = '2px solid var(--primary-color)';
        });
        
        chatElements.messageItems.forEach(el => {
            el.style.borderBottomColor = '#444';
        });
    } else {
        // Применяем светлые стили
        chatElements.container.forEach(el => {
            el.style.backgroundColor = '#f0f0f0';
            el.style.borderColor = '#ddd';
        });
        
        chatElements.messages.forEach(el => {
            el.style.backgroundColor = '#fff';
            el.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
            el.style.color = '';
        });
        
        chatElements.outgoingMessages.forEach(el => {
            el.style.backgroundColor = 'var(--primary-color)';
            el.style.color = 'white';
        });
        
        chatElements.contactInfo.forEach(el => {
            el.style.backgroundColor = '#f9f9f9';
            el.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
            el.style.borderColor = '';
            el.style.color = '';
        });
        
        chatElements.contactAvatars.forEach(el => {
            el.style.backgroundColor = '#e0e0e0';
            el.style.color = '#333';
        });
        
        chatElements.headers.forEach(el => {
            el.style.backgroundColor = 'var(--primary-color)';
            el.style.borderBottom = '';
        });
        
        chatElements.messageItems.forEach(el => {
            el.style.borderBottomColor = '#eee';
        });
    }
}

// Проверяем наличие MutationObserver для наблюдения за изменениями в DOM
if (typeof MutationObserver !== 'undefined') {
    // Наблюдаем за изменениями класса в html, чтобы отлавливать изменения темы
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                updatePageTheme();
            }
        });
    });
    
    // Начинаем наблюдение за html элементом
    observer.observe(document.documentElement, { attributes: true });
} 

// Добавляем обработчик события window.onload
window.onload = function() {
    // Вызываем updatePageTheme после полной загрузки страницы
    // Это обеспечит правильную стилизацию всех элементов, особенно для чата
    updatePageTheme();
    
    // Проверяем наличие полей ввода в чате и добавляем им автоматическое изменение высоты
    const chatInput = document.getElementById('id_content');
    if (chatInput) {
        // Автоматическое изменение высоты поля ввода
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Применяем текущие стили в зависимости от темы
        updatePageTheme();
    }
}; 