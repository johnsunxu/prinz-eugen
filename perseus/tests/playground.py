import sys
sys.path.append('../src')
from perseus import Perseus
import time

api = Perseus()

def statsToWiki(stats, extend):
    out = ""
    for stat in stats:
        if stat == "hp":
            out += f" | Health{extend} = {stats[stat]}\n"
        elif stat == "fp":
            out += f" | Fire{extend} = {stats[stat]}\n"
        elif stat == "aa":
            out += f" | AA{extend} = {stats[stat]}\n"
        elif stat == "trp":
            out += f" | Torp{extend} = {stats[stat]}\n"
        elif stat == "avi":
            out += f" | Air{extend} = {stats[stat]}\n"
        elif stat == "rld":
            out += f" | Reload{extend} = {stats[stat]}\n"
        elif stat == "eva":
            out += f" | Evade{extend} = {stats[stat]}\n"
        elif stat == "oil":
            out += f" | Consumption{extend} = {stats[stat]}\n"
        elif stat == "asw":
            out += f" | ASW{extend} = {stats[stat]}\n"
        elif stat == "acc":
            out += f" | Acc{extend} = {stats[stat]}\n"

    return out+"\n"

out = ""

s = api.Ship("August von Parseval",retrofit=False)
s.enhancements = False
s.limit_break = 0
s.affinity = 0
s.level = 1
print(s.stats["hp"]+750)
out += statsToWiki(s.stats, "Initial")

s.limit_break = 3
s.enhancements = True
s.affinity = 0
s.level = 100


out += statsToWiki(s.stats, "Max")

s.level = 120
statsToWiki(s.stats, "Max")
out += statsToWiki(s.stats, "120")


print(out)