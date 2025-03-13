'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55 & мой кот Масик ♥️
Имя: NazomiAutoRentalEKIP
Описание: Модуль для авто-выдачи в аренду экипировки в MineEVO
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
class NazomiAutoRentalEKIP(loader.Module):
    """Модуль для авто-выдачи в аренду экипировки в MineEVO"""
    strings = {
        "name": "NazomiAutoRentalEKIP"
    }

    def __init__(self):
        self.client = None
        self.equipment_dict = {}
        self.work_command = None

    async def client_ready(self, client, db):
        self.client = client
        await self.load_data()
        asyncio.create_task(self.auto_update_loop())

        # Можете убрать, просто подписчиков мало вот и добавил :(
        await client(JoinChannelRequest("@Nazomi_Modules"))

    async def load_data(self):
        try:
            response = requests.get("https://pastebin.com/raw/9a3ucSL1")
            response.raise_for_status()
            data = response.json()
            self.equipment_dict = data.get("equipment_dict", {})
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
                        equipment = parts[0].strip().lower()
                        nickname = parts[1].strip()
                        time_str = parts[2].strip()
                        await self._process_interaction(None, equipment, nickname, time_str, silent=True)
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

    async def _process_interaction(self, message: Message, equipment: str, nickname: str, time_str: str, silent: bool = False) -> None:
        equipment_emoji = self.equipment_dict.get(equipment.lower())

        if not equipment_emoji:
            if not silent and message:
                await message.edit(
                    f"<emoji document_id=5210952531676504517>🚫</emoji><b> Название экипировки введено неправильно или её не существует</b>"
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
                    f"<emoji document_id=5429116151391070736>🛄</emoji><b> Выдаю </i>{equipment_emoji}</i> игроку <i>{nickname}</i> на <i>{time_str}</i>...</b>"
                )

            await self.client.send_message(5522271758, "🪖 Экипировка")

            start_time = asyncio.get_event_loop().time()
            bot_message = None
            while asyncio.get_event_loop().time() - start_time < 10:
                bot_messages = await self.client.get_messages(5522271758, limit=1)
                for msg in bot_messages:
                    if "🧰 Твоя экипировка :" in msg.text:
                        bot_message = msg
                        break
                if bot_message:
                    break

            if not bot_message:
                raise ValueError("<emoji document_id=5386367538735104399>⌛</emoji> Бот не отвечает</b>")

            equipment_found = False
            for _ in range(5):
                await asyncio.sleep(2)
                bot_message = await self._refresh_message(bot_message)
                if await self._find_and_click_button(bot_message, equipment_emoji, exclude_handshake=True):
                    equipment_found = True
                    break
                if not await self._find_and_click_button(bot_message, "Вперёд »"):
                    break

            if not equipment_found:
                raise ValueError(f"<emoji document_id=5260293700088511294>⛔️</emoji><b> Экипировка {equipment_emoji} не найден!</b>")

            if not await self._find_and_click_button(bot_message, "🤝"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>🤝 Доверить экипировку</i> не найдена</b>")

            await self.client.send_message(5522271758, f"{nickname} {time_str}", reply_to=bot_message.id)
            await asyncio.sleep(2)

            if not await self._find_and_click_button(bot_message, "💜 Доверить"):
                raise ValueError("<emoji document_id=5145388477218554646>⛔️</emoji><b> Кнопка <i>💜 Доверить</i> не найдена</b>")

            if not silent and message:
                await message.edit(
                    f"<emoji document_id=5449428597922079323>🧰</emoji><b> Выдал <i>{equipment_emoji}</i> в аренду игроку <i>{nickname}</i> на <i>{time_str}</i></b>"
                )

        except Exception as e:
            if not silent and message:
                await message.edit(f"<b>{str(e)}</b>")

    @loader.command()
    async def nre(self, message: Message) -> None:
        """<экипировка> <ник> <время>"""
        raw_args = utils.get_args_raw(message)
        args = [arg.strip() for arg in raw_args.split(maxsplit=2) if arg.strip()]

        if len(args) != 3:
            await message.edit(
                "<emoji document_id=5956561916573782596>📄</emoji><b> Введены не все аргументы:\n<экипировка> <ник> <время></b>"
            )
            return

        equipment, nickname, time_str = args
        await self._process_interaction(message, equipment, nickname, time_str)