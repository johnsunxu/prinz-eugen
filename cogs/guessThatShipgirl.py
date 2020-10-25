import discord
import random
from discord.ext import commands
import asyncio
import json
import hashlib
import os
import io
from azurlane.azurapi import AzurAPI
from PIL import Image
import tempfile
import requests
import urllib.request
import numpy as np
import shutil


#encode channel into my jank format
def encodeChannel(message):
    return str(message.guild.id) +"+"+ str(message.channel);

#loads the list of all the channels
def loadChannelList():
    with open('cogs/channelList.json') as json_file:
        return json.load(json_file);

#Saves the entire json list
def saveChannelList(data):
    #dictionary data
    with open('cogs/channelList.json', 'w') as outfile:
        json.dump(data, outfile)

#Save a certain value into the current message. This is the ship name for now.
def saveChannelData(message, data):
    #message message
    #string data
    list = loadChannelList()
    list[encodeChannel(message)] = data
    saveChannelList(list)

#reads the value of the game that is running in a certain channel
def getChannelData(message):
    #message message
    data = loadChannelList();
    if encodeChannel(message) in data:
        return data[encodeChannel(message)]
    else:
        return 0;

#clears the data for the game running in a certain channel
def deleteChannelData(message):
    #message message
    list = loadChannelList()
    list.pop(encodeChannel(message),None)
    saveChannelList(list)

def loadSkinList():
    with open('cogs/shipSkinList.json', 'r') as json_file:
        return json.load(json_file)

embedColor = 0xf01111

#Set up API
api = AzurAPI()

#get all ships
ships = api.getAllShips();

