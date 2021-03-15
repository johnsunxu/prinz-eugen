import random
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = ";")
client.remove_command("help")

@client.event
async def on_message(message):
    # do some extra stuff here
    if message.author.bot == False and message != None and message.content.startswith(';') and message.guild:
        await client.process_commands(message)
        print(message.guild)

    #yell at people in #meta-help
    channel = 643697081210503168 #769323138009661484;
    if message.channel.id == channel and message.author.bot == True and message.content != 'Please avoid using bots unless part of a discussion!':
        #whitelist
        lastMessages = await message.channel.history(limit=5).flatten();

                    #FCLC,              Drakomire           Solle               Tipin               Smugg                 TheStrictNein     Fire                AwkwardNinja        Endiku              Tsubonk
        whitelist = [517171091060293633, 318076068290494466,256098495667240961, 820729385983410256, 181096628394917889, 324219750790201345, 820729887659917332, 170431340448186370, 199713237636349952, 184925630998118400,
        #Loxi               #Mirrage Rebellion  #Fal               #Captain Mika        dontcallmeFFC
        299903786422632448, 158331365757157376, 218864290646458368, 799884633042845716, 494130472859729922];



        if not lastMessages[1].author.id in whitelist:
            await message.channel.send("Please avoid using bots unless part of a discussion!");

#Load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Load successful!")

#Unload cogs
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Unload successful!")

#Scan for cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.environ.get('token'))
