'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55
Имя: NozomiConverter
Описание: Модуль для конвертации и просмотра курсов
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (2, 5, 0)

from .. import loader, utils
from ..inline.types import InlineCall


@loader.tds
class NozomiConverter(loader.Module):
	'''Модуль для конвертации и просмотра курсов'''
	strings = {'name': 'NozomiConverter'}

	async def client_ready(self, client, db):
		await self.load_data()

	async def load_data(self):
		import requests
		try:
			def fetch_json():
				response = requests.get('https://raw.githubusercontent.com/NazomiModules/Hikka_Modules/main/Modules_Data/NozomiConverter_Data.json', timeout=10)
				response.raise_for_status()
				return response.json()
			data = await utils.run_sync(fetch_json)
			self.strings_data = data.get('strings', {})
			self.courses = data.get('courses', {})
			self.currency_display = data.get('currency_display', {})
		except Exception:
			self.strings_data = {}
			self.courses = {}
			self.currency_display = {}

	def standard_buttons(self, back_callback):
		return [
			[
				{'text': '👈 Назад', 'callback': back_callback},
				{'text': '🔻 Закрыть', 'action': 'close'}
			]
		]

	def format_number(self, value: float) -> str:
		thresholds = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
		formats = ['.1f', '.1f', '.2f', '.3f', '.4f', '.5f', '.6f']
		for threshold, fmt in zip(thresholds, formats):
			if value >= threshold:
				return f'{value:{fmt}}'.rstrip('0').rstrip('.')
		return '0'

	@loader.command()
	async def nc(self, message):
		'''Конвертация'''
		args = utils.get_args_raw(message)
		if not args or len(args.split()) % 2 != 0:
			await utils.answer(message, self.strings_data.get('error', '').format(prefix=self.get_prefix()))
			return

		input_pairs = []
		pairs = args.split()
		emoji_to_text = self.currency_display.get('emoji_to_text', {})

		try:
			for i in range(0, len(pairs), 2):
				count = float(pairs[i])
				case = emoji_to_text.get(pairs[i + 1].lower(), pairs[i + 1].lower())
				if case not in self.courses:
					raise ValueError
				input_pairs.append((count, case))
		except Exception:
			await utils.answer(message, self.strings_data.get('error', '').format(prefix=self.get_prefix()))
			return

		if not self.courses:
			await utils.answer(message, '<b><emoji document_id=5422649047334794716>😵</emoji> Сервер недоступен, оповестите @Murex55</b>')
			return

		total_myth = sum(count * self.courses[case] for count, case in input_pairs)
		response = [f'💱 <code>{args}</code> <b>в:</b>']

		for case, rate in self.courses.items():
			equivalent = total_myth / rate
			display = self.currency_display['text_to_display'].get(case, case)
			response.append(f'<b>{display}:</b> <code>{self.format_number(equivalent)}</code>')

		await utils.answer(message, '\n'.join(response))

	async def show_main_menu(self, message_or_call):
		markup = [
			[
				{'text': '👜 Прд', 'callback': self.show_prd_menu},
				{'text': '🧰 Экип', 'callback': self.show_ekip_menu}
			],
			[{'text': '🔻 Закрыть', 'action': 'close'}]
		]
		text = self.strings_data.get('main_menu', '')
		if isinstance(message_or_call, InlineCall):
			await message_or_call.edit(text=text, reply_markup=markup)
		else:
			await self.inline.form(text=text, message=message_or_call, reply_markup=markup)

	@loader.command()
	async def nk(self, message):
		'''Курсы прд и экип'''
		await self.show_main_menu(message)

	async def show_prd_menu(self, call: InlineCall):
		markup = [
			[{'text': '👜 Предметы', 'callback': self.show_items_menu}],
			[{'text': '📈 Прокачка', 'callback': self.show_upgrade_menu}],
		] + self.standard_buttons(self.show_main_menu)
		await call.edit(text=self.strings_data.get('items_menu', ''), reply_markup=markup)

	async def show_ekip_menu(self, call: InlineCall):
		markup = [
			[{'text': '🧰 Экипировка', 'callback': self.show_equipment_menu}],
			[{'text': '📈 Прокачка', 'callback': self.show_e_upgrade_menu}],
		] + self.standard_buttons(self.show_main_menu)
		await call.edit(text=self.strings_data.get('ekip_menu', ''), reply_markup=markup)

	async def show_items_menu(self, call: InlineCall):
		await call.edit(text=self.strings_data.get('items_prices', ''), reply_markup=self.standard_buttons(self.show_prd_menu))

	async def show_equipment_menu(self, call: InlineCall):
		await call.edit(text=self.strings_data.get('ekip_prices', ''), reply_markup=self.standard_buttons(self.show_ekip_menu))

	async def show_upgrade_menu(self, call: InlineCall):
		await call.edit(text=self.strings_data.get('upgrade_menu', ''), reply_markup=self.standard_buttons(self.show_prd_menu))
	
	async def show_e_upgrade_menu(self, call: InlineCall):
		await call.edit(text=self.strings_data.get('e_upgrade_menu', ''), reply_markup=self.standard_buttons(self.show_ekip_menu))

	@loader.command()
	async def ncu(self, message):
		'''Последняя дата обновления курсов'''
		if not self.strings_data:
			await utils.answer(message, '<b><emoji document_id=5422649047334794716>😵</emoji> Сервер недоступен, оповестите @Murex55</b>')
			return
		last_update_text = self.strings_data.get('last_update', '')
		report_rate_text = self.strings_data.get('report_rate', '')
		await utils.answer(message, f'{last_update_text}\n\n{report_rate_text}')
