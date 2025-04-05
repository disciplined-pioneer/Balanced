import logging
import asyncio
from aiogram import Dispatcher

from core.bot import bot
from bot.handlers import routers
from bot.handlers.message_tracking import reporter_loop


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_routers(*routers)


async def main():
    asyncio.create_task(reporter_loop())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("\nБот запущен ✅\n")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен 🛑\n")
    except Exception as e:
        print(f"\n❌ Возникла ошибка : {e}\n")