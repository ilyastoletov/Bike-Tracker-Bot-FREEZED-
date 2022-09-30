import datetime
from aiogram import types, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from keyboards.reply import sub_kb
from utils.db_api.main import Database
from states.admin import AdminSub
from keyboards.inline import admin_sub_kb
from filters.admin import Adm
import logging

router = Router()
db = Database()

@router.message(Adm(), text='🧩Обяз.подписка')
async def admin_sub_start(message: types.Message, state: FSMContext):
    await state.set_state(AdminSub.admin_sub)
    channels = db.get_channels(all=True)
    await message.answer("Каналы: ", reply_markup=sub_kb)
    if channels:
        for channel in channels:
            admin_kb = admin_sub_kb('Удалить', callback_data=f'delete_{channel[1]}')
            await message.answer(
                f"Канал: {channel[1]}\nСсылка: {channel[2]}",reply_markup=admin_kb)
    else:
        await message.answer("Каналов нет")

@router.message(Adm(), text='✅Добавить Канал', state=AdminSub.admin_sub)
async def admin_sub_add_id(message: types.Message, state: FSMContext):
    await message.answer("Введите id канала, либо перешлите с него пост")
    await state.set_state(AdminSub.admin_sub_id)

@router.message(Adm(), state=AdminSub.admin_sub_id)
async def admin_sub_add_link(message: types.Message, state: FSMContext):
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
    else:
        channel_id = message.text
    await state.update_data(channel_id=channel_id)
    await state.set_state(AdminSub.admin_sub_link)
    await message.answer("Введите ссылку: ")

@router.message(Adm(), state=AdminSub.admin_sub_link)
async def admin_sub_add_start(message: types.Message, state: FSMContext):
    channel_link = message.text

    await state.update_data(channel_link=channel_link)
    await state.set_state(AdminSub.admin_sub_start)
    await message.answer("Введите дату начала: \n\nПример: <code>2018-06-29 08:15</code> ")

@router.message(Adm(), state=AdminSub.admin_sub_start)
async def admin_sub_add_end(message: types.Message, state: FSMContext):
    date_start = message.text
    try:
        cheak = datetime.datetime.strptime(date_start, '%Y-%m-%d %H:%M')
    except ValueError:
        await message.answer("Не верный формат даты\n\nПример: <code>2018-06-29 08:15</code> ")
        return

    await state.update_data(date_start=date_start)
    await state.set_state(AdminSub.admin_sub_end)
    await message.answer("Введите дату конца (время должно быть по UTC!): \n\nПример: <code>2018-06-29 08:15</code> ")

@router.message(Adm(), state=AdminSub.admin_sub_end)
async def admin_sub_add(message: types.Message, state: FSMContext):
    data = await state.get_data()

    date_start = data.get('date_start')
    channel_link = data.get('channel_link')
    channel_id = data.get('channel_id')
    date_end = message.text
    try:
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d %H:%M')
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d %H:%M')
    except ValueError:
        await message.answer('Не верный формат даты\n\nПример: <code>2018-06-29 08:15</code> ')
        return
    await state.set_state(AdminSub.admin_sub)
    try:
        print(channel_id, channel_link, date_start, date_end)
        db.add_channel(channel_id, channel_link, date_start, date_end)
        await message.answer('Канал добавлен')
    except Exception as e:
        logging.error(e)
        await message.answer('Ошибка')

    await admin_sub_start(message, state)

@router.callback_query(Adm(), Text(text_startswith='delete_'))
async def admin_sub_delete(callback: types.CallbackQuery):
    channel_id = int(callback.data.split('_')[-1])
    db.delete_channel(channel_id)
    await callback.message.edit_text('Канал удален', reply_markup=None)
