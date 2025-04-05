import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from utils.message_tracking import *


router = Router()


# Получение имени пользователя и его username
def get_user_info(message: Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "[без username]"
    return {
        "username": username,
        "user_id": message.from_user.id,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# Обработка входящих сообщений из супергрупп
@router.message(F.chat.type == ChatType.SUPERGROUP)
async def read_messages(message: Message):
    user_info = get_user_info(message)
    now = datetime.now()

    if 0 <= now.hour < 12:
        if user_info["user_id"] not in cache_night:
            cache_night[user_info["user_id"]] = user_info
    else:
        if user_info["user_id"] not in cache_day:
            cache_day[user_info["user_id"]] = user_info

    print(f"[{user_info['timestamp']}] {user_info['username']}: {message.text or '[не текстовое сообщение]'}")
