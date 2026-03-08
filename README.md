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

# Установить зависимости
pip install -r requirements.txt

# Скопировать конфигурацию
cp .env.example .env
```

## Запуск

### Stdio режим (для Claude Desktop, MCP Inspector)

```bash
python -m src.main
```

### SSE режим (для удалённого доступа)

```bash
uvicorn src.main_sse:app --port 3344
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

### Юнит-тесты (с моками)

```bash
PYTHONPATH=. python tests/test_tools_unit.py
```

### Интеграционные тесты (stdio)

```bash
PYTHONPATH=. python tests/test_all_tools.py
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
