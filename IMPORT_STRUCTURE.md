# 🐍 Организация импортов для безотказного запуска

## Что было сделано (✅ Готово)

### 1. **Относительные импорты** 
Все абсолютные импорты `from src.server import ...` заменены на относительные:
```python
# ❌ ДО
from src.server import mcp
from src.core.logging import get_logger

# ✅ ПОСЛЕ (в файлах src/)
from .server import mcp
from .core.logging import get_logger
from ..core.logging import get_logger  # для подпапок
```

**Файлы обновлены:**
- src/main.py
- src/server.py
- src/tools/http_tools.py
- src/tools/time_tools.py
- src/tools/web_tools.py
- src/tools/ollama_tools.py

### 2. **Entry Point** (`src/__main__.py`)
Создан файл для запуска пакета как модуля:
```bash
python -m src
```

### 3. **Package Configuration** (`pyproject.toml`)
Добавлены:
- Автоматическое обнаружение пакетов (`setuptools`)
- Scripts entry point для команды `mcp-server`

---

## 🚀 Способы запуска проекта

### ✓ Способ 1: Python модуль (РЕКОМЕНДУЕТСЯ)
```bash
python -m src
```

### ✓ Способ 2: FastMCP Inspector (ДА, используй этот способ)
```bash
# Самый безопасный способ
fastmcp dev inspector python -m src

# ИЛИ (альтернатива)
fastmcp dev inspector src_for_fastmcp.py
```

### ✓ Способ 3: SSE Server (FastAPI)
```bash
python -m uvicorn src.main_sse:app --port 3344
```

### ✓ Способ 4: Прямой импорт (для скриптов)
```python
# Из корня проекта
from src.main import server_main
```

---

## ⚙️ Установка и настройка

### Обязательная установка (один раз)
```bash
cd /home/ej/Code/PetProjects/MCP-tools-server
pip install -e .  # editable mode
```
Это гарантирует, что пакет доступен везде.

### Проверка импортов
```bash
# Проверяет, что все импорты работают
python -c "from src.main import server_main; print('✓ OK')"
```

---

## 📋 Итоговая таблица совместимости

| Способ | Требует `pip install -e .` | Работает | Команда |
|--------|---------------------------|---------|---------|
| Python -m | ❌ Нет | ✅ Да | `python -m src` |
| FastMCP dev | ✅ Да | ✅ Да | `fastmcp dev inspector python -m src` |
| FastAPI/SSE | ❌ Нет | ✅ Да | `python -m uvicorn src.main_sse:app` |
| Import | ❌ Нет (из корня) | ✅ Да | `from src.main import ...` |

---

## 🔧 Если всё ещё не работает

### 1. Очистить кэш Python
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

### 2. Переустановить пакет
```bash
pip uninstall mcp-tools-server -y
pip install -e .
```

### 3. Проверить sys.path
```bash
python -c "import sys; print('\n'.join(sys.path))"
```
Должен содержать корневую папку проекта.

### 4. Использовать абсолютный путь
```bash
cd /home/ej/Code/PetProjects/MCP-tools-server
python -c "import sys; sys.path.insert(0, '.'); from src.main import server_main"
```

---

## 💡 Почему это работает?

**Относительные импорты + `__main__.py` + правильный `pyproject.toml`** гарантируют:
- ✅ Работает `python -m src`
- ✅ Работает FastMCP Inspector
- ✅ Работает прямой импорт
- ✅ Работает установленный пакет
- ✅ Работает везде, где есть Python
