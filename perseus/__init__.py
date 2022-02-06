"""
Import requirements
"""

from typing import Generator, List
from PIL import Image
from io import BytesIO
import requests
from ._util import Lang, _API
from ._ships.ship import _Ship
from ._ships import Pos
from ._gear import gear_from_api, gear_by_type, _Gear

#Erros so user can catch them
from ._util._erros import PerseusAPIError, PerseusAPIConnectionError, PerseusAPIPathNotFoundError, PerseusAPIReturnError
from perseus._ships import ship

#Set up the API class
class Perseus():
    def __init__(self, url: str="http://perseusapi.duckdns.org:5000"):
        if url.endswith("/"): url = url[:-1]
        self._api = _API(url)

    def Ship(self, ship: str, **kwargs) -> _Ship:
        return _Ship.from_api(self._api,ship,**kwargs)

    def Gear(self, gear: str, **kwargs) -> _Gear:
        return gear_from_api(self._api,gear,**kwargs)

    def getAllShipNames(self,lang: Lang=Lang.EN) -> List[str]:
        return self._api._getFromAPI(f"ship/all_names?{lang=}")

    def getAllShips(self,**kwargs) -> Generator[_Ship,None,None]:
        res = requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/ships/ships.json")
        if res.status_code == 200:
            ships = res.json()
        else:
            raise PerseusAPIError("Could not connect to github")

        for ship_id in ships:
            yield _Ship(ships[ship_id],**kwargs)

    def getAllGear(self,**kwargs) -> Generator[_Gear,None,None]:
        res = requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/gear/gear.json")
        if res.status_code == 200:
            gear = res.json()
        else:
            raise PerseusAPIError("Could not connect to github")

        for gear_id in gear:
            yield gear_by_type(gear[gear_id],**kwargs)

    def downloadImage(self,url: str) -> Image.Image:
        req = requests.get(url)
        if req.status_code == 200:
            return Image.open(BytesIO(req.content))
        else:
            req = requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/master/AzurLaneImages/assets/artresource/atlas/squareicon/unknown.png")
            return Image.open(BytesIO(req.content))
