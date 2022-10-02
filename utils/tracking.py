from aiogram import Bot
from keyboards.inline import ride_settings
from utils.gaversinus import count_gaversinus

class Tracking:

    def __init__(self):
        self.sport = None
        self.bot = None
        self.message_id = None
        self.user_id = None
        self.lat_start = None
        self.lon_start = None
        self.status = '🟢 Активна'
        self.metres = 0
        self.duration = 0
        self.calories = 0

    async def __edit_message(self):
        await self.bot.edit_message_text(chat_id=self.user_id,
                                         text=f'📐 Метры: <b>{self.metres}</b>\n🧭 Длительность: <b>{self.duration}</b> мин.\n🔥 Сожжено каллорий: <b>{self.calories}</b>\n\nСтатус: <b>{self.status}</b>',
                                         message_id=self.message_id, reply_markup=ride_settings())

    async def get_parametres(self, bot: Bot, sport_type: str, message_id: int, user_id: int, lat: float, lon: float):
        self.bot = bot
        self.sport = sport_type
        self.lat_start = lat
        self.lon_start = lon
        self.message_id = message_id
        self.user_id = user_id
        await self.__edit_message()
        return

    async def count_metres(self, lat: float, lon: float):
        if self.status == '🟢 Активна':
            distance = count_gaversinus(self.lat_start, self.lon_start, lat, lon)
            self.metres += distance
            self.duration += 1
            self.lat_start = lat
            self.lon_start = lon
            await self.__edit_message()

