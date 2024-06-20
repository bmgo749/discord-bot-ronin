import nextcord
from nextcord.ext import commands, application_checks, tasks
import json, os, sqlite3, random
from datetime import datetime
import time, schedule
import datetime, asyncio
from nextcord import Embed, Interaction, mentions
import itertools

exp_amount = random.randint(10, 20)
jade_amount = random.randint(25, 50)
honor_amount = random.randint(2, 7)
coin_amount = random.randint(950, 1250)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.inventory = {
            'sacred_scroll': 0
        }

    @staticmethod
    def get_npc_stats(has_sacred_scroll=False):
        if has_sacred_scroll:
            bosses = [
                {
                    'name': '<:saito:1252525845101150279> Saito Nobumasa - The Best Japan Spearman',
                    'attack': random.randint(560, 645),
                    'hp': 3500,
                    'max_hp': 3500,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(1, 5),
                    'dodge': random.randint(1, 5),
                    'block': random.randint(100, 150),
                    'skills': [
                        {
                            'name': 'Triple Blood Lance',
                            'damage': 450,
                            'rate': 0.6,
                            'buff': {
                                'name': 'Cruel',
                                'damage_increase': 100
                            }
                        },
                        {
                            'name': 'Blood Spear',
                            'damage': 600,
                            'rate': 0.4,
                            'multiplier': 2,
                            'rate_skill': 0.3
                        }
                    ],
                    'passive': {
                        'name': 'Ironheart of Spear',
                        'hp_threshold': 0.5,  # 50% HP threshold
                        'heal_amount': 0.25  # 25% HP heal
                    }
                },
                {
                    'name': '<:hironi:1252525784384409600> Elite Samurai - Hirano Masanori',
                    'attack': random.randint(745, 870),
                    'hp': 5000,
                    'max_hp': 5000,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(5, 10),
                    'dodge': random.randint(5, 10),
                    'block': random.randint(200, 300),
                    'skills': [
                        {
                            'name': 'Fury of Katana',
                            'damage': 900,
                            'rate': 0.5,
                            'bonus_damage': 1.0  # 100% of base damage
                        },
                        {
                            'name': 'Fast Bleeding Slash',
                            'damage': 2000,
                            'rate': 0.3,
                            'bleed': {
                                'damage_percent': 0.05,  # 5% HP per round
                                'rounds': 3
                            }
                        }
                    ],
                    'passive': {
                        'name': 'Samurai Resilience',
                        'hp_threshold': 0.25,  # 25% HP threshold
                        'defense_boost': 0.5  # 50% defense boost
                    }
                }
            ]
            return random.choice(bosses)
        
        else:
            npcs = [
                {
                    'name': 'Shogun Swordsman',
                    'attack': random.randint(210, 250),
                    'hp': 485,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(1, 5),
                    'dodge': random.randint(1, 5),
                    'block': random.randint(65, 95)
                },
                {
                    'name': 'Shogun Spearman',
                    'attack': random.randint(230, 270),
                    'hp': 535,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(1, 5),
                    'dodge': random.randint(1, 5),
                    'block': random.randint(85, 105)
                },
                {
                    'name': 'Shogun Musket',
                    'attack': random.randint(285, 320),
                    'hp': 465,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(1, 5),
                    'dodge': random.randint(1, 5),
                    'block': random.randint(35, 65)
                }
            ]
            return random.choice(npcs)
        
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = User(user_id)
    return users[user_id]

async def update_hp_message(embed_message, ctx, max_hp, cursor, db):
    user_id = ctx.author.id
    cursor.execute(f"SELECT hp FROM stats WHERE user_id = ?", (user_id,))
    hp = cursor.fetchone()[0]
    current_hp = hp
    while current_hp < max_hp:
        current_hp += 10
        if current_hp > max_hp:
            current_hp = max_hp
        embed1 = Embed(title=f"HEALTH REGENERATION", description=f"**<:health20:1249262232227938316> Your HP:** `{current_hp}/{max_hp}`", colour=nextcord.Color.random())
        await embed_message.edit(embed=embed1)
        # Perbarui nilai HP di database
        cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (current_hp, user_id))
        await asyncio.sleep(1)  # Tunggu 1 detik sebelum mengupdate pesan

    embed2 = Embed(title=f"HEALTH REGENERATION", description=f"**<a:swords:1250358353818030093> Your HP already full, ready set for battle again!**", colour=nextcord.Color.random())
    await embed_message.edit(embed=embed2)
    db.commit()  # Komit transaksi setelah loop selesai

