from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable, Dict
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.db_api.main import Database

db = Database()

class ViewMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],event: Message, data: Dict[str, Any]) -> Any:
        views = db.get_views()
        for view in views:
            if not db.check_view(view[1], event.from_user.id):
                await handler(event, data)
                kb = InlineKeyboardBuilder()
                kb.add(InlineKeyboardButton(text=f'{view[4]}', url=f'{view[5]}'))
                await event.answer(view[3], reply_markup=kb.as_markup())
                db.update_view_counter(view[1], event.from_user.id)
                raise StopIteration()
        await handler(event, data)