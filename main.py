import webserver
from lib.bot import bot

VERSION = "0.0.2"

webserver.keep_alive()
bot.run(VERSION)