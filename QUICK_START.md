# 🚀 Quick Start Guide - MCP Tools Server

## 📦 Установка (требуется один раз)

```bash
# В корне проекта
pip install -e .
```

## 🏄 Запуск сервера

### Вариант 1: Stdio (для Claude Desktop, MCP Inspector)
```bash
python -m src
# или
fastmcp dev src/main.py
```

### Вариант 2: HTTP/SSE (для REST API)
```bash
python -m uvicorn src.main_sse:app --port 3344
# Сервер доступен на http://localhost:3344
```

## ✅ Тестирование (выберите один вариант)

### 1️⃣ REST Client в VS Code (самый быстрый)

```bash
# Предоставляет расширение "REST Client"
# Откройте файл: api.http
# Кликните "Send Request" над каждым запросом
```

**Плюсы:**
- ✨ Супер быстро и удобно
- 📁 Встроено в VS Code
- 💾 Сохраняет историю

### 2️⃣ Python Test Client (интерактивный)

```bash
# Интерактивное меню
python test_client.py

# Или автоматические тесты
python test_client.py --auto
```

**Плюсы:**
- 🎮 Интерактивное управление
- 🔧 Полный контроль параметров
- 📊 Видно всё в логах

### 3️⃣ Postman (рекомендуется для команды)

```bash
# Автоматический запуск тестов (Python)
python run_postman_tests.py

# Или через bash
./run_postman_tests.sh

# Или в Postman App
# File → Import → postman_collection.json
```

**Плюсы:**
- 👥 Легко делиться с командой
- 🤖 Автоматизация session_id
- 📈 История тестов
- 🔐 Сохранение переменных окружения

## 📊 Полный workflow

```bash
# Терминал 1: Запустить сервер
python -m uvicorn src.main_sse:app --port 3344

# Терминал 2: Запустить тесты
python run_postman_tests.py
# или
python test_client.py --auto
# или
# Откройте api.http в VS Code и кликните Send
```

## 🔍 Основные endpointi

| Method | URL | Описание |
|--------|-----|---------|
| GET | `/health` | Проверка здоровья |
| GET | `/sse` | Создать SSE сессию |
| POST | `/message?session_id=X` | Вызвать инструмент |

## 📝 Примеры запросов

### 1. Создать сессию
```bash
curl http://localhost:3344/sse
# Ответ: SSE stream с sessionId
```

### 2. Список инструментов
```bash
curl -X POST http://localhost:3344/message?session_id=YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

### 3. Вызвать инструмент
```bash
curl -X POST http://localhost:3344/message?session_id=YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "call_tool",
    "params": {
      "name": "get_current_time",
      "arguments": {}
    }
  }'
```

## 📚 Дополнительная документация

- 📖 [CLAUDE.md](CLAUDE.md) - Технические детали проекта
- 🧪 [TESTING.md](TESTING.md) - Полное руководство по тестированию
- 📮 [POSTMAN.md](POSTMAN.md) - Работа с Postman
- 🤖 [POSTMAN_AUTOMATION.md](POSTMAN_AUTOMATION.md) - Автоматизация в Postman
- 🛠️ [IMPORT_STRUCTURE.md](IMPORT_STRUCTURE.md) - Структура импорта

## 🐛 Отладка

### Проверить логи
```bash
# Сервер выводит логи в stderr
python -m uvicorn src.main_sse:app --log-level debug
```

### Мониторит запросы
```bash
# Используйте Postman Console (Cmd+Alt+C)
# Или встроенный логгер VS Code
```

### Полезные команды
```bash
# Проверить здоровье сервера
curl http://localhost:3344/health

# Форматировать код
ruff format .

# Проверить линтер
ruff check .

# Запустить unit тесты
pytest
```

## 💡 Советы

1. **Для разработки:** используйте `api.http` в VS Code - это самый быстрый способ
2. **Для команды:** используйте Postman - легко делиться и автоматизировать
3. **Для CI/CD:** используйте `python run_postman_tests.py` или `./run_postman_tests.sh`
4. **Для отладки:** включите `--log-level debug` при запуске сервера

## 🆘 Помощь

Если что-то не работает:

1. **Проверьте обслуживаемость сервера:**
   ```bash
   curl http://localhost:3344/health
   # Должен вернуть: {"status": "ok"}
   ```

2. **Проверьте логи:**
   ```bash
   # В терминале где запущен сервер должны быть логи
   ```

3. **Перезагрузите сессию:**
   - В Postman: Кликните "Create SSE Session" снова
   - В test_client.py: Выйдите и повторно запустите

4. **Проверьте зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

---

**Версия:** 1.0  
**Последнее обновление:** 2024-01-XX  
**Статус:** ✅ Production Ready
