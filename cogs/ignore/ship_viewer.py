#Add Perseus API
from io import BytesIO
from discord import embeds

from discord.embeds import Embed
from perseus.ships import retrofit
from discord.ext import commands, menus
import discord
import sys
sys.path.append("./")

from perseus import Perseus
api = Perseus()

from base_graphics import BaseGraphics
from PIL import Image, ImageDraw
import glob

background_color = BaseGraphics.getBackgroundColor()

import noise
import numpy as np
from PIL import Image

import random

#Open images
STAT_IMAGES = {}
for file in glob.glob("resources/images/stat_icons/*.png"):
    img = Image.open(file)
    width,height = img.size
    stat = file.split("/")[-1].replace(".png","")
    if stat == "luck":
        scale = .8
    elif stat == "hit":
        scale = .25
    else:
        scale = .5


    img = img.resize((int(width*scale),int(height*scale)))
    STAT_IMAGES[stat] = img

def alpha_composite_centered(img,img2,locations):
    offset_x,offset_y = img2.size
    x,y = locations

    loc = int(x-offset_x/2),int(y-offset_y/2)

    img.alpha_composite(img2,loc)

from discord.ext import menus

class Menu(menus.Menu):
    def __init__(self, embeds, page, thumbnail = ""):
        super().__init__(timeout=60.0, delete_message_after=False)
        self.embeds = embeds
        self.page = page
        self.thumbnail = thumbnail

        for embed in self.embeds:
            embed[0].set_thumbnail(url=self.thumbnail)

    async def send_initial_message(self, ctx, channel):
        if len(self.embeds[self.page]) >= 1:
            return await channel.send(embed=self.embeds[self.page][0],file=self.embeds[self.page][1])
        else:
            return await channel.send(embed=self.embeds[self.page][0],file=None)

    async def send_edited_message(self):
        if len(self.embeds[self.page]) >= 1:
            await self.message.edit(embed=self.embeds[self.page][0])
        else:
            await self.message.edit(embed=self.embeds[self.page][0])

    @menus.button('⬅️')
    async def on_thumbs_up(self, payload):
        self.page = max(self.page-1,0)
        await self.send_edited_message()

    @menus.button('➡️')
    async def on_thumbs_down(self, payload):
        self.page = min(self.page+1,len(self.embeds)-1)
        await self.send_edited_message()




async def sendShipMenu(ctx, *args, page=0):
    ship_name = ' '.join(args)
    s = api.Ship(ship_name,nicknames=True)

    #-------------------------------Ship Stats Page--------------------------------------
    ship_stats_embed = discord.Embed(title=f"{s.name_en}'s Stats")
    limit_break_text = '\n'.join([f"`{i}`" for i in s.limit_break_text["en"]])
    slot_text = '\n'.join([f"{f'`{int(s.efficiency[count]*100)}%:`'.ljust(9)}{'/'.join(equip)}" for count,equip in enumerate(s.slot_names[:3])])

    ship_stats_embed.add_field(name="Limit Break", value=limit_break_text, inline=False)
    ship_stats_embed.add_field(name="Gear", value=slot_text, inline=False)

    img = Image.new(mode = "RGBA", size = (468, 268), color=background_color)
    draw = ImageDraw.Draw(img)

    stats = s.stats
    stats["armor"] = s.armor_type
    
    x_spacing = 150
    y_spacing = 50

    stats_to_draw = [
        [["durability","hp"],["armor","armor"],["reload","rld"]],
        [["cannon","fp"],["torpedo","trp"],["dodge","eva"]],
        [["antiaircraft","aa"],["air","avi"],["expend","oil"]],
        [["antisub","asw"]],
        [["luck","luk"],["hit","acc"],["speed","spd"]],
    ]

    if s.hull_type.lower() in ["submarine","aviation submarine"]:
        print("here")
        stats_to_draw[3] += [["oxy_max","oxy"]]

    for _y,_ in enumerate(stats_to_draw):
        for _x,array in enumerate(_):
            icon,stat = array

            x = _x*x_spacing+7+8
            y = _y*y_spacing+12+8

            #Draw light red box
            draw.rectangle((x-7,y-12,x+40,y-12+y_spacing),fill=BaseGraphics.getHighlightColor())

            #Draw vertical lines
            draw.line((x-7,y-12,x-7,y+y_spacing-12),fill="white")
            draw.line((x-7+x_spacing,y-12,x-7+x_spacing,y+y_spacing-12),fill="white")

            #Draw Horizontal
            draw.line((x-7,y-12,x-7+x_spacing,y-12),fill="white")
            draw.line((x-7,y-12+y_spacing,x-7+x_spacing,y-12+y_spacing),fill="white")

            alpha_composite_centered(img,STAT_IMAGES[icon],(x+17,y+15))
            draw.text((x+48,y+3),str(stats[stat]),fill="white",font=BaseGraphics.getFont())

    ship_stats_embed.set_footer(text=f";view {s.name}")

    with BytesIO() as image_binary:
        img.save(image_binary,format="PNG")
        #send the embed
        file = discord.File(fp=image_binary, filename='stats.png')
        image_url = "attachment://stats.png"
        image_binary.seek(0)
        ship_stats_embed.set_image(url=image_url)
        ship_stats_embed = [ship_stats_embed,file]



    #-----------------------------Ship Skills Page--------------------------------------
    ship_skills_embed = discord.Embed(title=f"{s.name}'s Skills")
    for skill in s.getSkills():
        ship_skills_embed.add_field(name=skill["name"],value=f"`{skill['description']}`",inline=False)



    skins = s.skins.copy()
    if s.retrofit:
        skins.pop(0)
    elif s.has_retrofit:
        skins.pop(-1)

    chibi = random.choice(skins)["chibi"]

    embeds = [ship_stats_embed,[ship_skills_embed,]]
    m = Menu(embeds, 0, thumbnail = chibi)
    await m.start(ctx)

