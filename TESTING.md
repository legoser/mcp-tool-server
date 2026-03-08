# API Testing Guide

Есть два способа тестирования API:

## 1. REST Client в VS Code (Рекомендуется)

### Установка расширения
1. Откройте VS Code
2. Перейти в Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Найти "REST Client" (автор: Huachao Mao)
4. Установить расширение

### Использование
1. Откройте файл `api.http` в VS Code
2. Вы увидите ссылку "Send Request" над каждым запросом
3. Кликните на "Send Request" для выполнения
4. Результат откроется в боковой панели

### Особенности
- ✅ Очень удобно и быстро
- ✅ Встроено в VS Code
- ✅ Сохраняет историю
- ✅ Поддерживает переменные

### Переменные в api.http
```
@host = http://localhost:3344
@session_id = YOUR_SESSION_ID
```

---

## 2. Python CLI Client

### Интерактивный режим
```bash
python test_client.py
```

Меню команд:
- 1. Health check
- 2. Create session
- 3. List tools
- 4-12. Вызовы инструментов
- 0. Выход

### Автоматические тесты
```bash
python test_client.py --auto
```

Запускает полный набор тестов и выводит результаты.

### Использование в VS Code
1. Нажмите F5 (Debug)
2. Выберите "Test Client (Interactive)" или "Test Client (Automated)"
3. Используйте интерпретатор VS Code

---

## 3. Запуск сервера на фоне

### Terminal 1 - Запустить сервер
```bash
python -m uvicorn src.main_sse:app --port 3344
```

### Terminal 2 - Запустить тесты
```bash
# Интерактивно
python test_client.py

# Или автоматически
python test_client.py --auto
```

---

## Workflow с VS Code

### Оптимальный способ:
1. **Terminal 1**: `python -m uvicorn src.main_sse:app --port 3344`
2. **Откройте `api.http`** и начните с "Send Request"
3. **Сначала**: GET /health
4. **Потом**: GET /sse (для создания сессии)
5. **Скопируйте sessionId** из ответа в переменную @session_id в api.http
6. **Используйте** остальные запросы для тестирования

---

## Примеры команд

### Из терминала (curl)
```bash
# Health check
curl http://localhost:3344/health

# Создать сессию и получить session_id
curl http://localhost:3344/sse

# Вызвать инструмент
curl -X POST "http://localhost:3344/message?session_id=YOUR_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {"name": "get_current_time", "arguments": {}}
  }'
```

---

## Проблемы и решения

### Проблема: "Connection refused"
**Решение:** Убедитесь, что сервер запущен:
```bash
python -m uvicorn src.main_sse:app --port 3344
```

### Проблема: "Invalid session"
**Решение:** Создайте новую сессию через `/sse` endpoint

### Проблема: "Tool not found"
**Решение:** Сначала запустите "List tools" опцию для проверки доступных инструментов

---

## Быстрый старт

```bash
# 1. Установить зависимости (если еще не установлены)
pip install -e .

# 2. Terminal 1 - Запустить сервер
python -m uvicorn src.main_sse:app --port 3344

# 3. Terminal 2 - Запустить тесты
python test_client.py --auto
```

✅ Готово! Должны пройти все тесты.
