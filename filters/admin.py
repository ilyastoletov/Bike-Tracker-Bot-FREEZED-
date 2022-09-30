from aiogram.filters import BaseFilter
from config import admin
from aiogram.types import Message

class Adm(BaseFilter):
    async def __call__(self, m: Message) -> bool:
        return m.from_user.id in admin