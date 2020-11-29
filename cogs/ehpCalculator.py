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
#[HP, Eva, Eva Rate, damage reduction, skill] (make function to format this)
#createSwitcher
def ehpAmagi(hp,eva,source,time):
    return [hp,eva,.1,0,"Efficacious Planning"];
def ehpAzuma(hp,eva,source,time):
    time = max(time,1)
    totalEVABoost = 0;
    for i in range(1,time):
        if time % 20 <= 12 and time >= 20:
            totalEVABoost+=.2
    return [hp,eva*(1+(totalEVABoost/time)),0,0,"Mizuho's Intuition"];
def ehpBremerton(hp,eva,source,time):
    return [hp,eva,0,.2,"One for the Team"];
def ehpGrafZeppelin(hp,eva,source,time):
    return [hp,eva,0,.15,"Iron Blood Wings"];
def ehpJintsuu(hp,eva,source,time):
    return [hp,eva,0,.2,"The Unyielding Jintsuu"];
def ehpNoshiro(hp,eva,source,time):
    return [hp,eva,.15,0,"Noshiro's Hoarfrost"];
def ehpSanrui(hp,eva,source,time):
    actualEVA=0;
    try:
        actualEVA = eva * (min(50/time,1)*1.35 +(1-(min(50/time,1))));
    except:
        actualEVA = eva;
    return [hp,actualEVA,0,0,"Engine Boost"];
def ehpSeattle(hp,eva,source,time):
    return [hp,eva,0,.15,"Dual Nock"];
def ehpShinano(hp,eva,source,time):
    return [hp,eva,0,.2 if source != 'Torpedo' else 0,"Protector of the New Moon" if source != 'Torpedo' else -1];
def ehpSuzutsuki(hp,eva,source,time):
    return [hp*1.15,eva,0,0,"Suzutsuki, Causing Confusion!"];
def ehpYukikaze(hp,eva,source,time):
    return [hp,eva,0,.25,"The Unsinkable Lucky Ship"];

