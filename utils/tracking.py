from aiogram import Bot
from keyboards.inline import ride_settings

class Tracking:

    def __init__(self):
        self.sport = None
        self.bot = None
        self.message_id = None
        self.user_id = None
        self.lat = None
        self.lon = None
        self.status = '🟢 Активна'
        self.metres = 0
        self.duration = 0
        self.calories = 0

    async def get_parametres(self, bot: Bot, sport_type: str, message_id: int, user_id: int, lat: int, lon: int):
        self.bot = bot
        self.sport = sport_type
        self.lat = lat
        self.lon = lon
        self.message_id = message_id
        self.user_id = user_id
        await self.bot.edit_message_text(chat_id=self.user_id, text=f'📐 Метры: <b>{self.metres}</b>\n🧭 Длительность: <b>{self.duration}</b> мин.\n🔥 Сожжено каллорий: <b>{self.calories}</b>\n\nСтатус: <b>{self.status}</b>', message_id=self.message_id, reply_markup=ride_settings())
        return