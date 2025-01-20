'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55
Имя: AutoMIRAGE
Описание: Модуль для автоматизации бота @MirageGamingBot
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 0)

import asyncio
from telethon.tl.types import Message
from .. import loader

@loader.tds
class AutoMIRAGE(loader.Module):
    """Модуль для автоматизации бота @MirageGamingBot"""

    strings = {"name": "AutoMIRAGE"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.chat_id = 7165856906
        self.messages = {
            "city": "🌆 Город",
            "business": "💼 Бизнес", 
            "mining": "🖥 Майнинг",
            "mine": "⚒ Шахта"
        }
        self.business_emojis = ["🏪", "🏬", "💊", "🍱", "🚕", "🏭", "🏖", "🖥", "🎬", "📰", "🧪"]
        self.delays = {
            "city": 3610,
            "business": 43210, 
            "mining": 3010,
            "mine": 610
        }
        self.last_executed = self.db.get('AutoMIRAGE', 'last_executed', {key: 0 for key in self.delays})
        self.action_delay = 3
        self._task = asyncio.create_task(self.loop())

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "main",
                False,
                lambda: "Основной параметр работы модуля",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "city",
                True,
                lambda: "Параметр для сбора налогов с города",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "business", 
                True,
                lambda: "Параметр для оплаты налогов в бизнесе",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "mining",
                True,
                lambda: "Параметр для оплаты налогов в майнинге", 
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "mine",
                True,
                lambda: "Параметр для добычи в шахте",
                validator=loader.validators.Boolean()
            ),
        )

    async def loop(self):
        while True:
            if self.config["main"]:
                try:
                    for action in ["city", "business", "mining", "mine"]:
                        if self.config[action] and (asyncio.get_event_loop().time() - self.last_executed[action] >= self.delays[action]):
                            self.last_executed[action] = asyncio.get_event_loop().time()
                            await self.client.send_message(self.chat_id, self.messages[action])
                            await asyncio.sleep(self.action_delay)
                    self.db.set('AutoMIRAGE', 'last_executed', self.last_executed)
                except Exception:
                    pass
            await asyncio.sleep(60)

    async def watcher(self, message: Message):
        if message.chat_id == self.chat_id and message.buttons:
            try:
                buttons = message.buttons
                if self.config["city"] and "🌆" in message.text:
                    for row in buttons:
                        for button in row:
                            if "💸 Собрать налоги" in button.text:
                                await button.click()
                                break

                if self.config["business"]:
                    if any(emoji in message.text for emoji in self.business_emojis):
                        for row in buttons:
                            for button in row:
                                if "💸 Оплатить налоги" in button.text:
                                    await button.click()
                                    break

                if self.config["mining"] and "🖥" in message.text:
                    for row in buttons:
                        for button in row:
                            if "💸 Оплатить электричество" in button.text:
                                await button.click()
                                break

                if self.config["mine"] and "⚒" in message.text:
                    for _ in range(15):
                        for row in buttons:
                            for button in row:
                                if "🔨 Добыть руду" in button.text:
                                    await button.click()
                                    await asyncio.sleep(3)
                                    break
            except Exception as e:
                if "Encrypted data invalid" in str(e):
                    return

    @loader.command()
    async def nmain(self, message: Message):
        """Включить/выключить модуль"""
        self.config["main"] = not self.config["main"]
        await message.edit(
            "<b><emoji document_id=5213302802205387293>✅</emoji> Модуль включен</b>" if self.config["main"] else "<b><emoji document_id=5215539470849288572>❌</emoji> Модуль выключен</b>"
        )

    @loader.command()
    async def ncity(self, message: Message):
        """Включить/выключить сбор налогов с города"""
        self.config["city"] = not self.config["city"]
        await message.edit(
            "<b><emoji document_id=5213302802205387293>✅</emoji> Авто-сбор налогов города включен</b>" if self.config["city"] else "<b><emoji document_id=5215539470849288572>❌</emoji> Авто-сбор налогов города выключен</b>"
        )

    @loader.command()
    async def nbusiness(self, message: Message):
        """Включить/выключить оплату налогов бизнеса"""
        self.config["business"] = not self.config["business"]
        await message.edit(
            "<b><emoji document_id=5213302802205387293>✅</emoji> Авто-оплата налогов бизнеса включена</b>" if self.config["business"] else "<b><emoji document_id=5215539470849288572>❌</emoji> Авто-оплата налогов бизнеса выключена</b>"
        )

    @loader.command()
    async def nmining(self, message: Message):
        """Включить/выключить оплату электричества майнинга"""
        self.config["mining"] = not self.config["mining"]
        await message.edit(
            "<b><emoji document_id=5213302802205387293>✅</emoji> Авто-оплата электричества майнинга включена</b>" if self.config["mining"] else "<b><emoji document_id=5215539470849288572>❌</emoji>Авто-оплата электричества майнинга выключена</b>"
        )

    @loader.command()
    async def nmine(self, message: Message):
        """Включить/выключить копание в шахте"""
        self.config["mine"] = not self.config["mine"]
        await message.edit(
            "<b><emoji document_id=5213302802205387293>✅</emoji> Авто-копание в шахте включено</b>" if self.config["mine"] else "<b><emoji document_id=5215539470849288572>❌</emoji> Авто-копание в шахте выключено</b>"
        )

    @loader.command()
    async def nstatus(self, message: Message):
        """Показать текущие значения модуля"""
        await message.edit(
            f"<b><emoji document_id=5341715473882955310>⚙️</emoji> Значения модуля:</b>\n\n<b>Основной модуль: {'<emoji document_id=5213302802205387293>✅</emoji>' if self.config['main'] else '<emoji document_id=5215539470849288572>❌</emoji>'}</b>\n"
            f"<b>Город: {'<emoji document_id=5213302802205387293>✅</emoji>' if self.config['city'] else '<emoji document_id=5215539470849288572>❌</emoji>'}</b>\n"
            f"<b>Бизнес: {'<emoji document_id=5213302802205387293>✅</emoji>' if self.config['business'] else '<emoji document_id=5215539470849288572>❌</emoji>'}</b>\n"
            f"<b>Майнинг: {'<emoji document_id=5213302802205387293>✅</emoji>' if self.config['mining'] else '<emoji document_id=5215539470849288572>❌</emoji>'}</b>\n"
            f"<b>Шахта: {'<emoji document_id=5213302802205387293>✅</emoji>' if self.config['mine'] else '<emoji document_id=5215539470849288572>❌</emoji>'}</b>"
                  )
