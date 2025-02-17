import discord

from discord.ext import commands
from core.bot import DeckBot
from core.converters import NumberConverter
from core.utils import format_number


class Developer(commands.Cog):
    def __init__(self, bot: DeckBot):
        self.bot = bot

    @commands.group(aliases=["dev"])
    @commands.is_owner()
    async def developer(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply("Invalid subcommand passed.")

    @developer.command(aliases=["printmoney"])
    async def addbalance(
        self, ctx: commands.Context, target: discord.Member, amount: NumberConverter([])  # type: ignore
    ):
        user = await self.bot.economy.get_user(target.id)

        if user.lock.locked():
            await ctx.reply("User is currently in a transaction.")

        async with user.lock:
            await user.add_balance(amount.value)

        await ctx.reply(
            f"Added $ {format_number(amount.value)} to {target.display_name}'s balance."
        )

    @developer.command(aliases=["give", "devitem"])
    @commands.is_owner()
    async def additem(
        self,
        ctx: commands.Context,
        target: discord.Member,
        item_id: str,
    ):
        user = await self.bot.economy.get_user(target.id)
        item = await self.bot.economy.get_item(item_id)

        if not item:
            return await ctx.reply("Item not found.")

        if user.lock.locked():
            await ctx.reply("User is currently in a transaction.")

        async with user.lock:
            await user.add_item(item)

        await ctx.reply(f"Gave {target.display_name} a {item.name}.")

    @developer.command()
    @commands.is_owner()
    async def createitem(self, ctx: commands.Context, item_id: str, item_name: str):
        item_doc = await self.bot.economy.create_item(item_id, item_name)
        await ctx.reply(f"Created item {item_doc.name} with id {item_doc}.")

    @developer.command()
    async def dump(self, ctx: commands.Context):
        await ctx.reply("Dumping database...")
        self.bot.economy.dump()
        await ctx.reply("Dumped database.")


async def setup(bot: DeckBot):
    await bot.add_cog(Developer(bot))
