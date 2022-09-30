from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message
from utils.db_api.main import Database
db = Database()

class NoReg(BaseFilter):
    async def __call__(self, m: Message, command: CommandObject):
        reg = db.exist_user(m.from_user.id)
        if not reg:
            return True
