from aiogram import Bot

import config
import asyncio


class MailingParams:
    SLEEP_BETWEEN: int = 1
    SIZE_CHUNK: int = 25
    FINAL_TEXT: str = 'Рассылка закончена:\n - {count_succ}(Успешных)\n  - {blocks}(Заблокированно)\n   - {count_err}(Ошибок)'
    FINAL_TEXT_TELEGRAM: str = '<b>Рассылка закончена:\n - <code>{count_succ}</code>(Успешных)\n  - <code>{blocks}</code>(Заблокированно)\n   - <code>{count_err}</code>(Ошибок)</b>'


class Mailing:
    def __init__(self):
        self.count_users: int = 0
        self.success_send: int = 0
        self.error_send: int = 0
        self.count_blocks: int = 0

    def __clear_all_counters(self):
        self.count_users = 0
        self.success_send = 0
        self.error_send = 0
        self.count_blocks = 0

    async def __alert_end_mailing(self):
        for adm in config.admin:
            await self.bot.send_message(
                adm,
                MailingParams.FINAL_TEXT_TELEGRAM.format(
                    count_succ=self.success_send,
                    blocks=self.count_blocks,
                    count_err=self.error_send
                )
            )
        return

    async def __send_copy_message(self, from_id: int, chat_id: int, message_id: int, keyboard) -> None:
        try:
            await self.bot.copy_message(from_id, chat_id, message_id, reply_markup=keyboard)
            self.success_send += 1
        except Exception:
            self.count_blocks += 1
        except Exception as error:
            print(error)
            self.error_send += 1
        return

    async def __preparing_chunks(self, users: list, chat_id: int, message_id: int, keyboard):
        tasks = []

        for num, user, in enumerate(users):
            task = self.__send_copy_message(user[0], chat_id, message_id, keyboard)
            tasks.append(task)
            if len(tasks) != MailingParams.SIZE_CHUNK and num + 1 != self.count_users:
                continue
            try:
                await asyncio.gather(*tasks)
                await asyncio.sleep(MailingParams.SLEEP_BETWEEN)
            except:
                self.error_send += 1
            tasks.clear()
        await asyncio.sleep(2)
        await self.__alert_end_mailing()
        print(MailingParams.FINAL_TEXT.format(
            count_succ=self.success_send,
            blocks=self.count_blocks,
            count_err=self.error_send
        ))
        return

    async def run(self, bot: Bot, message, users):
        self.bot = bot
        self.__clear_all_counters()
        self.count_users = len(users)
        await self.__preparing_chunks(users, message.chat.id, message.message_id, message.reply_markup)
        return