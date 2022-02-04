# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

import discord
import random
from discord.ext import commands
import requests
import urllib.request
import math
from PIL import Image, ImageDraw, ImageFont
import tempfile
import io
import requests
import numpy
from base_graphics import BaseGraphics

background_color = BaseGraphics.getBackgroundColor()

#Add Perseus API
from perseus.src.perseus import Perseus, PerseusAPIError
api = Perseus()

#Open images
import glob
STAT_IMAGES = {}
for file in glob.glob("resources/images/stat_icons/*.png"):
    STAT_IMAGES[file.split("/")[-1].replace(".png","")] = Image.open(file)

skillBoostDict = {
    'hp' : 0,
    'eva' : 1,
    'evaRate' : 2,
    'zombie' : 3,
    'damageReduction' : 4,
    'luck' : 5,
    'name' : 6,
    'description' : 7,
    'notes' : 8
}

#Structure of return data
#[HP, Eva, Eva Rate, Zombie Amount, damage reduction, skill, notes] (make function to format this)
def skillBoost(hp=0,aa=0,eva=0,evaRate=0,zombie=0,damageReduction=0,luck=0,name="",description="",notes=""):
    return {
        'hp' : hp,
        'eva' : eva,
        'aa' : aa,
        'evasion_rate' : evaRate,
        'zombie' : zombie,
        'damage_reduction' : damageReduction,
        'luk' : luck,
        'name' : name,
        'description' : description,
        'notes' : notes
    }

#createSwitcher
def ehpAmagi(source,time,rld):
    return skillBoost(evaRate=.1,name="Efficacious Planning",description="While alive in fleet, reduces Burn damage taken by the Main Fleet by 5% (15%) and increases their Evasion Rate by 4% (10%).")
def ehpAzuma(source,time,rld):
    time = max(time,1)
    totalEVABoost = 0
    for i in range(1,time):
        if time % 20 <= 12 and time >= 20:
            totalEVABoost+=.2*.7
    return skillBoost(eva=totalEVABoost/time,name="Mizuho's Intuition",description="Every 20 seconds: 30% (70%) chance to increase own Evasion by 10% (20%) and Accuracy by 20% (50%) for 12 seconds.")
def ehpBaltimore(source,time,rld):
    return skillBoost(name="Adaptive Tactics", aa=.7)
def ehpBremerton(source,time,rld):
    damReduc = 0
    try:
        damReduc =(min(30/time,1)*1.2 +(1-(min(30/time,1))))
    except:
        damReduc = 1.2
    return skillBoost(damageReduction=damReduc-1,name="One for the Team",description="At the start of the battle, if this ship is in the frontmost position of your Vanguard: decreases this ship's DMG taken by 5.0% (20.0%) for 30s If not in this position, increases this ship's AA by 15.0% (25.0%) until the end of the battle.")
def ehpCheshire(source,time,rld):
    return skillBoost(eva=.15,damageReduction=.15,name="Grin and Fire! and Bounce Right Back",notes="Bounce Right Back is assumed to be at max level.")
def ehpDrake(source,time,rld):
    hpBoost = 0.0284131968948*math.floor(time/20)
    return skillBoost(eva=.15,zombie=hpBoost,name="Flintlock Burst",notes="Sortied as lead vanguard. Barrage is assumed to have 100% accuracy")
def ehpDuca(source,time,rld):
    per = 0
    try:
        per =(min(60/time,1)*1.15 +(1-(min(60/time,1))))
    except:
        per = 1.15
    return skillBoost(eva=per-1,aa=per-1,zombie=.09,damageReduction=(.2 if source == 'AP' else 0),name="Halo of Flames and Solemn Zealotry (Lead vanguard DR not included)")
def ehpFriedrich(source,time,rld):
    return skillBoost(damageReduction=.1,name="Rhapsody of Darkness")
def ehpGrafZeppelin(source,time,rld):
    return skillBoost(damageReduction=.15,name="Iron Blood Wings")
def ehpHelena(source,time,rld):
    return skillBoost(name="Radar Scan Plus")
def ehpJintsuu(source,time,rld):
    return skillBoost(damageReduction=.2,name="The Unyielding Jintsuu")
def ehpMinneapolis(source,time,rld):
    return skillBoost(zombie=.2,name="Dullahan")
def ehpMogami(source,time,rld):
    return skillBoost(damageReduction=(.2 if source == 'AP' else 0),name=("AP Protection" if source == 'AP' else -1))
def ehpNingHai(source,time,rld):
    return skillBoost(evaRate=.3,damageReduction=.2,name="Dragon Empery Bond",description="When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).",notes="This is skill is Yat Sen's.")
def ehpNoshiro(source,time,rld):
    return skillBoost(evaRate=.15,name="Noshiro's Hoarfrost")
