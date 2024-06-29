import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions, user
from event import Event
from inventory import InventoryCommand
from equip import EquipCommand
from talenttree1 import talenttree
from campaign import Campaign
from clan import ClanCommands
from guide import GuideCommands
import apscheduler
#MAIN CODE

TOKEN_OS = "BOT_TOKEN_LOL"

client = commands.Bot(command_prefix=lambda client, msg:f"<@{client.user.id}> ", help_command=None, default_guild_ids="1250831919936049273")

client.add_cog(Event(client))
client.add_cog(InventoryCommand(client))
client.add_cog(EquipCommand(client))
client.add_cog(talenttree(client))
client.add_cog(Campaign(client))
client.add_cog(ClanCommands(client))
client.add_cog(GuideCommands(client))
#SQLITE PERM

default_guild_ids="1250831919936049273"

@client.event
async def on_ready():
    print(f"Logged in {client.user}!")
    await client.change_presence(activity=nextcord.activity.Game(name="Samurai Gambit 🎲"), status=nextcord.Status.idle)
    await client.sync_all_application_commands()

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

@client.slash_command(name="help", description="Show all of commands", force_global=True)
async def help_command(ctx: Interaction):

    embed = nextcord.Embed(
        title="⛩️ Help Command",
        description="""
        `Prefix : / (Slash Command)`

        **🗒️ START**
        `ronin / daily / daily_box / start_mission / start`

        **📦 INVENTORY**
        `equip <id item> / unequip <id item> / inv / shop`

        **⚙️ EQUIPMENT**
        `craft <id item> / dismantle <id item>`

        **🚀 TALENT**
        `Talent_tree <attack/defense>, up_talent <talent_name>`

        **🪧 CLAN (ONLY SHOGUN PATH)**
        `create_clan <clan_name> <url_image> <clan_description> ==> (ALL REQUIRED) / delete_clan / join_clan <clan_name> / leave_clan / search_clan <name> / edit_imageclan <new_image_url> / edit_nameclan / edit_description / buy_item <item>`

        **🩸 PVP**
        `fight / start_regeneration`

        **🗡️ ATTACK TALENT NAME**

        `Tameshigiri, StormSword, Sharpness, Strike, LifestealBlow, LeechEnhance, SwordEnchant, PoisonSword, SwordAgil, FlowSword, BloodPierce, SwordPosture, Dissension, Resistance, Talisman, LifeOrbs, Phoenix`

        **🛡️ DEFENSE TALENT NAME**

        `Vitality, VitalPos, Dodge, Scud, Flow, Sturdy, Penet, BlockedSoul, YokaiScroll, HeartsSirit, Hawkeye, Concentrate, Acc, StormMove, SteelWill, FireMove, Craziness, Onimusha, Gauge`

        **🔢 ID ITEM (THE NUMBER BELOW)**

        **📌 Id item can be found in the emoji but i will show it now**\n
        `1 = Shura Sword\n2 = Mensen Sword\n3 = Yokai Whirlwind Sword\n4 = Jewel Necklace\n5 = Fire Ring\n6 = Golden Tiger Ring\n7 = Velvet Ring\n8 = Blue Jewel Necklace\n9 = Hell's Necklace\n10 = Apricot Flower Folding Fan\n11 = Blood Pattern Folding Fan\n12 = Hakama\n13 = Samurai\n14 = Shinobi (CAN'T CRAFTED OR DISMANTLE GET IN LIMITED EVENT)\n15 = Traveler\n16 = Wallet Folding Fan\n17 = Naginata Jade (CAN'T BE CRAFTED OR DISMANTLE)\n18 = Gozen's Bow (CAN'T BE CRAFTED OR DISMANTLE)\n19 = Blood Fox Ring (CAN'T BE CRAFTED OR DISMANTLE)`
        """,
        color=0x111111
    )
    embed.set_footer(text="All ronin bot commands")
    
    await ctx.send(embed=embed, ephemeral=True)

