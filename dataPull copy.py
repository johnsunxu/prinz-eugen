import discord
import gspread
import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands 



#create class
class CheckPlayer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        global time 
        time = message.created_at
        print(time)
    
    @commands.command(aliases = ["test"])
    async def analyze(self, ctx, playerName, *extraArgs):
        #Check if player has entered too many arguments
        if len(extraArgs) != 0: 
            print(extraArgs)
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return

        global playerFound
        #Search each cell in the player column for the inputted player
        for i in range(len(storedPlayerData)): 
            #Check if player is found in spreadsheet
            if playerName == storedPlayerData[i]:
                #Send message with value
                #Only send "Here is the player data" if it is the first time 
                if playerFound == False: 
                    await ctx.send(f"Here is the player data \n{rows[i]} \n")
                else: 
                    await ctx.send(f"{rows[i]} \n")
                #Set playerFound to True now that the player has been found 
                playerFound = True

                #print(playerName, storedPlayerData[i])
                
        if playerFound == False: 
            await ctx.send("Player not found.")
        playerFound = False    
    
    @commands.command(aliases = [""])
    async def addPlayer(self,ctx, playerName, time, date, *extraArgs):
        #Check if player has entered too many arguments
        if len(extraArgs) != 0:
            print(extraArgs)
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return
        
        #Verify data entries 
        #Check for correct time format
        if time.count(":") != 1: 
            await ctx.send("Use HH:MM format! Please put in UTC+8!")
            return
        #Check if time string is too long
        if len(time) != 5: 
            await ctx.send("Too many numbers!")
            return
        #Check if string isn't long enough, indicating no zeros
        if len(date) != 10:
            await ctx.send("Remember 0's in DD/NN/YYYY format! Please put in UTC+8!")
        #Check if month is too large, indicating wrong format
        if int(date[3:5]) > 12:
            await ctx.send("Use DD/MM/YYYY format! Please put in UTC+8!")
            return

        #Create list of player data
        dataEntry = ["Avrora", playerName, time+":00", date, "Prinz Eugen"]
        #Add to sheet
        sheet.insert_row(dataEntry, len(rows)+2)
        await ctx.send("Data entry successful!")
        return


    

        

def setup(client):
    client.add_cog(CheckPlayer(client))


#Set variables
playerFound = False


#Variables for spreadsheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json",scope)
client = gspread.authorize(creds)


#Open sheet
sheet = client.open("Azur Lane Avrora PvP Exercise log").sheet1
#Obtain data
sheetData = sheet.get_all_records()

storedPlayerData = []
rows = []
#Add rows to variable rows
for i in range(len(sheetData)): 
    rows.append([sheetData[i].get("Server"), sheetData[i].get("User"), sheetData[i].get("Time"), sheetData[i].get("Date")])

#Create variable to find the column that contains the player  
for row in range(len(sheetData)):
    storedPlayerData.append(sheetData[row].get("User")) 

