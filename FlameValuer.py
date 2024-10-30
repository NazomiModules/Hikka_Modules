import asyncio
import requests as r
import re
from .. import loader, utils
import base64

# meta developer: @flame_modules
@loader.tds
class FlameValuer(loader.Module):
    """💳 Модуль для оценки стоимости кейсов и статистики игроков MineEVO"""
    strings = {"name": "FlameValuer"}
    a = base64.b64decode("aHR0cHM6Ly90aW55dXJsLmNvbS80bXMyenlrdg==").decode('utf-8')
    b = (
        "<emoji document_id=5447644880824181073>⚠️</emoji> "
        "<b>Сервис недоступен. Попробуйте позже.</b>"
    )
    @loader.command()
    async def fpc(self, m):
        """Оценить стоимость кейсов по реплаю на сообщение с кейсами"""
        c = await m.get_reply_message()
        await utils.answer(
            m,
            "<emoji document_id=5818687127000452892>🔎</emoji> <b>Сканируем рынок...</b>",
        )
        await asyncio.sleep(1)
        try:
            d = r.get(self.a, timeout=10)
            d.raise_for_status()
            e = d.json()
            f = e.get("a")
            g = e.get("b")
            h = e.get("c")
            i = e.get("e")
            j = e.get("f")
            k = e.get("g")
            l = e.get("i")
            m_ = e.get("k")
            n = e.get("l")
        except:
            await utils.answer(m, self.b)
            return
        if not c or c.sender_id != f:
            await utils.answer(m, j)
            return
        if n not in c.raw_text:
            await utils.answer(m, k)
            return
        o = c.raw_text
        await utils.answer(m, m_)
        await asyncio.sleep(1)
        p = 0
        for q, r_ in g.items():
            s = self.s(q, o)
            if s:
                t = s / r_
                p += t
        p = round(p)
        u = round(p * i)
        v = round((p / h) * 100, 2)
        await asyncio.sleep(1)
        w = l.format(
            total_myths=p,
            total_evo_coins=u,
            percentage=v,
        )
        await utils.answer(m, w)
    @loader.command()
    async def fsc(self, m):
        """Оценить стоимость открытых кейсов по реплаю на сообщение со статистикой игрока"""
        c = await m.get_reply_message()
        await utils.answer(
            m,
            "<emoji document_id=5818687127000452892>🔎</emoji> <b>Сканируем рынок...</b>",
        )
        await asyncio.sleep(1)
        try:
            d = r.get(self.a, timeout=10)
            d.raise_for_status()
            e = d.json()
            f = e.get("a")
            g = e.get("b")
            i = e.get("e")
            h = e.get("d")
            j = e.get("f")
            k = e.get("h")
            l = e.get("j")
            m_ = e.get("k")
            n = e.get("m")
        except:
            await utils.answer(m, self.b)
            return
        if not c or c.sender_id != f:
            await utils.answer(m, j)
            return
        if n not in c.raw_text:
            await utils.answer(m, k)
            return
        o = c.raw_text
        await utils.answer(m, m_)
        await asyncio.sleep(1)
        p = 0
        for q, r_ in g.items():
            s = self.s(q, o, field='Открыто')
            if r_ and s:
                t = s / r_
                p += t
        p = round(p)
        u = round(p * i)
        v = round((p / h) * 100, 2)
        await asyncio.sleep(1)
        w = l.format(
            opened_myths=p,
            opened_evo_coins=u,
            percentage=v,
        )
        await utils.answer(m, w)
    @loader.command()
    async def fpi(self, m):
        """Показать информацию о модуле и дату обновления курсов"""
        await utils.answer(
            m,
            "<emoji document_id=5215493819641895305>🚛</emoji> <b>Загружаем информацию...</b>",
        )
        await asyncio.sleep(1)
        try:
            d = r.get(self.a, timeout=10)
            d.raise_for_status()
            e = d.json()
            x = e.get("o")
            y = e.get("n")
            z = x.format(last_updated=y)
        except:
            await utils.answer(m, self.b)
            return
        await utils.answer(m, z)
    def s(self, a, b, field=None):
        if field:
            c = re.compile(
                rf"{re.escape(a)}\s*\|\s*{re.escape(field)}\s*:\s*([\d,.]+)", re.IGNORECASE
            )
        else:
            c = re.compile(
                rf"{re.escape(a)}\s*\|?\s*.*?:?\s*([\d,.]+)\s*шт\.?", re.IGNORECASE
            )
        d = c.search(b)
        if d:
            e = d.group(1).replace(",", "").replace(".", "")
            try:
                return int(e)
            except:
                return 0
        return 0