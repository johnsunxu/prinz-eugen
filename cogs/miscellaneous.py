import discord
import random
from discord.ext import commands
import json

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

        #Clear out channelList
        with open('cogs/channelList.json', 'w') as outfile:
            json.dump({}, outfile)

    #Coinflip function
    @commands.command(aliases = ["flipcoin", "coinflip"])
    async def flipCoin(self, ctx):
        reply = ["Heads","Heads","Tails","Tails","Tails","Tails"]
        await ctx.send("%s" %(random.choice(reply)))

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title = "Help Menu")

        embed.add_field(name =":small_red_triangle: ;addPlayer [server] [player] [minutes from present, default 0] [days from present, default 0]", value = "Create a report on a rusher.\nExample `;addPlayer Avrora test123`", inline = False)

        embed.add_field(name = ":small_red_triangle: ;analyze [server] [player1] [player2]...", value = "Displays reports on a player.\nExample: `;analyze Avrora test123 \"test 123\"`", inline = False)

        embed.add_field(name = ":small_red_triangle: ;flipcoin", value = "Displays the result of a unbiased coin flip.", inline = False)

        embed.add_field(name = ":small_red_triangle: ;patchNotes", value = "Displays patch notes.", inline = False)

        embed.add_field(name = ":small_red_triangle: ;guess help", value = "Shows how to play the shipgirl guessing game.", inline = False)

        embed.add_field(name = ":small_red_triangle: ;ehp help", value = "Shows how to calculate eHP for a ship in exercises.", inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases=["patchnotes"])
    async def patchNotes(self, ctx):
        embed = discord.Embed(title = "Patch Notes - December 12th 2020")
        embed.add_field(name ="Version 1.82", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "**NEW** eHP calculator now supports PvE by using the argument PvE. Damage reduction support is also added.")
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
