import asyncio
#import webserver
from lib.bot import bot

VERSION = "0.0.5"


async def main():
    await bot.start(VERSION)

#webserver.keep_alive()

asyncio.run(main())
