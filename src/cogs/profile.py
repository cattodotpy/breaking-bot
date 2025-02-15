import discord

from discord.ext import commands
from core.bot import BreakingBot
from core.utils import format_number
from core.ui import base_embed


class Profile(commands.Cog):
    def __init__(self, bot: BreakingBot):
        self.bot = bot

    @commands.command(aliases=["bal", "balance"])
    async def profile(self, ctx: commands.Context, target: discord.Member = None):
        if target is None:
            target = ctx.author
        user = await self.bot.economy.get_user(target.id)
        embed = base_embed()

        embed.title = f"{target.display_name}'s Profile"

        embed.add_field(name="Balance", value=f"$ {format_number(user.balance)}")

        return await ctx.reply(embed=embed)


async def setup(bot: BreakingBot):
    await bot.add_cog(Profile(bot))
