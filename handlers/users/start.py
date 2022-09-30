from aiogram import Router, Bot
from aiogram.filters import CommandObject
from aiogram.types import Message
from utils.db_api.main import Database
import datetime
from keyboards.reply import menu_kb
import logging
from filters.reg_filter import NoReg

router = Router()
db = Database()
@router.message(NoReg(), commands=['start'])
async def not_registered_start(m: Message, command: CommandObject, bot: Bot):
    await m.answer('Добро пожаловать в бота', reply_markup=menu_kb())
    db.register_user(m.from_user.id, m.from_user.username, datetime.datetime.utcnow(), command.args)
    if command.args is not None:
        logging.error(command.args)
        if command.args.isnumeric():
            db.add_refs(command.args)
            logging.error('Referal')
            if int(db.fetch_refs(command.args)) % 25 == 0:
                db.increase_gold(command.args, 5000)
        else:
            db.add_income(command.args)
            logging.error('Ref. Svodka')

@router.message(commands=['start'])
async def regged_start(m: Message):
    await m.answer('Добро пожаловать в бота', reply_markup=menu_kb())