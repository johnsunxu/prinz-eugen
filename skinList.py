import numpy as np
from PIL import Image
import os
from azurlane.azurapi import AzurAPI
import urllib.request
import string
import json


try:
    api = AzurAPI()
    skinJson = {};

    for i in range(1,473+1):
        try:
            print(str(i).rjust(3,'0'));
            HTML = api.getShip(ship=str(i).rjust(3,'0'));
            name = HTML['names']['en'];

            #Download skins
            for i in HTML['skins']:
                print('skin');
                skinName = i['name']
                imageURL = i['image'];

                extra = 'Skins';
                if skinName == 'Default':
                    extra = 'Default'
                elif skinName == 'Retrofit':
                    extra = 'Retrofit'
                #remove banned characters from skin name
                skinName.replace("<",'#1').replace(">",'#2').replace(":",'#3').replace('"','#4').replace("/",'#5').replace("\\",'#6').replace("|",'#7').replace("?",'#8').replace("*",'#9')

                if name in skinJson:
                    skinJson[name]+=[skinName];
                else:
                    skinJson[name] = [skinName];
        except:
            print("Something went wrong");
    with open('cogs/shipSkinList.json', 'w') as outfile:
        json.dump(skinJson, outfile)

except Exception as e:
  print(e)

while (True):
    pass;
