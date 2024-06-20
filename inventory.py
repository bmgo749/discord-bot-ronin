import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
import itertools

class InventoryCommand(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inv(self, ctx):

        view = Equipment(ctx.author.id)

        List = [None, "<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind", "<:Kalung1:1249538107389509762>  Jewel Necklace", "<:Cincin2:1249538232161538078>  Fire Ring",
                "<:Cincin3:1249538267364462703> Golden Tiger Ring", "<:Cincin1:1249538201862017104>  Velvet Ring", "<:Kalung3:1249538167573446667>  Blue Jewel Necklace", "<:Kalung2:1249538142114152459>  Hell's Necklace", "<:Kipas2:1249539571905986692>  Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383>  Blood Pattern Folding Fan", "<:Hakama:1249348241536057425> Hakama Samurai", "<:Shogun:1249348180236177478> Shogun Armor", "<:Shinobi:1249348208014921840> Shinobi Armor",
                "<:Pengembara:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan"]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM equipment WHERE user_id = {ctx.author.id}")
        list = cursor.fetchone()

        list_ = [f"{i} x{j}" for i, j in itertools.zip_longest(List, list) if j > 0 and j < 100000000000000000]
    
        list_ = "\n".join(list_) if len(list_) > 0 else "**You don't have any equipment**"

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {ctx.author.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           jade = 100
           coin = 1000

        embed = Embed(title=f"{ctx.author.name} INVENTORY & LIST ITEM",
                      colour=nextcord.Color.random())
    
        embed.add_field(name="<:atk:1249261884960538686> Equipment : ", value=f"**{list_}**", inline=False)
        embed.add_field(name=f"<a:ruby:1249305945767546921> Valuable : ", value=f"<a:coin2:1249302963042648094>`Ryo Coin {coin}x`\n<:jade:1249302977450344481>`Tagamata Jade {jade}x`", inline=False)
        embed.set_footer(text="THIS IS WAS ALL OF YOUR ITEMS")
        embed.timestamp = datetime.datetime.now()

        await ctx.message.reply(embed=embed, mention_author = False, view=view)

        db.commit()
        cursor.close()
        db.close()

class Previous(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    async def interaction_check(self, interaction):
        # Hanya izinkan pengguna yang mengeksekusi perintah untuk berinteraksi dengan tombol
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("**You are not allowed to interact with this button.**", ephemeral=True)
            return False
        return True
    
    @nextcord.ui.button(label="Previous", style=nextcord.ButtonStyle.gray)
    async def previous(self, button: nextcord.ui.Button, ctx: Interaction):
        if ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return

        view2 = Equipment(ctx.user.id)
        
        List = [None, "<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlwind", "<:Kalung1:1249538107389509762>  Jewel Necklace", "<:Cincin2:1249538232161538078>  Fire Ring",
                "<:Cincin3:1249538267364462703> Golden Tiger Ring", "<:Cincin1:1249538201862017104>  Velvet Ring", "<:Kalung3:1249538167573446667>  Blue Jewel Necklace", "<:Kalung2:1249538142114152459>  Hell's Necklace", "<:Kipas2:1249539571905986692>  Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383>  Blood Pattern Folding Fan", "<:Hakama:1249348241536057425> Hakama Samurai", "<:Shogun:1249348180236177478> Shogun Armor", "<:Shinobi:1249348208014921840> Shinobi Armor",
                "<:Pengembara:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan"]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM equipment WHERE user_id = {ctx.user.id}")
        list = cursor.fetchone()

        list_ = [f"{i} x{j}" for i, j in itertools.zip_longest(List, list) if j > 0 and j < 100000000000000000]
    
        list_ = "\n".join(list_) if len(list_) > 0 else "**You don't have any equipment**"

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {ctx.user.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           jade = 100
           coin = 1000

        embed = Embed(title=f"{ctx.user.name} INVENTORY & LIST ITEM",
                      colour=nextcord.Color.random())
    
        embed.add_field(name="<:atk:1249261884960538686> Equipment : ", value=f"**{list_}**", inline=False)
        embed.add_field(name=f"<a:ruby:1249305945767546921> Valuable : ", value=f"<a:coin2:1249302963042648094>`Ryo Coin {coin}x`\n<:jade:1249302977450344481>`Tagamata Jade {jade}x`", inline=False)
        embed.set_footer(text="THIS IS WAS ALL OF YOUR ITEMS")
        embed.timestamp = datetime.datetime.now()

        await ctx.response.edit_message(embed=embed, view=view2)

        db.commit()
        cursor.close()
        db.close()

class Equipment(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    async def interaction_check(self, interaction):
        # Hanya izinkan pengguna yang mengeksekusi perintah untuk berinteraksi dengan tombol
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("**You are not allowed to interact with this button.**", ephemeral=True)
            return False
        return True

    @nextcord.ui.button(label="Equipment", style=nextcord.ButtonStyle.primary)
    async def equip1(self, button: nextcord.ui.Button, ctx: Interaction):
        if ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return

        view1 = Previous(ctx.user.id)
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = {ctx.user.id}")
        equipdata = cursor.fetchone()
        try:
            katana = equipdata[0]
            armor = equipdata[1]
            necklace = equipdata[2]
            ring1 = equipdata[3]
            ring2 = equipdata[4]
            fan = equipdata[5]
        except:
            katana = ""
            armor = ""
            necklace = ""
            ring1 = ""
            ring2 = ""
            fan = ""

        embed = Embed(title=f"{ctx.user.display_name} DATA EQUIPMENT IS USING",
                      colour=nextcord.Color.random())
        
        embed.add_field(name="<:samurai:1249260973337088041> EQUIPMENT :", value=f"<:atk:1249261884960538686> Katana : {katana}\n<:armorsam:1249586824339390609> Armor : {armor}\n<:necklacesam:1249586802159779851> Necklace : {necklace}\n💍 Ring 1 : {ring1}\n💍 Ring 2 : {ring2}\n<:foldingfan:1249586779041042504> Folding Fan : {fan}")
        embed.set_footer(text=f"{ctx.user.display_name} EQUIPMENT IS USING")
        embed.timestamp = datetime.datetime.now()

        await ctx.response.edit_message(embed=embed, view=view1)

        db.commit()
        cursor.close()
        db.close()