from datetime import datetime, timedelta, timezone

from src.core.logging import get_logger

logger = get_logger(__name__)


async def get_current_time() -> str:
    """Возвращает текущую дату и время по Москве (UTC+3)."""
    moscow_tz = timezone(timedelta(hours=3))
    now = datetime.now(moscow_tz)
    return now.strftime("%d.%m.%Y %H:%M:%S (МСК)")
