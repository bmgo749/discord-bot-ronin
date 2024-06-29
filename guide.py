import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions, user

class GuideCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='start', description='Start your path!, choose yourself and get bonus!', force_global=bool)
    async def start_command(self, ctx: Interaction):

        author = ctx.user
        reply = ctx.send
        send = ctx.send

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT path FROM data WHERE user_id = {author.id}")
        path = cursor.fetchone()

        if not path:
            await send("You dont have the data")
            return
        
        path = path[0]

        if path == "Shogun" or path == "Ronin":
            await reply("**🗡️ You have already chosen your path and already started! ⚔️**")
            return

        viewsupport = nextcord.ui.Button(label="Support Server", url="https://discord.gg/z3UASrwZyx")
        view = ButtonGuide2()
        view.add_item(viewsupport)
        embed = nextcord.Embed(
            title="⛩️ Welcome, Wanderer!",
            description=f"So, is your name {author.mention}, right?\n\n"
                        "So, Let Me Introduce Myself, My Name is Hanzou, So I Will Give You a Choice, Which is, Do You Want to Be a <:Shogun:1255355636200243220> Shogun or a <:ronin:1255355659080437831> Ronin?\n\n"
                        "If you choose <:ronin:1255355659080437831> Ronin, then you can choose your own destiny, and form a Ronin group to overthrow the <:Shogun:1255355636200243220> Shogun's reign.\n\n"
                        "And if you choose the <:Shogun:1255355636200243220> Shogun, You Will Be Chosen as One of the Lords, And You Have a Mission to Topple the <:ronin:1255355659080437831> Ronin Rebellion.",
            color=0xAC3229
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1251151968265568326/1255416971789598770/Tak_berjudul52_20240626145829.png?ex=667d0daa&is=667bbc2a&hm=49ebdc9ae45f59cd8d9a62e842476341b194001ae60ec53cc357381e4ac7dbcd&")
        embed.add_field(name="Choose Your Path", value="React with <:Shogun:1255355636200243220> to become a Shogun or <:ronin:1255355659080437831> to become a Ronin.", inline=False)

        await send(embed=embed, view=view)

    @nextcord.slash_command(name='craft', description='Craft your item!', force_global=bool)
    async def craft(self, ctx: Interaction, item: str = None):

        author = ctx.user
        reply = ctx.send
        send = ctx.send

        if item is None:
            await send("*Type the name item that you want to craft! (type the id item, for more info check in @Ronin inv)*")
            return

        author = user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM resource WHERE user_id = ?", (author.id,))
        resource = cursor.fetchone()

        if not resource:
            await send("LOL", ephemeral=True)
            cursor.close()
            db.close()
            return
        
        cursor.execute("SELECT * FROM equipment WHERE user_id = ?", (author.id,))
        equipment = cursor.fetchone()

        if not equipment:
            await send("LOL")
            cursor.close()
            db.close()
            return
        
        if item == "1":

            res1 = 95
            res2 = 45
            res3 = 35

            if resource[1] < res1 or resource[5] < res2 or resource[6] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:Woood:1255191065409884212> Wood)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot1 = ? WHERE user_id = ?", (equipment[1] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Shura Sword` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "2":

            res1 = 55
            res2 = 25
            res3 = 20

            if resource[1] < res1 or resource[5] < res2 or resource[6] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:Woood:1255191065409884212> Wood)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot2 = ? WHERE user_id = ?", (equipment[2] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Mensen Sword` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "3":

            res1 = 55
            res2 = 25
            res3 = 20

            if resource[1] < res1 or resource[5] < res2 or resource[6] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:Woood:1255191065409884212> Wood)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot3 = ? WHERE user_id = ?", (equipment[3] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Yokai Whirlwind Sword` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "5":

            res1 = 65
            res2 = 55
            res3 = 15

            if resource[1] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot5 = ? WHERE user_id = ?", (equipment[5] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Fire Ring` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "6":

            res1 = 25
            res2 = 15
            res3 = 5

            if resource[1] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot6 = ? WHERE user_id = ?", (equipment[6] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Golden Tiger Ring` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "7":

            res1 = 35
            res2 = 25
            res3 = 10

            if resource[1] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot7 = ? WHERE user_id = ?", (equipment[7] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Velvet Ring` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "4":

            res1 = 5
            res2 = 10
            res3 = 15

            if resource[6] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:Woood:1255191065409884212> Wood, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot4 = ? WHERE user_id = ?", (equipment[4] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Jewel Necklace` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "8":

            res1 = 25
            res2 = 40
            res3 = 55

            if resource[6] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:Woood:1255191065409884212> Wood, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot8 = ? WHERE user_id = ?", (equipment[8] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Blue Jewel Necklace` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "9":

            res1 = 35
            res2 = 55
            res3 = 75

            if resource[6] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:Woood:1255191065409884212> Wood, {res2} <:rocck:1255191037970743380> Ore, {res3} <:TagamataJade:1255191134376951878> Jewel)*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] - res3, author.id))
            cursor.execute("UPDATE equipment SET slot9 = ? WHERE user_id = ?", (equipment[9] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Hell's Necklace` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "10":

            res1 = 15
            res2 = 20
            res3 = 10

            if resource[6] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:Woood:1255191065409884212> Wood, {res3} <:rocck:1255191037970743380> Ore, {res2} <:leather:1255408408761335894> Leather)*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE equipment SET slot10 = ? WHERE user_id = ?", (equipment[10] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Apricot Flower Folding Fan` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "11":

            res1 = 25
            res2 = 35
            res3 = 25

            if resource[6] < res1 or resource[3] < res2 or resource[4] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:Woood:1255191065409884212> Wood, {res3} <:rocck:1255191037970743380> Ore, {res2} <:leather:1255408408761335894> Leather)*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] - res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] - res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE equipment SET slot11 = ? WHERE user_id = ?", (equipment[11] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Blood Pattern Folding Fan` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()

        elif item == "12":

            res1 = 40
            res2 = 55
            res3 = 65

            if resource[1] < res1 or resource[5] < res2 or resource[2] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:fabric:1255405019037962293> Cloth)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] - res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE equipment SET slot12 = ? WHERE user_id = ?", (equipment[12] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Hakama` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()
        
        elif item == "13":

            res1 = 35
            res2 = 45
            res3 = 50

            if resource[1] < res1 or resource[5] < res2 or resource[2] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:fabric:1255405019037962293> Cloth)*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] - res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE equipment SET slot13 = ? WHERE user_id = ?", (equipment[13] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Samurai` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()
        
        elif item == "15":

            res1 = 15
            res2 = 20
            res3 = 15

            if resource[1] < res1 or resource[5] < res2 or resource[2] < res3:
                await send(f"*You don't have enough resource to craft it! (Need {res1} <:IronIngot:1255191092501024779> Iron, {res2} <:leather:1255408408761335894> Leather, {res3} <:fabric:1255405019037962293> Cloth)*")
                return
            
            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] - res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] - res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] - res2, author.id))
            cursor.execute("UPDATE equipment SET slot15 = ? WHERE user_id = ?", (equipment[15] + 1, author.id))
            await send("**SUCCESSFULLY CRAFT** `Traveler` **CHECK YOUR INVENTORY!**")
            db.commit()
            cursor.close()
        else:
            await ctx.send("*Not found it.*")

    @nextcord.slash_command(name='dismantle', description='Dismantle your equipment!', force_global=bool)
    async def dismantle(self, ctx: Interaction, item: str = None):

        author = ctx.user
        reply = ctx.send
        send = ctx.send

        if item is None:
            await send("*Type the name item that you want to dismantle! (type the id item, for more info check in @Ronin inv)*")
            return

        author = user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM resource WHERE user_id = ?", (author.id,))
        resource = cursor.fetchone()

        if not resource:
            await send("LOL", ephemeral=True)
            cursor.close()
            db.close()
            return
        
        cursor.execute("SELECT * FROM equipment WHERE user_id = ?", (author.id,))
        equipment = cursor.fetchone()

        if not equipment:
            await send("LOL")
            cursor.close()
            db.close()
            return
        
        if item == "1":

            res1 = 95
            res2 = 45
            res3 = 35

            if equipment[1] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot1 = ? WHERE user_id = ?", (equipment[1] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Shura Sword` **ALL OF RESOURCE GET BACK!!**")
            db.commit()
            cursor.close()

        elif item == "2":

            res1 = 55
            res2 = 25
            res3 = 20

            if equipment[2] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot2 = ? WHERE user_id = ?", (equipment[2] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Mensen Sword` **ALL OF RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "3":

            res1 = 55
            res2 = 25
            res3 = 20

            if equipment[3] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot3 = ? WHERE user_id = ?", (equipment[3] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Yokai Whirlwind Sword` **ALL OF RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "5":

            res1 = 65
            res2 = 55
            res3 = 15

            if equipment[5] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot5 = ? WHERE user_id = ?", (equipment[5] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Fire Ring` **ALL OF RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "6":

            res1 = 25
            res2 = 15
            res3 = 5

            if equipment[6] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot6 = ? WHERE user_id = ?", (equipment[6] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Golden Tiger Ring` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "7":

            res1 = 35
            res2 = 25
            res3 = 10

            if equipment[7] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot7 = ? WHERE user_id = ?", (equipment[7] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Velvet Ring` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "4":

            res1 = 5
            res2 = 10
            res3 = 15

            if equipment[4] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot4 = ? WHERE user_id = ?", (equipment[4] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Jewel Necklace` **ALL OF YOUR RESOURCE GET BACK!**")
            db.commit()
            cursor.close()

        elif item == "8":

            res1 = 25
            res2 = 40
            res3 = 55

            if equipment[8] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot8 = ? WHERE user_id = ?", (equipment[8] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Blue Jewel Necklace` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "9":

            res1 = 35
            res2 = 55
            res3 = 75

            if equipment[9] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res2, author.id))
            cursor.execute("UPDATE resource SET jewel = ? WHERE user_id = ?", (resource[4] + res3, author.id))
            cursor.execute("UPDATE equipment SET slot9 = ? WHERE user_id = ?", (equipment[9] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Hell's Necklace` **ALL OF YOUR RESOURCE GET BACK!**")
            db.commit()
            cursor.close()

        elif item == "10":

            res1 = 15
            res2 = 20
            res3 = 10

            if equipment[10] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE equipment SET slot10 = ? WHERE user_id = ?", (equipment[10] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Apricot Flower Folding Fan` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "11":

            res1 = 25
            res2 = 35
            res3 = 25

            if equipment[11] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET wood = ? WHERE user_id = ?", (resource[6] + res1, author.id))
            cursor.execute("UPDATE resource SET ore = ? WHERE user_id = ?", (resource[3] + res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE equipment SET slot11 = ? WHERE user_id = ?", (equipment[11] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Blood Pattern Folding Fan` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()

        elif item == "12":

            res1 = 40
            res2 = 55
            res3 = 65

            if equipment[12] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] + res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE equipment SET slot12 = ? WHERE user_id = ?", (equipment[12] - 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Hakama` **ALL OF YOUR RESOURCE GET BACK!**")
            db.commit()
            cursor.close()
        
        elif item == "13":

            res1 = 35
            res2 = 45
            res3 = 50

            if equipment[13] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] + res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE equipment SET slot13 = ? WHERE user_id = ?", (equipment[13] + 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Samurai` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()
        
        elif item == "15":

            res1 = 15
            res2 = 20
            res3 = 15

            if equipment[15] <= 0:
                await send(f"*You don't have the item. Craft or get it!*")
                return

            cursor.execute("UPDATE resource SET iron = ? WHERE user_id = ?", (resource[1] + res1, author.id))
            cursor.execute("UPDATE resource SET cloth = ? WHERE user_id = ?", (resource[2] + res3, author.id))
            cursor.execute("UPDATE resource SET leather = ? WHERE user_id = ?", (resource[5] + res2, author.id))
            cursor.execute("UPDATE equipment SET slot15 = ? WHERE user_id = ?", (equipment[15] + 1, author.id))
            await send("**SUCCESSFULLY DISMANTLE** `Traveler` **ALL OF YOUR RESOURCE GET BACK**")
            db.commit()
            cursor.close()
        else:
            await ctx.send("*Not found it.*")

class ButtonGuide2(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Ronin", style=nextcord.ButtonStyle.red, emoji="<:ronin:1255355659080437831>")
    async def button_ronin_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT path FROM data WHERE user_id = {user.id}")
        path = cursor.fetchone()

        if not path:
            await ctx.send("You dont have the data")
            return
        
        path = path[0]

        if path == "Shogun" or path == "Ronin":
            await ctx.response.send_message("**🗡️ You already choosing your own path! ⚔️.**")
            return
        
        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {user.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           await ctx.send("LOL")
        
        cursor.execute(f"UPDATE data SET path = ? WHERE user_id = ?", ("Ronin", user.id))
        cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin + 550, user.id))

        embed = Embed(title="RONIN PATH ⚔️", description=f"**You are choosing** `RONIN` **Path. Now you can just continue your own path without any Order. (Extra 550 Coins for start!) ⚖️**", colour=nextcord.Color.random())
        embed.set_footer(text="YOU ARE CHOOSING RONIN PATH")
        embed.timestamp = datetime.datetime.now()
        db.commit()

        await ctx.response.edit_message(content=None, embed=embed, delete_after=6)

        db.commit()
        cursor.close()
        db.close()

    @nextcord.ui.button(label="Shogun", style=nextcord.ButtonStyle.blurple, emoji="<:Shogun:1255355636200243220>")
    async def button_ronin2_callback(self, button: nextcord.ui.Button, ctx: Interaction):

        user = ctx.user

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT path FROM data WHERE user_id = {user.id}")
        path = cursor.fetchone()

        if not path:
            await ctx.send("You dont have the data")
            return
        
        path = path[0]

        if path == "Shogun" or path == "Ronin":
            await ctx.response.send_message("**🗡️ You already choosing your own path! ⚔️.**")
            return
        
        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {user.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           await ctx.send("LOL")
        
        cursor.execute(f"UPDATE data SET path = ? WHERE user_id = ?", ("Shogun", user.id))
        cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin + 550, user.id))

        embed = Embed(title="SHOGUN PATH 🗡️", description=f"**You are choosing** `SHOGUN` **Path. Now you can just continue your own path without any Order ⚖️**", colour=nextcord.Color.random())
        embed.set_footer(text="YOU ARE CHOOSING SHOGUN PATH")
        embed.timestamp = datetime.datetime.now()
        db.commit()

        await ctx.response.edit_message(content=None, embed=embed, delete_after=6)

        db.commit()
        cursor.close()
        db.close()