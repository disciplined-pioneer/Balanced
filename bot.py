import asyncio
from settings import settings
from telethon.sync import TelegramClient
from datetime import datetime, timedelta, timezone

api_id = settings.bot.API_ID
api_hash = settings.bot.API_HASH
group_username = settings.bot.GROUP_NAME

async def check_messages():
    async with TelegramClient("session_name", api_id, api_hash) as client:

        last_check_time = datetime.now(timezone.utc) - timedelta(minutes=5) #hours=1)  # Проверяем за последний час
        async for message in client.iter_messages(group_username):

            # Проверяем, если дата сообщения позже, чем last_check_time
            if message.date > last_check_time:
                sender_id = message.sender_id
                if sender_id is not None:

                    # Получаем объект пользователя
                    sender = await client.get_entity(sender_id)
                    username = f"@{sender.username}" if sender.username else None

                    print(f"[{message.date}] ID: {sender_id}, Username: {username}, Text: {message.text}")
                else:
                    print(f"[{message.date}] Отправитель не найден (пользователь удалён или это бот), Text: {message.text}")

async def scheduler():
    while True:
        await check_messages()
        await asyncio.sleep(5)
        print("\n")

if __name__ == "__main__":
    try:
        asyncio.run(scheduler())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен 🛑\n")