#create class
class ShipViewer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def view(self, ctx, *args):
        await sendShipMenu(ctx, *args, page=0)


        # width,height = (1000,425)
        # img = Image.new(mode = "RGBA", size = (width, height), color=background_color)
        # # img = overlay_noise(img)

        # skins = s.skins.copy()
        # if s.retrofit:
        #     skins.pop(0)
        # elif s.has_retrofit:
        #     skins.pop(-1)

        # chibi = random.choice(skins)["chibi"]

        # draw = ImageDraw.Draw(img)
        # def drawCenteredText(loc,text,font,fill="white",align="center"):
        #     draw.text((loc[0]-font.getsize(text)[0]/2,loc[1]), text, fill=fill, font=font,align=align)
        

        # #draw name
        # # draw.text((105,10),s.name,fill='white',font=BaseGraphics.getNameFont())

        # #Draw stats and stat icons
        # stats_to_draw = [
        #     [["durability","hp"],["armor","armor"],["reload","rld"]],
        #     [["cannon","fp"],["torpedo","trp"],["dodge","eva"]],
        #     [["antiaircraft","aa"],["air","avi"],["expend","oil"]],
        #     [["antisub","asw"]],
        #     [["luck","luk"],["hit","acc"],["speed","spd"]],
        # ]

        # if s.hull_type.lower() in ["submarine","aviation submarine"]:
        #     print("here")
        #     stats_to_draw[3] += [["oxy_max","oxy"]]



        # stats = s.stats
        # stats["armor"] = s.armor_type
        
        # x_spacing = 150
        # y_spacing = 50

        # #-------------------Stats--------------------------

        # for _y,_ in enumerate(stats_to_draw):
        #     for _x,array in enumerate(_):
        #         icon,stat = array

        #         x = _x*x_spacing+32
        #         y = _y*y_spacing+25

        #         #Draw light red box
        #         draw.rectangle((x-7,y-12,x+40,y-12+y_spacing),fill=BaseGraphics.getHighlightColor())

        #         #Draw vertical lines
        #         draw.line((x-7,y-12,x-7,y+y_spacing-12),fill="white")
        #         draw.line((x-7+x_spacing,y-12,x-7+x_spacing,y+y_spacing-12),fill="white")

        #         #Draw Horizontal
        #         draw.line((x-7,y-12,x-7+x_spacing,y-12),fill="white")
        #         draw.line((x-7,y-12+y_spacing,x-7+x_spacing,y-12+y_spacing),fill="white")

        #         alpha_composite_centered(img,STAT_IMAGES[icon],(x+17,y+15))
        #         draw.text((x+48,y+3),str(stats[stat]),fill="white",font=BaseGraphics.getFont())

        # #-------------------Efficiency---------------------
        # font_size = [20,16,16,16]
        # cell_height = 30

        # def makeSlotsNice(n):
        #     return "/".join([str(i) for i in s.slot_names[n]])

        # cells = [
        #     [70,["Slot","1","2","3"]],
        #     [110,["Efficiency",str(int(s.efficiency[0]*100))+"%",str(int(s.efficiency[1]*100))+"%",str(int(s.efficiency[2]*100))+"%"]],
        #     [280,["Equip Type",makeSlotsNice(0),makeSlotsNice(1),makeSlotsNice(2)]],
        # ]


        # x = 25
        # for cell in cells:
        #     _w = cell[0]
        #     y = 300
        #     for count,text in enumerate(cell[1]):

        #         #Draw horizontal lines
        #         draw.line((x,y-cell_height/2,x,y+cell_height/2),fill="white")
        #         draw.line((x+_w,y-cell_height/2,x+_w,y+cell_height/2),fill="white")

        #         #Draw vertical lines
        #         draw.line((x,y-cell_height/2,x+_w,y-cell_height/2),fill="white")
        #         draw.line((x,y+cell_height/2,x+_w,y+cell_height/2),fill="white")
                
        #         drawCenteredText((x+_w/2,y-font_size[count]/2),text,font=BaseGraphics.getFontAtSize(font_size[count]))

        #         y+=cell_height
        #     x+=_w

        # #-------------------Hunting Range--------------------
        # if s.hunting_range != None:
        #     x = 500
        #     y = 20
        #     for _x,row in enumerate(s.hunting_range):
        #         for _y,cell in enumerate(row):
        #             drawCenteredText((x+_x*25,y+_y*25),str(cell),font=BaseGraphics.getFontAtSize(15))

        # embed = discord.Embed(title=f"{s.name}'s Stats", description="Change pages for more information!", color=0x00ff00)

        # skill_text = '\n\n'.join([f"`{i['name']}: {i['description']}`" for i in s.getSkills()])
        # limit_break_text = '\n'.join([f"`{i}`" for i in s.limit_break_text["en"]])

        # with BytesIO() as image_binary:
        #     img.save(image_binary,format="PNG")
        #     #send the embed
        #     file = discord.File(fp=image_binary, filename='stats.png')
        #     image_url = "attachment://stats.png"
        #     embed.set_image(url=image_url)
        #     embed.set_thumbnail(url=chibi)
        #     embed.color = BaseGraphics.getEmbedColor()
        #     image_binary.seek(0)
        #     embed.add_field(name="Skills", value=skill_text, inline=False)
        #     embed.add_field(name="Limit Break", value=limit_break_text, inline=False)

        #     await message.channel.send(embed=embed,file=file)




def setup(client):
    client.add_cog(ShipViewer(client))
