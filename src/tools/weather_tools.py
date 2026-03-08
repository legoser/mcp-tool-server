from datetime import date, timedelta

from pydantic import BaseModel, Field

from ..core.logging import get_logger
from ..utils.http_client import get_http_client

logger = get_logger(__name__)

MAX_DAYS = 21  # TODO move to settings


class WeatherInput(BaseModel):
    city: str = Field(description="Название населённого пункта")
    days: int = Field(default=1, ge=1, le=MAX_DAYS, description="Количество дней прогноза (1-21)")
    forecast_date: date | None = Field(
        default=None, description="Дата прогноза (не далее 21 дня от текущей). Формат: YYYY-MM-DD"
    )


def get_weather_description(code: int) -> str:
    descriptions = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Туман",
        51: "Лёгкая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        56: "Лёгкий ледяной дождь",
        57: "Сильный ледяной дождь",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        66: "Лёгкий ледяной дождь",
        67: "Сильный ледяной дождь",
        71: "Небольшой снег",
        73: "Умеренный снег",
        75: "Сильный снег",
        77: "Снежные зёрна",
        80: "Небольшие ливни",
        81: "Умеренные ливни",
        82: "Сильные ливни",
        85: "Небольшие снежные ливни",
        86: "Сильные снежные ливни",
        95: "Гроза",
        96: "Гроза с градом",
        99: "Сильная гроза с градом",
    }
    return descriptions.get(code, f"Код {code}")


async def get_weather(city: str, days: int = 1, forecast_date: str | None = None) -> str:
    """Получает прогноз погоды для указанного населённого пункта.

    Args:
        city: Название населённого пункта
        days: Количество дней прогноза (1-21, по умолчанию 1)
        forecast_date: Дата прогноза в формате YYYY-MM-DD (не далее 21 дня от текущей)
    """
    today = date.today()
    target_date: date | None = None

    if forecast_date:
        try:
            target_date = date.fromisoformat(forecast_date)
        except ValueError:
            return "Ошибка: неверный формат даты. Используйте формат YYYY-MM-DD"

        if target_date < today:
            return "Ошибка: дата не может быть в прошлом"
        if (target_date - today).days > MAX_DAYS:
            return f"Ошибка: дата не далее {MAX_DAYS} дней от текущей"

    if target_date:
        days_ahead = (target_date - today).days + 1
        days = min(days, days_ahead)

    client = await get_http_client()

    try:
        geo_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ru", "format": "json"},
        )

        if geo_resp.status_code != 200:
            return f"Ошибка геокодирования: статус {geo_resp.status_code}"

        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return f"Город '{city}' не найден"

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        tz = location.get("timezone", "UTC")
        city_name = location.get("name", city)
        country = location.get("country", "")

        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
            "timezone": tz,
            "forecast_days": days,
        }

        if target_date:
            end_date = target_date + timedelta(days=days - 1)
            weather_params["start_date"] = target_date.isoformat()
            weather_params["end_date"] = end_date.isoformat()
            del weather_params["forecast_days"]

        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params=weather_params,
        )

        if weather_resp.status_code != 200:
            return f"Ошибка получения погоды: статус {weather_resp.status_code}"

        weather_data = weather_resp.json()
        daily = weather_data.get("daily", {})

        times = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        codes = daily.get("weathercode", [])

        if not times:
            return "Нет данных о погоде"

        output = f"Прогноз погоды: {city_name}"
        if country:
            output += f", {country}"
        output += f"\n{'=' * 40}\n"

        for i in range(len(times)):
            day_date = date.fromisoformat(times[i])
            day_name = "Сегодня" if day_date == today else day_date.strftime("%a, %d %b")

            output += f"\n📅 {day_name}\n"
            output += f"   🌡️  {min_temps[i]:.1f}°...{max_temps[i]:.1f}°C\n"
            output += f"   🌥️  {get_weather_description(codes[i])}\n"
            if precip[i] > 0:
                output += f"   💧 Осадки: {precip[i]:.1f} мм\n"

        return output

    except Exception as e:
        logger.error(f"Weather error: {e}")
        return f"Ошибка получения погоды: {str(e)}"