class Campaign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hp_regeneration_task = None

    def calculate_damage(self, attacker_stats, defender_stats):
        base_damage = attacker_stats['attack'] - defender_stats['block']
        base_damage = max(base_damage, 0)

        critical_hit = False
        burn_applied = False
        poison_applied = False
        lifesteal_amount = 0

        if random.random() < (attacker_stats['crit'] / 100):
            base_damage *= 2
            critical_hit = True
        
        if random.random() < (attacker_stats['burn_dmg'] / 100):
            base_damage *= 1.5
            burn_applied = True

        if random.random() < (attacker_stats['poison_dmg'] / 100):
            base_damage *= 1.5
            poison_applied = True

        lifesteal_amount = base_damage * (attacker_stats['lifesteal'] / 100)
        if random.random() < (attacker_stats['lifesteal'] / 100):
            attacker_stats['hp'] += lifesteal_amount

        dodge_chance = defender_stats['dodge'] / 100
        if random.random() < dodge_chance:
            base_damage = 0
            dodge_applied = True
        else:
            dodge_applied = False

        return base_damage, critical_hit, burn_applied, lifesteal_amount, poison_applied, dodge_applied

    @commands.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def fight(self, ctx):

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT attack, hp, posture, poison_dmg, burn_dmg, lifesteal, crit, dodge, block, maxhp FROM stats WHERE user_id = {ctx.author.id}")
        stats = cursor.fetchone()
        
        if stats is None:
            await ctx.send("You do not have stats available.")
            return

        challenger_stats = {
            'attack': stats[0],
            'hp': stats[1],
            'posture': stats[2],
            'poison_dmg': stats[3],
            'burn_dmg': stats[4],
            'lifesteal': stats[5],
            'crit': stats[6],
            'dodge': stats[7],
            'block': stats[8],
            'maxhp': stats[9]
        }

        user = get_user(ctx.author.id)

        if random.random() < 0.2 or user.inventory['sacred_scroll'] > 0:
            user.inventory['sacred_scroll'] += 1
            await ctx.send("`You found and have a Sacred Scroll! You will fight the boss Saito Nobumasa or Hironi Musashi. Prepare!`")
            enemy_stats = User.get_npc_stats(has_sacred_scroll=True)
            user.inventory['sacred_scroll'] -= 1
        else:
            await ctx.send("`You did not get a Sacred Scroll. Try next time`")
            enemy_stats = User.get_npc_stats()

        view = Button1(challenger_stats, enemy_stats, self.calculate_damage, ctx.author.id)

        if random.random() < 0.2:
            embed = nextcord.Embed(title=f"<a:swords:1250358353818030093> You Found a General {enemy_stats['name']}! He is very strong, be careful!", color=nextcord.Color.blue())
            embed.add_field(name=f"<:health20:1249262232227938316> Your HP: ", value=f"<:health20:1249262232227938316> `{challenger_stats['hp']}` **HEALTH POINT**", inline=True)
            embed.add_field(name=f"<:health20:1249262232227938316> {enemy_stats['name']} HP: ", value=f"<:health20:1249262232227938316> `{enemy_stats['hp']}` **HEALTH POINT**", inline=True)
            embed.set_footer(text=f"⚔️ DEFEAT HIM TO GET 200 EXP! and 5 Talent Point and 300 Jade and 20 Honor Point! With 3500 Coin!")
            embed.timestamp = datetime.datetime.now()
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f"<a:swords:1250358353818030093> You found {enemy_stats['name']}! Defeat him to get exp!", color=nextcord.Color.blue())
            embed.add_field(name=f"<:health20:1249262232227938316> Your HP: ", value=f"<:health20:1249262232227938316> `{challenger_stats['hp']}` **HEALTH POINT**", inline=True)
            embed.add_field(name=f"<:health20:1249262232227938316> {enemy_stats['name']} HP: ", value=f"<:health20:1249262232227938316> `{enemy_stats['hp']}` **HEALTH POINT**", inline=True)
            embed.set_footer(text=f"⚔️ DEFEAT HIM TO GET {exp_amount} EXP! and 1 Talent Point and {jade_amount} Jade and {honor_amount} Honor Point! With {coin_amount} Coin!")
            embed.timestamp = datetime.datetime.now()
            await ctx.send(embed=embed, view=view)
        db.close()

    @commands.command()
    async def start_regeneration(self, ctx):        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        user_id = ctx.author.id
        cursor.execute("SELECT maxhp FROM stats WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
           max_hp = row[0]  # Maksimum HP yang diizinkan
           embed = Embed(title=f"HEALTH REGENERATION", description="**Starting HP regeneration...**", colour=nextcord.Color.random())
           embed_message = await ctx.reply(embed=embed)
           await update_hp_message(embed_message, ctx, max_hp, cursor, db)
        else:
           await ctx.send("User data not found.")

        cursor.close()
        db.close()

    @fight.error
    async def fight_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = Embed(description="**You can use @Ronin fight command in 25 second again!**")
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)

