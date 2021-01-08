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
def ehpAmagi(hp,eva,source,time):
    return [hp,eva,.1,0,0,"Efficacious Planning","While alive in fleet, reduces Burn damage taken by the Main Fleet by 5% (15%) and increases their Evasion Rate by 4% (10%)."];
def ehpAzuma(hp,eva,source,time):
    time = max(time,1)
    totalEVABoost = 0;
    for i in range(1,time):
        if time % 20 <= 12 and time >= 20:
            totalEVABoost+=.2*.7
    return [hp,eva*(1+(totalEVABoost/time)),0,0,0,"Mizuho's Intuition","Every 20 seconds: 30% (70%) chance to increase own Evasion by 10% (20%) and Accuracy by 20% (50%) for 12 seconds."];
def ehpBremerton(hp,eva,source,time):
    damReduc = 0;
    try:
        damReduc =(min(30/time,1)*1.2 +(1-(min(30/time,1))));
    except:
        damReduc = 1.2;
    return [hp,eva,0,0,damReduc-1,"One for the Team","At the start of the battle, if this ship is in the frontmost position of your Vanguard: decreases this ship's DMG taken by 5.0% (20.0%) for 30s; If not in this position, increases this ship's AA by 15.0% (25.0%) until the end of the battle."];
def ehpCheshire(hp,eva,source,time):
    return [hp,eva*1.15,0,0,.15,"Grin and Fire! and Bounce Right Back","Decrease this ship's DMG taken by 5% (15.0%). Every 12s after the start of the battle: 50% (100%) chance to fire a special barrage (DMG is based on the skill's level). Decrease the loading time of this ship's first wave of torpedoes by 40% (70.0%). When this ship takes DMG: 15.0% chance to increase this ship's FP, EVA, and AA by 1% (5.0%) until the end of the battle. Can be stacked up to 3 times.","Bounce Right Back is assumed to be at max level."];
def ehpFriedrich(hp,eva,source,time):
    return [hp,eva,0,0,.1,"Rhapsody of Darkness","""When own HP is between:
100% and 70% of max HP: increases own Firepower by 10% (20%).
70% and 30% of max HP: increases own Firepower by 4% (10%) and decreases damage taken by self by 4% (10%).
30% and 1% of max HP: decreases damage taken by self by 10% (20%)."""];
def ehpGrafZeppelin(hp,eva,source,time):
    return [hp,eva,0,0,.15,"Iron Blood Wings"];
def ehpJintsuu(hp,eva,source,time):
    return [hp,eva,0,0,.2,"The Unyielding Jintsuu"];
def ehpMinneapolis(hp,eva,source,time):
    return [hp,eva,0,.2,0,"Dullahan"];
def ehpMogami(hp,eva,source,time):
    return [hp,eva,0,0,.2 if source == 'AP' else 0,"AP Protection" if source == 'AP' else -1];
def ehpNingHai(hp,eva,source,time):
    return [hp,eva,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).","This is skill is Yat Sen's."];
def ehpNoshiro(hp,eva,source,time):
    return [hp,eva,.15,0,0,"Noshiro's Hoarfrost"];
def ehpPhoenix(hp,eva,source,time):
    return [hp,eva,0,.25,0,"Red Phoenix","When Health falls under 20%, heals 15% (25%) of max Health and increase own Firepower by 30% for 15 seconds. Can only occur once per battle."];
def ehpPingHai(hp,eva,source,time):
    return [hp,eva,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%).","This is skill is Yat Sen's."];
def ehpSanrui(hp,eva,source,time):
    try:
        actualEVA = eva * (min(50/time,1)*1.35 +(1-(min(50/time,1))));
    except:
        actualEVA = eva;
    return [hp,actualEVA,0,0,0,"Engine Boost"];
def ehpSeattle(hp,eva,source,time):
    return [hp,eva,0,0,.15,"Dual Nock"];
def ehpShinano(hp,eva,source,time):
    return [hp,eva,0,0,.2 if source != 'Torpedo' else 0,"Protector of the New Moon" if source != 'Torpedo' else -1];
