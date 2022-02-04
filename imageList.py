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
import urllib.request
import string


try:
    import hashlib

    for folderName in os.listdir("cogs/GuessThatShipgirl/ImageNormal"):
        for filename in os.listdir(f'cogs/GuessThatShipgirl/ImageNormal/{folderName}'):
            try:
                image = Image.open(f"cogs\GuessThatShipgirl\ImageNormal\{folderName}\{filename}") # open colour image
                x = np.array(image)
                r, g, b, a = np.rollaxis(x, axis=-1)
                r[a != 0] = 0;
                g[a != 0] = 0;
                b[a != 0] = 0;
                x = np.dstack([r, g, b, a])

                image = Image.fromarray(x, 'RGBA');
                hName = hash(filename)
                image.save(f'cogs\GuessThatShipgirl\ImageSilhouette\{folderName}\{hashlib.sha224(filename.encode("utf-8")).hexdigest()}.png')
            except Exception as e:
                print(e);
except Exception as e:
  print(e)

while (True):
    pass;
