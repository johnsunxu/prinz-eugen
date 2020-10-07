import discord
import gspread
import pytz
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands 

#procedure for updating the time the bot is at in PST 
def updateTime():
    global serverTime, time, date
    serverTime = datetime.now(pytz.timezone("US/Pacific"))
    time = serverTime.strftime("%H:%M:%S")
    date = serverTime.strftime("%d/%m/%Y")

#procedure for updating spreadsheet values
def updateSpreadsheet():
    global storedPlayerData, rows, sheetData
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



#create class
class CheckPlayer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        #Update time and date
        #global time, date 
        #time = message.created_at
        #date = time.strftime("%d/%m/%Y")
        #time = time.strftime("%H:%M:%S")
        
        updateTime()
        print(time, "\n", date)
        
    


    @commands.command(aliases = ["test"], brief = "Call for reports on the player.")
    async def analyze(self, ctx, playerName, *extraArgs):
        updateSpreadsheet()
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
    
    @commands.command(aliases = [""], brief = "Add player to spreadsheet in UTC time.")
    async def addPlayer(self,ctx, playerName, customTime = None, customDate = None, *extraArgs):
        #Update Spreadsheet
        updateSpreadsheet()
        updateTime()
        #Check if player has entered too many arguments
        if len(extraArgs) != 0 and customTime == None and customDate == None:
            print(extraArgs)
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return
        #Create list of player data
        global time, date
        if customTime != None and customDate != None: 
            dataEntry = ["Avrora", playerName, customTime, customDate, "Prinz Eugen"]
        else:
            dataEntry = ["Avrora", playerName, time, date, "Prinz Eugen"]
        #Add to sheet
        sheet.append_row(dataEntry, value_input_option="USER_ENTERED")
        await ctx.send("Data entry successful!")
        #updateSpreadsheet()
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

