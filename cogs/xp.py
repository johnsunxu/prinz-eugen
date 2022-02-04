# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

import discord
import math

from azurlane.azurapi import AzurAPI
from shipGirlNicknameHandler import getNickname


from discord.ext import commands

class Xp(commands.Cog):
    #init
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def xp(self, ctx, shipName, curLevel, stage, mvp = 100): 
        #check if ship exists 
        api = AzurAPI() 

        try: 
            ship = api.getShipByNameEn(ship = shipName)
        except: 
            await ctx.send("Ship does not exist!")
            return
        
        #Check rarity 
        if ship["rarity"] == "Decisive" or ship["rarity"] == "Ultra Rare": 
            xp = shipXPUR
        else: 
            xp = shipXP

        #check backline or not
        if ship["hullType"] == "Aircraft Carrier" or ship["hullType"] == "Light Carrier" or ship["hullType"] == "Battleship"  or ship["hullType"] == "Battlecruiser" or ship["hullType"] == "Aviation Battleship" : 
            flagship = 1.5
        else: 
            flagship = 1
        
        xpRequired = xp[120] - xp[int(curLevel)] 

        sRank = 0.2

        mood = 0.2

        mvp = mvp/100 * 1

        try:
            stage = stageXP[f"{stage.strip()}"]
        except:
            await ctx.send("Stage not supported")
            return

        sortiesRequired = math.ceil(xpRequired / (stage * (1+sRank) * (1+mood) * (1+mvp) * flagship))

        oil = int(ship["stats"]["level120"]["oilConsumption"]) * sortiesRequired

        embed = discord.Embed(color = embedColor, title= "Leveling Information")
        embed.add_field(name = "XP Required", value = f"{int(xpRequired)}", inline = False)
        embed.add_field(name = "Sorties Required", value = f"{sortiesRequired}", inline = False)
        embed.add_field(name = "Oil Requried", value = f"{oil}", inline = False)

        await ctx.send(embed = embed)
    
    #function for calculating calculating xp/sorties/oil required for a ship at a level 

def setup(client):
    client.add_cog(Xp(client))


#Misc vars
embedColor = 0xf01111

stageXP = {
    "2-1": 150.0,
    "3-4": 225.0,
    "6-1": 390.0,
    "6-2": 405.0,
    "6-3": 420.0,
    "6-4": 435.0,
    "7-1": 445.0,
    "7-2": 455.0,
    "7-3": 465.0,
    "7-4": 475.0,
    "8-1": 460.0,
    "8-2": 470.0,
    "8-3": 480.0,
    "8-4": 490.0,
    "9-1": 500.0,
    "9-2": 510.0,
    "9-3": 520.0,
    "9-4": 530.0,
    "10-1": 540.0,
    "10-2": 545.0,
    "10-3": 555.0,
    "10-4": 565.0,
    "11-1": 719.0,
    "11-2": 725.0,
    "11-3": 731.0,
    "11-4": 737.0,
    "12-1": 750.0,
    "12-2": 756.0,
    "12-3": 762.0,
    "12-4": 768.0,
    "13-1": 780.0,
    "13-2": 786.0,
    "13-3": 792.0,
    "13-4": 798.0
}

