# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

from discord.ext import commands, menus
import discord
import sys
sys.path.append("./")
from perseus.src.perseus import Perseus, PerseusAPIError
api = Perseus()
from base_graphics import BaseGraphics

class SkillMenu(menus.Menu):
    def __init__(self, skills) -> None:
        self.embeds = []

        for index,skill in enumerate(skills):
            embed = discord.Embed(title=skill["name"], description=skill["description"], color=BaseGraphics.getEmbedColor())
            embed.set_footer(text=f"Skill {index+1}")
            embed.set_thumbnail(url=skill['icon'])
            self.embeds += [embed]

        self.curr = 0

        super().__init__()

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.embeds[0])

    @menus.button('◀️')
    async def on_thumbs_up(self, payload):
        self.curr -= 1
        if self.curr < 0:
            self.curr = len(self.embeds)-1
        await self.message.edit(embed=self.embeds[self.curr])

    @menus.button('▶️')
    async def on_thumbs_down(self, payload):
        self.curr += 1
        if self.curr > len(self.embeds)-1:
            self.curr = 0
        await self.message.edit(embed=self.embeds[self.curr])

#create class
class ShipSkills(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def skills(self, ctx, *args):
        name = ' '.join(args)
        try:
            s = api.Ship(name,nicknames=True)
        except PerseusAPIError:
            await ctx.channel.send(f"Ship girl {name.title()} does not exist!")
            return

        menu = SkillMenu(s.getFormattedSkills())
        await menu.start(ctx)

def setup(client):
    client.add_cog(ShipSkills(client))