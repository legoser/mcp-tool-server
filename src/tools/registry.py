from src.tools import http_tools, ollama_tools, time, web_tools


def get_all_tools() -> list:
    return [
        time.get_current_time,
        http_tools.get_random_joke,
        http_tools.get_random_quote,
        http_tools.get_random_fact,
        web_tools.web_search,
        web_tools.web_fetch,
        ollama_tools.generate_text,
        ollama_tools.chat_with_ai,
        ollama_tools.list_ollama_models,
    ]
