import discord
import random
from discord.ext import commands
from azurlane.azurapi import AzurAPI
import requests
import urllib.request
from shipGirlNicknameHandler import getNickname
import math
from PIL import Image, ImageDraw, ImageFont
import tempfile
import io
import requests
import numpy


api = AzurAPI()

#Structure of return data
#[HP, Eva, Eva Rate, Zombie Amount, damage reduction, skill, skillDisc, notes] (make function to format this)
#createSwitcher
def ehpAmagi(source,time,rld):
    return [0,0,.1,0,0,"Efficacious Planning","While alive in fleet, reduces Burn damage taken by the Main Fleet by 5% (15%) and increases their Evasion Rate by 4% (10%)."];
def ehpAzuma(source,time,rld):
    time = max(time,1)
    totalEVABoost = 0;
    for i in range(1,time):
        if time % 20 <= 12 and time >= 20:
            totalEVABoost+=.2*.7
    return [0,(totalEVABoost/time),0,0,0,"Mizuho's Intuition","Every 20 seconds: 30% (70%) chance to increase own Evasion by 10% (20%) and Accuracy by 20% (50%) for 12 seconds."];
def ehpBremerton(source,time,rld):
    damReduc = 0;
    try:
        damReduc =(min(30/time,1)*1.2 +(1-(min(30/time,1))));
    except:
        damReduc = 1.2;
    return [0,0,0,0,damReduc-1,"One for the Team","At the start of the battle, if this ship is in the frontmost position of your Vanguard: decreases this ship's DMG taken by 5.0% (20.0%) for 30s; If not in this position, increases this ship's AA by 15.0% (25.0%) until the end of the battle."];
def ehpCheshire(source,time,rld):
    return [0,.15,0,0,.15,"Grin and Fire! and Bounce Right Back","Bounce Right Back is assumed to be at max level."];
def ehpDrake(source,time,rld):
    hpBoost = 0.0284131968948*math.floor(time/20)
    return [0,.15,0,hpBoost,0,"Flintlock Burst","Sortied as lead vanguard. Barrage is assumed to have 100% accuracy"];
def ehpFriedrich(source,time,rld):
    return [0,0,0,0,.1,"Rhapsody of Darkness"];
def ehpGrafZeppelin(source,time,rld):
    return [0,0,0,0,.15,"Iron Blood Wings"];
def ehpJintsuu(source,time,rld):
    return [0,0,0,0,.2,"The Unyielding Jintsuu"];
def ehpMinneapolis(source,time,rld):
    return [0,0,0,.2,0,"Dullahan"];
def ehpMogami(source,time,rld):
    return [0,0,0,0,.2 if source == 'AP' else 0,"AP Protection" if source == 'AP' else -1];
def ehpNingHai(source,time,rld):
    return [0,0,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).","This is skill is Yat Sen's."];
def ehpNoshiro(source,time,rld):
    return [0,0,.15,0,0,"Noshiro's Hoarfrost"];
def ehpPhoenix(source,time,rld):
    return [0,0,0,.25,0,"Red Phoenix","When Health falls under 20%, heals 15% (25%) of max Health and increase own Firepower by 30% for 15 seconds. Can only occur once per battle."];
def ehpPingHai(source,time,rld):
    return [0,0,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).","This is skill is Yat Sen's."];
def ehpPola(source,time,rld):
    try:
        actualEVA = eva * (min(45/time,1)*1.15 +(1-(min(45/time,1))));
    except:
        actualEVA = eva;
    return [0,0,0,0,6,"Audacious Challenger"];
def ehpPrinzHeinrich(source,time,rld):
    return [0,.15,0,0,0,"Heinrich's Hunch Punch"];
def ehpSanrui(source,time,rld):
    try:
        actualEVA = 1 * (min(50/time,1)*1.35 +(1-(min(50/time,1))));
    except:
        actualEVA = 1;
    return [0,actualEVA-1,0,0,0,"Engine Boost"];
def ehpSeattle(source,time,rld):
    return [0,0,0,0,.15,"Dual Nock"];
