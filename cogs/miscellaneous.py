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
        reply = ["Heads","Heads","Heads","Tails","Tails"]
        await ctx.send("%s" %(random.choice(reply)))

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title = "Help Menu")

        embed.add_field(name =":small_red_triangle: ;addPlayer [server] [player] [minutes from present, default 0] [days from present, default 0]", value = "Create a report on a rusher.\nExample `;addPlayer Avrora test123`", inline = False)

        embed.add_field(name = ":small_red_triangle: ;analyze [server] [player1] [player2]...", value = "Displays reports on a player.\nExample: `;analyze Avrora test123 \"test 123\"`", inline = False)

        #embed.add_field(name = ":small_red_triangle: ;analyzeMulti [server] [player1] [player2] [player3] [player4]", value = "Displays report for four players\nExample: `;analyzeMulti Avrora \"Test one\" test2 test3 test4`",inline = False)

        embed.add_field(name = ":small_red_triangle: ;flipcoin", value = "Displays the result of a unbiased coin flip.", inline = False)

        embed.add_field(name = ":small_red_triangle: ;patchNotes", value = "Displays patch notes.", inline = False)

        embed.add_field(name = ":small_red_triangle: ;guess help", value = "Shows how to play the shipgirl guessing game.", inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases=["patchnotes"])
    async def patchNotes(self, ctx):
        embed = discord.Embed(title = "Patch Notes - October 23rd 2020")
        embed.add_field(name ="Version 1.4B", value = "** **", inline = False)
        embed.add_field(name = "** **", value = "**UPDATED** ;analyze is now not case sensitive and looks for match up to 82%", inline = False)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