class Button1(nextcord.ui.View):
    def __init__(self, challenger_stats, npc_stats, calculate_damage, user_id):
        super().__init__()
        self.challenger_stats = challenger_stats
        self.npc_stats = npc_stats
        self.calculate_damage = calculate_damage
        self.user_id = user_id
        self.max_damage = self.challenger_stats['attack']
        self.npc_poison_counter = 0
        self.npc_burn_counter = 0
        self.enemy_stats = User.get_npc_stats()

    @nextcord.ui.button(label="Attack", style=nextcord.ButtonStyle.red, emoji="⚔️")
    async def attack_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("**🎲 You are not allowed to use this button 🏴**", ephemeral=True)
            return

        challenger_hp = self.challenger_stats['hp']
        npc_hp = self.npc_stats['hp']
        enemy_stats = User.get_npc_stats()

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT maxhp FROM stats WHERE user_id = {self.user_id}")
        maxhp = cursor.fetchone()[0]

        cursor.execute("SELECT honor FROM clan WHERE member_ids LIKE ?", (f'%{self.user_id}%',))
        clans = cursor.fetchone()
        
        if not clans:
            await interaction.response.send_message("**YOU DONT HAVE A CLAN SO YOU CANT GET THE HONOR REWARD**", ephemeral=True)
            return
        
        honor = clans[0]

        cursor.execute(f"SELECT exp, talent FROM level WHERE user_id = {self.user_id}")
        stats3 = cursor.fetchone()
        try:
           exp = stats3[0]
           talent = stats3[1]
        except:
            await interaction.response.send_message("HELLO")

        cursor.execute(f"SELECT jade, coin FROM jewelry2 WHERE user_id = {self.user_id}")
        jewel = cursor.fetchone()
        try:
           jade = jewel[0]
           coin = jewel[1]
        except:
            await interaction.send("AHH")

        damage_to_npc = random.randrange(self.challenger_stats['attack'])

        damage_to_npc, crit_hit, burn_applied, lifesteal_amount, poison_applied, dodge_applied = self.calculate_damage(self.challenger_stats, self.npc_stats)
        npc_hp -= damage_to_npc
        npc_hp = max(npc_hp, 0)  # Ensure NPC HP is not negative

        message = f"**<a:soulair:1250094797423775816> You dealt** `{damage_to_npc}` **damage to the** `{self.npc_stats['name']}`"
        if crit_hit:
            message += "\n\n<a:Soul1:1250102286311493674> **BUFF :** **<:emoji_36:1250080702146285579> Critical Hit!**"
        elif burn_applied:
            self.npc_burn_counter = 3
            message += "\n\n<a:Soul1:1250102286311493674> **BUFF :** **<:emoji_50:1250081338040782940> Burn Damage applied! Increased damage by 1.5x.**"
        elif poison_applied:
            self.npc_poison_counter = 3
            message += "\n\n<a:Soul1:1250102286311493674> **BUFF :** **<:emoji_40:1250080830080942213> Poison Damage applied! Increased damage by 1.5x.**"
        elif dodge_applied:
            message += "\n\n**⚔️ The NPC dodged your attack! No damage dealt.**"

        dodge_chance = self.challenger_stats['dodge'] / 100
        if random.random() < dodge_chance:
                damage_to_challenger = 0
                message += "\n\n**⚔️ You dodged the attack! No damage taken.**"

        else:
            if npc_hp > 0:  # Apply lifesteal only if NPC is still alive
                if lifesteal_amount > 0:
                    lifesteal_amount_rounded = round(lifesteal_amount)
                    challenger_hp += lifesteal_amount_rounded
                    message += f"\n\n<a:Soul1:1250102286311493674> **BUFF :** **<:emoji_45:1250081148361506907> Lifesteal activated! Restored** `{lifesteal_amount_rounded}` **HP.**"
                    cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (challenger_hp, self.user_id))
            if challenger_hp > maxhp:
                challenger_hp = maxhp
                cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (challenger_hp - lifesteal_amount_rounded, self.user_id))
        
        if npc_hp <= 0:
            winner = interaction.user
            loser = self.npc_stats['name']
            message += f"\n\n**<a:exp2:1249296823655338046> You defeated** **{self.npc_stats['name']}** **! Now you can get {exp_amount} exp! and 1 Talent Point with {jade_amount} Jade and get {honor_amount} Honor Point too! You can type @Ronin start_regeneration to regenerate your hp**"
            cursor.execute("UPDATE level set exp = ? WHERE user_id = ?", (exp + exp_amount, self.user_id))
            cursor.execute("UPDATE level set talent = ? WHERE user_id = ?", (talent + 1, self.user_id))
            cursor.execute("UPDATE jewelry2 set jade = ? WHERE user_id = ?", (jade + jade_amount, self.user_id))
            cursor.execute("UPDATE jewelry2 set coin = ? WHERE user_id = ?", (coin + coin_amount, self.user_id))
            cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + honor_amount, f'%{self.user_id}%',))
            self.stop()

        else:
            dodge_chance = self.challenger_stats['dodge'] / 100
            if random.random() < dodge_chance:
                damage_to_challenger = 0
                message += "\n\n**⚔️ You dodged the attack! No damage taken.**"
            else:
                damage_to_challenger, _, _, _, _, _ = self.calculate_damage(self.npc_stats, self.challenger_stats)

                challenger_hp -= damage_to_challenger
                challenger_hp = max(challenger_hp, 0)
                message += f"\n\n**<a:exp:1249296269721993258> The {self.npc_stats['name']} dealt `{damage_to_challenger}` damage to you.**" # Ensure Challenger HP is not negative

            enemy_stats_saito = {
                    'name': '<:saito:1252525845101150279> Saito Nobumasa - The Best Japan Spearman',
                    'attack': random.randint(560, 645),
                    'hp': 3500,
                    'max_hp': 3500,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(1, 5),
                    'dodge': random.randint(1, 5),
                    'block': random.randint(100, 150),
                    'skills': [
                        {
                            'name': 'Triple Blood Lance',
                            'damage': 450,
                            'rate': 0.6,
                            'buff': {
                                'name': 'Cruel',
                                'damage_increase': 100
                            }
                        },
                        {
                            'name': 'Blood Spear',
                            'damage': 700,
                            'rate': 0.4,
                            'multiplier': 2,
                            'rate_skill': 0.3
                        }
                    ],
                    'passive': {
                        'name': 'Ironheart of Spear',
                        'hp_threshold': 0.5,  # 50% HP threshold
                        'attack_boost': 0.3  # 25% HP heal
                    }
                }
            
            enemy_stats_hironi = {
                    'name': '<:hironi:1252525784384409600> Elite Samurai - Hirano Masanori',
                    'attack': random.randint(745, 870),
                    'hp': 5000,
                    'max_hp': 5000,
                    'posture': 5,
                    'poison_dmg': 0,
                    'burn_dmg': 0,
                    'lifesteal': 0,
                    'crit': random.randint(5, 10),
                    'dodge': random.randint(5, 10),
                    'block': random.randint(200, 300),
                    'skills': [
                        {
                            'name': 'Fury of Katana',
                            'damage': 900,
                            'rate': 0.5,
                            'bonus_damage': 1.0  # 100% of base damage
                        },
                        {
                            'name': 'Fast Bleeding Slash',
                            'damage': 2200,
                            'rate': 0.3,
                            'bleed': {
                                'damage_percent': 0.05,  # 5% HP per round
                                'rounds': 3
                            }
                        }
                    ],
                    'passive': {
                        'name': 'Samurai Resilience',
                        'hp_threshold': 0.25,  # 25% HP threshold
                        'defense_boost': 0.5  # 50% defense boost
                    }
                }
                # Kode dibawah

            if self.npc_stats['name'] == "<:saito:1252525845101150279> Saito Nobumasa - The Best Japan Spearman":
                if 'passive' in enemy_stats_saito and enemy_stats_saito['hp'] <= (enemy_stats_saito['max_hp'] * enemy_stats_saito['passive']['hp_threshold']):
                    message += "\n\n<a:swords:1250358353818030093> **Saito Nobumasa activates Ironheart of Spear! His attack increases by 30% Due to low HP!**"
                    enemy_stats_saito['attack'] += enemy_stats_saito['attack'] * enemy_stats_saito['passive']['attack_boost']

                elif random.random() < 0.6 and enemy_stats_saito is not None and 'skills' in enemy_stats_saito:
                    # Skill: Triple Blood Lance
                    damage = enemy_stats_saito['skills'][0]['damage']
                    message += f"\n\n**<a:exp2:1249296823655338046> {enemy_stats_saito['name']} uses {enemy_stats_saito['skills'][0]['name']} and deals {damage} damage!**"
                    challenger_hp -= damage
                    # Apply buff "Cruel"
                    self.challenger_stats['attack'] += enemy_stats_saito['skills'][0]['buff']['damage_increase']
                    message += f"\n\n**<a:soulair:1250094797423775816> {enemy_stats_saito['skills'][0]['buff']['name']} is applied to {enemy_stats_saito['name']}. {enemy_stats_saito['name']}'s attack has increased by** `{enemy_stats_saito['skills'][0]['buff']['damage_increase']}!`"

                elif random.random() < 0.3 and enemy_stats_saito is not None and 'skills' in enemy_stats_saito:
                    # Skill: Blood Spear
                    if random.random() < enemy_stats_saito['skills'][1]['rate_skill']:
                        damage = enemy_stats_saito['skills'][1]['damage'] * enemy_stats_saito['skills'][1]['multiplier']
                    else:
                        damage = enemy_stats_saito['skills'][1]['damage']
                    message += f"\n\n**{enemy_stats_saito['name']} uses {enemy_stats_saito['skills'][1]['name']} and deals {damage} damage!**"
                    challenger_hp -= damage
                    cursor.execute("UPDATE level set exp = ? WHERE user_id = ?", (exp + 200, self.user_id))
                    cursor.execute("UPDATE level set talent = ? WHERE user_id = ?", (talent + 5, self.user_id))
                    cursor.execute("UPDATE jewelry2 set jade = ? WHERE user_id = ?", (jade + 300, self.user_id))
                    cursor.execute("UPDATE jewelry2 set coin = ? WHERE user_id = ?", (coin + 3500, self.user_id))
                    cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + 20, f'%{self.user_id}%',))
                    db.commit()
                    pass
                    
            # Kode untuk NPC Hironi Musashi
            elif self.npc_stats['name'] == "<:hironi:1252525784384409600> Elite Samurai - Hirano Masanori":
                if 'passive' in enemy_stats_hironi and enemy_stats_hironi['hp'] <= (enemy_stats_hironi['max_hp'] * 0.5):
                    message += "\n\n<a:swords:1250358353818030093> **<:hironi:1252525784384409600> Hirano Masanori activates Samurai Resilience! His block damage increases by 30% Due to low HP!**"
                    enemy_stats_hironi['block'] += enemy_stats_hironi['block'] * 0.3

                elif random.random() < enemy_stats_hironi['skills'][0]['rate'] and 'skills' in enemy_stats_hironi:
                    # Skill: Fury of Katana
                    damage = enemy_stats_hironi['skills'][0]['damage'] * enemy_stats_hironi['skills'][0]['bonus_damage']
                    message += f"\n\n**<a:exp2:1249296823655338046> <:hironi:1252525784384409600> Hirano Masanori uses {enemy_stats_hironi['skills'][0]['name']} and deals {damage} damage!**"
                    challenger_hp -= damage
                    # Apply buff "Focused Mind"
                    self.challenger_stats['attack'] += damage * enemy_stats_hironi['skills'][0]['bonus_damage']
                    message += f"\n\n**<a:soulair:1250094797423775816> Focused Mind is applied to <:hironi:1252525784384409600> Hirano Masanori. His attack has increased by** `{damage}`!"

                elif random.random() < enemy_stats_hironi['skills'][1]['rate'] and 'skills' in enemy_stats_hironi:
                    # Skill: Fast Bleeding Slash
                    damage = enemy_stats_hironi['skills'][1]['damage']
                    message += f"\n\n**🏮 <:hironi:1252525784384409600> Hirano Masanori uses {enemy_stats_hironi['skills'][1]['name']} and deals {damage} damage!**"
                    challenger_hp -= damage
                    # Apply bleed effect
                    bleed_damage = self.challenger_stats['max_hp'] * enemy_stats_hironi['skills'][1]['bleed']['damage_percent']
                    rounds = enemy_stats_hironi['skills'][1]['bleed']['rounds']
                    message += f"\n\n**<a:swords:1250358353818030093> You are bleeding from Fast Bleeding Slash. You will take {bleed_damage} damage per round for the next {rounds} rounds!**"
                    # Track bleed damage in the challenger's stats (assuming 'bleed_damage' is a field or property)
                    self.challenger_stats['bleed_damage'] = bleed_damage
                    self.challenger_stats['bleed_rounds'] = rounds

                    cursor.execute("UPDATE level set exp = ? WHERE user_id = ?", (exp + 200, self.user_id))
                    cursor.execute("UPDATE level set talent = ? WHERE user_id = ?", (talent + 5, self.user_id))
                    cursor.execute("UPDATE jewelry2 set jade = ? WHERE user_id = ?", (jade + 300, self.user_id))
                    cursor.execute("UPDATE jewelry2 set coin = ? WHERE user_id = ?", (coin + 3500, self.user_id))
                    cursor.execute("UPDATE clan SET honor = ? WHERE member_ids LIKE ?", (honor + 20, f'%{self.user_id}%',))
                    db.commit()
