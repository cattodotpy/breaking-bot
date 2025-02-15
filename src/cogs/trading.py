import discord

from discord.ext import commands
from core.bot import BreakingBot
from core.converters import NumberConverter, Value
from core.utils import format_number
from core.ui import Confirm


class Trading(commands.Cog):
    def __init__(self, bot: BreakingBot):
        self.bot = bot

    @commands.command(aliases=["give", "wire"])
    async def transfer(
        self, ctx: commands.Context, target: discord.Member, amount: NumberConverter()  # type: ignore
    ):
        if target.id == ctx.author.id:
            return await ctx.reply("You can't transfer money to yourself.")

        amount: Value = amount

        if amount.value and amount.value <= 0:
            return await ctx.reply("You can't transfer negative or zero amounts.")

        user = await self.bot.economy.get_user(ctx.author.id)
        target_user = await self.bot.economy.get_user(target.id)

        if amount.special == "all":
            amount = user.balance
        elif amount.special == "half":
            amount = user.balance / 2
        else:
            amount = amount.value

        if user.balance < amount:
            return await ctx.reply("You don't have enough money to transfer.")

        confirm = Confirm()

        confirmation = await ctx.reply(
            f"Are you sure you want to transfer $ {format_number(amount)} to {target.display_name}?",
            view=confirm,
        )

        original_amt = user.balance

        async with user.lock, target_user.lock:
            await confirm.wait()

            if not confirm.value:
                # return await ctx.reply("No money for you.")

                return await confirmation.edit(
                    content=f"Damn, someone changed their mind.",
                    view=None,
                )
            if original_amt != user.balance:
                # return await ctx.reply("Someone tried to hack the system, heh")
                return await confirmation.edit(
                    content=f"Someone tried to hack the system, heh.",
                    view=None,
                )
            await user.remove_balance(amount)
            await target_user.add_balance(amount)

        return await confirmation.edit(
            content=f"$ {format_number(amount)} transferred to {target.display_name}.",
            view=None,
        )


async def setup(bot: BreakingBot):
    await bot.add_cog(Trading(bot))
