import discord
import gspread
import pytz
import jellyfish
import psycopg2
import sys
import os
from datetime import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path



#Check if user entered correct servers
def checkServerInput(server):
    global avrora_cur,washington_cur,lexington_cur,amagi_cur,sandy_cur, avrora_conn,washington_conn,lexington_conn,amagi_conn,sandy_conn

    validServer = False
    serverList = ["Avrora", "Sandy", "Washington", "Lexington", "Amagi"]
    cursorList= [avrora_cur,sandy_cur,washington_cur,lexington_cur,amagi_cur]
    connectionList =[avrora_conn,sandy_conn,washington_conn,lexington_conn,amagi_conn]

    for i in range(len(serverList)):
        if validServer == False:
            #print(server.lower(), i.lower())
            if server.lower() == serverList[i].lower():
                server = serverList[i]
                validServer = True
                cursor = cursorList[i]
                connection = connectionList[i]
    return validServer, server,cursor, connection

#procedure for updating the time the bot is at in PST/MOUNTAIN
def updateTime():
    global serverTime, time, date
    serverTime = datetime.now(pytz.timezone("US/Mountain"))
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


# def sendData(server, data):

#     sheet = updateSpreadsheet(server)
#     sheet.append_row(data, value_input_option="USER_ENTERED")
def sendData(server, serverCursor, serverConnection, rusherName, time, date, reporterName):
    #find out entry number
    serverCursor.execute(f"SELECT * FROM {server.lower()}_entries;")
    entryNumber = serverCursor.fetchall()[len(serverCursor.fetchall())-1][0]+1
    print("ENTRY NUM IS", entryNumber)
    print(f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    serverCursor.execute(f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    serverConnection.commit()
#create class


class CheckPlayer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["analyzemulti", "analyzeMulti"])
    async def analyze(self, ctx, server, *players):
        await ctx.send("Sorry this command is currently under maintenance.")
        return
        
        #Check if user entered correct servers
        if checkServerInput(server)[0] != True:
            await ctx.send("Server input incorrect!")
            return
        else:
            server = checkServerInput(server)[1]
            serverCursor = checkServerInput(server)[2]
            serverConnection = checkServerInput(server)[3]

        #Check if user has entered too many arguments
        # if len(extraArgs) != 0:
        #     print(extraArgs)
        #     await ctx.send("No spaces! Use \" \" for names with spaces.")
        #     return

        #Receive variables
        sheet = updateSpreadsheet(server)
        # sheetData = sheet.get_all_records()
        serverCursor.execute(f"SELECT * FROM {server}_entries;")
        sheetData = serverCursor.fetchall()
        storedPlayerData = []
        rows = []
        playerInput = []
        for player in players:
            playerInput.append(player)
        playerOutput = []
        #add lists for each player inputted
        for i in range(len(playerInput)):
            playerOutput.append([])

        #Add rows to variable rows
        for i in range(len(sheetData)):
            rows.append([sheetData[i].get("Server"), sheetData[i].get("User"), sheetData[i].get("Time"), sheetData[i].get("Date")])
        #Create variable to find the column that contains the player
        for row in range(len(sheetData)):
            storedPlayerData.append(sheetData[row].get("User"))

        #Loop through number of players
        for i in range(len(playerInput)):
            #Loop through the spreadsheet
            for j in range(len(storedPlayerData)):
                #Check the player matches
                # if playerInput[i].strip() == storedPlayerData[j].strip():
                #     playerOutput[i].append(rows[j])
                #check percent match
                if jellyfish.damerau_levenshtein_distance(playerInput[i].strip().lower(), storedPlayerData[j].strip().lower())/len(storedPlayerData[j].strip()) <= 0.18:
                    playerOutput[i].append(rows[j])

        #Create output string
        await ctx.send("Reminder: Times are in server time!")
        str = ""
        for i in range(len(playerInput)):
            #Check if player isn't found
            if len(playerOutput[i]) == 0:
                str += playerInput[i]+" not found. \n"
                continue
            str += playerInput[i]+":```+\n"
            for report in playerOutput[i]:
                str += ", ".join(report)+"\n"
            str += "```"
        await ctx.send(str)

    @commands.command(aliases=["addplayer"], brief="Add player to spreadsheet in UTC time.")
    async def addPlayer(self, ctx, server, playerName, customTime="0", customDate="0", *extraArgs):
        
        # await ctx.send("Sorry this command is currently under maintenance.")
        # return

        #Update Spreadsheet
        #updateSpreadsheet()
        updateTime()

        #Check if player has entered too few arguments
        if playerName == None:
            await ctx.send("Remember to input the server!")
            return

        #Check if player has entered too many arguments
        if len(extraArgs) != 0 and customTime == None and customDate == None:
            print(extraArgs)
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return

        #Check customTime and customDate
        try:
            customTime = int(customTime)
            customDate = int(customDate)
        except:
            await ctx.send("No spaces! Use \" \" for names with spaces.")
            return

        #Check if user entered correct servers
        if checkServerInput(server)[0] != True:
            await ctx.send("Server input incorrect!")
            return
        else:
            server = checkServerInput(server)[1]
            serverCursor = checkServerInput(server)[2]
            serverConnection = checkServerInput(server)[3]

        #Remove white spaces
        playerName = playerName.strip()
        #Create list of player data
        deltaTime = timedelta(days=customDate, minutes=customTime)
        global serverTime
        temp = serverTime-deltaTime
        time = temp.strftime("%H:%M:%S")
        date = temp.strftime("%d/%m/%Y")
        reporterName = ctx.message.author.name

        # dataEntry = [server, playerName, temp.strftime("%H:%M:%S"), temp.strftime("%d/%m/%Y"), ctx.message.author.name]
        #Add to sheet
        sendData(server, serverCursor, serverConnection,playerName,time,date,reporterName)
        # sheet.append_row(dataEntry, value_input_option="USER_ENTERED")
        await ctx.send("Data entry successful!")
        #updateSpreadsheet()
        return


def setup(client):
    client.add_cog(CheckPlayer(client))

#Database connections
load_dotenv(dotenv_path="./dev.env")
DATABASE_URL = os.getenv('DATABASE_URL')
avrora_db = DATABASE_URL
amagi_db = os.getenv('HEROKU_POSTGRESQL_SILVER_URL')
sandy_db = os.getenv('HEROKU_POSTGRESQL_COPPER_URL')
lexington_db = os.getenv('HEROKU_POSTGRESQL_MAROON_URL')
washington_db = os.getenv('HEROKU_POSTGRESQL_GREEN_URL')

print(avrora_db)

avrora_conn = psycopg2.connect(avrora_db,sslmode="allow")
amagi_conn = psycopg2.connect(amagi_db, sslmode="allow")
sandy_conn = psycopg2.connect(sandy_db, sslmode="allow")
lexington_conn=psycopg2.connect(lexington_db, sslmode="allow")
washington_conn=psycopg2.connect(washington_db,sslmode="allow")

avrora_cur=avrora_conn.cursor()
amagi_cur=amagi_conn.cursor()
sandy_cur=sandy_conn.cursor()
lexington_cur=lexington_conn.cursor()
washington_cur=washington_conn.cursor()

#Set variables
playerFound = False

#Variables for spreadsheet
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
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