def ehpShinano(source,time,rld):
    return [0,0,0,0,.2 if source != 'Torpedo' else 0,"Protector of the New Moon" if source != 'Torpedo' else -1];
def ehpSuzutsuki(source,time,rld):
    #calculate average evasion rate
    time = max(time,1)
    totalEVABoost = 0;
    for i in range(1,time):
        if i <= 3:
            pass;
        elif i <= 8:
            totalEVABoost+=.4
        elif i-8 % 15 <= 5:
            totalEVABoost+=.4*.3
    return [0,0,totalEVABoost/time,.15,0,"Suzutsuki, Causing Confusion!"];
def ehpTakatoClass(source,time,rld):
    AoAProcTime = rld*4;
    try:
        evaRate = 1 * (min(AoAProcTime/time,1) + (1-(min(AoAProcTime/time,1)))*1.1);
    except:
        evaRate = 1;
    return [0,0,evaRate-1,0,0,"All out Assualt"];
def ehpYatSen(source,time,rld):
    return [0,0,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%)."];
def ehpYukikaze(source,time,rld):
    return [0,0,0,0,.25,"The Unsinkable Lucky Ship"];

skillSwitch = {
    'Amagi' : ehpAmagi,
    'Atago' :ehpTakatoClass,
    'Azuma' : ehpAzuma,
    'Bremerton' : ehpBremerton,
    'Choukai' :ehpTakatoClass,
    'Drake' : ehpDrake,
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
    'Seattle' : ehpSeattle,
    'Shinano' : ehpShinano,
    'Suzutsuki' : ehpSuzutsuki,
    'Takao' :ehpTakatoClass,
    'Yat Sen' : ehpYatSen,
    'Yukikaze' : ehpYukikaze
}

