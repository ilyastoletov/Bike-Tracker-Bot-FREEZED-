from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from utils.db_api.main import Database
from states.admin import Admin, AdminSummary
from filters.admin import Adm
from keyboards.reply import admin_kb

router = Router()
db = Database()

@router.message(Adm(), text='Добавка')
async def admin_summary_set(message: types.Message, state: FSMContext):
    await message.answer("👤Введите username: ")
    await state.set_state(AdminSummary.summary_set_username)

@router.message(Adm(), state=AdminSummary.summary_set_username)
async def admin_summary_set_username(message: types.Message, state: FSMContext):
    username = message.text
    if '@' in username:
        username = username.replace('@', '')
    await state.update_data(username=username)
    await message.answer("💸Введите цену: ")
    await state.set_state(AdminSummary.summary_set_price)

@router.message(Adm(), state=AdminSummary.summary_set_price)
async def admin_summary_set_price(message: types.Message, state: FSMContext):
    price = message.text
    if price.isdigit():
        await state.update_data(price=price)
        await state.set_state(AdminSummary.summary_set_name)
        await message.answer("🚀Введи рефку(англ буквами, без спец.знаков): ")
    else:
        await message.answer("Не число")

@router.message(Adm(), state=AdminSummary.summary_set_name)
async def admin_summary_set_source(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    source = message.text
    username = data.get('username')
    price = data.get('price')
    bot = await bot.get_me()

    text = f'''
👤Ник: {username}
💸Цена: {price}
🚀Рефка: {source}

👉 http://t.me/{bot.username}?start={source}

✅Добавлено'''

    db.add_ad(name=username, price=int(price), username=source)
    await message.answer(text)
    await state.set_state(Admin.admin)
    await message.answer("Админ меню", reply_markup=admin_kb)

@router.message(Adm(), text='📔Сводка')
async def admin_summary(message: types.Message):
    await message.answer('<i>Собираю статистику...</i>')
    referals = db.get_referals()
    if referals:
        text = []
        referal_counter = 0
        counter = 0

        spent = 0
        for referal in referals:
            source = referal[1]
            count = referal[4]
            line = f'Рефералка: <b>{source}</b> : <b>{count}</b> человек'
            if source.isdigit():
                referal_counter = referal_counter + count
            else:
                source_data = db.get_ad(name=source)
                if source_data:
                    if int(count) > 0:
                        passed_op = db.passed_op(source_data[2])
                        line = f'👤 @{source} | 🚀Реф: <b>{source_data[2]}</b> | 💵<b>{source_data[3]}</b> | Зашло <b>{count}</b> |  Прошли ОП <b>{passed_op[0][0]}</b> | В {round(int(source_data[3]) / int(count), 1)} рублей   '
                    else:
                        line = f'👤 @{source} | 🚀Реф: <b>{source_data[2]}</b> | 💵<b>{source_data[3]}</b> | Зашло <b>{count}</b> | В (ошибка подсчета) рублей   '
                    spent = spent + source_data[3]
                    counter = counter + count
                text.append(line + '\n')
        if int(counter) > 0:
            text.append(f'💰С рекламы зашло: {counter}\nПотрачено: {spent}\nВ среднем в {round(spent / counter, 1)}рубля')
        else:
            text.append(f'💰С рекламы зашло: {counter}\nПотрачено: {spent}\nВ среднем в (ошибка подсчета) рубля')
        while text:
            temp = text[0:10]
            await message.answer("\n".join(temp))
            del text[0:10]

    else:
        await message.answer("Тут ничего нету")
