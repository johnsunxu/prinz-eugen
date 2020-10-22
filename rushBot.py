import random
import discord
import os
from discord.ext import commands


client = commands.Bot(command_prefix = ";")
client.remove_command("help")
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


#client.run("NzU1OTc4MzQyMjg4NzE5OTgy.X2LJsg.5llVkpjjXdq2WufOHOaXCMLTdWo")
client.run("NzMzOTkyODM2ODczMzIyNTI3.XxLOGQ.lOPYsnq0sdEIDE9EdhowJPnAg8c")
