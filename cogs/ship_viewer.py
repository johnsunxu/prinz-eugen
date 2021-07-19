#Add Perseus API
from io import BytesIO
from mmap import MADV_WILLNEED

from requests.api import request
from discord.ext import commands
import discord
import sys
sys.path.append("./")

from perseus import Perseus, APIError
api = Perseus()

from base_graphics import BaseGraphics
from PIL import Image, ImageDraw
import glob

background_color = BaseGraphics.getBackgroundColor()

import numpy as np
from PIL import Image
import requests

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

#create class
class ShipViewer(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def view(self, ctx, *args):
        width,height = (660,505)
        img = Image.new(mode = "RGBA", size = (width, height), color=background_color)
        # img = overlay_noise(img)

        name = ' '.join(args)
        s = api.Ship(name,nicknames=True)

        # skins = s.skins.copy()
        # if s.retrofit:
        #     skins.pop(0)
        # elif s.has_retrofit:
        #     skins.pop(-1)

        if s.retrofit:
            thumbnail = s.skins[-1]["thumbnail"]
        else:
            thumbnail = s.skins[0]["thumbnail"]

        draw = ImageDraw.Draw(img)

        def drawCenteredText(loc,text,font,fill="white",align="center"):
            draw.text((loc[0]-font.getsize(text)[0]/2,loc[1]), text, fill=fill, font=font,align=align)

        # draw name and thumbnail image
        thumbnail_width, thumbnail_height = (75,75)
        thumbnail_image = api.downloadImage(thumbnail).resize((thumbnail_width,thumbnail_height))
        title = f"{s.name}{' Kai' if s.retrofit else ''}'s Stats"
        
        loc = (width/2,25)
        font = BaseGraphics.getNameFont()
        draw_x = int(loc[0]-(font.getsize(title)[0]-thumbnail_width+10)/2)
        draw.text((draw_x,loc[1]),title,fill='white',font=font)
        img.alpha_composite(thumbnail_image,(draw_x-thumbnail_width-10,loc[1]-15))

        #Draw stats and stat icons
        stats_to_draw = [
            [["durability","hp"],["armor","armor"],["reload","rld"]],
            [["cannon","fp"],["torpedo","trp"],["dodge","eva"]],
            [["antiaircraft","aa"],["air","avi"],["expend","oil"]],
            [["antisub","asw"]],
            [["luck","luk"],["hit","acc"],["speed","spd"]],
        ]

        if s.hull_type.lower() in ["submarine","aviation submarine"]:
            stats_to_draw[3] += [["oxy_max","oxy"]]



        stats = s.stats
        stats["armor"] = s.armor_type
        
        x_spacing = 150
        y_spacing = 50
        x_offset = (width-x_spacing*3)/2
        y_offset = 110

        #-------------------Stats--------------------------

        for _y,_ in enumerate(stats_to_draw):
            for _x,array in enumerate(_):
                icon,stat = array

                x = _x*x_spacing+x_offset
                y = _y*y_spacing+y_offset

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

        #-------------------Efficiency---------------------
        font_size = [20,16,16,16]
        cell_height = 30

        def makeSlotsNice(n):
            return "/".join([str(i) for i in s.slot_names[n]])

        cells = [
            [70,["Slot","1","2","3"]],
            [90,["Mounts"]+[str(i) for i in s.base_list[0:3]]],
            [110,["Efficiency",str(int(s.efficiency[0]*100))+"%",str(int(s.efficiency[1]*100))+"%",str(int(s.efficiency[2]*100))+"%"]],
            [90,["CE",str(int(s.efficiency[0]*100)*s.base_list[0])+"%",str(int(s.efficiency[1]*100)*s.base_list[1])+"%",str(int(s.efficiency[2]*100)*s.base_list[2])+"%"]],
            [280,["Equip Type",makeSlotsNice(0),makeSlotsNice(1),makeSlotsNice(2)]],
        ]


        x = 10
        for cell in cells:
            _w = cell[0]
            y = 380
            for count,text in enumerate(cell[1]):

                #Draw horizontal lines
                draw.line((x,y-cell_height/2,x,y+cell_height/2),fill="white")
                draw.line((x+_w,y-cell_height/2,x+_w,y+cell_height/2),fill="white")

                #Draw vertical lines
                draw.line((x,y-cell_height/2,x+_w,y-cell_height/2),fill="white")
                draw.line((x,y+cell_height/2,x+_w,y+cell_height/2),fill="white")
                
                drawCenteredText((x+_w/2,y-font_size[count]/2),text,font=BaseGraphics.getFontAtSize(font_size[count]))

                y+=cell_height
            x+=_w

        #-------------------Hunting Range--------------------
        if s.hunting_range != None:
            x = 500
            y = 20
            for _x,row in enumerate(s.hunting_range):
                for _y,cell in enumerate(row):
                    drawCenteredText((x+_x*25,y+_y*25),str(cell),font=BaseGraphics.getFontAtSize(15))

        # embed = discord.Embed(title=f"{s.name}'s Stats")
        # skill_text = '\n\n'.join([f"`{i['name']}: {i['description']}`" for i in s.getFormattedSkills()])
        # limit_break_text = '\n'.join([f"`{i}`" for i in s.limit_break_text["en"]])
        # chibi = random.choice(skins)["chibi"]

        with BytesIO() as image_binary:
            img.save(image_binary,format="PNG")
            file = discord.File(fp=image_binary, filename='stats.png')
            #send the embed
            # image_url = "attachment://stats.png"
            # embed.set_image(url=image_url)
            # embed.set_thumbnail(url=chibi)
            # embed.color = BaseGraphics.getEmbedColor()
            # embed.add_field(name="Skills", value=skill_text, inline=False)
            # embed.add_field(name="Limit Break", value=limit_break_text, inline=False)
            # await ctx.channel.send(embed=embed,file=file)
            image_binary.seek(0)
            await ctx.channel.send(file=file)


    # @commands.command()
    # async def retrofit(self, ctx, *args):
    #     ship_name = ' '.join(args)
    #     try:
    #         s = api.Ship(ship_name)
    #     except APIError:
    #         await ctx.send("Ship does not exist.")
    #         return

    #     if s.has_retrofit == False:
    #         await ctx.send("Ship does not have an retrofit.")
    #         return

    #     x_offset = 20
    #     y_offset = 20
    #     spacing = 64+15

    #     img = Image.new(size=(spacing*6+40,spacing*3+40),mode="RGBA",color=BaseGraphics.getBackgroundColor())
    #     draw = ImageDraw.Draw(img)

    #     line_color = (0,0,0,255)

    #     #Draw the retrofit tree
    #     for node in s.retrofit_nodes:
    #         #Download the icon
    #         icon = Image.open(BytesIO(requests.get(node["icon"]).content)).resize(size=(64,64))

    #         getXDrawLoc = lambda x: x*spacing+x_offset
    #         getYDrawLoc = lambda y: y*spacing+y_offset
    #         getDrawLoc = lambda x: (getXDrawLoc(x[0]),getYDrawLoc(x[1]))
    #         def getArrowDrawLoc(x):
    #             x = getDrawLoc(x)
    #             return (x[0]+32,x[1]+32)

    #         def sign(x):
    #             if (x == 0): return 0
    #             elif (x>0): return 1
    #             else: return -1

    #         def drawArrow(draw,start_node,end_node):
    #             nonlocal line_color
    #             dir_x = sign(start_node[0]-end_node[0])
    #             dir_y = sign(start_node[1]-end_node[1])

    #             arrow_height = 8
    #             arrow_width = 6

    #             node_xy = getArrowDrawLoc(end_node)

    #             facing_right_triangle = (
    #                 (node_xy[0]-32,node_xy[1]),
    #                 (node_xy[0]-32-arrow_height,node_xy[1]+arrow_width),
    #                 (node_xy[0]-32-arrow_height,node_xy[1]-arrow_width),
    #             )
    #             facing_left_triangle = (
    #                 (node_xy[0]+32,node_xy[1]),
    #                 (node_xy[0]+32+arrow_height,node_xy[1]+arrow_width),
    #                 (node_xy[0]+32+arrow_height,node_xy[1]-arrow_width),
    #             )
    #             facing_up_triangle = (
    #                 (node_xy[0],node_xy[1]+32),
    #                 (node_xy[0]-arrow_width,node_xy[1]+32+arrow_height),
    #                 (node_xy[0]+arrow_width,node_xy[1]+32+arrow_height),
    #             )
    #             facing_down_triangle = (
    #                 (node_xy[0],node_xy[1]-32),
    #                 (node_xy[0]-arrow_width,node_xy[1]-32-arrow_height),
    #                 (node_xy[0]+arrow_width,node_xy[1]-32-arrow_height),
    #             )

    #             triangle = ()
    #             if dir_x == 1:
    #                 triangle = facing_left_triangle
    #             elif dir_x == -1:
    #                 triangle = facing_right_triangle
    #             elif dir_y == 1:
    #                 triangle = facing_up_triangle
    #             elif dir_y == -1:
    #                 triangle = facing_down_triangle
    #             else:
    #                 return

    #             draw.polygon(
    #                 triangle,
    #                 fill=line_color
    #             )

    #         x = node["x"]
    #         y = node["y"]

    #         #Draw the arrows
    #         for n in node["next_nodes"]:
    #             arrow_start_loc = (x,y)
    #             arrow_end_loc = (s.retrofit_nodes[n%100-1]["x"],s.retrofit_nodes[n%100-1]["y"])

    #             #Diagnol lines need more work
    #             if (arrow_start_loc[0] == arrow_end_loc[0] or arrow_start_loc[1] == arrow_end_loc[1]):
    #                 draw.line(getArrowDrawLoc(arrow_start_loc)+getArrowDrawLoc(arrow_end_loc),fill=line_color,width=2)
    #                 drawArrow(draw,arrow_start_loc,arrow_end_loc)
    #             else:
    #                 arrow_mid_loc = (
    #                     max(arrow_start_loc[0],arrow_end_loc[0]),
    #                     arrow_start_loc[1]
    #                 )

    #                 draw.line(getArrowDrawLoc(arrow_start_loc)+getArrowDrawLoc(arrow_mid_loc),fill=line_color,width=2)
    #                 draw.line(getArrowDrawLoc(arrow_mid_loc)+getArrowDrawLoc(arrow_end_loc),fill=line_color,width=2)
    #                 drawArrow(draw,arrow_mid_loc,arrow_end_loc)


    #         #Draw the image
    #         img.paste(icon,getDrawLoc((x,y)))

    #     with BytesIO() as image_binary:
    #         img.save(image_binary,format="PNG")
    #         image_binary.seek(0)
    #         await ctx.send(file=discord.File(image_binary,filename="retrofit_tree.png"))



def setup(client):
    client.add_cog(ShipViewer(client))