def ehpPhoenix(source,time,rld):
    return skillBoost(zombie=.25,name="Red Phoenix",description="When Health falls under 20%, heals 15% (25%) of max Health and increase own Firepower by 30% for 15 seconds. Can only occur once per battle.")
def ehpPingHai(source,time,rld):
    return skillBoost(evaRate=.3,damageReduction=.2,name="Dragon Empery Bond",description="When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).",notes="This is skill is Yat Sen's.")
def ehpPola(source,time,rld):
    try:
        actualEVA = 1 * (min(45/time,1)*1.15 +(1-(min(45/time,1))))
    except:
        actualEVA = 1
    return skillBoost(eva=actualEVA-1,damageReduction=6,name="Audacious Challenger")
def ehpPrinzHeinrich(source,time,rld):
    return skillBoost(eva=.15,name="Heinrich's Hunch Punch")
def ehpSanrui(source,time,rld):
    try:
        actualEVA = 1 * (min(50/time,1)*1.35 +(1-(min(50/time,1))))
    except:
        actualEVA = 1
    return skillBoost(eva=actualEVA-1,name="Engine Boost")
def ehpSanDiego(source,time,rld):
    return skillBoost(name="Sparkling Battle Star!", aa=.25)
def ehpSeattle(source,time,rld):
    return skillBoost(damageReduction=.15,name="Dual Nock")
def ehpShinano(source,time,rld):
    return skillBoost(damageReduction=(.2 if source != 'Torpedo' else 0),name=("Protector of the New Moon" if source != 'Torpedo' else -1))
def ehpSuzutsuki(source,time,rld):
    #calculate average evasion rate
    time = max(time,1)
    totalEVABoost = 0
    for i in range(1,time):
        if i <= 3:
            pass
        elif i <= 8:
            totalEVABoost+=.4
        elif i-8 % 15 <= 5:
            totalEVABoost+=.4*.3
    return skillBoost(evaRate=totalEVABoost/time,zombie=.15,name="Suzutsuki, Causing Confusion!")
def ehpTakatoClass(source,time,rld):
    AoAProcTime = rld*4
    try:
        evaRate = 1 * (min(AoAProcTime/time,1) + (1-(min(AoAProcTime/time,1)))*1.1)
    except:
        evaRate = 1
    return skillBoost(evaRate=evaRate-1,name="All out Assualt")
def ehpYatSen(source,time,rld):
    return skillBoost(evaRate=.3,damageReduction=.2,name="Dragon Empery Bond",description="When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).")
def ehpYukikaze(source,time,rld):
    return skillBoost(damageReduction=.25,name="The Unsinkable Lucky Ship")

skillSwitch = {
    'Amagi' : ehpAmagi,
    'Atago' :ehpTakatoClass,
    'Azuma' : ehpAzuma,
    'Baltimore' : ehpBaltimore,
    'Bremerton' : ehpBremerton,
    'Choukai' :ehpTakatoClass,
    'Cheshire' : ehpCheshire,
    'Drake' : ehpDrake,
    'Duca degli Abruzzi' : ehpDuca,
    'Friedrich der Große' : ehpFriedrich,
    'Jintsuu' : ehpJintsuu,
    'Maya' :ehpTakatoClass,
    'Minneapolis' : ehpMinneapolis,
    'Mogami' : ehpMogami,
    'Ning Hai' : ehpNingHai,
    'Noshiro' : ehpNoshiro,
    'Phoenix' : ehpPhoenix,
    'Ping Hai' : ehpPingHai,
    'Prinz Heinrich' : ehpPrinzHeinrich,
    'Saint Louis' : ehpSanrui,
    'San Diego': ehpSanDiego,
    'Seattle' : ehpSeattle,
    'Shinano' : ehpShinano,
    'Suzutsuki' : ehpSuzutsuki,
    'Takao' :ehpTakatoClass,
    'Yat Sen' : ehpYatSen,
    'Yukikaze' : ehpYukikaze
}

class ShipDoesNotExistError(ValueError):
    def __init__(self, name: str) -> None:
        self.name = name.strip()
        super().__init__()

#multiline text function
def text_wrap(text, font, max_width):
        """Wrap text base on specified width.
        This is to enable text of width more than the image width to be display
        nicely.
        @params:
            text: str
                text to wrap
            font: obj
                font of the text
            max_width: int
                width to split the text with
        @return
            lines: list[str]
                list of sub-strings
        """
        lines = []

        # If the text width is smaller than the image width, then no need to split
        # just add it to the line list and return
        if font.getsize(text)[0]  <= max_width:
            lines.append(text)
        else:
            #split the line by spaces to get words
            words = text.split(' ')
            i = 0
            # append every word to a line while its width is shorter than the image width
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i]+ " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines


