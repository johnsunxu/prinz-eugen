from discord.ext import commands, menus
import discord
import sys
sys.path.append("./")

from perseus import Perseus, APIError
api = Perseus()

from base_graphics import BaseGraphics

class SkinMenu(menus.Menu):
    def __init__(self, skins) -> None:
        self.embeds = []

        for skin in skins:
            embed = discord.Embed(title=skin["name"], description=skin["description"], color=BaseGraphics.getEmbedColor())
            if "image" in skin:
                embed.set_image(url=skin["image"])
            embed.set_thumbnail(url=skin["chibi"])
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
class ShipArt(commands.Cog):
    #init func
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def art(self, ctx, *args):
        name = ' '.join(args)
        try:
            s = api.Ship(name,nicknames=True)
        except APIError:
            await ctx.channel.send(f"Ship girl {name.title()} does not exist!")
            return

        menu = SkinMenu(s.skins)
        await menu.start(ctx)

def setup(client):
    client.add_cog(ShipArt(client))