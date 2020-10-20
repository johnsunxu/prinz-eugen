import discord
import gspread
import pytz
from datetime import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands 

#Check if user entered correct servers
def checkServerInput(server):
       
    validServer = False
    serverList = ["Avrora", "Sandy", "Washington", "Lexington", "Amagi"]

    for i in serverList:
        if validServer == False:
            print(server.lower(), i.lower())
            if server.lower() == i.lower():
                server = i
                validServer = True
    return validServer,server

#procedure for updating the time the bot is at in PST 
def updateTime():
    global serverTime, time, date
    serverTime = datetime.now(pytz.timezone("US/Pacific"))
    time = serverTime.strftime("%H:%M:%S")
    date = serverTime.strftime("%d/%m/%Y")
    print(time)
    print(date)

#procedure for updating spreadsheet values
def updateSpreadsheet(server):
    #global storedPlayerData, rows, sheetData
    #Obtain data
    sheet = client.open("Azur Lane Avrora PvP Exercise log").worksheet(server)

    return sheet

def sendData(server, data): 
    
    sheet = updateSpreadsheet(server)
    sheet.append_row(data, value_input_option="USER_ENTERED")

#create class
class CheckPlayer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
    
    # @commands.Cog.listener()
    # async def on_message(self, message):        
    #     updateTime()
    #     print(time, "\n", date)

    @commands.command(aliases = [], brief = "Call for reports on the player.")
    async def analyze(self, ctx, server, playerName, *extraArgs):
        #Check if user entered correct servers
        if checkServerInput(server)[0] != True:
            await ctx.send("Server input incorrect!")
            return
        else: 
            server = checkServerInput(server)[1]

        sheet = updateSpreadsheet(server)
        sheetData = sheet.get_all_records()
        storedPlayerData = []
        rows = []
        #Add rows to variable rows
        for i in range(len(sheetData)):
            rows.append([sheetData[i].get("Server"), sheetData[i].get("User"), sheetData[i].get("Time"), sheetData[i].get("Date")])
        #Create variable to find the column that contains the player
        for row in range(len(sheetData)):
            storedPlayerData.append(sheetData[row].get("User"))

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
    
    @commands.command(aliases = ["addplayer"], brief = "Add player to spreadsheet in UTC time.")
    async def addPlayer(self,ctx, server, playerName, customTime = 0, customDate = 0, *extraArgs):
        #Update Spreadsheet
        #updateSpreadsheet()
        updateTime()

        #Check if player has entered too many arguments
        if len(extraArgs) != 0 and customTime == None and customDate == None:
            print(extraArgs)
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return

        #Check if user entered correct servers
        if checkServerInput(server)[0] != True: 
            await ctx.send("Server input incorrect!")
            return
        else:
            server = checkServerInput(server)[1]

        #Create list of player data
        deltaTime = timedelta(days=customDate, minutes=customTime)
        global serverTime
        temp = serverTime-deltaTime
        dataEntry = [server, playerName, temp.strftime("%H:%M:%S"), temp.strftime("%d/%m/%Y"), ctx.message.author.name]
        #Add to sheet
        sendData(server, dataEntry)
        # sheet.append_row(dataEntry, value_input_option="USER_ENTERED")
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
# sheet = client.open("Azur Lane Avrora PvP Exercise log").sheet1

# #Obtain data
# sheetData = sheet.get_all_records()

# storedPlayerData = []
# rows = []
#Add rows to variable rows
# for i in range(len(sheetData)): 
#     rows.append([sheetData[i].get("Server"), sheetData[i].get("User"), sheetData[i].get("Time"), sheetData[i].get("Date")])

# #Create variable to find the column that contains the player  
# for row in range(len(sheetData)):
#     storedPlayerData.append(sheetData[row].get("User")) 

