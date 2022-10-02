from aiogram.filters import BaseFilter
import data.config as config
from aiogram.types import Message

class Adm(BaseFilter):
    async def __call__(self, m: Message) -> bool:
        return m.from_user.id in config.ADMINS