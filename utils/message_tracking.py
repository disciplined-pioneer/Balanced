import asyncio
from cachetools import TTLCache
from aiogram.types import Message
from datetime import datetime, timedelta


# Кэши: дневной и ночной
CACHE_TTL_SECONDS = 12 * 60 * 60  # 12 часов

cache_morning = TTLCache(maxsize=10000, ttl=CACHE_TTL_SECONDS)
cache_evening = TTLCache(maxsize=10000, ttl=CACHE_TTL_SECONDS)


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

        # Обрабатываем утро
        if 0 <= now.hour < 12:
            await wait_until(12, 1)
            users = dict(cache_morning)
            cache_morning.clear()
            period = "УТРО (00:01 – 12:00)"

        # Обрабатываем вечер
        else:
            await wait_until(0, 1)
            users = dict(cache_evening)
            cache_evening.clear()
            period = "НОЧЬ (12:01 – 00:00)"

        print(f"\n[{period}] Пользователи, написавшие впервые за период:")
        if users:
            for user_info in users.values():
                print(f" - {user_info['username']} (ID: {user_info['user_id']}) | Время: {user_info['timestamp']}")
        else:
            print(" - Никто не писал")
        print()


# Получение имени пользователя и его username
def get_user_info(message: Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "[без username]"
    return {
        "username": username,
        "user_id": message.from_user.id,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }