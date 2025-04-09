import asyncio
from cachetools import TTLCache
from aiogram.types import Message
from datetime import datetime, timedelta
from integrations.google_sheets.google_sheets import filling_table

# Время жизни кэшей — сутки (так как проверка раз в день)
CACHE_TTL_SECONDS = 25 * 60 * 60  # 25 часов

cache_morning = TTLCache(maxsize=100_000, ttl=CACHE_TTL_SECONDS)
cache_evening = TTLCache(maxsize=100_000, ttl=CACHE_TTL_SECONDS)

# Ожидание до 00:01
async def wait_until_midnight():
    now = datetime.now()
    future = now.replace(hour=0, minute=1, second=0, microsecond=0)
    if future <= now:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())


# Получение имени пользователя и его username
def get_user_info(message: Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "[без username]"
    return {
        "username": username,
        "user_id": message.from_user.id,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():
    while True:
        await wait_until_midnight()
        
        now = datetime.now()
        weekday = now.weekday()

        # 5 = суббота, 6 = воскресенье — пропускаем
        if weekday >= 5:
            continue

        # Утро: 00:01 – 12:00
        if cache_morning:
            for user_info in cache_morning.values():
                print(f" - {user_info['username']} (ID: {user_info['user_id']}) | Время: {user_info['timestamp']}")
        else:
            print(" - Никто не писал")
        
        # Вечер: 15:00 – 00:00
        if cache_evening:
            for user_info in cache_evening.values():
                print(f" - {user_info['username']} (ID: {user_info['user_id']}) | Время: {user_info['timestamp']}")
        else:
            print(" - Никто не писал")
        
        # Заполнение всей таблицы и очистка кеша
        try:
            morning_data = {user_info['user_id']: user_info for user_info in cache_morning.values()}
            evening_data = {user_info['user_id']: user_info for user_info in cache_evening.values()}
            filling_table(morning_data, evening_data)

        except Exception as e:
            print(f"\nПроизошла ошибка: {e}\n")

        cache_morning.clear()
        cache_evening.clear()

        print()
