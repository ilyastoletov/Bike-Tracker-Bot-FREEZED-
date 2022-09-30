from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='🚲 Начать заезд')
    kb.button(text='🗂 Мои заезды')
    kb.row(KeyboardButton(text='📊 Статистика'))
    return kb.as_markup(resize_keyboard=True)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊Статистика"),KeyboardButton(text="📈Рассылка Статистика")],
        [KeyboardButton(text="🧩Обяз.подписка"),KeyboardButton(text="📔Сводка"),KeyboardButton(text="Добавка")],
        [KeyboardButton(text="Выгруз"),KeyboardButton(text="Рассылка"),KeyboardButton(text="Показы")],
        [KeyboardButton(text='💰 Добавить голду на баланс 💰')],
        [KeyboardButton(text="В меню")]

    ], resize_keyboard=True
)

def broadcast_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text='Да'), KeyboardButton(text='Нет'))
    return kb.as_markup(resize_keyboard=True)

sub_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Добавить Канал")
        ],
        [KeyboardButton(text="Назад")]

    ], resize_keyboard=True
)

views_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Добавить Показы")
        ],
        [KeyboardButton(text="Назад")]

    ], resize_keyboard=True
)
