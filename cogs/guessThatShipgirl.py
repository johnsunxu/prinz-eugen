import discord
import random
from discord.ext import commands
import asyncio
import json
import hashlib
import os

#encode channel function
def encodeChannel(message):
    return str(message.guild.name) +":"+ str(message.channel);

def loadChannelList():
    with open('cogs/channelList.json') as json_file:
        return json.load(json_file);
def saveChannelList(data):
    with open('cogs/channelList.json', 'w') as outfile:
        json.dump(data, outfile)
def saveChannelData(message, data):
    list = loadChannelList()
    list[encodeChannel(message)] = data
    saveChannelList(list)
def getChannelData(message):
    data = loadChannelList();
    if encodeChannel(message) in data:
        return data[encodeChannel(message)]
    else:
        return 0;
def deleteChannelData(message):
    list = loadChannelList()
    list.pop(encodeChannel(message),None)
    saveChannelList(list)

#create class
class GuessThatShipgirl(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    #Main function
    @commands.command(aliases = ["guess"])
    async def run(self, message, arg):

        if (arg == 'start'):
            if getChannelData(message) != 0:
                #The channel has a game running. Send error.
                await message.channel.send('This channel already has a game running! Try again in a different channel or wait until this game is over.');

            else:
                #The channel does not have a game running. Start it.
                #set answer
                answer = random.choice(os.listdir("cogs\GuessThatShipgirl\ImageNormal\default")).replace('Default.png','');
                #Save to outfile
                saveChannelData(message,answer);

                #send start embed
                embedVar = discord.Embed(title='Guess The Shipgirl with ";guess [name]"', color=0x00ff00)
                imageLoc = f'cogs\GuessThatShipgirl\ImageSilhouette\default\{hashlib.sha224((answer+"Default.png").encode("utf-8")).hexdigest()}.png';
                file = discord.File(imageLoc, filename="Do Not Cheat.png");
                await message.channel.send("Guess the Shipgirl with ;guess [name]! You have 2 minutes!",file = file);


                #set timeout
                await asyncio.sleep(120)
                #If game is still running, end.
                if (getChannelData(message) != 0):
                    await message.channel.send("Timeout");
                    deleteChannelData(message);

        elif (arg == 'give' or arg == 'give up'):
            ans = getChannelData(message);
            file = discord.File(f'cogs\GuessThatShipgirl\ImageNormal\default\{ans}Default.png', filename="Do Not Cheat.png");
            await message.channel.send(f"{message.author} ended the game. The correct answer was {ans}.", file = file);
            deleteChannelData(message);
        else:
            #determine if game is running
            ans = getChannelData(message);
            if ans == 0:
                await message.channel.send("A game is not running right now. Start a new game with ;guess start!");
            elif ans.lower() == arg.lower():
                file = discord.File(f'cogs\GuessThatShipgirl\ImageNormal\default\{ans}Default.png', filename="Do Not Cheat.png");
                await message.channel.send(f"Hooray! {ans} was the correct answer!", file = file);
                deleteChannelData(message);
            else:
                await message.channel.send(f"{arg} was not the correct answer.");




def setup(client):
    client.add_cog(GuessThatShipgirl(client))
