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
from shipGirlNicknameHandler import getNickname


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

def saveChannelDataEncoded(encodedMessage,data):
    list = loadChannelList()
    list[encodedMessage] = data
    saveChannelList(list)
def getChannelDataEncoded(encodedMessage):
    #message message
    data = loadChannelList();
    if encodedMessage in data:
        return data[encodedMessage]
    else:
        return 0;
def deleteChannelDataEncoded(encodedMessage):
    #message message
    list = loadChannelList()
    list.pop(encodedMessage,None)
    saveChannelList(list)

#clears the data for the game running in a certain channel
def deleteChannelData(message):
    #message message
    list = loadChannelList()
    list.pop(encodeChannel(message),None)
    saveChannelList(list)

def loadSkinList():
    with open('cogs/shipSkinList.json', 'r') as json_file:
        return json.load(json_file)

async def startGame(message,encodedMessage, args):
    #The channel does not have a game running. Start it.
    pool = ["Default","Retrofit"];
    #Get arguments
    #Go through all to see if valid.
    skip = False;
    #set mode
    mode = 'normal';
    for i in args:
        i = i.lower();
        if i == "+skins" or i == "+s" or i =="s":
            pool += ["Skins"]
        elif i == "+retrofit" or i == "+r" or i == "+retro" or i == "r" :
            pool[1] = '';
        elif i == "-default" or i == "-d" or i == "d":
            pool[0] = '';
        elif i == 'endless':
            #if endless is arg, set mode to endless.
            mode = 'endless';
        elif (i != "start"):
            #There was an error. Tell the player that they are using an invalid argument.
            await message.channel.send(f"{i.title()} is an invalid argument. View `;guess help` to see what went wrong.");
            skip = True;
            break;
    if (skip == False):
        skinArr = [];
        if (not "Default" in pool) and (not "Retrofit" in pool) and (not "Skins" in pool):
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
            if not os.path.exists(f"cogs/GuessThatShipgirl/{encodedMessage}/dont_try_to_cheat.png"):
                os.mkdir(f"cogs/GuessThatShipgirl/{encodedMessage}");
                #its saved at cogs/GuessThatShipgirl/dont_try_to_cheat.png. Thought the name would be funny.
                urllib.request.urlretrieve(shipData['skin']['image'], f"cogs/GuessThatShipgirl/{encodedMessage}/dont_try_to_cheat.png");

                #Save to outfile
                saveChannelDataEncoded(encodedMessage,[shipData,encodedMessage,args,mode]);

                #turn the image into a sillouete
                image = Image.open(f"cogs/GuessThatShipgirl/{encodedMessage}/dont_try_to_cheat.png") # open colour image
                x = np.array(image)
                r, g, b, a = np.rollaxis(x, axis=-1)
                r[a!=0] = 0;
                g[a!=0] = 0;
                b[a!=0] = 0;
                x = np.dstack([r, g, b, a])
                image = Image.fromarray(x, 'RGBA');
                image.save(f'cogs/GuessThatShipgirl/{encodedMessage}/dont_try_to_cheat.png')

                desc = "Type `;g stop` to stop the game.";
                if (mode == 'endless'):
                    desc += "\nType `;g stop endless` to stop endless mode.";

                #send the embed
                file = discord.File(f"cogs/GuessThatShipgirl/{encodedMessage}/dont_try_to_cheat.png");
                embedVar = discord.Embed(title="Guess the Shipgirl with ;guess [name]! You have 2 minutes!", description=desc,color=embedColor)
                imageURL = "attachment://dont_try_to_cheat.png"
                embedVar.set_image(url=imageURL)
                await message.channel.send(embed = embedVar,file = file);

                #delete the files
                shutil.rmtree(f"cogs/GuessThatShipgirl/{encodedMessage}")

            #set timeout. 120 = 2 minutes.
            await asyncio.sleep(120)
            #If game is still running, end.
            if (getChannelDataEncoded(encodedMessage) != 0):
                if (getChannelDataEncoded(encodedMessage)[0] == shipData):
                    #Send time out embed. I have to make this a function.
                    desc = "";
                    if mode == 'endless':
                        desc = "Endless mode has been ended due to a timeout."
                    embedVar = discord.Embed(title=f"The game timed out. {shipData['name']} was the correct answer.",description = desc, color=embedColor)
                    imageURL = shipData['skin']['image']
                    embedVar.set_image(url=imageURL)
                    await message.channel.send(embed = embedVar);

                    #Delete data to end the game
                    deleteChannelDataEncoded(encodedMessage);

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
    @commands.command(aliases = ["g"])
    async def guess(self, message, *args):

        #Combine the args into one so it is easier to referance later
        arg = " ".join(args);


        #Help menu embed.
        if (arg == 'help'):
            embed = discord.Embed(title = "Guess Game Help Menu")
            embed.add_field(name =":small_red_triangle: ;guess", value = "Start a guessing game\n`s` to add skins.\n`r` to remove retrofit skins.\n`d` to remove default skins.\n`endless` to play in endless mode.\nex. `;guess s d`", inline = False)
            embed.add_field(name =":small_red_triangle: ;guess stop", value = "Ends a guessing game if one is running.", inline = False)
            embed.add_field(name =":small_red_triangle: ;guess [Shipgirl Name]", value = 'Guess a shipgirl.\nex.`;guess Howe`\nex.`;guess Long Island`', inline = False)

            await message.channel.send(embed = embed);

        #Handle player giving up
        elif (arg.find('give') != -1 or arg.find('stop') != -1 or arg.find('quit') != -1 or arg.find('give up') != -1 or arg.find('giveup') != -1 or (arg.find('end') != -1 and arg.find('endless') == -1) or arg.find('skip') != -1):
            if getChannelData(message) != 0:
                #Find out what the answer was
                data = getChannelData(message);
                ans = data[0]['name'];

                #Delete the game from memory
                deleteChannelData(message);

                #Send the embed for timeout
                embedVar = discord.Embed(title=f"{message.author} stopped the game. The correct answer was {ans}.",color=embedColor)
                imageURL = data[0]['skin']['image']
                embedVar.set_image(url=imageURL)
                await message.channel.send(embed = embedVar);

                #if endless mode, start the next game.
                if data[3] == 'endless' and not 'endless' in args:
                    await startGame(message,data[1],data[2]);
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
                await startGame(message,encodeChannel(message),args);

            else:
                ans = data[0]['name'];
                #Do all the special checks
                arg2 = arg.lower().replace('"','');

                arg2 = getNickname(arg2);

                #Here is where special characters are handled. Ex. Muse, special o, e, and a.
                if (ans.lower().replace('ö','o').replace('é', 'e').replace('â','a').replace('µ','muse') == arg2):
                    c = True;

                if (ans.lower() == arg2):
                    c = True;

                if (c == True):
                    #win the game
                    deleteChannelData(message);

                    embedVar = discord.Embed(title=f"Hooray! {ans} was the correct answer!", color=embedColor)
                    imageURL = data[0]['skin']['image']
                    embedVar.set_image(url=imageURL)
                    await message.channel.send(embed = embedVar);

                    #if endless, start a new game.
                    if data[3] == 'endless':
                        await startGame(message,data[1],data[2]);

            #If the answer was not correct, its incorrect. Tell the player that.
            if (c == False):
                #check if answer is included
                if (len(arg) == 0):
                    await message.channel.send(f"You must include an answer!");
                else:
                    await message.channel.send(f"{arg.title()} was not the correct answer.");



#set this up with cogs and pray it works
def setup(client):
    client.add_cog(GuessThatShipgirl(client))
