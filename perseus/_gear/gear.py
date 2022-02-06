from functools import lru_cache
from .._util import _API

class _Gear():
    def __init__(self,gear_info,level=10):

        self.gear = gear_info
        self.id = str(gear_info["id"])
        self.level = level
        
    @property
    def name(self):
        return self.name_en

    @property
    def name_en(self):
        try:
            return self.gear["name_EN"]
        except:
            return None

    @property
    def name_jp(self):
        try:
            return self.gear["name_JP"]
        except:
            return None

    @property
    def name_cn(self):
        try:
            return self.gear["name_CN"]
        except:
            return None

    @property
    def rarity(self):
        return self.gear["rarity"]

    @property
    def type_id(self):
        return self.gear["type"]

    @property
    def ship_type_forbidden(self):
        return self.gear["ship_type_forbidden"]

    @property
    def attribute(self):
        return self.gear["attribute"]

    @property
    def icon(self):
        return self.gear["image"]

    @property
    def nationality_id(self):
        return self.gear["nationality"]

    @property
    def equip_limit(self):
        return self.gear["equip_limit"]

    @property
    def stat_boosts(self):
        stats = zip(self.gear["stat_boost_types"], self.gear["stat_boost"][self.level])
        return [stat for stat in stats if stat[0]]