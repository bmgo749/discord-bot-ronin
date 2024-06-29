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

    @nextcord.slash_command(name='inv', description='All of your Items in inventory!', force_global=bool)
    async def inv(self, ctx: Interaction):

        author =  ctx.user
        message =  ctx.send

        view = Equipment( author.id)

        List = [None, "<:1_:1255403773086666782> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:3_:1249342716366684212> Yokai Whirlind", "<:4_:1249538107389509762> Jewel Necklace", "<:5_:1255403870658625637> Fire Ring",
                "<:6_:1249538267364462703> Golden Tiger Ring", "<:7_:1249538201862017104> Velvet Ring", "<:8_:1255404269197201499> Blue Jewel Necklace", "<:9_:1255404187680903199> Hell's Necklace", "<:10:1249539571905986692> Apricot Flower Floding Fan",
                "<:11:1249539515291533383> Blood Pattern Folding Fan", "<:12:1255403750080778260> Hakama Samurai", "<:13:1255403728417193994> Shogun Armor", "<:14:1255403801700073533> Shinobi Armor",
                "<:15:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan", "<:17:1253647561143619696> Naginata Jade Blade", "<:18:1253647592772866100> Gozen's Bow", "<:19:1253647911057887383> Blood Fox Ring"]
        
        ListR = [None, "<:IronIngot:1255191092501024779> Iron", "<:fabric:1255405019037962293> Cloth", "<:rocck:1255191037970743380> Ore", "<:TagamataJade:1255191134376951878> Jewel", 
                 "<:leather:1255408408761335894> Leather", "<:Woood:1255191065409884212> Wood"]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM equipment WHERE user_id = { author.id}")
        list = cursor.fetchone()

        cursor.execute(f"SELECT * FROM resource WHERE user_id = { author.id}")
        listR = cursor.fetchone()

        list_ = [f"{i} x{j}" for i, j in itertools.zip_longest(List, list) if j > 0 and j < 100000000000000000]
        list_r = [f"{i} x{j}" for i, j in itertools.zip_longest(ListR, listR) if j > 0 and j < 100000000000000000]
    
        list_ = "\n".join(list_) if len(list_) > 0 else "**You don't have any equipment**"
        list_r = "\n".join(list_r) if len(list_r) > 0 else "**You don't have any resource**"

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = { author.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           jade = 0
           coin = 0

        embed = Embed(title=f"{ author.name} INVENTORY & LIST ITEM",
                      colour=nextcord.Color.random())
    
        embed.add_field(name="<:atk:1249261884960538686> Equipment : ", value=f"**{list_}**", inline=False)
        embed.add_field(name=f"<a:ruby:1249305945767546921> Valuable : ", value=f"<:coin:1255419339038003271>`Ryo Coin {coin}x`\n<:TagamataJade:1255191134376951878>`Tagamata Jade {jade}x`", inline=False)
        embed.add_field(name="<:resource2:1255736004527001712> Resource :", value=f"**{list_r}**", inline=False)
        embed.set_footer(text="THIS IS WAS ALL OF YOUR ITEMS")
        embed.timestamp = datetime.datetime.now()

        await  message(embed=embed, view=view)

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
        if  ctx.user.id != self.user_id:
            await ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return
        
        user = ctx.user

        view2 = Equipment( user.id)
        
        List = [None, "<:1_:1255403773086666782> Shura", "<:2_:1249342749715595417> Mensen Sword", "<:3_:1249342716366684212> Yokai Whirlind", "<:4_:1249538107389509762> Jewel Necklace", "<:Cincin2:1249538232161538078> Fire Ring",
                "<:6_:1249538267364462703> Golden Tiger Ring", "<:7_:1249538201862017104> Velvet Ring", "<:8_:1255404269197201499> Blue Jewel Necklace", "<:9_:1255404187680903199> Hell's Necklace", "<:Kipas2:1249539571905986692> Apricot Flower Floding Fan",
                "<:Kipas1:1249539515291533383> Blood Pattern Folding Fan", "<:14:1255403801700073533> Hakama Samurai", "<:13:1255403728417193994> Shogun Armor", "<:14:1255403801700073533> Shinobi Armor",
                "<:15:1249348267645468702> Traveler Armor", "<:waletfan:1250032616690683955> Black Walet Folding Fan", "<:17:1253647561143619696> Naginata Jade Blade", "<:18:1253647592772866100> Gozen's Bow", "<:19:1253647911057887383> Blood Fox Ring"]
        
        ListR = [None, "<:IronIngot:1255191092501024779> Iron", "<:fabric:1255405019037962293> Cloth", "<:rocck:1255191037970743380> Ore", "<:TagamataJade:1255191134376951878> Jewel", 
                 "<:leather:1255408408761335894> Leather", "<:Woood:1255191065409884212> Wood"]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM equipment WHERE user_id = { user.id}")
        list = cursor.fetchone()

        cursor.execute(f"SELECT * FROM resource WHERE user_id = { user.id}")
        listR = cursor.fetchone()

        list_ = [f"{i} x{j}" for i, j in itertools.zip_longest(List, list) if j > 0 and j < 100000000000000000]
        list_r = [f"{i} x{j}" for i, j in itertools.zip_longest(ListR, listR) if j > 0 and j < 100000000000000000]
    
        list_ = "\n".join(list_) if len(list_) > 0 else "**You don't have any equipment**"
        list_r = "\n".join(list_r) if len(list_r) > 0 else "**You don't have any resource**"

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = { user.id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
           jade = 0
           coin = 0

        embed = Embed(title=f"{ user.name} INVENTORY & LIST ITEM",
                      colour=nextcord.Color.random())
    
        embed.add_field(name="<:atk:1249261884960538686> Equipment : ", value=f"**{list_}**", inline=False)
        embed.add_field(name=f"<a:ruby:1249305945767546921> Valuable : ", value=f"<:coin:1255419339038003271>`Ryo Coin {coin}x`\n<:TagamataJade:1255191134376951878>`Tagamata Jade {jade}x`", inline=False)
        embed.add_field(name="<:resource2:1255736004527001712> Resource :", value=f"**{list_r}**", inline=False)
        embed.set_footer(text="THIS IS WAS ALL OF YOUR ITEMS")
        embed.timestamp = datetime.datetime.now()

        await  ctx.response.edit_message(embed=embed, view=view2)

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

        user = ctx.user

        if  user.id != self.user_id:
            await  ctx.response.send_message("**YOU ARE NOT THE USER THAT EXECUTED THIS COMMAND.**", ephemeral=True)
            return

        view1 = Previous( user.id)
        
        db = sqlite3.connect("main.sqlite") 
        cursor = db.cursor()
        
        cursor.execute(f"SELECT katana, armor, necklace, ring1, ring2, fan FROM equipdata WHERE user_id = { user.id}")
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

        embed = Embed(title=f"{ user.display_name} DATA EQUIPMENT IS USING",
                      description="**To Equip or Unequip The Equipment you only just to type /equip <id item> or /unequip <id item> (id item in emoji, tap the equipment emoji in the inventory. Just type the number without _ or any symbol)**",
                      colour=nextcord.Color.random())
        
        embed.add_field(name="<:samurai:1249260973337088041> EQUIPMENT :", value=f"<:atk:1249261884960538686> Katana : {katana}\n<:armorsam:1249586824339390609> Armor : {armor}\n<:necklacesam:1249586802159779851> Necklace : {necklace}\n💍 Ring 1 : {ring1}\n💍 Ring 2 : {ring2}\n<:foldingfan:1249586779041042504> Folding Fan : {fan}")
        embed.set_footer(text=f"{ user.display_name} EQUIPMENT IS USING")
        embed.timestamp = datetime.datetime.now()

        await  ctx.response.edit_message(embed=embed, view=view1)

        db.commit()
        cursor.close()
        db.close()