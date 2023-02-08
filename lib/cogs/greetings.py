from discord.ext.commands import Cog
from discord import Embed

import config


def create_welcome_message(member):
    welcome_embed = Embed(title="Greetings my friend!", description=f'Добро пожаловать {member.mention}!'
                          , colour=0x66BB55)

    welcome_embed.add_field(name="Присоединяйся в Telegram канал, чтобы видеть все анонсы",
                            value="https://t.me/+eCyurNGK8A4yZDRi", inline=False)

    welcome_embed.add_field(name="Колличество подпивасов в канале: ",
                            value=member.guild.member_count, inline=False)

    welcome_embed.set_author(name="ladAgent", icon_url=member.guild.icon.url)

    return welcome_embed


class Greetings(Cog):
    def __int__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("TEST")

    @Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        print(channel)
        if channel is not None:
            await channel.send("HI")
            await channel.send(embed=create_welcome_message(member))


async def setup(bot):
    await bot.add_cog(Greetings(bot))