#numbers are for total xp  
shipXPUR = {
    1: 0,
    2: 120,
    3: 360,
    4: 720,
    5: 1200,
    6: 1800,
    7: 2520,
    8: 3360,
    9: 4320,
    10: 5400,
    11: 6600,
    12: 7920,
    13: 9360,
    14: 10920,
    15: 12600,
    16: 14400,
    17: 16320,
    18: 18360,
    19: 20520,
    20: 22800,
    21: 25200,
    22: 27720,
    23: 30360,
    24: 33120,
    25: 36000,
    26: 39000,
    27: 42120,
    28: 45360,
    29: 48720,
    30: 52200,
    31: 55800,
    32: 59520,
    33: 63360,
    34: 67320,
    35: 71400,
    36: 75600,
    37: 79920,
    38: 84360,
    39: 88920,
    40: 93600,
    41: 98400,
    42: 103440,
    43: 108720,
    44: 114240,
    45: 120000,
    46: 126000,
    47: 132240,
    48: 138720,
    49: 145440,
    50: 152400,
    51: 159600,
    52: 167040,
    53: 174720,
    54: 182640,
    55: 190800,
    56: 199200,
    57: 207840,
    58: 216720,
    59: 225840,
    60: 235200,
    61: 244800,
    62: 254760,
    63: 265080,
    64: 275760,
    65: 286800,
    66: 298200,
    67: 309960,
    68: 322080,
    69: 344560,
    70: 347400,
    71: 360600,
    72: 374280,
    73: 388440,
    74: 403080,
    75: 418200,
    76: 433800,
    77: 449800,
    78: 466440,
    79: 483480,
    80: 501000,
    81: 519000,
    82: 537600,
    83: 556800,
    84: 576600,
    85: 597000,
    86: 618000,
    87: 639600,
    88: 661800,
    89: 684600,
    90: 708000,
    91: 734000,
    92: 761300,
    93: 789900,
    94: 821100,
    95: 854900,
    96: 893900,
    97: 939400,
    98: 991400,
    99: 1069400,
    100: 1241000,
    101: 1325000,
    102: 1411400,
    103: 1500200,
    104: 1591400,
    105: 1685000,
    106: 1787000,
    107: 1903400,
    108: 2034200,
    109: 2179400,
    110: 2339000,
    111: 2513000,
    112: 2708600,
    113: 2925800,
    114: 3164600,
    115: 3425000,
    116: 3707000,
    117: 4014200,
    118: 4346600,
    119: 4704200,
    120: 5087000
}

shipXP = {
    1: 0,
    2: 100,
    3: 300,
    4: 600,
    5: 1000,
    6: 1500,
    7: 2100,
    8: 2800,
    9: 3600,
    10: 4500,
    11: 5500,
    12: 6600,
    13: 7800,
    14: 9100,
    15: 10500,
    16: 12000,
    17: 13600,
    18: 15300,
    19: 17100,
    20: 19000,
    21: 21000,
    22: 23100,
    23: 25300,
    24: 27600,
    25: 30000,
    26: 32500,
    27: 35100,
    28: 37800,
    29: 40600,
    30: 43500,
    31: 46500,
    32: 49600,
    33: 52800,
    34: 56100,
    35: 59500,
    36: 63000,
    37: 66600,
    38: 70300,
    39: 74100,
    40: 78000,
    41: 82000,
    42: 86200,
    43: 90600,
    44: 95200,
    45: 100000,
    46: 105000,
    47: 110200,
    48: 115600,
    49: 121200,
    50: 127000,
    51: 133000,
    52: 139200,
    53: 145600,
    54: 152200,
    55: 159000,
    56: 166000,
    57: 173200,
    58: 180600,
    59: 188200,
    60: 196000,
    61: 204000,
    62: 212300,
    63: 220900,
    64: 229800,
    65: 239000,
    66: 248500,
    67: 258300,
    68: 268400,
    69: 278800,
    70: 289500,
    71: 301600,
    72: 314140,
    73: 327120,
    74: 340540,
    75: 354400,
    76: 368700,
    77: 383440,
    78: 398620,
    79: 414240,
    80: 430300,
    81: 447550,
    82: 465375,
    83: 483775,
    84: 502750,
    85: 522300,
    86: 542425,
    87: 563125,
    88: 584400,
    89: 606250,
    90: 628675,
    91: 652675,
    92: 677875,
    93: 704275,
    94: 733075,
    95: 764275,
    96: 800275,
    97: 842275,
    98: 890275,
    99: 962275,
    100: 1120675,
    101: 1190675,
    102: 1262675,
    103: 1336675,
    104: 1412675,
    105: 1490675,
    106: 1575675,
    107: 1672675,
    108: 1781675,
    109: 1902675,
    110: 2035675,
    111: 2180675,
    112: 2343675,
    113: 2524675,
    114: 2723675,
    115: 2940675,
    116: 3175675,
    117: 3431675,
    118: 3708675,
    119: 4006675,
    120: 4325675.
}
