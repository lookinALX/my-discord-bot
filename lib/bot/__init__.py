from glob import glob

from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
import os
import telegram
import config

PREFIX = "!"
OWNER_IDS = [668042075031207947]
TG = telegram.Bot(token=config.TOKEN_TEL)
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Bot(BotBase):
    def __init__(self):
        self.TOKEN = None
        self.VERSION = None
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )

    async def load(self):
        print(os.listdir("./lib/cogs"))
        for cog in COGS:
            await self.load_extension(f"lib.cogs.{cog}")

    async def setup_hook(self) -> None:
        print("loading cogs...")
        await bot.load()

    async def start(self, version):
        self.VERSION = version

        self.TOKEN = config.TOKEN_DIS

        print("running bot...")
        await super().start(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        channel = self.get_channel(1071798085098934363)
        await channel.send("An error occured")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(config.GUILD_ID)

            channel_status = self.get_channel(config.STATUS_CHANNEL)
            await channel_status.send("I'm now online!")

            self.ready = True
            print("bot ready")
            print(f"Guild: {self.guild}")
        else:
            print("bot reconnected")


bot = Bot()
