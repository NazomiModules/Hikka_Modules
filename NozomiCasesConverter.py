#   █▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
#   █░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

#   https://t.me/Nazomi_Modules
# ---------------------------------------------------------------------------
# Автор: @Murex55
# Имя: NozomiCasesConverter
# Описание: Модуль для конвертации кейсов в другие
# ---------------------------------------------------------------------------

# meta developer: @Nazomi_Modules
__version__ = (1, 0, 0)
import base64
import requests
from hikka import loader, utils

@loader.tds
class NozomiCasesConverter(loader.Module):
    """Модуль для конвертации кейсов/эк в другие"""

    strings = {
        "name": "NozomiCasesConverter",
        "unavailable": "<b><emoji document_id=5226717982230591144>🐍</emoji> Сервер недоступен, оповестите @Murex55</b>",
    }

    def __init__(self):
        self.data_url = base64.b64decode(
            "aHR0cHM6Ly90aW55dXJsLmNvbS8yNmI1NHBydQ=="
        ).decode("utf-8")
        self.to_myth = {}
        self.display_mapping = {}
        self.emoji_to_text = {}
        self.error_text = self.strings["unavailable"]

    async def fetch_data(self):
        try:
            response = requests.get(self.data_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    async def initialize(self):
        data = await self.fetch_data()
        if data:
            self.to_myth = data.get("to_myth", {})
            self.display_mapping = data.get("display_mapping", {})
            self.emoji_to_text = data.get("emoji_to_text", {})
            self.error_text = data.get("strings", {}).get("error", self.strings["unavailable"])

    async def client_ready(self, client, db):
        await self.initialize()

    def format_number(self, value: float) -> str:
        thresholds = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
        formats = [".1f", ".1f", ".2f", ".3f", ".4f", ".5f", ".6f"]

        for threshold, fmt in zip(thresholds, formats):
            if value >= threshold:
                return f"{value:{fmt}}".rstrip("0").rstrip(".")
        return "0"

    @loader.command()
    async def nc(self, message: utils.Message):
        """Конвертировать кейсы/эк в другие"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.error_text.format(prefix=self.get_prefix()))
            return

        input_pairs = args.split()
        if len(input_pairs) % 2 != 0:
            await utils.answer(message, self.error_text.format(prefix=self.get_prefix()))
            return

        total_myth_value = 0
        for i in range(0, len(input_pairs), 2):
            try:
                count = float(input_pairs[i])
            except ValueError:
                await utils.answer(message, self.error_text.format(prefix=self.get_prefix()))
                return

            case = input_pairs[i + 1].lower()
            case = self.emoji_to_text.get(case, case)

            if case not in self.to_myth:
                await utils.answer(message, self.error_text.format(prefix=self.get_prefix()))
                return

            total_myth_value += count * self.to_myth[case]

        if not self.to_myth or not self.display_mapping:
            await utils.answer(message, self.strings["unavailable"])
            return

        response = f"<emoji document_id=5471899089425667918>💱</emoji> <code>{args}</code> <b>в:</b>\n\n"
        for text_case, rate in self.to_myth.items():
            equivalent = total_myth_value / rate
            display_name = self.display_mapping.get(text_case, text_case)
            formatted_value = self.format_number(equivalent)
            response += f"<b>{display_name}:</b> <code>{formatted_value}</code>\n"

        await utils.answer(message, response)