skillSwitch = {
    'Amagi' : ehpAmagi,
    'Azuma' : ehpAzuma,
    'Bremerton' : ehpBremerton,
    'Jintsuu' : ehpJintsuu,
    'Noshiro' : ehpNoshiro,
    'Saint Louis' : ehpSanrui,
    'Seattle' : ehpSeattle,
    'Shinano' : ehpShinano,
    'Suzutsuki' : ehpSuzutsuki,
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
    async def ehp(self, message, shipName, *args):
        try:
            if (shipName == 'help'):
                embed = discord.Embed(title = "EHP Help Menu")
                embed.add_field(name =":small_red_triangle: ;ehp [ship name] [args]", value =
                """
`ship name` - The ship that you want to calculate the eHP of in exercises. Use quotes for character names with a space.""", inline = False)
                embed.add_field(name =":small_red_triangle: Args", value =
"""`Args`-
    **hitN** = Set enemy hit stat to value N.
    **luckN** = set enemy luck to value N.
    **timeN** = Set battle duration stat to value N.
    **hpN** = Add N HP to the ship.
    **evaN** = Add N percent eva to the ship.
    **evaRateN** = Add N percent EVA rate to the ship.
    **AP** = Change enemy ammo type to AP. 110/90/70 is used for vanguard ships. 45/130/110 is used for backline ships.
    **HE** = Change enemy ammo type to HE. 135/95/70 is used for vanguard ships. 140/110/90 is used for backline ships.
    **avi** = View eHP vs aviation damage. 80/100/120 are used as the modifiers.
    **torp** = View eHP vs tor\*\*\*\* damage. 80/100/130 are used as the modifers.
    **crash** = View eHP vs crash damage.
    **[t,x/y/z]** = View eHP with custom ammo modifiers x/y/z and ammo type t.
    **retrofit** = use the retrofit version of this ship""", inline = False)

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
                shipName = shipName.replace('"',"");
                #nicknames
                shipName = getNickname(shipName.lower())
#                print(shipName)
                shipData = api.getShip(ship=shipName)
                #get the needed data
                name = shipData['names']['en'];
                sClass = shipData['class'];
                hullType = shipData['hullType'];
                retrofit = False;

                #damage mods
                HEDamageMods = [135,95,70] if hullType in vanguard else [140,110,90];
                APDamageMods = [110,90,70] if hullType in vanguard else [45,130,110];
                AviationDamageMods = [80,100,120];
                TorpedoDamageMods = [80,100,130];
                #Get damage source
                damageSource = 'HE'
                damageModifiers = HEDamageMods


                #get arguments
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
                            hp += iInt;
                        elif "evarate" in i.lower():
                            extraEvaRate = iInt/100;
                        elif "eva" in i.lower():
                            eva *= (1+iInt/100);
                        elif "[" in i.lower() and "]" in i.lower():
                            m = i.replace('[','').split('/');
                            try:
                                damageModifiers[0] = int(''.join(x for x in '0'+m[1] if x.isdigit()));
                                damageModifiers[1] = int(''.join(x for x in '0'+m[2] if x.isdigit()));
                                damageModifiers[2] = int(''.join(x for x in '0'+m[3] if x.isdigit()));
                                damageSource = 'HE';
                                if 'he' in m[0]:
                                    damageSource = 'HE'
                                if 'ap' in m[0]:
                                    damageSource = 'AP'
                                if 'avi' in m[0]:
                                    damageSource = 'Aviation'
                            except:
                                await message.channel.send("The custom armor modifiers are incorrect! HE modifiers have been used instead.");
                                damageSource = 'HE';
                        elif "ap" in i.lower():
                            damageSource = 'AP'
                            damageModifiers = APDamageMods
                        elif "torp" in i.lower():
                            damageSource = 'Torpedo'
                            damageModifiers = TorpedoDamageMods
                        elif "avi" in i.lower():
                            damageSource = 'Aviation'
                            damageModifiers = AviationDamageMods
                        elif "crash" in i.lower():
                            damageSource = 'Crash'
                        elif "retro" in i.lower():
                            retrofit = True;

                level = 'level120'
                if retrofit:
                    level = 'level120Retrofit'
                    try:
                        shipData['stats'][level]
                    except:
                        level = 'level120'
                        retrofit = False;
                        await message.channel.send("This ship does not have a retrofit! The normal ship has been used instead.")

                hp = int(shipData['stats'][level]['health']);
                eva = int(shipData['stats'][level]['evasion']);
                lck = int(shipData['stats'][level]['luck']);
                aa = int(shipData['stats'][level]['antiair']);
                armor = shipData['stats'][level]['armor'];

                #set default args
                evaSkill = 0;
                eHit = 150;
                eLck = 50;
                time = 30;
                extraHP = 0;
                extraEva = 0;
                extraEvaRate = 0;
                noSkill = False;

                #multiply HP by modifiers
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
                def calcEHP(exHP,exEva,rtime,isVHArmor):
                    realHP = hp+exHP;
                    realEva = eva+exEva;
                    #Claculate skills
                    e = 0;
                    #switcher
                    #bypass switcher if in retrofitless skill
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(realHP,realEva,damageSource,time);
                        realHP = result[0]/(1-result[3])
                        realEva = result[1]
                        e = result[2];

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
                            if damageSource in "HE" or damageSource in "Normal":
                                realHP *= (1/(1-.03))
                            elif damageSource in "AP":
                                realHP *= (1/(1-.06))

                    realHP *= (100/damageModifiers[tempArmor] if damageModifiers[tempArmor] != 0 else 100)

                    #reduce damage taken by AA stat if AVI
                    if damageSource == 'Aviation' or damageSource == 'Crash':
                        realHP *= (1+(aa/150))

                    repairHeal = 1+(math.floor(rtime/15) * .01)
                    if damageSource != "Crash":
                        #Claculate accuracy
                        acc = 0.1 + (eHit)/(eHit+realEva+2) + (eLck-lck+0)/(1000) - (e+extraEvaRate);
                        acc = max(acc,.1);
                        #devide HP by acc to get eHP
                        return round((realHP*2.34*repairHeal)/acc);
                    else:
                        return round(realHP*2.34*repairHeal)

                def getIncludedSkill():
                    if name in skillSwitch and noSkill == False and (name in needRetro and retrofit or not name in needRetro):
                        func = skillSwitch.get(name, "nothing")
                        result = func(0,0,damageSource,0);
                        if result[4] == -1:
                            return "No skills are included in this calculation.";
                        return "Skills included: " + result[4] + "\nAdd noskill as an argument to ignore this skill.";
                    else:
                        return "No skills are included in this calculation.";

                #choose skin
                if retrofit:
                    skin = shipData["skins"][1]
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

                    #Start drawing the text on the image
                    font = ImageFont.truetype("ArialUnicodeMS.ttf", 16)
                    draw = ImageDraw.Draw(output)

                    #get the ships armor type
                    DMGInfo = '';
                    if damageSource == "HE":
                        DMGInfo = f'HE ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "AP":
                        DMGInfo = f'AP ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Aviation":
                        DMGInfo = f'Aviation damage ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]}) Damage taken is reduced with AA stat.'
                    elif damageSource == "Torpedo":
                        DMGInfo = f'Torpedo damage ({damageModifiers[0]}/{damageModifiers[1]}/{damageModifiers[2]})'
                    elif damageSource == "Crash":
                        DMGInfo = 'crash damage.'


                    draw.text((40, 40),f"{shipName.title()}'s eHP vs {DMGInfo}",(255,255,255),font=font)
                    draw.text((40, 60),f"Enemy Hit: {eHit} | Enemy Luck: {eLck} | Battle Duration: {time}s",(255,255,255),font=font)

                    gearArr=[
                        ['No Gear',0,0,0,False],
                        ['Rudder',60,40,0,False],
                        ['Beaver',75,35,0,False],
                        ['Toolkit',500,0,time,False],
                        ['Pearl',500,0,0,False],
                        ['Kicks',0,28,0,False]
                    ]
                    if hullType in ['Battleship', 'Large Cruiser', 'Battlecruiser', 'Aviation Battleship','Aircraft Carrier']:
                        gearArr.append(['VH',650,0,0,True])
                    if hullType in vanguard:
                        gearArr.append(['Fire Sup.',266,0,0,False])
                    if hullType in ['Aircraft Carrier', 'Light Carrier', 'Aviation Battleship']:
                        gearArr.append(['Catapult',75,0,0,False])

                    xSpacing = 75;
                    ySpacing = 35;
                    xOffset = 35;
                    yOffset = 90;
                    #Draw gear names
                    for i in range(len(gearArr)):
                        draw.text((xOffset+(i+1)*xSpacing, yOffset),gearArr[i][0],(255,255,255),font=font)
                    for i in range(len(gearArr)):
                        draw.text((xOffset, yOffset+(i+1)*ySpacing),gearArr[i][0],(255,255,255),font=font)
                    #calculate eHP amoutns
                    eHPArray = []
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
                                eHPArray[i][j] = calcEHP(gearArr[i][1]+gearArr[j][1],gearArr[i][2]+gearArr[j][2],max(gearArr[i][3],gearArr[j][3]),gearArr[i][4] or gearArr[j][4])
                    #Draw HP amounts
                    maxeHP = max(max(0 if isinstance(i, str) else i for i in x) for x in eHPArray);
                    mineHP = min(min(100000 if isinstance(i, str) else i for i in x) for x in eHPArray);
                    for i in range(len(gearArr)):
                        for j in range(len(gearArr)):
                            if isinstance(eHPArray[i][j], str):
                                ehp = eHPArray[i][j]
                            else:
                                ehp = str(eHPArray[i][j]);
                            color = (255,255,255)
                            if ehp == str(mineHP):
                                color = (240,125,125);
                            elif ehp == str(maxeHP):
                                color = (134,232,132);
                            draw.text((xOffset+(i+1)*xSpacing, yOffset+(j+1)*ySpacing),ehp,color,font=font)
                    #Draw skills
                    draw.text((xOffset,450),str(getIncludedSkill()),(255,255,255),font=font)
                    #Draw warning
                    draw.text((xOffset,460+ySpacing),"This is not an accurate representation of this ship's eHP in PvE.",(255,255,255),font=font)


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
            await message.channel.send(f"{shipName.title()} is an invalid ship name! Please try again.");
            raise








#set this up with cogs and pray it works
def setup(client):
    client.add_cog(ehpCalculator(client))
