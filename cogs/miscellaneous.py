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
    async def help(self, ctx):
        embed = discord.Embed(title = "Help Menu")

        embed.add_field(name =";addPlayer", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "```;addPlayer [server] [player] [minutes from present, default 0] [days from present, default 0]```", inline = False)
        embed.add_field(name = "** **", value = "Create a report on a rusher.", inline = False)
        embed.add_field(name = "** **", value = "Example ```;addPlayer Avrora test123```", inline = False)

        embed.add_field(name = ";analyze", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "```;analyze [server] [player]```")
        embed.add_field(name = "** **", value = "Displays reports on a player.", inline = False)
        embed.add_field(name = "** **", value = "Example: ```;analyze test123```", inline = False)

        embed.add_field(name = ";analyzeMulti", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "```;analyzeMulti [server] [player1] [player2] [player3] [player4]```")
        embed.add_field(name = "** **", value = "Displays report for four players", inline = False)
        embed.add_field(name = "** **", value = "Example: ```;analyzeMulti Avrora \"Test one\" test2 test3 test4```")

        embed.add_field(name = ";flipcoin", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "```;flipcoin```", inline = False)
        embed.add_field(name = "** **",value ="Displays the result of a coin flip.", inline = False)

        embed.add_field(name = ";patchNotes", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "```;patchNotes```", inline = False)
        embed.add_field(name = "** **", value = "Displays patch notes.", inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases=["patchnotes"])
    async def patchNotes(self, ctx):
        embed = discord.Embed(title = "Patch Notes - October 21st 2020")
        embed.add_field(name ="Version 1.2B", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "**NEW** analyzeMulti ", inline = False)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
