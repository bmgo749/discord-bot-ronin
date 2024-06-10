import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
from event import Event
from inventory import InventoryCommand

#MAIN CODE

TOKEN_OS = "MTI0ODA2OTQ0NDI3ODgxMjc3Ng.Gz3GvH.quD-EJmGJ9Xf4Saqk5wt_Tyn44Cme5-8_NBOvY"

client = commands.Bot(command_prefix= lambda bot, msg:f"<@{bot.user.id}> ", intents=nextcord.Intents.all())

client.add_cog(Event(client))
client.add_cog(InventoryCommand(client))

#SQLITE PERMS

@client.event
async def on_ready():
    print(f"Logged in {client.user}!")
    await client.change_presence(activity=nextcord.activity.Game(name="Samurai Gambit 🎲"), status=nextcord.Status.idle)

@client.command()
async def profile(ctx):
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
    embed.add_field(name=f"**<:samurai:1249260973337088041> Character :**", value=f"<:roles:1249284936142422088> Roles : `{roles}`\n<:Kenshin:1249284889132531793> Character Name : `{char_name}`\n🍃 Gender : `{gender}`\n", inline=False)
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

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(description=f"**You still in cooldown!, wait until the cooldown time is done!**\n\n`Cooldown time = {round(error.retry_after)} second`")
        await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN_OS)