import discord
import random
from discord.ext import commands
import json
from datetime import datetime
import math
from rushBot import client


#create class
class Pace(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pace(self, message, exercisesLeft, score):
        now = datetime.now()
        seconds = now.timestamp()

        # seconds -= 10 * 60 * 60 * 24
        # seconds -= 60 * 60

        if not (exercisesLeft.isdigit() and score.isdigit()):
            await message.channel.send("This command only takes numbers you pepega!")
            return

        exercisesLeft = min(10,int(exercisesLeft))
        exercisesStored = exercisesLeft
        score = int(score)

        if (score > 9999 or  exercisesLeft > 9999):
            await message.channel.send(f"Stop trying to break the bot <:Shinei:820504358071828492>")
            return

        minutes = math.floor(seconds/60)
        hours = math.floor(minutes/60)-7
        days = math.floor(hours/24)

        hoursElapsed = (hours) %24
        # print("Days " + str(days))

        daysElapsed = (days+3)%14+1

        # print("Hours Elapsed " + str(hoursElapsed))
        # print("Days Elapsed " + str(daysElapsed))

        resets = 0
        if (hoursElapsed >= 0):
            resets += 1

        if (hoursElapsed >= 12):
            resets += 1

        if (hoursElapsed >= 18):
            resets += 1

        # print("Resets " +str(resets))


        exercisesLeft += (14-daysElapsed)*3*5 + (3-resets)*5

        #4 different scores are calculated here for more accuracy
        negOneScore = score
        plusOneScore = score
        plusTwoScore = score

        def calculateScoreToAdd(score):
            gain = 0
            if score < 100:
                gain = 25
            elif score < 200:
                gain = 22
            elif score < 300:
                gain = 20
            elif score < 400:
                gain = 17
            elif score < 550:
                gain = 15
            elif score < 700:
                gain = 15
            elif score < 850:
                gain = 15
            elif score < 1050:
                gain = 12
            else:
                gain = 10
            
            return gain
            
        for i in range(0,exercisesLeft):
            score += calculateScoreToAdd(score)
            negOneScore += calculateScoreToAdd(negOneScore)
            plusOneScore += calculateScoreToAdd(plusOneScore)
            plusTwoScore += calculateScoreToAdd(plusTwoScore)

            #Bonus points will be given on the first exercise of a reset
            if ((exercisesLeft-i) % 5 == 0):
                negOneScore -= 1
                plusOneScore += 1
                plusTwoScore += 2


        #create the embed
        embed = discord.Embed(title = "Predicted Scores:")

        embed.add_field(name = "Season Stats:", value = f'''
        Exercises Left: {exercisesLeft}
        Full Days Left: {14-daysElapsed}
        Resets Left: {math.floor((exercisesLeft-exercisesStored)/5)}
        ''', inline = False)
        embed.add_field(name = "Predicted EOS Scores:", value = f'''
        `-1:` {negOneScore}
        `+0:` {score}
        `+1:` {plusOneScore}
        `+2:` {plusTwoScore}
        ''', inline = False)

        await message.channel.send(embed = embed)




def setup(client):
    client.add_cog(Pace(client))
