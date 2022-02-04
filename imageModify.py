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


try:
    api = AzurAPI()

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

                extra = 'skins/';
                if skinName == 'Default':
                    extra = 'default/'
                elif skinName == 'Retrofit':
                    extra = 'retrofit/'
                #remove banned characters from skin name
                skinName.replace("<",'#1').replace(">",'#2').replace(":",'#3').replace('"','#4').replace("/",'#5').replace("\\",'#6').replace("|",'#7').replace("?",'#8').replace("*",'#9')
                urllib.request.urlretrieve(imageURL, f'cogs/GuessThatShipgirl/ImageNormal/{extra}{name}{skinName}.png');
        except:
            print("Something went wrong");



    for folderName in os.listdir("cogs/GuessThatShipgirl/ImageNormal"):
        for filename in os.listdir(f'cogs/GuessThatShipgirl/ImageNormal/{folderName}'):
            image = Image.open(f"cogs\GuessThatShipgirl\ImageNormal\{folderName}\{filename}") # open colour image
            x = np.array(image)
            r, g, b, a = np.rollaxis(x, axis=-1)
            r[a != 0] = 0;
            g[a != 0] = 0;
            b[a != 0] = 0;
            x = np.dstack([r, g, b, a])

            image = Image.fromarray(x, 'RGBA');
            hName = hash(filename)
            image.save(f'cogs\GuessThatShipgirl\ImageSilhouette\{folderName}\{hName}.png')

except Exception as e:
  print(e)

while (True):
    pass;
