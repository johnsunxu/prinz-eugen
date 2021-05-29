import discord
import os
import psycopg2
import random

from dotenv import load_dotenv
from discord.ext import commands

#Function for reconnecting in case connecting randomly dies
def reconnect():
    global quote_conn, quote_cur
    quote_conn = psycopg2.connect(quote_db, sslmode="allow")
    quote_cur = quote_conn.cursor()

#Function to execute SQL query while accounting for errors
async def _execute(ctx, query, returning=False):
    global quote_conn, quote_cur
    try:
        quote_cur.execute(query)
        quote_conn.commit()
        #return the printout from the query
        if returning == True:
            temp = quote_cur.fetchall() 
            # print(temp)
            return temp
    #In case of bad query, definitely not the best way to solve this error
    except psycopg2.InternalError:
        quote_cur.rollback()
        await _execute(ctx, query, returning)
    #If query fails, reconnect to databases
    except (psycopg2.InterfaceError, psycopg2.OperationalError):
        await ctx.send("Please wait, reconnecting to database.")
        reconnect()
        try:
            quote_cur.execute(query)
            quote_conn.commit()
        #report unaccounted for errors to creator
        except Exception as e:
            print("ERROR:", e)
            await ctx.send("Database error, ping SomeDude#0172")

#Function that generates id for quote and adds to to DB
async def addToDB(ctx, name, content): 
    #Make ID from fetching latest entry
    id = await _execute(ctx, f"SELECT id FROM quotes ORDER BY id desc limit 1;", returning = True)
    print(id)
    id = id[0][0]+1
    await _execute(ctx, f"INSERT INTO quotes(id, name, content) VALUES({id}, \'{name}\', \'{content}\');")


class Quote(commands.Cog):
    #init
    def __init__(self, client): 
        self.client = client

    @commands.command()
    async def quote(self, ctx, help): 
        embed = discord.Embed(color = embedColor, title = "Quote Help Menu")

        embed.add_field(name = "`;; [quote name] [quote]`", value = "Create a new quote.", inline = False)

        embed.add_field(name = "`;;; [quote name]`", value = "Summon a quote.", inline = False)

        embed.add_field(name = "`;authorize [role name]`", value = "Give permissions to add quotes from a role. Use \" \" for roles with spaces.", inline = False)

        embed.add_field(name = "`;deauthorize [role name]`", value = "Remove permissions to add quotes from a role. Use \" \" for roles with spaces.", inline = False)

        await ctx.send(embed = embed)

    #Command so admin can authorize which roles can quote things
    @commands.command(brief = "Add quoting permissions to a role. Case sensitive.")
    async def authorize(self, ctx, role): 
        #Check if user is admin
        user = ctx.message.author
        if not user.guild_permissions.administrator: 
            await ctx.send("Access Denied!")
            return
        
        #retrieve list of roles from server
        serverRoles = user.guild.roles

        for serverRole in serverRoles:
            validRole = False 
            if serverRole.name == role.strip(): 
                role = serverRole
                validRole = True
                break
        if validRole: 
            await _execute(ctx, f"INSERT INTO ROLES(serverid, roleid) VALUES(\'{user.guild.id}\', \'{role.id}\');") 
            await ctx.send("Role authorized!")
        else: 
            await ctx.send("Role does not exist!")
            return
    
    @commands.command(aliases = ["unauthorize"], brief = "Remove quoting permissions from a role. Case sensitive.")
    async def deauthorize(self, ctx, role): 
        #Check if user is admin
        user = ctx.message.author
        if not user.guild_permissions.administrator: 
            await ctx.send("Access Denied!")
            return

        #retrieve list of roles from server
        serverRoles = user.guild.roles

        #check input and get role object if input is a valid role
        for serverRole in serverRoles:
            validRole = False
            if serverRole.name == role.strip():
                role = serverRole
                validRole = True
                break
        #remove role
        if validRole:
            await _execute(ctx, f"DELETE FROM ROLES WHERE roleid = \'{role.id}\';")
            await ctx.send("Role deauthorized!")
        else:
            await ctx.send("Role does not exist!")
            return

    #Command to add a quote
    @commands.command(aliases=[";"], brief="Add a quote.")
    async def createQuote(self, ctx, name, *args): 
        #Check if user has perms
        #If user is not an admin 
        user = ctx.message.author
        if not user.guild_permissions.administrator: 
            #check if user has role to add quotes
            #obtain roles of caller
            roles = user.roles
            #valid roles
            validRolesIds = await _execute(ctx, f"SELECT roleid FROM roles WHERE serverid=\'{user.guild.id}\';", returning = True)
            valid = False
            for role in roles: 
                for validRoleId in validRolesIds: 
                    if role.id == int(validRoleId[0]): 
                        valid = True

            if not valid: 
                await ctx.send("Access Denied!")
                return

        #Check if user attached an image instead of a url/string
        if len(ctx.message.attachments) == 1: 
            #should only be one attachment max
            attachment = ctx.message.attachments[0]
            url = attachment.url
            url += " "
            #add any strings
            for arg in args: 
                url+= str(arg)
            #add to database here
            await addToDB(ctx, name, url)

        #string
        else: 
            content = ""
            for arg in args: 
                content+= str(arg)
            
            #check if user didn't quote anything 
            if len(content) == 0: 
                await ctx.send("Quote something you pepega!")
                return
            #add to database
            await addToDB(ctx, name, content)
            await ctx.send("Quote added")

    @commands.command(aliases = [";;"], brief = "Summon a quote.")
    async def call(self, ctx, name):
        data = await _execute(ctx, f"SELECT * FROM quotes WHERE LOWER(name) LIKE LOWER(\'{name}\')", returning = True)
        choice = random.randint(0, len(data)-1)
        await ctx.send(f"`#{data[choice][0]}` {data[choice][2]}")


def setup(client):
    client.add_cog(Quote(client))


#DATABASE CONNECTIONS
load_dotenv(dotenv_path="./dev.env")
quote_db = os.getenv("HEROKU_POSTGRESQL_PUCE_URL")
quote_conn = psycopg2.connect(quote_db, sslmode = "allow")
quote_cur = quote_conn.cursor()

#Misc vars
embedColor = 0xf01111
