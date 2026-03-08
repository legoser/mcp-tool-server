# Postman Automation Guide - MCP Tools Server

## 🎯 Автоматизация сессии

Коллекция Postman теперь полностью автоматизирована для работы с MCP Tools Server SSE.

## 📋 Что происходит автоматически

### 1️⃣ Create SSE Session (Создание сессии)

**Pre-request скрипт:**
```javascript
// Очищает старый session_id перед каждым запросом
pm.environment.set('session_id', 'PENDING');
```

**Test скрипт:**
- ✅ Проверяет HTTP 200
- ✅ Проверяет `Content-Type: text/event-stream`
- ✅ Парсит SSE ответ построчно
- ✅ Извлекает `sessionId` из `data.result.sessionId`
- ✅ Сохраняет в переменную окружения `{{session_id}}`
- ✅ Сохраняет в глобальные переменные (для использования в других папках)
- ✅ Добавляет timestamp

**Результат:**
```
✓ Session ID найден: f47ac10b-58cc-4372-a567-0e02b2c3d479
✓ Session saved to environment and globals
```

### 2️⃣ Остальные запросы (Tools, Calls)

Все запросы автоматически:
- ✅ Используют сохраненный `{{session_id}}`
- ✅ Передают его как query-параметр: `?session_id={{session_id}}`
- ✅ Имеют Pre-request скрипты для проверки наличия session_id

## 🚀 Как использовать

### Вариант 1: Ручное тестирование

1. **Откройте Postman**
2. **Импортируйте коллекцию:**
   - File → Import
   - Выберите `postman_collection.json`
   
3. **Создайте окружение или используйте дефолтное:**
   - Create Environment (или используйте `postman_environment.json`)
   - Установите переменную `host`: `http://localhost:3344`

4. **Запустите "Create SSE Session":**
   - Кликните Send
   - Посмотрите в Response tab
   - Проверьте Environment - там будет `session_id`

5. **Запустите любой другой запрос:**
   - Session ID автоматически подставится
   - Запрос выполнится с правильной сессией

### Вариант 2: Collection Runner

```bash
# Установить Newman (CLI для Postman)
npm install -g newman

# Запустить всю коллекцию
newman run postman_collection.json \
  --environment postman_environment.json \
  --iteration-count 1
```

### Вариант 3: CI/CD Pipeline

**GitHub Actions:**
```yaml
- name: Run API tests
  run: |
    npm install -g newman
    newman run postman_collection.json \
      --environment postman_environment.json \
      --reporters cli,json
```

## 📊 Структура Postman коллекции

```
MCP Tools Server API/
├── 🏥 Health Check
│   └── Health                    # GET /health
│
├── 🔌 Session Management
│   └── Create SSE Session        # GET /sse (с автоматизацией)
│
├── 🛠️ Tools
│   ├── List Tools               # POST /message + tools/list
│   └── [Other tools...]         # Все доступные инструменты
│
├── 📞 Tool Calls
│   ├── Get Current Time
│   ├── Get Random Quote
│   ├── Get Random Joke
│   ├── Get Random Fact
│   ├── Web Search
│   ├── Web Fetch
│   ├── List Ollama Models
│   ├── Generate Text (Ollama)
│   └── Chat with AI (Ollama)
│
├── ❌ Error Cases
│   ├── Invalid Session ID
│   ├── Non-existent Tool
│   └── [Other error scenarios...]
│
└── 🔐 Authentication (future)
    ├── [Token-based auth tests]
    └── [OAuth tests]
```

## 🔍 Переменные окружения

### Основные переменные:

| Переменная | Значение | Описание |
|-----------|----------|---------|
| `host` | `http://localhost:3344` | Адрес сервера |
| `session_id` | `AUTO` | Заполняется автоматически из SSE |
| `timestamp` | `AUTO` | Заполняется при создании сессии |

### Как использовать переменные:

```
GET {{host}}/health
POST {{host}}/message?session_id={{session_id}}
Body: {"method": "tools/list"}
```

## 🧪 Тестирование при нулевом session_id

Если session_id не установлен или истёк:

1. **Pre-request скрипт выбросит ошибку:**
   ```
   ❌ Session ID не найден. Запустите Create SSE Session первым.
   ```

2. **Автоисправление:**
   - Вернитесь к "Create SSE Session"
   - Кликните Send
   - Session ID обновится
   - Повторите запрос

## 📝 Примеры скриптов

### Pre-request (проверка session_id):
```javascript
var sessionId = pm.environment.get('session_id');
if (!sessionId || sessionId === 'PENDING' || sessionId === '') {
  throw new Error('❌ Session ID не найден. Запустите Create SSE Session первым.');
}
```

### Test (сохранение переменной):
```javascript
if (data.result && data.result.sessionId) {
  // Сохраняем в переменную окружения
  pm.environment.set('session_id', data.result.sessionId);
  
  // Также сохраняем глобально (для других папок)
  pm.globals.set('session_id', data.result.sessionId);
  
  console.log('✓ Session saved');
}
```

### Test (валидация ответа):
```javascript
pm.test('Valid JSONRPC response', function() {
  var data = pm.response.json();
  pm.expect(data).to.have.property('jsonrpc', '2.0');
  pm.expect(data).to.have.property('id');
  pm.expect(data).to.have.property('result');
});
```

## 🐛 Отладка

### Включить логирование в Postman Console:

1. View → Show Postman Console (Cmd+Alt+C)
2. Кликните Send на любом запросе
3. Посмотрите вывод консоли

### Часто встречаемые ошибки:

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Session ID не найден | session_id не установлен | Запустите Create SSE Session |
| 404 на /message | Сессия приемени сервер перезагружен | Создайте новую сессию |
| Content-Type не text/event-stream | Неправильный endpoint | Используйте GET /sse |
| sessionId = null | SSE ответ некорректный | Проверьте логи сервера |

## 🔄 Full Workflow

1. **Запустить сервер:**
   ```bash
   # В одном терминале
   python -m uvicorn src.main_sse:app --port 3344
   ```

2. **Открыть Postman:**
   ```bash
   # В другом терминале
   postman
   ```

3. **Импортировать коллекцию:**
   - File → Import → `postman_collection.json`

4. **Выполнить сценарий:**
   - Кликнуть "Create SSE Session" → Session создана 🎉
   - Кликнуть "List Tools" → tools/list выполнена 🛠️
   - Кликнуть "Get Current Time" → tool выполнена ⏰
   - И так далее...

## 📦 Альтернативный импорт

**Через Postman App:**
```
1. Collections tab → + Create new
2. Switch to this workspace
3. Paste URL: file:///path/to/postman_collection.json
4. Or drag-and-drop файл
```

## 🎓 Дополнительные ресурсы

- [Postman Collections Docs](https://learning.postman.com/docs/sending-requests/managing-environments/)
- [Newman CLI](https://learning.postman.com/docs/running-collections/using-newman-cli/)
- [Pre-request Scripts](https://learning.postman.com/docs/writing-scripts/pre-request-scripts/)
- [Tests](https://learning.postman.com/docs/writing-scripts/test-scripts/)

---

**Версия:** 1.0  
**Дата:** 2024  
**Статус:** ✅ Production Ready
