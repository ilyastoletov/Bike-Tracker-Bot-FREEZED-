from aiogram import Router
from aiogram.fsm.context import FSMContext
from utils.db_api.main import Database
from states.main import BikeStates as States
from aiogram.types import Message

r = Router()
db = Database()

@r.message(state=States.registration)
async def registration(m: Message, state: FSMContext):
    data = m.text.split(", ")
    if all(isinstance(x, int) for x in data):
        pass
    else:
        await m.answer('Введите числовое значение!')
        return