#create class
class GuessThatShipgirl(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    #Main function
    @commands.command(aliases = ["guess","g"])
    async def run(self, message, *args):

        #Combine the args into one so it is easier to referance later
        arg = " ".join(args);

        #Help menu embed.
        if (arg == 'help'):
            embed = discord.Embed(title = "Guess Game Help Menu")
            embed.add_field(name =":small_red_triangle: ;guess", value = "Start a guessing game\n`+skins`, `+s`, or `s` to add skins.\n`+retro`, `+r`, or `r` to add retrofit skins.\n`-default`, `-d`, or `d` to remove default skins.\n", inline = False)
            embed.add_field(name =":small_red_triangle: ;guess stop", value = "Ends a guessing game if one is running.", inline = False)
            embed.add_field(name =":small_red_triangle: ;guess [Shipgirl Name]", value = 'Guess a shipgirl.\nex.`;guess Howe`\nex.`;guess Long Island`', inline = False)

            await message.channel.send(embed = embed);

        #Start game argument
        # elif (len(args) == 0):
            # if getChannelData(message) != 0:
            #     #The channel has a game running. Send error.
            #     await message.channel.send('This channel already has a game running! Try again in a different channel or wait until this game is over.');
            #
            # else:
            #     #The channel does not have a game running. Start it.
            #     pool = ["Default"];
            #     #Get arguments
            #     if "+skins" in args or "+s" in args or "s" in args:
            #         pool += ["Skins"]
            #     if "+retrofit" in args or "+r" in args or "+retro" in args or "r" in args:
            #         pool += ["Retrofit"]
            #     if "-default" in args or "-d" in args or "d" in args:
            #         pool[0] = '';
            #
            #     skinArr = [];
            #     if len(pool) == 1 and pool[0] == '':
            #         await message.channel.send("You need to play with at least one category!");
            #     else:
            #         #Choose random ship
            #         while True:
            #             randomShip = random.choice(ships)
            #             skinsArr = randomShip['skins']
            #             #print('\n'+randomShip['names']['en'])
            #             #Remove what doesn't belong
            #             i = 0;
            #             sizeOfSkinArr = len(skinsArr);
            #             for j in range(0,sizeOfSkinArr):
            #                 try:
            #                     if (skinsArr[i]['name'] == 'Default'):
            #                         if not "Default" in pool:
            #                             skinsArr.pop(i);
            #                             i-=1;
            #                             #print(skinsArr[i]['name'])
            #                     elif skinsArr[i]['name'] == 'Retrofit':
            #                         if not "Retrofit" in pool:
            #                             skinsArr.pop(i);
            #                             i-=1;
            #                             #print(skinsArr[i]['name'])
            #                     else:
            #                         if not "Skins" in pool:
            #                             skinsArr.pop(i);
            #                             i-=1;
            #                             #print(skinsArr[i]['name'])
            #                 except:
            #                     break;
            #                 i+=1;
            #             if (len(skinsArr) > 0):
            #                 break;
            #
            #         #Create data structure that will store ship data
            #         shipData = {
            #             'name' : '',
            #             'skin' : ''
            #         }
            #         #Populate the dictionary
            #         shipData['name'] = randomShip['names']['en'];
            #         shipData['skin'] = random.choice(skinsArr);
            #
            #         #make dir
            #         os.mkdir(f"cogs/GuessThatShipgirl/{encodeChannel(message)}");
            #         #its saved at cogs/GuessThatShipgirl/dont_try_to_cheat.png. Thought the name would be funny.
            #         urllib.request.urlretrieve(shipData['skin']['image'], f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png");
            #
            #         #Save to outfile
            #         saveChannelData(message,shipData);
            #
            #         #turn the image into a sillouete
            #         image = Image.open(f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png") # open colour image
            #         x = np.array(image)
            #         r, g, b, a = np.rollaxis(x, axis=-1)
            #         r[a!=0] = 0;
            #         g[a!=0] = 0;
            #         b[a!=0] = 0;
            #         x = np.dstack([r, g, b, a])
            #         image = Image.fromarray(x, 'RGBA');
            #         image.save(f'cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png')
            #
            #         #send the embed
            #         file = discord.File(f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png");
            #         embedVar = discord.Embed(title="Guess the Shipgirl with ;guess [name]! You have 2 minutes!", color=embedColor)
            #         imageURL = "attachment://dont_try_to_cheat.png"
            #         embedVar.set_image(url=imageURL)
            #         await message.channel.send(embed = embedVar,file = file);
            #
            #         #delete the files
            #         shutil.rmtree(f"cogs/GuessThatShipgirl/{encodeChannel(message)}")
            #
            #         #set timeout. 120 = 2 minutes.
            #         await asyncio.sleep(120)
            #         #If game is still running, end.
            #         if (getChannelData(message) != 0):
            #             if (getChannelData(message) == shipData):
            #                 #Send time out embed. I have to make this a function.
            #                 embedVar = discord.Embed(title=f"The game timed out. {shipData['name']} was the correct answer.", color=embedColor)
            #                 imageURL = shipData['skin']['image']
            #                 embedVar.set_image(url=imageURL)
            #                 await message.channel.send(embed = embedVar);
            #
            #                 #Delete data to end the game
            #                 deleteChannelData(message);

        #Handle player giving up
        elif (arg == 'give' or arg == 'give up' or arg == 'quit' or arg == 'stop' or arg == 'end' or arg == 'giveup' or arg == "skip"):
            if getChannelData(message) != 0:
                #Find out what the answer was
                data = getChannelData(message);
                ans = data['name'];
                #Send the embed for timeout
                embedVar = discord.Embed(title=f"{message.author} stopped the game. The correct answer was {ans}.", color=embedColor)
                imageURL = data['skin']['image']
                embedVar.set_image(url=imageURL)
                await message.channel.send(embed = embedVar);

                #Delete the game from memory
                deleteChannelData(message);
            else:
                #no game is running. Send error message.
                await message.channel.send("A game is not running right now. Start a new game with ;guess or ;g!");
        else:
            #determine if game is running
            data = getChannelData(message);
            c = False;
            #A game is not running if it is not in the json list. getChannelData() returns 0 if a game is not found.
            if data == 0:
                #C is the bool used to tell if the answer is true
                c = True;
                #This is where I start a new game apparently.
                #await message.channel.send("A game is not running right now. Start a new game with ;guess or ;g!");
                            #if getChannelData(message) != 0:
                #The channel has a game running. Send error.
                #await message.channel.send('This channel already has a game running! Try again in a different channel or wait until this game is over.');
                #The channel does not have a game running. Start it.
                pool = ["Default"];
                #Get arguments
                #Go through all to see if valid.
                skip = False;
                for i in args:
                    i = i.lower();
                    if i == "+skins" or i == "+s" or i =="s":
                        pool += ["Skins"]
                    elif i == "+retrofit" or i == "+r" or i == "+retro" or i == "r" :
                        pool += ["Retrofit"]
                    elif i == "-default" or i == "-d" or i == "d":
                        pool[0] = '';
                    elif (i != "start"):
                        #There was an error. Tell the player that they are using an invalid argument.
                        await message.channel.send(f"{i.title()} is an invalid argument. View ;guess help to see what went wrong.");
                        skip = True;
                        break;

                if (skip == False):
                    skinArr = [];
                    if len(pool) == 1 and pool[0] == '':
                        await message.channel.send("You need to play with at least one category!");
                    else:
                        #Choose random ship
                        while True:
                            randomShip = random.choice(ships)
                            skinsArr = randomShip['skins']
                            #print('\n'+randomShip['names']['en'])
                            #Remove what doesn't belong
                            i = 0;
                            sizeOfSkinArr = len(skinsArr);
                            for j in range(0,sizeOfSkinArr):
                                try:
                                    if (skinsArr[i]['name'] == 'Default'):
                                        if not "Default" in pool:
                                            skinsArr.pop(i);
                                            i-=1;
                                            #print(skinsArr[i]['name'])
                                    elif skinsArr[i]['name'] == 'Retrofit':
                                        if not "Retrofit" in pool:
                                            skinsArr.pop(i);
                                            i-=1;
                                            #print(skinsArr[i]['name'])
                                    else:
                                        if not "Skins" in pool:
                                            skinsArr.pop(i);
                                            i-=1;
                                            #print(skinsArr[i]['name'])
                                except:
                                    break;
                                i+=1;
                            if (len(skinsArr) > 0):
                                break;

                        #Create data structure that will store ship data
                        shipData = {
                            'name' : '',
                            'skin' : ''
                        }
                        #Populate the dictionary
                        shipData['name'] = randomShip['names']['en'];
                        shipData['skin'] = random.choice(skinsArr);

                        #make dir
                        os.mkdir(f"cogs/GuessThatShipgirl/{encodeChannel(message)}");
                        #its saved at cogs/GuessThatShipgirl/dont_try_to_cheat.png. Thought the name would be funny.
                        urllib.request.urlretrieve(shipData['skin']['image'], f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png");

                        #Save to outfile
                        saveChannelData(message,shipData);

                        #turn the image into a sillouete
                        image = Image.open(f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png") # open colour image
                        x = np.array(image)
                        r, g, b, a = np.rollaxis(x, axis=-1)
                        r[a!=0] = 0;
                        g[a!=0] = 0;
                        b[a!=0] = 0;
                        x = np.dstack([r, g, b, a])
                        image = Image.fromarray(x, 'RGBA');
                        image.save(f'cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png')

                        #send the embed
                        file = discord.File(f"cogs/GuessThatShipgirl/{encodeChannel(message)}/dont_try_to_cheat.png");
                        embedVar = discord.Embed(title="Guess the Shipgirl with ;guess [name]! You have 2 minutes!", color=embedColor)
                        imageURL = "attachment://dont_try_to_cheat.png"
                        embedVar.set_image(url=imageURL)
                        await message.channel.send(embed = embedVar,file = file);

                        #delete the files
                        shutil.rmtree(f"cogs/GuessThatShipgirl/{encodeChannel(message)}")

                        #set timeout. 120 = 2 minutes.
                        await asyncio.sleep(120)
                        #If game is still running, end.
                        if (getChannelData(message) != 0):
                            if (getChannelData(message) == shipData):
                                #Send time out embed. I have to make this a function.
                                embedVar = discord.Embed(title=f"The game timed out. {shipData['name']} was the correct answer.", color=embedColor)
                                imageURL = shipData['skin']['image']
                                embedVar.set_image(url=imageURL)
                                await message.channel.send(embed = embedVar);

                                #Delete data to end the game
                                deleteChannelData(message);
            else:
                ans = data['name'];
                #Do all the special checks
                arg2 = arg.lower().replace('"','');

                #Handle nick names. Im proud of this solution tbh.
                nicknameDic = {
                    "fdg" : "Friedrich der Große",
                    "bad" : "Izumo",
                    "warcorgi" : "Warspite",
                    "warpoi" : "Warspite",
                    "nanoda" : "Yukikaze",
                    "yuki" : "Yukikaze",
                    "graf" : "Graf Zeppelin",
                    "enty" : "Enterprise",
                    "owari da" : "Enterprise",
                    "st louis" : "St. louis",
                    "sanrui" : "Saint Louis",
                    "jesus" : "Juneau",
                    "sandy" : "San Diego",
                    "bisko" : "Bismark",
                    "bisco" : "Bismark",
                    "kgv" : "King George V",
                    "clevebro" : "Cleveland",
                    "pow" : "Prince of Wales",
                    "doy" : "Duke of York",
                    "qe" : "Queen Elizabeth",
                    "bulin" : "Universal Bulin",
                    "purin" : "Prototype Bulin MKII",
                    "urin" : "Specialized Bulin Custom MKIII",
                    "ur bulin" : "Specialized Bulin Custom MKIII",
                    "hipper" : "Admiral Hipper",
                    "hipper muse" : "Admiral Hipper µ",
                    "spee" : "Graf Spee",
                    "indy" : "Indianapolis",
                    "177013" : "Marblehead",
                    'prinz' : "Prinz Eugen",
                    'sara' : "Saratoga",
                    'iroha' : "I-168",
                    "lolicon" : "Ark Royal",
                    "massa" : "Massachusetts",
                    "poi" : "Yuudachi",
                    "lusty" : "Illustrious",
                    "ayaya" : "Ayanami",
                    "nimi" : "Z23",
                    "monty" : "Montpelier",
                    "pamiat" : "Pamiat Merkuria",
                    "rossiya" : "Sovetskaya Rossiya",
                    "kaga (bb)" : "Kaga (Battleship)",
                    "kaga bb" : "Kaga (Battleship)",
                    "jb" : "Jean Bart"


                }

                #if answer is a nickname, replace answer with ship it is referencing.
                if arg2 in nicknameDic:
                    arg2 = nicknameDic[arg2].lower();

                #Here is where special characters are handled. Ex. Muse, special o, e, and a.
                if (ans.lower().replace('ö','o').replace('é', 'e').replace('â','a').replace('µ','muse') == arg2):
                    c = True;

                if (ans.lower() == arg2):
                    c = True;

                if (c == True):
                    embedVar = discord.Embed(title=f"Hooray! {ans} was the correct answer!", color=embedColor)
                    imageURL = data['skin']['image']
                    embedVar.set_image(url=imageURL)
                    await message.channel.send(embed = embedVar);

                    deleteChannelData(message);
            #If the answer was not correct, its incorrect. Tell the play that.
            if (c == False):
                #check if answer is included
                if (len(arg) == 0):
                    await message.channel.send(f"You must include an answer!");
                else:
                    await message.channel.send(f"{arg.title()} was not the correct answer.");



#set this up with cogs and pray it works
def setup(client):
    client.add_cog(GuessThatShipgirl(client))
