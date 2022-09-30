from aiogram import Dispatcher
import handlers.admin.admin as admin
import handlers.admin.admin_mailing as mail
import handlers.admin.admin_op as op
import handlers.users.start as start
import handlers.admin.admin_ref_links as ref
import handlers.admin.admin_shows as shows
import handlers.admin.admin_misc as misc
import handlers.users.main_users as main

def reg_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(main.r)
    dp.include_router(admin.router)
    dp.include_router(mail.router)
    dp.include_router(op.router)
    dp.include_router(ref.router)
    dp.include_router(shows.router)
    dp.include_router(misc.router)