"""
Import requirements
"""

from .download import init
from PIL import Image
from io import BytesIO
import requests

#Set up the API class
class Perseus:
    def __init__(self):
        self.initiate()

    def initiate(self,**kwargs):
        init(**kwargs)

        from .ships.ship import Ship
        from .ships.__init__ import ships
        from .gear.gear import Gear
        from .gear.__init__ import gear

        self.Ship = Ship
        self.ship_json = ships
        self.Gear = Gear
        self.gear_json = gear

    def update(self):
        self.initiate()

    def getAllShips(self,*args,**kwargs):
        out = []
        for key in self.ship_json:
            out += [self.Ship(int(key),**kwargs)]
        return out

    def getAllGear(self,*args,**kwargs):
        out = []
        for key in self.gear_json:
            out += [self.Gear(int(key),**kwargs)]
        return out

    def downloadImage(self,url):
        req = requests.get(url)
        if req.status_code == 200:
            return Image.open(BytesIO(req.content))
        else:
            req = requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/master/AzurLaneImages/assets/artresource/atlas/squareicon/unknown.png")
            return Image.open(BytesIO(req.content))
