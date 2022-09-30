from uuid import uuid4
from aiogram import types, Router, Bot
import datetime
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from utils.db_api.main import Database
from keyboards.inline import admin_view_kb
from states.admin import Admin, AdminViews
from keyboards.reply import views_kb
from keyboards.reply import admin_kb
from filters.admin import Adm

db = Database()
router = Router()

@router.message(Adm(), text='Показы')
async def views_start(message: types.Message):
    views = db.get_views()
    await message.answer("Показы: " ,reply_markup=views_kb)
    if views:
        for view in views:
            utcnow = datetime.datetime.utcnow()
            admin_kb = await admin_view_kb('Удалить' ,callback_data=f'view_del_{view[1]}' ,text2='Сменить время'
                                           ,callback_data2=f'change_view_{view[1]}')
            await message.answer \
                (f"Показ: {view[1]}\nТекст: {view[3]}\nУвидело {view[6]}\nЗакончится через {view[7] - utcnow}\n\nКнопка текст: {view[4]}\nКнопка ссылка: {view[5]}"
                ,reply_markup=admin_kb ,disable_web_page_preview=True)
    else:
        await message.answer("Показов нет")

@router.message(Adm(), text='✅Добавить Показы')
async def views_get_text(message :types.Message ,state :FSMContext):
    await message.answer("Пришлите пост, можно только с 1 кнопкой!")
    await state.set_state(AdminViews.admin_text)

@router.message(Adm(), state=AdminViews.admin_text)
async def views_proccess_text(message :types.Message, state: FSMContext, bot: Bot):

    btn_text, btn_url = '', ''
    if message.reply_markup:
        btn = message.reply_markup.inline_keyboard[0][0]
        btn_text, btn_url = btn.text, btn.url
    text = message.html_text if message.html_text else ''

    utcnow = datetime.datetime.utcnow()
    tomorrow = utcnow + datetime.timedelta(days=1)


    db.add_view(
        view_uuid=str(uuid4()),
        message_id=message.message_id,
        text=text,
        btn_text=btn_text,
        btn_url=btn_url,
        end_time=tomorrow
    )
    await bot.copy_message(message.chat.id, message.chat.id, message.message_id
                                   ,reply_markup=message.reply_markup)
    print(message.reply_markup)
    await message.answer \
        ("Создан показ, если тут больше 1 кнопки, все кроме первой не будут добавлены\nЗавершится через 24 часа!"
        ,reply_markup=admin_kb)
    await state.set_state(Admin.admin)

@router.callback_query(Adm(), Text(text_contains='view_del'))
async def view_delete(callback :types.CallbackQuery):
    view_id = (callback.data.split('_')[2])
    db.delete_view(view_id)
    await callback.message.edit_text('Показ удален' ,reply_markup=None)

@router.callback_query(Text(text_contains='change_view_'))
async def view_change_date_input_minutes(callback :types.CallbackQuery ,state :FSMContext):
    view_id = (callback.data.split('_')[2])
    await state.update_data(view_id = view_id)
    await callback.message.answer('Напишите через сколько закончится показ в минутах, относительно времени сейчас: '
                                  ,reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminViews.admin_views)

@router.message(state=AdminViews.admin_views)
async def view_change_date(message :types.Message ,state :FSMContext):
    minutes = message.text

    try:
        minutes = int(minutes)
    except Exception:
        await message.answer("Введите кол-во минут, или если хотите вернутся /start")
        return
    data = await state.get_data()
    view_id = data.get('view_id')
    utcnow = datetime.datetime.utcnow()
    end_date = utcnow + datetime.timedelta(minutes=minutes)
    db.update_view_end(end_date, view_id)
    await message.answer('Обновлено')
    await views_start(message=message)