@client.slash_command(name="ronin", description="Show your stats data!", force_global=True)
async def ronin(ctx: Interaction):

    member =  ctx.user

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
        atk = stats1[0]
        hp = stats1[1]
        posture = stats1[2]
        poison = stats1[3]
        burn = stats1[4]
        lifesteal = stats1[5]
        crit = stats1[6]
        dodge = stats1[7]
        block = stats1[8]

    cursor.execute(f"SELECT roles, char_name, gender, path FROM data WHERE user_id = {member.id}")
    stats2 = cursor.fetchone()
    try:
        roles = stats2[0]
        char_name = stats2[1]
        gender = stats2[2]
        path = stats2[3]
    except:
        roles = "None"
        char_name = "Kenji Iwamura"
        gender = "Man"
        path = "None"

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
    embed.add_field(name=f"**<:samurai:1249260973337088041> Character :**", value=f"<:roles:1249284936142422088> Roles : `{roles}`\n<:Kenshin:1249284889132531793> Character Name : `{char_name}`\n🍃 Gender : `{gender}`\n🍀 Path : `{path}`", inline=True)
    embed.set_footer(text="THE STATS CAN GROW UP OR GROW DOWN BECAUSE SOME ACTION")
    embed.timestamp = datetime.datetime.now()

    await ctx.response.send_message(embed=embed, ephemeral=True)

    db.commit()
    cursor.close()
    db.close()

@client.slash_command(name='daily', description='Give jade and coins free per day', force_global=True)
async def daily(ctx: Interaction):

    send = ctx.send

    author = ctx.user
    is_allowed, retry_after = check_cooldown(author.id, 'daily', 86400)
    if not is_allowed:
        embed = Embed(description=f"**You are still on cooldown!**\n\n`Cooldown time = {int(retry_after)} seconds`")
        await ctx.send(embed=embed, ephemeral=True)
        return

    amount = random.randint(50, 500)
    amount2 = random.randint(5, 20)

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor() 

    cursor.execute(f"SELECT * FROM jewelry2 WHERE user_id = {author.id}")
    jewel = cursor.fetchone()
    try:
        jade = jewel[1]
        coin = jewel[2]
    except:
        await send("SORRY!")

    cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade + amount2, author.id))
    cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin + amount, author.id))
    
    embed = Embed(title=f"DAILY EARNINGS", description=f"<@{author.id}>**, you already use a 🍃 daily earnings to get free coin and jade!. You get  <a:coin2:1249302963042648094> `{amount}x` Ryo Coin and <:jade:1249302977450344481> `{amount2}x` Tagamata Jade!, you can use 🌿 daily earning again in 24H from now.**",
                  colour= nextcord.Color.random())
    embed.set_footer(text="YOU CAN USE DAILY EARNING AGAIN IN 24H FROM NOW")
    embed.timestamp = datetime.datetime.now()

    await send(embed=embed, ephemeral=True)

    db.commit()
    cursor.close()
    db.close()

@client.slash_command(name='daily_box', description='Give free equipment per day', force_global=True)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily_box(ctx: Interaction):

    send = ctx.send

    author = ctx.user

    is_allowed, retry_after = check_cooldown(author.id, 'daily_box', 86400)
    if not is_allowed:
        embed = Embed(description=f"**You are still on cooldown!**\n\n`Cooldown time = {int(retry_after)} seconds`")
        await ctx.send(embed=embed, ephemeral=True)
        return

    List = [None, "<:1_:1255403773086666782> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:3_:1249342716366684212> Yokai Whirlind", "<:4_:1249538107389509762> Jewel Necklace",
                "<:6_:1249538267364462703> Golden Tiger Ring", "<:7_:1249538201862017104> Velvet Ring", "<:8_:1255404269197201499> Blue Jewel Necklace", "<:Kipas2:1249539571905986692> Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383> Blood Pattern Folding Fan", "<:13:1255403728417193994> Shogun Armor",
                "<:15:1249348267645468702> Traveler Armor"]
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
        
    cursor.execute(f"SELECT * FROM equipment WHERE user_id = {author.id}")
    list = cursor.fetchone()

    list_box = random.choice(List)

    if list_box == List[1]:
        cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (list[1] + 1, author.id))
    if list_box == List[2]:
        cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (list[2] + 1, author.id))
    if list_box == List[3]:
        cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (list[3] + 1, author.id))
    if list_box == List[4]:
        cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (list[4] + 1, author.id))
    if list_box == List[5]:
        cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (list[6] + 1, author.id))
    if list_box == List[6]:
        cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (list[7] + 1, author.id))
    if list_box == List[7]:
        cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (list[8] + 1, author.id))
    if list_box == List[8]:
        cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (list[10] + 1, author.id))
    if list_box == List[9]:
        cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (list[11] + 1, author.id))
    if list_box == List[10]:
        cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (list[13] + 1,  author.id))
    if list_box == List[11]:
        cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (list[15] + 1,  author.id))
    if list_box == List[0]:
        await  send("*SO DUMB, HAHAHA YOU GET NOTHING!*")
        return
        
    embed = Embed(title="DAILY EQUIPMENT BOX",
                  description=f"**You get {list_box}!. 🍃 New item is added to your inventory, check it and if you want to use it, use @Ronin equip id item! (id item in emoji without _ or any symbols.) 🎲**",
                  colour=nextcord.Color.random())
    embed.set_footer(text="YOU CAN USE THIS COMMAND AGAIN IN 24H FROM NOW!")
    embed.timestamp = datetime.datetime.now()

    await  send(embed=embed, ephemeral=True)

    db.commit()
    cursor.close()
    db.close()

