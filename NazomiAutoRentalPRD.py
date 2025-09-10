'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55 & мой кот Масик ♥️
Имя: NazomiAutoClanRentalPRD
Описание: Модуль для автовыдачи в аренду предметов в MineEVO специально для кланов
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (2, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message, ChatAdminRights
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import events, functions, errors
import asyncio
import re
import time

@loader.tds
class NazomiAutoClanRentalPRD(loader.Module):
    '''Модуль для автовыдачи в аренду предметов специально для кланов'''
    strings = {'name': 'NazomiAutoClanRentalPRD'}

    config = loader.ModuleConfig(
        loader.ConfigValue('allowed_chats', [], 'Список чатов для выдачи'),
        loader.ConfigValue('blacklist', [], 'Список ID пользователей, находящихся в чёрном списке'),
        loader.ConfigValue('time', '5м', 'Время аренды (например, 5м, 1ч, 1д)'),
        loader.ConfigValue('money', 10, 'Количество денег в переводе'),
        loader.ConfigValue('command_trigger', '!выдай', 'Префикс для команды выдачи'),
        loader.ConfigValue('item_times', {}, 'Индивидуальные времена')
    )

    async def client_ready(self, client, db):
        self.client = client
        self.allowed_chats = set(self.config.get('allowed_chats') or [])
        self.blacklist = set(self.config.get('blacklist') or [])
        self.item_times = self.config.get('item_times') or {}
        self.command_trigger = self.config.get('command_trigger')
        self.current_pattern = r'^' + re.escape(self.command_trigger)
        self.lock = asyncio.Lock()

        try:
            self.work_channel, _ = await utils.asset_channel(self.client, 'NazomiAutoClanRentalPRD', 'Группа для работы NazomiAutoClanRentalPRD', silent=True, archive=True, _folder='hikka')
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

        self.client.add_event_handler(self.custom_rent_handler, events.NewMessage(pattern=self.current_pattern))
        await self.load_data()

        try:
            await self.client(JoinChannelRequest('@Nazomi_Modules'))
        except:
            pass

    async def format_user(self, user_id: int) -> str:
        try:
            entity = await self.client.get_entity(user_id)
            if hasattr(entity, 'username') and entity.username:
                return f'@{entity.username}'
            else:
                return f'<a href="tg://user?id={user_id}">{user_id}</a>'
        except Exception:
            return f'<a href="tg://user?id={user_id}">{user_id}</a>'

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

    async def custom_rent_handler(self, event):
        text = event.raw_text or ''
        trigger = self.config.get('command_trigger')
        if not text.startswith(trigger):
            return

        chat_id = event.chat_id
        allowed = set(self.config.get('allowed_chats') or [])
        blacklist = set(self.config.get('blacklist') or [])

        if not allowed or chat_id not in allowed:
            return

        if event.sender_id in blacklist:
            await event.reply('<b><emoji document_id=5231302159739395058>🔒</emoji> Вы находитесь в черном списке</b>')
            return

        args_text = text[len(trigger):].strip()
        args = args_text.split()
        if not args:
            await event.reply(f'<b><emoji document_id=5210952531676504517>❌</emoji> Неверный формат команды\nИспользуйте: <code>{trigger}</code> <предмет> [т]</b>')
            return

        subject = args[0].lower()
        lvl_emoji = None
        if len(args) >= 2:
            level_arg = args[1].strip().lower()
            m = re.match(r'^[тТ]\s*([1-7])$', level_arg)
            if m:
                level = m.group(1)
                lt = getattr(self, 'level_to_emoji', {})
                lvl_emoji = lt.get(f'т{level}')

        emoji_map = self.subject_dict
        subject_emoji = self.get_emoji_by_name(subject)
        if not subject_emoji:
            await event.reply('<b><emoji document_id=5210952531676504517>❌</emoji> Название предмета введено неверно или его не существует</b>')
            return

        async with self.lock:
            try:
                money = self.config.get('money')
                pay_message = await self.client.send_message(chat_id, f'Перевести {money}', reply_to=event.message.id)
                response = await self.wait_for_event(
                    events.NewMessage(func=lambda e: (e.chat_id == chat_id and e.sender_id == 5522271758 and e.raw_text.startswith('✔') and 'перевел' in e.raw_text)), timeout=3)

                if response is None:
                    await event.reply('<b><emoji document_id=5382194935057372936>⌛</emoji> Бот не ответил на команду перевода</b>')
                    return

                match = re.search(r'✔\s*\S+\s+перевел(?:\(а\))?\s+игроку\s+(\S+)\s*-', response.raw_text)
                if match:
                    nickname = match.group(1).strip()
                else:
                    await event.reply('<b><emoji document_id=5249110030451494411>🪪</emoji> Не удалось получить ник</b>')
                    return

                await pay_message.delete()
                await response.delete()
            except asyncio.TimeoutError:
                await event.reply('<b><emoji document_id=5382194935057372936>⌛</emoji> Бот не ответил на команду перевода</b>')
                return
            except Exception as e:
                await event.reply(f'<b><emoji document_id=5377857202771992680>😳</emoji> Непредвиденная ошибка:</b> {str(e)}')
                return

            item_times = self.config.get('item_times') or {}
            default_time = self.config.get('time')
            if lvl_emoji:
                level_key = f'{subject_emoji}|{lvl_emoji}'
                time_str = item_times.get(level_key) or item_times.get(subject_emoji) or default_time
            else:
                time_str = item_times.get(subject_emoji) or default_time

            await self.process_interaction(event.message, subject_emoji, nickname, time_str, lvl_emoji=lvl_emoji)
            await asyncio.sleep(3)

    @loader.command()
    async def nbl(self, message: Message):
        '''Добавить/удалить пользователя в чёрный список'''
        args = utils.get_args(message)
        user_id = None

        if args:
            target = args[0]
            try:
                user_id = int(target)
            except ValueError:
                try:
                    entity = await self.client.get_entity(target)
                    user_id = entity.id
                except Exception:
                    return await utils.answer(message, f'<b><emoji document_id=5922712343011135025>🚫</emoji> Не удалось найти пользователя "{target}"</b>')

        elif message.is_reply:
            reply_msg = await message.get_reply_message()
            user_id = reply_msg.sender_id

        if not user_id:
            return await utils.answer(message, '<b><emoji document_id=5210952531676504517>❌</emoji> Укажите юзер/айди или используйте команду в ответ</b>')

        if user_id in self.blacklist:
            self.blacklist.remove(user_id)
            self.config['blacklist'] = list(self.blacklist)
            formatted_user = await self.format_user(user_id)
            return await utils.answer(message, f'<b><emoji document_id=5215635927224820367>➖</emoji> Пользователь {formatted_user} удалён из чёрного списка</b>')
        else:
            self.blacklist.add(user_id)
            self.config['blacklist'] = list(self.blacklist)
            formatted_user = await self.format_user(user_id)
            return await utils.answer(message, f'<b><emoji document_id=5217791902023162643>➕</emoji> Пользователь {formatted_user} добавлен в чёрный список</b>')

    @loader.command()
    async def nbls(self, message: Message):
        '''Показать чёрный список'''
        if not self.blacklist:
            return await utils.answer(message, '<b><emoji document_id=5197269100878907942>✍️</emoji> Чёрный список пуст</b>')

        entries = []
        for user_id in self.blacklist:
            formatted_user = await self.format_user(user_id)
            entries.append(formatted_user)
        blacklist_text = '\n'.join(entries)
        return await utils.answer(message, f'<b><emoji document_id=5197269100878907942>✍️</emoji> Чёрный список:\n{blacklist_text}</b>')

    @loader.command()
    async def nsp(self, message: Message):
        '''Изменить префикс выдачи'''
        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, '<b><emoji document_id=5886763041541853781>🏷</emoji> Укажите новый префикс</b>')
        new_command = args[0].strip()
        try:
            self.client.remove_event_handler(self.custom_rent_handler, events.NewMessage(pattern=self.current_pattern))
        except:
            pass
        self.command_trigger = new_command
        self.config['command_trigger'] = new_command
        self.current_pattern = r'^' + re.escape(new_command)
        self.client.add_event_handler(self.custom_rent_handler, events.NewMessage(pattern=self.current_pattern))
        return await utils.answer(message, f'<b><emoji document_id=5870525453822859417>🏷</emoji> Префикс выдачи предметов изменен на <code>{new_command}</code></b>')

    @loader.command()
    async def nsc(self, message: Message):
        '''Добавить/удалить чат для выдачи'''
        if message.is_private:
            return await utils.answer(message, '<b><emoji document_id=6037254263187443802>💬</emoji> Это не групповой чат!</b>')
        chat_id = message.chat_id
        if chat_id in self.allowed_chats:
            self.allowed_chats.remove(chat_id)
            self.config['allowed_chats'] = list(self.allowed_chats)
            await utils.answer(message, f'<b><emoji document_id=5276384644739129761>🗑</emoji> Чат <code>{chat_id}</code> удален из выдачи</b>')
        else:
            self.allowed_chats.add(chat_id)
            self.config['allowed_chats'] = list(self.allowed_chats)
            await utils.answer(message, f'<b><emoji document_id=5397916757333654639>➕</emoji> Чат <code>{chat_id}</code> добавлен в выдачу</b>')

    @loader.command()
    async def nestr(self, message: Message):
        '''Установить время'''
        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, '<b><emoji document_id=5382194935057372936>⏱</emoji> Укажите время. Используйте: <code>5м</code>, <code>2ч</code>, <code>1д</code></b>')

        time_arg = args[0].strip()
        if not self.validate_time_format(time_arg):
            return await utils.answer(message, '<b><emoji document_id=5382194935057372936>⏱</emoji> Неправильное время. Используйте: <code>5м</code>, <code>2ч</code>, <code>1д</code></b>')

        self.config['time'] = time_arg
        return await utils.answer(message, f'<b><emoji document_id=5206607081334906820>✔️</emoji> Время аренды установлено на <code>{time_arg}</code></b>')

    @loader.command()
    async def ntra(self, message: Message):
        '''Установить индивидуальное время'''
        args = utils.get_args(message)
        if len(args) not in (2, 3):
            return await utils.answer(message, '<b><emoji document_id=5210952531676504517>❌</emoji> Формат: <code>{prefix}ntra</code> <предмет> [т] <время></b>'.format(prefix=self.get_prefix()))

        item_name = args[0].strip().lower()
        level_arg = None
        time_arg = None

        if len(args) == 3:
            level_arg = args[1].strip().lower()
            time_arg = args[2].strip()
        else:
            time_arg = args[1].strip()

        subject_emoji = self.get_emoji_by_name(item_name)
        if not subject_emoji:
            return await utils.answer(message, '<b><emoji document_id=5210952531676504517>❌</emoji> Название предмета введено неверно или его не существует</b>')

        if not self.validate_time_format(time_arg):
            return await utils.answer(message, '<b><emoji document_id=5382194935057372936>⏱</emoji> Укажите время\nИспользуйте: <code>5м</code>, <code>2ч</code>, <code>1д</code></b>')

        key = subject_emoji
        if level_arg is not None:
            m = re.match(r'^[тТ]\s*([1-7])$', level_arg)
            if not m:
                return await utils.answer(message, '<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
            lvl = m.group(1)
            lvl_emoji = (self.level_to_emoji or {}).get(f'т{lvl}')
            if not lvl_emoji:
                return await utils.answer(message, '<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
            key = f'{subject_emoji}|{lvl_emoji}'

        self.item_times[key] = time_arg
        self.config['item_times'] = self.item_times

        pretty_item = key.replace('|', '')
        return await utils.answer(message, f'<b><emoji document_id=5206607081334906820>✔️</emoji> Для {pretty_item} установлено время <code>{time_arg}</code></b>')

    @loader.command()
    async def ntrd(self, message: Message):
        '''Удалить индивидуальное время'''
        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, '<b><emoji document_id=5465665476971471368>❌</emoji> Формат: <code>{prefix}ntrd</code> предмет [т1]</b>')

        item_name = args[0].strip().lower()
        level_arg = args[1].strip().lower() if len(args) >= 2 else None

        subject_emoji = self.get_emoji_by_name(item_name)
        if not subject_emoji:
            return await utils.answer(message, '<b><emoji document_id=5210952531676504517>❌</emoji> Название предмета введено неверно или его не существует</b>')

        candidate_keys = []
        if level_arg is not None:
            m = re.match(r'^[тТ]\s*([1-7])$', level_arg)
            if not m:
                return await utils.answer(message, '<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
            lvl = m.group(1)
            lvl_emoji = (self.level_to_emoji or {}).get(f'т{lvl}')
            if not lvl_emoji:
                return await utils.answer(message, '<b><emoji document_id=5260293700088511294>⛔️</emoji> Уровень указан неверно\nИспользуйте: <code>т4</code></b>')
            candidate_keys.append(f'{subject_emoji}|{lvl_emoji}')

        candidate_keys.append(subject_emoji)

        deleted = False
        for key in candidate_keys:
            if key in self.item_times:
                del self.item_times[key]
                deleted = True
        if deleted:
            self.config['item_times'] = self.item_times
            pretty_item = (candidate_keys[0] if level_arg else subject_emoji).replace('|', '')
            return await utils.answer(message, f'<b><emoji document_id=5445267414562389170>🗑</emoji> Индивидуальное время для {pretty_item} удалено</b>')
        else:
            pretty_item = (candidate_keys[0] if level_arg else subject_emoji).replace('|', '')
            return await utils.answer(message, f'<b><emoji document_id=5429627407118116617>😐</emoji> Для {pretty_item} не было установлено индивидуального времени</b>')

    @loader.command()
    async def ntrs(self, message: Message):
        '''Показать список индивидуальных времен'''
        if not self.item_times:
            return await utils.answer(message, '<b><emoji document_id=5197269100878907942>✍️</emoji> Нет установленных индивидуальных времён</b>')

        entries = []
        for key, time_value in self.item_times.items():
            pretty_key = key.replace('|', '')
            entries.append(f'<b>{pretty_key} - <code>{time_value}</code></b>')
        times_text = '\n'.join(entries)
        return await utils.answer(message, f'<b><emoji document_id=5382194935057372936>⏱</emoji> Индивидуальные времена:</b>\n{times_text}')

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
                await message.reply('<b><emoji document_id=5382194935057372936>⏱</emoji> Неправильное время\nИспользуйте: <code>5м</code>, <code>2ч</code>, <code>1д</code></b>')
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
                    raise ValueError('<emoji document_id=5386367538735104399>⌛</emoji><b> Бот не отвечает</b>')
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
                await message.reply(success_message)

        except Exception as e:
            if not silent and message:
                await message.reply(f'{str(e)}')
