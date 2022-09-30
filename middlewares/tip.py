from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message
from utils.db_api.main import Database
from keyboards.inline import under_kb

class TipMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],event: Message, data: Dict[str, Any]) -> Any:
        tip = Database().tip_viewed(event.from_user.id)
        if not tip:
            await event.answer('<b>Чтобы транслировать свою геолокацию:</b>\n\nПрикрепить вложение -> локация -> транслировать мою геопозицию', reply_markup=under_kb())
            await handler(event, data)
        else:
            await handler(event, data)