@client.slash_command(name='equip', description='Equip your own equipment!', force_global=True)
async def equip(ctx: Interaction, equip: str):

    author = ctx.user
    send = ctx.send
    reply = ctx.send
    message = ctx.send

    EQUIPLIST = ["1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10",
            "11", "12", "13", "14",
            "15", "16", "17", "18", "19"]
    
    EQUIPLIST1 = ["<:1_:1255403773086666782> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:3_:1249342716366684212> Yokai Whirlwind", "<:4_:1249538107389509762> Jewel Necklace", "<:5_:1255403870658625637> Fire Ring",
                "<:6_:1249538267364462703> Golden Tiger Ring", "<:7_:1249538201862017104> Velvet Ring", "<:8_:1255404269197201499> Blue Jewel Necklace", "<:9_:1255404187680903199> Hell's Necklace", "<:10:1249539571905986692> Apricot Flower Floding Fan",
                "<:11:1249539515291533383> Blood Pattern Folding Fan", "<:12:1255403750080778260> Hakama Samurai", "<:13:1255403728417193994> Shogun Armor", "<:14:1255403801700073533> Shinobi Armor",
                "<:15:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan", "<:17:1253647561143619696> Naginata Jade Blade", "<:18:1253647592772866100> Gozen's Bow", "<:19:1253647911057887383> Blood Fox Ring"]
    
    EQUIPSWORD = ["<:Shura:1249342778039734354> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind"]
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16, slot17, slot18, slot19 FROM equipment WHERE user_id = { author.id}")
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
        slot17 = equip_list[16]
        slot18 = equip_list[17]
        slot19 = equip_list[18]
    except Exception as e:
        await  send(f"SORRY {e}")

    cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp FROM stats WHERE user_id = { author.id}")
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
        await  send("SORRY")

    cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = { author.id}")
    equipdata = cursor.fetchone()
    try:
        katana = equipdata[0]
        armor = equipdata[1]
        necklace = equipdata[2]
        ring1 = equipdata[3]
        ring2 = equipdata[4]
        fan = equipdata[5]
    except Exception as e:
        await  send(f"SORRY {e}")
 
    else:
        current_item = EQUIPLIST1
        if equip == EQUIPLIST[0]:
            if katana and katana in current_item:
                await  reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await  reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot1 == 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (slot1 - 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:1_:1255403773086666782> Shura**",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 235,  author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + 7,  author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_41:1255403773086666782> `{EQUIPLIST[0]}`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 235, AND CRIT RATE INCREASE 7%")
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[16]:
            if katana and katana in current_item:
                await  reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await  reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot17 == 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot17 = ? WHERE user_id = ?", (slot17 - 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:17:1253647561143619696> Naginata Jade Blade**",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 500,  author.id))
                embed = Embed(description=f"**You have equipped **<:naginata:1253647561143619696> `Naginata Jade Blade`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 500, NEW SKILL WILL ADDED NEXT UPDATE ==> Dragonwhirl")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[17]:
            if katana and katana in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot18 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot18 = ? WHERE user_id = ?", (slot18 - 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:18:1253647592772866100> Gozen's Bow**",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 500,  author.id))
                embed = Embed(description=f"**You have equipped **<:gozen:1253647592772866100> `Gozen's Bow`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 500, NEW SKILL WILL ADDED NEXT UPDATE ==> Lightning Strike Arrow")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[18]:
            if ring2 and ring2 in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring2 and ring2 not in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot19 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot19 = ? WHERE user_id = ?", (slot19 - 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("**<:19:1253647911057887383> Blood Fox Ring**",  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 600,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 600,  author.id))
                embed = Embed(description=f"**You have equipped **<:foxring:1253647911057887383> `Blood Fox Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 600")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[1]:
            if katana and katana in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot2 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (slot2 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:2_:1249342749715595417> Mensen Sword**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 65, author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 3, author.id))
                embed = Embed(description=f"**You have equipped **<:Crested:1249342749715595417> `Mensen Sword`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 65, AND BLOCKED DAMAGE INCREASE 3")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[2]:
            if katana and katana in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            if katana and katana not in current_item:
                await reply("**YOU ALREADY HAVE A SWORD, UNEQUIP IT FIRST**")
            elif slot3 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (slot3 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("**<:3_:1249342716366684212> Yokai Whirlwind**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 45, author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 7, author.id))
                embed = Embed(description=f"**You have equipped **<:Whirlwind:1249342716366684212> `Yokai Whirlwind Sword`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 25, AND DODGE RATE INCREASE 7%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[3]:
            if necklace and necklace in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot4 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (slot4 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:4_:1249538107389509762> Jewel Necklace**", author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 20, author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 2, author.id))
                embed = Embed(description=f"**You have equipped **<:Kalung1:1249538107389509762> `Jewel Necklace`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR POSTURE INCREASE 20, AND BLOCKED DAMAGE INCREASE 2")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[4]:
            if ring1 and ring1 in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring1 and ring1 not in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot5 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (slot5 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("**<:Cincin2:1249538232161538078> Fire Ring**", author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 250, author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 250, author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 85, author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_43:1255403870658625637> `Fire Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 250, AND ATTACK INCREASE 85")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[5]:
            if ring2 and ring2 in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring2 and ring2 not in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot6 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (slot6 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("**<:6_:1249538267364462703> Golden Tiger Ring**", author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 4, author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 3, author.id))
                embed = Embed(description=f"**You have equipped **<:Cincin3:1249538267364462703> `Golden Tiger Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR BLOCK INCREASE 4, AND DODGE RATE INCREASE 3%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[6]:
            if ring1 and ring1 in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            if ring1 and ring1 not in current_item:
                await reply("**YOU ALREADY HAVE A RING, UNEQUIP IT FIRST**")
            elif slot7 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (slot7 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("**<:7_:1249538201862017104> Velvet Ring**", author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 40, author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 40, author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 20, author.id))
                embed = Embed(description=f"**You have equipped **<:Cincin1:1249538201862017104> `Velvet Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 40, AND POSTURE INCREASE 20")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[7]:
            if necklace and necklace in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot8 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (slot8 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:8_:1255404269197201499> Blue Jewel Necklace**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 175, author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos + 15, author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_45:1255404269197201499> `Blue Jewel Ring`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 175, AND POSTURE INCREASE 15")
                embed.timestamp = datetime.datetime.now()
            await message  (embed=embed)
            pass
        elif equip == EQUIPLIST[8]:
            if necklace and necklace in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            if necklace and necklace not in current_item:
                await reply("**YOU ALREADY HAVE A NECKLACE, UNEQUIP IT FIRST**")
            elif slot9 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (slot9 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("**<:9_:1255404187680903199> Hell's Necklace**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 205, author.id))
                cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn + 5, author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_44:1255404187680903199> `Hell's Necklace`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 205, AND BURN RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[9]:
            if fan and fan in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot10 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (slot10 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:10:1249539571905986692> Apricot Flower Floding Fan**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 20, author.id))
                cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison + 5, author.id))
                embed = Embed(description=f"**You have equipped **<:Kipas2:1249539571905986692> `Apricot Flower Floding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 20, AND POISON RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[10]:
            if fan and fan in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot11 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (slot11 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:11:1249539515291533383> Blood Pattern Folding Fan**", author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + 5, author.id))
                cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + 5, author.id))
                embed = Embed(description=f"**You have equipped **<:Kipas1:1249539515291533383> `Blood Pattern Floding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR CRIT RATE INCREASE 5%, AND LIFESTEAL RATE INCREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[11]:
            if armor and armor in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot12 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (slot12 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:12:1255403750080778260> Hakama Samurai**", author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 95, author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 650, author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 650, author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Hakama", author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_40:1255403750080778260> `{EQUIPLIST[11]} Samurai Armor`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK INCREASE 95, AND HP INCREASE 650")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[12]:
            if armor and armor in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot13 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (slot13 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:13:1255403728417193994> Shogun Armorr**", author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 520, author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Shogun", author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 520, author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_39:1255403728417193994> `{EQUIPLIST[12]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 520")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[13]:
            if armor and armor in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot14 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (slot14 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:14:1255403801700073533> Shinobi Armor**", author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 820, author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 820, author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 10, author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Shinobi", author.id))
                embed = Embed(description=f"**You have equipped **<:emoji_42:1255403801700073533> `{EQUIPLIST[13]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP INCREASE 820, AND DODGE RATE INCREASE 10%")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        elif equip == EQUIPLIST[14]:
            if armor and armor in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            if armor and armor not in current_item:
                await reply("**YOU ALREADY HAVE AN ARMOR, UNEQUIP IT FIRST**")
            elif slot15 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
               cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (slot15 - 1, author.id))
               cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("**<:15:1249348267645468702> Traveler Armor**", author.id))
               cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 225, author.id))
               cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 225, author.id))
               cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + 10, author.id))
               cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Traveler", author.id))
               embed = Embed(description=f"**You have equipped **<:Pengembara:1249348267645468702> `{EQUIPLIST[14]}` Armor, **Your stats is grow up!**", colour=nextcord.Color.random())
               embed.set_footer(text=f"YOUR HP INCREASE 225, AND BLOCKED DAMAGE INCREASE 10")
               embed.timestamp = datetime.datetime.now()
               await message  (embed=embed)
               pass
        elif equip == EQUIPLIST[15]:
            if fan and fan in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            if fan and fan not in current_item:
                await reply("**YOU ALREADY HAVE A FOLDING FAN, UNEQUIP IT FIRST**")
            elif slot16 == 0:
                await reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot16 = ? WHERE user_id = ?", (slot16 - 1, author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("**<:waletfan:1250032616690683955> Black Walet Folding Fan**", author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + 5, author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 15, author.id))
                embed = Embed(description=f"**You have equipped **<:waletfan:1250032616690683955> `Black Walet Folding Fan`, **Your stats is grow up!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR DODGE RATE INCREASE 5%, AND ATTACK RATE INCREASE 25")
                embed.timestamp = datetime.datetime.now()
                await message  (embed=embed)
                pass
        else:
            await  send("**Item Not Found, Only 1 - 19 Id Item**")

        db.commit()
        cursor.close()
        db.close()

@client.slash_command(name='unequip', description='Unequip your equipment!', force_global=True)
async def unequip(ctx: Interaction, equip: str):

    author = ctx.user
    reply = ctx.send
    send = ctx.send
    message = ctx.send

    EQUIPLIST = ["1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10",
            "11", "12", "13", "14",
            "15", "16", "17", "18", "19"]
    
    EQUIPLIST1 = ["<:1_:1255403773086666782> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:3_:1249342716366684212> Yokai Whirlwind", "<:4_:1249538107389509762> Jewel Necklace", "<:5_:1255403870658625637> Fire Ring",
                "<:6_:1249538267364462703> Golden Tiger Ring", "<:7_:1249538201862017104> Velvet Ring", "<:8_:1255404269197201499> Blue Jewel Necklace", "<:9_:1255404187680903199> Hell's Necklace", "<:10:1249539571905986692> Apricot Flower Floding Fan",
                "<:11:1249539515291533383> Blood Pattern Folding Fan", "<:12:1255403750080778260> Hakama Samurai", "<:13:1255403728417193994> Shogun Armor", "<:14:1255403801700073533> Shinobi Armor",
                "<:15:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan", "<:17:1253647561143619696> Naginata Jade Blade", "<:18:1253647592772866100> Gozen's Bow", "<:19:1253647911057887383> Blood Fox Ring"]
    
        
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16, slot17, slot18, slot19 FROM equipment WHERE user_id = { author.id}")
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
        slot17 = equip_list[16]
        slot18 = equip_list[17]
        slot19 = equip_list[18]
    except:
        await  send("SORRY")

    cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp FROM stats WHERE user_id = { author.id}")
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
        await  send("SORRY")

    cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = { author.id}")
    equipdata = cursor.fetchone()
    try:
        katana = equipdata[0]
        armor = equipdata[1]
        necklace = equipdata[2]
        ring1 = equipdata[3]
        ring2 = equipdata[4]
        fan = equipdata[5]
    except:
        await  send("SORRY")
 
    else:
        current_item = EQUIPLIST1
        if equip == EQUIPLIST[0]:
            if katana == "":
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[1]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[17]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[16]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif katana != current_item[0]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot1 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (slot1 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 235,  author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit - 7,  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_41:1255403773086666782> `{EQUIPLIST[0]}`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 235, AND CRIT RATE DECREASE 7%")
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[16]:
            if katana == "":
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[0]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[1]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[17]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana != current_item[16]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot17 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot17 = ? WHERE user_id = ?", (slot17 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 500,  author.id))
                embed = Embed(description=f"**You have equipped **<:naginata:1253647561143619696> `Naginata Jade Blade`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 500")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[17]:
            if katana == "":
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[0]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[1]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[16]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana != current_item[17]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot18 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot18 = ? WHERE user_id = ?", (slot18 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 500,  author.id))
                embed = Embed(description=f"**You have equipped **<:gozen:1253647592772866100> `Gozen's Bow`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 500")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[18]:
            if ring2 == "":
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring2 != current_item[18]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif ring2 == current_item[5]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot19 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot19 = ? WHERE user_id = ?", (slot19 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 600,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 600,  author.id))
                embed = Embed(description=f"**You have equipped **<:foxring:1253647911057887383> `Blood Fox Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 600")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[1]:
            if katana == "":
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana == current_item[0]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[2]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[17]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[16]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif katana != current_item[1]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot2 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (slot2 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 65,  author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 3,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Crested:1249342749715595417> `Mensen Sword`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 65, AND BLOCKED DAMAGE DECREASE 3")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[2]:
            if katana == "":
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif katana  == current_item[0]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[1]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[17]:
                await  reply("**YOU ALREADY HAVE A SWORD IN CURRENT EQUIPMENT**")
            elif katana == current_item[16]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif katana != current_item[2]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot3 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (slot3 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET katana = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 45,  author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 7,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Whirlwind:1249342716366684212> `Yokai Whirlwind Sword`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 25, AND DODGE RATE DECREASE 7%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[3]:
            if necklace == "":
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[7]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[8]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[3]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot4 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (slot4 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 20,  author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 2,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Kalung1:1249538107389509762> `Jewel Necklace`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR POSTURE DECEREASE 20, AND BLOCKED DAMAGE DECREASE 2")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[4]:
            if ring1 == "":
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring1 == current_item[6]:
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT**")
            elif ring1 != current_item[4]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot5 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (slot5 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 250,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 250,  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 85,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin2:1249538232161538078> `Fire Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 250, AND ATTACK DECREASE 85")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[5]:
            if ring2 == "":
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring2 == current_item[19]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif ring2 != current_item[5]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot6 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (slot6 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET ring2 = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 4,  author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 3,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin3:1249538267364462703> `Golden Tiger Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR BLOCK DECREASE 4, AND DODGE RATE DECREASE 3%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[6]:
            if ring1 == "":
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif ring1 == current_item[4]:
                await  reply("**YOU ALREADY HAVE A RING IN CURRENT EQUIPMENT**")
            elif ring1 != current_item[6]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot7 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (slot7 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET ring1 = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 40,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 40,  author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 20,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Cincin1:1249538201862017104> `Velvet Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 40, AND POSTURE DECREASE 20")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[7]:
            if necklace == "":
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[3]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[8]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[7]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot8 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (slot8 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 175,  author.id))
                cursor.execute(f"UPDATE stats SET posture = ? WHERE user_id = ?", (pos - 15,  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_45:1255404269197201499> `Blue Jewel Ring`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 175, AND POSTURE DECREASE 15")
                embed.timestamp = datetime.datetime.now()
            await  message  (embed=embed)
            pass
        elif equip == EQUIPLIST[8]:
            if necklace == "":
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif necklace == current_item[3]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace == current_item[7]:
                await  reply("**YOU ALREADY HAVE A NECKLACE IN CURRENT EQUIPMENT**")
            elif necklace != current_item[8]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot9 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (slot9 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET necklace = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 205,  author.id))
                cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn - 5,  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_44:1255404187680903199> `Hell's Necklace`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 205, AND BURN RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[9]:
            if fan == "":
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[10]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[15]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[9]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot10 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (slot10 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 20,  author.id))
                cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison - 5,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Kipas2:1249539571905986692> `Apricot Flower Floding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 20, AND POISON RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[10]:
            if fan == "":
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[9]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[15]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[10]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot11 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (slot11 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit - 5,  author.id))
                cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal - 5,  author.id))
                embed = Embed(description=f"**You have unequipped **<:Kipas1:1249539515291533383> `Blood Pattern Floding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR CRIT RATE DECREASE 5%, AND LIFESTEAL RATE DECREASE 5%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[11]:
            if armor == "":
                await  reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[12]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[11]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot12 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (slot12 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 95,  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 650,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 650,  author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin",  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_40:1255403750080778260> `{EQUIPLIST[11]} Samurai Armor`, **Your stats is been reset**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR ATTACK DECREASE 95, AND HP DECREASE 650")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[12]:
            if armor == "":
                await  reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[12]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot13 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (slot13 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 520,  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 520,  author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin",  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_39:1255403728417193994> `{EQUIPLIST[12]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 520")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[13]:
            if armor == "":
                await  reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[12]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[14]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[13]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot14 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (slot14 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 820,  author.id))
                cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 820,  author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 10,  author.id))
                cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Ronin",  author.id))
                embed = Embed(description=f"**You have unequipped **<:emoji_42:1255403801700073533> `{EQUIPLIST[13]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR HP DECREASE 200, AND DODGE RATE DECREASE 10%")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        elif equip == EQUIPLIST[14]:
            if armor == "":
                await  reply("**YOU ALREADY HAVE AN ARMOR IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif armor == current_item[11]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[12]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor == current_item[13]:
                await  reply("**YOU ALREADY HAVE A ARMOR IN CURRENT EQUIPMENT**")
            elif armor != current_item[14]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot15 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
               cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (slot15 + 1,  author.id))
               cursor.execute(f"UPDATE equipdata SET armor = ? WHERE user_id = ?", ("",  author.id))
               cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp - 225,  author.id))
               cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp - 225,  author.id))
               cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block - 10,  author.id))
               cursor.execute(f"UPDATE data SET roles = ? WHERE user_id = ?", ("Traveler",  author.id))
               embed = Embed(description=f"**You have unequipped **<:Pengembara:1249348267645468702> `{EQUIPLIST[14]}` Armor, **Your stats is been reset!**", colour=nextcord.Color.random())
               embed.set_footer(text=f"YOUR HP DECREASE 175, AND BLOCKED DAMAGE DECREASE 10")
               embed.timestamp = datetime.datetime.now()
               await  message  (embed=embed)
               pass
        elif equip == EQUIPLIST[15]:
            if fan == "":
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT, EQUIP IT FIRST**")
            elif fan == current_item[9]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan == current_item[10]:
                await  reply("**YOU ALREADY HAVE A FAN IN CURRENT EQUIPMENT**")
            elif fan != current_item[15]:
                await  send("**YOU ALREADY UNEQUIP IT, EQUIP IT AGAIN FIRST**")
            elif slot16 < 0:
                await  reply("**YOU DONT HAVE THE ITEMS, GET IT FIRST!**")
            else:
                cursor.execute(f"UPDATE equipment SET slot16 = ? WHERE user_id = ?", (slot16 + 1,  author.id))
                cursor.execute(f"UPDATE equipdata SET fan = ? WHERE user_id = ?", ("",  author.id))
                cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge - 5,  author.id))
                cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk - 15,  author.id))
                embed = Embed(description=f"**You have unequipped **<:waletfan:1250032616690683955> `Black Walet Folding Fan`, **Your stats is been reset!**", colour=nextcord.Color.random())
                embed.set_footer(text=f"YOUR DODGE RATE DECREASE 5%, AND ATTACK RATE DECREASE 25")
                embed.timestamp = datetime.datetime.now()
                await  message  (embed=embed)
                pass
        else:
            await  send("**Item Not Found, Only 1 - 19 Id Item**")

        db.commit()
        cursor.close()
        db.close()

if __name__ == '__main__':
    client.run(TOKEN_OS)
