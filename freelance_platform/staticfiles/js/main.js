// Main JavaScript for WorkBy

// Функция для инициализации всех тултипов
function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// Функция для инициализации всех поповеров
function initPopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

// Функция для инициализации форм переключения языка
function initLanguageForms() {
    // Находим все формы переключения языка
    const languageForms = document.querySelectorAll('.language-form');
    
    languageForms.forEach(form => {
        // Находим кнопку внутри формы
        const button = form.querySelector('button');
        // Находим выбранный язык
        const langInput = form.querySelector('input[name="language"]');
        
        if (button && langInput) {
            // Добавляем обработчик на клик по кнопке
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Получаем выбранный язык
                const selectedLang = langInput.value;
                
                // Получаем текущий URL
                let currentPath = window.location.pathname;
                
                // Отправляем форму, но не переходим по ее действию
                fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    credentials: 'same-origin'
                }).then(response => {
                    // После отправки формы, перенаправляем пользователя на URL с правильным префиксом языка
                    let newPath = currentPath;
                    
                    // Удаляем существующий префикс языка, если он есть
                    const langPrefixes = ['/en/', '/ru/', '/kk/'];
                    for (const prefix of langPrefixes) {
                        if (currentPath.startsWith(prefix)) {
                            currentPath = currentPath.substring(prefix.length - 1);
                            break;
                        }
                    }
                    
                    // Если начинается с '/', сохраняем, иначе добавляем '/'
                    if (!currentPath.startsWith('/')) {
                        currentPath = '/' + currentPath;
                    }
                    
                    // Если выбранный язык не является языком по умолчанию (английский), добавляем префикс
                    if (selectedLang !== 'en') {
                        newPath = '/' + selectedLang + currentPath;
                    } else {
                        newPath = currentPath;
                    }
                    
                    // Перенаправляем на новый URL
                    window.location.href = newPath;
                });
            });
        }
    });
}

// Функция для анимации числовых счетчиков
function animateCounters() {
    const counters = document.querySelectorAll('.counter-value');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 секунды
        const step = target / (duration / 16); // 16ms - примерно один кадр при 60fps
        
        let count = 0;
        const updateCounter = () => {
            count += step;
            
            // Когда достигаем целевого значения, останавливаем анимацию
            if (count >= target) {
                counter.textContent = target.toLocaleString();
                return;
            }
            
            counter.textContent = Math.floor(count).toLocaleString();
            requestAnimationFrame(updateCounter);
        };
        
        updateCounter();
    });
}

// Функция для обработки переключения типа метода оплаты
function handlePaymentMethodToggle() {
    const methodSelector = document.querySelector('.method-type-select');
    if (!methodSelector) return;
    
    const toggleFields = (value) => {
        const cardFields = document.querySelectorAll('.card-field');
        const bankFields = document.querySelectorAll('.bank-field');
        
        if (value === 'card') {
            cardFields.forEach(field => field.closest('.mb-3').style.display = 'block');
            bankFields.forEach(field => field.closest('.mb-3').style.display = 'none');
        } else if (value === 'bank') {
            cardFields.forEach(field => field.closest('.mb-3').style.display = 'none');
            bankFields.forEach(field => field.closest('.mb-3').style.display = 'block');
        } else {
            cardFields.forEach(field => field.closest('.mb-3').style.display = 'none');
            bankFields.forEach(field => field.closest('.mb-3').style.display = 'none');
        }
    };
    
    // Начальное состояние
    toggleFields(methodSelector.value);
    
    // Обработка изменений
    methodSelector.addEventListener('change', (e) => {
        toggleFields(e.target.value);
    });
}

// Функция для инициализации фильтров для списка проектов
function initProjectFilters() {
    const filterForm = document.getElementById('project-filter-form');
    if (!filterForm) return;
    
    const applyFilters = () => {
        filterForm.submit();
    };
    
    // Применяем фильтры при изменении селекторов
    const selects = filterForm.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', applyFilters);
    });
    
    // Применяем фильтры при нажатии на чекбоксы
    const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
}

