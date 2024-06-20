import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
from event import Event
from inventory import InventoryCommand
from equip import EquipCommand
from talenttree1 import talenttree
from campaign import Campaign
from clan import ClanCommands
import apscheduler
#MAIN CODE

TOKEN_OS = "MTI0ODA2OTQ0NDI3ODgxMjc3Ng.Gz3GvH.quD-EJmGJ9Xf4Saqk5wt_Tyn44Cme5-8_NBOvY"

client = commands.Bot(command_prefix= lambda bot, msg:f"<@{bot.user.id}> ", intents=nextcord.Intents.all())

client.add_cog(Event(client))
client.add_cog(InventoryCommand(client))
client.add_cog(EquipCommand(client))
client.add_cog(talenttree(client))
client.add_cog(Campaign(client))
client.add_cog(ClanCommands(client))
#SQLITE PERM

@client.event
async def on_ready():
    print(f"Logged in {client.user}!")
    await client.change_presence(activity=nextcord.activity.Game(name="Samurai Gambit 🎲"), status=nextcord.Status.idle)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(description=f"**You still in cooldown!, wait until the cooldown time is done!**\n\n`Cooldown time = {round(error.retry_after)} second`")
        await ctx.send(embed=embed)

@client.command()
async def ronin(ctx):
    member = ctx.author

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block FROM stats WHERE user_id = {member.id}")
    stats1 = cursor.fetchone()
    try:
        atk = stats1[0]
        hp = stats1[1]
        posture = stats1[2]
        poison = stats1[3]
        burn = stats1[4]
        lifesteal = stats1[5]
        crit = stats1[6]
        dodge = stats1[7]
        block = stats1[8]
    except:
        atk = 30
        hp = 150
        posture = 100
        poison = 0
        burn = 0
        lifesteal = 0
        crit = 0
        dodge = 0
        block = 15

    cursor.execute(f"SELECT roles, char_name, gender FROM data WHERE user_id = {member.id}")
    stats2 = cursor.fetchone()
    try:
        roles = stats2[0]
        char_name = stats2[1]
        gender = stats2[2]
    except:
        roles = ""
        char_name = "Kenji Iwamura"
        gender = "Man"

    cursor.execute(f"SELECT level, talent, exp FROM level WHERE user_id = {member.id}")
    stats3 = cursor.fetchone()
    try:
        level = stats3[0]
        talent = stats3[1]
        exp = stats3[2]
    except:
        level = 1
        talent = 0
        exp = 0

    embed = Embed(title=f"{member.name} Ronin Stats & Data",
                  colour=nextcord.Color.random())
    
    embed.add_field(name=f"**<:samurai:1249260973337088041> Stats :**", value=f"<:atk:1249261884960538686> Attack : `{atk}` **Damage**\n<:health20:1249262232227938316> Vitality : `{hp}` **Health**\n<:posture:1249263278673235968> Posture : `{posture}`\n<:blocked:1249265783192944732> Block : `{block}` **Blocked Damage**\n\n<:poison1:1249263596089901188> Poison Rate: `{poison}%`\n<:burnkatana:1249263882044837888> Burn Rate : `{burn}%`\n<:lifesteal:1249261927880982528> Lifesteal Rate : `{lifesteal}%`\n<:criticaldmg:1249265313267187753> Critical Rate : `{crit}%`\n<:dodge:1249265279578542131> Dodge Rate : `{dodge}%`", inline=True)
    embed.add_field(name=f"**<:samurai:1249260973337088041> Level :**", value=f"<:soulspirit:1249295825528422401> Level : `{level}`\n<a:exp2:1249296823655338046> EXP Point : `{exp}`\n<a:exp:1249296269721993258> Talent Point : `{talent}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name=f"**<:samurai:1249260973337088041> Character :**", value=f"<:roles:1249284936142422088> Roles : `{roles}`\n<:Kenshin:1249284889132531793> Character Name : `{char_name}`\n🍃 Gender : `{gender}`\n", inline=True)
    embed.set_footer(text="THE STATS CAN GROW UP OR GROW DOWN BECAUSE SOME ACTION")
    embed.timestamp = datetime.datetime.now()

    await ctx.message.reply(embed=embed, mention_author=False)

    db.commit()
    cursor.close()
    db.close()

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):

    amount = random.randint(50, 500)
    amount2 = random.randint(5, 20)

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM jewelry2 WHERE user_id = {ctx.author.id}")
    jewel = cursor.fetchone()
    try:
        jade = jewel[1]
        coin = jewel[2]
    except:
        await ctx.send("SORRY!")

    cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade + amount2, ctx.author.id))
    cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin + amount, ctx.author.id))
    
    embed = Embed(title=f"DAILY EARNINGS", description=f"<@{ctx.author.id}>**, you already use a 🍃 daily earnings to get free coin and jade!. You get  <a:coin2:1249302963042648094> `{amount}x` Ryo Coin and <:jade:1249302977450344481> `{amount2}x` Tagamata Jade!, you can use 🌿 daily earning again in 24H from now.**",
                  colour= nextcord.Color.random())
    embed.set_footer(text="YOU CAN USE DAILY EARNING AGAIN IN 24H FROM NOW")
    embed.timestamp = datetime.datetime.now()

    await ctx.message.reply(embed=embed, mention_author=False)

    db.commit()
    cursor.close()
    db.close()

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily_box(ctx):

    List = [None, "<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind", "<:Kalung1:1249538107389509762>  Jewel Necklace", "<:Cincin2:1249538232161538078>  Fire Ring",
                "<:Cincin3:1249538267364462703> Golden Tiger Ring", "<:Cincin1:1249538201862017104>  Velvet Ring", "<:Kalung3:1249538167573446667>  Blue Jewel Necklace", "<:Kalung2:1249538142114152459>  Hell's Necklace", "<:Kipas2:1249539571905986692>  Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383>  Blood Pattern Folding Fan", "<:Hakama:1249348241536057425> Hakama Samurai", "<:Shogun:1249348180236177478> Shogun Armor", "<:Shinobi:1249348208014921840> Shinobi Armor",
                "<:Pengembara:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan"]
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
        
    cursor.execute(f"SELECT * FROM equipment WHERE user_id = {ctx.author.id}")
    list = cursor.fetchone()

    list_box = random.choice(List)

    if list_box == List[1]:
        cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (list[1] + 1, ctx.author.id))
    if list_box == List[2]:
        cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (list[2] + 1, ctx.author.id))
    if list_box == List[3]:
        cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (list[3] + 1, ctx.author.id))
    if list_box == List[4]:
        cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (list[4] + 1, ctx.author.id))
    if list_box == List[5]:
        cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (list[5] + 1, ctx.author.id))
    if list_box == List[6]:
        cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (list[6] + 1, ctx.author.id))
    if list_box == List[7]:
        cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (list[7] + 1, ctx.author.id))
    if list_box == List[8]:
        cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (list[8] + 1, ctx.author.id))
    if list_box == List[9]:
        cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (list[9] + 1, ctx.author.id))
    if list_box == List[10]:
        cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (list[10] + 1, ctx.author.id))
    if list_box == List[11]:
        cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (list[11] + 1, ctx.author.id))
    if list_box == List[12]:
        cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (list[12] + 1, ctx.author.id))
    if list_box == List[13]:
        cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (list[13] + 1, ctx.author.id))
    if list_box == List[14]:
        cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (list[14] + 1, ctx.author.id))
    if list_box == List[15]:
        cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (list[15] + 1, ctx.author.id))
    if list_box == List[16]:
        cursor.execute(f"UPDATE equipment SET slot16 = ? WHERE user_id = ?", (list[16] + 1, ctx.author.id))
    if list_box == List[0]:
        await ctx.send("*SO DUMB, HAHAHA YOU GET NOTHING!*")
        return
        
    embed = Embed(title="DAILY EQUIPMENT BOX",
                  description=f"**You get {list_box}!. 🍃 New item is added to your inventory, check it and if you want to use it, use @Ronin equip name_equip! 🎲**",
                  colour=nextcord.Color.random())
    embed.set_footer(text="YOU CAN USE THIS COMMAND AGAIN IN 24H FROM NOW!")
    embed.timestamp = datetime.datetime.now()

    await ctx.message.reply(embed=embed, mention_author=False)

    db.commit()
    cursor.close()
    db.close()

