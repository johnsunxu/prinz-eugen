from bs4 import BeautifulSoup
from azurlane.azurapi import AzurAPI
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from io import BytesIO
import base64
import requests
import discord
from discord.ext import commands
import os
from shipGirlNicknameHandler import getNickname


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures
from webdriver_manager.chrome import ChromeDriverManager

from base_graphics import BaseGraphics

import sys
sys.path.append('resources')

#Add Perseus API
from perseus import Perseus, APIError
api = Perseus(url=os.environ["API_URL"])

#set chrome options
opt = Options()
opt.headless = True
chrome_prefs = {}
opt.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
opt.add_argument("--disable-dev-shm-usage")
opt.add_argument("--no-sandbox")
#start driver
driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(),options = opt)
#old version of getting chrome driver
#driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"),options = opt)

class ShipDoesNotExistException(Exception):
    def __init__(self, desc, name) -> None:
        self.name = name
        super().__init__(desc)

#create class
class shipGearFinder(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client

    #Main function
    @commands.command()
    async def gear(self,ctx,*args):
        #send editing text
        message = await ctx.send("Finding best in slot gear...")

        shipName = " ".join(args)
        #Create ship object
        try:
            s = api.Ship(shipName,nicknames=True)
        except APIError:
            raise ShipDoesNotExistException("Ship does not exist",shipName)
        shipName = s.name.lower()
        #Replace certain characters with the code thing slime uses. For some reason urllib didn't work so I had to do this.
        shipName = shipName.replace(" ","_").replace("ü","%FC").replace("ö","%F6").replace("ä","%E4").replace("é","%E9").replace("â","%E2").replace("É","%E9").replace("ß","%DF").replace("μ","%B5").replace("pamiat'", "pamiat")
        #neptune needs to be HMS neptune
        if (shipName == 'neptune'):
            shipName = 'hms_neptune'
        if (shipName == 'kaga(bb)'):
            shipName = 'kaga_(battleship)'

        try:
            def text_wrap(text, font, max_width):
                    """Wrap text base on specified width.
                    This is to enable text of width more than the image width to be display
                    nicely.
                    @params:
                        text: str
                            text to wrap
                        font: obj
                            font of the text
                        max_width: int
                            width to split the text with
                    @return
                        lines: list[str]
                            list of sub-strings
                    """
                    lines = []

                    # If the text width is smaller than the image width, then no need to split
                    # just add it to the line list and return
                    if font.getsize(text)[0]  <= max_width:
                        lines.append(text)
                    else:
                        #split the line by spaces to get words
                        words = text.split(' ')
                        i = 0
                        # append every word to a line while its width is shorter than the image width
                        while i < len(words):
                            line = ''
                            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                                line = line + words[i]+ " "
                                i += 1
                            if not line:
                                line = words[i]
                                i += 1
                            lines.append(line)
                    return lines


            #Get data from chrome driver


            url = f"https://slaimuda.github.io/ectl/#/home?ship={shipName}"
            driver.get(url)
            element = driver.page_source
            #find close button
        #    closeButton = driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/div[1]/button')[0]
    #        closeButton.click()
            #refresh driver
            driver.get("data:,")


        #    driver.quit()


            #now we have the HTML so parse it
            soup = BeautifulSoup(element, "html.parser")

            objects = soup.body.find_all('div',class_="modal-body")[0].find_all('div', class_="row")[0]

            #Create blank gear array to save images. Safe to create 5 columns. There will always be 5.
            catagoryNames = ["","","","",""]
            gearImgArr = [[],[],[],[],[]]
            gearDownloadList = []


            #itterate through everything to get a list of the gear
            children = list(objects.children)

            #Create longestCatagory variable. This will be used to decide the size of the image later.
            longestCatagory = 0
            try:
                #create tag number to keep track of itteration.
                tagNumber = 0
                for i in children:
                    #get catagory name
                    catagoryNames[tagNumber] = i.find_all("h6")[0].text
                    g = i.find_all("img")
                    itterationNumber = 0
                    for j in g:
                        #check if gear is valid
                        if j['alt'] == "...":
                            #print name
                            gearSrc = j['src']
                            #get gear rarity
                            gearClass = j['class']
                            #Add images to gear download queue
                            gearDownloadList+=[[gearSrc,gearClass,tagNumber,itterationNumber]]

                            longestCatagory = max(longestCatagory,itterationNumber)
                            itterationNumber+=1
                    tagNumber+=1
            except:
                pass
            #Download the gear with multicore processing :exushock:
            def image_Modify(arr):
                try:
                    gearSrc = arr[0]
                    gearClass = arr[1]
                    #Check if base64
                    imageContent = 0
                    if len(gearSrc) > 200:
                        #Base64
                        imageContent = base64.b64decode(gearSrc.split(',')[1])   # im_bytes is a binary image
                    else:
                        #likely URL
                        response = requests.get("https://slaimuda.github.io"+gearSrc)
                        imageContent = response.content
                    imgBack = None
                    if gearClass[3] == "rarity-ultra-rare":
                        imgBack = Image.open('resources/images/Gear_Rairity/rarityRainbow70x70.png')
                    elif gearClass[3] == "rarity-super-rare":
                        imgBack = Image.open('resources/images/Gear_Rairity/rarityGold70x70.png')
                    elif gearClass[3] == "rarity-elite":
                        imgBack = Image.open('resources/images/Gear_Rairity/rarityPurple70x70.png')
                    else:
                        imgBack = Image.open('resources/images/Gear_Rairity/rarityBlue70x70.png')
                    image_bytes = BytesIO(imageContent)
                    img = Image.open(image_bytes)
                    #image is now open. Add a background depending on rarity.
                    img = img.resize((70,70))

                    #open background image
                    imgFinal = Image.alpha_composite(imgBack.convert("RGBA").resize((70,70)),img.convert("RGBA").resize((70,70)))
                    #return picture and location
                    return [imgFinal,arr[2],arr[3]]
                except Exception as e:
                    raise
            #put the pictures into the array for drawing
            with concurrent.futures.ThreadPoolExecutor() as exector:
                for i in exector.map(image_Modify, gearDownloadList):
                    gearImgArr[i[1]]+=[i[0]]


            #all the gear is downloaded now
            #--------------------------------------------------now we can create the image---------------------------------------------------------------
            #create the new image to specifications
            imageSize = 70
            imagePaddding = 5
            img = Image.new('RGBA', (85+(max(longestCatagory,6)+1)*(imageSize+imagePaddding)+15,480),color = BaseGraphics.getBackgroundColor())

            #create font
            font = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 16)
            fontName = ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 28)

            #download thumbnail
            try:
                if (not s.retrofit):
                    thumbnail = requests.get(s.skins[0]["thumbnail"]).content
                else:
                    thumbnail = requests.get(s.skins[-1]["thumbnail"]).content
                image_bytes = BytesIO(thumbnail)
                thumbnailImage = Image.open(image_bytes).resize((85,85)).convert("RGBA")
            except UnidentifiedImageError:
                thumbnail = requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/master/AzurLaneImages/assets/artresource/atlas/squareicon/unknown.png").content
                image_bytes = BytesIO(thumbnail)
                thumbnailImage = Image.open(image_bytes).resize((85,85)).convert("RGBA")


            #put thumbnail on image
            img.alpha_composite(thumbnailImage,(10,10))
            draw = ImageDraw.Draw(img)

            #draw name
            draw.text((105,10),s.name,fill='white',font=fontName)

            #paste gear
            for i in range(0,len(gearImgArr)):
                lines = text_wrap(catagoryNames[i],font,80)
                color = 'rgb(255,255,255)'  # Red color
                x = 85/2+10
                y = 95+(imageSize+imagePaddding)/2+(imageSize+imagePaddding)*i-len(lines)*8
                for line in lines:
                    draw.multiline_text(tuple([x-font.getsize(line)[0]/2,y]), line, fill=color, font=font,align="center")
                    y = y + 16    # update y-axis for new line
                for j in range(0,len(gearImgArr[i])):
                    img.paste(gearImgArr[i][j],(95+j*(imageSize+imagePaddding),100+i*(imageSize+imagePaddding)))

            with img as img:
                #upload to discord
                with BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file = discord.File(fp=image_binary,filename='shipGear.png')
                    #embedVar = discord.Embed(title=f"{shipName.title()}'s eHP",filename='eHPCalc.png')
                    imageURL = "attachment://shipGear.png"
                    #embedVar.set_image(url=imageURL)
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await message.delete()
                    await ctx.send("Gear recommendations are from https://slaimuda.github.io/ectl/#/home !", file=file)

        except ShipDoesNotExistException as e:
            await message.edit(content = f"{e.ship.title()} does not exist or is not on the EN tier list! Please try again.")
            raise





#set this up with cogs and pray it works
def setup(client):
    client.add_cog(shipGearFinder(client))
