from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from utils.message_tracking import *


router = Router()


# Обработка входящих сообщений из супергрупп
@router.message(F.chat.type == ChatType.SUPERGROUP)
async def read_messages(message: Message):
    user_info = get_user_info(message)
    now = datetime.now()

    if 0 <= now.hour < 12:
        if user_info["user_id"] not in cache_morning:
            cache_morning[user_info["user_id"]] = user_info
            
    elif 15 <= now.hour <= 23:
        if user_info["user_id"] not in cache_evening:
            cache_evening[user_info["user_id"]] = user_info
            
    print(f"[{user_info['timestamp']}] {user_info['username']} ({user_info['user_id']}): {message.text or '[не текстовое сообщение]'}")
