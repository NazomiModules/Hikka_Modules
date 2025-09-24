'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55 & мой кот Масик ♥️
Имя: NazomiAutoRentalPRD
Описание: Модуль для автовыдачи в аренду предметов
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (2, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message, ChatAdminRights
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl import functions
import asyncio
import re
import time

@loader.tds
class NazomiAutoRentalPRD(loader.Module):
    """Модуль для автовыдачи в аренду предметов"""
    strings = {"name": "NazomiAutoRentalPRD"}

    async def client_ready(self, client, db):
        self.client = client
        self.subject_dict = {}
        self.work_command = None
        await self.load_data()
        self.lock = asyncio.Lock()
        
        try:
            self.work_channel, _ = await utils.asset_channel(self.client, 'NazomiAutoRentalPRD', 'Группа для работы NazomiAutoRentalPRD', silent=True, archive=True, _folder='hikka')

            try:
                await self.client(functions.channels.InviteToChannelRequest(self.work_channel, [5522271758]))
            except Exception:
                self.work_channel = None
            if self.work_channel is not None:
                try:
                    await self.client(functions.channels.EditAdminRequest(channel=self.work_channel, user_id=5522271758, admin_rights=ChatAdminRights(ban_users=False, post_messages=True, edit_messages=True), rank='EVO'))
                except Exception:
                    pass
        except Exception:
            self.work_channel = None

        try:
            await self.client(JoinChannelRequest('@Nazomi_Modules'))
        except:
            pass
            
    async def wait_for_event(self, event_filter, timeout):
        result_container = {'event': None, 'received': False}

        async def handler(event):
            if not result_container['received']:
                result_container['event'] = event
                result_container['received'] = True

        self.client.add_event_handler(handler, event_filter)

        try:
            start_time = asyncio.get_event_loop().time()
            while not result_container['received']:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    return None
                await asyncio.sleep(0.01)

            return result_container['event']

        finally:
            try:
                self.client.remove_event_handler(handler, event_filter)
            except Exception:
                try:
                    self.client.remove_event_handler(handler)
                except Exception:
                    pass

    def get_emoji_by_name(self, name: str) -> str | None:
        name = name.lower()
        for emoji, names in self.subject_dict.items():
            if name in names:
                return emoji
        return None

    async def load_data(self):
        import requests
        try:
            def fetch_json():
                response = requests.get('https://raw.githubusercontent.com/NazomiModules/Hikka_Modules/main/Modules_Data/NazomiAutoRentalPRD_Data.json', timeout=10)
                response.raise_for_status()
                return response.json()
            data = await utils.run_sync(fetch_json)
            self.subject_dict = data.get('subject_dict', {})
            self.level_to_emoji = data.get('level_to_emoji', {})
        except Exception:
            self.subject_dict = {}
            self.level_to_emoji = {}

    def validate_time_format(self, time_str: str) -> bool:
        return bool(re.match(r'^\d+[мчд]$', time_str))

    async def refresh_message(self, message: Message) -> Message:
        if not message:
            return None
        try:
            msgs = await self.client.get_messages(message.peer_id, ids=[message.id])
            return msgs[0] if msgs else message
        except Exception:
            return message

    async def process_interaction(self, message: Message, subject_emoji: str, nickname: str, time_str: str, lvl_emoji: str = None, silent: bool = False) -> None:
        if not self.validate_time_format(time_str):
            if not silent and message:
                await utils.answer(message, '<b><emoji document_id=5382194935057372936>⏱</emoji> Неправильное время\nИспользуйте: <code>5м</code>, <code>2ч</code>, <code>1д</code></b>')
            return

        status_message = None
        start_time = time.time()
        try:
            work_chat = getattr(self, 'work_channel', None) or 5522271758
            try:
                await self.client.send_message(work_chat, '🧤 Предметы')
            except Exception:
                self.work_channel = None
                work_chat = 5522271758
                await self.client.send_message(work_chat, '🧤 Предметы')
            bot_message = None
            while time.time() - start_time < 5:
                try:
                    msgs = await self.client.get_messages(work_chat, limit=1)
                except Exception:
                    self.work_channel = None
                    work_chat = 5522271758
                    await self.client.send_message(work_chat, '🧤 Предметы')
                    msgs = await self.client.get_messages(work_chat, limit=1)
                for m in msgs:
                    try:
                        if m and m.text and ('👜 Твои предметы' in m.text) and getattr(m, 'sender_id', None) == 5522271758:
                            bot_message = m
                            issuance_start_time = time.time()
                            break
                    except Exception:
                        continue
                if bot_message:
                    break

            if not bot_message:
                raise ValueError('<b><emoji document_id=5386367538735104399>⌛</emoji> Бот не отвечает</b>')

            async def try_click(msg, required_texts, exclude_handshake=False):
                msg = await self.refresh_message(msg)
                if not msg or not msg.buttons:
                    return False
                for row in msg.buttons:
                    for btn in row:
                        if exclude_handshake and ('🤝' in btn.text or '🖐' in btn.text):
                            continue
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
            timeout = 10
            start_time = time.time()

            while time.time() - start_time < timeout:
                await asyncio.sleep(0.01)

                new_msg = await self.refresh_message(bot_message)
                if new_msg.buttons != bot_message.buttons:
                    bot_message = new_msg

                required_tokens = [subject_emoji] if not lvl_emoji else [subject_emoji, lvl_emoji]

                if await try_click(bot_message, required_tokens, exclude_handshake=True):
                    found = True
                    break

                if not await try_click(bot_message, '»'):
                    break

            if not found:
                if lvl_emoji:
                    raise ValueError(f'<b><emoji document_id=5260293700088511294>⛔️</emoji> Предмета {subject_emoji}{lvl_emoji} нету:\nОн одет или попросту нету</b>')
                raise ValueError(f'<b><emoji document_id=5260293700088511294>⛔️</emoji> Предмета {subject_emoji} нету:\nОн одет или попросту нету</b>')

            if not await try_click(bot_message, '🤝'):
                raise ValueError('<b><emoji document_id=5145388477218554646>⛔️</emoji> Кнопки <i>«🤝 Доверить предмет»</i> нету:\nБот не отвечает или выдаче помешали</b>')

            try:
                await self.client.send_message(work_chat, f'{nickname} {time_str}', reply_to=bot_message.id)
            except Exception:
                self.work_channel = None
                work_chat = 5522271758
                await self.client.send_message(work_chat, '🧤 Предметы')
                issuance_start_time = time.time()
                fetch_start = time.time()
                bot_message = None
                while time.time() - fetch_start < 5:
                    msgs = await self.client.get_messages(work_chat, limit=1)
                    for m in msgs:
                        try:
                            if m and m.text and ('👜 Твои предметы' in m.text) and getattr(m, 'sender_id', None) == 5522271758:
                                bot_message = m
                                break
                        except Exception:
                            continue
                    if bot_message:
                        break
                if not bot_message:
                    raise ValueError('<b><emoji document_id=5386367538735104399>⌛</emoji> Бот не отвечает</b>')
                await self.client.send_message(work_chat, f'{nickname} {time_str}', reply_to=bot_message.id)

            trust_button_found = False
            trust_wait_start = time.time()

            while time.time() - trust_wait_start < 10:
                await asyncio.sleep(0.01)

                new_msg = await self.refresh_message(bot_message)
                if new_msg.buttons != bot_message.buttons:
                    bot_message = new_msg

                if await try_click(bot_message, '💜 Доверить'):
                    trust_button_found = True
                    break

            if not trust_button_found:
                raise ValueError('<b><emoji document_id=5145388477218554646>⛔️</emoji> Кнопки <i>«💜 Доверить»</i> нету:\nБот не отвечает или выдаче помешали</b>')

            end_time = time.time()
            duration = end_time - issuance_start_time

            if not silent and message:
                success_message = (f'<b><emoji document_id=5380056101473492248>👜</emoji> Успешная выдача!\n• Предмет: <code>{subject_emoji}{lvl_emoji or ""}</code>\n• Получатель: <code>{nickname}</code>\n• Время аренды: <code>{time_str}</code>\n• Выдан за: <code>{duration:.2f} сек</code></b>')
                await utils.answer(message, success_message)

        except Exception as e:
            if not silent and message:
                await utils.answer(message, f'{str(e)}')
                
    @loader.command()
    async def nrp(self, message: Message) -> None:
        """<предмет> [т] <ник> <время> - выдать предмет в аренду"""
        async with self.lock:
            args = utils.get_args(message)

            if not (3 <= len(args) <= 4):
                await utils.answer(message, '<b><emoji document_id=5956561916573782596>📄</emoji> Неверное количество аргументов.\nИспользуйте: <code>.nrp <предмет> [т] <ник> <время></code></b>')
                return

            level_str = None
            lvl_emoji = None
            
            if len(args) == 4:
                subject_name, level_str, nickname, time_str = args
            else:
                subject_name, nickname, time_str = args

            subject_emoji = self.get_emoji_by_name(subject_name)
            if not subject_emoji:
                await utils.answer(message, f'<b><emoji document_id=5210952531676504517>❌</emoji> Название предмета введено неправильно или его не существует</b>')
                return

            if level_str:
                match = re.match(r'^[тТ]\s*([1-7])$', level_str)
                if match:
                    lvl = match.group(1)
                    lvl_emoji = (self.level_to_emoji or {}).get(f'т{lvl}')
                    if not lvl_emoji:
                        await utils.answer(message, f'<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
                        return
                else:
                    await utils.answer(message, '<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
                    return

            await self.process_interaction(message=message, subject_emoji=subject_emoji, nickname=nickname, time_str=time_str, lvl_emoji=lvl_emoji, silent=False)
