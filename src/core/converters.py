from dataclasses import dataclass
from typing import List
from discord.ext import commands

from core.utils import denumerize


@dataclass
class Value:
    value: float | None = None
    special: str | None = None


def NumberConverter(special_units: List[str] = ["all", "half"]):
    class converter(commands.Converter):
        async def convert(self, _, argument):
            if argument.lower() in special_units:
                return Value(special=argument.lower())
            try:
                number = denumerize(argument)
                return Value(value=number)
            except ValueError:
                raise commands.BadArgument("Invalid number provided.")

    return converter
