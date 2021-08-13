import os
import json
import math
from .__init__ import STAT_KEYWORDS

EFF_LOC = {
    "equipment_proficiency_1" : 0,
    "equipment_proficiency_2" : 1,
    "equipment_proficiency_3" : 2,
}

class Retrofit:
    def __init__(self):
        pass

    @staticmethod
    def getRetrofitStats(ship):
        '''
        :param ship: ship class to calculate the stats of.
        :return: ships retrofit stats as per documentation.
        '''

        out = {}

        for node in ship.ship["retrofit"]:
            for r in node["effect"]:
                for key in r:
                    if (key in STAT_KEYWORDS):
                        if (STAT_KEYWORDS[key] in out):
                            out[STAT_KEYWORDS[key]] += r[key]
                        else:
                            out[STAT_KEYWORDS[key]] = r[key]
        return out

    @staticmethod
    def getRetrofitEfficiency(ship):
        eff_out = [0,0,0]

        for node in ship.ship["retrofit"]:
            for r in node["effect"]:
                for key in r:
                    if (key in EFF_LOC):
                        eff_out[EFF_LOC[key]] += r[key]
        
        return eff_out

    @staticmethod
    def getRetrofitShipID(ship):
        """
        :param ship: The ship Object
        :return: the ships retrofit ID if it has one. Otherwise returns the original ID.
        """
        try: return str(ship.ship["retrofit_id"]//10)
        except KeyError: return ship.id
