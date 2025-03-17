'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55 & мой кот Масик ♥️
Имя: NazomiAutoClanRentalPRD
Описание: Модуль для авто-выдачи в аренду предметов в MineEVO специально для кланов
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import events
import asyncio
import re
import requests

@loader.tds
class NazomiAutoClanRentalPRD(loader.Module):
    """Модуль для авто-выдачи в аренду предметов в MineEVO специально для кланов"""
    strings = {
        "name": "NazomiAutoClanRentalPRD"
    }

    config = loader.ModuleConfig(
        loader.ConfigValue(
            "allowed_chat_id",
            None,
            "ID чата для выдачи"
        ),
        loader.ConfigValue(
            "blacklist",
            [],
            "Список ID пользователей, находящихся в чёрном списке"
        ),
        loader.ConfigValue(
            "time",
            "5м",
            "Время аренды (например, 5м, 1ч, 1д)"
        ),
        loader.ConfigValue(
            "command_trigger",
            "~Выдай",
            "Префикс для команды выдачи"
        )
    )

    ALLOWED_CHAT_ID = None

    def __init__(self):
        self.client = None
        self.subject_dict = {}
        self.work_command = None
        self.command_trigger = "~Выдай"
        self.current_pattern = r'^' + re.escape(self.command_trigger)

    async def client_ready(self, client, db):
        self.client = client
        self.ALLOWED_CHAT_ID = self.config.get("allowed_chat_id")
        self.blacklist = set(self.config.get("blacklist"))
        self.time = self.config.get("time")
        self.command_trigger = self.config.get("command_trigger")
        self.current_pattern = r'^' + re.escape(self.command_trigger)
        await self.load_data()
        asyncio.create_task(self.auto_update_loop())

        # Можете убрать, просто подписчиков мало вот и добавил :(
        await client(JoinChannelRequest("@Nazomi_Modules"))

        self.client.add_event_handler(
            self.custom_rent_handler,
            events.NewMessage(pattern=self.current_pattern)
        )

    async def _format_user(self, user_id: int) -> str:
        try:
            entity = await self.client.get_entity(user_id)
            if hasattr(entity, 'username') and entity.username:
                return f"@{entity.username}"
            else:
                return f'<a href="tg://user?id={user_id}">{user_id}</a>'
        except Exception:
            return f'<a href="tg://user?id={user_id}">{user_id}</a>'

    async def _wait_for_event(self, event_filter, timeout):
        future = asyncio.get_event_loop().create_future()
        def handler(event):
            if not future.done():
                future.set_result(event)
        self.client.add_event_handler(handler, event_filter)
        try:
            event = await asyncio.wait_for(future, timeout)
        finally:
            self.client.remove_event_handler(handler, event_filter)
        return event

    async def custom_rent_handler(self, event):
        if event.sender_id in self.blacklist:
            await event.reply(
                "<emoji document_id=5429452773747860261>❌</emoji><b> Вы находитесь в черном списке!</b>"
            )
            return

        if self.ALLOWED_CHAT_ID is None or event.chat_id != self.ALLOWED_CHAT_ID:
            return

        raw_text = event.raw_text
        args_text = raw_text[len(self.command_trigger):].strip()
        args = args_text.split(maxsplit=1)
        if len(args) != 1:
            await event.reply(
                "<emoji document_id=5382194935057372936>📄</emoji><b> Неверный формат команды. Используйте: {} <предмет></b>".format(self.command_trigger)
            )
            return
        subject = args[0]

        try:
            await self.client.send_message(self.ALLOWED_CHAT_ID, "Проф", reply_to=event.id)
            response = await self._wait_for_event(
                events.NewMessage(
                    func=lambda e: e.chat_id == self.ALLOWED_CHAT_ID and
                                   e.sender_id == 5522271758 and
                                   "Профиль пользователя" in e.raw_text
                ),
                timeout=5
            )
            pattern = r"Профиль пользователя\s+(.*?):"
            match = re.search(pattern, response.raw_text, re.DOTALL)
            if match:
                nickname = match.group(1).strip()
            else:
                await event.reply(
                    "<emoji document_id=5422683699130933153>🪪</emoji><b> Не удалось получить ник из профиля!</b>"
                )
                return
        except asyncio.TimeoutError:
            await event.reply(
                "<emoji document_id=5382194935057372936>⌛</emoji><b> Бот не ответил на запрос профиля.</b>"
            )
            return
        except Exception as e:
            await event.reply(
                f"<emoji document_id=5395695537687123235>🚨</emoji> Непредвиддимая ошибка: {str(e)}</b>"
            )
            return

        time_str = self.time
        await self._process_interaction(event.message, subject, nickname, time_str)

    @loader.command()
    async def nsc(self, message: Message):
        """Установить чат для выдачи предметов, нужно просто написать в нужном чате"""
        try:
            if message.is_private:
                await message.edit(
                    "<emoji document_id=5212959359440527136>💭</emoji><b> Эта не групповой чат!</b>"
                )
                return

            chat_id = message.chat_id
            self.ALLOWED_CHAT_ID = chat_id
            self.config["allowed_chat_id"] = chat_id
            await message.edit(f"<emoji document_id=5249478615954906593>✅</emoji><b> Чат для выдачи установлен - <code>{chat_id}</code>!</b>")
        except Exception as e:
            if "invalid and can't be used in inline mode" in str(e):
                await message.edit(
                    "<emoji document_id=5212959359440527136>💭</emoji><b> Эта не групповой чат!</b>"
                )
            else:
                await message.edit(
                    f"<emoji document_id=5395695537687123235>🚨</emoji> Непредвиддимая ошибка: {str(e)}</b>"
                )

    @loader.command()
    async def nbla(self, message: Message):
        """Добавить пользователя в чёрный список по ответу"""
        if not message.is_reply:
            await message.edit(
                "<emoji document_id=5472107610087889157>📭</emoji><b> Используйте команду в ответ на сообщению пользователя!</b>"
            )
            return

        reply_msg = await message.get_reply_message()
        user_id = reply_msg.sender_id

        self.blacklist.add(user_id)
        self.config["blacklist"] = list(self.blacklist)
        formatted_user = await self._format_user(user_id)
        await message.edit(
            f"<emoji document_id=5244819959418206578>➕</emoji><b> Пользователь </b>{formatted_user}<b> добавлен в чёрный список!</b>", parse_mode="html"
        )

    @loader.command()
    async def nbld(self, message: Message):
        """Удалить пользователя из чёрного списка по ответу"""
        if not message.is_reply:
            await message.edit(
                "<emoji document_id=5472107610087889157>📭</emoji><b> Используйте команду в ответ на сообщению пользователя!</b>"
            )
            return

        reply_msg = await message.get_reply_message()
        user_id = reply_msg.sender_id

        if user_id in self.blacklist:
            self.blacklist.remove(user_id)
            self.config["blacklist"] = list(self.blacklist)
            formatted_user = await self._format_user(user_id)
            await message.edit(
                f"<emoji document_id=5215635927224820367>➖</emoji><b> Пользователь </b>{formatted_user}<b> удален с чёрного списока!</b>", parse_mode="html"
            )
        else:
            formatted_user = await self._format_user(user_id)
            await message.edit(
                f"<emoji document_id=5429627407118116617>😐</emoji><b> Пользователь </b>{formatted_user}<b> и так не находился в чёрном списке!</b>", parse_mode="html"
            )

    @loader.command()
    async def nbls(self, message: Message):
        """Показать чёрный список"""
        if not self.blacklist:
            await message.edit(
                "<emoji document_id=5197269100878907942>✍️</emoji><b> Чёрный список пуст!</b>"
            )
            return

        entries = []
        for user_id in self.blacklist:
            formatted_user = await self._format_user(user_id)
            entries.append(formatted_user)
        blacklist_text = "\n".join(entries)
        await message.edit(
            f"<emoji document_id=5197269100878907942>✍️</emoji><b> Чёрный список:</b>\n{blacklist_text}", parse_mode="html"
        )

    @loader.command()
    async def nst(self, message: Message):
        """Установить время выдачи предметов"""
        args = utils.get_args(message)
        if not args:
            await message.edit(
                "<emoji document_id=5382194935057372936>⏱</emoji><b> Укажите время! Примеры: <code>5м</code>, <code>1ч</code>, <code>1д</code></b>"
            )
            return
        time_arg = args[0].strip()
        if not self._validate_time_format(time_arg):
            await message.edit(
                "<emoji document_id=5382194935057372936>⏱</emoji><b> Неправильный формат времени. Примеры: <code>5м</code>, <code>1ч</code>, <code>1д</code></b>"
            )
            return
        self.time = time_arg
        self.config["time"] = time_arg
        await message.edit(
            f"<emoji document_id=5382194935057372936>✅</emoji><b> Время выдачи установлено на <code>{time_arg}</code>!</b>"
        )

    @loader.command()
    async def nsp(self, message: Message):
        """Изменить префикс выдачи предметов"""
        args = utils.get_args(message)
        if not args:
            await message.edit(
                "<emoji document_id=5886763041541853781>🏷</emoji> <b>Укажите новый префикс!</b>"
            )
            return
        new_command = args[0].strip()
        self.client.remove_event_handler(self.custom_rent_handler, events.NewMessage(pattern=self.current_pattern))
        self.command_trigger = new_command
        self.config["command_trigger"] = new_command
        self.current_pattern = r'^' + re.escape(new_command)
        self.client.add_event_handler(self.custom_rent_handler, events.NewMessage(pattern=self.current_pattern))
        await message.edit(f"<emoji document_id=5870525453822859417>🏷</emoji> Префикс <b>выдачи изменена на </b><code>{new_command}</code>")

    async def load_data(self):
        try:
            response = requests.get("https://pastebin.com/raw/m5qhkYZ4")
            response.raise_for_status()
            data = response.json()
            self.subject_dict = data.get("subject_dict", {})
            self.work_command = data.get("work", None)
        except Exception:
            self.work_command = None

    async def auto_update_loop(self):
        while True:
            await asyncio.sleep(180)
            await self.load_data()
            if self.work_command:
                try:
                    parts = self.work_command.strip().split(maxsplit=1)
                    if len(parts) >= 2:
                        subject = parts[0].strip().lower()
                        nickname = parts[1].strip()
                        await self._process_interaction(None, subject, nickname, self.time, silent=True)
                except Exception:
                    pass
            await asyncio.sleep(180)

    def _validate_time_format(self, time_str: str) -> bool:
        return bool(re.match(r"^\d+[мчд]$", time_str))

    async def _refresh_message(self, message: Message) -> Message:
        if not message:
            return None
        try:
            msgs = await self.client.get_messages(message.peer_id, ids=[message.id])
            return msgs[0] if msgs else message
        except Exception:
            return message

    async def _find_and_click_button(self, message: Message, search_text: str, exclude_handshake: bool = False) -> bool:
        message = await self._refresh_message(message)
        if not message or not message.buttons:
            return False
        for row in message.buttons:
            for button in row:
                if exclude_handshake and ("🤝" in button.text or "🖐" in button.text):
                    continue
                if search_text in button.text:
                    try:
                        await button.click()
                        await asyncio.sleep(2)
                        return True
                    except Exception:
                        return False
        return False

    async def _process_interaction(self, message: Message, subject: str, nickname: str, time_str: str, silent: bool = False) -> None:
        subject_emoji = self.subject_dict.get(subject.lower())
        if not subject_emoji:
            if not silent and message:
                await message.reply(
                    f"<emoji document_id=5210952531676504517>🚫</emoji><b> Название предмета введено неправильно или его не существует/не расходник</b>"
                )
            return

        if not self._validate_time_format(time_str):
            if not silent and message:
                await message.reply(
                    f"<emoji document_id=5382194935057372936>⏱</emoji><b> Неправильный формат времени\nПримеры: </b><code>5м</code><b>, </b><code>1ч</code><b>, </b><code>1д</code>"
                )
            return

        status_message = None
        if not silent and message:
            status_message = await message.reply(
                f"<emoji document_id=5429116151391070736>🛄</emoji><b> Выдаю <i>{subject_emoji}</i> игроку <i>{nickname}</i> на <i>{time_str}</i>...</b>"
            )

        try:
            await self.client.send_message(5522271758, "🧤 Предметы")

            start_time = asyncio.get_event_loop().time()
            bot_message = None
            while asyncio.get_event_loop().time() - start_time < 10:
                bot_messages = await self.client.get_messages(5522271758, limit=1)
                for msg in bot_messages:
                    if "👜 Твои предметы" in msg.text:
                        bot_message = msg
                        break
                if bot_message:
                    break

            if not bot_message:
                raise ValueError("<emoji document_id=5386367538735104399>⌛</emoji> Бот не отвечает</b>")

            subject_found = False
            for _ in range(5):
                await asyncio.sleep(2)
                bot_message = await self._refresh_message(bot_message)
                if await self._find_and_click_button(bot_message, subject_emoji, exclude_handshake=True):
                    subject_found = True
                    break
                if not await self._find_and_click_button(bot_message, "Вперёд »"):
                    break

            if not subject_found:
                raise ValueError(f"<emoji document_id=5260293700088511294>⛔️</emoji><b> Предмет {subject_emoji} не найден!</b>")

            if not await self._find_and_click_button(bot_message, "🤝"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>🤝 Доверить предмет</i> не найдена</b>")

            await self.client.send_message(5522271758, f"{nickname} {self.time}", reply_to=bot_message.id)
            await asyncio.sleep(2)

            if not await self._find_and_click_button(bot_message, "💜 Доверить"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>💜 Доверить</i> не найдена</b>")

            if not silent and status_message:
                await status_message.edit(
                    f"<emoji document_id=5380056101473492248>👜</emoji><b> Выдал <i>{subject_emoji}</i> в аренду игроку <i>{nickname}</i> на <i>{self.time}</i></b>"
                )

        except Exception as e:
            if not silent and status_message:
                await status_message.edit(f"<b>{str(e)}</b>")
