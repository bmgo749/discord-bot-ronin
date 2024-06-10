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
            user_id INTERGER, attack INTERGER, hp INTERGER, posture INTERGER, poison_dmg INTERGER, burn_dmg INTERGER, lifesteal INTERGER, crit INTERGER, dodge INTERGER,
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
            user_id INTERGER, slot1 INTERGER, slot2 INTERGER, slot3 INTERGER
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
            sql = ("INSERT INTO stats(user_id, attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (author.id, 30, 150, 100, 0, 0, 0, 0, 0, 15)
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
            val = (author.id, 100, 1000)
            cursor.execute(sql, val)

        cursor.execute(f"SELECT user_id FROM equipment WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO equipment(user_id, slot1, slot2, slot3) VALUES (?, ?, ?, ?)")
            val = (author.id, 1, 1, 1)
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()