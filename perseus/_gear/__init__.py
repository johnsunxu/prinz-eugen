import json
import os

from .gear import _Gear
from .weapon import _Weapon, _Gun, _Torpedo
from .plane import _Plane, _Armament
from .._util import _API

def gear_from_api(api: _API,gear: int,**kwargs) -> "_Gear":
    res = api._getFromAPI(f"gear/{gear}")
    return gear_by_type(res,**kwargs)

__res_class__ = {
    "cannon" : _Gun,
    "torpedo" : _Torpedo,
    "air" : _Plane
}

def gear_by_type(res,**kwargs):
    return __res_class__.get(res["class_type"],_Gear)(res,**kwargs)
