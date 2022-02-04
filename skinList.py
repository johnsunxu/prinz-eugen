# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

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
