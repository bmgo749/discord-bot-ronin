import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
import itertools

EQUIPLIST1 = ["Shura", "Mensen Sword", "Yokai Whirlwind", "Jewel Necklace", "Fire Ring",
                "Golden Tiger Ring", "Velvet Ring", "Blue Jewel Necklace", "Hell's Necklace", "Apricot Flower Folding Fan",
                "Blood Pattern Folding Fan", "Hakama Samurai", "Shogun Armor", "Shinobi Armor",
                "Traveler Armor"]

EMOJIS = ["<:Shura:1249342778039734354>", "<:Crested:1249342749715595417>", "<:Whirlwind:1249342716366684212>", "<:Kalung1:1249538107389509762>", "<:Cincin2:1249538232161538078>",
                "<:Cincin3:1249538267364462703>", "<:Cincin1:1249538201862017104>", "<:Kalung3:1249538167573446667>", "<:Kalung2:1249538142114152459>", "<:Kipas2:1249539571905986692>",
                "<:Kipas1:1249539515291533383>", "<:Hakama:1249348241536057425>", "<:Shogun:1249348180236177478>", "<:Shinobi:1249348208014921840>",
                "<:Pengembara:1249348267645468702>"]

EQUIPLIST = ["<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlwind", "<:Kalung1:1249538107389509762> Jewel Necklace", "<:Cincin2:1249538232161538078> Fire Ring",
                "<:Cincin3:1249538267364462703> Golden Tiger Ring", "<:Cincin1:1249538201862017104> Velvet Ring", "<:Kalung3:1249538167573446667> Blue Jewel Necklace", "<:Kalung2:1249538142114152459> Hell's Necklace", "<:Kipas2:1249539571905986692>Apricot Flower Folding Fan",
                "<:Kipas1:1249539515291533383> Blood Pattern Folding Fan", "<:Hakama:1249348241536057425> Hakama Samurai", "<:Shogun:1249348180236177478> Shogun Armor", "<:Shinobi:1249348208014921840> Shinobi Armor",
                "<:Pengembara:1249348267645468702> Traveler Armor"]
        
PRICES = [500, 500, 500, 250, 350, 200, 300, 325, 450, 150, 250, 950, 825, 800, 550]

shop_items = random.sample(EQUIPLIST1, 6)
shop_prices = [PRICES[EQUIPLIST1.index(item)] for item in shop_items]  # Exclude the last empty string
items = [EQUIPLIST1.index(item) for item in shop_items]
emojis = [EMOJIS[EQUIPLIST1.index(item)] for item in shop_items]

class Menu(nextcord.ui.View):

    @nextcord.ui.select(
        placeholder="BUY OPTION!",
        options=[nextcord.SelectOption(label=f"{item}", value=item, description=f"Price - {PRICES[EQUIPLIST1.index(item)]}", emoji=f"{EMOJIS[EQUIPLIST1.index(item)]}") for emoji, item in zip(EMOJIS, shop_items)
                 
        ]
    )

    async def select_callback(self, select, ctx: nextcord.Interaction):
        select.disabled = True
        selected_item = select.values[0]
        item_index = shop_items.index(selected_item)
        item_price = shop_prices[item_index]
        item_emoji = emojis[item_index]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15 FROM equipment WHERE user_id = {ctx.user.id}")
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
        except:
            await ctx.send("SORRY")

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {ctx.user.id}")
        jewel = cursor.fetchone()
        try:
            jade = jewel[0]
            coin = jewel[1]
        except:
            await ctx.send("SORRY")
        if item_price > coin:
            await ctx.message.reply("**YOU CANNOT BUY IT ANYMORE!, YOUR COIN WILL BE MINUS OR ERROR!**")
        else:
            if "Shura" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot1 = ? WHERE user_id = ?", (slot1 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Mensen Sword" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot2 = ? WHERE user_id = ?", (slot2 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Yokai Whirlwind" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot3 = ? WHERE user_id = ?", (slot3 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Jewel Necklace" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot4 = ? WHERE user_id = ?", (slot4 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Fire Ring" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot5 = ? WHERE user_id = ?", (slot5 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Golden Tiger Ring" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot6 = ? WHERE user_id = ?", (slot6 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Velvet Ring" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot7 = ? WHERE user_id = ?", (slot7 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Blue Jewel Necklace" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot8 = ? WHERE user_id = ?", (slot8 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Hell's Necklace" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot9 = ? WHERE user_id = ?", (slot9 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id)) 
            elif "Apricot Flower Folding Fan" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot10 = ? WHERE user_id = ?", (slot10 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Blood Pattern Folding Fan" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot11 = ? WHERE user_id = ?", (slot11 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Hakama Samurai" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot12 = ? WHERE user_id = ?", (slot12 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Shogun Armor" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot13 = ? WHERE user_id = ?", (slot13 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Shinobi Armor" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot14 = ? WHERE user_id = ?", (slot14 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            elif "Traveler Armor" in selected_item:
                cursor.execute(f"UPDATE equipment SET slot15 = ? WHERE user_id = ?", (slot15 + 1, ctx.user.id))
                cursor.execute(f"UPDATE jewelry2 SET coin = ? WHERE user_id = ?", (coin - item_price, ctx.user.id))
            else:
                await ctx.message.reply("**🍃YOU DONT HAVE ENOUGH OF COIN!, GET IT FIRST AND BUY THE ITEMS THAT YOU WANT!**")
                return
            
            await ctx.message.reply(f"**You get {item_emoji} {selected_item} with price ** `{item_price}` **<a:coin2:1249302963042648094> Ryo Coin**")

            db.commit()
            cursor.close()
            db.close()



class EquipCommand(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def shop(self, ctx):
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15 FROM equipment WHERE user_id = {ctx.author.id}")
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
        except:
            await ctx.send("SORRY")
            return
    # Randomly select 6 items from EQUIPLIST1
        view = Menu()

        embed = Embed(title="<:scroll:1249924069139157073> EQUIPMENT SHOPS", description="**⛩️ Welcome to the Traveler Market! Here are today's special offer for you. There is six offer good luck for choosing!:**", colour=nextcord.Color.random())
        for index, (emoji, item, price) in enumerate(zip(emojis, shop_items, shop_prices), start=1):
            embed.add_field(name=f"`{index}`. {emoji} {item}", value=F"**- Price : ** `{price}` <a:coin2:1249302963042648094> **Ryo Coin**\n", inline=False)
            embed.set_footer(text="RYO COIN IS FOR TRADE OR BUY, JADE IS FOR GACHA AND TRADE TOO")
            embed.timestamp = datetime.datetime.now()
        
        await ctx.message.reply(embed=embed, mention_author=False, view=view)

        db.commit()
        cursor.close()
        db.close()

    @shop.error
    async def shop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = Embed(description="**You can use @Ronin shop command in 15 Minutes again!**")
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)