# Импорт коллекции в Postman

## 📥 Способ 1: Импорт через Postman UI (Рекомендуется)

### Шаг 1: Откройте Postman
- Скачайте [Postman](https://www.postman.com/downloads/)
- Установите и запустите приложение

### Шаг 2: Импортируйте коллекцию
1. Нажмите кнопку **"Import"** в левом верхнем углу
2. Выберите вкладку **"File"**
3. Выберите файл `postman_collection.json` из этого проекта
4. Нажмите **"Import"**

### Шаг 3: Импортируйте Environment (опционально)
1. Нажмите на значок **"⚙️"** (Settings) справа вверху
2. Выберите **"Environments"**
3. Нажмите **"Import"**
4. Выберите файл `postman_environment.json`

### Шаг 4: Выберите окружение
1. В правом верхнем углу найдите dropdown "No Environment"
2. Выберите **"MCP Tools Server"**

---

## 🎯 Способ 2: Использование Postman Web
1. Откройте https://web.postman.co/
2. Нажмите **"Create"** → **"Import"**
3. Выберите файл **`postman_collection.json`**

---

## 📋 Структура коллекции

```
├── 🏥 Health Check
│   └── Health                    # GET /health
├── 🔌 Session Management
│   └── Create SSE Session        # GET /sse (автоматически сохраняет session_id)
├── 📚 Tools Management
│   └── List Tools               # POST /message (tools/list)
├── 🔧 Tool Calls
│   ├── Get Current Time
│   ├── Get Random Joke
│   ├── Get Random Quote
│   ├── Get Random Fact
│   ├── Web Search
│   ├── Web Fetch
│   ├── Generate Text (Ollama)
│   ├── Chat with AI (Ollama)
│   └── List Ollama Models
└── ❌ Error Cases
    ├── Invalid Session
    ├── Method Not Found
    └── Tool Not Found
```

---

## 🚀 Быстрый старт

### 1. Запустите сервер
```bash
python -m uvicorn src.main_sse:app --port 3344
```

### 2. Импортируйте коллекцию
- Откройте Postman
- Import → `postman_collection.json`

### 3. Запустите тесты
1. Нажмите на папку **"🏥 Health Check"**
2. Нажмите на 3 точки и выберите **"Run folder"**

### 4. Или запустите вручную
1. Откройте **"🏥 Health Check"** → **"Health"**
2. Нажмите **"Send"**
3. Откройте **"🔌 Session Management"** → **"Create SSE Session"**
4. Нажмите **"Send"** (это автоматически сохранит session_id)
5. Тестируйте инструменты из **"🔧 Tool Calls"**

---

## 🧪 Встроенные тесты

Каждый запрос имеет тесты в закладке **"Tests"**:
- ✅ Проверка статус кода
- ✅ Проверка структуры ответа
- ✅ Автоматическое сохранение переменных

Для запуска всех тестов:
1. Нажмите на коллекцию **"MCP Tools Server API"**
2. Выберите **"Run"** (справа внизу папочки)
3. Нажмите **"Run MCP Tools Server API"**

---

## 🔑 Автоматизм session_id

При запуске **"Create SSE Session"** коллекция автоматически:
1. Подключается к SSE endpoint
2. Парсит ответ
3. Извлекает `sessionId`
4. Сохраняет в переменную `{{session_id}}`

Теперь все остальные запросы используют этот session_id автоматически!

---

## 📊 Переменные окружения

| Переменная | Значение | Используется |
|-----------|----------|-------------|
| `host` | `http://localhost:3344` | во всех URL |
| `session_id` | автоматически | в query параметрах |

### Изменить хост:
1. Выберите environment **"MCP Tools Server"**
2. Нажмите на значок **"⚙️"** → **"Environments"**
3. Отредактируйте переменную `host`

---

## 🐛 Troubleshooting

### Проблема: "Could not get any response"
**Решение:** Убедитесь, что сервер запущен:
```bash
python -m uvicorn src.main_sse:app --port 3344
```

### Проблема: "Invalid session" при вызове инструментов
**Решение:** Запустите **"Create SSE Session"** перед вызовом других методов

### Проблема: Переменные не сохраняются
**Решение:** Убедитесь, что вы выбрали правильное окружение в dropdown сверху

### Проблема: Тесты не работают
**Решение:** Откройте вкладку **"Console"** (Ctrl+Alt+C) для просмотра логов

---

## 💡 Советы

### Сохранение результаты в Postman
- Нажмите **"Save Response"** → **"Save as example"**
- Можно просматривать сохраненные примеры позже

### Запуск коллекции по расписанию
- Используйте **"Postman Monitor"** (Premium feature)
- Или используйте **Newman** (CLI инструмент):
```bash
npm install -g newman
newman run postman_collection.json -e postman_environment.json
```

### Экспорт результатов
- При запуске коллекции нажмите **"Export Results"** после завершения

---

## 📚 Дополнительные ресурсы

- [Postman Documentation](https://learning.postman.com/)
- [Collections Guide](https://learning.postman.com/docs/collections/collections-overview/)
- [Testing](https://learning.postman.com/docs/writing-scripts/test-scripts/)
- [Newman CLI](https://learning.postman.com/docs/running-collections/using-newman-cli/)
