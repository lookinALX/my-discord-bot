from discord.ext.commands import Cog
from discord.ext.commands import command
from aiohttp import request


class Fun(Cog):
    def __int__(self, bot):
        self.bot = bot

    @command(name="jokeEN", aliases=['jokeen', 'joke_en'])
    async def give_joke_en(self, ctx):
        URL = "https://icanhazdadjoke.com/"

        async with request("GET", URL, headers={"Accept": "application/json"}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(data["joke"])
            else:
                await ctx.send(f"API returned a {response.status} status")

    @command(name="jokeRU", aliases=['joke', 'joke_ru'])
    async def give_joke_ru(self, ctx):
        URL = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.text()
                data = data.replace("\"", '')
                data = data.replace("content:", '')
                data = data.replace("{", '')
                data = data.replace("}", '')
                await ctx.send(data)
            else:
                await ctx.send(f"API returned a {response.status} status")


async def setup(bot):
    await bot.add_cog(Fun(bot))
