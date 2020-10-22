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

shipgirlNames = ["	Universal Bulin	",
"	Prototype Bulin MKII	",
"	Specialized Bulin Custom MKIII	",
"	Dewey	",
"	Cassin	",
"	Downes	",
"	Gridley	",
"	Craven	",
"	McCall	",
"	Maury	",
"	Fletcher	",
"	Charles Ausburne	",
"	Thatcher	",
"	Aulick	",
"	Foote	",
"	Spence	",
"	Benson	",
"	Laffey	",
"	Sims	",
"	Hammann	",
"	Eldridge	",
"	Omaha	",
"	Raleigh	",
"	Brooklyn	",
"	Phoenix	",
"	Helena	",
"	Atlanta	",
"	Juneau	",
"	San Diego	",
"	Cleveland	",
"	Columbia	",
"	Pensacola	",
"	Salt Lake City	",
"	Northampton	",
"	Chicago	",
"	Houston	",
"	Portland	",
"	Indianapolis	",
"	Astoria	",
"	Quincy	",
"	Vincennes	",
"	Wichita	",
"	Baltimore	",
"	Nevada	",
"	Oklahoma	",
"	Pennsylvania	",
"	Arizona	",
"	Tennessee	",
"	California	",
"	Colorado	",
"	Maryland	",
"	West Virginia	",
"	North Carolina	",
"	Washington	",
"	South Dakota	",
"	Long Island	",
"	Bogue	",
"	Langley	",
"	Lexington	",
"	Saratoga	",
"	Ranger	",
"	Yorktown	",
"	Enterprise	",
"	Hornet	",
"	Wasp	",
"	Vestal	",
"	Amazon	",
"	Acasta	",
"	Ardent	",
"	Beagle	",
"	Bulldog	",
"	Comet	",
"	Crescent	",
"	Cygnet	",
"	Foxhound	",
"	Fortune	",
"	Grenville	",
"	Glowworm	",
"	Hardy	",
"	Hunter	",
"	Javelin	",
"	Juno	",
"	Vampire	",
"	Leander	",
"	Achilles	",
"	Ajax	",
"	Dido	",
"	Southampton	",
"	Sheffield	",
"	Gloucester	",
"	Edinburgh	",
"	Belfast	",
"	Arethusa	",
"	Galatea	",
"	Aurora	",
"	London	",
"	Shropshire	",
"	Kent	",
"	Suffolk	",
"	Norfolk	",
"	Dorsetshire	",
"	York	",
"	Exeter	",
"	Renown	",
"	Repulse	",
"	Hood	",
"	Queen Elizabeth	",
"	Warspite	",
"	Nelson	",
"	Rodney	",
"	King George V	",
"	Prince of Wales	",
"	Duke of York	",
"	Hermes	",
"	Unicorn	",
"	Eagle	",
"	Ark Royal	",
"	Illustrious	",
"	Victorious	",
"	Formidable	",
"	Glorious	",
"	Erebus	",
"	Terror	",
"	Fubuki	",
"	Ayanami	",
"	Akatsuki	",
"	Hibiki	",
"	Ikazuchi	",
"	Inazuma	",
"	Shiratsuyu	",
"	Yuudachi	",
"	Shigure	",
"	Yukikaze	",
"	Kagerou	",
"	Shiranui	",
"	Nowaki	",
"	Hatsuharu	",
"	Wakaba	",
"	Hatsushimo	",
"	Ariake	",
"	Yuugure	",
"	Kuroshio	",
"	Oyashio	",
"	Yuubari	",
"	Nagara	",
"	Isuzu	",
"	Kinu	",
"	Abukuma	",
"	Mogami	",
"	Mikuma	",
"	Furutaka	",
"	Kako	",
"	Aoba	",
"	Kinugasa	",
"	Myoukou	",
"	Nachi	",
"	Ashigara	",
"	Takao	",
"	Atago	",
"	Maya	",
"	Choukai	",
"	Kongou	",
"	Hiei	",
"	Haruna	",
"	Kirishima	",
"	Fusou	",
"	Yamashiro	",
"	Ise	",
"	Hyuuga	",
"	Nagato	",
"	Mutsu	",
"	Kii	",
"	Tosa	",
"	Hiyou	",
"	Junyou	",
"	Houshou	",
"	Shouhou	",
"	Ryuujou	",
"	Akagi	",
"	Kaga	",
"	Souryuu	",
"	Hiryuu	",
"	Shoukaku	",
"	Zuikaku	",
"	Taihou	",
"	Shinano	",
"	Akashi	",
"	Z1	",
"	Z23	",
"	Z25	",
"	Königsberg	",
"	Karlsruhe	",
"	Köln	",
"	Leipzig	",
"	Admiral Hipper	",
"	Prinz Eugen	",
"	Deutschland	",
"	Admiral Graf Spee	",
"	Scharnhorst	",
"	Gneisenau	",
"	Bismarck	",
"	Tirpitz	",
"	Graf Zeppelin	",
"	An Shan	",
"	Fu Shun	",
"	Chang Chun	",
"	Tai Yuan	",
"	Yat Sen	",
"	Ning Hai	",
"	Ping Hai	",
"	Avrora	",
"	Bailey	",
"	Z19	",
"	Z20	",
"	Z21	",
"	Z46	",
"	Kamikaze	",
"	Matsukaze	",
"	Mutsuki	",
"	Kisaragi	",
"	Uzuki	",
"	Minazuki	",
"	Fumizuki	",
"	Nagatsuki	",
"	Mikazuki	",
"	Kawakaze	",
"	Kiyonami	",
"	Niizuki	",
"	Harutsuki	",
"	Yoizuki	",
"	Radford	",
"	Jenkins	",
"	Nicholas	",
"	Richmond	",
"	Honolulu	",
"	St. Louis	",
"	Jupiter	",
"	Jersey	",
"	Sendai	",
"	Jintsuu	",
"	Naka	",
"	Urakaze	",
"	Isokaze	",
"	Hamakaze	",
"	Tanikaze	",
"	Mikasa	",
"	Agano	",
"	Noshiro	",
"	Matchless	",
"	Musketeer	",
"	Fiji	",
"	Jamaica	",
"	Montpelier	",
"	Denver	",
"	Asashio	",
"	Ooshio	",
"	Michishio	",
"	Arashio	",
"	Little Bel	",
"	Abercrombie	",
"	Sussex	",
"	I-19	",
"	I-26	",
"	I-58	",
"	U-81	",
"	Dace	",
"	U-47	",
"	U-557	",
"	Z35	",
"	Z18	",
"	Le Triomphant	",
"	Forbin	",
"	Émile Bertin	",
"	Surcouf	",
"	Le Mars	",
"	Dunkerque	",
"	Jean Bart	",
"	Massachusetts	",
"	Bush	",
"	Centaur	",
"	Essex	",
"	Albacore	",
"	Le Téméraire	",
"	Memphis	",
"	Newcastle	",
"	Hobby	",
"	Kalk	",
"	Minneapolis	",
"	Hazelwood	",
"	Concord	",
"	Amagi	",
"	Kaga (Battleship)	",
"	Hatakaze	",
"	Makinami	",
"	Sirius	",
"	Curacoa	",
"	Curlew	",
"	Kimberly	",
"	Mullany	",
"	Chaser	",
"	Independence	",
"	Shangri-La	",
"	Z2	",
"	Bunker Hill	",
"	I-13	",
"	Suzuya	",
"	Hiei-chan	",
"	Akagi-chan	",
"	Zeppy	",
"	U-556	",
"	U-73	",
"	Z36	",
"	Echo	",
"	Lena	",
"	Clevelad	",
"	Li'l Sandy	",
"	Swiftsure	",
"	Le Malin	",
"	L'Opiniâtre	",
"	I-25	",
"	I-56	",
"	I-168	",
"	U-101	",
"	U-522	",
"	Alabama	",
"	Cavalla	",
"	Bataan	",
"	San Juan	",
"	Birmingham	",
"	Aylwin	",
"	Bache	",
"	Black Prince	",
"	Stanly	",
"	Littorio	",
"	Conte di Cavour	",
"	Giulio Cesare	",
"	Zara	",
"	Trento	",
"	Carabiniere	",
"	U-110	",
"	Smalley	",
"	Gascogne µ	",
"	Akagi µ	",
"	Cleveland µ	",
"	Sheffield µ	",
"	Admiral Hipper µ	",
"	Glasgow	",
"	Kasumi	",
"	Suruga	",
"	Ryuuhou	",
"	Halsey Powell	",
"	Biloxi	",
"	Uranami	",
"	Grozny	",
"	Minsk	",
"	Tashkent	",
"	Pamiat Merkuria	",
"	Chapayev	",
"	Gangut	",
"	Sovetskaya Rossiya	",
"	Intrepid	",
"	Bremerton	",
"	Cooper	",
"	Reno	",
"	Bluegill	",
"	Casablanca	",
"	Marblehead	",
"	Hanazuki	",
"	Naganami	",
"	Little Renown	",
"	Tartu	",
"	Richelieu	",
"	Jeanne d'Arc	",
"	Algérie	",
"	La Galissonnière	",
"	Vauquelin	",
"	Béarn	",
"	Little Illustrious	",
"	Eskimo	",
"	Howe	",
"	Perseus	",
"	Hermione	",
"	Valiant	",
"	Icarus	",
"	Z26	",
"	U-96	",
"	Suzutsuki	",
"	Kumano	",
"	Chitose	",
"	Chiyoda	",
"	Kashino	",
"	Princeton	"]
embedColor = 0xf01111

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
                answer = random.choice(shipgirlNames).replace('\t','');
                #Save to outfile
                saveChannelData(message,answer);

                #send start embed
                embedVar = discord.Embed(title="Guess the Shipgirl with ;guess [name]! You have 2 minutes!", color=embedColor)
                imageURL = f'https://github.com/Drakomire/AzurLaneShipgirls/blob/master/ImageSilhouette/default/{hashlib.sha224((answer+"Default.png").encode("utf-8")).hexdigest()}.png?raw=true';
                embedVar.set_image(url=imageURL)
                await message.channel.send(embed = embedVar);

                #set timeout
                await asyncio.sleep(120)
                #If game is still running, end.
                if (getChannelData(message) != 0):
                    if (getChannelData(message) == answer):
                        embedVar = discord.Embed(title=f"The game timed out. {answer} was the correct answer.", color=embedColor)
                        imageURL = f'https://github.com/Drakomire/AzurLaneShipgirls/blob/master/ImageNormal/default/{answer}Default.png?raw=true';
                        embedVar.set_image(url=imageURL)
                        await message.channel.send(embed = embedVar);

        elif (arg == 'give' or arg == 'give up'):
            ans = getChannelData(message);
            embedVar = discord.Embed(title=f"{message.author} stopped the game. The correct answer was {ans}.", color=embedColor)
            imageURL = f'https://github.com/Drakomire/AzurLaneShipgirls/blob/master/ImageNormal/default/{ans}Default.png?raw=true';
            embedVar.set_image(url=imageURL)
            await message.channel.send(embed = embedVar);


            deleteChannelData(message);
        else:
            #determine if game is running
            ans = getChannelData(message);
            if ans == 0:
                await message.channel.send("A game is not running right now. Start a new game with ;guess start!");
            elif ans.lower() == arg.lower():
                embedVar = discord.Embed(title=f"Hooray! {ans} was the correct answer!", color=embedColor)
                imageURL = f'https://github.com/Drakomire/AzurLaneShipgirls/blob/master/ImageNormal/default/{ans}Default.png?raw=true';
                embedVar.set_image(url=imageURL)
                await message.channel.send(embed = embedVar);


                deleteChannelData(message);
            else:
                await message.channel.send(f"{arg} was not the correct answer.");




def setup(client):
    client.add_cog(GuessThatShipgirl(client))
