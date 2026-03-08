# MCP Tools Server

Асинхронный MCP сервер с набором инструментов для LLM.

## Возможности

| Инструмент | Описание |
|------------|----------|
| `get_current_time` | Текущее время (МСК) |
| `get_random_joke` | Случайная шутка |
| `get_random_quote` | Случайная цитата |
| `get_random_fact` | Случайный факт |
| `web_search` | Поиск в интернете (DuckDuckGo HTML) |
| `web_fetch` | Загрузка веб-страниц |
| `generate_text` | Генерация текста (Ollama) |
| `chat_with_ai` | Чат с AI (Ollama) |
| `list_ollama_models` | Список моделей Ollama |

## Установка

```bash
# Клонировать репозиторий
cd mcp-tools-server

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Установить зависимости продакшина
pip install -r requirements.txt

# (Опционально) Установить dev зависимости для тестирования/линтинга
pip install -r requirements-dev.txt

# Скопировать конфигурацию
cp .env.example .env
```

### Требования зависимостей

**Production** (`requirements.txt`):

- `mcp` — MCP Protocol SDK
- `httpx` — Асинхронный HTTP клиент
- `pydantic-settings` — Конфигурация из .env
- `pydantic` — Валидация данных
- `fastapi` — Web framework
- `sse-starlette` — SSE transport
- `uvicorn` — ASGI сервер
- `beautifulsoup4` — HTML парсинг

**Development** (`requirements-dev.txt`):

- `pytest`, `pytest-asyncio` — Тестирование
- `ruff` — Линтинг и форматирование

## Запуск

### Stdio режим (для Claude Desktop, MCP Inspector)

```bash
python -m src.main
```

### SSE режим (для удалённого доступа)

```bash
uvicorn src.main_sse:app --port 3344
```

## Docker

### Сборка образа

```bash
# Собрать образ с multi-stage build на Alpine (оптимизирован по размеру)
docker build -t mcp-tools-server:latest .

# Собрать с определённым тегом версии
docker build -t mcp-tools-server:0.1.0 .

# Проверить размер образа
docker images | grep mcp-tools-server
```

### Запуск контейнера

#### Базовый запуск (SSE сервер)

```bash
docker run -p 3344:3344 \
  --env-file .env \
  --name mcp-server \
  mcp-tools-server:latest
```

#### С локальным хостом (для доступа к Ollama)

```bash
docker run -p 3344:3344 \
  --env-file .env \
  --network host \
  --name mcp-server \
  mcp-tools-server:latest
```

#### С пробросом в локальную сеть (для домашней лаборатории)

```bash
docker run -p 192.168.1.100:3344:3344 \
  --env-file .env \
  --name mcp-server \
  mcp-tools-server:latest
```

> Замените `192.168.1.100` на IP вашего хоста в локальной сети

#### С Docker Compose

Создайте файл `docker-compose.yml`:

```yaml
version: '3.9'

services:
  mcp-server:
    build: .
    container_name: mcp-tools-server
    ports:
      - "3344:3344"
    environment:
      OPENAI_BASE_URL: http://ollama:11434/v1
      OPENAI_API_KEY: ollama
      LLM_MODEL_NAME: llama3
    env_file: .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3344/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    
    # Опционально, если Ollama запущен в отдельном контейнере
    # depends_on:
    #   - ollama
    
    # networks:
    #   - mcp-network

  # ollama:
  #   image: ollama/ollama:latest
  #   container_name: ollama
  #   volumes:
  #     - ollama_data:/root/.ollama
  #   environment:
  #     OLLAMA_HOST: 0.0.0.0:11434
  #   networks:
  #     - mcp-network

# volumes:
#   ollama_data:

# networks:
#   mcp-network:
#     driver: bridge
```

Запуск:

```bash
docker-compose up -d
```

### Docker образ оптимизация

Dockerfile использует **multi-stage build на Alpine**:

1. **Builder stage** (`python:3-alpine`): Компилирует зависимости в виртуальном окружении
2. **Runtime stage** (`python:3-alpine`): Копирует только необходимое в финальный образ

**Alpine преимущества:**

- Base image: ~50 MB (вместо ~300 MB slim образа)
- Финальный размер: ~80-120 MB (вместо 300-400 MB с slim)
- Экономия ≈ 70% от размера контейнера
- Снижение времени загрузки и использования ресурсов

**Результаты оптимизации:**