// Функция для обработки динамического добавления полей этапов в контрактах
function initMilestoneFormset() {
    const addBtn = document.getElementById('add-milestone');
    if (!addBtn) return;
    
    const formsetContainer = document.getElementById('milestone-formset');
    const totalForms = document.getElementById('id_milestone_set-TOTAL_FORMS');
    
    addBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        const formCount = parseInt(totalForms.value);
        
        // Клонируем первую форму
        const emptyForm = document.querySelector('.milestone-form').cloneNode(true);
        
        // Обновляем индексы в id и name атрибутах
        emptyForm.innerHTML = emptyForm.innerHTML.replace(/-0-/g, `-${formCount}-`);
        emptyForm.innerHTML = emptyForm.innerHTML.replace(/_0_/g, `_${formCount}_`);
        
        // Очищаем значения полей
        const inputs = emptyForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Добавляем новую форму в контейнер
        formsetContainer.appendChild(emptyForm);
        
        // Увеличиваем счетчик форм
        totalForms.value = formCount + 1;
    });
}

// Функция для переключения светлой/темной темы
function initThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;
    
    themeToggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
        
        // Сохраняем предпочтение в localStorage
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('dark-mode', isDarkMode);
    });
    
    // Применяем сохраненное предпочтение при загрузке
    const savedDarkMode = localStorage.getItem('dark-mode') === 'true';
    if (savedDarkMode) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
    } else {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
    }
}

// Функция для инициализации чата через веб-сокеты
function initChatWebSocket() {
    const chatContainer = document.getElementById('chat-container');
    if (!chatContainer) return;
    
    const conversationId = chatContainer.getAttribute('data-conversation-id');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-message');
    
    // Создаем WebSocket соединение
    const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const chatSocket = new WebSocket(
        `${wsProtocol}${window.location.host}/ws/chat/${conversationId}/`
    );
    
    // Обработка входящих сообщений
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        addMessageToChat(data.message, data.sender_id, data.sender_username, data.timestamp);
        
        // Прокручиваем чат вниз
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };
    
    // Обработка закрытия соединения
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
    
    // Отправка сообщения при нажатии на кнопку
    sendBtn.addEventListener('click', function() {
        sendMessage();
    });
    
    // Отправка сообщения при нажатии Enter
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Функция отправки сообщения
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        }
    }
    
    // Функция добавления сообщения в чат
    function addMessageToChat(message, senderId, senderUsername, timestamp) {
        const currentUserId = chatContainer.getAttribute('data-user-id');
        const isSent = senderId.toString() === currentUserId.toString();
        
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isSent ? 'sent' : 'received');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('content');
        
        if (!isSent) {
            const senderElement = document.createElement('div');
            senderElement.classList.add('sender');
            senderElement.textContent = senderUsername;
            messageContent.appendChild(senderElement);
        }
        
        const textElement = document.createElement('div');
        textElement.classList.add('text');
        textElement.textContent = message;
        messageContent.appendChild(textElement);
        
        const timeElement = document.createElement('div');
        timeElement.classList.add('time');
        
        const date = new Date(timestamp);
        timeElement.textContent = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageContent.appendChild(timeElement);
        messageElement.appendChild(messageContent);
        
        chatContainer.appendChild(messageElement);
    }
    
    // Прокручиваем чат вниз при инициализации
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Функция для обновления количества непрочитанных сообщений/уведомлений
function updateUnreadCounters() {
    // Проверяем, авторизован ли пользователь
    if (!document.querySelector('.message-badge')) return;
    
    fetch('/chat/api/unread/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const messageCount = document.getElementById('message-count');
        const notificationCount = document.getElementById('notification-count');
        
        if (messageCount) {
            messageCount.textContent = data.unread_messages;
            if (data.unread_messages > 0) {
                messageCount.style.display = 'inline-block';
            } else {
                messageCount.style.display = 'none';
            }
        }
        
        if (notificationCount) {
            notificationCount.textContent = data.unread_notifications;
            if (data.unread_notifications > 0) {
                notificationCount.style.display = 'inline-block';
            } else {
                notificationCount.style.display = 'none';
            }
        }
    })
    .catch(error => console.error('Error updating unread counters:', error));
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация компонентов Bootstrap
    initTooltips();
    initPopovers();
    
    // Инициализация пользовательских функций
    initLanguageForms();
    animateCounters();
    handlePaymentMethodToggle();
    initProjectFilters();
    initMilestoneFormset();
    initThemeToggle();
    initChatWebSocket();
    
    // Обновление счетчиков непрочитанных сообщений и уведомлений
    updateUnreadCounters();
    
    // Обновляем счетчики каждые 60 секунд
    setInterval(updateUnreadCounters, 60000);
}); 