def ehpSuzutsuki(hp,eva,source,time):
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
    return [hp,eva,totalEVABoost/time,.15,0,"Suzutsuki, Causing Confusion!"];
def ehpYatSen(hp,eva,source,time):
    return [hp,eva,.3,0,.2,"Dragon Empery Bond","When sortied with Ning Hai and/or Ping Hai, Yat Sen and the aforementioned ships have their damage taken decreased by 8% (20%) and Evasion Rate increased by 15% (30%)."];
def ehpYukikaze(hp,eva,source,time):
    return [hp,eva,0,0,.25,"The Unsinkable Lucky Ship"];

skillSwitch = {
    'Amagi' : ehpAmagi,
    'Azuma' : ehpAzuma,
    'Bremerton' : ehpBremerton,
    'Friedrich der Große' : ehpFriedrich,
    'Jintsuu' : ehpJintsuu,
    'Minneapolis' : ehpMinneapolis,
    'Mogami' : ehpMogami,
    'Ning Hai' : ehpNingHai,
    'Noshiro' : ehpNoshiro,
    'Phoenix' : ehpPhoenix,
    'Ping Hai' : ehpPingHai,
    'Saint Louis' : ehpSanrui,
    'Seattle' : ehpSeattle,
    'Shinano' : ehpShinano,
    'Suzutsuki' : ehpSuzutsuki,
    'Yat Sen' : ehpYatSen,
    'Yukikaze' : ehpYukikaze
}

