from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from ..db import db

import os
import telegram
import config
import re

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

        db.autosave(self.scheduler)

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

        channel = self.get_channel(config.STATUS_CHANNEL)
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
            self.scheduler.start()

            channel_status = self.get_channel(config.STATUS_CHANNEL)
            await channel_status.send("I'm now online!")

            self.ready = True
            print("bot ready")
            print(f"Guild: {self.guild}")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if message.channel.id in config.channelIDsToListen and not message.author.bot:
            if "@everyone" in message.content:
                print(f'Message from {message.author}: {message.content}')
                new_message = re.sub('@everyone', '', message.content)
                if new_message is not None:
                    await TG.sendMessage(config.TEL_CHANNEL_ID, new_message)
            else:
                print(f'Message from {message.author}: {message.content}')
                await TG.sendMessage(config.TEL_CHANNEL_ID, message.content)

        if (message.channel.id == config.MAIN_CHAT_CHANNEL or message.channel.id == 1073957627463225454) and not message.author.bot:
            await self.process_commands(message)


bot = Bot()
