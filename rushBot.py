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
    if message.channel.id == 643697081210503168 and message.author.bot == True and message.content != "Dont use bots in #meta-help-discussion! <:Shinei:820504358071828492>":
        print(message.content);
        await message.channel.send("Dont use bots in #meta-help-discussion! <:Shinei:820504358071828492>");

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
