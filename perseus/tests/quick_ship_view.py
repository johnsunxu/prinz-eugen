import sys
sys.path.append('../src')
from perseus import Perseus

api = Perseus()

ships = [
    39905

]

out = ""


for ship in ships:
    s = api.Ship(ship)

    this_ship_pretty = s.name_cn+"\n"

    #Stats
    for count,key in enumerate(s.stats.keys()):
        x = count%3
        if x == 0: this_ship_pretty+="\n"
        this_ship_pretty += (key.ljust(3)+": "+str(s.stats[key])).ljust(15)

    this_ship_pretty+="\n\n"

    #limit breaks
    for line in s.limit_break_text["cn"]:
        this_ship_pretty+=line+"\n"

    this_ship_pretty+="\n"

    # this_ship_pretty += str(s.efficiency)+"\n"

    #Skills
    for i in s.getSkills():
        if i["name"] != "Siren Killer Ⅰ":
            this_ship_pretty += i["name"]+"\n"
            this_ship_pretty += i["description"]
        else:
            this_ship_pretty += "Siren Killer\n"
            this_ship_pretty += "Increases own damage dealt to Sirens by 5% (15%)."

        this_ship_pretty += "\n"

    

    print(this_ship_pretty)