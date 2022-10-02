import uuid
import psycopg2
from data.config import PG_HOST as host, PG_USER as user, PG_PASSWORD as password, PG_DATABASE as database
import datetime
import logging

class Database():

    def __init__(self):
        self.connection = psycopg2.connect(host=host, user=user, password=password, database=database)
        self.connection.autocommit = True
        sql = '''
        CREATE TABLE IF NOT EXISTS public.users (
    user_id bigint NOT NULL,
    username character varying(255),
    balance real DEFAULT 0,
    last_seen timestamp without time zone,
    source character varying(255),
    registered_at timestamp without time zone,
    status smallint,
    blocked_at timestamp without time zone
);
        CREATE TABLE IF NOT EXISTS public.channels_to_sub (
    ad_id uuid NOT NULL,
    chat_id bigint NOT NULL,
    link text NOT NULL,
    start_time timestamp without time zone,
    stop_time timestamp without time zone
);
        CREATE TABLE IF NOT EXISTS public.ads (
    username character varying(255),
    price integer,
    source character varying(255) NOT NULL,
    create_time timestamp without time zone
);
CREATE TABLE IF NOT EXISTS public.views (
    view_uuid uuid NOT NULL,
    text text,
    view_count integer DEFAULT 0,
    btn_text character varying(255),
    btn_url character varying(255),
    message_id bigint,
    from_chat_id bigint,
    view_end_count integer
);
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(sql)

    def register_user(self, user_id, username, created_at, source):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute('insert into users(user_id, username, registered_at, source) values(%s, %s, %s, %s)', (user_id, username, created_at, source))
            except Exception as ex:
                logging.error(ex)
                logging.error('User already registered')

    def tip_viewed(self, user_id) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute('select tip from users where user_id = %s', (user_id,))
            return bool(cursor.fetchone()[0])

    def tip_change(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute('update users set tip = true where user_id = %s', (user_id,))

    def exist_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from users where user_id = %s', (user_id,))
            if cursor.fetchone() == None:
                return False
            else:
                return True
    def analyze_registered(self, since: datetime.datetime, untill: datetime.datetime, source: str = ''):
        sql = f"SELECT count(user_id) FROM users WHERE created_at >= %s AND created_at <= %s {source} "
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (since, untill))
            return int(cursor.fetchall()[0][0])

    def update

    def analyze_all(self, active: bool=False):
        with self.connection.cursor() as cursor:
            if active:
                cursor.execute('select * from users where blocked_at is null')
                return len(cursor.fetchall())
            else:
                cursor.execute('select * from users')
                return len(cursor.fetchall())

    def analyze_blocked(self, since: datetime, until: datetime, source: str = ''):
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT count(user_id) FROM users WHERE blocked_at >= %s AND blocked_at <= %s {source}', (since, until))
            return int(cursor.fetchall()[0][0])

    def get_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute('select user_id from users')
            return cursor.fetchall()

    def add_channel(self, channel_id: int, link: str, start_time: datetime, end_time: datetime):
        with self.connection.cursor() as cursor:
            cursor.execute('insert into op_channels(channel_id, link, start_time, end_time) values(%s, %s, %s, %s)', (channel_id, link, start_time, end_time))

    def delete_channel(self, channel_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute('delete from op_channels where channel_id = %s', (channel_id,))

    def get_channels(self, all:bool=False):
        with self.connection.cursor() as cursor:
            if all:
                cursor.execute('select * from op_channels')
            else:
                cursor.execute('select * from op_channels')
            return cursor.fetchall()

    def register_block(self, user_id: int, date: datetime):
        with self.connection.cursor() as cursor:
            cursor.execute('update users set blocked_at = %s where user_id = %s', (date, user_id))

    def add_ad(self, name: str, price: int, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute('insert into ref_links(name, price, username) values(%s, %s, %s)', (name, price, username))

    def get_ad(self, name: str):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from ref_links where name = %s', (name,))
            return cursor.fetchone()

    def get_referals(self):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from ref_links')
            return cursor.fetchall()

    def add_income(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute('update ref_links set income = income + 1 where username = %s', (name,))

    def add_view(self, view_uuid: str, message_id: int, text: str, btn_text: str, btn_url: str, end_time: datetime):
        with self.connection.cursor() as cursor:
            cursor.execute('insert into views(view_uuid, message_id, text, btn_text, btn_url, end_time) values(%s, %s, %s, %s, %s, %s)',
                           (view_uuid, message_id, text, btn_text, btn_url, end_time))

    def update_view_end(self, end_time: datetime, uuid: str):
        with self.connection.cursor() as cursor:
            cursor.execute('update views set end_time = %s where view_uuid = %s', (end_time, uuid))

    def get_views(self):
        with self.connection.cursor() as cursor:
            utcnow = datetime.datetime.utcnow()
            cursor.execute('select * from views where end_time >= %s', (utcnow,))
            return cursor.fetchall()

    def check_view(self, uuid: str, user_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from views_history where user_id = %s and view_id = %s', (user_id, uuid))
            try:
                res = cursor.fetchall()[0]
                return True
            except IndexError:
                return False

    def delete_view(self, uuid: str):
        with self.connection.cursor() as cursor:
            cursor.execute('delete from views where view_uuid = %s', (uuid,))

    def update_view_counter(self, uuid: str, user_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute('update views set counter = counter + 1 where view_uuid = %s', (uuid,))
            cursor.execute('insert into views_history(user_id, view_id) values(%s, %s)', (user_id, uuid))

    def update_op(self, user_id: int):
        with self.connection.cursor() as c:
            utcnow = datetime.datetime.utcnow()
            c.execute('update users set passed_op = %s where user_id = %s', (utcnow, user_id))

    def passed_op(self, name: str):
        with self.connection.cursor() as c:
            c.execute('select count(user_id) from users where source = %s and passed_op is not null', (name,))
            return c.fetchall()

    def increase_gold_adm(self, username: str, amount: int):
        with self.connection.cursor() as cursor:
            cursor.execute('update users set gold = gold + %s where username = %s', (amount, username))

    def increase_rolls(self):
        with self.connection.cursor() as cursor:
            cursor.execute('update users set rolls = 3 where rolls = 0')

    def unincrease_gold(self, user_id: str, amount: int):
        with self.connection.cursor() as cursor:
            cursor.execute('update users set gold = gold - %s where user_id = %s', (amount, user_id))

    def check_inventory(self, user_id: int):
        with self.connection.cursor() as c:
            c.execute('select item_id from users_inventory where user_id = %s', (user_id,))
            return c.fetchall()

    def fetch_item(self, item_id: int):
        with self.connection.cursor() as c:
            c.execute('select * from item_indexes where index = %s', (item_id,))
            return c.fetchone()

    def add_item(self, user_id: int, item_id: int):
        with self.connection.cursor() as c:
            c.execute('insert into users_inventory(user_id, item_id) values(%s, %s)', (user_id, item_id))

    def sell_from_inventory(self, user_id: int, item_id: int, price: int):
        with self.connection.cursor() as c:
            c.execute('DELETE FROM users_inventory WHERE ctid IN (SELECT ctid FROM users_inventory WHERE user_id = %s AND item_id = %s LIMIT 1)', (user_id, item_id))
            c.execute('update users set gold = gold + %s where user_id = %s', (price, user_id))

    def update_last_seen(self, time: int, user_id: int):
        with self.connection.cursor() as c:
            c.execute('update users set last_seen = %s where user_id = %s', (time, user_id))

    def analyze_today(self, since: datetime, until: datetime):
        with self.connection.cursor() as cursor:
            cursor.execute('select count(user_id) from users where last_seen >= %s and last_seen <= %s', (since, until))
            try:
                return cursor.fetchall()[0][0]
            except:
                return 0
