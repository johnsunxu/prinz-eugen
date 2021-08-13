import sys
import os
import time
from PIL import Image
import requests
import io
import json
import os
import math


sys.path.append('../src')

#Import the module
from perseus import Perseus

api = Perseus()

ships = api.getAllShips(enhancements=False)

out = []
for ship in ships:
    # print(ship.id)
    if (ship.id in ["10000","10001","10002"]):
        ship.limit_break = 0
    v = {
        "id" : ship.id,
        "retrofit_id" : ship.getRetrofitShipID(),
        "name_en" : ship.name_en,
        "name_cn" : ship.name_cn,
        "name_jp" : ship.name_jp,
        "stats" : [],
        "base_list" : [],
        "skills" : ship.getSkills(),
        "enhancements" : ship.ship["enhancement"],
        "retrofit_nodes" : ship.retrofit_nodes,
        "retrofit_stats" : ship.getRetrofitStats(),
        "hull_id" : ship.hull_id,
        "hull_type" : ship.hull_type,
        "armor_id" : ship.armor_id,
        "armor_type" : ship.armor_type,
        "skins" : ship.skins,
        "stats_growth" : ship.stats_growth,
        "stats_growth_extra" : ship.stats_growth_extra,
        "hunting_range" : ship.hunting_range,
    }

    for count,dataKey in enumerate(ship.ship["data"]):
        ship.limit_break = count
        v["stats"] += [ship.stats]
        v["base_list"] += [ship.ship["data"][dataKey]["base_list"]]



    out += [v]

f = open("all_ships.json",'w',encoding='utf-8')
f.write(json.dumps(out,indent=4,ensure_ascii=False).encode("utf-8").decode())
f.close()