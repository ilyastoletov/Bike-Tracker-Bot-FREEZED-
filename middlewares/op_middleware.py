from typing import Any, Awaitable, Dict, Callable
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberLeft
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.db_api.main import Database

db = Database()

class OpMiddleware(BaseMiddleware):
    async def __call__(self,handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],event: Message, data: Dict[str, Any]) -> Any:
        channels = db.get_channels(all=False)
        bot = data.get('bot')
        links = []
        for channel in channels:
            check = await bot.get_chat_member(channel[1], event.from_user.id)
            if type(check) is ChatMemberLeft:
                links.append(channel[2])
        if links:
            kb = InlineKeyboardBuilder()
            for link in links:
                kb.row(InlineKeyboardButton(text='Подписаться ➕', url=f'{link}'))
            kb.row(InlineKeyboardButton(text='Проверить подписку ✅', callback_data='check_sub'))
            await event.answer('Чтобы начать пользоваться ботом, нужно подписаться на каналы спонсоров', reply_markup=kb.as_markup())
            raise CancelHandler()
        else:
            await handler(event, data)