#Usefull vanguard array
vanguard = ['Destroyer', 'Light Cruiser', 'Heavy Cruiser', 'Large Cruiser', 'Munition Ship']

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
                embed.add_field(name =":small_red_triangle: ;ehp [ship name] [args]", value =
                """
`ship name` - The ship that you want to calculate the eHP in PvE or exercises. Use argument PvP if you want to switch to PvP mode.""", inline = False)
                embed.add_field(name =":small_red_triangle: Args", value =
"""**PvP** = Switches mode to PvP mode.
    **hitN** = Set enemy hit stat to value N.
    **luckN** = set enemy luck to value N.
    **timeN** = Set battle duration stat to value N.
    **hpN** = Add N HP to the ship.
    **evaN** = Add N percent eva to the ship.
    **evaRateN** = Add N percent EVA rate to the ship.
    **drN** = Add N percent damage reduction to the ship.
    **rldN** = Set gun reload to value N.
    **AP** = Change enemy ammo type to AP. 110/90/70 is used for vanguard ships. 45/130/110 is used for backline ships.
    **HE** = Change enemy ammo type to HE. 135/95/70 is used for vanguard ships. 140/110/90 is used for backline ships.
    **avi** = View eHP vs aviation damage. 80/100/120 are used as the modifiers.
    **torp** = View eHP vs tor\*\*\*\* damage. 80/100/130 are used as the modifers.
    **crash** = View eHP vs crash damage.
    **[t/x/y/z]** = View eHP with custom ammo modifiers x/y/z and damage type t.
    **noRetro** = Do not use the retrofit version of this ship""", inline = False)

                embed.add_field(name =":small_red_triangle: Examples", value =
"""`;ehp Akagi` - get Akagi's eHP.
    `;ehp "Graf Zeppelin" hit100` - get Graf Zeppelin's eHP with an enemy hit stat of 100.
    `;ehp "Prinz Eugen" time30 HE` - get Prinz Eugen's eHP with a battle time of 30s seconds vs HE ammo.
    `;ehp Amagi [AP/45/130/115]` - get Amagi's eHP vs custom AP ammo with the modifers 45/130/115.
""", inline = False)



                await message.channel.send(embed = embed);
            else:

                #name
                nameArray = [];
                #damage mods
                AviationDamageMods = [80,100,120];
                TorpedoDamageMods = [80,100,130];
                #set default args
                evaSkill = 0;
                eLck = 50;
                extraHP = 0;
                extraEva = 0;
                extraEvaRate = 0;
                evaMultiplier = 1;
                noSkill = False;
                extraDamReduc = 0;


                PvEMode = True;
                #set to invalid value so it can be checked if a custom value was used
                eHit = -1;
                eLck = -1;
                time = -1;
                damageSource = 'Typeless';
                damageModifiers = [100,80,60];
                retrofit = True;
                rld = 5.0;

                siren = False;

                #get args
                for i in args:
                    if "noskill" in i.lower():
                        noSkill = True;
                    else:
                        iInt = float(''.join(x for x in '0'+i if x.isdigit() or x == "."));
                        stringNumberless = ''.join([j for j in i.lower() if not j.isdigit() and j != "."])
                        if "hit" == stringNumberless:
                            eHit = iInt;
                        elif "luck" == stringNumberless:
                            eLck = iInt;
                        elif "time" == stringNumberless:
                            time = iInt;
                        elif "hp" == stringNumberless:
                            extraHP = iInt;
                        elif "evar" == stringNumberless:
                            extraEvaRate = iInt/100;
                        elif "eva" == stringNumberless:
                            evaMultiplier = 1+(1+iInt/100);
                        elif "dr" == stringNumberless:
                            extraDamReduc = iInt/100;
                        elif "rld" == stringNumberless:
                            rld = iInt;
                        elif "[" in i.lower() and "]" in i.lower():
                            m = i.replace('[','').split('/');
                            try:
                                damageModifiers[0] = int(''.join(x for x in '0'+m[1] if x.isdigit()));
                                damageModifiers[1] = int(''.join(x for x in '0'+m[2] if x.isdigit()));
                                damageModifiers[2] = int(''.join(x for x in '0'+m[3] if x.isdigit()));
                                damageSource = 'Typeless';
                                if 'he' in m[0].lower():
                                    damageSource = 'HE'
                                if 'ap' in m[0].lower():
                                    damageSource = 'AP'
                                if 'avi' in m[0].lower():
                                    damageSource = 'Aviation'
                                if 'torp' in m[0].lower():
                                    damageSource = 'Torpedo'
                                if 'typeless' in m[0].lower():
                                    damageSource = 'Typeless'
                            except:
                                await message.channel.send("The custom armor modifiers are incorrect! Normal modifiers have been used instead.");
                                damageSource = 'Typeless';
                                damageModifiers = [100,80,60];
                        elif "ap" == stringNumberless:
                            damageSource = 'AP'
                        elif "he" == stringNumberless:
                            damageSource = 'HE'
                        elif "torp" == stringNumberless:
                            damageSource = 'Torpedo'
                            damageModifiers = TorpedoDamageMods
                        elif "avi" == stringNumberless:
                            damageSource = 'Aviation'
                            damageModifiers = AviationDamageMods
                        elif "crash" == stringNumberless:
                            damageSource = 'Crash'
                        elif "pvp" == stringNumberless:
                            PvEMode = False;
                            #set defualt eva,time,hit if not set yet
                            if eHit == -1:
                                eHit = 150
                            if eLck == -1:
                                eLck = 50
                            if time == -1:
                                time = 45
                        elif "noretro" in stringNumberless or "nonretro" in stringNumberless or "nokai" in stringNumberless or "nonkai" in stringNumberless:
                            retrofit = False;
                        elif "siren" == stringNumberless:
                            siren = True;
                        else:
                            #no arguments so add to name thing
                            nameArray+=[stringNumberless];


                #get ship name
                shipName = " ".join(nameArray);
                #nicknames
                shipName = getNickname(shipName.lower())
                shipData = api.getShip(ship=shipName)
                #get the needed data
                name = shipData['names']['en'];
                sClass = shipData['class'];
                hullType = shipData['hullType'];
                level = 'level120'
                if retrofit:
                    level = 'level120Retrofit'
                    try:
                        shipData['stats'][level]
                    except:
                        level = 'level120'
                        retrofit = False;

                hp = int(shipData['stats'][level]['health'])+extraHP;
                eva = int(shipData['stats'][level]['evasion'])*evaMultiplier;
                lck = int(shipData['stats'][level]['luck']);
                aa = int(shipData['stats'][level]['antiair']);
                armor = shipData['stats'][level]['armor'];

                #recalculate armor mods if PvP mode is turned on
                if PvEMode == False:

                    HEDamageMods = [135,95,70] if hullType in vanguard else [140,110,90];
                    APDamageMods = [110,90,70] if hullType in vanguard else [45,130,110];

                    if damageSource == 'HE':
                        damageModifiers = HEDamageMods;
                    if damageSource == 'AP':
                        damageModifiers = APDamageMods;
                else:
                    #set defualt eva,time,hit if not set yet
                    if eHit == -1:
                        eHit = 75
                    if eLck == -1:
                        eLck = 25
                    if time == -1:
                        time = 60


                #multiply HP by modifiers
                if PvEMode == False:
                    if hullType == "Destroyer":
                        extraEvaRate += .05;
                        hp /= 1-.25;

                    elif hullType == "Light Cruiser":
                        hp /= 1-.2;

                    elif hullType == "Heavy Cruiser":
                        hp /= 1-.15;

                #certain ships need retro for survivability skill
                needRetro = [
                    "Jintsuu"
                ]
                def getSkillBoost():
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, [0,0,0,0,0])
                        return func(damageSource,time,rld);
                    else:
                        return [0,0,0,0,0]

                def calcEHP(nameX,nameY,exHP,exEva,exDamReduc,rtime,isVHArmor,pve,torpDamageReduc):
                    realHP = hp+exHP;
                    realEva = eva+exEva;
                    #Claculate skills
                    e = 0;
                    #switcher
                    #bypass switcher if in retrofitless skill
                    result = getSkillBoost()
                    realHP = (realHP+result[0])/(1-result[4])
                    realEva *= (1+result[1])
                    e = result[2];

                    #extra damage reduction
                    if exDamReduc != 1:
                        realHP = realHP/(1-exDamReduc)
                    #add siren damage reduction if costal report
                    if nameX == "Recon Report" or nameY == "Recon Report":
                        realHP = realHP/(1-.06)

                    #get armor type
                    ArmorModLoc = {
                        'Light' : 0,
                        'Medium' : 1,
                        'Heavy' : 2
                    }
                    tempArmor = ArmorModLoc[armor]
                    #switch armor to heavy is the VH armor is used
                    if isVHArmor:
                        if armor != 'Heavy':
                            tempArmor = 2
                        else:
                            if damageSource in "HE" or damageSource in "Normal" or damageSource in "Typeless":
                                realHP *= (1/(1-.03))
                            elif damageSource in "AP":
                                realHP *= (1/(1-.06))
                    if torpDamageReduc and damageSource == "Torpedo":
                        realHP *= (1/(1-torpDamageReduc));
                    realHP *= (100/damageModifiers[tempArmor] if damageModifiers[tempArmor] != 0 else 100)

                    #reduce damage taken by AA stat if AVI
                    if damageSource == 'Aviation' or damageSource == 'Crash':
                        realHP *= (1+(aa/150))

                    PvPMult = 2.34;
                    if pve:
                        PvPMult = 1;

                    repairHeal = 1+(math.floor(rtime/15) * .01)
                    if damageSource != "Crash":
                        #Claculate accuracy
                        acc = 0.1 + (eHit)/(eHit+realEva+2) + (eLck-lck+0)/(1000) - (e+extraEvaRate);
                        acc = max(acc,.1);
                        #devide HP by acc to get eHP

                        return round((realHP*PvPMult*repairHeal)/acc);
                    else:
                        return round(realHP*PvPMult*repairHeal)
                def getZombie():
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(damageSource,time,0);
                        if result[4] == -1:
                            return 0;
                        return result[3];
                    else:
                        return 0;
                def getIncludedSkill():
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(damageSource,0,0);
                        if result[5] != -1:
                            return "Skills included: " + result[5];
                        return 'No Skill is included.';
                    else:
                        return "No Skill is included.";

                #image modify function
                def make_image():
                    #Start drawing the text on the image
                    font = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 24)
                    fontSmall = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 19)
                    fontNumbers = ImageFont.truetype("resources/fonts/Lato-Regular.ttf", 20)
                    fontNumbersBold = ImageFont.truetype("resources/fonts/Lato-Bold.ttf", 20)
                    fontNumbersSmall = ImageFont.truetype("resources/fonts/Lato-Regular.ttf", 20)

                    #get the ships armor type
                    DMGInfo = '';
                    if damageSource == "HE":
                        DMGInfo = f'HE ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "AP":
                        DMGInfo = f'AP ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Aviation":
                        DMGInfo = f'Aviation damage ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Torpedo":
                        DMGInfo = f'Torpedo damage ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Typeless":
                        DMGInfo = f'Normal Ammo ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Crash":
                        DMGInfo = 'crash damage'

                    gearArr=[
                        ['No_Gear',0,0,0,False,0],
                        ['Improved_Hydraulic_Rudder',60,40,0,False,0],
                        ['Little_Beaver_Squadron_Tag',75,35,0,False,0],
                        ['Pearl_Tears',500,0,0,False,0],
                        ['Celestial_Body',550,0,0,False,0],
                        ['Cosmic_Kicks',0,28,0,False,0],
                        ['SG_Radar',0,18,0,False,0],
                        ['Repair_Toolkit',500,0,time,False,0],
                        ['Anti-Torpedo_Bulge',350,0,0,False,.30],
                        ['Fire_Extinguisher',266,0,0,False,0],
                        #['Recon Report',120,15,0,False,0]

                    ]
                    if hullType in ['Battleship', 'Large Cruiser', 'Battlecruiser', 'Aviation Battleship','Aircraft Carrier']:
                        gearArr.insert(3,['VH_Armor_Plating',650,0,0,True,0])
                    if hullType in ['Aircraft Carrier', 'Light Carrier', 'Aviation Battleship']:
                        gearArr.insert(3,['Steam_Catapult',75,0,0,False,0])

                    gearImageSize = 70;
                    gearImagePadding = 10;
                    spacing = gearImageSize+gearImagePadding;
                    xOffset = 10;
                    yOffset = 116+20;

                    #Create the backround
                    #find grid size so image size can be made in relation to it
                    gridSize = (len(gearArr)+1)*spacing
                    isSpecialTextNeeded = False;
                    result = getSkillBoost()
                    if (extraHP !=0):
                        isSpecialTextNeeded = True;
                    #evasion
                    if (result[1] != 0 or evaMultiplier != 1):
                        isSpecialTextNeeded = True;
                    #evasion rate
                    if (result[2] != 0 or extraEvaRate != 0):
                        isSpecialTextNeeded = True;
                    #zombie
                    if (result[3] != 0):
                        isSpecialTextNeeded = True;
                    #damage reduction
                    if (result[4] != 0 or extraDamReduc != 0):
                        isSpecialTextNeeded = True;

                    output = Image.new('RGBA', (xOffset+gridSize+isSpecialTextNeeded*420,yOffset+gridSize+50),color = 'rgb(45,54,69)');
                    draw = ImageDraw.Draw(output)

                    #Get thumbnail image
                    thumbnail = requests.get(shipData['thumbnail']).content;
                    image_bytes = io.BytesIO(thumbnail)
                    thumbnailImage = Image.open(image_bytes).convert('RGB');
                    #Draw thumbnail in corner
                    output.paste(thumbnailImage,(10,10))

                    #Draw header text
                    draw.text((116+20, 10),f"{shipName.title()}'s eHP vs {DMGInfo} in {'Exercises.' if PvEMode == False else 'PvE.'}",(255,255,255),font=font)
                    draw.text((116+20, 40),f"Enemy Hit: {eHit} | Enemy Luck: {eLck} | Battle Duration: {time}s",(255,255,255),font=font)


                    #Draw gear pictures
                    for i in range(1,len(gearArr)+1):
