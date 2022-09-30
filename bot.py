from aiogram import Dispatcher, Bot
import logging
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import data.config as config
from utils.set_commands import set_default_commands
from setup import reg_routers

scheduler = AsyncIOScheduler()

async def admin_notify(bot: Bot):
    for admin in config.ADMINS:
        await bot.send_message(admin, 'Бот запущен')

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(lineno)s - %(name)s - %(message)s')
    logging.error('Starting bot...')
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    await set_default_commands(bot)
    reg_routers(dp)
    try:
        scheduler.start()
        await admin_notify(bot)
        await dp.start_polling(bot)
        logging.error('Bot started!')
    except:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')

if __name__ == '__main__':
    cli()
