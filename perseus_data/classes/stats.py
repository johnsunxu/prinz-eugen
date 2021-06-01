import math

class Stats:
    def __init__(self,id,ship):
        self.id = id
        self.ship = ship

    def calculateStat(self,stat):
        index = str(self.ship["id"]*10 + self.limit_break)

        attr = self.ship["data"][index]["stats"][stat]
        attrs_growth = self.ship["data"][index]["stats_growth"][stat]
        attrs_growth_extra = self.ship["data"][index]["stats_growth_extra"][stat]

        #Set defualt affinity_multiplier
        affinity_multiplier = 1

        if (stat != "spd" and stat != "luk"):
            if (self.oathed):
                if (self.affinity < 200):
                    affinity_multiplier = 1.09
                else:
                    affinity_multiplier = 1.12
            elif (self.affinity <= 60):
                affinity_multiplier = 1
            elif (self.affinity <= 80):
                affinity_multiplier = 1.01
            elif (self.affinity <= 99):
                affinity_multiplier = 1.03
            elif (self.affinity <= 100):
                affinity_multiplier = 1.06

        value = attr + (self.level-1)*attrs_growth/1000 + (self.level-100)*(attrs_growth_extra/1000)
        # Add enhancement values to the stat
        if (stat in self.ship["enhancement"]):
            value += self.ship["enhancement"][stat]
        return math.floor(value*affinity_multiplier)

    def getStats(self,level,limit_break,affinity,oathed):

        self.level = level
        self.limit_break = limit_break
        self.affinity = affinity
        self.oathed = oathed

        return {
          "hp": self.calculateStat("hp"),
          "fp": self.calculateStat("fp"),
          "trp": self.calculateStat("trp"),
          "aa": self.calculateStat("aa"),
          "avi": self.calculateStat("avi"),
          "rld": self.calculateStat("rld"),
          "acc": self.calculateStat("acc"),
          "eva": self.calculateStat("eva"),
          "spd": self.calculateStat("spd"),
          "luk": self.calculateStat("luk"),
          "asw": self.calculateStat("asw")
        }
