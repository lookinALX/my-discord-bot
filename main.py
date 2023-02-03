from discord.ext import tasks
import asyncio
import webserver
import discord
import telegram
import config

tg = telegram.Bot(token=config.TOKEN_TEL)


class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channelIDsToListen = [1069667005491318804, 1070112919846666341]
        if message.channel.id in channelIDsToListen:
            print(f'Message from {message.author}: {message.content}')
            await tg.sendMessage(config.TEL_CHANNEL_ID, message.content)

    async def background_task(self):
        while not self.is_closed():
            print("started")
            await asyncio.sleep(5)


intents = discord.Intents.all()
intents.message_content = True

client = MyBot(intents=intents)
webserver.keep_alive()
client.run(config.TOKEN_DIS)

