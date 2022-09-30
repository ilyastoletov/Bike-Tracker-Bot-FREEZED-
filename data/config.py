from environs import Env
import pathlib


env = Env()
env.read_env((pathlib.Path(__file__).parent.parent / '.env').__str__())

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str

ADMINS = list(map(int, env.list("ADMINS")))  # Тут у нас будет список из админов

PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_DATABASE = env.str("PG_DATABASE")
PG_HOST = env.str('PG_HOST')