from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.reply import menu_kb
from keyboards.reply import admin_kb
from utils.db_api.main import Database
from mailing import Mailing
from filters.admin import Adm
import datetime

mail = Mailing()
router = Router()
db = Database()

@router.message(Adm(), commands='admin')
async def admin_start(message:types.Message,state:FSMContext):
    await message.answer("Привет админ",reply_markup=admin_kb)

@router.message(Adm(), text='Назад')
async def back_admin(m: types.Message):
    await m.answer('Админ меню', reply_markup=admin_kb)

@router.message(text='В меню')
async def admin_cancel(message:types.Message,state:FSMContext):
    await state.clear()
    await message.answer("Меню",reply_markup=menu_kb())

@router.message(Adm(), text='📊Статистика')
async def stats_admin(m: types.Message):
    utcnow = datetime.datetime.utcnow()
    today = datetime.datetime(
        year=utcnow.year, month=utcnow.month, day=utcnow.day
    )
    yesterday = today - datetime.timedelta(days=1)
    week_ago = today - datetime.timedelta(days=7)

    registered_today = db.analyze_registered(today, utcnow)
    registered_source = db.analyze_registered(today, utcnow, "AND source is not null")
    registered_yesterday = db.analyze_registered(yesterday, today)
    registered_yesterday_source = db.analyze_registered(yesterday, today, "AND source is not null")
    invented_friends = db.analyze_registered(today, utcnow, "AND source ~ '^[0-9\.]+$'")
    invented_friends_yesterday = db.analyze_registered(yesterday, today, "AND source ~ '^[0-9\.]+$'")
    registered_week = db.analyze_registered(week_ago, today)
    all = db.analyze_all(active=False)
    all_active = db.analyze_all(active=True)
    blocked_today = db.analyze_blocked(today, utcnow)
    blocked_yesterday = db.analyze_blocked(yesterday, today)

    active_today = db.analyze_today(today, utcnow)

    text = f"""
📉Статистика Стандофф
    
    Всего юзеров: {all} 
    Активных: {all_active} 

💹Зарегистрировались
    За день: {registered_today} (С рекл {registered_source - invented_friends})
    За вчера: {registered_yesterday} (С рекл {registered_yesterday_source - invented_friends_yesterday})
    За неделю {registered_week}

🧾Саморост
    За день: {registered_today - (registered_source - invented_friends)}
    С друзей за день: {invented_friends}
    За вчера: {registered_yesterday - (registered_yesterday_source - invented_friends_yesterday)}
    C друзей за вчера: {invented_friends_yesterday}
    

⛔️Заблокировали
    За день: {blocked_today}
    За вчера {blocked_yesterday}

🧽Чистыми
    Чистый приход за день: {registered_today - blocked_today}
    Чистый приход за вчера: {registered_yesterday - blocked_yesterday}
    
🌟 Актив за день: {active_today}
    """
    await m.answer(text)
