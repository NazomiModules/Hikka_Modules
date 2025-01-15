'''
█▄░█ ▄▀█ ▀█ █▀█ █▀▄▀█ █   █▀▄▀█ █▀█ █▀▄ █░█ █░░ █▀▀ █▀
█░▀█ █▀█ █▄ █▄█ █░▀░█ █   █░▀░█ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█

Канал: https://t.me/Nazomi_Modules

--------------------------------------------------------------------
Автор: @Murex55
Имя: NozomiConverter
Описание: Модуль для конвертации кейсов/эк и отображения курсов бустеров/прд
--------------------------------------------------------------------
'''

# meta developer: @Nazomi_Modules
__version__ = (2, 0, 0)

import requests
from .. import loader, utils
from ..inline.types import InlineCall

@loader.tds
class NozomiConverter(loader.Module):
    """Модуль для конвертации кейсов/эк и отображения курсов бустеров/прд"""

    strings = {
        "name": "NozomiConverter",
        "unavailable": "<b><emoji document_id=5422649047334794716>😵</emoji> Сервер недоступен, оповестите @Murex55</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "show_sf",
                False,
                lambda: "Включить отображение сф в конвертации",
                validator=loader.validators.Boolean()
            ),
        )

        self.data_url = "https://pastebin.com/raw/MW9FnJmA"
        self.strings_data = {}
        self.currency_conversion = {}
        self.currency_display = {}
        self.boosts = {}

    async def fetch_data(self):
        try:
            response = requests.get(self.data_url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None

    async def initialize(self):
        data = await self.fetch_data()
        if data:
            self.strings_data = data.get("strings", {})
            self.currency_conversion = data.get("currency_conversion", {}).get("to_myth", {})
            self.currency_display = data.get("currency_display", {})
            self.boosts = data.get("boosts", {})

    async def client_ready(self, client, db):
        await self.initialize()

    def format_boosts(self, rarity):
        if rarity not in self.boosts.get("prices", {}):
            return self.strings_data.get("unavailable", "")
        result = [self.strings_data["boost_headers"].get(rarity, "")]
        for resource_type in ["ore", "plasma"]:
            if resource_type in self.boosts["prices"][rarity]:
                result.append(self.strings_data["resource_headers"].get(resource_type, ""))

                result.extend([
                    self.strings_data.get("time_format", "").format(time=time, price=price)
                    for time, price in self.boosts["prices"][rarity][resource_type].items()
                ])
                result.append("")
        return "\n".join(result).rstrip()

    def format_number(self, value: float) -> str:
        thresholds = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
        formats = [".1f", ".1f", ".2f", ".3f", ".4f", ".5f", ".6f"]

        for threshold, fmt in zip(thresholds, formats):
            if value >= threshold:
                return f"{value:{fmt}}".rstrip("0").rstrip(".")
        return "0"

    @loader.command()
    async def nc(self, message):
        """Конвертировать кейсы/эк в другие"""
        args = utils.get_args_raw(message)
        if not args or len(args.split()) % 2 != 0:
            await utils.answer(
                message,
                self.strings_data.get("error", "").format(prefix=self.get_prefix())
            )
            return

        input_pairs = []
        pairs = args.split()
        emoji_to_text = self.currency_display.get("emoji_to_text", {})
        
        try:
            for i in range(0, len(pairs), 2):
                count = float(pairs[i])
                case = emoji_to_text.get(pairs[i + 1].lower(), pairs[i + 1].lower())
                if case == "сф" and not self.config["show_sf"]:
                    await utils.answer(
                        message,
                        self.strings_data.get("sf_disabled", "").format(prefix=self.get_prefix())
                    )
                    return
                
                if case not in self.currency_conversion:
                    raise ValueError
                input_pairs.append((count, case))
        except:
            await utils.answer(
                message,
                self.strings_data.get("error", "").format(prefix=self.get_prefix())
            )
            return

        if not self.currency_conversion:
            await utils.answer(message, self.strings_data.get("unavailable", ""))
            return

        total_myth = sum(count * self.currency_conversion[case] for count, case in input_pairs)
        response = [f"💱 <code>{args}</code> <b>в:</b>\n"]
        
        for case, rate in self.currency_conversion.items():
            if case == "сф" and not self.config["show_sf"]:
                continue
                
            equivalent = total_myth / rate
            display = self.currency_display['text_to_display'].get(case, case)
            response.append(f"<b>{display}:</b> <code>{self.format_number(equivalent)}</code>")

        await utils.answer(message, "\n".join(response))

    async def _show_main_menu(self, message_or_call):
        markup = [
            [{"text": "⚡ Бустеры", "callback": self.show_boosts_menu}],
            [{"text": "👜 Прд", "callback": self.show_prd_menu}],
            [{"text": "🔻 Закрыть", "action": "close"}]
        ]

        if isinstance(message_or_call, InlineCall):
            await message_or_call.edit(
                text=self.strings_data.get("main_menu", ""),
                reply_markup=markup
            )
        else:
            await self.inline.form(
                text=self.strings_data.get("main_menu", ""),
                message=message_or_call,
                reply_markup=markup
            )

    @loader.command()
    async def nk(self, message):
        """Показать курсы всех бустеров и прд"""
        await self._show_main_menu(message)

    async def show_prd_menu(self, call: InlineCall):
        await call.edit(
            text=self.strings_data.get("items_menu", ""),
            reply_markup=[
                [{"text": "👜 Предметы", "callback": self.show_items_menu}],
                [{"text": "📈 Прокачка", "callback": self.show_upgrade_menu}],
                [{"text": "◀️ Назад", "callback": self._show_main_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    async def show_items_menu(self, call: InlineCall):
        await call.edit(
            text=self.strings_data.get("items_prices", ""),
            reply_markup=[
                [{"text": "◀️ Назад", "callback": self.show_prd_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    async def show_upgrade_menu(self, call: InlineCall):
        await call.edit(
            text=self.strings_data.get("upgrade_menu", ""),
            reply_markup=[
                [{"text": "◀️ Назад", "callback": self.show_prd_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    async def show_boosts_menu(self, call: InlineCall):
        rarity_buttons = [
            [
                {"text": "⚪ (×2)", "callback": lambda c: self.show_rarity_menu(c, "white")},
                {"text": "🟢 (×5)", "callback": lambda c: self.show_rarity_menu(c, "green")}
            ],
            [
                {"text": "🔵 (×10)", "callback": lambda c: self.show_rarity_menu(c, "blue")},
                {"text": "🟣 (×20)", "callback": lambda c: self.show_rarity_menu(c, "purple")}
            ],
            [
                {"text": "🟡 (×50)", "callback": lambda c: self.show_rarity_menu(c, "yellow")},
                {"text": "🟠 (×100)", "callback": lambda c: self.show_rarity_menu(c, "orange")}
            ]
        ]
        reply_markup = rarity_buttons + [
            [{"text": "💰 Деньги", "callback": self.boosts_money_menu}],
            [{"text": "🔴, ⚫, 🟤 (×500, ×1000, ×5000)", "callback": self.boosts_exclusive_menu}],
            [{"text": "◀️ Назад", "callback": self._show_main_menu}, {"text": "🔻 Закрыть", "action": "close"}],
        ]
        await call.edit(text=self.strings_data.get("boosts_menu", ""), reply_markup=reply_markup)

    async def show_rarity_menu(self, call: InlineCall, rarity: str):
        await call.edit(
            text=self.format_boosts(rarity),
            reply_markup=[
                [{"text": "◀️ Назад", "callback": self.show_boosts_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    async def boosts_money_menu(self, call: InlineCall):
        await call.edit(
            text=self.strings_data.get("money_boosts", ""),
            reply_markup=[
                [{"text": "◀️ Назад", "callback": self.show_boosts_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    async def boosts_exclusive_menu(self, call: InlineCall):
        exclusive_config = self.strings_data.get("exclusive_boosts", {})
        text = "\n\n".join([
            exclusive_config.get("header", ""),
            exclusive_config.get("info", ""),
            *[
                "\n".join([
                    rarity_data.get("header", ""),
                    rarity_data.get("ore", ""),
                    rarity_data.get("plasma", "")
                ])
                for rarity_data in [
                    exclusive_config.get("red", {}),
                    exclusive_config.get("black", {}),
                    exclusive_config.get("brown", {})
                ]
            ]
        ])
        await call.edit(
            text=text,
            reply_markup=[
                [{"text": "◀️ Назад", "callback": self.show_boosts_menu}],
                [{"text": "🔻 Закрыть", "action": "close"}],
            ]
        )

    @loader.command()
    async def ncup(self, message):
        """Показать последнию дату обновления курсов, информацию"""
        if not self.strings_data:
            await utils.answer(message, self.strings_data.get("unavailable", ""))
            return

        last_update_text = self.strings_data.get("last_update", "")
        report_rate_text = self.strings_data.get("report_rate", "")
        await utils.answer(message, f"{last_update_text}\n\n{report_rate_text}")
