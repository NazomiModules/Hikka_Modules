from telethon.errors import FloodWaitError
from .. import loader, utils
import asyncio
import time

# meta developer: @flame_modules
@loader.tds
class FlameMiner(loader.Module):
    """🔥Модуль для автоматического копания в выбранной шахте"""
    strings = {
        "name": "FlameMiner",
        "a": "<emoji document_id=5420315771991497307>🔥</emoji> <b>Копание включено</b>",
        "b": "<emoji document_id=5462990652943904884>😴</emoji> <b>Копание выключено</b>",
        "c": "<emoji document_id=5980930633298350051>✅</emoji> <b>Вы выбрали шахту:</b> ",
        "d": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Ошибка:</b> Неверная шахта! Пожалуйста, выберите <b>Gold</b>, <b>Emerald</b> или <b>Ruby</b>."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "cooldown", 2.0, "Задержка копания в секундах",
        )
        self.w = {
            "Gold": 7168860714,
            "Emerald": 7084173311,
            "Ruby": 7066508668,
        }
        self.e = {
            "Gold": "<emoji document_id=5380036576552178412>💛</emoji>",
            "Emerald": "<emoji document_id=5379866611811375909>💚</emoji>",
            "Ruby": "<emoji document_id=5382255988017483709>❤️</emoji>",
        }
        self.r = 0

    async def client_ready(self, t, y):
        self.u = t
        self.i = y
        self.o = self.i.get(self.strings['name'], "p", "Gold")
        self.set("s", False)

    @loader.command()
    async def flcd(self, a):
        """Изменить задержку копания (в секундах)"""
        try:
            self.config["cooldown"] = float(utils.get_args_raw(a))
            await utils.answer(a, f"<emoji document_id=5980930633298350051>✅</emoji> <b>Задержка копания изменена на {self.config['cooldown']} сек</b>")
        except ValueError:
            await utils.answer(a, "<emoji document_id=5240241223632954241>🚫</emoji> <b>Ошибка:</b> Укажите числовое значение!")

    @loader.command()
    async def flmine(self, s):
        """Выбрать шахту (Gold, Emerald, Ruby)"""
        d = utils.get_args_raw(s).capitalize()
        if d in self.w:
            self.o = d
            self.i.set(self.strings['name'], "p", d)
            f = self.e[d]
            await utils.answer(s, f"{self.strings['c']} {f} <b>{d}</b>")
        else:
            await utils.answer(s, self.strings["d"])

    @loader.command()
    async def fl(self, g):
        """Включение/Выключение копания"""
        h = not self.get("s", False)
        self.set("s", h)
        j = self.e[self.o]
        if h:
            await utils.answer(g, f"{j} {self.strings['a']}")
            await self.k()
        else:
            await utils.answer(g, f"{j} {self.strings['b']}")

    async def k(self):
        while self.get("s", False):
            l = time.time()
            if l >= self.r:
                try:
                    await self.u.send_message(self.w[self.o], "коп")
                except FloodWaitError as z:
                    self.r = l + z.seconds
                    await asyncio.sleep(z.seconds)
                await asyncio.sleep(self.config["cooldown"])
            else:
                await asyncio.sleep(self.r - l)
