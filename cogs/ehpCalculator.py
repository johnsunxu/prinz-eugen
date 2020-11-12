import discord
import random
from discord.ext import commands
from azurlane.azurapi import AzurAPI
from PIL import Image
import requests
import urllib.request
from shipGirlNicknameHandler import getNickname
import math


api = AzurAPI()

#Structure of return data
#[HP, Eva, Eva Rate, skill] (make function to format this)
#createSwitcher
def ehpAmagi(hp,eva,time):
    return [hp,eva,.1,"Efficacious Planning"];
def ehpAzuma(hp,eva,time):
    totalEVABoost = 0;
    iteration = 1;
    #Probably working
    for i in range(1,math.floor(time/20)):
        totalEVABoost+=.7*.2;
        iteration+=1;

    if time>20:
        timeLeft = time % 20;
        if timeLeft<=12:
            totalEVABoost+=.7*.2;
        else:
            totalEVABoost+=.7*.2;
            iteration+=1;
    return [hp,eva*(1+(totalEVABoost*1.2)/(iteration*.8)),0,"Mizuho's Intuition"];
def ehpGrafZeppelin(hp,eva,time):
    return [hp*1.15,eva,0,"Iron Blood Wings"];
def ehpJintsuu(hp,eva,time):
    return [hp*1.2,eva,0,"The Unyielding Jintsuu"];
def ehpNoshiro(hp,eva,time):
    return [hp,eva,.15,"Noshiro's Hoarfrost"];
def ehpSanrui(hp,eva,time):
    actualEVA=0;
    try:
        actualEVA = eva * (min(50/time,1)*1.35 +(1-(min(50/time,1))));
    except:
        actualEVA = eva;
    return [hp,actualEVA,0,"Engine Boost"];
def ehpYukikaze(hp,eva,time):
    return [hp*1.25,eva,0,"The Unsinkable Lucky Ship"];
def ehpShinano(hp,eva,time):
    return [hp*1.2,eva,0,"Protector of the New Moon"];

skillSwitch = {
    'Amagi' : ehpAmagi,
    'Azuma' : ehpAzuma,
    'Jintsuu' : ehpJintsuu,
    'Noshiro' : ehpNoshiro,
    'Saint Louis' : ehpSanrui,
    'Shinano' : ehpShinano,
    'Yukikaze' : ehpYukikaze
}

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
`ship name` - The ship that you want to calculate the eHP of in exercises. Use quotes for character names with a space.
`Args`-
    hitN = Set enemy hit stat to value N.
    luckN = set enemy luck to value N.
    timeN = Set battle duration stat to value N.
Example:
    `;ehp Akagi` - get Akagi's eHP.
    `;ehp "Graf Zeppelin" hit100` - get Graf Zeppelin's eHP with an enemy hit stat of 100.
""", inline = False)



                await message.channel.send(embed = embed);
            else:
                shipName = shipName.replace('"',"");
                #nicknames
                shipName = getNickname(shipName.lower())
                shipData = api.getShip(ship=shipName)
                #get the needed data
                name = shipData['names']['en'];
                sClass = shipData['class'];
                hullType = shipData['hullType'];
                hp = int(shipData['stats']['level120']['health']);
                eva = int(shipData['stats']['level120']['evasion']);
                lck = int(shipData['stats']['level120']['luck']);
                armor = shipData['stats']['level120']['armor'];

                #set default args
                evaSkill = 0;
                eHit = 150;
                eLck = 50;
                time = 30;
                #get arguments
                for i in args:
                    iInt = int(''.join(x for x in i if x.isdigit()));
                    if "hit" in i.lower():
                        eHit = iInt;
                    if "luck" in i.lower():
                        eLck = iInt;
                    if "time" in i.lower():
                        time = iInt;


                #multiply HP by modifiers
                if hullType == "Destroyer":
                    evaSkill += .05;
                    hp *= 1.25;

                if hullType == "Light Cruiser":
                    hp *= 1.2;

                if hullType == "Heavy Cruiser":
                    hp *= 1.15;

                def calcEHP(exHP,exEva,rtime):
                    realHP = hp+exHP;
                    realEva = eva+exEva;
                    #Claculate skills
                    e = 0;
                    #switcher
                    if name in skillSwitch:
                        func = skillSwitch.get(name, "nothing")
                        result = func(realHP,realEva,time);
                        realHP = result[0]
                        realEva = result[1]
                        e = result[2];

                    #Claculate accuracy
                    acc = 0.1 + (eHit)/(eHit+realEva+2) + (eLck-lck+0)/(1000) - (evaSkill+e);
                    acc = max(acc,.1);
                    repairHeal = 1+(math.floor(rtime/15) * .01)
                    #devide HP by acc to get eHP
                    return round((realHP/acc)*2.34*repairHeal);

                def getIncludedSkill():
                    if name in skillSwitch:
                        func = skillSwitch.get(name, "nothing")
                        result = func(0,0,0);
                        return "Skills included: " + result[3];
                    else:
                        return "No skills are included in this calculation.";

                s = f"""
            Enemy Hit: {eHit} | Enemy Luck: {eLck} | Battle Duration: {time}s
```python
          No Gear    Beaver    Toolkit
No Gear   {calcEHP(0,0,0)}      {calcEHP(75,35,0)}     {calcEHP(0,0,time)}
Rudder    {calcEHP(60,40,0)}      {calcEHP(75+60,35+40,0)}     {calcEHP(540,40,time)}
Toolkit   {calcEHP(500,0,time)}      {calcEHP(575,35,time)}     {calcEHP(1000,0,time)}
```
    {getIncludedSkill()}
This is NOT an representation of a ships eHP in PvE.
                """
    #Tear      {calcEHP(500,0,0)}      {calcEHP(575,35,0)}     {calcEHP(1000,0,time)}



                embed = discord.Embed(title=f"{name}'s EHP in Exercises", description=s)
                r = random.choice(shipData["skins"])['chibi'];
                embed.set_thumbnail(url=r);

                await message.channel.send(embed = embed);


        except Exception as e:
            await message.channel.send(f"{shipName.title()} is an invalid ship name! Please try again.");
            print(e)








#set this up with cogs and pray it works
def setup(client):
    client.add_cog(ehpCalculator(client))
