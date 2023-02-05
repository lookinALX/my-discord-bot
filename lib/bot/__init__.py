from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, Embed
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
            print(f"Guild: {self.guild}")

            channel_status = self.get_channel(config.STATUS_CHANNEL)
            await channel_status.send("I'm now online!")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if message.channel.id in config.channelIDsToListen:
            print(f'Message from {message.author}: {message.content}')
            await TG.sendMessage(config.TEL_CHANNEL_ID, message.content)

        if message.channel.id in [1071798085098934363] and message.author != self.user:
            wellcome_embed = Embed(title="Greetings my friend!", description=f'Добро пожаловать {message.author}!',
                                   colour=0x66BB55)

            wellcome_embed.add_field(name="Присоединяйся в Telegram канал, чтобы видеть все анонсы",
                                     value="https://t.me/+eCyurNGK8A4yZDRi", inline=False)

            wellcome_embed.set_author(name="ladAgent", icon_url=self.guild.icon.url)
            channel = self.get_channel(1071798085098934363)
            await channel.send(embed=wellcome_embed)
            await channel.send(f"Нас уже {self.guild.member_count} подпивасов")


bot = Bot()