#Usefull vanguard array
vanguard = ['Destroyer', 'Light Cruiser', 'Heavy Cruiser', 'Large Cruiser', 'Munition Ship']

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
"""`Args`-
    **PvP** = Switches mode to PvP mode.
    **hitN** = Set enemy hit stat to value N.
    **luckN** = set enemy luck to value N.
    **timeN** = Set battle duration stat to value N.
    **hpN** = Add N HP to the ship.
    **evaN** = Add N percent eva to the ship.
    **evaRateN** = Add N percent EVA rate to the ship.
    **drN** = Add N percent damage reduction to the ship.
    **AP** = Change enemy ammo type to AP. 110/90/70 is used for vanguard ships. 45/130/110 is used for backline ships.
    **HE** = Change enemy ammo type to HE. 135/95/70 is used for vanguard ships. 140/110/90 is used for backline ships.
    **avi** = View eHP vs aviation damage. 80/100/120 are used as the modifiers.
    **torp** = View eHP vs tor\*\*\*\* damage. 80/100/130 are used as the modifers.
    **crash** = View eHP vs crash damage.
    **[t/x/y/z]** = View eHP with custom ammo modifiers x/y/z and damage type t.
    **siren** = set damage source to sirens.
    **noRetro** = Do not use the retrofit version of this ship""", inline = False)

                embed.add_field(name =":small_red_triangle: Examples", value =
"""
Example:
    `;ehp Akagi` - get Akagi's eHP.
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
                eHit = 75;
                eLck = 25;
                time = 60;
                damageSource = 'Typeless';
                damageModifiers = [100,80,60];
                retrofit = True;

                siren = False;

                #get args
                for i in args:
                    if "noskill" in i.lower():
                        noSkill = True;
                    else:
                        iInt = int(''.join(x for x in '0'+i if x.isdigit()));
                        if "hit" in i.lower():
                            eHit = iInt;
                        elif "luck" in i.lower():
                            eLck = iInt;
                        elif "time" in i.lower():
                            time = iInt;
                        elif "hp" in i.lower():
                            extraHP = iInt;
                        elif "evar" in i.lower():
                            extraEvaRate = iInt/100;
                        elif "eva" in i.lower():
                            evaMultiplier = 1+(1+iInt/100);
                        elif "dr" in i.lower():
                            extraDamReduc = iInt/100;
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
                        elif "ap" == i.lower():
                            damageSource = 'AP'
                        elif "he" == i.lower():
                            damageSource = 'HE'
                        elif "torp" in i.lower():
                            damageSource = 'Torpedo'
                            damageModifiers = TorpedoDamageMods
                        elif "avi" in i.lower():
                            damageSource = 'Aviation'
                            damageModifiers = AviationDamageMods
                        elif "crash" in i.lower():
                            damageSource = 'Crash'
                        elif "pvp" in i.lower():
                            PvEMode = False;
                            eHit = 150;
                            eLck = 50;
                            time = 45;
                        elif "noretro" in i.lower() or "nonretro" in i.lower() or "nokai" in i.lower() or "nonkai" in i.lower():
                            retrofit = False;
                        elif "siren" in i.lower():
                            siren = True;
                        else:
                            #no arguments so add to name thing
                            nameArray+=[i.lower()];


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
                def calcEHP(nameX,nameY,exHP,exEva,exDamReduc,rtime,isVHArmor,pve,torpDamageReduc):
                    realHP = hp+exHP;
                    realEva = eva+exEva;
                    #Claculate skills
                    e = 0;
                    #switcher
                    #bypass switcher if in retrofitless skill
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(realHP,realEva,damageSource,time);
                        realHP = result[0]/(1-result[4])
                        realEva = result[1]
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
                        result = func(0,0,damageSource,0);
                        if result[4] == -1:
                            return 0;
                        return result[3];
                    else:
                        return 0;
                def getIncludedSkill():
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(0,0,damageSource,0);
                        if result[5] != -1:
                            return "Skills included: " + result[5] + "\nAdd noskill as an argument to ignore this skill.";
                        return "No skills are included in this calculation.";
                    else:
                        return "No skills are included in this calculation.";

                #choose skin
                skin = {
                    'name' : 0,
                };
                if retrofit:
                    i = 0;
                    while skin['name'] != "Retrofit":
                        skin = shipData["skins"][i]
                        i+=1;
                else:
                    skin = shipData["skins"][0]
                #Create Image
                url = skin['background']
                background = requests.get(url, timeout=4.0)
                if background.status_code != requests.codes.ok:
                    assert False, 'Status code error: {}.'.format(r.status_code)
                url = skin['image']
                character = requests.get(url, timeout=4.0)
                if background.status_code != requests.codes.ok:
                    assert False, 'Status code error: {}.'.format(r.status_code)

                #Create rouned rectangle functions
                def round_corner(radius, fill):
                    #Draw a round corner
                    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(corner)
                    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
                    return corner


                def round_rectangle(size, radius, fill):
                    #Draw a rounded rectangle
                    width, height = size
                    rectangle = Image.new('RGBA', size, fill)
                    corner = round_corner(radius, fill)
                    rectangle.paste(corner, (0, 0))
                    rectangle.paste(corner.rotate(90), (0, height - radius))  # Rotate the corner and paste it
                    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
                    rectangle.paste(corner.rotate(270), (width - radius, 0))
                    return rectangle

                #image modify function
                def get_concat_h(back,char):

                    back = back.convert('RGBA');
                    char = char.convert('RGBA');
                    #resize backround
                    back = back.resize((1024,576));

                    OldWidth, OldHeight = char.size
                    NewWidth, NewHeight = back.size
                    imageWidth = int(OldWidth*(NewHeight/OldHeight));
                    char = char.resize((imageWidth,NewHeight));

                    back.paste(char, (875-int(imageWidth/2), 0), char)

                    tempIMG = Image.new('RGBA', (NewWidth, NewHeight), color = (0,0,0,0))
                    imgD = ImageDraw.Draw(tempIMG)
                    #Draw rounded rectangle
                    rect = round_rectangle((715, 526),30,(0,0,0,180));
                    back.paste(rect, (10,25), rect)


                    #imgD.rectangle([(25, 25), (750, 526)], fill = (15,15,15,180))

                    output = Image.alpha_composite(back,tempIMG);
                    output = output.convert('RGB');

                    #Start drawing the text on the image
                    font = ImageFont.truetype("Trebuchet_MS.ttf", 16)
                    fontSmall = ImageFont.truetype("Trebuchet_MS.ttf", 12)
                    fontNumbers = ImageFont.truetype("Lato-Regular.ttf", 12)
                    fontNumbersBold = ImageFont.truetype("Lato-Bold.ttf", 12)
                    fontNumbersSmall = ImageFont.truetype("Lato-Regular.ttf", 9);

                    draw = ImageDraw.Draw(output)

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


                    draw.text((40, 40),f"{shipName.title()}'s eHP vs {DMGInfo} in {'Exercises.' if PvEMode == False else 'PvE.'}",(255,255,255),font=font)
                    draw.text((40, 60),f"Enemy Hit: {eHit} | Enemy Luck: {eLck} | Battle Duration: {time}s",(255,255,255),font=font)

                    gearArr=[
                        ['No Gear',0,0,0,False,0],
                        ['Rudder',60,40,0,False,0],
                        ['Beaver',75,35,0,False,0],
                        ['Toolkit',500,0,time,False,0],
                        ['500 HP',500,0,0,False,0],
                        ['550 HP',550,0,0,False,0],
                        ['Kicks',0,28,0,False,0]
                    ]
                    if hullType in ['Battleship', 'Large Cruiser', 'Battlecruiser', 'Aviation Battleship','Aircraft Carrier']:
                        gearArr.append(['VH',650,0,0,True,0])

                    if hullType in vanguard:
                        if hullType not in ['Large Cruiser']:
                            gearArr.append(['Fire Sup.',266,0,0,False,0])
                        gearArr.append(['Torp Bg.',350,0,0,False,.30])
                        if siren:
                            gearArr.append(['Recon Report',120,15,0,False,0])
                    if hullType in ['Aircraft Carrier', 'Light Carrier', 'Aviation Battleship']:
                        gearArr.append(['Catapult',75,0,0,False,0])

                    xSpacing = 60;
                    ySpacing = 30;
                    xOffset = 35;
                    yOffset = 100;
                    #Draw gear names
                    for i in range(len(gearArr)):
                        draw.text((xOffset+(i+1)*xSpacing, yOffset),gearArr[i][0],(255,255,255),font=fontSmall)
                    for i in range(len(gearArr)):
                        if gearArr[i][0] == 'Recon Report':
                            text = 'Recon Rp.'
                        else:
                            text = gearArr[i][0];
                        draw.text((xOffset, yOffset+(i+1)*ySpacing),text,(255,255,255),font=fontSmall)
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
                            bypassDualGear = ['Rudder', 'Beaver', 'VH Armor', 'Pearl', 'Kicks'];
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
                                color = (150,220,150)
                                if zombiePercent != 0:
                                    #get text size to calculate offset
                                    zombieText = "+"+zombieAmount;
                                    zw, zh = draw.textsize(zombieText)
                                    draw.text((xOffset+(i+1)*xSpacing+xSpacing-zw-20, yOffset+13+(j+1)*ySpacing),zombieText,color,font=fontNumbersSmall)
                                ehp = str(ehp);
                            color = (255,255,255)
                            if ehp == str(mineHP):
                                color = (240,125,125);
                                f = fontNumbersBold
                            elif ehp == str(maxeHP):
                                f = fontNumbersBold
                                color = (150,220,150);
                            draw.text((xOffset+(i+1)*xSpacing, yOffset+(j+1)*ySpacing),ehp,color,font=f)

                    #Draw skills
                    draw.text((xOffset,450),str(getIncludedSkill()),(255,255,255),font=fontSmall)
                    #Draw warning
                    draw.text((xOffset,460+ySpacing-8),"""This is not not an accurate representation of this ship's eHP in PvE.""" if PvEMode == False else """Use argument "PvP" to switch to PvP mode.""" ,(255,255,255),font=fontSmall)

                    return output;

                imCat = get_concat_h(Image.open(io.BytesIO(background.content)), Image.open(io.BytesIO(character.content)))

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
