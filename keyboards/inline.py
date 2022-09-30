from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_sub_kb(text:str,callback_data:str):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=text, callback_data=callback_data))
    return kb.as_markup()

async def admin_view_kb(text:str,callback_data:str,text2:str,callback_data2:str):
    admin_sub_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text,callback_data=callback_data),InlineKeyboardButton(text=text2,callback_data=callback_data2)]])
    return admin_sub_kb