import random, nextcord, asyncio, sqlite3
from nextcord.ext import commands

class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
            user_id INTERGER, attack INTERGER, hp INTERGER, posture INTERGER, poison_dmg INTERGER, burn_dmg INTERGER, lifesteal INTERGER, crit INTERGER, dodge INTERGER, block INTERGER, maxhp INTERGER
            block INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
            user_id INTERGER, roles INTERGER, char_name INTERGER, gender INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS level (
            user_id INTERGER, level INTERGER, talent INTERGER, exp INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS jewelry2 (
            user_id INTERGER, jade INTERGER, coin INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipment (
            user_id INTERGER, slot1 INTERGER, slot2 INTERGER, slot3 INTERGER, slot4 INTERGER, slot5 INTERGER, slot6 INTERGER, slot7 INTERGER, slot8 INTERGER, slot9 INTERGER, slot10 INTERGER, slot11 INTERGER, slot12 INTERGER, slot13 INTERGER, slot14 INTERGER, slot15 INTERGER, slot16 INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipdata (
            user_id INTERGER, katana INTERGER, armor INTERGER, necklace INTERGER, ring1 INTERGER, ring2 INTERGER, fan INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS talenttree1 (
            user_id INTERGER, tameshigiri INTERGER, storm INTERGER, sharp INTERGER, strike INTERGER, life_blow INTERGER, leech INTERGER, sword_enchant INTERGER, poison_sword INTERGER, sword_agil INTERGER, flow INTERGER, blood_pene INTERGER, sword_pos INTERGER, dissension INTERGER, resistance INTERGER, talisman INTERGER, orbs INTERGER, phoenix INTERGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS talenttree2 (
            user_id INTERGER, vitality INTERGER, vitalpos INTERGER, dodge INTERGER, scud INTERGER, flow INTERGER, sturdy INTERGER, penet INTERGER, blockedsoul INTERGER, yokaiscroll INTERGER, heartspirit INTERGER, hawkeye INTERGER, concentrate INTERGER, acc INTERGER, stormmove INTERGER, steelwill INTERGER, firemove INTERGER, craziness INTERGER, onimusha INTERGER, gauge INTERGER
        )''')
        print("Data online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        author = message.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM stats WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO stats(user_id, attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, 30, 150, 100, 0, 0, 0, 0, 0, 15, 150)
            cursor.execute(sql, val)
        
        cursor.execute(f"SELECT user_id FROM data WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO data(user_id, roles, char_name, gender) VALUES (?, ?, ?, ?)")
            val = (author.id, "Ronin", "Kenshin Iwamura", "Man")
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM level WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO level(user_id, level, talent, exp) VALUES (?, ?, ?, ?)")
            val = (author.id, 1, 0, 0)
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM jewelry2 WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO jewelry2(user_id, jade, coin) VALUES (?, ?, ?)")
            val = (author.id, 250, 2500)
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM equipment WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO equipment(user_id, slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM talenttree1 WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO talenttree1(user_id, tameshigiri, storm, sharp, strike, life_blow, leech, sword_enchant, poison_sword, sword_agil, flow, blood_pene, sword_pos, dissension, resistance, talisman, orbs, phoenix) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
        
        cursor.execute(f"SELECT user_id FROM talenttree2 WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO talenttree2(user_id, vitality, vitalpos, dodge, scud, flow, sturdy, penet, blockedsoul, yokaiscroll, heartspirit, hawkeye, concentrate, acc, stormmove, steelwill, firemove, craziness, onimusha, gauge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Locked", 0)
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM equipdata WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO equipdata(user_id, katana, armor, necklace, ring1, ring2, fan) VALUES (?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, "", "", "", "", "", "")
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()