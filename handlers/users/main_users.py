from aiogram import Router, Bot
from aiogram.filters import Text, ContentTypesFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from middlewares.tip import TipMiddleware
from utils.db_api.main import Database
from keyboards.inline import choose_sport_kb, ready
from states.main import BikeStates as States
from utils.tracking import Tracking
import asyncio

track = Tracking()
db = Database()
r = Router()
r.message.middleware(TipMiddleware())
@r.message(text='🚲 Начать заезд')
async def start_ride(m: Message, state: FSMContext):
    await state.set_state(States.choose_sport)
    await m.answer('Выберете тип занятия:', reply_markup=choose_sport_kb())

@r.callback_query(Text(text_startswith='sport_'), state=States.choose_sport)
async def sports_choosing(c: CallbackQuery, state: FSMContext):
    await c.message.delete()
    await state.update_data(sport=c.data.split('_')[1])
    await c.message.answer('Теперь пришли мне свою "живую локацию"')
    await state.set_state(States.location_start)

@r.message(state=States.location_start, content_types='location')
async def location_got(m: Message, state: FSMContext):
    await m.answer('Готовы начать занятие?', reply_markup=ready())
    await state.update_data(lat=m.location.latitude, lon=m.location.longitude)
    await state.set_state(States.ready)

@r.callback_query(state=States.ready, text='ready')
async def start_ride(c: CallbackQuery, state: FSMContext, bot: Bot):
    await c.message.edit_text('Занятие начато!')
    data = await state.get_data()
    await track.get_parametres(bot=bot, sport_type=data['sport'], message_id=c.message.message_id, user_id=c.from_user.id, lat=data['lat'], lon=data['lon'])
    await state.set_state(States.ride)

@r.edited_message(state=States.ride)

@r.callback_query(text='understand')
async def tip_notshow(c: CallbackQuery):
    await c.message.delete()
    db.tip_change(c.from_user.id)