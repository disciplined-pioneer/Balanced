import asyncio
from aiogram.types import Message
from datetime import datetime, timedelta

from integrations.google_sheets.scoring import update_habits_and_ids
from integrations.google_sheets.accrual_fines_users import accrual_fines_users

# Используем обычные словари
cache_morning = {}
cache_evening = {}

# Храним время последней очистки
last_clear_time = datetime.now()


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


# Функция для заполнения всей таблицы
def filling_table(cache_morning: dict, cache_evening: dict):
    print('-'*40)
    print('Заполняем данные...')
    all_user_ids = update_habits_and_ids(cache_morning, cache_evening)
    print('Баллы были начислены')
    accrual_fines_users(all_user_ids)
    print('Штрафы были начислены')
    print('-'*40)


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():
    global last_clear_time

    while True:
        await wait_until_midnight()

        # Проверка — не прошло ли 25 часов с момента последней очистки
        if datetime.now() - last_clear_time >= timedelta(hours=25):
            cache_morning.clear()
            cache_evening.clear()
            last_clear_time = datetime.now()
            print('Прошло 25 часов — кеш очищен')

        # Определяем день недели вчерашнего дня
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_weekday = yesterday.weekday()

        # Если вчера была суббота или воскресенье — пропускаем обработку
        if yesterday_weekday >= 5:
            cache_morning.clear()
            cache_evening.clear()
            continue
        
        try:
            morning_data = {user_info['user_id']: user_info for user_info in cache_morning.values()}
            evening_data = {user_info['user_id']: user_info for user_info in cache_evening.values()}
            filling_table(morning_data, evening_data)

        except Exception as e:
            print(f"\nПроизошла ошибка: {e}\n")