- Исключены инструменты сборки после builder stage (build-base, python3-dev)
- Удалены кэши pip и apk
- Использован ultra-slim базовый образ Alpine
- Добавлен non-root user (uid 1000) для безопасности
- Healthcheck встроен в образ

### Переменные окружения для Docker

Создайте `.env` файл перед запуском:

```bash
# Ollama (локальная LLM)
OPENAI_BASE_URL=http://192.168.57.139:11434/v1
OPENAI_API_KEY=ollama
LLM_MODEL_NAME=llama3

# Brave Search API (опционально)
BRAVE_API_KEY=your_api_key
```

### Проверка здоровья контейнера

```bash
# Проверить статус healthcheck
docker ps | grep mcp-server

# Просмотреть логи
docker logs -f mcp-server

# Проверить вручную
curl http://localhost:3344/health
```

## Конфигурация

Создайте файл `.env`:

```bash
# Ollama (локальная LLM)
OPENAI_BASE_URL=http://192.168.57.139:11434/v1
OPENAI_API_KEY=ollama
LLM_MODEL_NAME=llama3

# Brave Search API (опционально, для большего количества провайдеров)
BRAVE_API_KEY=your_api_key
```

## Поисковые провайдеры

Модуль `src/utils/search_providers.py` содержит:

- `DuckDuckGoProvider` — API DuckDuckGo (JSON)
- `DuckDuckGoHTMLProvider` — HTML DuckDuckGo (с rate limiting)
- `BraveSearchProvider` — Brave Search (требует API ключ)

Функция `search_with_ddg()` использует DuckDuckGo HTML с rate limiting (30 зап/мин).

## Тестирование

Убедитесь что установлены dev зависимости:

```bash
pip install -r requirements-dev.txt
```

### Юнит-тесты (с моками)

```bash
PYTHONPATH=. python -m pytest tests/test_tools_unit.py -v
```

### Интеграционные тесты (stdio)

```bash
PYTHONPATH=. python -m pytest tests/test_all_tools.py -v
```

### Запуск всех тестов

```bash
pytest
```

### Линтинг и форматирование

```bash
# Проверить код с ruff
ruff check .

# Форматировать код
ruff format .
```

## SSE API (примеры curl)

### Шаг 1: Подключиться к SSE и получить session_id

```bash
# Подключаемся к SSE и получаем session_id
curl -N http://localhost:3344/sse
```

В ответе будет поле `session_id`, например:

```json
event: endpoint
data: {"session_id": "abc-123-def", "server": ...}
```

### Шаг 2: Использовать session_id в запросах

```bash
SESSION="ваш-session-id"

# tools/list
curl -s -X POST "http://localhost:3344/messages/?session_id=$SESSION" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# get_current_time
curl -s -X POST "http://localhost:3344/messages/?session_id=$SESSION" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_current_time","arguments":{}}}'

# web_search
curl -s -X POST "http://localhost:3344/messages/?session_id=$SESSION" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"web_search","arguments":{"query":"Python","num_results":3}}}'

# web_fetch
curl -s -X POST "http://localhost:3344/messages/?session_id=$SESSION" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"web_fetch","arguments":{"url":"http://example.com"}}}'
```

## Структура проекта

```shell
mcp-tools-server/
├── src/
│   ├── main.py            # Stdio entry
│   ├── main_sse.py       # SSE entry (port 3344)
│   ├── server.py         # MCP Server
│   ├── core/
│   │   ├── config.py     # Настройки
│   │   └── logging.py    # Логирование
│   ├── tools/
│   │   ├── time_tools.py       # get_current_time
│   │   ├── http_tools.py       # joke, quote, fact
│   │   ├── web_tools.py        # web_search, web_fetch
│   │   ├── ollama_tools.py     # generate_text, chat, list
│   │   ├── weather_tools.py    # weather
│   │   └── registry.py         # Регистрация инструментов
│   └── utils/
│       ├── rate_limiter.py     # Rate limiting
│       ├── search_providers.py # Провайдеры поиска (DuckDuckGo, Brave)
│       ├── web_fetcher.py       # Загрузка/парсинг страниц
│       └── http_client.py      # Общий HTTP клиент
├── tests/
│   ├── test_tools_unit.py      # Юнит-тесты (моки)
│   └── test_all_tools.py       # Интеграционные тесты
├── pyproject.toml
└── README.md
```

## Требования

- Python 3.10+
- Ollama (опционально, для AI инструментов)

## Лицензия

MIT
