import discord
import gspread
import pytz
import jellyfish
import psycopg2
import sys
import os
import asyncio
import matplotlib
import matplotlib.pyplot as plt
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
async def _execute(ctx, server, serverCursor, serverConnection, query, returning = False):
    try:
        serverCursor.execute(query)
        serverConnection.commit()
        #return the printout from the query
        if returning == True:
            return serverCursor.fetchall()
    #In case of bad query, definitely not the best way to solve this error
    except psycopg2.InternalError:
        serverCursor.rollback()
        _execute(ctx, server, serverCursor, serverConnection, query, returning)
    #If query fails, reconnect to databases
    except (psycopg2.InterfaceError, psycopg2.OperationalError):
        await ctx.send("Please wait, reconnecting to database.")
        reconnect()
        #re define variables
        if server == "avrora": 
            serverCursor= avrora_cur
            serverConnection = avrora_conn
        elif server == "lexington": 
            serverCursor = lexington_cur
            serverConnection = lexington_conn
        elif server == "washington": 
            serverCursor = washington_cur
            serverConnection = washington_conn
        elif server == "sandy": 
            serverCursor = sandy_cur
            serverConnection = sandy_conn
        elif server == "amagi": 
            serverCursor = amagi_cur
            serverCursor = amagi_conn
        try:
            serverCursor.execute(query)
            serverConnection.commit()
        #report unaccounted for errors to creator
        except Exception as e:
            print("ERROR:", e )
            await ctx.send("Database error, ping SomeDude#0172")

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
    serverTime = datetime.now(pytz.timezone("US/Pacific"))
    time = serverTime.strftime("%H:%M:%S")
    date = serverTime.strftime("%d/%m/%Y")
    print(time)
    print(date)

