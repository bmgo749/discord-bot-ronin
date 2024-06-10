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

        List = [None, "<:Shura:1249342778039734354> Shura", "<:Crested:1249342749715595417> Mensen Sword", "<:Whirlwind:1249342716366684212> Yokai Whirlind"]

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

        await ctx.message.reply(embed=embed, mention_author = False)

        db.commit()
        cursor.close()
        db.close()