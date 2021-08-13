import sys

sys.path.append('../src')
from perseus import Perseus, Lang, Pos
from perseus._ships.skill import Skill

from pprint import pprint

# api = Perseus(url="http://localhost:5000")
api = Perseus(url="http://perseusapi.duckdns.org:5000")

import time

# for s in api.getAllShips():
#     slots = s.slot_ids
#     slots_flattened = [slot for all_in_slot in slots for slot in all_in_slot]
#     if 12 in slots_flattened:
#         print(s.name)

# s = api.Ship("Nagato",nicknames=True)
# ship2 = api.Ship("Taihou")

# print(f"Nagato effects on Taihou {Skill.apply_skill(ship2,[],s.skills[0],pos=Pos.FLAGSHIP)}")
# print(f"Nagato effects on self {Skill.apply_skill(s,[],s.skills[0],pos=Pos.FLAGSHIP)}")

# s = api.Ship("Bremerton")
# print(f"Effects on self (Lead) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.LEADER)}")
# print(f"Effects on self (Center) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.CENTER)}")
# print(f"Effects on self (Rear) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.REAR)}")

# s = api.Ship("San Francisco")
# print(f"Effects on self (Lead) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.LEADER)}")
# print(f"Effects on self (Center) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.CENTER)}")
# print(f"Effects on self (Rear) {Skill.apply_skill(s,[],s.skills[1],pos=Pos.REAR)}")

s = api.Ship("Ardent",retrofit=True,enhancements=True)
print(s.efficiency)
print(s.getFormattedSkills())

# print(s.skills[0]._game_effect)