help_menu_desc = """
Parameters are used by writing the parameter name followed by a number. 
Ex. `;ehp Perseus aa25 %aa25 time60`
Ex. `;ehp illustrious muse evar15 dr5 aa10`
Ex. `;ehp Howe he`

Player Ship Stat Boost Parameters:
`luk`,`hp`,`eva`,`rld`,`aa`
These params can be stared with a `%` or `p` to change a constant stat boost to a percent stat boost.

Other Parameters:
`ehit` - enemy hit
`eluk` - enemy luck 
`time`
`evar` - evasion rate
`dr` - damage reduction
`+13` - equipment is +13
`pvp`
`level`
`tryhard` - enables PvP and +13 equips

Ammo Type Presets:
`HE`, `AP`, `AVI`, `Torp`, `Crash` (crash damage)

Custom Ammo Types
`[AMMO TYPE/Lght Modifier/Medium Modifier/Heavy Modifier]`
Ex. `;ehp cheshire [AP/50/90/70]`
Ex. `;ehp sirius [HE/140/70/30]`
"""

#create class
class ehpCalculator(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    #Main function
    @commands.command()
    async def ehp(self, message, *args):
        try:
            if (args[0] == 'help'):
                embed = discord.Embed(title = "EHP Help Menu")
                embed.add_field(name =":small_red_triangle: ehp [ship name] [args]", value =
                """
`ship name` - The ship that you want to calculate the eHP of""", inline = False)
                embed.add_field(name =":small_red_triangle: Parameters", value =help_menu_desc, inline = False)



                await message.channel.send(embed = embed)
            else:
                ##List of regular/percent params

                args = list(args)

                params = {
                    "player_stat_params" : [
                        "luk",
                        "hp",
                        "eva",
                        "rld",
                        "aa"
                    ],

                    "constants" : [
                        "ehit",
                        "eluck",
                        "time",
                        "level",
                        "limit_break"
                    ],

                    "percent_only_params" : [
                        "evar", #evasion rate
                        "dr" #damage reduction
                    ],

                    "damage_presets" : [
                        "ap",
                        "he",
                        "avi",
                        "torp",
                        "crash"
                    ],

                    "boolean_params" : [
                        "plusthirteen",
                        "tryhard",
                        "siren",
                        "oath",
                        "pvp",
                        "no_retro",
                        "no_skill"
                    ]
                }

                constants = {
                    "ehit" : 75,
                    "eluck" : 25,
                    "time" : 60,
                    "level" : 120,
                    "limit_break" : 3
                }

                COMMAND_ALIAS = {
                    "+13" : "plusthirteen",
                    "noretro" : "no_retro",
                    "noskill" : "no_skill",
                    "torp" : "trp",
                    "lb" : "limit_break",
                    "mlb" : "lb3"

                }

                def getCommandAlias(param):
                    if param in COMMAND_ALIAS:
                        return COMMAND_ALIAS[param]
                    else:
                        return param

                kwargs = {k:False for k in params["boolean_params"]}

                all_options = [val for key in params for val in params[key]]
                ship_name = ""

                toInt = lambda x: int(''.join((number if number in '1234567890' else "" for number in x)))
                toFloat = lambda x: float(''.join((number if number in '1234567890.' else "" for number in x)))/100

                for count,arg in enumerate(args):
                    arg = getCommandAlias(arg)
                    stripped_arg = ''.join([letter if ord(letter) in range(65,90) or ord(letter) in range(97,122) or letter == "_" else "" for letter in arg.replace("%","")]).lower()
                    stripped_arg = getCommandAlias(stripped_arg)

                    if stripped_arg not in all_options and stripped_arg[1:] not in all_options:
                        ship_name += arg + " "
                    elif stripped_arg in params["constants"]:
                        constants[stripped_arg] = toInt(arg)

                #nicknames
                try:
                    ship = api.Ship(ship_name.strip(),nicknames=True,retrofit=True, level=constants["level"], limit_break=constants["limit_break"])
                except PerseusAPIError:
                    raise ShipDoesNotExistError(name=ship_name)

                #get the needed data
                name = ship.name

                #HE and AP can be made more accurate if the ship is checked to be in the vangaurd or not
                NORMAL_DAMAGE_MODS = 100,80,60,
                AVIATION_DAMAGE_MODS = 80,100,120,
                TORPEDO_DAMAGE_MODS = 80,100,130,
                CRASH_DAMAGE_MODS = 100,100,100,

                damage_modifiers = list(NORMAL_DAMAGE_MODS)
                damage_source = "Normal"

                VANGUARD_SHIPS = ['Destroyer', 'Light Cruiser', 'Heavy Cruiser', 'Large Cruiser', 'Munition Ship']
                if (ship.hull_type in VANGUARD_SHIPS):
                    AP_DAMAGE_MODS = 110,90,70,
                    HE_DAMAGE_MODS = 135,95,70,
                else:
                    AP_DAMAGE_MODS = 45,130,110
                    HE_DAMAGE_MODS = 140,110,90,

                stats = ship.stats
                stats["damage_reduction"] = 0
                stats["evasion_rate"] = 0

                percent_boosts = {}
                constant_boosts = {}

                for arg in args:
                    arg = getCommandAlias(arg)
                    stripped_arg = ''.join([letter if ord(letter) in range(65,90) or ord(letter) in range(97,122) or letter == "_" else "" for letter in arg.replace("%","")]).lower()

                    if stripped_arg in params["player_stat_params"] or stripped_arg[1:] in params["player_stat_params"]:
                        #% or regular boost
                        if "%" in arg:
                            stats[stripped_arg] *= 1+toFloat("0" + arg)
                            percent_boosts[stripped_arg] = toFloat("0" + arg)
                        elif arg[0] in ["p","P"]:
                            stats[stripped_arg[1:]] *= 1+toFloat("0" + arg)
                            percent_boosts[stripped_arg[1:]] = toFloat("0" + arg)
                        else:
                            stats[stripped_arg] += toInt(arg)
                            constant_boosts[stripped_arg]= toInt(arg)
                    elif stripped_arg in params["percent_only_params"]:
                        if stripped_arg == "evar":
                            stats["evasion_rate"] = toFloat(arg)
                            percent_boosts["evasion_rate"] = toFloat(arg)
                        if stripped_arg == "dr":
                            stats["damage_reduction"] = toFloat(arg)
                            percent_boosts["damage_reduction"] = toFloat(arg)
                    elif "[" in arg and "]" in arg:
                        m = arg.replace('[','').split('/')
                        try:
                            damage_modifiers[0] = int(''.join(x for x in '0'+m[1] if x.isdigit()))
                            damage_modifiers[1] = int(''.join(x for x in '0'+m[2] if x.isdigit()))
                            damage_modifiers[2] = int(''.join(x for x in '0'+m[3] if x.isdigit()))
                            damage_source = 'Normal'
                            if 'he' in m[0].lower():
                                damage_source = 'HE'
                            if 'ap' in m[0].lower():
                                damage_source = 'AP'
                            if 'avi' in m[0].lower():
                                damage_source = 'Aviation'
                            if 'torp' in m[0].lower():
                                damage_source = 'Torpedo'
                            if 'normal' in m[0].lower():
                                damage_source = 'Normal'
                        except:
                            await message.channel.send("The custom armor modifiers are incorrect! Normal modifiers have been used instead.")
                            damage_source = 'Normal'
                            damage_modifiers = NORMAL_DAMAGE_MODS
                    elif stripped_arg in params["damage_presets"]:
                        if stripped_arg == "ap":
                            damage_modifiers = AP_DAMAGE_MODS
                            damage_source = 'AP'
                        if stripped_arg == "he":
                            damage_modifiers = HE_DAMAGE_MODS
                            damage_source = 'HE'
                        if stripped_arg == "avi":
                            damage_modifiers = AVIATION_DAMAGE_MODS
                            damage_source = 'Aviation'
                        if stripped_arg == "torp":
                            damage_modifiers = TORPEDO_DAMAGE_MODS
                            damage_source = 'Torpedo'
                        if stripped_arg == "crash":
                            damage_modifiers = CRASH_DAMAGE_MODS
                            damage_source = 'Crash'
                    elif stripped_arg in params["boolean_params"]:
                        kwargs[stripped_arg] = True
                    else: continue

                if kwargs["tryhard"]:
                    kwargs["pvp"] = True
                    kwargs["plusthirteen"] = True

                #multiply HP by modifiers
                if kwargs["pvp"]:
                    if ship.hull_type in ["Destroyer", "Munition Ship"]:
                        stats["damage_reduction"] = 1 - (1-stats["damage_reduction"]) * (1-.25)

                    elif ship.hull_type == "Light Cruiser":
                        stats["damage_reduction"] = 1 - (1-stats["damage_reduction"]) * (1-.2)

                    elif ship.hull_type in ["Heavy Cruiser", "Large Cruiser"]:
                        stats["damage_reduction"] = 1 - (1-stats["damage_reduction"]) * (1-.15)

                #certain ships need retro for survivability skill
                NEED_RETRO = [
                    "Jintsuu"
                ]


                def getSkillBoost(ship: api.Ship, time :int,no_skill:bool =False, need_retro: list=NEED_RETRO, no_retro=False, stats :dict = {"rld" : 100} ):
                    name = ship.name
                    if name in skillSwitch and no_skill == False and no_retro == False and (name in need_retro and ship.retrofit or not name in need_retro):
                        func = skillSwitch.get(name, [0,0,0,0,0])
                        return func(damage_source,time,stats["rld"])
                    else:
                        return skillBoost()
                def getZombie(ship: api.Ship,no_skill=False,need_retro=NEED_RETRO,no_retro=False):
                    return getSkillBoost(ship,no_retro=no_retro,no_skill=no_skill,time=1)["zombie"]

                def getIncludedSkill(ship: api.Ship,no_skill=False,need_retro=NEED_RETRO,no_retro=False):
                    res = getSkillBoost(ship,no_retro=no_retro,no_skill=no_skill,time=1)
                    if res["name"] != "":
                        return "Skills included: " + res['name']
                    else:
                        return "No Skill is included."

                def calcEHP(ship: api.Ship, stats: dict, gearX: str,gearY: str, time: int, 
                enemy_luk: int = 0, enemy_hit: int = 0,
                plusthirteen:bool = False, tryhard:bool = False, siren:bool = False, pvp:bool = False, no_retro:bool = False, no_skill:bool = False
                ):
                    stats = stats.copy()

                    #Vangaurd ships need AA from stats accounted for
                    for slot in ship.slot_ids:
                        if 6 in slot: #AA gun ID is 6
                            stats["aa"] += 45

                    skill_stats = getSkillBoost(ship,time=time,stats=stats,no_skill=no_skill,need_retro=NEED_RETRO,no_retro=no_retro)
                    for stat in skill_stats:
                        try:
                            stats[stat] = (1+stats[stat]) * (1+skill_stats[stat]) - 1

                            if stat in ["damage_reduction","evasion_rate"]:
                                if stats[stat] == 0:
                                    stats[stat] = skill_stats[stat]

                        except KeyError:
                            stats[stat] = skill_stats[stat]

                    def isGearName(gearName):
                        return gearX == gearName or gearY == gearName

                    #extra damage reduction
                    if stats["damage_reduction"] != 1:
                        stats["hp"] = stats["hp"] /(1-stats["damage_reduction"])


                    #add siren damage reduction if costal report
                    if (isGearName("Intel_Report_-_Arctic_Stronghold") or isGearName("NY_City_Coast_Recon_Report")) and siren:
                        realHP = stats["hp"]/(1-.06)

                    #switch armor to heavy is the VH armor is used
                    armor_id = ship.armor_id-1
                    if isGearName("VH_Armor_Plating"):
                        if ship.armor_type != 'Heavy':
                            armor_id = 2
                        else:
                            if damage_source in "HE" or damage_source in "Normal" or damage_source in "Normal":
                                stats["hp"] *= (1/(1-.03))
                            elif damage_source in "AP":
                                stats["hp"] *= (1/(1-.06))
                    
                    torpDamageReduc = 0
                    if isGearName("Anti-Torpedo_Bulge") and damage_source == "Torpedo":
                        stats["hp"] *= (1/.7)
                        

                    
                    stats["hp"] *= (100/damage_modifiers[armor_id] if damage_modifiers[armor_id] != 0 else 100)

                    #reduce damage taken by AA stat if AVI
                    if damage_source == 'Aviation' or damage_source == 'Crash':
                        stats["hp"] *= (1+(stats["aa"]/150))

                    pvp_multiplier = 1
                    if pvp:
                        pvp_multiplier = 2.34

                    repair_toolkit_heal_multiplier = 1
                    if isGearName("Repair_Toolkit"):
                        repair_toolkit_heal_multiplier = 1+(math.floor(time/15) * .01)

                    #speical gear interaction with helena
                    if isGearName("SG_Radar") and ship.name == 'Helena':
                        stats["eva"]*=1.1

                    if damage_source != "Crash":
                        #Claculate accuracy
                        acc = 0.1 + (enemy_hit)/(enemy_hit+stats["eva"]+2) + (enemy_luk-stats["luk"]+0)/1000 - stats["evasion_rate"]
                        acc = max(acc,.1)
                        #devide HP by acc to get eHP

                        return round((stats["hp"]*pvp_multiplier*repair_toolkit_heal_multiplier)/acc)
                    else:
                        return round(stats["hp"]*pvp_multiplier*repair_toolkit_heal_multiplier)

                def drawRectangleOutline(draw, coordinates, color, borderColor, width):
                    draw.rectangle((coordinates[0][0],coordinates[1][0],coordinates[0][1],coordinates[1][1]), fill = color)
                    for i in range(width):
                        rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
                        rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
                        draw.rectangle((rect_start[0], rect_end[0],rect_start[1],rect_end[1]), outline = borderColor)

                #image modify function
                def make_image():
                    #Start drawing the text on the image
                    font = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 24)
                    fontSmall = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 20)
                    fontNumbers = ImageFont.truetype("resources/fonts/Lato-Regular.ttf", 20)
                    fontNumbersBold = ImageFont.truetype("resources/fonts/Lato-Bold.ttf", 20)
                    fontNumbersSmall = ImageFont.truetype("resources/fonts/Lato-Regular.ttf", 20)

                    #get the ships armor type
                    DMGInfo = ''
                    if damage_source == "HE":
                        DMGInfo = f'HE ({damage_modifiers[0]}/{damage_modifiers[1]}/{damage_modifiers[2]})'
                    elif damage_source == "AP":
                        DMGInfo = f'AP ({damage_modifiers[0]}/{damage_modifiers[1]}/{damage_modifiers[2]})'
                    elif damage_source == "Aviation":
                        DMGInfo = f'Aviation damage ({damage_modifiers[0]}/{damage_modifiers[1]}/{damage_modifiers[2]})'
                    elif damage_source == "Torpedo":
                        DMGInfo = f'Torpedo damage ({damage_modifiers[0]}/{damage_modifiers[1]}/{damage_modifiers[2]})'
                    elif damage_source == "Normal":
                        DMGInfo = f'Normal Ammo ({damage_modifiers[0]}/{damage_modifiers[1]}/{damage_modifiers[2]})'
                    elif damage_source == "Crash":
                        DMGInfo = 'crash damage'

                    #Name, +10 Stats, +13 Stats
                    gearArr=[
                        ['No_Gear',[0,0,0],[0,0,0]],
                        ['Improved_Hydraulic_Rudder',[60,49,0],[72,49,0]],
                        ['Little_Beaver_Squadron_Tag',[75,35,0],[90,44,0]],
                        ['Pearl_Tears',[500,0,0],[590,0,0]],
                        ['Celestial_Body',[550,0,0],[640,0,0]],
                        ['Cosmic_Kicks',[0,28,0],[0,34,0]],
                        ['SG_Radar',[0,15,0],[0,18,0]],
                        ['High_Performance_Anti-Air_Radar',[0,0,100],[0,0,118]],
                        ['Repair_Toolkit',[500,0,0],[530,0,0]],
                        ['Anti-Torpedo_Bulge',[350,0,0],[371,0,0]],
                        ['Improved_Boiler',[245,0,0],[260,0,0]],
                        ['Fuel_Filter',[350,5,0],[371,6,0]],
                        ['Ocean_Soul_Camouflage',[100,18,0],[110,19,0]],
                        ['NY_City_Coast_Recon_Report',[120,15,0],[130,16,0]],
                        ['Intel_Report_-_Arctic_Stronghold',[180,0,0],[190,0,0]],
                        ['Fire_Extinguisher',[287,0,0],[287,0,0]],
                        ['Naval_Camouflage',[48,19,0],[48,19,0]],
                        ['Hydraulic_Steering_Gear',[48,19,0],[48,19,0]],

                        #['Recon Report',120,15,0,False,0]

                    ]
                    if ship.hull_type in ['Battleship', 'Large Cruiser', 'Battlecruiser', 'Aviation Battleship','Aircraft Carrier']:
                        gearArr.insert(3,['VH_Armor_Plating',[650,0,0],[740,0,0]])
                    if ship.hull_type in ['Aircraft Carrier', 'Light Carrier', 'Aviation Battleship']:
                        gearArr.insert(3,['Steam_Catapult',[75,0,0],[90,0,0]])

                    gearImageSize = 70
                    gearImagePadding = 10
                    spacing = gearImageSize+gearImagePadding
                    xOffset = 10
                    yOffset = 116+20

                    #Create the backround
                    #find grid size so image size can be made in relation to it
                    gridSize = (len(gearArr)+1)*spacing
                    isSpecialTextNeeded = False

                    output = Image.new('RGBA', (xOffset+gridSize+450,yOffset+gridSize+50),color = background_color)
                    draw = ImageDraw.Draw(output)
                    def drawCenteredText(loc,text,fill,font,align):
                        draw.text((loc[0]-font.getsize(text)[0]/2,loc[1]), text, fill=fill, font=font,align=align)

                    # #Get thumbnail image
                    # thumbnail = requests.get(shipData['thumbnail']).content
                    # image_bytes = io.BytesIO(thumbnail)
                    # thumbnailImage = Image.open(image_bytes).convert('RGB')
                    #Draw thumbnail in corner
                    # output.paste(thumbnailImage,(10,10))
                    #Draw backround rectangle
                    drawRectangleOutline(draw,((xOffset,xOffset+gridSize-10),(20,100)),BaseGraphics.getDarkHighlightColor(),'rgb(0,0,0)',3)
                    #Draw header text
                    lineSpacing = 25
                    drawCenteredText((xOffset+gridSize/2, 33),f"{ship.name+(' Kai' if ship.retrofit else '')}'s eHP vs {DMGInfo} in {'Exercises.' if kwargs['pvp'] else 'PvE.'}",(255,255,255),font,"center")
                    drawCenteredText((xOffset+gridSize/2, 33+25),f"Enemy Hit: {constants['ehit']} | Enemy Luck: {constants['eluck']} | Battle Duration: {constants['time']}s",(255,255,255),font,"center")


                    #Draw gear pictures
                    for i in range(1,len(gearArr)+1):
