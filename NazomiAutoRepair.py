'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55
Название: NazomiAutoRepair
Описание: Модуль для автопочинки экипировки, которую тебе дают
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 2)

from .. import loader, utils
from telethon.tl.types import Message, ChatAdminRights
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon import events, functions
import asyncio
import re
import time
import emoji

@loader.tds
class NazomiAutoRepair(loader.Module):
    '''Модуль для автопочинки экипировки, которую тебе дают'''
    strings = {'name': 'NazomiAutoRepair'}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("auto_repair", True, 'Статус автопочинки', validator=loader.validators.Boolean())
        )
        self.sleep_until = 0
        self.lock = None
        self.client = None
        self.work_channel = None

    async def client_ready(self):
        self.lock = asyncio.Lock()

        try:
            self.work_channel, _ = await utils.asset_channel(self.client, 'NazomiAutoRepair', 'Группа для работы NazomiAutoRepair', silent=True, archive=True, _folder='hikka')

            try:
                await self.client(functions.channels.InviteToChannelRequest(self.work_channel, [5522271758]))
                await self.client(functions.channels.EditAdminRequest(channel=self.work_channel, user_id=5522271758, admin_rights=ChatAdminRights(ban_users=False, post_messages=True, edit_messages=True), rank='EVO'))
            except Exception:
                self.work_channel = None
        except Exception:
            self.work_channel = None
            
        try:
            await self.client(JoinChannelRequest('@Nazomi_Modules'))
        except:
            pass

        self.client.add_event_handler(self.repair_handler, events.NewMessage(chats=5522271758, pattern=r'^💜 Тебе доверена экипировка!'))

    async def repair_handler(self, event: Message):
        if not self.config["auto_repair"] or time.time() < self.sleep_until:
            return

        text = event.raw_text or ""
        lines = text.splitlines()
    
        try:
            eq_line_index = next(i for i, line in enumerate(lines) if "доверил тебе" in line) + 1
            eq_line = lines[eq_line_index].strip()
        except (StopIteration, IndexError):
            return

        emojis_list = emoji.distinct_emoji_list(eq_line)
        if not emojis_list:
            return

        inverted_emojis = "".join(emojis_list[::-1])

        await self.repair_interaction(inverted_emojis)
        await asyncio.sleep(2)
        
    @loader.command()
    async def nar(self, message: Message):
        '''Включить/выключить автопочинку'''
        current_status = self.config['auto_repair']
        new_status = not current_status
        self.config['auto_repair'] = new_status

        if new_status:
            await utils.answer(message, '<b><emoji document_id=5462921117423384478>🛠</emoji> Автопочинка включена</b>')
        else:
            await utils.answer(message, '<b><emoji document_id=5462990652943904884>😴</emoji> Автопочинка выключена</b>')

    @loader.command()
    async def nars(self, message: Message):
        '''Приостановить автопочинку на время'''
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await utils.answer(message, '<b><emoji document_id=5462990652943904884>😴</emoji> Укажите время в секундах</b>')
            return

        sleep_duration = int(args)
        if sleep_duration <= 0:
            await utils.answer(message, '<b><emoji document_id=5210952531676504517>❌</emoji> Время должно быть больше 0</b>')
            return

        self.sleep_until = time.time() + sleep_duration
        await utils.answer(message, f'<b><emoji document_id=5339574256592233562>⛔️</emoji> Автопочинка приостановлена на <code>{sleep_duration}</code> секунд</b>')

    async def refresh_message(self, message: Message) -> Message:
        if not message:
            return None
        try:
            msgs = await self.client.get_messages(message.peer_id, ids=[message.id])
            return msgs[0] if msgs else message
        except Exception:
            return message

    async def repair_interaction(self, inverted_emojis: str):
        start_time = time.time()
        work_chat = getattr(self, 'work_channel', None) or 5522271758
        try:
            await self.client.send_message(work_chat, '🪖 Экипировка')
        except Exception:
            self.work_channel = None
            work_chat = 5522271758
            await self.client.send_message(work_chat, '🪖 Экипировка')

        bot_message = None
        while time.time() - start_time < 5:
            try:
                msgs = await self.client.get_messages(work_chat, limit=1)
            except Exception:
                self.work_channel = None
                work_chat = 5522271758
                await self.client.send_message(work_chat, '🪖 Экипировка')
                msgs = await self.client.get_messages(work_chat, limit=1)
            for m in msgs:
                try:
                    if m and m.raw_text and ('🧰 Экипировка' in m.raw_text) and getattr(m, 'sender_id', None) == 5522271758:
                        bot_message = m
                        break
                except Exception:
                    continue
            if bot_message:
                break

        async def try_click(msg, required_texts):
            msg = await self.refresh_message(msg)
            if not msg or not msg.buttons:
                return False
            for row in msg.buttons:
                for btn in row:
                    if isinstance(required_texts, (list, tuple, set)):
                        tokens = list(required_texts)
                    else:
                        tokens = [required_texts]
                    if all(token in btn.text for token in tokens):
                        try:
                            await asyncio.wait_for(btn.click(), timeout=1.0)
                            await asyncio.sleep(0.01)
                        except asyncio.TimeoutError:
                            pass
                        return True
            return False

        found = False
        start_time = time.time()

        while time.time() - start_time < 10:
            await asyncio.sleep(0.01)

            new_msg = await self.refresh_message(bot_message)
            if new_msg.buttons != bot_message.buttons:
                bot_message = new_msg

            required_tokens = ['🤝'] + list(inverted_emojis)

            if await try_click(bot_message, required_tokens):
                found = True
                break

            if not await try_click(bot_message, '»'):
                break

        await asyncio.sleep(0.5)
        if not await try_click(bot_message, '🛠'):
            return

        await try_click(bot_message, '🛠 Починить')
        await asyncio.sleep(0.5)

        if not await try_click(bot_message, '◀ Назад'):
            return

        await asyncio.sleep(0.5)
        if not await try_click(bot_message, '❌ Вернуть'):
            return
        await asyncio.sleep(0.5)
        if not await try_click(bot_message, '❌ Вернуть'):
            return
