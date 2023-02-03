from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext.commands import Bot as BotBase
import telegram
import config

PREFIX = "+"
OWNER_IDS = [668042075031207947]
TG = telegram.Bot(token=config.TOKEN_TEL)


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

    def run(self, version):
        self.VERSION = version
        self.TOKEN = config.TOKEN_DIS

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(config.GUILD_ID)
            print("bot ready")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if message.channel.id in config.channelIDsToListen:
            print(f'Message from {message.author}: {message.content}')
            await TG.sendMessage(config.TEL_CHANNEL_ID, message.content)


bot = Bot()
