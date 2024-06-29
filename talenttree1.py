import nextcord
from nextcord.ext import commands, application_checks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
import itertools

class talenttree(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='talent_tree', description='Show your attack or defense talent_tree', force_global=bool)
    async def talent_tree(self, ctx: Interaction, talent: str = nextcord.SlashOption(
        name='talent',
        choices={"attack": "attack", "defense": "defense"},
        )
    ):

        send = ctx.send
        reply = ctx.send
        author = ctx.user

        print("DATA EXECUTED")

        OPTION = ["attack", "defense"]

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT tameshigiri, storm, sharp, strike, life_blow, leech, sword_enchant, poison_sword, sword_agil, flow, blood_pene, sword_pos, dissension, resistance, talisman, orbs, phoenix FROM talenttree1 WHERE user_id = { author.id}")
        talenttree = cursor.fetchone()
        print(f"Talent Tree : {talenttree}")

        try:
            tameshigiri = talenttree[0]
            storm = talenttree[1]
            sharp = talenttree[2]
            strike = talenttree[3]
            life_blow = talenttree[4]
            leech = talenttree[5]
            sword_enchant = talenttree[6]
            poison_sword = talenttree[7]
            sword_agil = talenttree[8]
            flow = talenttree[9]
            blood_pene = talenttree[10]
            sword_pos = talenttree[11]
            dissension = talenttree[12]
            resistance = talenttree[13]
            talisman = talenttree[14]
            orbs = talenttree[15]
            phoenix = talenttree[16]
        except:
            tameshigiri = 0
            storm = 0
            sharp = 0
            strike = 0
            life_blow = 0
            leech = 0
            sword_enchant = 0
            poison_sword = 0
            sword_agil = 0
            flow = 0
            blood_pene = 0
            sword_pos = 0
            dissension = 0
            resistance = 0
            talisman = 0
            orbs = 0
            phoenix = 0
        
        cursor.execute(f"SELECT vitality, vitalpos, dodge, scud, flow, sturdy, penet, blockedsoul, yokaiscroll, heartspirit, hawkeye, concentrate, acc, stormmove, steelwill, firemove, craziness, onimusha, gauge FROM talenttree2 WHERE user_id = { author.id}")
        talenttree11 = cursor.fetchone()
        if talenttree11:
            vitality, vitalpos, dodge, scud, flow1, sturdy, penet, blockedsoul, yokaiscroll, heartspirit, hawkeye, concentrate, acc, stormmove, steelwill, firemove, craziness, onimusha, gauge = talenttree11
        else:
            vitality = vitalpos = dodge = scud = flow1 = sturdy = penet = blockedsoul = yokaiscroll = heartspirit = hawkeye = concentrate = acc = stormmove = steelwill = firemove = craziness = gauge = 0
            onimusha = "Locked"

        if talent == OPTION[0]:
            embed = Embed(title=f"{ author.name} ATTACK TALENT TREE",
                          colour=nextcord.Color.random())
            embed.add_field(name=f"<a:soulair:1250094797423775816> Sword Enhancement Talent Tree:", value=f"<:emoji_34:1250080593610412182> **Tameshigiri :**`Level {tameshigiri}/15`\n<:emoji_33:1250080563814072330> **Storm Sword :**`Level {storm}/10`\n<:emoji_39:1250080804231708682> **Sword Enchant :**`Level {sword_enchant}/10`\n<:emoji_41:1250080954333270157> **Sword Agility :**`Level {sword_agil}/10`\n<:emoji_44:1250081114585043075> **Sword Posture :**`Level {sword_pos}/15`\n<:emoji_36:1250080702146285579> **Strike Blow :**`Level {strike}/5`\n<:emoji_35:1250080661067272293> **Sharpness :**`Level {sharp}/10`", inline=True)
            embed.add_field(name=f"<a:soul1:1250094883105013851> Lifesteal Talent Tree:", value=f"<:emoji_42:1250081027523870730> **Flow Sword :**`Level {flow}/15`\n<:emoji_43:1250081088894668840> **Blood Pierce :**`Level {blood_pene}/10`\n<:emoji_45:1250081148361506907> **Dissension :**`Level {dissension}/5`\n**<:emoji_49:1250081305979519069> Life Orbs :**`Level {orbs}/5`\n<:emoji_37:1250080738397913279> **Lifesteal Blow :**`Level {life_blow}/5`\n<:emoji_38:1250080772149350450> **Leech Enhance :**`Level {leech}/5`", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) 
            embed.add_field(name=f"<a:Soul1:1250102286311493674> Burn and Poison Enhancement Talent Tree:", value=f"<:emoji_40:1250080830080942213> **Poison Sword :**`Level {poison_sword}/5`\n<:emoji_50:1250081338040782940> **Phoenix :**`Level {phoenix}/5`\n<:emoji_47:1250081245422157958><:emoji_48:1250081271766581278> **Talisman :**`Level {talisman}/5`", inline=True)
            embed.add_field(name=f"<a:exp2:1249296823655338046> Unique Talent Tree:", value=f"<:emoji_46:1250081179408011355> **Resistance :**`Level {resistance}/3`", inline=True)
            embed.set_footer(text=f"ATTACK TALENT TREE")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1197079152281538694/1250083798373372007/Picsart_24-06-11_19-54-52-760.png?ex=6669a6c2&is=66685542&hm=01ba3875e28767e911bc4083aaf40964da19f0ef28fa05ff21c6cb86e9e1c901&")
            embed.timestamp = datetime.datetime.now()
            print("Reached before embed")
            await  reply(embed=embed)
            print("Reached after embed")

        elif talent == OPTION[1]:
            embed = Embed(title=f"{ author.name} DEFENSE TALENT TREE",
                          colour=nextcord.Color.random())
            embed.add_field(name=f"<a:soulair:1250094797423775816> Defense and Vitality Talent Tree:", value=f"<:emoji_33:1250301086640767056> **Vitality :**`Level {vitality}/15`\n<:emoji_34:1250301127744950293> **Vital Posture :**`Level {vitalpos}/10`\n<:emoji_36:1250301233932144672> **Sturdy :**`Level {sturdy}/5`\n<:emoji_49:1250301758723592203> **Gauge :**`Level {gauge}/1`\n<:emoji_46:1250301613864652860> **Steel Will :**`Level {steelwill}/5`\n<:emoji_44:1250301543874433036> **Heart Spirit**`Level {heartspirit}/10`", inline= True)
            embed.add_field(name=f"<a:soul1:1250094883105013851> Dodge Posture Talent Tree:", value=f"<:emoji_35:1250301180186464296> **Dodge :**`Level {dodge}/10`\n<:emoji_37:1250301281382432849> **Flow :**`Level {flow1}/10`\n<:emoji_38:1250301314999521321> **Scud :**`Level {scud}/10`\n<:emoji_48:1250301725227876373> **Storm Movement :**`Level {stormmove}/3`\n<:emoji_47:1250301691677642772> **Fire Movement :**`Level {firemove}/3`", inline= True)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name=f"<a:Soul1:1250102286311493674> Dodge and Blocking Talent Tree", value=f"<:emoji_39:1250301353277001759> **Penetration :**`Level {penet}/5`\n<:emoji_40:1250301380946558997> **Blocked Soul :**`Level {blockedsoul}/5`\n<:emoji_41:1250301444289200160> **Concentrate :**`Level {concentrate}/5`\n<:emoji_42:1250301477591715881> **Hawk Eye :**`Level {hawkeye}/5`\n<:emoji_43:1250301509845913680> **Accurate Eye :**`Level {acc}/10`\n<:emoji_45:1250301577869398067> **Yokai Scroll :**`Level {yokaiscroll}/5`", inline=True)
            embed.add_field(name=f"<a:exp2:1249296823655338046> Unique Talent Tree", value=f"<:emoji_50:1250301790805561395> **Craziness :**`Level {craziness}/3`\n<:emoji_51:1250301834686496981> **Onimusha : **`{onimusha}`", inline=True)
            embed.set_footer(text=f"DEFENSE TALENT TREE")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1248138075863781472/1250251334846906468/Picsart_24-06-12_07-51-58-920.jpg?ex=666a42ca&is=6668f14a&hm=83c3ee0729475e78159ac57de997df002fcf92c3b8fcd14b3c0f443b454110d3&")
            embed.timestamp = datetime.datetime.now()
            print("Reached before embed")
            await  reply(embed=embed)
            print("Reached after embed")

        elif talent.lower() not in OPTION:
            await  send(f"**THERE IS NO OPTION {talent}!, ONLY attack OR defense...**")

        db.commit()
        cursor.close()
        db.close()

    @nextcord.slash_command(name='up_talent', description='Upgrade your attack and defense talent', force_global=bool)
    async def up_talent(self, ctx: Interaction, name_talent: str, category: str = nextcord.SlashOption(
        name='talent',
        choices={"attack": "attack", "defense": "defense"},
        ),
    ):

        send = ctx.send
        reply = ctx.send
        author = ctx.user

        OPTION = ["attack", "defense"]
        TALENTATTACK = ["Tameshigiri", "StormSword", "Sharpness", "Strike", "LifestealBlow",
                        "LeechEnhance", "SwordEnchant", "PoisonSword", "SwordAgil", "FlowSword",
                        "BloodPierce", "SwordPosture", "Dissension", "Resistance", "Talisman",
                        "LifeOrbs", "Phoenix"]
        
        TALENTDEFENSE = ["Vitality", "VitalPos", "Dodge", "Scud", 'Flow', 'Sturdy', 'Penet', 'BlockedSoul', 'YokaiScroll', 
                         'HeartsSirit', 'Hawkeye', 'Concentrate', 'Acc', 'StormMove', 'SteelWill', 'FireMove', 'Craziness', 
                         'Onimusha', 'Gauge']

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

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

        cursor.execute(f"SELECT tameshigiri, storm, sharp, strike, life_blow, leech, sword_enchant, poison_sword, sword_agil, flow, blood_pene, sword_pos, dissension, resistance, talisman, orbs, phoenix FROM talenttree1 WHERE user_id = { author.id}")
        talenttree = cursor.fetchone()

        if talenttree:
            tameshigiri, storm, sharp, strike, life_blow, leech, sword_enchant, poison_sword, sword_agil, flow, blood_pene, sword_pos, dissension, resistance, talisman, orbs, phoenix = talenttree
        else:
            tameshigiri = storm = sharp = strike = life_blow = leech = sword_enchant = poison_sword = sword_agil = flow = blood_pene = sword_pos = dissension = resistance = talisman = orbs = phoenix = 0

        cursor.execute(f"SELECT vitality, vitalpos, dodge, scud, flow, sturdy, penet, blockedsoul, yokaiscroll, heartspirit, hawkeye, concentrate, acc, stormmove, steelwill, firemove, craziness, onimusha, gauge FROM talenttree2 WHERE user_id = { author.id}")
        talenttree2 = cursor.fetchone()
        if talenttree2:
            vitality, vitalpos, dodge1, scud, flow1, sturdy, penet, blockedsoul, yokaiscroll, heartspirit, hawkeye, concentrate, acc, stormmove, steelwill, firemove, craziness, onimusha, gauge = talenttree2
        else:
            vitality = vitalpos = dodge1 = scud = flow1 = sturdy = penet = blockedsoul = yokaiscroll = heartspirit = hawkeye = concentrate = acc = stormmove = steelwill = firemove = craziness = gauge = 0
            onimusha = "Locked"

        cursor.execute(f"SELECT level, talent, exp FROM level WHERE user_id = { author.id}")
        stats3 = cursor.fetchone()
        try:
            level = stats3[0]
            talent = stats3[1]
            exp = stats3[2]
        except:
            await  send("LOL")

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = { author.id}")
        jewel = cursor.fetchone()
        try:
            jade = jewel[0]
            coin = jewel[1]
        except:
            await  send("LOL")

        if category == OPTION[0]:
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[0]:
                    if tameshigiri < 15:
                        if tameshigiri < 6:
                            talent_cost = 1
                            atk_stats = 5
                            jade_cost = 20
                        elif tameshigiri < 11:
                            talent_cost = 2
                            atk_stats = 7
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            atk_stats = 9
                            jade_cost = 40

                    level_talent = tameshigiri + 1

                    if tameshigiri == 15:
                        await  reply(f"**YOUR <:emoji_34:1250080593610412182> TAMESHIGIRI TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET tameshigiri = ? WHERE user_id = ?", (tameshigiri + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_34:1250080593610412182> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent}`**, your attack stats grow up** `+{atk_stats}`",
                                      colour=nextcord.Color.random())
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[1]:
                    if storm < 10:
                        if storm < 4:
                            talent_cost = 1
                            atk_stats = 5
                            dodge_stats = 0.5
                            jade_cost = 25
                        elif storm < 7:
                            talent_cost = 2
                            atk_stats = 9
                            dodge_stats = 1
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            atk_stats = 13
                            dodge_stats = 1
                            jade_cost = 40

                    level_talent1 = storm + 1

                    if tameshigiri < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_34:1250080593610412182> TAMESHIGIRI TALENT TO LEVEL 10!**")

                    elif storm == 10:
                        await  reply(f"**YOUR <:emoji_33:1250080563814072330> STORM TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET storm = ? WHERE user_id = ?", (storm + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_33:1250080563814072330> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack stats grow up** `+{atk_stats}` **with dodge rate thats grow up too** `+{dodge_stats}`",
                                      colour=nextcord.Color.random())
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[2]:
                    if sharp < 10:
                        if sharp < 4:
                            talent_cost = 1
                            atk_stats = 3
                            jade_cost = 30
                        elif sharp < 7:
                            talent_cost = 2
                            atk_stats = 5
                            jade_cost = 35
                        else:
                            talent_cost = 3
                            atk_stats = 7
                            jade_cost = 45

                    level_talent1 = sharp + 1

                    if storm < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_33:1250080563814072330> STORM TALENT TO LEVEL 5!**")

                    elif sharp == 10:
                        await  reply(f"**YOUR <:emoji_35:1250080661067272293> SHARPNESS TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET sharp = ? WHERE user_id = ?", (sharp + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_35:1250080661067272293> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack stats grow up** `+{atk_stats}`")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[3]:
                    if strike < 5:
                        if strike < 2:
                            talent_cost = 2
                            atk_stats = 10
                            crit_stats = 2
                            jade_cost = 35
                        elif strike < 4:
                            talent_cost = 3
                            atk_stats = 15
                            crit_stats = 3
                            jade_cost = 40
                        else:
                            talent_cost = 4
                            atk_stats = 20
                            crit_stats = 5
                            jade_cost = 50

                    level_talent1 = strike + 1

                    if sharp < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_35:1250080661067272293> SHARPNESS TALENT TO LEVEL 5!**")

                    elif strike == 5:
                        await  reply(f"**YOUR <:emoji_36:1250080702146285579> STRIKE BLOW TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET strike = ? WHERE user_id = ?", (strike + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + crit_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_36:1250080702146285579> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack stats grow up** `+{atk_stats}`**, with crit rate that grow too `+{crit_stats}`**")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[4]:
                    if life_blow < 5:
                        if life_blow < 2:
                            talent_cost = 2
                            lifesteal_stats = 1
                            jade_cost = 25
                        elif life_blow < 4:
                            talent_cost = 2
                            lifesteal_stats = 2
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            lifesteal_stats = 3
                            jade_cost = 35

                    level_talent1 = life_blow + 1

                    if strike < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_36:1250080702146285579> STRIKE BLOW TALENT TO LEVEL 3!**")

                    elif life_blow == 5:
                        await  reply(f"**YOUR <:emoji_37:1250080738397913279> LIFESTEAL BLOW TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET life_blow = ? WHERE user_id = ?", (life_blow + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_37:1250080738397913279> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate** {lifesteal_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[5]:
                    if leech < 5:
                        if leech < 2:
                            talent_cost = 2
                            lifesteal_stats = 1
                            jade_cost = 25
                        elif leech < 4:
                            talent_cost = 2
                            lifesteal_stats = 2
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            lifesteal_stats = 3
                            jade_cost = 35

                    level_talent1 = leech + 1

                    if strike < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_37:1250080738397913279> LIFESTEAL BLOW TALENT TO LEVEL 3!**")

                    elif leech == 5:
                        await  reply(f"**YOUR <:emoji_38:1250080772149350450> LEECH ENHANCE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET leech = ? WHERE user_id = ?", (leech + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_38:1250080772149350450> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate** {lifesteal_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[6]:
                    if sword_enchant < 10:
                        if sword_enchant < 4:
                            talent_cost = 2
                            atk_stats = 3
                            jade_cost = 35
                        elif sword_enchant < 7:
                            talent_cost = 2
                            atk_stats = 6
                            jade_cost = 40
                        else:
                            talent_cost = 3
                            atk_stats = 9
                            jade_cost = 45

                    level_talent1 = sword_enchant + 1

                    if life_blow < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_38:1250080772149350450> <:emoji_37:1250080738397913279> LIFESTEAL BLOW TALENT TO LEVEL 3!**")

                    elif sword_enchant == 10:
                        await  reply(f"**YOUR <:emoji_39:1250080804231708682> SWORD ENCHANT TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET sword_enchant = ? WHERE user_id = ?", (sword_enchant + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_39:1250080804231708682> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack been grow up** {atk_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[7]:
                    if poison_sword < 5:
                        if poison_sword < 2:
                            talent_cost = 2
                            pois_stats = 5
                            jade_cost = 35
                        elif poison_sword < 4:
                            talent_cost = 3
                            pois_stats = 7
                            jade_cost = 40
                        else:
                            talent_cost = 3
                            pois_stats = 10
                            jade_cost = 45

                    level_talent1 = poison_sword + 1

                    if sword_enchant < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_39:1250080804231708682> SWORD ENCHANT TALENT TO LEVEL 5!**")

                    elif poison == 5:
                        await  reply(f"**YOUR <:emoji_40:1250080830080942213> POISON SWORD TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET poison_sword = ? WHERE user_id = ?", (poison_sword + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison + pois_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_40:1250080830080942213> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your poison rate been grow up** {pois_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[8]:
                    if sword_agil < 10:
                        if sword_agil < 4:
                            talent_cost = 1
                            atk_stats = 2
                            jade_cost = 20
                        elif sword_agil < 8:
                            talent_cost = 2
                            atk_stats = 4
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            atk_stats = 6
                            jade_cost = 40

                    level_talent = sword_agil + 1

                    if sword_agil == 10:
                        await  reply(f"**YOUR <:emoji_41:1250080954333270157> SWORD AGILITY TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET sword_agil = ? WHERE user_id = ?", (sword_agil + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_41:1250080954333270157> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent}`**, your attack stats grow up** `+{atk_stats}`",
                                      colour=nextcord.Color.random())
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[9]:
                    if flow < 15:
                        if flow < 6:
                            talent_cost = 1
                            lifesteal_stats = 0.5
                            jade_cost = 10
                        elif flow < 11:
                            talent_cost = 2
                            lifesteal_stats = 1
                            jade_cost = 20
                        else:
                            talent_cost = 3
                            lifesteal_stats = 1.5
                            jade_cost = 25

                    level_talent1 = flow + 1

                    if sword_agil < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_41:1250080954333270157> SWORD AGILITY TALENT TO LEVEL 10!**")

                    elif flow == 15:
                        await  reply(f"**YOUR <:emoji_42:1250081027523870730> FLOW SWORD TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET flow = ? WHERE user_id = ?", (flow + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_42:1250081027523870730> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate grow up** `+{lifesteal_stats}`",
                                      colour=nextcord.Color.random())
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[10]:
                    if blood_pene < 10:
                        if blood_pene < 4:
                            talent_cost = 1
                            lifesteal_stats = 0.5
                            jade_cost = 10
                        elif blood_pene < 8:
                            talent_cost = 1
                            lifesteal_stats = 1
                            jade_cost = 20
                        else:
                            talent_cost = 2
                            lifesteal_stats = 1.5
                            jade_cost = 30

                    level_talent1 = blood_pene + 1

                    if flow < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_42:1250081027523870730> FLOW SWORD TALENT TO LEVEL 5!**")

                    elif blood_pene == 10:
                        await  reply(f"**YOUR <:emoji_43:1250081088894668840> BLOOD PIERCE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET blood_pene = ? WHERE user_id = ?", (sharp + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_43:1250081088894668840> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate grow up** `+{lifesteal_stats}`")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[11]:
                    if sword_pos < 15:
                        if sword_pos < 6:
                            talent_cost = 2
                            atk_stats = 2
                            crit_stats = 0.5
                            jade_cost = 35
                        elif sword_pos < 11:
                            talent_cost = 3
                            atk_stats = 4
                            crit_stats = 1
                            jade_cost = 40
                        else:
                            talent_cost = 4
                            atk_stats = 6
                            crit_stats = 2
                            jade_cost = 50

                    level_talent1 = sword_pos + 1

                    if blood_pene < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_43:1250081088894668840> BLOOD PIERCE TALENT TO LEVEL 5!**")

                    elif sword_pos == 15:
                        await  reply(f"**YOUR <:emoji_44:1250081114585043075> SWORD POSTURE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET sword_pos = ? WHERE user_id = ?", (sword_pos + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET crit = ? WHERE user_id = ?", (crit + crit_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_44:1250081114585043075> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack stats grow up** `+{atk_stats}`**, with crit rate that grow too `+{crit_stats}`**")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[12]:
                    if dissension < 5:
                        if dissension < 2:
                            talent_cost = 2
                            lifesteal_stats = 1
                            jade_cost = 25
                        elif dissension < 4:
                            talent_cost = 2
                            lifesteal_stats = 2
                            jade_cost = 30
                        else:
                            talent_cost = 3
                            lifesteal_stats = 3
                            jade_cost = 35

                    level_talent1 = dissension + 1

                    if sword_pos < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_44:1250081114585043075> SWORD POSTURE TALENT TO LEVEL 10!**")

                    elif dissension == 5:
                        await  reply(f"**YOUR <:emoji_45:1250081148361506907> DISSENSION TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET dissension = ? WHERE user_id = ?", (dissension + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_45:1250081148361506907> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate** {lifesteal_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[15]:
                    if orbs < 5:
                        if orbs < 2:
                            talent_cost = 2
                            lifesteal_stats = 2
                            jade_cost = 30
                        elif orbs < 4:
                            talent_cost = 3
                            lifesteal_stats = 3
                            jade_cost = 35
                        else:
                            talent_cost = 3
                            lifesteal_stats = 4
                            jade_cost = 40

                    level_talent1 = orbs + 1

                    if dissension < 3 or talisman < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_45:1250081148361506907> DISSENSION AND <:emoji_47:1250081245422157958><:emoji_48:1250081271766581278> TALISMAN TALENT TO LEVEL 3!**")

                    elif orbs == 5:
                        await  reply(f"**YOUR <:emoji_49:1250081305979519069> LIFE ORBS TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET orbs = ? WHERE user_id = ?", (orbs + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET lifesteal = ? WHERE user_id = ?", (lifesteal + lifesteal_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_49:1250081305979519069> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your lifesteal rate** {lifesteal_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[13]:
                    if resistance < 3:
                        if resistance < 1:
                            talent_cost = 5
                            atk_stats = 30
                            jade_cost = 60
                        elif resistance < 7:
                            talent_cost = 10
                            atk_stats = 65
                            jade_cost = 120
                        else:
                            talent_cost = 15
                            atk_stats = 100
                            jade_cost = 240

                    level_talent1 = leech + 1

                    if sword_pos < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_44:1250081114585043075> SWORD POSTURE TALENT TO LEVEL 3!**")

                    elif resistance == 3:
                        await  reply(f"**YOUR <:emoji_46:1250081179408011355> RESISTANCE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET resistance = ? WHERE user_id = ?", (resistance + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + atk_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK UNIQUE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_46:1250081179408011355> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your attack been grow up** {atk_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[14]:
                    if talisman < 5:
                        if talisman < 2:
                            talent_cost = 2
                            pois_stats = 5
                            burn_stats = 5
                            jade_cost = 35
                        elif talisman < 4:
                            talent_cost = 3
                            pois_stats = 7
                            burn_stats = 7
                            jade_cost = 40
                        else:
                            talent_cost = 3
                            pois_stats = 10
                            burn_stats = 10
                            jade_cost = 45

                    level_talent1 = talisman + 1

                    if dissension < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_45:1250081148361506907> DISSENSION TALENT TO LEVEL 3!**")

                    elif talisman == 5:
                        await  reply(f"**YOUR <:emoji_47:1250081245422157958><:emoji_48:1250081271766581278> TALISMAN TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET talisman = ? WHERE user_id = ?", (talisman + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET poison_dmg = ? WHERE user_id = ?", (poison + pois_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn + burn_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_47:1250081245422157958><:emoji_48:1250081271766581278> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your poison and burn rate been grow up POISON =** `+{pois_stats}%`**, BURN =** `+{burn_stats}%`")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
            if name_talent in TALENTATTACK:
                if name_talent == TALENTATTACK[16]:
                    if phoenix < 5:
                        if phoenix < 2:
                            talent_cost = 2
                            burn_stats = 5
                            jade_cost = 35
                        elif phoenix < 4:
                            talent_cost = 3
                            burn_stats = 7
                            jade_cost = 40
                        else:
                            talent_cost = 3
                            burn_stats = 10
                            jade_cost = 45

                    level_talent1 = phoenix + 1

                    if orbs < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_49:1250081305979519069> LIFE ORBS TALENT TO LEVEL 5!**")

                    elif phoenix == 5:
                        await  reply(f"**YOUR <:emoji_50:1250081338040782940> PHOENIX TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTATTACK:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree1 SET phoenix = ? WHERE user_id = ?", (phoenix + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET burn_dmg = ? WHERE user_id = ?", (burn + burn_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} ATTACK TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_50:1250081338040782940> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your burn rate been grow up** +{burn_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

        elif category == OPTION[1]:
            if name_talent in TALENTDEFENSE:
                if name_talent == TALENTDEFENSE[0]:
                    if vitality < 15:
                        if vitality < 6:
                            talent_cost = 1
                            jade_cost = 20
                            hp_stats = 30
                        elif vitality < 11:
                            talent_cost = 2
                            jade_cost = 25
                            hp_stats = 40
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            hp_stats = 50

                    level_talent1 = vitality + 1

                    if vitality == 15:
                        await  reply(f"**YOUR <:emoji_33:1250301086640767056> VITALITY TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET vitality = ? WHERE user_id = ?", (vitality + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_33:1250301086640767056> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your hp has been grow up** +{hp_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[2]:
                    if dodge1 < 10:
                        if dodge1 < 4:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 0.5
                        elif dodge1 < 8:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 1
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            dodge_stats = 1.5

                    level_talent1 = dodge1 + 1

                    if vitalpos < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_34:1250301127744950293> VITAL POSTURE TALENT TO LEVEL 5!**")

                    elif dodge1 == 10:
                        await  reply(f"**YOUR <:emoji_35:1250301180186464296> DODGE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET dodge = ? WHERE user_id = ?", (dodge1 + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_35:1250301180186464296> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[1]:
                    if vitalpos < 10:
                        if vitalpos < 4:
                            talent_cost = 1
                            jade_cost = 20
                            hp_stats = 30
                        elif vitalpos < 8:
                            talent_cost = 2
                            jade_cost = 25
                            hp_stats = 40
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            hp_stats = 50

                    level_talent1 = vitalpos + 1

                    if vitality < 10:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_33:1250301086640767056> VITALITY TALENT TO LEVEL 10!**")

                    elif vitalpos == 10:
                        await  reply(f"**YOUR <:emoji_34:1250301127744950293> VITAL POSTURE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET vitalpos = ? WHERE user_id = ?", (vitalpos + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_34:1250301127744950293> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your hp has been grow up** +{hp_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[5]:
                    if sturdy < 5:
                        if sturdy < 2:
                            talent_cost = 1
                            jade_cost = 20
                            hp_stats = 30
                        elif sturdy < 4:
                            talent_cost = 2
                            jade_cost = 25
                            hp_stats = 40
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            hp_stats = 50

                    level_talent1 = sturdy + 1

                    if dodge < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_35:1250301180186464296> DODGE TALENT TO LEVEL 5!**")

                    elif sturdy == 10:
                        await  reply(f"**YOUR <:emoji_36:1250301233932144672> STURDY TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET sturdy = ? WHERE user_id = ?", (sturdy + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_36:1250301233932144672> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your hp has been grow up** +{hp_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[3]:
                    if scud < 10:
                        if scud < 4:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 0.5
                        elif scud < 8:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 1
                        else:
                            talent_cost = 2
                            jade_cost = 30
                            dodge_stats = 1.5

                    level_talent1 = scud + 1

                    if sturdy < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_36:1250301233932144672> STURDY TALENT TO LEVEL 3!**")

                    elif scud == 10:
                        await  reply(f"**YOUR <:emoji_38:1250301314999521321> SCUD TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET scud = ? WHERE user_id = ?", (scud + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_38:1250301314999521321> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[6]:
                    if penet < 5:
                        if penet < 2:
                            talent_cost = 1
                            jade_cost = 20
                            block_stats = 5
                        elif penet < 4:
                            talent_cost = 3
                            jade_cost = 25
                            block_stats = 10
                        else:
                            talent_cost = 3
                            jade_cost = 35
                            block_stats = 20

                    level_talent1 = penet + 1

                    if scud < 5 and flow < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_38:1250301314999521321> SCUD AND <:emoji_37:1250301281382432849> FLOW TALENT TO LEVEL 5!**")

                    elif penet == 5:
                        await  reply(f"**YOUR <:emoji_39:1250301353277001759> PENETRATION TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET penet = ? WHERE user_id = ?", (penet + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + block_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_39:1250301353277001759> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your blocked damage has been grow up** +{block_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[4]:
                    if flow1 < 10:
                        if flow1 < 4:
                            talent_cost = 1
                            jade_cost = 15
                            dodge_stats = 0.5
                        elif flow1 < 8:
                            talent_cost = 2
                            jade_cost = 20
                            dodge_stats = 1
                        else:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 1.5

                    level_talent1 = flow1 + 1

                    if sturdy < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_36:1250301233932144672> STURDY TALENT TO LEVEL 5!**")

                    elif flow1 == 10:
                        await  reply(f"**YOUR <:emoji_37:1250301281382432849> FLOW TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    elif talent >= talent_cost and jade >= jade_cost:
                        cursor.execute(f"UPDATE talenttree2 SET flow = ? WHERE user_id = ?", (flow1 + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_37:1250301281382432849> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[7]:
                    if blockedsoul < 5:
                        if blockedsoul < 2:
                            talent_cost = 2
                            jade_cost = 25
                            block_stats = 25
                        elif blockedsoul < 4:
                            talent_cost = 3
                            jade_cost = 30
                            block_stats = 30
                        else:
                            talent_cost = 3
                            jade_cost = 35
                            block_stats = 35

                    level_talent1 = blockedsoul + 1

                    if penet < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_39:1250301353277001759> PENETRATION TALENT TO LEVEL 5!**")

                    elif blockedsoul == 5:
                        await  reply(f"**YOUR <:emoji_40:1250301380946558997> BLOCKED SOUL TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET blockedsoul = ? WHERE user_id = ?", (blockedsoul + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + block_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_40:1250301380946558997> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your blocked damage has been grow up** +{block_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

            
            #TALENT KE DUA


                elif name_talent == TALENTDEFENSE[11]:
                    if concentrate < 5:
                        if concentrate < 2:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 1
                        elif concentrate < 4:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 1.5
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            dodge_stats = 2

                    level_talent1 = concentrate + 1

                    if concentrate == 5:
                        await  reply(f"**YOUR <:emoji_41:1250301444289200160> CONCENTRATE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET concentrate = ? WHERE user_id = ?", (concentrate + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge1 + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_41:1250301444289200160> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[10]:
                    if hawkeye < 5:
                        if hawkeye < 2:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 1
                        elif hawkeye < 4:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 1.5
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            dodge_stats = 2

                    level_talent1 = hawkeye + 1

                    if concentrate < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_41:1250301444289200160> CONCENTRATE TALENT TO LEVEL 3!**")

                    elif hawkeye == 5:
                        await  reply(f"**YOUR <:emoji_42:1250301477591715881> HAWK EYE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET hawkeye = ? WHERE user_id = ?", (hawkeye + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_42:1250301477591715881> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[12]:
                    if acc < 10:
                        if acc < 4:
                            talent_cost = 1
                            jade_cost = 10
                            dodge_stats = 0.25
                        elif acc < 8:
                            talent_cost = 2
                            jade_cost = 15
                            dodge_stats = 0.5
                        else:
                            talent_cost = 2
                            jade_cost = 20
                            dodge_stats = 1

                    level_talent1 = acc + 1

                    if hawkeye < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_42:1250301477591715881> HAWK EYE TALENT TO LEVEL 3!**")

                    elif acc == 10:
                        await  reply(f"**YOUR <:emoji_43:1250301509845913680> ACCURATE EYE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET acc = ? WHERE user_id = ?", (acc + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_43:1250301509845913680> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[9]:
                    if heartspirit < 10:
                        if heartspirit < 4:
                            talent_cost = 1
                            jade_cost = 25
                            hp_stats = 35
                        elif heartspirit < 8:
                            talent_cost = 3
                            jade_cost = 30
                            hp_stats = 45
                        else:
                            talent_cost = 3
                            jade_cost = 35
                            hp_stats = 55

                    level_talent1 = heartspirit + 1

                    if acc < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_43:1250301509845913680> ACCURATE EYE TALENT TO LEVEL 10!**")

                    elif heartspirit == 10:
                        await  reply(f"**YOUR <:emoji_44:1250301543874433036> HEART SPIRIT TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET heartspirit = ? WHERE user_id = ?", (heartspirit + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_44:1250301543874433036> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your hp has been grow up** +{hp_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[14]:
                    if steelwill < 5:
                        if steelwill < 2:
                            talent_cost = 1
                            jade_cost = 20
                            hp_stats = 30
                        elif steelwill < 4:
                            talent_cost = 2
                            jade_cost = 25
                            hp_stats = 40
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            hp_stats = 50

                    level_talent1 = steelwill + 1

                    if heartspirit < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_44:1250301543874433036> HEART SPIRIT TALENT TO LEVEL 5!**")

                    elif steelwill == 5:
                        await  reply(f"**YOUR <:emoji_46:1250301613864652860> STEELWILL TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET steelwill = ? WHERE user_id = ?", (steelwill + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + hp_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_46:1250301613864652860> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your hp has been grow up** +{hp_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[15]:
                    if firemove < 3:
                        if firemove < 1:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 2
                        elif firemove < 2:
                            talent_cost = 2
                            jade_cost = 30
                            dodge_stats = 3
                        else:
                            talent_cost = 3
                            jade_cost = 35
                            dodge_stats = 4

                    level_talent1 = firemove + 1

                    if heartspirit < 5:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_44:1250301543874433036> HEART SPIRIT TALENT TO LEVEL 5!**")

                    elif firemove == 3:
                        await  reply(f"**YOUR <:emoji_47:1250301691677642772> FIRE MOVEMENT TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET firemove = ? WHERE user_id = ?", (firemove + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_47:1250301691677642772> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[8]:
                    if yokaiscroll < 5:
                        if yokaiscroll < 2:
                            talent_cost = 1
                            jade_cost = 20
                            block_stats = 5
                        elif yokaiscroll < 4:
                            talent_cost = 2
                            jade_cost = 25
                            block_stats = 7
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            block_stats = 10

                    level_talent1 = yokaiscroll + 1

                    if heartspirit < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_44:1250301543874433036> HEART SPIRIT TALENT TO LEVEL 3!**")

                    elif yokaiscroll == 5:
                        await  reply(f"**YOUR <:emoji_45:1250301577869398067> YOKAISCROLL TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET yokaiscroll = ? WHERE user_id = ?", (yokaiscroll + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + block_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_45:1250301577869398067> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your blocked damage has been grow up** +{block_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[13]:
                    if stormmove < 3:
                        if stormmove < 1:
                            talent_cost = 1
                            jade_cost = 20
                            dodge_stats = 2
                        elif stormmove < 2:
                            talent_cost = 2
                            jade_cost = 25
                            dodge_stats = 3
                        else:
                            talent_cost = 3
                            jade_cost = 30
                            dodge_stats = 4

                    level_talent1 = stormmove + 1

                    if yokaiscroll < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_45:1250301577869398067> YOKAI SCROLL TALENT TO LEVEL 3!**")

                    elif stormmove == 3:
                        await  reply(f"**YOUR <:emoji_48:1250301725227876373> STORM MOVEMENT TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET stormmove = ? WHERE user_id = ?", (stormmove + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_48:1250301725227876373> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your dodge rate has been grow up** +{dodge_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[18]:
                    if gauge < 1:
                        talent_cost = 5
                        jade_cost = 55
                        block_stats = 75
                        dodge_stats = 10

                    level_talent1 = gauge + 1

                    if stormmove < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_48:1250301725227876373> STORM MOVEMENT TALENT TO LEVEL 3!**")

                    elif gauge == 1:
                        await  reply(f"**YOUR <:emoji_49:1250301758723592203> GAUGE TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET gauge = ? WHERE user_id = ?", (gauge + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + block_stats,  author.id))
                        cursor.execute(f"UPDATE stats SET dodge = ? WHERE user_id = ?", (dodge1 + dodge_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} DEFENSE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_49:1250301758723592203> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your blocked damage has been grow up** +{block_stats} **and dodge rate increase +{dodge_stats}**")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass

                elif name_talent == TALENTDEFENSE[16]:
                    if craziness < 3:
                        if craziness < 1:
                            talent_cost = 2
                            jade_cost = 35
                            block_stats = 50
                        elif craziness < 2:
                            talent_cost = 3
                            jade_cost = 45
                            block_stats = 100
                        else:
                            talent_cost = 3
                            jade_cost = 60
                            block_stats = 150

                    level_talent1 = craziness + 1
                    
                    if firemove < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_47:1250301691677642772> FIRE MOVEMENT TALENT TO LEVEL 3!**")

                    elif craziness == 3:
                        await  reply(f"**YOUR <:emoji_50:1250301790805561395> CRAZINESS TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET craziness = ? WHERE user_id = ?", (craziness + 1,  author.id))
                        cursor.execute(f"UPDATE stats SET block = ? WHERE user_id = ?", (block + block_stats,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} UNIQUE TALENT UPGRADE",
                                      description=f"**Successfully upgrade your** <:emoji_50:1250301790805561395> `{name_talent}` **Talent!, now your talent is upgraded to Level** `{level_talent1}`**, your blocked damage has been grow up** +{block_stats}")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
                
                elif name_talent == TALENTDEFENSE[17]:
                    if craziness < 3:
                        await  reply(f"**YOU NEED ATLEAST UPGRADE YOUR <:emoji_50:1250301790805561395> CRAZINESS TALENT TO LEVEL 3!**")

                    elif onimusha == "Unlocked":
                        await  reply(f"**YOUR <:emoji_51:1250301834686496981> ONIMUSHA TALENT ALREADY REACH MAX LEVEL!**")
                    
                    elif talent < talent_cost or jade < jade_cost:
                        await  reply("**YOU DONT HAVE ENOUGH JADE OR TALENT, GET IT FIRST!**")
                    
                    elif name_talent not in TALENTDEFENSE:
                        await  reply(f"**NO TALENT NAMED {name_talent}!**")

                    elif category not in OPTION:
                        await  reply(f"**NO CATEGORY NAMED {category}, ONLY attack OR defense CATEGORY!**")

                    else:
                        cursor.execute(f"UPDATE talenttree2 SET onimusha = ? WHERE user_id = ?", ("Unlocked",  author.id))
                        cursor.execute(f"UPDATE stats SET attack = ? WHERE user_id = ?", (atk + 200,  author.id))
                        cursor.execute(f"UPDATE stats SET hp = ? WHERE user_id = ?", (hp + 500,  author.id))
                        cursor.execute(f"UPDATE stats SET maxhp = ? WHERE user_id = ?", (maxhp + 500,  author.id))
                        cursor.execute(f"UPDATE level SET talent = ? WHERE user_id = ?", (talent - talent_cost,  author.id))
                        cursor.execute(f"UPDATE jewelry2 SET jade = ? WHERE user_id = ?", (jade - jade_cost,  author.id))

                        embed = Embed(title=f"{ author.name} UNIQUE TALENT UPGRADE",
                                      description=f"**Successfully unlock your** <:emoji_51:1250301834686496981> `{name_talent}` **Talent!, now your talent is unlocked!, your damage and hp has been grow up +** `{atk_stats}` **and** `{hp_stats}`")
                        embed.set_footer(text=f"TALENT COST {talent_cost} AND JADE COST {jade_cost}")
                        embed.timestamp = datetime.datetime.now()
                        await  reply(embed=embed  )
                        pass
        db.commit()
        cursor.close()
        db.close()