#                        draw.text((xOffset+(i+1)*spacing, yOffset),gearArr[i][0],(255,255,255),font=fontSmall)
                        gearImage = Image.open(f"resources/images/Gear/{gearArr[i-1][0]}.png").resize((70,70))

                        output.paste(gearImage,(xOffset+spacing*i,yOffset))
                        output.paste(gearImage,(xOffset,yOffset+spacing*i))

                    #calculate eHP amoutns
                    eHPArray = []
                    zombiePercent = getZombie(ship,no_skill=kwargs["no_skill"],no_retro=kwargs["no_retro"])
                    for i in range(len(gearArr)):
                        eHPArray.append([])
                        for j in range(len(gearArr)):
                            eHPArray[i].append(0)
                    for i in range(len(gearArr)):
                        for j in range(len(gearArr)):
                            #Bypass dual gear
                            bypassDualGear = ['Improved_Hydraulic_Rudder', 'Little_Beaver_Squadron_Tag', 'VH VH_Armor_Plating', 'Pearl_Tears', 'Cosmic_Kicks', 'Naval_Camouflage', "Celestial Body"]
                            if gearArr[i][0] in bypassDualGear and gearArr[i][0] == gearArr[j][0]:
                                eHPArray[i][j] = 'N/A'
                            else:
                                gearLevel = 1
                                if kwargs["plusthirteen"]:
                                    gearLevel=2
                                tempStats = stats.copy()
                                tempStats["hp"] += gearArr[i][gearLevel][0] + gearArr[j][gearLevel][0]
                                tempStats["eva"] += gearArr[i][gearLevel][1] + gearArr[j][gearLevel][1]
                                tempStats["aa"] += gearArr[i][gearLevel][2] + gearArr[j][gearLevel][2]


                                eHPArray[i][j] = calcEHP(
                                    ship,
                                    tempStats,
                                    gearArr[i][0],
                                    gearArr[j][0],

                                    no_skill=kwargs["no_skill"],
                                    no_retro=kwargs["no_retro"],

                                    pvp=kwargs["pvp"],

                                    time=constants['time'],
                                    enemy_luk=constants["eluck"],
                                    enemy_hit=constants["ehit"]
                                    )

                    #Draw HP amounts
                    maxeHP = max(max(0 if isinstance(i, str) else i for i in x) for x in eHPArray)
                    mineHP = min(min(100000 if isinstance(i, str) else i for i in x) for x in eHPArray)
                    for i in range(len(gearArr)):
                        for j in range(len(gearArr)):
                            f = fontNumbers
                            if isinstance(eHPArray[i][j], str):
                                ehp = eHPArray[i][j]
                            else:
                                ehp = eHPArray[i][j]
                                zombieAmount = str(round(ehp*zombiePercent))
                                #draw Zombie text:
                                color = (200,200,200)
                                ehp = str(ehp)
                                tSize = font.getsize(ehp)
                                textOffset = 0
                                if zombiePercent != 0:
                                    #get text size to calculate offset
                                    zombieText = "+"+zombieAmount
                                    zw, zh = draw.textsize(zombieText)
                                    draw.text((xOffset+(i+1)*spacing+(gearImageSize-tSize[0]+5)/2, yOffset+(j+1)*spacing+gearImageSize/2),zombieText,color,font=fontNumbersSmall)
                                    textOffset = tSize[1]/-2

                            color = (255,255,255)
                            if ehp == str(mineHP):
                                color = (240,125,125)
                                f = fontNumbersBold
                            elif ehp == str(maxeHP):
                                f = fontNumbersBold
                                color = (150,220,150)
                            elif maxeHP*.95 < float(''.join(x for x in '0'+ehp if x.isdigit())):
                                f = fontNumbersBold
                                color = (21,158,57)
                            #i have no idea why i need the 5 to center it. I've been debugging for an hour so im done with this.
                            draw.text((xOffset+(i+1)*spacing+(gearImageSize-tSize[0]+5)/2, yOffset+(j+1)*spacing+gearImageSize/2-tSize[1]/2+ textOffset),ehp,color,font=f)

                    #Draw backround rectangle
                    #https://stackoverflow.com/questions/39017018/how-to-join-two-list-of-tuples-without-duplicates
                    skill_boosts = getSkillBoost(ship=ship,stats = stats, time = constants["time"],no_skill=kwargs["no_skill"], need_retro=NEED_RETRO)
                    all_tuples = tuple(val for val in tuple(skill_boosts.keys()) if skill_boosts[val] != 0 and val not in ("description","name","notes"))
                    all_tuples += tuple(constant_boosts.keys())
                    all_tuples += tuple(percent_boosts.keys())
                    stats_to_draw_in_corner = []
                    [stats_to_draw_in_corner.append(x) for x in all_tuples if x not in stats_to_draw_in_corner]

                    PARAM_Y_SPACING = 80

                    box_height = max(630+80,80+PARAM_Y_SPACING*len(stats_to_draw_in_corner))

                    drawRectangleOutline(draw,((xOffset+gridSize+20,xOffset+gridSize+430),(20,box_height)),BaseGraphics.getDarkHighlightColor(),'rgb(0,0,0)',3)

                    #Draw skills
                    lines = text_wrap(str(getIncludedSkill(ship,no_skill=kwargs["no_skill"],no_retro=kwargs["no_retro"])),font,380)
                    color = 'rgb(255,255,255)'
                    x = xOffset+gridSize+20
                    y = 33
                    for line in lines:
                        drawCenteredText((x+10+192,y), line, fill=color, font=font,align="left")
                        y = y + 30    # update y-axis for new line

                    y = yOffset
                    draw.text(tuple([65+x+380/2-font.getsize("Stat Params")[0]/2,y]), "Stat Params", fill=color, font=font,align="cener")
                    y+=lineSpacing
                    #Draw catagory text
                    skillCenter = 380/2-80+65
                    extraCenter = 380/2+110+30
                    draw.text((x+skillCenter-font.getsize("Skills")[0]/2,y+10), "Skills", fill=color, font=font,align="left")
                    draw.text((x+extraCenter-font.getsize("Extra")[0]/2,y+10), "Extra", fill=color, font=font,align="left")

                    def roundToPlaceValue(n,p):
                        p=pow(10,p+1)
                        return str(round(n*p)/p)

                    y+=70
                    
                    def drawParam(name,x,y):
                        draw_name = name
                        draw_name = draw_name.replace("damage_reduction","dr").replace("evasion_rate","evar")
                        drawCenteredText((x+50,y), str(draw_name), fill=color, font=font,align="left")
                        
                        if name in tuple(skill_boosts.keys()):
                            if skill_boosts[name] != 0:
                                drawCenteredText((x+skillCenter,y), roundToPlaceValue(skill_boosts[name]*100,2)+"%", fill=color, font=font,align="left")

                        boost_text = ""
                        if name in tuple(percent_boosts.keys()):
                            boost_text += roundToPlaceValue(percent_boosts[name]*100,2)+"%"
                        if name in tuple(constant_boosts.keys()):
                            if boost_text != "":
                                boost_text += "+"
                            boost_text+=roundToPlaceValue(constant_boosts[name],2)

                        if boost_text != "":
                            drawCenteredText((x+extraCenter,y), boost_text, fill=color, font=font,align="left")

                    for name in stats_to_draw_in_corner:
                        drawParam(name,x,y)
                        y+=PARAM_Y_SPACING


                    #Draw warning
                    #warning text
                    warning = """This is not not an accurate representation of this ship's eHP in PvE.""" if kwargs["pvp"] else """Use argument "PvP" to switch to PvP mode."""
                    #Gun Reload
                    # if (noSkill == False and (name in ["Takao", "Atago", "Choukai", "Maya"])):
                    #     draw.text((x+10,y), "Main Gun\nReload", fill=color, font=font,align="left")
                    #     drawCenteredText((x+skillCenter,y), "N/A", fill=color, font=font,align="left")
                    #     drawCenteredText((x+extraCenter,y), str(rld)+"s", fill=color, font=font, align="left")
                    #     warning += ' Reload does not account for Absolute Cooldown, Volley Time, or Reload Stat.'
                    #     y+=80
                    # warning += " "
                    warning += "Use Argument '+13' to switch to +13 equips." if kwargs["plusthirteen"] == False else "Equipment is +13."
                    draw.text((xOffset,yOffset+gridSize+10), warning,(255,255,255),font=font)

                    return output

                imCat = make_image()

                with imCat as img:
                    #upload to discord
                    with io.BytesIO() as image_binary:
                        img.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        file = discord.File(fp=image_binary,filename='eHPCalc.png')
                        #embedVar = discord.Embed(title=f"{shipName.title()}'s eHP",filename='eHPCalc.png')
                        imageURL = "attachment://eHPCalc.png"
                        #embedVar.set_image(url=imageURL)
                        img.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await message.channel.send(file=file)



        except ShipDoesNotExistError as e:
            await message.channel.send(f"{e.name.title()} is not a ship! Please try again.")
        except Exception as e:
            await message.channel.send(f"Something went wrong! Please try again.")
            raise e









#set this up with cogs and pray it works
def setup(client):
    client.add_cog(ehpCalculator(client))