# Past

        if challenger_hp <= 0:
            winner = self.npc_stats['name']
            loser = interaction.user
            message += f"\n\n**You have been defeated by the** **{self.npc_stats['name']}**, **Try again later!, You can type @Ronin start_regeneration to regenerate your hp**"
            self.stop()

        if self.npc_poison_counter > 0:
            poison_damage = 50  # Example poison damage per turn
            npc_hp -= poison_damage
            npc_hp = max(npc_hp, 0)
            self.npc_poison_counter -= 1
            message += f"\n\n**<:emoji_40:1250080830080942213> Poison Effect :** **{self.npc_stats['name']}** **takes** `{poison_damage}` **poison damage.**"  

        if self.npc_burn_counter > 0:
            burn_damage = 50  # Example poison damage per turn
            npc_hp -= burn_damage
            npc_hp = max(npc_hp, 0)
            self.npc_burn_counter -= 1
            message += f"\n\n**<:emoji_47:1250301691677642772> Flames Effect :** **{self.npc_stats['name']}** **takes** `{burn_damage}` **burn damage.**" 

        self.challenger_stats['hp'] = challenger_hp
        self.npc_stats['hp'] = npc_hp

        embed = nextcord.Embed(title="Battle Continues", color=nextcord.Color.blue())
        
        embed.add_field(name="<:health20:1249262232227938316> Your HP: ", value=f"<:health20:1249262232227938316> `{max(challenger_hp, 0)}` **HEALTH POINT**", inline=True)
        embed.add_field(name=f"<:health20:1249262232227938316> {self.npc_stats['name']} HP: ", value=f"<:health20:1249262232227938316> `{npc_hp}` **HEALTH POINT**", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Battle Log :", value=message, inline=False)
        embed.timestamp = datetime.datetime.now()

        await interaction.response.edit_message(content=None, embed=embed, view=self)
        
        cursor.execute("UPDATE stats SET hp = ? WHERE user_id = ?", (max(challenger_hp, 0), self.user_id))

        db.commit()
        cursor.close()
        db.close()

    @nextcord.ui.button(label="Retreat", style=nextcord.ButtonStyle.gray, emoji="🏳️")
    async def retreat(self, button: nextcord.ui.Button, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("**🎲 You are not allowed to use this button 🏴.**", ephemeral=True)
            return
        await interaction.message.delete()
        await interaction.response.send_message("**You have retreated 🏳️, if you want fight again make sure if your HP already full again!🛡️ After it you can just fight normally ⚔️**", ephemeral=True)
        self.stop()