from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_sub_kb(text:str,callback_data:str):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=text, callback_data=callback_data))
    return kb.as_markup()

def under_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Я понял, скрыть подсказку', callback_data='understand'))
    return kb.as_markup()

def choose_sport_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='🏃 Бег', callback_data='sport_running'))
    kb.add(InlineKeyboardButton(text='🚴‍♂️ Вело', callback_data='sport_bike'))
    kb.add(InlineKeyboardButton(text='🚶 Ходьба', callback_data='sport_walk'))
    kb.adjust(1)
    return kb.as_markup()

def ready() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Готов!', callback_data='ready'))
    return kb.as_markup()

def ride_settings() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='⏸️ Пауза', callback_data='pause'), InlineKeyboardButton(text='⏹ Завершить', callback_data='stop'))
    return kb.as_markup()

async def admin_view_kb(text:str,callback_data:str,text2:str,callback_data2:str):
    admin_sub_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text,callback_data=callback_data),InlineKeyboardButton(text=text2,callback_data=callback_data2)]])
    return admin_sub_kb