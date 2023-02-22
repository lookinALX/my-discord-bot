from discord.ext.commands import Cog
from discord.ext.commands import command
from ..db import db
import re
from ..functions import sql


class Сollector(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="tag")
    async def set_tg_user_tag(self, ctx):
        tg_tag = re.findall('(?<=!tag )[\w]+', ctx.message.content)
        if len(tg_tag) < 1 or ('@' in tg_tag):
            await ctx.send(f"Привет {ctx.author.mention}! Пожалуйста напиши свой телеграм тэг c пробелом после "
                           f"команды и без \"@\"")
        else:
            await ctx.send(f"Твой телеграм тэг -> {tg_tag[0]}, я его запомнил")
            sql.insert_tg_tag(ctx.author, tg_tag[0])
            db.commit()

    @command(name="tag-for-user")
    async def set_tg_tag_for_user(self, ctx):
        tg_tag = re.findall('(?<=!tag-for-user )[\w]+', ctx.message.content)
        if len(tg_tag) < 1 or ('@' in tg_tag):
            await ctx.send(f"Привет {ctx.author.mention}! Пожалуйста напиши телеграм тэг c пробелом после "
                           f"команды и без \"@\", затем упомините пользователя")
        else:
            sql.insert_tg_tag(ctx.message.mentions[0], tg_tag[0])
            db.commit()
        
    @command(name="set-ds-id-all")
    async def set_ds_id_for_all(self, ctx):
        guild = ctx.author.guild
        for member in guild.members:
            sql.insert_ds_userid(member)
        db.commit()

    @command(name="set-ds-id")
    async def set_ds_id_for_member(self, ctx):
        users = ctx.message.mentions
        if len(users) < 1:
            await ctx.send("Что-то не так")
        else:
            await ctx.send(f"Я добавил {len(users)} discord ids")
            for user in users:
                sql.insert_ds_userid(user)
                db.commit()


async def setup(bot):
    await bot.add_cog(Сollector(bot))
