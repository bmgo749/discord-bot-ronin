import sqlite3
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Embed, Color, Button, Interaction, ButtonStyle
from nextcord.ui import View
import datetime, asyncio, pytz, random
from datetime import timedelta, time, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import deque

cooldowns = {}

def check_cooldown(user_id, command_name, cooldown_seconds):
    current_time = datetime.datetime.now().timestamp()
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    user_cooldowns = cooldowns[user_id]

    if command_name in user_cooldowns:
        last_used = user_cooldowns[command_name]
        if (current_time - last_used) < cooldown_seconds:
            return False, cooldown_seconds - (current_time - last_used)
    
    user_cooldowns[command_name] = current_time
    return True, 0

class ClanCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='start_mission', description='Start Mission and get reward from Mr. Kurobahaki!', force_global=bool)
    @commands.cooldown(1, 86400, commands.BucketType.user)  # Cooldown 24 jam per pengguna
    async def start_mission(self, ctx: Interaction):

        is_allowed, retry_after = check_cooldown(ctx.user.id, 'start_mission', 86400)
        if not is_allowed:
            embed = Embed(description=f"**You are still on cooldown!**\n\n`Cooldown time = {int(retry_after)} seconds`")
            await ctx.send(embed=embed, ephemeral=True)
            return

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        user_id =  ctx.user.id

        send =  ctx.send

        send = ctx.send
        author = ctx.user

        # Periksa apakah pengguna sudah memiliki misi yang sedang berjalan
        cursor.execute("SELECT * FROM missions WHERE user_id = ?", (user_id,))
        existing_mission = cursor.fetchone()

        if existing_mission:
            if existing_mission[3]:  # Jika misi sudah selesai (completed = bool)
                # Hapus misi yang sudah selesai sebelumnya
                cursor.execute("DELETE FROM missions WHERE user_id = ?", (user_id,))
                db.commit()
            else:
                await  send("**You already have an ongoing mission! Complete it before starting a new one.**")
                return

        # Tentukan NPC untuk misi
        npc_names = [
            '<:saito:1252525845101150279> Saito Nobumasa - The Best Japan Spearman',
            '<:hironi:1252525784384409600> Elite Samurai - Hirano Masanori',
            '<:kuroda:1253998989582405683> Kuroda Takanosuke - Master of Gun Flames',
            '<:kumabe:1253998984129810482> Rikishi Kumabe - Monk of Boju'
            # Tambahkan NPC lain sesuai kebutuhan
        ]
        mission_npc = random.choice(npc_names)

        # Simpan misi ke dalam database
        current_time = datetime.datetime.now()
        cursor.execute("INSERT INTO missions (user_id, mission, npc_name, completed, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (user_id, "Defeat the NPC", mission_npc, False, current_time))
        db.commit()

        embed = Embed(title="🎯 Daily Mission Started!",
                      description=f"**Your mission is to defeat the NPC {mission_npc}. 📜 You will get some bonus from Sir Kurobahaki if you defeat him. Good Luck!**")
        embed.timestamp = current_time

        await send(embed=embed)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='create_clan', description='Creating clan and get some feature!', force_global=bool)
    async def create_clan(self,  ctx: Interaction, name: str = None, image: str = None, *, desc: str = None):

        send = ctx.send
        author = ctx.user
        send = ctx.send

        if not name or not image or not desc:
            await  send("**Please provide name, image URL, and description for your clan!**")
            return
    
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if clan:
            await  send("**You already have a clan!**")
            cursor.close()
            db.close()
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        if path is None or path == "":
            await  send("`You are not choosing your own path, choose it first in` **start** `command!`")
            return

        sql = '''INSERT INTO clan (leader_id, member_ids, clan_name, image, description, level, exp, honor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        val = ( author.id, str( author.id), name, image, desc, 1, 0, 0)
        cursor.execute(sql, val)
        db.commit()

        new_clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not new_clan:
            await  send("**Failed to create clan. Please try again later.**")
            cursor.close()
            db.close()
            return

        embed = Embed(title="🏮 Successfully setup your clan!",
                      colour=Color.random())
        embed.add_field(name="<:emoji_4:1251444126571036693> Name Clan:", value=f"`{name}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader Clan:", value=f"`{ author.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level Clan:", value=f"`Level {new_clan[5]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description Clan:", value=f"`{desc}`")
        embed.set_thumbnail(url=image)
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed, mention_author=False)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='leaderboard', description='Show leaderboard clan', force_global=bool)
    async def leaderboard(self, ctx: Interaction):

        send = ctx.send
        author = ctx.user
        send = ctx.send

        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM clan ORDER BY level DESC, exp DESC LIMIT 10")
            clans = cursor.fetchall()

            if not clans:
                await  send("No clans found.")
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

            await  send(embed=embed)

        except Exception as e:
            print(f"An error occurred: {e}")
            await  send("An error occurred while executing the command.")
        finally:
            cursor.close()
            db.close()

    @nextcord.slash_command(name='join_clan', description='Join any clan', force_global=bool)
    async def join_clan(self,  ctx: Interaction, *, name: str = None):

        send = ctx.send
        author = ctx.user
        send = ctx.send

        if not name:
            await  send("**Please specify the name of the clan you want to join!**")
            return
        
        if await self.is_in_clan( author.id):
            await  send("**You are already in a clan!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute('SELECT * FROM clan WHERE clan_name LIKE ?', (f'%{name}%',)).fetchone()
        if not clan:
            await  send("**Clan not found!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        member_ids = clan[1].split(',')
        member_ids.append(str( author.id))

        cursor.execute('UPDATE clan SET member_ids = ? WHERE leader_id = ?', (','.join(member_ids), clan[0]))
        db.commit()

        embed = Embed(title=f"🔰 You have joined clan {name}",
                      description=f"**Welcome to clan** 🍃`{name}`**!, now you can access more feature in clan like donation or 🍀clan fight boss with your member clan!, check it out!🎲**",
                      colour=Color.random())
        embed.set_thumbnail(url=clan[3])
        embed.timestamp = datetime.datetime.now()
        await  send(embed=embed)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='leave_clan', description='Leaving any clan', force_global=bool)
    async def leave_clan(self, ctx: Interaction):

        send = ctx.send
        author = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{ author.id}%',)).fetchone()
        if not clan:
            await  send("**You are not a member of any clan!**")
            cursor.close()
            db.close()
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        if str( author.id) == str(clan[0]):
            await  send("**As the leader of the clan, you cannot leave! You can delete the clan instead.**")
            cursor.close()
            db.close()
            return

        member_ids = clan[1].split(',')
        if str( author.id) in member_ids:
            member_ids.remove(str( author.id))
        else:
            await  send("**You are not a member of this clan!**")
            cursor.close()
            db.close()
            return

        cursor.execute('UPDATE clan SET member_ids = ? WHERE leader_id = ?', (','.join(member_ids), clan[0]))
        db.commit()

        embed = Embed(title="You left the clan!",
                      description=f"🏴 **You have left clan** `{clan[2]}`**. You can join another clan now.**")
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='search_clan', description='Searching any clan by their name', force_global=bool)
    async def search_clan(self,  ctx: Interaction, clan_name: str = None):

        send = ctx.send
        author = ctx.user

        if not clan_name:
            await  send("**Please specify the name of the clan you want to search!**")
            return
    
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return

        cursor.execute('SELECT * FROM clan WHERE clan_name LIKE ?', (f'%{clan_name}%',))
        clan = cursor.fetchone()

        if not clan:
            await  send("**Clan not found!**")
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
        embed.add_field(name="<:emoji_4:1251444126571036693> Clan Name:", value=f"`{clan_name}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader:", value=f"`{leader.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level:", value=f"`Level {clan[5]}`")
        embed.add_field(name="<:emoji_6:1251444163225063534> EXP:", value=f"`EXP {clan[6]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description:", value=f"`{clan[4]}`")
        embed.set_thumbnail(url=clan[3])
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='hall_clan', description='Showing some clan feature', force_global=bool)
    async def hall_clan(self, ctx: Interaction):

        send = ctx.send
        author = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{ author.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await  send("**You are not a member of any clan!**")
            cursor.close()
            db.close()
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        view = ButtonClan( author.id)
        
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
        embed.add_field(name="<:emoji_4:1251444126571036693> Clan Name:", value=f"`{clan[2]}`")
        embed.add_field(name="<:emoji_8:1251444230031806484> Leader:", value=f"`{leader.name}`")
        embed.add_field(name="<:emoji_8:1251444211056771092> Level:", value=f"`Level {clan[5]}`")
        embed.add_field(name="<:emoji_6:1251444163225063534> EXP:", value=f"`EXP {clan[6]}`")
        embed.add_field(name="<:emoji_7:1251444186666766397> Description:", value=f"`{clan[4]}`")
        embed.add_field(name="🍀 Honor Points:", value=f"`{clan[7]} Honor Point`")
        
        embed.add_field(name="⛩️ Members:", value=f"`{', '.join(member_names)}`")
        embed.set_thumbnail(url=clan[3])
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed, view=view)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='delete_clan', description='Deleting clan (Only processed by Leader)', force_global=bool)
    async def delete_clan(self, ctx: Interaction):

        send = ctx.send
        author = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan:
            await  send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return

        cursor.execute('DELETE FROM clan WHERE leader_id = ?', ( author.id,))
        db.commit()

        embed = Embed(title="🏴 Clan Deleted!",
                      description=f"**Your clan** `{clan[2]}` **has been successfully deleted. You can join another clan now.**")
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed)

        cursor.close()
        db.close()

    @nextcord.slash_command(name='kick_memberclan', description='Kicking bad member clan', force_global=bool)
    async def kick_memberclan(self,  ctx: Interaction, member: nextcord.Member):

        send = ctx.send
        author = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
 
    # Periksa apakah pengguna adalah leader dari clan
        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan:
            await  send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return

    # Periksa apakah member adalah bagian dari clan
        clan_members = cursor.execute("SELECT member_ids FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan_members or str(member.id) not in clan_members[0].split(','):
            await  send(f"**{member.mention} IS NOT A MEMBER OF YOUR CLAN!**")
            return
        
        if member.id ==  author.id:
           await  send("**YOU CANNOT KICK YOURSELF OR KICK LEADER!!**")
           return

    # Keluarkan member dari clan
        updated_members = ','.join([m_id for m_id in clan_members[0].split(',') if m_id != str(member.id)])
        cursor.execute("UPDATE clan SET member_ids = ? WHERE leader_id = ?", (updated_members,  author.id))
        db.commit()

        embed = nextcord.Embed(title="🏴 Member Kicked!",
                           description=f"**{member.mention} has been successfully kicked from the clan** `{clan[2]}`.")
        embed.timestamp = datetime.datetime.now()

        await  send(embed=embed)

        cursor.close()
        db.close()

    async def is_in_clan(self, user_id):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        clan = cursor.execute('SELECT * FROM clan WHERE member_ids LIKE ?', (f'%{user_id}%',)).fetchone()
        db.close()
        return bool(clan)
    
    @nextcord.slash_command(name='edit_nameclan', description='Edit clan name', force_global=bool)
    async def edit_nameclan(self,  ctx: Interaction, *, new_name: str = None): 

        send = ctx.send
        author = ctx.user

        if new_name is None:
            await  send("**TYPE THE NEW NAME OF YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan:
            await  send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()
        
        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        cursor.execute("UPDATE clan SET clan_name = ? WHERE leader_id = ?", (new_name,  author.id,))
        db.commit()

        await  send(f"**YOU ALREADY SET NEW CLAN NAME INTO ==>** `{new_name}` ⛩️")

        cursor.close()
        db.close

    @nextcord.slash_command(name='edit_imageclan', description='Edit clan image', force_global=bool)
    async def edit_imageclan(self,  ctx: Interaction, new_image: str = None):

        send = ctx.send
        author = ctx.user

        if new_image is None:
            await  send("**GIVE THE NEW URL IMAGE YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan:
            await  send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        cursor.execute("UPDATE clan SET image = ? WHERE leader_id = ?", (new_image,  author.id,))
        db.commit()

        await  send(f"**YOU ALREADY SET NEW IMAGE, CHECK IT IN HALL_CLAN OR SEARCH_CLAN 🏮**")

        cursor.close()
        db.close

    @nextcord.slash_command(name='edit_description', description='Edit clan description', force_global=bool)
    async def edit_description(self,  ctx: Interaction, *, new_desc: str = None):

        send = ctx.send
        author = ctx.user

        if new_desc is None:
            await  send("**TYPE THE NEW DESCRIPTION OF YOUR CLAN!**")
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        clan = cursor.execute("SELECT * FROM clan WHERE leader_id = ?", ( author.id,)).fetchone()
        if not clan:
            await  send("**YOU ARE NOT THE LEADER OF ANY CLAN!**")
            return
        
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return
        
        cursor.execute("UPDATE clan SET description = ? WHERE leader_id = ?", (new_desc,  author.id,))
        db.commit()

        await  send(f"**YOU ALREADY SET NEW CLAN DESCRIPTION INTO ==>** `{new_desc}` 🎲")

        cursor.close()
        db.close

    @nextcord.slash_command(name='buy_itemclan', description='Buy some legendary item in Trading Post clan', force_global=bool)
    async def buy_itemclan(self,  ctx: Interaction, item: str = None):

        send = ctx.send
        author = ctx.user

        if item is None:
            await  send("**Type the name of the item that you want to buy!**")
            return
        
        print(f"{item}, tipe:{type(item)}")

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        listItem = ['naginata', 'gozen', 'foxring']

        if item and item not in listItem:
            await  send("**Specify the item name! The options are only <:naginata:1253647561143619696> naginata, <:gozen:1253647592772866100> gozen, and <:foxring:1253647911057887383> foxring**")
            return

        clan = cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ author.id}%',)).fetchone()
        valuable = cursor.execute("SELECT * FROM jewelry2 WHERE user_id = ?", ( author.id,)).fetchone()
        legendItem = cursor.execute("SELECT * FROM equiplegendary").fetchone()
        itemList = cursor.execute("SELECT * FROM equipment WHERE user_id = ?", ( author.id,)).fetchone()
        checkPath = cursor.execute(f"SELECT path FROM data WHERE user_id = { author.id}").fetchone()

        if not checkPath:
            await  send("`You aren't choosing your own path, choose it first in` **start** `command!`")
            cursor.close()
            db.close()
            return

        path = checkPath[0]

        if path == "Ronin":
            await  send("`You are not Shogun, you can't access clan feature command!`")
            cursor.close()
            db.close()
            return

        if not clan:
            await  send("**You are not in any alliance!**")
            return
    # Check if trading post feature is unlocked
        if clan[10] < 1:
            await  send("**Your clan's Trading post feature has not been unlocked! Unlock it first to use it.**")
            return

        if item == listItem[0]:
            try:
                if valuable[1] < 6500:
                    await  send("**You don't have enough <:jade:1249302977450344481> Jade to buy it**")
                    return
                if legendItem[0] <= 0:
                    await  send("**The items are already out of stock ⚠️**")
                    return
                if itemList[17] == 1:
                    await  send("**This is an OP Equipment, you can only have 1! 💀**")
                    return
                cursor.execute("UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (valuable[1] - 6500,  author.id,))
                cursor.execute("UPDATE equipment SET slot17 = ? WHERE user_id = ?", (itemList[17] + 1,  author.id,))
                cursor.execute("UPDATE equiplegendary SET naginata = ?", (legendItem[0] - 1,))
                await  send("**Successfully bought <:naginata:1253647561143619696> Naginata Blade!**")
            except Exception as e:
                print(f"There is an error: {e}")

        elif item == listItem[1]:
            if valuable[2] < 635000:
                await  send("**You don't have enough <a:coin2:1249302963042648094> Coin to buy it**")
                return
            if legendItem[1] <= 0:
                await  send("**The items are already out of stock ⚠️**")
                return
            if itemList[18] == 1:
                await  send("**This is an OP Equipment, you can only have 1! 💀**")
                return
            cursor.execute("UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (valuable[2] - 635000,  author.id,))
            cursor.execute("UPDATE equipment SET slot18 = ? WHERE user_id = ?", (itemList[18] + 1,  author.id,))
            cursor.execute("UPDATE equiplegendary SET gozen = ?", (legendItem[1] - 1,))
            await  send("**Successfully bought <:gozen:1253647592772866100> Gozen's Bow!**")
            print(f"User { author.id} bought Gozen's Bow")

        elif item == listItem[2]:
            if valuable[1] < 4750:
                await  send("**You don't have enough <:jade:1249302977450344481> Jade to buy it**")
                return
            if legendItem[2] <= 0:
                await  send("**The items are already out of stock ⚠️**")
                return
            if itemList[19] == 1:
                await  send("**This is an OP Equipment, you can only have 1! 💀**")
                return
            cursor.execute("UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (valuable[1] - 4750,  author.id,))
            cursor.execute("UPDATE equipment SET slot19 = ? WHERE user_id = ?", (itemList[19] + 1,  author.id,))
            cursor.execute("UPDATE equiplegendary SET foxring = ?", (legendItem[2] - 1,))
            await  send("**Successfully bought <:foxring:1253647911057887383> Blood Foxring!**")
            print(f"User { author.id} bought Blood Foxring")

        db.commit()
        cursor.close()

class ButtonClan(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    def disable_shop_button(self):
        for child in self.children:
            if isinstance(child, nextcord.ui.Button) and child.label == "Trading Post":
                child.disabled = bool
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
        return bool

    @nextcord.ui.button(label="Donation", style=nextcord.ButtonStyle.green, emoji="<:coin3:1250433911885004811>")
    async def on_button_callback(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):

        user = ctx.user
        response = ctx.response

        if  user.id != self.user_id:
            await  response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return

        embed = nextcord.Embed(title="Donation Options", description="Choose your donation option:", color=nextcord.Color.random())
        embed.add_field(name="<:coin3:1250433911885004811> 500 Coins", value="**Donate 500 <:coin3:1250433911885004811> coins to get 20 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.add_field(name="<:coin3:1250433911885004811> 1000 Coins", value="**Donate 1000 <:coin3:1250433911885004811> coins to get 40 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.add_field(name="<:jade:1249302977450344481> 100 Jade", value="**Donate 100 <:jade:1249302977450344481> Jade to get 80 <:emoji_8:1251444211056771092> exp clan**", inline=False)
        embed.set_footer(text="LATEST INFORMATION BY TAKEDA GOVERNMENT")
        embed.timestamp = datetime.datetime.now()

        view = DonateClan( user.id)
        await  response.send_message(embed=embed, view=view, ephemeral=True)

    @nextcord.ui.button(label="Clan Boss", style=nextcord.ButtonStyle.red, emoji="<:emoji_5:1251444143884992604>")
    async def global_boss_button_callback(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):

        user = ctx.user
        response = ctx.response

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await  response.send_message("**YOU ARE NOT IN ANY CLAN!**", ephemeral=True)
            return
        
        await  response.send_message("**🏮 STILL IN DEVELOPMENT!, STAY TUNE! ⚔️**")

    @nextcord.ui.button(label="Facillity", style=nextcord.ButtonStyle.blurple, emoji="⛩️")
    async def facility_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.author
        response = ctx.response

        if  user.id != self.user_id:
            await  response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND!**", ephemeral=True)

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

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
        clans = cursor.fetchone()

        if not clans:
            await  response.send_message("LOL")
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
        await  response.send_message(embed=embed, view=view, ephemeral=True)

        db.commit()
        db.close()

    @nextcord.ui.button(label="Trading Post", style=nextcord.ButtonStyle.gray, emoji="<:trading:1252197613571280916>")
    async def trading_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        response = ctx.response

        if  user.id != self.user_id:
            await  response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        legendWeapon = cursor.execute("SELECT * FROM equiplegendary").fetchone()

        cursor.execute("SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
        clan = cursor.fetchone()

        if not clan:
            await  response.send_message("**YOU DONT IN ANY ALLIANCE!**", ephemeral=True)
            return
        
        trade_post = clan[10]

        if trade_post < 1:
            await  response.send_message("**YOUR CLAN TRADING SHOP FEATURE HAS NOT BEEN UNLOCK!, UNLOCK IT FIRST AND YOU CAN USE IT!**", ephemeral=True)
            return

        embed = Embed(title="WELCOME TO TRADING POST CLAN! ⚖️",
                      description=f"**🔰 Welcome to trading post clan, 🍀 in this place you can buy any stuff like valuable stuff, 🌿 legendary stuff or jade or coin. 🏮You can just buy it with ur jade or coin or trade with you equipment! 🎲**",
                      colour=Color.random())
        embed.add_field(name="<:naginata:1253647561143619696> Naginata Blade", value=f"`6500` **<:TagamataJade:1255191134376951878> Jade (SLOT ITEM {legendWeapon[0]}/1)**", inline=False)
        embed.add_field(name="<:gozen:1253647592772866100> Gozen's Bow", value=f"`635000` **<:coin:1255419339038003271> Coin (SLOT ITEM {legendWeapon[1]}/1)**", inline=False)
        embed.add_field(name="<:foxring:1253647911057887383> Blood Fox Ring", value=f"`4750` **<:TagamataJade:1255191134376951878> Jade (SLOT ITEM {legendWeapon[2]}/1)**")
        embed.set_footer(text="FOR NOW YOU CAN'T BUY IT BUT IN THE NEXT UPDATE YOU CAN BUY IT!!!")
        embed.timestamp = datetime.datetime.now()
        await  response.send_message(embed=embed, ephemeral=True)
        
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

    @nextcord.ui.button(label="Donate 500 Coin", style=nextcord.ButtonStyle.green, emoji="<:coin:1255419339038003271>")
    async def donate2_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        response = ctx.response

        try:
            if  user.id != self.user_id:
                await  response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await  response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", ( user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await  response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if coin < 500:
                    await  ctx.send("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", ( user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await  response.send_message("**⚖️ You have reached the max donation count for today! Please wait until reset in 00.00 UTC!🎲**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 20, f'%{ user.id}%',))
                cursor.execute("UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - 500,  user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", ( user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", ( user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user { user.id}")
                
                await  response.send_message(f"**🍀YOU ALREADY DONATE A** `500` **<:coin:1255419339038003271> COIN FOR** `20` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

        except Exception as e:
            print(f"ERROR in donate_button_callback: {str(e)}")

    @nextcord.ui.button(label="Donate 1000 Coin", style=nextcord.ButtonStyle.green, emoji="<:coin:1255419339038003271>")
    async def donate_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        response = ctx.response

        try:
            if  user.id != self.user_id:
                await  response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await  response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", ( user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await  response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if coin < 1000:
                    await  ctx.send("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", ( user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await  response.send_message("**You have reached the max donation count for today! Please wait until reset in 00.00 UTC!**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 40, f'%{ user.id}%',))
                cursor.execute("UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - 1000,  user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", ( user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", ( user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user { user.id}")
                
                await  response.send_message(f"**🍀YOU ALREADY DONATE A** `1000` **<:coin:1255419339038003271> COIN FOR** `40` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

        except Exception as e:
            print(f"ERROR in donate_button_callback: {str(e)}")

    @nextcord.ui.button(label="Donate 100 Jade", style=nextcord.ButtonStyle.green, emoji="<:TagamataJade:1255191134376951878>")
    async def donate3_button_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        response = ctx.response

        try:
            if  user.id != self.user_id:
                await  response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
                return

            with sqlite3.connect("main.sqlite") as db:
                cursor = db.cursor()
                
                # Fetch clan data
                cursor.execute("SELECT exp, honor FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
                clan = cursor.fetchone()
                if not clan:
                    await  response.send_message("**YOU ARE NOT IN THE CLAN!**")
                    return

                exp_gain = clan[0]
                honor = clan[1]
                honor_amount = random.randint(1, 5)

                # Fetch user data
                cursor.execute("SELECT jade, coin FROM jewelry2 WHERE user_id = ?", ( user.id,))
                jewel = cursor.fetchone()
                if not jewel:
                    await  response.send_message("LOL")
                    return

                jade = jewel[0]
                coin = jewel[1]

                if jade < 100:
                    await  ctx.send("**YOU DON'T HAVE ENOUGH COINS TO DONATE!**")
                    return

                # Check donation count
                cursor.execute("SELECT donation_count FROM donations WHERE user_id = ?", ( user.id,))
                result = cursor.fetchone()
                if result and result[0] >= 3:
                    await  response.send_message("**You have reached the max donation count for today! Please wait until reset in 00.00 UTC!**", ephemeral=True)
                    return

                # Update data
                cursor.execute("UPDATE clan SET exp = ? WHERE member_ids LIKE ?", (exp_gain + 80, f'%{ user.id}%',))
                cursor.execute("UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - 100,  user.id))

                if result:
                    cursor.execute("UPDATE donations SET donation_count = donation_count + 1 WHERE user_id = ?", ( user.id,))
                else:
                    cursor.execute("INSERT INTO donations (user_id, donation_count) VALUES (?, 1)", ( user.id,))

                cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{ user.id}%',))
                
                db.commit()
                print(f"DEBUG: Updated honor to {honor + honor_amount} for user { user.id}")
                
                await  response.send_message(f"**🍀YOU ALREADY DONATE A** `100` **<:TagamataJade:1255191134376951878> JADE FOR** `80` **<:emoji_6:1251444163225063534> EXP CLAN WITH** `{honor_amount}` **HONOR POINT EXTRA!**")

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
        select.disabled=bool
        if select.values[0] == "1":

            user = ctx.user

            response = ctx.response

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await  response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[8]
            honor = clan[7]

            cursor.execute(f"SELECT attack FROM stats WHERE user_id = ?", ( user.id,))
            stats = cursor.fetchone()

            if not stats:
                await  response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
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
                await  response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await  response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await  response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET training_ground = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ user.id}%',))
            cursor.execute("UPDATE stats SET attack = ? WHERE user_id = ?", (stats[0] + amount,  user.id))

            embed = Embed(
                title="⚔️ LAND OF SEKIGAHARA UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Training Combat place in <:doubsword:1252197660899803176> Sekigahara Land, Level ⚔️ Land of Sekigahara became Grade** `{level}` **and the feature is Unlock! Now your attack is increasing 4% by your damage now =>** `{amount}` **Damage.**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Land of Sekigahara successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await  response.send_message(embed=embed, delete_after=20)

            db.commit()
            cursor.close()
            db.close()

        if select.values[0] == "2":

            user = ctx.user

            response = ctx.response

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await  response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[9]
            honor = clan[7]

            cursor.execute(f"SELECT hp FROM stats WHERE user_id = ?", ( user.id,))
            stats = cursor.fetchone()

            if not stats:
                await  response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
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
                await  response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await  response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await  response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET castle = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ user.id}%',))
            cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (stats[0] + amount,  user.id))
            cursor.execute("UPDATE stats SET maxhp = ? WHERE user_id = ?", (stats[0] + amount,  user.id))

            embed = Embed(
                title="🏯 CASTLE HOKOKU UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Training place in <:castle1:1252197628217786368> Castle Hokoku, Level 🏯 Castle Hokoku became Grade** `{level}` **and the feature is Unlock! Now your HP is increasing 4% by your HP now =>** `{amount}` **Health Point.**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Castle Hokoku successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await  response.send_message(embed=embed, delete_after=30)

            db.commit()
            cursor.close()
            db.close()

        if select.values[0] == "3":

            user = ctx.user

            response = ctx.response

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await  response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[11]
            honor = clan[7]

            cursor.execute(f"SELECT attack, hp, maxhp FROM stats WHERE user_id = ?", ( user.id,))
            stats = cursor.fetchone()

            if not stats:
                await  response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
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
                await  response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            if honor < cost:
                await  response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 5:
                await  response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 5**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET kurama_temple = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ user.id}%',))
            cursor.execute("UPDATE stats SET attack = ? WHERE user_id = ?", (stats[0] + amount,  user.id))
            cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (stats[1] + amount1,  user.id))
            cursor.execute("UPDATE stats SET maxhp = ? WHERE user_id = ?", (stats[2] + amount1,  user.id))

            embed = Embed(
                title="⛩️ TEMPLE KURAMA DERA UPGRADE SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Meditation place in <:temple1:1252197648727801896> Temple Kurama Dera, Level ⛩️ Temple Kurama Dera became Grade** `{level}` **and the feature is Unlock! Now your HP and Attack is increasing 4% by your HP and Attack now =>** `{amount1}` **Health Point,** `{amount}` **Damage**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Temple Kurama Dera successfully upgraded!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await  response.send_message(embed=embed, delete_after=30)

            db.commit()
            cursor.close()
            db.close()
        
        if select.values[0] == "4":

            user = ctx.user

            response = ctx.response

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM clan WHERE member_ids LIKE ?", (f'%{ user.id}%',))
            clan = cursor.fetchone()

            if not clan:
                await  response.send_message("**YOU NOT IN ANY ALIANCE**", ephemeral=True)
                return

            combat = clan[10]
            honor = clan[7]

            cursor.execute(f"SELECT attack, hp, maxhp FROM stats WHERE user_id = ?", ( user.id,))
            stats = cursor.fetchone()

            if not stats:
                await  response.send_message("**YOU DONT HAVE A STATS!**", ephemeral=True)
                return
            
            if combat != 0:
                await  response.send_message("Invalid combat level.", ephemeral=True)
                print(f"Invalid combat level: {combat}")
                return

            cost = 50
            lvl = 1

            if honor < cost:
                await  response.send_message("**YOU DON'T HAVE ENOUGH HONOR POINTS TO UPGRADE THE FACILITY!**", ephemeral=True)
                return

            if combat == 1:
                await  response.send_message("**YOU CAN'T UPGRADE THIS FACILITY MORE THAN GRADE 1**", ephemeral=True)
                return

            level = combat + 1
            
            cursor.execute("UPDATE clan SET trade_post = ? WHERE member_ids LIKE ?", (combat + lvl, f'%{ user.id}%',))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor - cost, f'%{ user.id}%',))

            embed = Embed(
                title="⚖️ TRADING POST UNLOCK SUCCESS",
                description=f"**🍀Clan successfully Unlock and Upgrade their Trading Post place <:trading:1252197613571280916> , Level ⚖️ Trading Post became Grade** `{level} (MAX)` **and the feature is Unlock! Now you can buy some Legendary Spear Jade or Legendary Bow or Some cool stuff that limited!**🏮",
                colour=Color.random()
            )
            embed.set_footer(text="Trading Post successfully unlocked!")
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=clan[3])

            await  response.send_message(embed=embed, delete_after=30)

            db.commit()
            cursor.close()
            db.close()