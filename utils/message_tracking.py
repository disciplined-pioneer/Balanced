import asyncio
from datetime import datetime, timedelta
from cachetools import TTLCache


# Кэши: дневной и ночной
CACHE_TTL_SECONDS = 12 * 60 * 60  # 12 часов
cache_day = TTLCache(maxsize=10000, ttl=CACHE_TTL_SECONDS)
cache_night = TTLCache(maxsize=10000, ttl=CACHE_TTL_SECONDS)


# Асинхронный помощник: ждет до нужного времени
async def wait_until(target_hour: int, target_minute: int = 1):
    now = datetime.now()
    future = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if future <= now:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())


# Фоновая задача: каждые 12 часов делает отчет и очищает кэш
async def reporter_loop():
    while True:
        now = datetime.now()

        if 0 <= now.hour < 12:
            await wait_until(12, 1)
            users = dict(cache_day)
            cache_day.clear()
            period = "НОЧЬ (12:01 – 00:00)"
        else:
            await wait_until(0, 1)
            users = dict(cache_night)
            cache_night.clear()
            period = "ДЕНЬ (00:01 – 12:00)"

        print(f"\n[{period}] Пользователи, написавшие впервые за период:")
        if users:
            for user_info in users.values():
                print(f" - {user_info['username']} (ID: {user_info['user_id']}) | Время: {user_info['timestamp']}")
        else:
            print(" - Никто не писал")
        print()

