from .. import loader, utils
import asyncio
from telethon import events

@loader.tds
class BfgxMod(loader.Module):
    """Этот модуль управляет депозитами и проверяет баланс (by SanyaDragon)"""
    strings = {'name': 'BFGDEPOZ'}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.is_active = False

    async def activatecmd(self, message):
        """Активировать авто-депозиты"""
        if self.is_active:
            await utils.answer(message, "<b>Авто-депозиты уже включены</b>")
            return
        self.is_active = True
        await utils.answer(message, "<b>Режим авто-депозитов активирован</b>")
        asyncio.create_task(self.deposit_cycle())

    async def deactivatecmd(self, message):
        """Отключить авто-депозиты"""
        if not self.is_active:
            await utils.answer(message, "<b>Авто-депозиты уже выключены</b>")
            return
        self.is_active = False
        await utils.answer(message, "<b>Авто-депозиты отключены</b>")

    async def checkbalancecmd(self, message):
        """Проверить баланс"""
        await self.client.send_message('@bforgame_bot', 'Б')

        @self.client.on(events.NewMessage(chats='@bforgame_bot'))
        async def handler(event):
            await self.client.send_message(message.chat_id, event.message.message)
            self.client.remove_event_handler(handler)

    async def deposit_cycle(self):
        while self.is_active:
            await self.client.send_message('@bforgame_bot', 'Депозит снять все')
            await asyncio.sleep(5)
            await self.client.send_message('@bforgame_bot', 'Депозит положить все')
            await asyncio.sleep(5 * 60 * 60)  
            if not self.is_active:
                break