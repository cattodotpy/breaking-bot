import discord

from discord.ext import commands
from core.bot import BreakingBot
from core.converters import NumberConverter, Value
from core.utils import format_number
from core.ui import Confirm, base_embed


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

        user = await self.bot.economy.get_user(ctx.author.id)
        target_user = await self.bot.economy.get_user(target.id)
        async with user.lock, target_user.lock:
            if amount.special == "all":
                amount = user.balance
            elif amount.special == "half":
                amount = user.balance / 2
            else:
                amount = amount.value

            if amount <= 0:
                return await ctx.reply("You can't transfer negative or zero amounts.")

            if user.balance < amount:
                return await ctx.reply("You don't have enough money to transfer.")

            confirm = Confirm()

            confirmation = await ctx.reply(
                embed=base_embed(
                    "Transfer Confirmation",
                    f"Are you sure you want to transfer $ {format_number(amount)} to {target.display_name}?",
                ),
                view=confirm,
            )

            await confirm.wait()

            if not confirm.value:
                # return await ctx.reply("No money for you.")

                return await confirmation.edit(
                    # content=f"Damn, someone changed their mind.",
                    embed=base_embed(
                        "Transfer Cancelled",
                        f"Someone changed their mind about transferring $ {format_number(amount)} to {target.display_name}.",
                    ),
                    view=None,
                )

            await user.remove_balance(amount)
            await target_user.add_balance(amount)

        return await confirmation.edit(
            # content=f"$ {format_number(amount)} transferred to {target.display_name}.",
            embed=base_embed(
                "Transfer Successful",
                f"$ {format_number(amount)} has been transferred to {target.display_name}.",
                discord.Color.green(),
            ),
            view=None,
        )


async def setup(bot: BreakingBot):
    await bot.add_cog(Trading(bot))
