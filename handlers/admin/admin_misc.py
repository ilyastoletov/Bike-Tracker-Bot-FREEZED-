from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from filters.admin import Adm
from utils.db_api.main import Database
from states.admin import Admin

router = Router()
db = Database()


@router.message(Adm(), text='Выгруз')
async def upload_users(message: Message):
    users_str = ''
    users = db.get_users()
    for user in users:
        users_str += f'{user[0]}\n'
    with open('data/users.txt', 'w') as file: file.write(users_str)
    await message.answer_document(document=FSInputFile(path='data/users.txt'), caption='Вот ваш список пользователей')


@router.message(Adm(), text='💰 Добавить голду на баланс 💰')
async def increase_gold_admin(m: Message, state: FSMContext):
    await m.answer('Введи юзернейм пользователя (без @) и количество золота через запятую')
    await state.set_state(Admin.gold)

@router.message(Adm(), state=Admin.gold)
async def gold_increased(m: Message):
    data = m.text.split(', ')
    db.increase_gold_adm(data[0], data[1])
    await m.answer(f'Успешно начислено {data[1]}G пользователю {data[0]}!')


