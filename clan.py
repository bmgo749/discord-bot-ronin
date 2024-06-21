import sqlite3
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Embed, Color, Button, Interaction, ButtonStyle
from nextcord.ui import View
import datetime, asyncio, pytz, random
from datetime import timedelta, time, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import deque

class ClanCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_clan(self, ctx, name: str = None, image: str = None, *, desc: str = None):
        if not name or not image or not desc:
            await ctx.send("**Please provide name, image URL, and description for your clan!**")
            return
    
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS clan (
        leader_id INTEGER PRIMARY KEY,
        member_ids TEXT,
        clan_name TEXT,
        image TEXT,
        description TEXT,
        level INTEGER,
        exp INTEGER,
        honor INTEGER
        )''')

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if clan:
            await ctx.send("**You already have a clan!**")
            cursor.close()
            db.close()
            return

        sql = '''INSERT INTO clan (leader_id, member_ids, clan_name, image, description, level, exp, honor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        val = (ctx.author.id, str(ctx.author.id), name, image, desc, 1, 0, 0)
        cursor.execute(sql, val)
        db.commit()

        new_clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if not new_clan:
            await ctx.send("**Failed to create clan. Please try again later.**")
            cursor.close()
            db.close()
            return

        embed = Embed(title="🏮 Successfully setup your clan!",
                      colour=Color.random())
        embed.add_field(name="<:emoji_4:1251444126571036693> Name Clan:", value=f"`{name}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader Clan:", value=f"`{ctx.author.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level Clan:", value=f"`Level {new_clan[5]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description Clan:", value=f"`{desc}`")
        embed.set_thumbnail(url=image)
        embed.timestamp = datetime.datetime.now()

        await ctx.reply(embed=embed, mention_author=False)

        cursor.close()
        db.close()

    @commands.command()
    async def leaderboard(self, ctx):
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM clan ORDER BY level DESC, exp DESC LIMIT 10")
            clans = cursor.fetchall()

            if not clans:
                await ctx.send("No clans found.")
                return

            embed = Embed(title="🏆 Clan Leaderboard", color=Color.gold())

            position = 1
            for clan in clans:
                leader_id = clan[0]
                leader = await self.bot.fetch_user(leader_id)
                embed.add_field(
                    name=f"{position}. {clan[2]} (Level {clan[5]})",
                    value=f"**Leader:** {leader.name}\n**Description:** {clan[4]}\n**Experience:** {clan[6]}",
                    inline=False,
                )
                position += 1

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred while executing the command.")
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def join_clan(self, ctx, *, name: str = None):
        if not name:
            await ctx.send("**Please specify the name of the clan you want to join!**")
            return
        
        if await self.is_in_clan(ctx.author.id):
            await ctx.send("**You are already in a clan!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute('SELECT * FROM clan WHERE clan_name LIKE ?', (f'%{name}%',)).fetchone()
        if not clan:
            await ctx.send("**Clan not found!**")
            return
        
        member_ids = clan[1].split(',')
        member_ids.append(str(ctx.author.id))

        cursor.execute('UPDATE clan SET member_ids = ? WHERE leader_id = ?', (','.join(member_ids), clan[0]))
        db.commit()

        embed = Embed(title=f"🔰 You have joined clan {name}",
                      description=f"**Welcome to clan** 🍃`{name}`**!, now you can access more feature in clan like donation or 🍀clan fight boss with your member clan!, check it out!🎲**",
                      colour=Color.random())
        embed.set_thumbnail(url=clan[3])
        embed.timestamp = datetime.datetime.now()
        await ctx.reply(embed=embed)

        cursor.close()
        db.close()

    @commands.command()
    async def leave_clan(self, ctx):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{ctx.author.id}%',)).fetchone()
        if not clan:
            await ctx.send("**You are not a member of any clan!**")
            cursor.close()
            db.close()
            return
        
        if str(ctx.author.id) == str(clan[0]):
            await ctx.send("**As the leader of the clan, you cannot leave! You can delete the clan instead.**")
            cursor.close()
            db.close()
            return

        member_ids = clan[1].split(',')
        if str(ctx.author.id) in member_ids:
            member_ids.remove(str(ctx.author.id))
        else:
            await ctx.send("**You are not a member of this clan!**")
            cursor.close()
            db.close()
            return

        cursor.execute('UPDATE clan SET member_ids = ? WHERE leader_id = ?', (','.join(member_ids), clan[0]))
        db.commit()

        embed = Embed(title="You left the clan!",
                      description=f"🏴 **You have left clan** `{clan[2]}`**. You can join another clan now.**")
        embed.timestamp = datetime.datetime.now()

        await ctx.reply(embed=embed)

        cursor.close()
        db.close()

    @commands.command()
    async def search_clan(self, ctx, clan_name: str = None):
        if not clan_name:
            await ctx.send("**Please specify the name of the clan you want to search!**")
            return
    
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('SELECT * FROM clan WHERE clan_name LIKE ?', (f'%{clan_name}%',))
        clan = cursor.fetchone()

        if not clan:
            await ctx.send("**Clan not found!**")
            cursor.close()
            db.close()
            return

        try:
            leader = await self.bot.fetch_user(clan[0])  # Assuming clan[0] is leader_id
        except nextcord.errors.NotFound:
            leader = "Unknown Leader"

        member_ids = clan[1].split(',')
        member_names = []
        for member_id in member_ids:
            try:
                member = await self.bot.fetch_user(int(member_id))
                member_names.append(member.name)
            except nextcord.errors.NotFound:
                member_names.append("Unknown Member")

        embed = Embed(title=f"{clan_name} Clan Information 🏮",
                     colour=Color.random())
        embed.add_field(name="<:emoji_4:1251444126571036693> Name Clan:", value=f"`{clan_name}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader Clan:", value=f"`{leader.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level Clan:", value=f"`Level {clan[5]}`")
        embed.add_field(name="<:emoji_6:1251444163225063534> EXP Clan:", value=f"`EXP {clan[6]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description Clan:", value=f"`{clan[4]}`")
        embed.add_field(name="⛩️ Members:", value=f"`{', '.join(member_names)}`")
        embed.set_thumbnail(url=clan[3])
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        await ctx.reply(embed=embed)

        cursor.close()
        db.close()

    @commands.command()
    async def hall_clan(self, ctx):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{ctx.author.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await ctx.send("**You are not a member of any clan!**")
            cursor.close()
            db.close()
            return
        
        view = ButtonClan(ctx.author.id)
        
        try:
            leader = await self.bot.fetch_user(clan[0])
        except nextcord.errors.NotFound:
            leader = "Unknown Leader"

        member_ids = clan[1].split(',')
        member_names = []
        for member_id in member_ids:
            try:
                member = await self.bot.fetch_user(int(member_id))
                member_names.append(member.name)
            except nextcord.errors.NotFound:
                member_names.append("Unknown Member")
        
        embed = Embed(title=f"🍀 Welcome to {clan[2]} Clan Hall!",
                      description=f"**⛩️ You can access some clan features in this hall. 🎲**",
                      colour=Color.random())
        embed.add_field(name="<:emoji_4:1251444126571036693> Name Clan:", value=f"`{clan[2]}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader Clan:", value=f"`{leader.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level Clan:", value=f"`Level {clan[5]}`")
        embed.add_field(name="<:emoji_6:1251444163225063534> EXP Clan:", value=f"`EXP {clan[6]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description Clan:", value=f"`{clan[4]}`")
        embed.add_field(name="🍀 Honor Clan:", value=f"`{clan[7]} Honor Point`")
        embed.add_field(name="⛩️ Members:", value=f"`{', '.join(member_names)}`")
        embed.set_thumbnail(url=clan[3])
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        await ctx.send(embed=embed, view=view)

        cursor.close()
        db.close()

    @commands.command()
    async def delete_clan(self, ctx):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if not clan:
            await ctx.send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return

        cursor.execute('DELETE FROM clan WHERE leader_id = ?', (ctx.author.id,))
        db.commit()

        embed = Embed(title="🏴 Clan Deleted!",
                      description=f"**Your clan** `{clan[2]}` **has been successfully deleted. You can join another clan now.**")
        embed.timestamp = datetime.datetime.now()

        await ctx.reply(embed=embed)

        cursor.close()
        db.close()

    async def is_in_clan(self, user_id):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        clan = cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{user_id}%',)).fetchone()
        db.close()
        return bool(clan)
    
    @commands.command()
    async def edit_nameclan(self, ctx, new_name: str = None):
        if new_name is None:
            await ctx.send("**TYPE THE NEW NAME OF YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if not clan:
            await ctx.send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        cursor.execute("UPDATE clan SET clan_name = ? WHERE leader_id = ?", (new_name, ctx.author.id,))
        db.commit()

        await ctx.reply(f"**YOU ALREADY SET NEW CLAN NAME INTO ==>** `{new_name}` ⛩️")

        cursor.close()
        db.close

    @commands.command()
    async def edit_imageclan(self, ctx, new_image: str = None):
        if new_image is None:
            await ctx.send("**GIVE THE NEW URL IMAGE YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if not clan:
            await ctx.send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        cursor.execute("UPDATE clan SET image = ? WHERE leader_id = ?", (new_image, ctx.author.id,))
        db.commit()

        await ctx.reply(f"**YOU ALREADY SET NEW IMAGE, CHECK IT IN HALL_CLAN OR SEARCH_CLAN 🏮**")

        cursor.close()
        db.close

    @commands.command()
    async def edit_description(self, ctx, *, new_desc: str = None):
        if new_desc is None:
            await ctx.send("**TYPE THE NEW DESCRIPTION OF YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", (ctx.author.id,)).fetchone()
        if not clan:
            await ctx.send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        cursor.execute("UPDATE clan SET description = ? WHERE leader_id = ?", (new_desc, ctx.author.id,))
        db.commit()

        await ctx.reply(f"**YOU ALREADY SET NEW CLAN DESCRIPTION INTO ==>** `{new_desc}` 🎲")

        cursor.close()
        db.close

class ButtonClan(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    def disable_shop_button(self):
        for child in self.children:
            if isinstance(child, nextcord.ui.Button) and child.label == "Trading Post":
                child.disabled = True
                break

    def enable_shop_button(self):
        for child in self.children:
            if isinstance(child, nextcord.ui.Button) and child.label == "Trading Post":
                child.disabled = False
                break

    async def interaction_check(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("**You are not allowed to interact with this button.**", ephemeral=True)
            return False
        return True

    @nextcord.ui.button(label="Donation", style=nextcord.ButtonStyle.green, emoji="<:coin3:1250433911885004811>")
    async def on_button_callback(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        if ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return

        embed = nextcord.Embed(title="Donation Options", description="Choose your donation option:", color=nextcord.Color.random())
        embed.add_field(name="<:coin3:1250433911885004811> 500 Coins", value="**Donate 500 <:coin3:1250433911885004811> coins to get 20 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.add_field(name="<:coin3:1250433911885004811> 1000 Coins", value="**Donate 1000 <:coin3:1250433911885004811> coins to get 40 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.add_field(name="<:jade:1249302977450344481> 100 Jade", value="**Donate 100 <:jade:1249302977450344481> Jade to get 80 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        view = DonateClan(ctx.user.id)
        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)

    @nextcord.ui.button(label="Clan Boss", style=nextcord.ButtonStyle.red, emoji="<:emoji_5:1251444143884992604>")
    async def global_boss_button_callback(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await ctx.response.send_message("**YOU ARE NOT IN ANY CLAN!**", ephemeral=True)
            return
        
        await ctx.response.send_message("**🏮 STILL IN DEVELOPMENT!, STAY TUNE! ⚔️**")

    @nextcord.ui.button(label="Facillity", style=nextcord.ButtonStyle.blurple, emoji="⛩️")
    async def facility_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):
        if ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND!**", ephemeral=True)

        view = FacillityView()

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        alter_table_queries = [
            "ALTER TABLE clan ADD COLUMN training_ground INTEGER DEFAULT 0",
            "ALTER TABLE clan ADD COLUMN castle INTEGER DEFAULT 0",
            "ALTER TABLE clan ADD COLUMN trade_post INTEGER DEFAULT 0",
            "ALTER TABLE clan ADD COLUMN kurama_temple INTEGER DEFAULT 0"
        ]

        for query in alter_table_queries:
            try:
                cursor.execute(query)
                print(f"Kolom berhasil ditambahkan: {query}")
            except sqlite3.OperationalError as e:
                print(f"Kolom mungkin sudah ada atau terjadi kesalahan: {e}")

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
        clans = cursor.fetchone()

        if not clans:
            await ctx.response.send_message("LOL")
            return
        
        name = clans[2]
        land = clans[8]
        castle = clans[9]
        temple = clans[11]
        shop = clans[10]

        embed = nextcord.Embed(title="⛩️ Clan Facilities 🎲", description=f"**🏮 STATUS OF {name} FEATURE 🍀**", colour=nextcord.Color.dark_red())
        embed.add_field(name="<:doubsword:1252197660899803176> Land of Sekigahara", value=f"`Level {land}` **(<:doubsword:1252197660899803176> Increases Attack by 20% : UNLOCK PER LEVEL REQUIRED 40-45 HONOR POINT)**", inline=False)
        embed.add_field(name="<:castle1:1252197628217786368> Castle Hokoku", value=f"`Level {castle}` **(<:castle1:1252197628217786368> Increases HP by 20% : UNLOCK PER LEVEL REQUIRED 40-45 HONOR POINT)**", inline=False)
        embed.add_field(name="<:temple1:1252197648727801896> Temple Kurama Dera", value=f"`Level {temple}` **(<:temple1:1252197648727801896> Increases Attack and HP by 10% : UNLOCK PER LEVEK REQUIRED 40-45 HONOR POINT)**", inline=False)
        embed.add_field(name="<:trading:1252197613571280916> Trade Post", value=f"`Level {shop}` **(<:trading:1252197613571280916> Unlock trade feature of clan : UNLOCK PLACE REQUIRED 50 HONOR POINT)**", inline=False)
        embed.set_footer(text="TO GET HONOR POINT, YOU CAN GET IT FROM DONATION OR FIGHTING ENEMY OR BOSS ⚔️")
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=clans[3])
        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)

        db.commit()
        db.close()

    @nextcord.ui.button(label="Trading Post", style=nextcord.ButtonStyle.gray, emoji="<:trading:1252197613571280916>")
    async def trading_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        if ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await ctx.response.send_message("**YOU DONT IN ANY ALLIANCE!**", ephemeral=True)
            return
        
        trade_post = clan[10]

        if trade_post < 1:
            await ctx.response.send_message("**YOUR CLAN TRADING SHOP FEATURE HAS NOT BEEN UNLOCK!, UNLOCK IT FIRST AND YOU CAN USE IT!**", ephemeral=True)
            return

        embed = Embed(title="WELCOME TO TRADING POST CLAN! ⚖️",
                      description=f"**🔰 Welcome to trading post clan, 🍀 in this place you can buy any stuff like valuable stuff, 🌿 legendary stuff or jade or coin. 🏮You can just buy it with ur jade or coin or trade with you equipment! 🎲**",
                      colour=Color.random())
        embed.add_field(name="<:naginata:1253647561143619696> Naginata Blade", value="`750` **<a:coin2:1249302963042648094> Jade**", inline=False)
        embed.add_field(name="<:gozen:1253647592772866100> Gozen's Bow", value="`70000` **<a:coin2:1249302963042648094> Coin**", inline=False)
        embed.add_field(name="<:foxring:1253647911057887383> Blood Fox Ring", value="`475` **<a:coin2:1249302963042648094> Jade**")
        embed.set_footer(text="FOR NOW YOU CAN'T BUY IT BUT IN THE NEXT UPDATE YOU CAN BUY IT!!!")
        embed.timestamp = datetime.datetime.now()
        await ctx.response.send_message(embed=embed, ephemeral=True)
        
        db.commit()
        db.close()

class DonateClan(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.db = sqlite3.connect("main.sqlite")
        self.cursor = self.db.cursor()
        self.user_id = user_id
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.reset_donation_count, trigger='cron', hour=7, minute=0, second=0, timezone='Asia/Jakarta')
        self.scheduler.start()
        print("Scheduler started successfully!")

    def reset_donation_count(self):
        try:
            now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
            if now.hour == 7 and now.minute == 0:
                with sqlite3.connect("main.sqlite") as db:
                    cursor = db.cursor()
                    cursor.execute(f"UPDATE donations SET donation_count = 0")
                    db.commit()
                print("Donation count reset successfully!")
            else:
                print("Scheduler triggered, but not yet time to reset.")
        except Exception as e:
            print(f"ERROR {str(e)}")

    async def interaction_check(self, interaction):
        return interaction.user.id == self.user_id

    async def on_timeout(self):
        # Tidak perlu menutup koneksi di sini, karena digunakan dengan konteks
        pass

    @nextcord.ui.button(label="Donate 500 Coin", style=nextcord.ButtonStyle.green, emoji="<:coin3:1250433911885004811>")
    async def donate2_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        try:
            if ctx.user.id != self.user_id:
                await ctx.response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await ctx.response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", (ctx.user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await ctx.response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if coin < 500:
                    await ctx.message.reply("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", (ctx.user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await ctx.response.send_message("**⚖️ You have reached the max donation count for today! Please wait until reset in 00.00 UTC!🎲**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 20, f'%{ctx.user.id}%',))
                cursor.execute("UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - 500, ctx.user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", (ctx.user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", (ctx.user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ctx.user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user {ctx.user.id}")
                
                await ctx.response.send_message(f"**🍀YOU ALREADY DONATE A** `500` **<:coin3:1250433911885004811> COIN FOR** `20` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

        except Exception as e:
            print(f"ERROR in donate_button_callback: {str(e)}")

    @nextcord.ui.button(label="Donate 1000 Coin", style=nextcord.ButtonStyle.green, emoji="<:coin3:1250433911885004811>")
    async def donate_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        try:
            if ctx.user.id != self.user_id:
                await ctx.response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await ctx.response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", (ctx.user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await ctx.response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if coin < 1000:
                    await ctx.message.reply("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", (ctx.user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await ctx.response.send_message("**You have reached the max donation count for today! Please wait until reset in 00.00 UTC!**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 40, f'%{ctx.user.id}%',))
                cursor.execute("UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - 1000, ctx.user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", (ctx.user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", (ctx.user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ctx.user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user {ctx.user.id}")
                
                await ctx.response.send_message(f"**🍀YOU ALREADY DONATE A** `1000` **<:coin3:1250433911885004811> COIN FOR** `40` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

        except Exception as e:
            print(f"ERROR in donate_button_callback: {str(e)}")

    @nextcord.ui.button(label="Donate 100 Jade", style=nextcord.ButtonStyle.green, emoji="<:jade:1249302977450344481>")
    async def donate3_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        try:
            if ctx.user.id != self.user_id:
                await ctx.response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await ctx.response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", (ctx.user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await ctx.response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if jade < 100:
                    await ctx.message.reply("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", (ctx.user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await ctx.response.send_message("**You have reached the max donation count for today! Please wait until reset in 00.00 UTC!**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 80, f'%{ctx.user.id}%',))
                cursor.execute("UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - 100, ctx.user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", (ctx.user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", (ctx.user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ctx.user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user {ctx.user.id}")
                
                await ctx.response.send_message(f"**🍀YOU ALREADY DONATE A** `100` **<:jade:1249302977450344481> JADE FOR** `80` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

        except Exception as e:
            print(f"ERROR in donate_button_callback: {str(e)}")


class FacillityView(View):

    @nextcord.ui.select(
        placeholder="FACILITY UPGRADE OPTION",
        options=[
            nextcord.SelectOption(label="Land of Sekigahara", value="1", description="Upgraded your Combat Land!", emoji="<:doubsword:1252197660899803176>"),
            nextcord.SelectOption(label="Castle Hokoku", value="2", description="Upgraded your Training Place!", emoji="<:castle1:1252197628217786368>"),
            nextcord.SelectOption(label="Temple Kurama Dera", value="3", description="Upgraded your Meditation Place!", emoji="<:temple1:1252197648727801896>"),
            nextcord.SelectOption(label="Trade Post", value="4", description="Unlock Trading Post Clan", emoji="<:trading:1252197613571280916>")
        ]
    )

    async def select_callback(self, select, ctx: Interaction):
        select.disabled=True
        if select.values[0] == "1":

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await ctx.response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[8]
            honor = clan[7]

            cursor.execute(f"SELECT attack FROM stats WHERE user_id = ?", (ctx.user.id,))
            stats = cursor.fetchone()

            if not stats:
                await ctx.response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
                return

            if combat == 0:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 1:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 2:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 3:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 4:
                amount = round(0.04 * stats[0])
                cost = 45
                lvl = 1
            else:
                await ctx.response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await ctx.response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await ctx.response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET training_ground = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE stats SET attack = ? WHERE user_id = ?", (stats[0] + amount, ctx.user.id))

            embed = Embed(
                title="⚔️ LAND OF SEKIGAHARA UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Training Combat place in <:doubsword:1252197660899803176> Sekigahara Land, Level ⚔️ Land of Sekigahara became Grade** `{level}` **and the feature is Unlock! Now your attack is increasing 4% by your damage now =>** `{amount}` **Damage.**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Land of Sekigahara successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await ctx.message.reply(embed=embed, delete_after=20, mention_author=False)

            db.commit()
            cursor.close()
            db.close()

        if select.values[0] == "2":

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await ctx.response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[9]
            honor = clan[7]

            cursor.execute(f"SELECT hp FROM stats WHERE user_id = ?", (ctx.user.id,))
            stats = cursor.fetchone()

            if not stats:
                await ctx.response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
                return

            if combat == 0:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 1:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 2:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 3:
                amount = round(0.04 * stats[0])
                cost = 40
                lvl = 1
            elif combat == 4:
                amount = round(0.04 * stats[0])
                cost = 45
                lvl = 1
            else:
                await ctx.response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await ctx.response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await ctx.response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET castle = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (stats[0] + amount, ctx.user.id))
            cursor.execute("UPDATE stats SET maxhp = ? WHERE user_id = ?", (stats[0] + amount, ctx.user.id))

            embed = Embed(
                title="🏯 CASTLE HOKOKU UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Training place in <:castle1:1252197628217786368> Castle Hokoku, Level 🏯 Castle Hokoku became Grade** `{level}` **and the feature is Unlock! Now your HP is increasing 4% by your HP now =>** `{amount}` **Health Point.**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Castle Hokoku successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await ctx.message.reply(embed=embed, delete_after=30, mention_author=False)

            db.commit()
            cursor.close()
            db.close()

        if select.values[0] == "3":

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await ctx.response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[11]
            honor = clan[7]

            cursor.execute(f"SELECT attack, hp, maxhp FROM stats WHERE user_id = ?", (ctx.user.id,))
            stats = cursor.fetchone()

            if not stats:
                await ctx.response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
                return

            if combat == 0:
                amount = round(0.02 * stats[0])
                amount1 = round(0.02 * stats[1])
                cost = 40
                lvl = 1
            elif combat == 1:
                amount = round(0.02 * stats[0])
                amount1 = round(0.02 * stats[1])
                cost = 45
                lvl = 1
            elif combat == 2:
                amount = round(0.02 * stats[0])
                amount1 = round(0.02 * stats[1])
                cost = 45
                lvl = 1
            elif combat == 3:
                amount = round(0.02 * stats[0])
                amount1 = round(0.02 * stats[1])
                cost = 50
                lvl = 1
            elif combat == 4:
                amount = round(0.02 * stats[0])
                amount1 = round(0.02 * stats[1])
                cost = 50
                lvl = 1
            else:
                await ctx.response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await ctx.response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await ctx.response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET kurama_temple = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE stats SET attack = ? WHERE user_id = ?", (stats[0] + amount, ctx.user.id))
            cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (stats[1] + amount1, ctx.user.id))
            cursor.execute("UPDATE stats SET maxhp = ? WHERE user_id = ?", (stats[2] + amount1, ctx.user.id))

            embed = Embed(
                title="⛩️ TEMPLE KURAMA DERA UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Meditation place in <:temple1:1252197648727801896> Temple Kurama Dera, Level ⛩️ Temple Kurama Dera became Grade** `{level}` **and the feature is Unlock! Now your HP and Attack is increasing 4% by your HP and Attack now =>** `{amount1}` **Health Point,** `{amount}` **Damage**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Temple Kurama Dera successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await ctx.message.reply(embed=embed, delete_after=30, mention_author=False)

            db.commit()
            cursor.close()
            db.close()
        
        if select.values[0] == "4":

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ctx.user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await ctx.response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[10]
            honor = clan[7]

            cursor.execute(f"SELECT attack, hp, maxhp FROM stats WHERE user_id = ?", (ctx.user.id,))
            stats = cursor.fetchone()

            if not stats:
                await ctx.response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
                return

            if combat == 0:
                cost = 50
                lvl = 1
            else:
                await ctx.response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await ctx.response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 1:
                await ctx.response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 1**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET trade_post = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ctx.user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ctx.user.id}%',))

            embed = Embed(
                title="⛩️ TEMPLE KU SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Trading Post place <:trading:1252197613571280916> , Level ⚖️ Trading Post became Grade** `{level} (MAX)` **and the feature is Unlock! Now you can buy some Legendary Spear Jade or Legendary Bow or Some cool stuff that limited!🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Trading Post successfully unlocked!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await ctx.message.reply(embed=embed, delete_after=30, mention_author=False)

            db.commit()
            cursor.close()
            db.close()