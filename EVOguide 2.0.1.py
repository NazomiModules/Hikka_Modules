#meta developer: @hikka_dmod
from .. import loader, utils
from asyncio import sleep

@loader.tds
class EVOguide(loader.Module):
    """гайд по MineEVO"""
    strings = {'name': 'EVOguide 2.0.1'}
    
    @loader.command(alias="гбусты")
    async def gbusts(self, message):
        """- посмотреть информацию о бустерах"""
        await message.edit("⚡️")
        await sleep(1) 
        await message.edit("⚡️ <b>Бусты</b>")
        await sleep(1)
        await message.edit("⚡️⛏ <b>Бусты руды</b>")
        await sleep(1)
        await message.edit("⚡️💰 <b>Бусты руды, денег</b>")
        await sleep(1)
        await message.edit("⚡️🔮 <b>Бусты руды, денег, плазмы</b>")
        await sleep(1)

        await message.edit(
            """
💰 <b>Бусты денег</b>
⏱ <b>Максимальное время:</b> <code>5 минут</code>
⏰ <b>Минимальное время:</b> <code>5 минут</code>
⚜ <b>Максимальный множитель:</b> <code>×500</code>
🟠 <b>Цена полной прокачки (с ×2 5 минут до ×500 5 минут):</b> <code>124</code> ☀️

⛏ <b>Бусты руды</b>
⏱ <b>Максимальное время:</b> <code>2 часа</code>
⏰ <b>Минимальное время:</b> <code>10 минут</code>
🚸 <b>Максимальный множитель:</b> <code>×100</code>
🔴 <b>Цена полной прокачки (с ×2 10 минут до ×100 2 часа):</b> <code>224</code> ☀️

🔮 <b>Бусты плазмы</b>
⏱ <b>Максимальное время:</b> <code>1 час</code>
⏰ <b>Минимальное время:</b> <code>5 минут</code>
🎵 <b>Максимальный множитель:</b> <code>×100</code>
⚫️ <b>Цена полной прокачки (с ×2 5 минут до ×100 1 час):</b> <code>432</code> ☀️

🌻 <b>Общая цена всех трёх максимальный бустеров:</b> <code>780</code> ☀️

💻 <b>Разработчик</b>: <code>@hikka_dmod</code>, <code>@Gydro4ka</code>
🎞 <b>Помощник</b>: <code>ANONIM</code>
            """
    )
    
    @loader.command(alias='гхз')
    async def gother(self, message):
        """- показать прочие улучшения в mineevo"""
        await message.edit(
            """
⛏ <b><i>Прочие улучшения в MineEVO </i></b>

🎆 <b>Шанс плазмы </b>
🎶 <b>Алиас</b>: <code>шп</code>
⚪️ <b>Цена первой прокачки</b>: <code>5 🎆</code>
🟢 <b>Цена последней прокачки:</b> <code>900</code>
🔵 <b>На полную прокачку:</b> <code>≈42.600</code>
✨ <b>Начальный и конечный проценты</b>: <code>10 &amp; 75%</code>
ℹ️: <i>улучшение дает +0.5% к шансу нахождения плазмы при добыче</i>

🎆 <b>Удача плазмы</b>
⛩ <b>Алиас</b>: <code>уп</code> 
🟢 <b>Цена первой прокачки</b>: <code>25 </code>
🔵 <b>Цена последней прокачки:</b> <code>3500 </code>
🟣 <b>На полную прокачку:</b> <code>≈246.750 </code>
✨ <b>Начальный и конечный проценты</b>: 0<code>% &amp; 70%</code>
ℹ️: <i>улучшение дает +0.5% к шансу получить 2 плазмы при добыче</i>

⛏<b> Мощность кирки</b>
⚖ <b>Алиас</b>: <code>мщ</code> 
🔵 <b>Цена первой прокачки</b>: <code>10 🎆</code>
🟣 <b>Цена последней прокачки</b>: <code>2100 </code>
🟡 <b>На полную прокачку</b>: <code>≈148.100 </code>
ℹ️: <i>улучшение удваивает выкапываемую руду киркой</i>

🍀 <b>Удача кирки</b>
🍁 <b>Алиас</b>: <code>уд</code>
🟣 <b>Цена первой прокачки</b>: <code>35 </code>
🟡 <b>Цена последней прокачки</b>: <code>3.850 </code>
🟠 <b>На полную прокачку</b>: <code>≈214.500 </code>
✨ <b>Начальный и конечный проценты</b>: <code>0% &amp; 55%</code>
ℹ️: <i>улучшение дает +0.5% к шансу получить в два раза больше руды при добыче</i>

🗡 <b>Урон</b>
⛓ <b>Алиас</b>: <code>урон</code>
🟡 <b>Цена первой прокачки</b>: <code>100 </code>
🟠 <b>Цена последней прокачки</b>: <code>4500 </code>
🔴 <b>На полную прокачку</b>: <code>≈43.700 </code>
✨ <b>Начальный и конечный урон</b>: <code>1 &amp; 35</code>

💢 <b>Критический урон</b>
♨️ <b>Алиас</b>: крит 
🟠 <b>Цена первой прокачки</b>: 5<code>5</code>
🔴 <b>Цена последней прокачки</b>: <code>3300</code>
⚫️ <b>Всего на прокачку</b>: <code>≈100 650</code>
✨ <b>Начальный и конечный проценты: </b><code>0% &amp; 30%</code>
ℹ️: <i>yлучшение дает +0.5% к шансу нанести в два раза больше урона при атаке босса</i>

🎆 <b>Вся прокачка в плазме</b>

💻 <b>Кодер:</b> <code>@Gydro4ka</code>
💿 <b>Канал:</b> <code>@hikka_dmod</code>
&lt;b&gt;#FREEDUROV&lt;/b&gt;
            """
    )
    @loader.command(alias='гаппрд')
    async def gupprd(self, message):
        """- показать стоимость прокачки предметов"""
        await message.edit("⚪️")
        await sleep(1)
        await message.edit("🟢")
        await sleep(1)
        await message.edit("🔵")
        await sleep(1)
        await message.edit("🟣")
        await sleep(1)
        await message.edit("🟡")
        await sleep(1)
        await message.edit("🟠")
        await sleep(1)
        await message.edit(
            """
⚫️ <b><i>Прокачка предмета в MineEVO</i></b>

✨ <b>Уровни</b>: ⚪️🟢🔵🟣🟡🟠

<b>Прокачка</b>: ⚪️ -&gt; 🟢
<b>Цена</b>: <code>200.000 🎆, 5 📜, 1 🎨</code>

<b>Прокачка</b>: ⚪️ -&gt; 🔵
<b>Цена</b>: <code>800.000 🎆, 15 📜, 5 🌀, 2 🎨</code>

<b>Прокачка</b>: ⚪️ -&gt; 🟣
<b>Цена</b>: <code>2.600.000 🎆, 1 🌌, 20 🌀, 45 📜, 3 🎨</code>

<b>Прокачка</b>: ⚪️ -&gt; 🟡
<b>Цена</b>: <code>8.000.000 🎆, 3 🌌, 65 🌀, 165 📜, 4 🎨</code>

<b>Прокачка</b>: ⚪️ -&gt; 🟠
<b>Цена</b>: <code>24.200.000 🎆, 6 🌌, 215 🌀, 765 📜, 5 🎨</code>

💻 <b>Программистка</b>: <code>@Gydro4ka</code>
📡 <b>Канал</b>: <code>@hikka_dmod</code>
&lt;b&gt;#FREEDUROV&lt;/b&gt;
            """
    )