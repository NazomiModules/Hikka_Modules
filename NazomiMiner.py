'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55
Идея: @lermuxx
Имя: NazomiMiner
Описание: Модуль для авто-добычи руды
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio

class NazomiMiner(loader.Module):
	'''Модуль для авто-добычи руды'''
	strings = {'name': 'NazomiMiner'}

	config = loader.ModuleConfig(loader.ConfigValue('cooldown', 5, 'Интервал добычи (в минутах)', validator=loader.validators.Integer(minimum=3)))

	async def client_ready(self, client, db):
		self.client = client
		self.db = db
		self.task = None

		if self.get('minestatus', False):
			self.task = asyncio.create_task(self.loop())

		try:
			await self.client(JoinChannelRequest('@Nazomi_Modules'))
		except:
			pass

	async def loop(self):
		while self.get('minestatus', False):
			try:
				await self.mine_once(self.config.get('cooldown'))
			except Exception:
				pass
			await asyncio.sleep(self.config.get('cooldown') * 60)

	async def refresh_message(self, message: Message) -> Message:
		if not message:
			return None
		try:
			msgs = await self.client.get_messages(message.peer_id, ids=[message.id])
			return msgs[0] if msgs else message
		except Exception:
			return message

	async def mine_once(self, cooldown: int):
		my_msg = await self.client.send_message(5522271758, '⛏ Добывать')
		await asyncio.sleep(1)

		msgs = await self.client.get_messages(5522271758, limit=3)
		bot_message = None
		for m in msgs:
			try:
				if m and m.text and ('⛏' in m.text or '⛏' in m.text.lower()) and getattr(m, 'sender_id', None) == 5522271758:
					bot_message = m
					break
			except Exception:
				continue

		if not bot_message:
			await my_msg.delete()
			return

		if not bot_message.buttons:
			await bot_message.delete()
			await my_msg.delete()
			return

		async def try_click(msg, required_texts):
			msg = await self.refresh_message(msg)
			if not msg or not msg.buttons:
				return False
			for row in msg.buttons:
				for btn in row:
					tokens = [required_texts] if isinstance(required_texts, str) else list(required_texts)
					if all(token in btn.text for token in tokens):
						try:
							await asyncio.wait_for(btn.click(), timeout=1.0)
							await asyncio.sleep(0.1)
						except asyncio.TimeoutError:
							pass
						return True
			return False

		if any("🧱 Собрать" in btn.text for row in bot_message.buttons for btn in row):
			await asyncio.sleep(2)
			my_msg2 = await self.client.send_message(5522271758, '⛏ Добывать')
			await asyncio.sleep(1)

			msgs2 = await self.client.get_messages(5522271758, limit=3)
			bot_msg2 = None
			for m in msgs2:
				try:
					if m and m.text and ('⛏' in m.text or '⛏' in m.text.lower()) and getattr(m, 'sender_id', None) == 5522271758:
						bot_msg2 = m
						break
				except Exception:
					continue

			if bot_msg2:
				if await try_click(bot_msg2, '🧱 Собрать'):
					await asyncio.sleep(3)
					await try_click(bot_msg2, '⛏ Добывать ещё')
					await bot_msg2.delete()
			await my_msg2.delete()
			return

		if await try_click(bot_message, '⛏ Добывать'):
			await bot_message.delete()
			await my_msg.delete()
			return

		await bot_message.delete()
		await my_msg.delete()

	@loader.command()
	async def nm(self, message: Message):
		'''Включить/выключить авто-добычу'''
		current_status = not self.get('minestatus', False)
		self.set('minestatus', current_status)

		if current_status:
			if self.task and not self.task.done():
				self.task.cancel()
				self.task = None
			self.task = asyncio.create_task(self.loop())
			await utils.answer(message, '<b><emoji document_id=5445284980978621387>🚀</emoji> Добыча включена</b>')
		else:
			if self.task and not self.task.done():
				self.task.cancel()
				self.task = None
			await utils.answer(message, '<b><emoji document_id=5462990652943904884>😴</emoji> Добыча выключена</b>')