#                        draw.text((xOffset+(i+1)*spacing, yOffset),gearArr[i][0],(255,255,255),font=fontSmall)
                        gearImage = Image.open(f"resources\images\Gear\{gearArr[i-1][0]}.png").resize((70,70));

                        output.paste(gearImage,(xOffset+spacing*i,yOffset))
                        output.paste(gearImage,(xOffset,yOffset+spacing*i))

                    #calculate eHP amoutns
                    eHPArray = []
                    zombiePercent = getZombie();
                    for i in range(len(gearArr)):
                        eHPArray.append([])
                        for j in range(len(gearArr)):
                            eHPArray[i].append(0)
                    for i in range(len(gearArr)):
                        for j in range(len(gearArr)):
                            #Bypass
                            bypassDualGear = ['Improved_Hydraulic_Rudder', 'Little_Beaver_Squadron_Tag', 'VH VH_Armor_Plating', 'Pearl_Tears', 'Cosmic_Kicks'];
                            if gearArr[i][0] in bypassDualGear and gearArr[i][0] == gearArr[j][0]:
                                eHPArray[i][j] = 'N/A'
                            else:
                                eHPArray[i][j] = calcEHP(gearArr[i][0],gearArr[j][0],gearArr[i][1]+gearArr[j][1],gearArr[i][2]+gearArr[j][2],extraDamReduc,max(gearArr[i][3],gearArr[j][3]),gearArr[i][4] or gearArr[j][4],PvEMode, max(gearArr[i][5], gearArr[j][5]))

                    #Draw HP amounts
                    maxeHP = max(max(0 if isinstance(i, str) else i for i in x) for x in eHPArray);
                    mineHP = min(min(100000 if isinstance(i, str) else i for i in x) for x in eHPArray);
                    for i in range(len(gearArr)):
                        for j in range(len(gearArr)):
                            f = fontNumbers;
                            if isinstance(eHPArray[i][j], str):
                                ehp = eHPArray[i][j]
                            else:
                                ehp = eHPArray[i][j];
                                zombieAmount = str(round(ehp*zombiePercent));
                                #draw Zombie text:
                                color = (200,200,200)
                                ehp = str(ehp);
                                tSize = font.getsize(ehp);
                                textOffset = 0
                                if zombiePercent != 0:
                                    #get text size to calculate offset
                                    zombieText = "+"+zombieAmount;
                                    zw, zh = draw.textsize(zombieText)
                                    draw.text((xOffset+(i+1)*spacing+(gearImageSize-tSize[0]+5)/2, yOffset+(j+1)*spacing+gearImageSize/2),zombieText,color,font=fontNumbersSmall)
                                    textOffset = tSize[1]/-2

                            color = (255,255,255)
                            if ehp == str(mineHP):
                                color = (240,125,125);
                                f = fontNumbersBold
                            elif ehp == str(maxeHP):
                                f = fontNumbersBold
                                color = (150,220,150);
                            elif maxeHP*.95 < float(''.join(x for x in '0'+ehp if x.isdigit())):
                                f = fontNumbersBold
                                color = (21,158,57);
                            #i have no idea why i need the 5 to center it. I've been debugging for an hour so im done with this.
                            draw.text((xOffset+(i+1)*spacing+(gearImageSize-tSize[0]+5)/2, yOffset+(j+1)*spacing+gearImageSize/2-tSize[1]/2+ textOffset),ehp,color,font=f)
                    #Draw skills
                    lines = text_wrap(str(getIncludedSkill()),font,380);
                    color = 'rgb(255,255,255)'
                    x = xOffset+gridSize+20
                    y = 10
                    for line in lines:
                        draw.multiline_text((x,y), line, fill=color, font=font,align="left")
                        y = y + 30    # update y-axis for new line

                    #Draw stat boosts
                    y = yOffset
                    draw.text(tuple([30+x+380/2-font.getsize("Stat Boosts")[0]/2,y]), "Stat Boosts", fill=color, font=font,align="cener")
                    y+=30
                    #Draw catagory text
                    skillCenter = 380/2-90+30
                    extraCenter = 380/2+90+30
                    draw.text((x+skillCenter-font.getsize("Skills")[0]/2,y+10), "Skills", fill=color, font=font,align="left")
                    draw.text((x+extraCenter-font.getsize("Extra")[0]/2,y+10), "Extra", fill=color, font=font,align="left")

                    def drawCenteredText(loc,text,fill,font,align):
                        draw.text((loc[0]-font.getsize(text)[0]/2,loc[1]), text, fill=fill, font=font,align=align);

                    def roundToPlaceValue(n,p):
                        p=pow(10,p+1)
                        return round(n*p)/p

                    y+=70

                    #warning text
                    warning = """This is not not an accurate representation of this ship's eHP in PvE.""" if PvEMode == False else """Use argument "PvP" to switch to PvP mode."""

                    #HP
                    if (extraHP !=0):
                        draw.text((x,y), "Health", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), "N/A", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), str(extraHP), fill=color, font=font,align="left")
                        y+=80

                    #evasion
                    if (result[1] != 0 or evaMultiplier != 1):
                        draw.text((x,y), "Evasion", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), str(roundToPlaceValue(result[1]*100,2))+"%", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), str(roundToPlaceValue((evaMultiplier-1)*100,2))+"%", fill=color, font=font,align="left")
                        y+=80

                    #evasion rate
                    if (result[2] != 0 or extraEvaRate != 0):
                        draw.text((x,y), "Evasion\nRate", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), str(roundToPlaceValue(result[2]*100,2))+"%", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), str(roundToPlaceValue(extraEvaRate*100,2))+"%", fill=color, font=font,align="left")
                        y+=80

                    #zombie
                    if (result[3] != 0):
                        draw.text((x,y), "Zombie", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), str(roundToPlaceValue(result[3]*100,2))+"%", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), "N/A", fill=color, font=font,align="left")
                        y+=80

                    #damage reduction
                    if (result[4] != 0 or extraDamReduc != 0):
                        draw.text((x,y), "Damage\nReduction", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), str(roundToPlaceValue(result[4]*100,2))+"%", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), str(roundToPlaceValue(extraDamReduc*100,2))+"%", fill=color, font=font,align="left")
                        y+=80

                    #Gun Reload
                    if (noSkill == False and (name in ["Takao", "Atago", "Choukai", "Maya", "Javelin", "Laffey"])):
                        draw.text((x,y), "Main Gun\nReload", fill=color, font=font,align="left")
                        drawCenteredText((x+skillCenter,y), "N/A", fill=color, font=font,align="left")
                        drawCenteredText((x+extraCenter,y), str(rld)+"s", fill=color, font=font, align="left")
                        warning += ' Reload does not account for Absolute Cooldown, Volley Time, or Reload Stat.'
                        y+=80

                    #Draw warning
                    draw.text((xOffset,yOffset+gridSize+10), warning,(255,255,255),font=fontSmall)

                    return output;

                imCat = make_image()

                with imCat as img:
                    #upload to discord
                    with io.BytesIO() as image_binary:
                        img.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        file = discord.File(fp=image_binary,filename='eHPCalc.png');
                        #embedVar = discord.Embed(title=f"{shipName.title()}'s eHP",filename='eHPCalc.png')
                        imageURL = "attachment://eHPCalc.png"
                        #embedVar.set_image(url=imageURL)
                        img.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await message.channel.send(file=file)



        except Exception as e:
            await message.channel.send(f"That shipgirl does not exist! Please try again.");
            raise








#set this up with cogs and pray it works
def setup(client):
    client.add_cog(ehpCalculator(client))
