from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    admin = State()
    posting = State()
    gold = State()


class AdminDossier(StatesGroup):
    admin_dossier = State()
    admin_dossier_menu = State()
    admin_dossier_money = State()
    admin_change_guess_age = State()
    admin_change_count_guess_age = State()
    admin_dossier_vip = State()
class AdminReports(StatesGroup):
    admin_report = State()

class AdminSummary(StatesGroup):
    summary_set_username = State()
    summary_set_price = State()
    summary_set_name = State()

class AdminSender(StatesGroup):
    admin_sender = State()
    admin_sender_load = State()
    admin_sender_send = State()




class AdminSub(StatesGroup):
    admin_sub = State()
    admin_sub_id = State()
    admin_sub_link = State()
    admin_sub_start = State()
    admin_sub_end = State()


class AdminViews(StatesGroup):
    admin_views = State()
    admin_text = State()
    admin_date = State()
