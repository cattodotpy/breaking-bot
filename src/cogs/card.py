import discord

from discord.ext import commands
from core.bot import DeckBot
from core.objects.card import Card
from core.utils import format_interval, format_number
from core.ui import base_embed


class CardCog(commands.Cog):
    def __init__(self, bot: DeckBot):
        self.bot = bot

    @commands.command()
    async def card(self, ctx: commands.Context, id: str = "0"):
        card = Card.get_card(id)

        embed = base_embed(
            title=f"{card.name}",
            description=card.description,
        )

        embed.set_thumbnail(url=card.icon)

        # embed.title = f"{card.name}"
        # embed.add_field(name="Description", value=card.description)
        embed.add_field(name="Rarity", value=card.rarity)

        embed.add_field(name="Attack", value=card.attack)

        embed.add_field(name="Defense", value=card.defense)

        embed.add_field(name="Health", value=card.health)

        embed.add_field(
            name="Reward",
            value=f"{card.reward.amount} {card.reward.item} every {format_interval(card.reward.interval)}",
        )

        embed.add_field(name="Cost", value=card.cost)

        return await ctx.reply(embed=embed)


async def setup(bot: DeckBot):
    await bot.add_cog(CardCog(bot))
