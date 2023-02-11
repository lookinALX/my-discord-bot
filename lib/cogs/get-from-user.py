from discord.ext.commands import Cog
from discord.ext.commands import command
from ..db import db
import re


class Сollector(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="tag")
    async def set_tg_user_tag(self, ctx):
        tg_tag = re.findall('(?<=!tag )[a-z,0-9]+', ctx.message.content)
        if len(tg_tag) < 1 or ('@' in tg_tag):
            await ctx.send(f"Привет {ctx.author.mention}! Пожалуйста напиши свой телеграм тэг c пробелом после "
                           f"команды и без \"@\"")
        else:
            await ctx.send(f"Твой телеграм тэг -> {tg_tag[0]}, я его запомнил")
            db.execute(f"UPDATE user_info SET User_Tel_Tag = ? WHERE UserID = ?", tg_tag[0], ctx.author.id)
            db.commit()

    @command(name="set-ds-id-all")
    async def set_ds_id_for_all(self, ctx):
        guild = ctx.author.guild
        for member in guild.members:
            tmp_none = "None"
            db.execute("INSERT OR IGNORE INTO user_info (UserID, User_Tel_Tag, User_Role) VALUES (?, ?, ?)", member.id,
                       tmp_none, tmp_none)
            print(f"{member.id} was added in the DB")
        db.commit()

    @command(name="set-ds-id")
    async def set_ds_id_for_member(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(Сollector(bot))
