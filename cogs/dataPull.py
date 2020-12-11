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

#procedure to re-establish connections
def reconnect():
    global avrora_conn,avrora_cur,amagi_conn,amagi_cur,sandy_conn,sandy_cur,lexington_conn,lexington_cur,washington_conn,washington_cur
    avrora_conn = psycopg2.connect(avrora_db, sslmode="allow")
    amagi_conn = psycopg2.connect(amagi_db, sslmode="allow")
    sandy_conn = psycopg2.connect(sandy_db, sslmode="allow")
    lexington_conn = psycopg2.connect(lexington_db, sslmode="allow")
    washington_conn = psycopg2.connect(washington_db, sslmode="allow")

    avrora_cur = avrora_conn.cursor()
    amagi_cur = amagi_conn.cursor()
    sandy_cur = sandy_conn.cursor()
    lexington_cur = lexington_conn.cursor()
    washington_cur = washington_conn.cursor()

#procedure to execute SQL query while accounting for errors
def _execute(ctx, server, serverCursor, serverConnection, query):
    try: 
        serverCursor.execute(query)
        serverConnection.commit()
    #If query fails, reconnect to databases
    except psycopg2.InterfaceError:
        ctx.send("Please wait, reconnecting to database.")
        reconnect()
        try: 
            serverCursor.execute(query)
            serverConnection.commit()
        #report unaccounted for errors to creator
        except: 
            ctx.send("Database error, ping SomeDude#0172")

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

#
def sendData(ctx, server, serverCursor, serverConnection, rusherName, time, date, reporterName):
    #find out entry number
    _execute(ctx, server, serverCursor, serverConnection,f"SELECT * FROM {server.lower()}_entries ORDER BY entrynumber;")
    # serverCursor.execute(f"SELECT * FROM {server.lower()}_entries ORDER BY entrynumber;")
    entryNumber = serverCursor.fetchall()[len(serverCursor.fetchall())-1][0]+1
    print("ENTRY NUM IS", entryNumber)
    print(f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    _execute(ctx, server, serverCursor, serverConnection, f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    # serverCursor.execute(f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    # serverConnection.commit()

class CheckPlayer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ["leaderboards"])
    async def leaderboard(self, ctx, server):
        #Check if user entered correct servers
        print("Checking server")
        try:
            if checkServerInput(server)[0] != True:
                await ctx.send("Server input incorrect!")
                return
            else:
                server = checkServerInput(server)[1]
                serverCursor = checkServerInput(server)[2]
                serverConnection = checkServerInput(server)[3]
        except:
            await ctx.send("Server input incorrect!")
            return
        print(f"Server is: {server}")
        _execute(ctx, server, serverCursor, serverConnection, "SELECT * FROM leaderboard ORDER BY entries DESC;")
        # serverCursor.execute("SELECT * FROM leaderboard ORDER BY entries DESC;")
        leaderboard = serverCursor.fetchall()
        str = f"{server}: \n```"
        for i in range(len(leaderboard)):
            str+=f"{leaderboard[i][0]} : {leaderboard[i][1]}\n"
        str += "```"
        await ctx.send(str)

    @commands.command(aliases=["analyzemulti", "analyzeMulti"])
    async def analyze(self, ctx, server, *players):
        # await ctx.send("Sorry this command is currently under maintenance.")
        # return

        #Check if user entered correct servers
        try:
            if checkServerInput(server)[0] != True:
                await ctx.send("Server input incorrect!")
                return
            else:
                server = checkServerInput(server)[1]
                serverCursor = checkServerInput(server)[2]
                serverConnection = checkServerInput(server)[3]
        except:
            await ctx.send("Server input incorrect!")
            return
            
        #Check if user has entered too many arguments
        # if len(extraArgs) != 0:
        #     print(extraArgs)
        #     await ctx.send("No spaces! Use \" \" for names with spaces.")
        #     return

        #Receive variables
        entries = []
        for i in range(len(players)):
            _execute(ctx,server,serverCursor,serverConnection, f"SELECT * FROM {server}_entries WHERE LOWER(rushername) LIKE LOWER(\'{players[i].lower()}\');")
            # serverCursor.execute(f"SELECT * FROM {server}_entries WHERE LOWER(rushername) LIKE LOWER(\'{players[i].lower()}\');")
            reports = serverCursor.fetchall()
            entries.append(reports)
        
        #Create output string
        await ctx.send("Reminder: Times are in server time!")
        str = ""

        for i in range(len(entries)):
            #check if no reports found
            if len(entries[i])==0:
                str+= players[i]+" not found. \n"
                continue
            #format string
            str+=players[i]+":```\n"
            for report in entries[i]: 
                str+= f"{report[1]}, {report[2]}, {report[3]}\n"
            str+="```"
        await ctx.send(str)
        

    @commands.command(aliases=["addplayer"], brief="Add player to spreadsheet in UTC time.")
    async def addPlayer(self, ctx, server, playerName, customTime="0", customDate="0", *extraArgs):
        
        # await ctx.send("Sorry this command is currently under maintenance.")
        # return

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

        #Add to sheet
        sendData(ctx,server, serverCursor, serverConnection,playerName,time,date,reporterName)
        # sheet.append_row(dataEntry, value_input_option="USER_ENTERED")
        await ctx.send("Data entry successful!")

        #Add entry to leaderboard
        _execute(ctx, server, serverCursor, serverConnection,"SELECT * FROM leaderboard;" )
        # serverCursor.execute("SELECT * FROM leaderboard;")
        test = serverCursor.fetchall()

        print("REPORTER VALUE IS", reporterName)
        for j in range(len(test)):
            print(f"Checking {test[j][0].strip()}")
            #check if already exists
            repeat =False
            if reporterName.strip()==test[j][0].strip(): 
                repeat =True
                print(f"reporter found, adding to {reporterName.strip()}")
                #add one to entries if exists
                #find out current number of entries
                entries= test[j][1]
                _execute(ctx,server,serverCursor,serverConnection,f"UPDATE leaderboard SET ENTRIES = {entries+1} WHERE USERNAME = \'{reporterName}\'")
                # serverCursor.execute(f"UPDATE leaderboard SET ENTRIES = {entries+1} WHERE USERNAME = \'{reporterName}\'")
                break
        if not repeat: 
            #print(f"no name found, creating new name:{reporterValues[i]};{test[i][0].strip()}")
            #else create new entry
            _execute(ctx, server, serverCursor, serverConnection,f"INSERT INTO leaderboard(username, entries) VALUES(\'{reporterName}\',1)" )
            # serverCursor.execute(f"INSERT INTO leaderboard(username, entries) VALUES(\'{reporterName}\',1)")
        serverConnection.commit()
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
