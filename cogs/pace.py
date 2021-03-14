import discord
import random
from discord.ext import commands
import json
from datetime import datetime
import math


#create class
class Pace(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pace(self, message, exercisesLeft, score):
        now = datetime.now()
        seconds = now.timestamp()
        exercisesStored = int(exercisesLeft);
        exercisesLeft = int(exercisesLeft);
        score = int(score);

        minutes = math.floor(seconds/60);
        hours = math.floor(minutes/60);
        days = math.floor(hours/24);

        hoursElapsed = (hours-7) %24;
        daysElapsed = (days+3)%14;

        print("Hours Elapsed " + str(hoursElapsed));
        print("Days Elapsed " + str(daysElapsed));

        resets = 0;
        if (hours > 0):
            resets += 1;

        if (hours >= 6):
            resets += 1;

        if (hours >= 12):
            resets += 1;

        print("Resets " +str(resets));


        exercisesLeft += (14-daysElapsed)*3*5 + (3-resets)*5;
        print("Exercises left " + str(exercisesLeft));

        for i in range(0,exercisesLeft):
            if score < 100:
                score += 25;
            elif score < 200:
                score += 22;
            elif score < 300:
                score += 20;
            elif score < 400:
                score += 17;
            elif score < 550:
                score += 15;
            elif score < 700:
                score += 15;
            elif score < 850:
                score += 15;
            elif score < 1050:
                score += 12;
            else:
                score += 10;


        #create the embed
        embed = discord.Embed(title = "Predicted Scores:")

        embed.add_field(name = "Season Stats:", value = f'''
        Exercises Left: {exercisesLeft}
        Days Left: {14-daysElapsed+1}
        Resets Left: {math.floor((exercisesLeft-exercisesStored)/5)}
        ''', inline = False)
        embed.add_field(name = "Predicted EOS Score:", value = str(score), inline = False)

        await message.channel.send(embed = embed);




def setup(client):
    client.add_cog(Pace(client))
