import math

class Stats:
    @staticmethod
    def calculateStat(stat,ship):
        index = ship.getRetrofitShipID() * ship._retrofit + ship.id * (not ship._retrofit)
        index = str(int(index)*10 + ship._limit_break)


        attr = ship.ship["data"][index]["stats"][stat]
        attrs_growth = ship.ship["data"][index]["stats_growth"][stat]
        attrs_growth_extra = ship.ship["data"][index]["stats_growth_extra"][stat]

        #Set defualt affinity_multiplier
        affinity_multiplier = 1

        if (stat != "spd" and stat != "luk"):
            if (ship.oathed):
                if (ship.affinity < 200):
                    affinity_multiplier = 1.09
                else:
                    affinity_multiplier = 1.12
            elif (ship.affinity <= 60):
                affinity_multiplier = 1
            elif (ship.affinity <= 80):
                affinity_multiplier = 1.01
            elif (ship.affinity <= 99):
                affinity_multiplier = 1.03
            elif (ship.affinity <= 100):
                affinity_multiplier = 1.06

        value = attr + (ship.level-1)*attrs_growth/1000 + (ship.level-100)*(attrs_growth_extra/1000)
        # Add enhancement values to the stat
        if (stat in ship.ship["enhancement"]):
            value += ship.ship["enhancement"][stat]

        value = math.floor(value*affinity_multiplier)

        #Add retrofit stat boost if retrofit
        if (ship._retrofit):
            retroStats = ship.getRetrofitStats()
            if (stat in retroStats):
                value += retroStats[stat]

        return value


    @staticmethod
    def getStats(ship):
        return {
          "hp": Stats.calculateStat("hp",ship),
          "fp": Stats.calculateStat("fp",ship),
          "trp": Stats.calculateStat("trp",ship),
          "aa":  Stats.calculateStat("aa",ship),
          "avi": Stats.calculateStat("avi",ship),
          "rld": Stats.calculateStat("rld",ship),
          "acc": Stats.calculateStat("acc",ship),
          "eva": Stats.calculateStat("eva",ship),
          "spd": Stats.calculateStat("spd",ship),
          "luk": Stats.calculateStat("luk",ship),
          "asw": Stats.calculateStat("asw",ship)
        }
