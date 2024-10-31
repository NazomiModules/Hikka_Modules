
# Not licensed
# meta developer: @siriusb1ack
__version__ = (0,2,0)

from telethon.tl.types import Message, ChatAdminRights
from telethon import functions
import asyncio
from .. import loader, utils
import re
from ..inline.types import InlineCall
import time

@loader.tds
class CaseList(loader.Module): 
    """Модуль для вывода статистики добытых ресурсов """

    strings = {
        "name": "CaseList",
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            
            loader.ConfigValue(
                "nickname",
                False,
                lambda: self.strings("nickname"),
                validator=loader.validators.Boolean()
            ),
        )
    

    @loader.watcher(only_messages=True)
    async def watcher(self,message):
    	converts = self.get("converts",0)
    	clicks = self.get("clicks",0)
    	bosses = self.get("bosses",0)
    	bosses_victory = self.get("bosses_victory",0)
    	r_converts = self.get("r_converts",0)
    	case = self.get("case",0)
    	r_case = self.get("r_case",0)
    	sumka = self.get("sumka",0)
    	portfel = self.get("portfel",0)
    	mif = self.get("mif",0)
    	crystal = self.get("crystal",0)
    	plasma = self.get("plasma",0)
    	zv = self.get("zv",0)
    	dk = self.get("dk",0)
    	plasma_boss = self.get("plasma_boss",0)
    	case_boss = self.get("case_boss",0)
    	rcase_boss = self.get("rcase_boss",0)
    	mifcase_boss = self.get("mifcase_boss",0)
    	essence_boss = self.get("essence_boss",0)
    	scrap = self.get("scrap",0)
    	medals = self.get("medals",0)
    	uron = self.get("uron",0)
    	uron_krit = self.get("uron_krit",0)
    	thx_plasm = self.get("thx_plasm",0)
    	thx_sun = self.get("thx_sun",0)
    	booster = self.get("booster",0)
    	boost_list = self.get("boost_list",{})
    	
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Руда на уровень"  in message.text:
    		clicks += 1
    		self.set("clicks",clicks)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "побежден игроком"  in message.text:
    		bosses += 1
    		self.set("bosses",bosses)
    		if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Плазма +" in message.text:
    		    text = message.text.replace(" (Бонус:  +200.0%)", "").replace(" (Бонус:  +100.0%)", "").replace("✨", "")
    		    pl_start = text.index("Плазма +") + len("Плазма +") # находим начало
    		    if (pl_start > 0):
    		        #pl_end = text.index(" (Бонус", pl_start) # находим конец 
    		        #if not (pl_end > 0):
    		        pl_end = text.index("</b>", pl_start) # находим конец                     
    		        pl_num = text[pl_start:pl_end] # извлекаем  
    		        plasmi = int(pl_num.replace("</b>","")) 
    		        plasma_boss += plasmi 
    		        self.set("plasma_boss",plasma_boss)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and  "<i>Найден Конверт <b>+1</b></i>" in message.text:
    		converts += 1
    		self.set("converts",converts)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and  "<i>Найден Конверт <b>+2</b></i>" in message.text:
    		converts += 2
    		self.set("converts",converts)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден Редкий Конверт <b>+1</b></i>" in message.text:
    		r_converts +=1
    		self.set("r_converts",converts)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден Редкий Конверт <b>+2</b></i>" in message.text:
    		r_converts +=2
    		self.set("r_converts",converts)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Кейс +1</b></i>" in message.text:
    		case += 1
    		self.set("case",case)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Кейс +2</b></i>" in message.text:
    		case += 2
    		self.set("case",case)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Дайс Кейс +1</b></i>" in message.text :
    		dk += 1
    		self.set("dk",dk)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Дайс Кейс +2</b></i>" in message.text :
    		dk += 2
    		self.set("dk",dk)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Редкий Кейс +1</b></i>" in message.text:
    		r_case += 1
    		self.set("r_case",r_case)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Редкий Кейс +2</b></i>" in message.text:
    		r_case += 2
    		self.set("r_case",r_case)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Мифический Кейс +1</b></i>" in message.text:
    		mif += 1
    		self.set("mif",mif)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Мифический Кейс +2</b></i>" in message.text :
    		mif += 2
    		self.set("mif",mif)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Кристальный Кейс +1</b></i>" in message.text:
    		crystal += 1
    		self.set("crystal",crystal)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<i>Найден <b>Кристальный Кейс +2</b></i>" in message.text:
    		crystal += 2
    		self.set("crystal",crystal)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<b>Сумка c Предметами +1</b>" in message.text:
    		sumka += 1
    		self.set("sumka",sumka)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<b>Сумка c Предметами +2</b>" in message.text:
    		sumka += 2
    		self.set("sumka",sumka)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<b>Портфель c Эскизами +1</b>" in message.text:
    		portfel += 1
    		self.set("portfel",portfel)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<b>Портфель c Эскизами +2</b>" in message.text:
    		portfel += 2
    		self.set("portfel",portfel)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "💫" in message.text:
    		zv += 1
    		self.set("zv",zv)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "<b><i>Плазма +" in message.text and "<b><i>Руда на уровень" in message.text:
    		pl_start = message.text.index("<b><i>Плазма +") + len("<b><i>Плазма +") # находим начало
    		if (pl_start > 0):
    			pl_end = message.text.index("</i></b>", pl_start) # находим конец 
    			pl_num = message.text[pl_start:pl_end] # извлекаем  
    			plasmi = int(pl_num) 
    			plasma += plasmi 
    			self.set("plasma",plasma)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Медаль" in message.text:
    		pattern = "Медаль +(.*?)</b>"
    		match = re.search(pattern, message.text, re.DOTALL)
    		if match:
    			medali = int(match.group(1))
    			medals += medali
    			self.set("medals",medals)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Эссенция" in message.text and "побежден игроком"  in message.text:
    		pattern = "Эссенция +(.*?)</b>"
    		match = re.search(pattern, message.text, re.DOTALL)
    		if match:
    			essence = int(match.group(1))
    			essence_boss += essence
    			self.set("essence_boss",essence_boss)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "повержен" in message.text:
    		bosses_victory += 1
    		self.set("bosses_victory",bosses_victory)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "побежден" in message.text and "Скрап" in message.text:
    		pattern = "Скрап +(.*?)</b>"
    		match = re.search(pattern, message.text, re.DOTALL)
    		if match:
    			scrapi = int(match.group(1))
    			scrap += scrapi
    			self.set("scrap",scrap)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "📦" in message.text and "Твоя награда" in message.text:
            pl_start = message.text.index("Кейс +") + len("Кейс +") # находим начало
            if (pl_start > 0):
                pl_end = message.text.index("</b>", pl_start) # находим конец 
                pl_num = message.text[pl_start:pl_end] # извлекаем  
                plasmi = int(pl_num) 
                case_boss += plasmi 
                self.set("case_boss",case_boss)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Найден бустер" in message.text:
            booster += 1
            pl_start = message.text.index("⚡") + len("⚡") # находим начало
            if (pl_start > 0):
                pl_end = message.text.index(")</b>", pl_start) + 1 # находим конец 
                pl_num = message.text[pl_start:pl_end] # извлекаем  
                boost_type = pl_num
                if boost_type in boost_list:
                    boost_list[boost_type] += 1
                else:
                    boost_list[boost_type] = 1
                self.set("boost_list",boost_list)
            self.set("booster",booster)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Редкий Кейс" in message.text and "Твоя награда" in message.text:
            pl_start = message.text.index("Кейс +") + len("Кейс +") # находим начало
            if (pl_start > 0):
                pl_end = message.text.index("</b>", pl_start) # находим конец 
                pl_num = message.text[pl_start:pl_end] # извлекаем  
                plasmi = int(pl_num) 
                rcase_boss += plasmi 
                self.set("rcase_boss",rcase_boss)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "Мифический Кейс" in message.text and "Твоя награда" in message.text:
            pl_start = message.text.index("Кейс +") + len("Кейс +") # находим начало
            if (pl_start > 0):
                pl_end = message.text.index("</b>", pl_start) # находим конец 
                pl_num = message.text[pl_start:pl_end] # извлекаем  
                plasmi = int(pl_num) 
                mifcase_boss += plasmi 
                self.set("mifcase_boss",mifcase_boss)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "нанес(ла) крит. удар" in message.text:            
                plasmi = 70 
                uron_krit += plasmi 
                self.set("uron_krit",uron_krit)
    	if (message.chat_id == 5522271758 or message.chat_id == 7168860714 or message.chat_id == 7084173311 or message.chat_id == 7066508668 or message.chat_id == 7168860714) and "нанес(ла) удар" in message.text:            
                plasmi = 35 
                uron += plasmi 
                self.set("uron",uron)
    	if hasattr(message, 'from_id') and message.from_id == 5522271758 and "🎆" in message.raw_text and "Sirius" in message.raw_text and "ты поблагодарил(а) игрока" in message.raw_text:
            ptthx = message.text.index("Награда :</b>  +") + len("Награда :</b>  +")
            pttthx = message.text.index(" 🎆</")
            ptttthx = message.text[ptthx:pttthx]
            pttttthx = ptttthx.replace(",","")
            thx_plasm += int(pttttthx)
            self.set("thx_plasm",thx_plasm)
    	if hasattr(message, 'from_id') and message.from_id == 5522271758 and "🎆" not in message.raw_text and "Sirius" in message.raw_text and "ты поблагодарил(а) игрока" in message.raw_text:
            ptthx = message.text.index("Награда :</b>  +") + len("Награда :</b>  +")
            pttthx = message.text.index("</i>") - 2
            ptttthx = message.text[ptthx:pttthx]
            pttttthx = ptttthx.replace(",","")
            thx_sun += int(pttttthx)
            self.set("thx_sun",thx_sun)
 
    @loader.command()
    async def qqq(self,message):
    	'''Показывает кейсы за всё время работы модуля'''
    	uron = self.get("uron",0)
    	booster = self.get("booster",0)
    	boost_list = self.get("boost_list",{})
    	uron_krit = self.get("uron_krit",0)
    	converts = self.get("converts",0)
    	clicks = self.get("clicks",0)
    	bosses = self.get("bosses",0)
    	r_converts = self.get("r_converts",0)
    	bosses_victory = self.get("bosses_victory",0)
    	case = self.get("case",0)
    	r_case = self.get("r_case",0)
    	mif = self.get("mif",0)
    	crystal = self.get("crystal",0)
    	plasma = self.get("plasma",0)
    	zv = self.get("zv",0)
    	dk = self.get("dk",0)
    	plasma_boss = self.get("plasma_boss",0)
    	scrap = self.get("scrap",0)
    	medals = self.get("medals",0)
    	case_boss = self.get("case_boss",0)
    	rcase_boss = self.get("rcase_boss",0)
    	thx_plasm = self.get("thx_plasm",0)
    	thx_sun = self.get("thx_sun",0)
    	mifcase_boss = self.get("mifcase_boss",0)
    	essence_boss = self.get("essence_boss",0)
    	sumka = self.get("sumka",0)
    	portfel = self.get("portfel",0)
    	start_time = self.get("start_time",time.time())
    	td = int(round((time.time() - start_time), 0))
    	days, total_seconds = divmod(td, 86400)
    	hours, remainder = divmod(total_seconds, 3600)
    	minutes, seconds = divmod(remainder, 60)
    	formatted_m = str(minutes).zfill(2)
    	formatted_s = str(seconds).zfill(2)
    	formatted_time = f"{days}д. {hours}:{formatted_m}:{formatted_s}"
    	result_ans = f"<b>💼 Всего сделано <code>{clicks}</code> кликов и добыто:</b>\n\n"
    	if (converts > 0):
    	    result_ans = result_ans + f"✉ <b>Конверты:</b> <code>{converts}</code>\n"
    	if (r_converts > 0):
    	    result_ans = result_ans + f"🧧 <b>Редкие конверты:</b> <code>{r_converts}</code>\n"
    	if (case > 0):
    	    result_ans = result_ans + f"📦 <b>Кейсы:</b> <code>{case}</code>\n"
    	if (r_case > 0):
    	    result_ans = result_ans + f"🗳 <b>Редкие кейсы:</b> <code>{r_case}</code>\n"
    	if (mif > 0):
    	    result_ans = result_ans + f"🕋 <b>Мифические кейсы:</b> <code>{mif}</code>\n"
    	if (crystal > 0):
    	    result_ans = result_ans + f"💎 <b>Кристальные кейсы</b> <code>{crystal}</code>\n"
    	if (dk > 0):
    	    result_ans = result_ans + f"🎲 <b>Дайс кейсы</b> <code>{dk}</code>\n"
    	if (zv > 0):
    	    result_ans = result_ans + f"🌌 <b>Звездные Кейсы:</b> <code>{zv}</code>\n"
    	if (sumka > 0):
    	    result_ans = result_ans + f"👜 <b>Сумки с предметами:</b> <code>{sumka}</code>\n"
    	if (portfel > 0):
    	    result_ans = result_ans + f"💼 <b>Портфели c Эскизами:</b> <code>{portfel}</code>\n"
    	
    	result_ans = result_ans + f"🎆 <b>Плазма:</b> <code>{plasma}</code>\n"
    	if (booster > 0):
    	    result_ans = result_ans + f"⚡ <b>Бусты:</b> <code>{booster}</code>, а именно:\n"
    	    for key, value in sorted(boost_list.items()):
    	        result_ans = result_ans + f"    {key}: <code>{value}</code>\n"
    	result_ans = result_ans + f"<b>\n👺 С <code>{bosses}</code> Боссов (<code>{bosses_victory}</code> повержено):</b>\n\n"
    	if (medals > 0):
    	    result_ans = result_ans + f"🎖 <b>Медали:</b> <code>{medals}</code>\n"
    	if (scrap > 0):
    	    result_ans = result_ans + f"🔩 <b>Скрап:</b> <code>{scrap}</code>\n"
    	if (plasma_boss > 0):
    	    result_ans = result_ans + f"🎆 <b>Плазма:</b> <code>{plasma_boss}</code>\n"
    	if (essence_boss > 0):
    	    result_ans = result_ans + f"🌀 <b>Эссенция:</b> <code>{essence_boss}</code>\n"
    	if (case_boss > 0):
    	    result_ans = result_ans + f"📦 <b>Кейсы:</b> <code>{case_boss}</code>\n"
    	if (rcase_boss > 0):
    	    result_ans = result_ans + f"🗳 <b>Редкие кейсы:</b> <code>{rcase_boss}</code>\n"
    	if (mifcase_boss > 0):
    	    result_ans = result_ans + f"🕋 <b>Мифические кейсы:</b> <code>{mifcase_boss}</code>\n"

    	result_ans = result_ans + f"\n🩸 <b>Нанесено урона:</b> <code>{uron}</code>\n💢 <b>Критического:</b> <code>{uron_krit}</code>\n\n 🎆 <b>Плазма с thx:</b> <code>{thx_plasm}</code>\n ☀️ <b>Солнечные фрагменты с thx:</b> <code>{thx_sun}</code> \n\nвремя работы:  <code>{formatted_time}</code>"
    	await utils.answer(message,result_ans)
    	#await utils.answer(message,f"<b>💼 Всего сделано <code>{clicks}</code> кликов и добыто:</b>\n\n✉ <b>Конверты:</b> <code>{converts}</code>\n🧧 <b>Редкие конверты:</b> <code>{r_converts}</code>\n📦 <b>Кейсы:</b> <code>{case}</code>\n🗳 <b>Редкие кейсы:</b> <code>{r_case}</code>\n🕋 <b>Мифические кейсы:</b> <code>{mif}</code>\n💎 <b>Кристальные кейсы</b> <code>{crystal}</code>\n🎲 <b>Дайс кейсы</b> <code>{dk}</code>\n🌌<b>Звездные Кейсы:</b> <code>{zv}</code>\n👜<b>Сумки с предметами:</b> <code>{sumka}</code>\n🎆 <b>Плазма:</b> <code>{plasma}</code>\n\n<b>👺 С <code>{bosses}</code> Боссов (<code>{bosses_victory}</code> повержено):</b>\n\n🎖 <b>Медали:</b> <code>{medals}</code>\n🔩 <b>Скрап:</b> <code>{scrap}</code>\n🎆 <b>Плазма:</b> <code>{plasma_boss}</code>\n🌀 <b>Эссенция:</b> <code>{essence_boss}</code>\n📦 <b>Кейсы:</b> <code>{case_boss}</code>\n🗳 <b>Редкие кейсы:</b> <code>{rcase_boss}</code>\n🕋 <b>Мифические кейсы:</b> <code>{mifcase_boss}</code>\n\n🩸 <b>Нанесено урона:</b> <code>{uron}</code>\n💢 <b>Критического:</b> <code>{uron_krit}</code>\n\n 🎆 <b>Плазма с thx:</b> <code>{thx_plasm}</code> \n\nвремя работы:  <code>{formatted_time}</code>")
    
    @loader.command()
    async def qqq_clear(self,message):
    	'''Очистка базы данных (всех кейсов и тд)'''
    	self.set("converts",0)
    	self.set("r_converts",0)
    	self.set("case",0)
    	self.set("r_case",0)
    	self.set("mif",0)
    	self.set("crystal",0)
    	self.set("plasma",0)
    	self.set("zv",0)
    	self.set("dk",0)
    	self.set("clicks",0)
    	self.set("bosses",0)
    	self.set("medals",0)
    	self.set("scrap",0)
    	self.set("plasma_boss",0)
    	self.set("case_boss",0)
    	self.set("rcase_boss",0)
    	self.set("bosses_victory",0)
    	self.set("uron_krit",0)
    	self.set("uron",0)
    	self.set("thx_plasm",0)
    	self.set("thx_sun",0)
    	self.set("sumka",0)
    	self.set("portfel",0)
    	self.set("mifcase_boss",0)
    	self.set("booster",0)
    	self.set("boost_list",{})
    	self.set("essence_boss",0)
    	self.set("start_time",time.time())
    	await utils.answer(message,"Статистика о кейсах и плазме очищена")
    	                
    async def cleardb(self, call: InlineCall):
    	# пака статистика
    	self.set("converts",0)
    	self.set("r_converts",0)
    	self.set("case",0)
    	self.set("r_case",0)
    	self.set("mif",0)
    	self.set("crystal",0)
    	self.set("plasma",0)
    	self.set("zv",0)
    	self.set("dk",0)
    	self.set("clicks",0)
    	self.set("bosses",0)
    	self.set("medals",0)
    	self.set("scrap",0)
    	self.set("plasma_boss",0)
    	self.set("case_boss",0)
    	self.set("rcase_boss",0)
    	self.set("bosses_victory",0)
    	self.set("sumka",0)
    	self.set("portfel",0)
    	self.set("mifcase_boss",0)
    	self.set("essence_boss",0)
    	self.set("booster",0)
    	self.set("boost_list",{})
    	self.set("start_time",time.time())
    	call.edit(call,"Статистика о кейсах и плазме очищена")