@client.command()
async def equip(ctx, equip: str):

    EQUIPLIST = ["Shura", "Mensen", "YokaiWhirlwind", "JewelNeck", "FireRing",
            "GoldenTiger", "Velvet", "BlueJewel", "HellNeck", "ApricotFlower",
            "BloodPattern", "Hakama", "Shogun", "Shinobi",
            "Traveler", "BlackWalet"]
    
    EQUIPLIST1 = ["<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind", "<:Kalung1:1249538107389509762>  Jewel Necklace", "<:Cincin2:1249538232161538078>  Fire Ring",
                "<:Cincin3:1249538267364462703> Golden Tiger Ring", "<:Cincin1:1249538201862017104>  Velvet Ring", "<:Kalung3:1249538167573446667>  Blue Jewel Necklace", "<:Kalung2:1249538142114152459>  Hell's Necklace", "<:Kipas2:1249539571905986692>  Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383>  Blood Pattern Folding Fan", "<:Hakama:1249348241536057425> Hakama Samurai", "<:Shogun:1249348180236177478> Shogun Armor", "<:Shinobi:1249348208014921840> Shinobi Armor",
                "<:Pengembara:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan"]
    
    EQUIPSWORD = ["<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind"]
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16 FROM equipment WHERE user_id = {ctx.author.id}")
    equip_list = cursor.fetchone()
    try:
        slot1 = equip_list[0]
        slot2 = equip_list[1]
        slot3 = equip_list[2]
        slot4 = equip_list[3]
        slot5 = equip_list[4]
        slot6 = equip_list[5]
        slot7 = equip_list[6]
        slot8 = equip_list[7]
        slot9 = equip_list[8]
        slot10 = equip_list[9]
        slot11 = equip_list[10]
        slot12 = equip_list[11]
        slot13 = equip_list[12]
        slot14 = equip_list[13]
        slot15 = equip_list[14]
        slot16 = equip_list[15]
    except:
        await ctx.send("SORRY")

    cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp FROM stats WHERE user_id = {ctx.author.id}")
    data = cursor.fetchone()
    try:
        atk = data[0]
        hp = data[1]
        pos = data[2]
        poison = data[3]
        burn = data[4]
        lifesteal = data[5]
        crit = data[6]
        dodge = data[7]
        block = data[8]
        maxhp = data[9]
    except:
        await ctx.send("SORRY")

    cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = {ctx.author.id}")
    equipdata = cursor.fetchone()
    try:
        katana = equipdata[0]
        armor = equipdata[1]
        necklace = equipdata[2]
        ring1 = equipdata[3]
        ring2 = equipdata[4]
        fan = equipdata[5]
    except:
        await ctx.send("SORRY")
 
    else:
        current_item = EQUIPLIST1
        if equip == EQUIPLIST[0]:
            if katana and katana in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot1 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (slot1 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:Shura:1249342778039734354> Shura**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 35, ctx.author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + 3, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Shura:1249342778039734354> `{EQUIPLIST[0]}`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 35, AND CRIT RATE INCREASE 3%")
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[1]:
            if katana and katana in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot2 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (slot2 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:Crested:1249342749715595417> Mensen Sword**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 65, ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 3, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Crested:1249342749715595417> `Mensen Sword`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 65, AND BLOCKED DAMAGE INCREASE 3")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[2]:
            if katana and katana in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot3 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (slot3 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:Whirlwind:1249342716366684212> Yokai Whirlwind**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 7, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Whirlwind:1249342716366684212> `Yokai Whirlwind Sword`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 25, AND DODGE RATE INCREASE 7%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[3]:
            if necklace and necklace in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot4 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (slot4 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:Kalung1:1249538107389509762> Jewel Necklace**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 20, ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 2, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Kalung1:1249538107389509762> `Jewel Necklace`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR POSTURE INCREASE 20, AND BLOCKED DAMAGE INCREASE 2")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[4]:
            if ring1 and ring1 in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring1 and ring1 not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot5 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (slot5 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("**<:Cincin2:1249538232161538078> Fire Ring**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 50, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 50, ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 15, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Cincin2:1249538232161538078> `Fire Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 50, AND ATTACK INCREASE 15")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[5]:
            if ring2 and ring2 in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring2 and ring2 not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot6 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (slot6 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("**<:Cincin3:1249538267364462703> Golden Tiger Ring**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 4, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 3, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Cincin3:1249538267364462703> `Golden Tiger Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR BLOCK INCREASE 4, AND DODGE RATE INCREASE 3%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[6]:
            if ring1 and ring1 in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring1 and ring1 not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot7 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (slot7 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("**<:Cincin1:1249538201862017104> Velvet Ring**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 40, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 40, ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 20, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Cincin1:1249538201862017104> `Velvet Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 40, AND POSTURE INCREASE 20")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[7]:
            if necklace and necklace in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot8 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (slot8 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:Kalung3:1249538167573446667> Blue Jewel Necklace**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 15, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Kalung3:1249538167573446667> `Blue Jewel Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 25, AND POSTURE INCREASE 15")
                embed.timestamp = datetime.datetime.now()
            await ctx.message.reply(embed=embed, mention_author=False)
            pass
        elif equip == EQUIPLIST[8]:
            if necklace and necklace in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot9 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (slot9 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:Kalung2:1249538142114152459> Hell's Necklace**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 35, ctx.author.id))
                cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn + 5, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Kalung2:1249538142114152459> `Hell's Necklace`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 25, AND BURN RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[9]:
            if fan and fan in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot10 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (slot10 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:Kipas2:1249539571905986692> Apricot Flower Floding Fan**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 20, ctx.author.id))
                cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison + 5, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Kipas2:1249539571905986692> `Apricot Flower Floding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 20, AND POISON RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[10]:
            if fan and fan in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot11 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (slot11 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:Kipas1:1249539515291533383> Blood Pattern Folding Fan**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + 5, ctx.author.id))
                cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + 5, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Kipas1:1249539515291533383> `Blood Pattern Floding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR CRIT RATE INCREASE 5%, AND LIFESTEAL RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[11]:
            if armor and armor in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot12 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (slot12 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:Hakama:1249348241536057425> Hakama Samurai**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 350, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 350, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Hakama", ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Hakama:1249348241536057425> `{EQUIPLIST[11]} Samurai Armor`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 25, AND HP INCREASE 350")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[12]:
            if armor and armor in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot13 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (slot13 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:Shogun:1249348180236177478> Samurai Armor**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 300, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Shogun", ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 300, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Shogun:1249348180236177478> `{EQUIPLIST[12]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 300")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[13]:
            if armor and armor in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot14 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (slot14 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:Shinobi:1249348208014921840> Shinobi Armor**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 200, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 200, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 10, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Shinobi", ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:Shinobi:1249348208014921840> `{EQUIPLIST[13]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 200, AND DODGE RATE INCREASE 10%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[14]:
            if armor and armor in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot15 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
               cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (slot15 - 1, ctx.author.id))
               cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:Pengembara:1249348267645468702> Traveler Armor**", ctx.author.id))
               cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 175, ctx.author.id))
               cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 175, ctx.author.id))
               cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 10, ctx.author.id))
               cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Traveler", ctx.author.id))
               embed = Embed(description=f"**You have equipped **<:Pengembara:1249348267645468702> `{EQUIPLIST[14]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
               embed.set_footer(text=f"YOUR HP INCREASE 175, AND BLOCKED DAMAGE INCREASE 10")
               embed.timestamp = datetime.datetime.now()
               await ctx.message.reply(embed=embed, mention_author=False)
               pass
        elif equip == EQUIPLIST[15]:
            if fan and fan in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await ctx.reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot16 == 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot16 = ? WHERE user_id = ?", (slot16 - 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:waletfan:1250032616690683955> Black Walet Folding Fan**", ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 5, ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 15, ctx.author.id))
                embed = Embed(description=f"**You have equipped **<:waletfan:1250032616690683955> `Black Walet Folding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR DODGE RATE INCREASE 5%, AND ATTACK RATE INCREASE 25")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        else:
            await ctx.send("**Item Not Found**")

        db.commit()
        cursor.close()
        db.close()

@client.command()
async def unequip(ctx, equip: str):

    EQUIPLIST = ["Shura", "Mensen", "YokaiWhirlwind", "JewelNeck", "FireRing",
            "GoldenTiger", "Velvet", "BlueJewel", "HellNeck", "ApricotFlower",
            "BloodPattern", "Hakama", "Shogun", "Shinobi",
            "Traveler", "BlackWalet"]
    
    EQUIPLIST1 = ["**<:Shura:1249342778039734354> Shura**", "**<:Crested:1249342749715595417> Mensen Sword**", "**<:Whirlwind:1249342716366684212> Yokai Whirlwind**", "**<:Kalung1:1249538107389509762> Jewel Necklace**", "**<:Cincin2:1249538232161538078> Fire Ring**",
                "**<:Cincin3:1249538267364462703> Golden Tiger Ring**", "**<:Cincin1:1249538201862017104> Velvet Ring**", "**<:Kalung3:1249538167573446667> Blue Jewel Necklace**", "**<:Kalung2:1249538142114152459> Hell's Necklace**", "**<:Kipas2:1249539571905986692> Apricot Flower Floding Fan**",
                "**<:Kipas1:1249539515291533383> Blood Pattern Folding Fan**", "**<:Hakama:1249348241536057425> Hakama Samurai**", "**<:Shogun:1249348180236177478> Shogun Armor**", "**<:Shinobi:1249348208014921840> Shinobi Armor**",
                "**<:Pengembara:1249348267645468702> Traveler Armor**", "**<:waletfan:1250032616690683955> Black Walet Folding Fan**"]
    
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16 FROM equipment WHERE user_id = {ctx.author.id}")
    equip_list = cursor.fetchone()
    try:
        slot1 = equip_list[0]
        slot2 = equip_list[1]
        slot3 = equip_list[2]
        slot4 = equip_list[3]
        slot5 = equip_list[4]
        slot6 = equip_list[5]
        slot7 = equip_list[6]
        slot8 = equip_list[7]
        slot9 = equip_list[8]
        slot10 = equip_list[9]
        slot11 = equip_list[10]
        slot12 = equip_list[11]
        slot13 = equip_list[12]
        slot14 = equip_list[13]
        slot15 = equip_list[14]
        slot16 = equip_list[15]
    except:
        await ctx.send("SORRY")

    cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp FROM stats WHERE user_id = {ctx.author.id}")
    data = cursor.fetchone()
    try:
        atk = data[0]
        hp = data[1]
        pos = data[2]
        poison = data[3]
        burn = data[4]
        lifesteal = data[5]
        crit = data[6]
        dodge = data[7]
        block = data[8]
        maxhp = data[9]
    except:
        await ctx.send("SORRY")

    cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = {ctx.author.id}")
    equipdata = cursor.fetchone()
    try:
        katana = equipdata[0]
        armor = equipdata[1]
        necklace = equipdata[2]
        ring1 = equipdata[3]
        ring2 = equipdata[4]
        fan = equipdata[5]
    except:
        await ctx.send("SORRY")
 
    else:
        current_item = EQUIPLIST1
        if equip == EQUIPLIST[0]:
            if katana == "":
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[1]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana != current_item[0]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot1 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (slot1 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 35, ctx.author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit - 3, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Shura:1249342778039734354> `{EQUIPLIST[0]}`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 35, AND CRIT RATE DECREASE 3%")
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[1]:
            if katana == "":
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[0]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana != current_item[1]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot2 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (slot2 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 65, ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 3, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Crested:1249342749715595417> `Mensen Sword`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 65, AND BLOCKED DAMAGE DECREASE 3")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[2]:
            if katana == "":
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana  == current_item[0]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[1]:
                await ctx.reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana != current_item[2]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot3 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (slot3 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 7, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Whirlwind:1249342716366684212> `Yokai Whirlwind Sword`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 25, AND DODGE RATE DECREASE 7%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[3]:
            if necklace == "":
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[7]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[8]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[3]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot4 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (slot4 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 20, ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 2, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Kalung1:1249538107389509762> `Jewel Necklace`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR POSTURE DECEREASE 20, AND BLOCKED DAMAGE DECREASE 2")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[4]:
            if ring1 == "":
                await ctx.reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring1 == current_item[6]:
                await ctx.reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT**")
            elif ring1 != current_item[4]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot5 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (slot5 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 50, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 50, ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 15, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin2:1249538232161538078> `Fire Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 50, AND ATTACK DECREASE 15")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[5]:
            if ring2 == "":
                await ctx.reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring2 == current_item[5]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot6 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (slot6 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 4, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 3, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin3:1249538267364462703> `Golden Tiger Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR BLOCK DECREASE 4, AND DODGE RATE DECREASE 3%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[6]:
            if ring1 == "":
                await ctx.reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring1 == current_item[4]:
                await ctx.reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT**")
            elif ring1 != current_item[6]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot7 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (slot7 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 40, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 40, ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 20, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin1:1249538201862017104> `Velvet Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 40, AND POSTURE DECREASE 20")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[7]:
            if necklace == "":
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[3]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[8]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[7]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot8 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (slot8 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 15, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Kalung3:1249538167573446667> `Blue Jewel Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 25, AND POSTURE DECREASE 15")
                embed.timestamp = datetime.datetime.now()
            await ctx.message.reply(embed=embed, mention_author=False)
            pass
        elif equip == EQUIPLIST[8]:
            if necklace == "":
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[3]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[7]:
                await ctx.reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[8]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot9 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (slot9 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 35, ctx.author.id))
                cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn - 5, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Kalung2:1249538142114152459> `Hell's Necklace`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 25, AND BURN RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[9]:
            if fan == "":
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[10]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[15]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[9]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot10 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (slot10 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 20, ctx.author.id))
                cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison - 5, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Kipas2:1249539571905986692> `Apricot Flower Floding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 20, AND POISON RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[10]:
            if fan == "":
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[9]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[15]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[10]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot11 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (slot11 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit - 5, ctx.author.id))
                cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal - 5, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Kipas1:1249539515291533383> `Blood Pattern Floding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR CRIT RATE DECREASE 5%, AND LIFESTEAL RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[11]:
            if armor == "":
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[12]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[11]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot12 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (slot12 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("****", ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 25, ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 350, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 350, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin", ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Hakama:1249348241536057425> `{EQUIPLIST[11]} Samurai Armor`, **Your stats is been reset**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 25, AND HP DECREASE 350")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[12]:
            if armor == "":
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[12]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot13 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (slot13 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 300, ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 300, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin", ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Shogun:1249348180236177478> `{EQUIPLIST[12]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 300")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[13]:
            if armor == "":
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[12]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[13]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot14 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (slot14 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 200, ctx.author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 200, ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 10, ctx.author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin", ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:Shinobi:1249348208014921840> `{EQUIPLIST[13]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 200, AND DODGE RATE DECREASE 10%")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        elif equip == EQUIPLIST[14]:
            if armor == "":
                await ctx.reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[12]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await ctx.reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[14]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot15 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
               cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (slot15 + 1, ctx.author.id))
               cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("", ctx.author.id))
               cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 175, ctx.author.id))
               cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 175, ctx.author.id))
               cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 10, ctx.author.id))
               cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Traveler", ctx.author.id))
               embed = Embed(description=f"**You have unequipped **<:Pengembara:1249348267645468702> `{EQUIPLIST[14]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
               embed.set_footer(text=f"YOUR HP DECREASE 175, AND BLOCKED DAMAGE DECREASE 10")
               embed.timestamp = datetime.datetime.now()
               await ctx.message.reply(embed=embed, mention_author=False)
               pass
        elif equip == EQUIPLIST[15]:
            if fan == "":
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[9]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[10]:
                await ctx.reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[15]:
                await ctx.send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot16 < 0:
                await ctx.reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot16 = ? WHERE user_id = ?", (slot16 + 1, ctx.author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("", ctx.author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 5, ctx.author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 15, ctx.author.id))
                embed = Embed(description=f"**You have unequipped **<:waletfan:1250032616690683955> `Black Walet Folding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR DODGE RATE DECREASE 5%, AND ATTACK RATE DECREASE 25")
                embed.timestamp = datetime.datetime.now()
                await ctx.message.reply(embed=embed, mention_author=False)
                pass
        else:
            await ctx.send("**Item Not Found**")

        db.commit()
        cursor.close()
        db.close()

if __name__ == '__main__':
    client.run(TOKEN_OS)