#
async def sendData(ctx, server, serverCursor, serverConnection, rusherName, time, date, reporterName):
    #find out entry number abd send query
    entryNumber = await _execute(ctx, server, serverCursor, serverConnection, f"SELECT * FROM {server.lower()}_entries ORDER BY entrynumber;", returning=True)
    entryNumber = len(entryNumber)+1
    # serverCursor.execute(f"SELECT * FROM {server.lower()}_entries ORDER BY entrynumber;")
    #entryNumber = serverCursor.fetchall()[len(serverCursor.fetchall())-1][0]+1
    print("ENTRY NUM IS", entryNumber)
    print(f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
    await _execute(ctx, server, serverCursor, serverConnection, f"INSERT INTO {server.lower()}_entries(entrynumber, rushername, time, date, reportername) VALUES({entryNumber},\'{rusherName}\',\'{time}\',\'{date}\',\'{reporterName}\');")
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
        await _execute(ctx, server, serverCursor, serverConnection, "SELECT * FROM leaderboard ORDER BY entries DESC;")
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

        #Function for creating graph of image. Input list of times and player name, returns discord.File
        def createGraph(data, playerName, num):
            #number of data points
            n = len(data)
            #coordinates
            x = []
            y = []

            for entry in data:
                #convert string into datetime objects
                x.append(datetime.strptime(entry[:5], "%H:%M"))
                y.append(5)

            x = matplotlib.dates.date2num(x)
            plt.plot_date(x, y, color=(0, 0, 0), ms=2, label="Report")

            #create data for resets
            x_reset = ["00:00", "12:00", "18:00"]
            y_reset = [5, 5, 5]
            #convert str to datetime object
            for i in range(len(x_reset)):
                x_reset[i] = datetime.strptime(x_reset[i], "%H:%M")
            x_reset = matplotlib.dates.date2num(x_reset)
            plt.plot_date(x_reset, y_reset, ms=6, label="Reset")

            #idk what this variable is
            ax = plt.gca()
            timeFormat = matplotlib.dates.DateFormatter("%H:%M")
            ax.xaxis.set_major_formatter(timeFormat)

            #graph extras
            print("playername (creategraph):", playerName)
            plt.title(f"Rushing Analysis of {playerName}")
            plt.yticks([])
            plt.xticks(x_reset)
            plt.gcf().autofmt_xdate()
            plt.legend(["Report", "Reset"])
            plt.xlabel("Time")
            plt.ylabel("")
            plt.savefig(f"./cogs/dataPull/{num}.png")

            #need to show the plot for some reason
            # print(data)
            # print("showing plot")
            plt.show(block=False)
            plt.close()
            #create discord file
            file = discord.File(f"./cogs/dataPull/{num}.png")
            return file

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

        #Receive variables
        entries = []
        for i in range(len(players)):
            await _execute(ctx, server, serverCursor, serverConnection, f"SELECT * FROM {server}_entries WHERE LOWER(rushername) LIKE LOWER(\'{players[i].lower()}\');")
            # serverCursor.execute(f"SELECT * FROM {server}_entries WHERE LOWER(rushername) LIKE LOWER(\'{players[i].lower()}\');")
            reports = serverCursor.fetchall()
            entries.append(reports)

        #Create output string
        updateTime()
        global time
        await ctx.send(f"Reminder: Times are in server time!\nCurrent server time is `{time}`")

        embedList = []
        graphList = []

        #Create table output
        output = ""
        for i in range(len(entries)):
            #check if no reports found
            if len(entries[i]) == 0:
                output += players[i]+" not found. \n"
            else:
                #format string
                output += "```\n"
                #sort by time
                entries[i].sort(key=lambda x: x[2])
                for report in entries[i]:
                    output += f"{report[2]} {report[3]}\n"
                output += "```"
            embed = discord.Embed(title="Analysis", color=embedColor)
            embed.add_field(name=f"{players[i]}", value=output)
            output = ""
            embedList.append(embed)

        #create graph of data
        #extract all times from entry
        timeList = []
        for player in entries:
            if len(player) == 0:
                continue
            for entry in player:
                timeList.append(entry[2])
            #print(entry)
            # print(player[0][1])
            # print(timeList)
            file = createGraph(timeList, player[0][1], entries.index(player))
            #create embed with graph and add to list
            embed = discord.Embed(
                color=embedColor, title=f"{entries.index(player)}")
            embed.set_image(url=f"attachment://{entries.index(player)}.png")
            graphList.append((embed, file))
            timeList = []

        #Variable to flip around pages in embed message
        page = 0

        msg = await ctx.send(embed=embedList[page])
        if len(players) > 1:
            await msg.add_reaction("⬅️")
            await msg.add_reaction("➡️")
        await msg.add_reaction("📈")

        for i in range(0, 180):
            def reaction_check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ["⬅️", "➡️", "📈"]

            await asyncio.sleep(0.5)

            #Added reaction
            reaction, user = await self.client.wait_for("reaction_add", check=reaction_check)
            #Only add pages if there is more than one player requested
            if len(players) > 1:
                if reaction.emoji == "⬅️":
                    try:
                        await msg.remove_reaction("⬅️", ctx.author)
                    except:
                        pass
                    #flip page
                    if page - 1 < 0:
                        page = len(players) - 1
                    else:
                        page = page-1

                    #Edit message
                    await msg.edit(embed=embedList[page])

                elif reaction.emoji == "➡️":
                    try:
                        await msg.remove_reaction("➡️", ctx.author)
                    except:
                        pass
                    #flip page
                    if page + 1 >= len(players):
                        page = 0
                    else:
                        page += 1
                    #Edit message
                    await msg.edit(embed=embedList[page])

            if reaction.emoji == "📈":
                #Edit message
                # await msg.edit(embed = graphList[page][0], file = graphList[page][1])
                await ctx.send(embed=graphList[page][0], file=graphList[page][1], delete_after=25)
                # await ctx.send(embed = graphList[page][0], file = graphList[page][1])
                # await msg.remove_reaction("📈", msg.author)
            #Removed reaction
            # reaction, user = await self.client.wait_for("reaction_remove", check = reaction_check)
            # if reaction.emoji == "📈":
            #     #Edit message back to table
            #     await msg.edit(embed = embedList[page])

        await msg.clear_reactions()


    @commands.command(aliases=["addplayer"], brief="Add player to spreadsheet in UTC time.")
    async def addPlayer(self, ctx, server, playerName, customTime="0", customDate="0", *extraArgs):

        #quick check to make sure the user is on ALM's sever
        #servers besides that one are banned to prevent trolling
        if (ctx.guild.name != "Azur Lane Meta"):
            await ctx.channel.send("Sorry, you can only use this command on Azur Lane Meta's server. Join at discord.gg/AzurLaneMeta.")
            #it probably is stopped with the return
            return

        # await ctx.send("Sorry this command is currently under maintenance.")
        # return
        # await ctx.send("Sorry this command is currently disabled.")
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

        #check for negative numbers
        if customTime <0 or customDate<0:
            await ctx.send("No negative numbers! Custom time is for minutes passed.")
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
        await sendData(ctx,server, serverCursor, serverConnection,playerName,time,date,reporterName)
        # sheet.append_row(dataEntry, value_input_option="USER_ENTERED")
        await ctx.send("Data entry successful!")

        #Add entry to leaderboard
        await _execute(ctx, server, serverCursor, serverConnection,"SELECT * FROM leaderboard;" )
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
                await _execute(ctx,server,serverCursor,serverConnection,f"UPDATE leaderboard SET ENTRIES = {entries+1} WHERE USERNAME = \'{reporterName}\'")
                # serverCursor.execute(f"UPDATE leaderboard SET ENTRIES = {entries+1} WHERE USERNAME = \'{reporterName}\'")
                break
        if not repeat:
            #print(f"no name found, creating new name:{reporterValues[i]};{test[i][0].strip()}")
            #else create new entry
            await _execute(ctx, server, serverCursor, serverConnection,f"INSERT INTO leaderboard(username, entries) VALUES(\'{reporterName}\',1)" )
            # serverCursor.execute(f"INSERT INTO leaderboard(username, entries) VALUES(\'{reporterName}\',1)")
        serverConnection.commit()
        return


def setup(client):
    client.add_cog(CheckPlayer(client))


#Misc vars
embedColor = 0xf01111

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
