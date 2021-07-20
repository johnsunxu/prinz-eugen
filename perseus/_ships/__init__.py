"""
Download constants and open files
This should be rerun when init() is run to refresh the data
"""


import json
import os
from .nicknames import *

#Constants
STAT_KEYWORDS = {
  "durability": "hp",
  "cannon" : "fp",
  "antiaircraft" : "aa",
  "torpedo" : "trp",
  "air" : "avi",
  "reload" : "rld",
  "dodge" : "eva",
  "hit" : "acc"
}

ARMOR_TYPE = {
  1 : "Light",
  2 : "Medium",
  3 : "Heavy"
}

SHIP_LOCATION = {
  1: "Vanguard",
  2: "Vanguard",
  3: "Vanguard",
  4: "Main Fleet",
  5: "Main Fleet",
  6: "Main Fleet",
  7: "Main Fleet",
  8: "Submarine",
  9: "Vanguard",
  10: "Main Fleet",
  11: "Vanguard",
  12: "Main Fleet",
  13: "Main Fleet",
  17: "Submarine",
  18: "Vanguard",
  19: "Vanguard"
}

EQUIP_TYPE_NAME = {
  1 : "DD Gun",
  2 : "CL Gun",
  3 : "CA Gun",
  4 : "BB Gun",
  5 : "Torpedo",
  6 : "AA Gun",
  7 : "Fighter",
  8 : "Torpedo Bomber",
  9 : "Dive Bomber",
  10 : "Auxiliary",
  11 : "CB Gun",
  12 : "Seaplanes",
  13 : "Submarine Torpedo",
  14 : "Auxiliary",
  15 : "ASW Bomber",
  18 : "Cargo"
}