import discord
import random
from discord.ext import commands

#create class
class Miscellaneous(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        #Set status of bot
        await self.client.change_presence(status=discord.Status.online, activity = discord.Game("Exercises"))

    #Coinflip function
    @commands.command(aliases = ["flipcoin", "coinflip"])
    async def flipCoin(self, ctx):
        reply = ["Heads","Heads","Heads","Tails","Tails"]
        await ctx.send("%s" %(random.choice(reply)))

    @commands.command()
    async def test(self, ctx):
        await ctx.send("%s" %(ctx.message.author))
        

def setup(client):
    client.add_cog(Miscellaneous(client))
