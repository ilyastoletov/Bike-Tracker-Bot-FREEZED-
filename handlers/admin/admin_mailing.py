from aiogram import types, Router, Bot
from aiogram.fsm.context import FSMContext
from keyboards.reply import admin_kb
from mailing import Mailing
from utils.db_api.main import Database
from states.admin import Admin, AdminSender
from keyboards.reply import broadcast_kb
from filters.admin import Adm

router = Router()
mail = Mailing()
db = Database()

@router.message(Adm(), text='Рассылка')
async def admin_sender_start(message :types.Message,state :FSMContext):
    await state.set_state(AdminSender.admin_sender)
    await message.answer(
        '<b>Отправьте контент для запуска</b>' ,reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(Adm(), state=AdminSender.admin_sender)
async def admin_sender_content(message :types.Message, state :FSMContext, bot: Bot):
    s_message = message.copy()
    await state.update_data(message=s_message)
    await bot.copy_message(message.from_user.id, message.chat.id, message.message_id
                                   ,reply_markup=message.reply_markup)
    await message.answer('Запускаем?' ,reply_markup=broadcast_kb())
    await state.set_state(AdminSender.admin_sender_send)

@router.message(Adm(), state=AdminSender.admin_sender_send)
async def admin_sender_run(message :types.Message ,state :FSMContext, bot: Bot):
    if message.text == 'Да':
        users = db.get_users()
        data = await state.get_data()
        msg = data.get('message')
        await message.answer("Запущено!" ,reply_markup=admin_kb)
        await state.set_state(Admin.admin)
        await mail.run(
            bot=bot,
            message=msg,
            users=users
        )
        await message.answer('Запущеная рассылка завершена!')
    else:
        await message.answer('Назад' ,reply_markup=admin_kb)
        await state.set_state(Admin.admin)

@router.message(Adm(), text='📈Рассылка Статистика')
async def admin_analyst_sender(message:types.Message):
    text = f'''
    ✅Рассылка: {mail.success_send}/{mail.count_users}
❌Заблокировали бота: {mail.count_blocks}'''
    await message.answer(text)
